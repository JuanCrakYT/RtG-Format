// ModelRegistry - Works both locally (file://) and via HTTP
// Embeds manifest and provides fallback loading for local use

class ModelRegistry {
    constructor(basePath) {
        this.basePath = basePath;
        this.manifest = null;
        this.loaded = new Map();
        this.loading = new Map();
        this.isFileProtocol = window.location.protocol === 'file:';
        this.embeddedManifest = null;
        this.embeddedModels = new Map(); // type -> { json, obj, branchObjs }
    }

    // Load manifest - tries HTTP first, falls back to embedded
    async loadManifest() {
        if (this.manifest) return this.manifest;

        // Try HTTP first
        if (!this.isFileProtocol) {
            try {
                await this._loadManifestHTTP();
                return this.manifest;
            } catch (e) {
                console.warn('HTTP manifest load failed, trying embedded:', e.message);
            }
        }

        // Fall back to embedded manifest
        if (this.embeddedManifest) {
            this.manifest = this.embeddedManifest;
            return this.manifest;
        }

        // Try to load embedded from global (set by inline script)
        if (window.RtGEmbeddedManifest) {
            this.embeddedManifest = window.RtGEmbeddedManifest;
            this.manifest = this.embeddedManifest;
            return this.manifest;
        }

        throw new Error('No model manifest available. For local use, include models-manifest.js before preview.js');
    }

    async _loadManifestHTTP() {
        const manifestUrl = this.basePath.replace(/\/[^/]+$/, '') + '/models.json';
        
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', manifestUrl, true);
            xhr.responseType = 'json';
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300 && xhr.response) {
                    this.manifest = xhr.response;
                    resolve(this.manifest);
                } else {
                    reject(new Error('Failed to load manifest: HTTP ' + xhr.status + ' (' + manifestUrl + ')'));
                }
            };
            xhr.onerror = () => reject(new Error('Network error loading manifest from ' + manifestUrl));
            xhr.send();
        });
    }

    // Set embedded manifest (called by models-manifest.js)
    setEmbeddedManifest(manifest) {
        this.embeddedManifest = manifest;
        this.manifest = manifest;
    }

    // Set embedded model data (called by model data scripts)
    setEmbeddedModel(type, modelData) {
        this.embeddedModels.set(type, modelData);
    }

    getModelInfo(type) {
        if (!this.manifest) return null;
        
        // Try exact match first
        if (this.manifest.models[type]) {
            return this.manifest.models[type];
        }
        
        // Try case-insensitive match
        const lowerType = type.toLowerCase();
        for (const [key, value] of Object.entries(this.manifest.models)) {
            if (key.toLowerCase() === lowerType) {
                return value;
            }
        }
        
        return null;
    }

    async getModel(type) {
        if (this.loaded.has(type)) {
            return this.loaded.get(type).clone(true);
        }
        
        if (this.loading.has(type)) {
            return this.loading.get(type);
        }
        
        const promise = this._loadModel(type);
        this.loading.set(type, promise);
        
        try {
            const model = await promise;
            this.loaded.set(type, model);
            return model.clone(true);
        } finally {
            this.loading.delete(type);
        }
    }

    async _loadModel(type) {
        const info = this.getModelInfo(type);
        if (!info) {
            throw new Error('Model not found in manifest: ' + type);
        }

        const baseUrl = this.basePath + info.folder + '/';

        // Embedded model lookup is case-insensitive, just like getModelInfo().
        let embedded = this.embeddedModels.get(type);
        if (!embedded) {
            const requestedType = type.toLowerCase();
            for (const [key, value] of this.embeddedModels.entries()) {
                if (key.toLowerCase() === requestedType) {
                    embedded = value;
                    break;
                }
            }
        }

        // Load the model JSON. It is the source of truth for model metadata.
        let modelData;
        if (embedded && embedded.json) {
            modelData = Array.isArray(embedded.json) ? embedded.json[0] : embedded.json;
        } else {
            const jsonUrl = baseUrl + String(info.json || ('./' + info.folder + '.json')).replace(/^\.\//, '');
            modelData = await this._loadJSON(jsonUrl);
        }

        if (!modelData || typeof modelData !== 'object' || Array.isArray(modelData)) {
            throw new Error('Invalid model JSON data for ' + type);
        }

        const preview = modelData['RtG-Format']?.['RtG-Preview'] || {};
        const rawSizeMap = preview.Size ?? {};
        const sizeMap = rawSizeMap && typeof rawSizeMap === 'object' && !Array.isArray(rawSizeMap)
            ? rawSizeMap
            : { default: rawSizeMap };

        // Size values can be a scalar or a [x, y, z] scale vector.
        const applyScale = (object, rawSize, label) => {
            const size = rawSize ?? 1;

            if (Array.isArray(size)) {
                if (
                    size.length !== 3 ||
                    size.some(value => !Number.isFinite(Number(value)) || Number(value) < 0)
                ) {
                    throw new Error('Invalid scale for ' + label);
                }

                object.scale.set(
                    Number(size[0]),
                    Number(size[1]),
                    Number(size[2])
                );
                return;
            }

            const scalar = Number(size);
            if (!Number.isFinite(scalar) || scalar < 0) {
                throw new Error('Invalid scale for ' + label);
            }

            object.scale.setScalar(scalar);
        };

        // Default Branch is a root-level field in the current RtG JSON schema.
        const defaultBranch = modelData['Default Branch'] ?? info.defaultBranch ?? ['./' + info.folder + '.obj'];
        const mainObj = Array.isArray(defaultBranch) ? defaultBranch[0] : defaultBranch;

        if (typeof mainObj !== 'string' || !mainObj) {
            throw new Error('Invalid Default Branch for model ' + type);
        }

        let mainMesh;
        if (embedded && embedded.obj) {
            mainMesh = this._parseOBJ(embedded.obj);
        } else {
            const mainObjUrl = baseUrl + mainObj.replace(/^\.\//, '');
            mainMesh = await this._loadOBJ(mainObjUrl);
        }

        this._applyDefaultMaterial(mainMesh);
        applyScale(mainMesh, sizeMap.default ?? info.size ?? 1, 'model ' + type);

        // Branches, Branches Start and LocalPoints are root-level JSON fields.
        // Always derive them from the current JSON, not a potentially stale manifest.
        const branchMap = modelData.Branches && typeof modelData.Branches === 'object'
            ? modelData.Branches
            : {};
        const branchesStart = modelData['Branches Start'] || {};
        const localPoints = modelData.LocalPoints || {};

        const modelBranches = Object.entries(branchMap).map(([pointId, obj]) => ({
            pointId,
            obj,
            start: branchesStart[obj] ?? null,
            connectionPoint: localPoints[pointId] ?? null,
            size: sizeMap[obj] ?? sizeMap['./' + String(obj).replace(/^\.\//, '')] ?? sizeMap.default ?? 1
        }));

        for (const branch of modelBranches) {
            if (typeof branch.obj !== 'string' || !branch.obj) {
                console.warn('Skipping invalid branch in model ' + type, branch);
                continue;
            }

            const branchKey = branch.obj.replace(/^\.\//, '');
            let branchMesh;

            if (embedded && embedded.branchObjs && embedded.branchObjs[branchKey]) {
                branchMesh = this._parseOBJ(embedded.branchObjs[branchKey]);
            } else {
                branchMesh = await this._loadOBJ(baseUrl + branchKey);
            }

            this._applyDefaultMaterial(branchMesh);

            const branchSize =
                sizeMap[branch.obj] ??
                sizeMap['./' + branchKey] ??
                branch.size ??
                sizeMap.default ??
                1;
            applyScale(branchMesh, branchSize, 'branch "' + branch.obj + '" in ' + type);

            if (branch.start) {
                const [pos, rot] = branch.start;

                if (
                    !Array.isArray(pos) || pos.length < 3 ||
                    !Array.isArray(rot) || rot.length < 3
                ) {
                    throw new Error('Invalid transform for branch "' + branch.obj + '" in ' + type);
                }

                branchMesh.position.set(
                    Number(pos[0]) || 0,
                    Number(pos[1]) || 0,
                    Number(pos[2]) || 0
                );
                branchMesh.rotation.set(
                    THREE.MathUtils.degToRad(Number(rot[0]) || 0),
                    THREE.MathUtils.degToRad(Number(rot[1]) || 0),
                    THREE.MathUtils.degToRad(Number(rot[2]) || 0)
                );
            }

            mainMesh.add(branchMesh);
        }

        mainMesh.userData = {
            modelType: type,
            modelData,
            connectionPoints: localPoints,
            branches: modelBranches,
            size: sizeMap.default ?? info.size ?? 1
        };

        return mainMesh;
    }

    async _loadJSON(url) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'json';
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300 && xhr.response) {
                    const arr = xhr.response;
                    if (Array.isArray(arr) && arr.length > 0) {
                        resolve(arr[0]);
                    } else {
                        reject(new Error('Invalid model JSON format'));
                    }
                } else {
                    reject(new Error('HTTP ' + xhr.status + ' for ' + url));
                }
            };
            xhr.onerror = () => reject(new Error('Network error loading ' + url));
            xhr.send();
        });
    }

    async _loadOBJ(url) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = () => {
                if (xhr.status === 200) {
                    try {
                        const loader = new THREE.OBJLoader();
                        const text = xhr.responseText.replace(/^mtllib\s+.*$/m, '');
                        const object = loader.parse(text);
                        resolve(object);
                    } catch (err) {
                        reject(err);
                    }
                } else {
                    reject(new Error('HTTP ' + xhr.status + ' for ' + url));
                }
            };
            xhr.onerror = () => reject(new Error('Network error loading ' + url));
            xhr.send();
        });
    }

    _parseOBJ(text) {
        const loader = new THREE.OBJLoader();
        const cleaned = text.replace(/^mtllib\s+.*$/m, '');
        return loader.parse(cleaned);
    }

    _applyDefaultMaterial(object) {
        object.traverse((child) => {
            if (child.isMesh) {
                child.material = new THREE.MeshPhongMaterial({ 
                    color: 0xcccccc, 
                    flatShading: true 
                });
            }
        });
    }
}

// Make available globally
window.ModelRegistry = ModelRegistry;