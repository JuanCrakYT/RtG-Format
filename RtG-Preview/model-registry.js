class ModelRegistry {
    constructor(basePath) {
        this.basePath = basePath;
        this.manifest = null;
        this.loaded = new Map();
        this.loading = new Map();
    }

    async loadManifest() {
        if (this.manifest) return this.manifest;
        
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
                    reject(new Error('Failed to load manifest: ' + xhr.status));
                }
            };
            xhr.onerror = () => reject(new Error('Network error loading manifest'));
            xhr.send();
        });
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
        
        // Load JSON metadata
        const jsonUrl = baseUrl + info.json.replace('./', '');
        const modelData = await this._loadJSON(jsonUrl);
        
        // Load main mesh - defaultBranch can be string or array
        var defaultBranch = info.defaultBranch;
        var mainObj = Array.isArray(defaultBranch) ? defaultBranch[0] : defaultBranch;
        const mainObjUrl = baseUrl + mainObj.replace('./', '');
        const mainMesh = await this._loadOBJ(mainObjUrl);
        
        // Apply default material
        this._applyDefaultMaterial(mainMesh);
        
        // Load branches if any (use manifest info which has pre-parsed branch data)
        if (info.hasBranches && info.branches) {
            for (const branch of info.branches) {
                const branchUrl = baseUrl + branch.obj.replace('./', '');
                const branchMesh = await this._loadOBJ(branchUrl);
                this._applyDefaultMaterial(branchMesh);
                
                // Position branch using Branches Start transform
                if (branch.start) {
                    const [pos, rot] = branch.start;
                    branchMesh.position.set(pos[0], pos[1], pos[2]);
                    branchMesh.rotation.set(
                        THREE.MathUtils.degToRad(rot[0]),
                        THREE.MathUtils.degToRad(rot[1]),
                        THREE.MathUtils.degToRad(rot[2])
                    );
                }
                
                // Attach to main mesh
                mainMesh.add(branchMesh);
            }
        }
        
        // Store connection points and metadata
        mainMesh.userData = {
            modelType: type,
            modelData: modelData,
            connectionPoints: modelData.LocalPoints || {},
            branches: info.branches || [],
            size: info.size || 1.0
        };
        
        // Apply model-specific scale
        const scale = info.size || 1.0;
        mainMesh.scale.setScalar(scale);
        
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