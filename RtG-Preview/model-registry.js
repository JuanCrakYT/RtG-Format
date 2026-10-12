// ModelRegistry resolves each model directly from assets/models/model/<type>/.
// No generated index or manifest is required: each build object names its model.
class ModelRegistry {
    constructor(basePath) {
        this.basePath = basePath.endsWith('/') ? basePath : basePath + '/';
        this.loaded = new Map();
        this.loading = new Map();
    }

    async getModel(type) {
        const key = String(type || '').trim();
        if (!key) throw new Error('Model type must be a non-empty string');

        if (this.loaded.has(key)) return this.loaded.get(key).clone(true);
        if (this.loading.has(key)) return (await this.loading.get(key)).clone(true);

        const promise = this._loadModel(key);
        this.loading.set(key, promise);
        try {
            const model = await promise;
            this.loaded.set(key, model);
            return model.clone(true);
        } finally {
            this.loading.delete(key);
        }
    }

    async _loadModel(type) {
        const encodedType = encodeURIComponent(type);
        const modelDir = this.basePath + encodedType + '/';
        const modelData = await this._loadJSON(modelDir + encodedType + '.json');
        if (!modelData || typeof modelData !== 'object' || Array.isArray(modelData)) {
            throw new Error('Invalid model JSON data for "' + type + '"');
        }

        const preview = modelData['RtG-Format']?.['RtG-Preview'] || {};
        const rawSize = preview.Size ?? {};
        const sizeMap = rawSize && typeof rawSize === 'object' && !Array.isArray(rawSize)
            ? rawSize
            : { default: rawSize };

        const applyScale = (object, value, label) => {
            const size = value ?? 1;
            if (Array.isArray(size)) {
                if (size.length !== 3 || size.some(v => !Number.isFinite(Number(v)) || Number(v) < 0)) {
                    throw new Error('Invalid scale for ' + label);
                }
                object.scale.set(Number(size[0]), Number(size[1]), Number(size[2]));
                return;
            }
            const scalar = Number(size);
            if (!Number.isFinite(scalar) || scalar < 0) throw new Error('Invalid scale for ' + label);
            object.scale.setScalar(scalar);
        };

        // Current schema stores Default Branch at the model root. Read the old
        // preview field only as a compatibility fallback for older model files.
        const defaultBranch = modelData['Default Branch']
            ?? preview['Default Branch']
            ?? ['./' + type + '.obj'];
        const mainObj = Array.isArray(defaultBranch) ? defaultBranch[0] : defaultBranch;
        if (typeof mainObj !== 'string' || !mainObj) {
            throw new Error('Invalid Default Branch for model "' + type + '"');
        }

        const mainMesh = await this._loadOBJ(new URL(mainObj, modelDir).href);
        this._applyDefaultMaterial(mainMesh);
        applyScale(mainMesh, sizeMap.default ?? 1, 'model "' + type + '"');

        const branchMap = modelData.Branches && typeof modelData.Branches === 'object'
            ? modelData.Branches
            : {};
        const branchesStart = modelData['Branches Start'] || {};
        const localPoints = modelData.LocalPoints || {};
        const branches = [];

        for (const [pointId, objPath] of Object.entries(branchMap)) {
            if (typeof objPath !== 'string' || !objPath) {
                console.warn('Skipping invalid branch in model "' + type + '" at point ' + pointId);
                continue;
            }

            const branchMesh = await this._loadOBJ(new URL(objPath, modelDir).href);
            this._applyDefaultMaterial(branchMesh);

            const branchKey = objPath.replace(/^\.\//, '');
            const branchScale = sizeMap[objPath] ?? sizeMap[branchKey] ?? sizeMap.default ?? 1;
            applyScale(branchMesh, branchScale, 'branch "' + objPath + '" in "' + type + '"');

            const start = branchesStart[objPath];
            if (start) {
                const position = start[0];
                const rotation = start[1];
                if (!Array.isArray(position) || position.length < 3 ||
                    !Array.isArray(rotation) || rotation.length < 3) {
                    throw new Error('Invalid transform for branch "' + objPath + '" in "' + type + '"');
                }
                branchMesh.position.set(Number(position[0]) || 0, Number(position[1]) || 0, Number(position[2]) || 0);
                branchMesh.rotation.set(
                    THREE.MathUtils.degToRad(Number(rotation[0]) || 0),
                    THREE.MathUtils.degToRad(Number(rotation[1]) || 0),
                    THREE.MathUtils.degToRad(Number(rotation[2]) || 0)
                );
            }

            mainMesh.add(branchMesh);
            branches.push({
                pointId,
                obj: objPath,
                start: start || null,
                connectionPoint: localPoints[pointId] ?? null,
                size: branchScale
            });
        }

        mainMesh.userData = {
            modelType: type,
            modelData,
            connectionPoints: localPoints,
            branches,
            size: sizeMap.default ?? 1
        };
        return mainMesh;
    }

    _loadJSON(url) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'json';
            xhr.onload = () => {
                if (xhr.status < 200 || xhr.status >= 300 || !xhr.response) {
                    reject(new Error('HTTP ' + xhr.status + ' loading model metadata: ' + url));
                    return;
                }
                const data = xhr.response;
                if (!Array.isArray(data) || data.length === 0 || !data[0] || typeof data[0] !== 'object') {
                    reject(new Error('Expected a non-empty JSON array in ' + url));
                    return;
                }
                resolve(data[0]);
            };
            xhr.onerror = () => reject(new Error('Network error loading model metadata: ' + url));
            xhr.send();
        });
    }

    _loadOBJ(url) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const loader = new THREE.OBJLoader();
                        resolve(loader.parse(xhr.responseText.replace(/^mtllib\s+.*$/m, '')));
                    } catch (error) {
                        reject(new Error('Could not parse OBJ "' + url + '": ' + error.message));
                    }
                } else {
                    reject(new Error('HTTP ' + xhr.status + ' loading model geometry: ' + url));
                }
            };
            xhr.onerror = () => reject(new Error('Network error loading model geometry: ' + url));
            xhr.send();
        });
    }

    _applyDefaultMaterial(object) {
        object.traverse(child => {
            if (child.isMesh) {
                child.material = new THREE.MeshPhongMaterial({
                    color: 0xcccccc,
                    flatShading: true
                });
            }
        });
    }
}

window.ModelRegistry = ModelRegistry;
