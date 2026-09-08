(function() {
    'use strict';

    var THREE_CDN = 'https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/';
    var previewScriptSrc = document.currentScript ? document.currentScript.src : '';
    var state = null;

    function loadScript(url) {
        return new Promise(function(resolve, reject) {
            var script = document.createElement('script');
            script.src = url;
            script.onload = resolve;
            script.onerror = function() { reject(new Error('Failed to load: ' + url)); };
            document.head.appendChild(script);
        });
    }

    function loadDependencies() {
        return loadScript(THREE_CDN + 'build/three.min.js')
            .then(function() {
                return loadScript(THREE_CDN + 'examples/js/loaders/OBJLoader.js');
            });
    }

    function resolveAssetUrl(type, extension) {
        if (previewScriptSrc) {
            return previewScriptSrc.replace(/\/RtG-Preview\/preview\.js$/, '/') + 'assets/models/' + type + '.' + extension;
        }
        return 'assets/models/' + type + '.' + extension;
    }

    function fitObjectToView(object) {
        var box = new THREE.Box3().setFromObject(object);
        var center = box.getCenter(new THREE.Vector3());
        var size = box.getSize(new THREE.Vector3());
        var maxDim = Math.max(size.x, size.y, size.z);

        if (maxDim === 0) return;

        var targetSize = 3;
        var scale = targetSize / maxDim;

        object.position.set(-center.x, -center.y, -center.z);
        object.scale.set(scale, scale, scale);
    }

    function createScene(container) {
        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a2e);

        var camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 2, 5);

        var renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        var ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        var directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 7);
        scene.add(directionalLight);

        return { scene: scene, camera: camera, renderer: renderer };
    }

    function setupInteraction(container, camera) {
        var isDragging = false;
        var previousPointerPosition = { x: 0, y: 0 };
        var spherical = { theta: 0, phi: Math.PI / 3, radius: 5 };

        function updateCameraPosition() {
            camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.position.y = spherical.radius * Math.cos(spherical.phi);
            camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.lookAt(0, 0, 0);
        }

        container.addEventListener('pointerdown', function(event) {
            isDragging = true;
            previousPointerPosition = { x: event.clientX, y: event.clientY };
            container.setPointerCapture(event.pointerId);
        });

        container.addEventListener('pointermove', function(event) {
            if (!isDragging) return;

            var deltaX = event.clientX - previousPointerPosition.x;
            var deltaY = event.clientY - previousPointerPosition.y;

            spherical.theta -= deltaX * 0.01;
            spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi - deltaY * 0.01));

            updateCameraPosition();
            previousPointerPosition = { x: event.clientX, y: event.clientY };
        });

        container.addEventListener('pointerup', function(event) {
            isDragging = false;
            container.releasePointerCapture(event.pointerId);
        });

        updateCameraPosition();
    }

    function parseBuild(build) {
        if (!Array.isArray(build)) {
            throw new Error('Build must be an array');
        }
        return build.map(function(obj) {
            if (!Array.isArray(obj) || obj.length < 1) {
                throw new Error('Invalid object tuple');
            }
            return {
                type: String(obj[0] || ''),
                connections: Array.isArray(obj[1]) ? obj[1] : [],
                properties: obj[2] && typeof obj[2] === 'object' ? obj[2] : {}
            };
        });
    }

    function loadModel(scene, type) {
        return new Promise(function(resolve, reject) {
            var url = resolveAssetUrl(type, 'obj');
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        var loader = new THREE.OBJLoader();
                        var text = xhr.responseText;
                        text = text.replace(/^mtllib\s+.*$/m, '');
                        var object = loader.parse(text);

                        object.traverse(function(child) {
                            if (child.isMesh) {
                                child.material = new THREE.MeshPhongMaterial({ color: 0xcccccc, flatShading: true });
                            }
                        });

                        fitObjectToView(object);
                        scene.add(object);
                        resolve(object);
                    } else {
                        reject(new Error('HTTP ' + xhr.status + ' for ' + url));
                    }
                }
            };

            xhr.send();
        });
    }

    function clearPrevious() {
        if (state) {
            cancelAnimationFrame(state.animationId);
            window.removeEventListener('resize', state.resizeHandler);
            if (state.container && state.renderer) {
                state.container.removeChild(state.renderer.domElement);
                state.renderer.dispose();
            }
        }
    }

    window.RtGPreview = {
        ready: new Promise(function(resolve) {
            window.RtGPreview._resolveReady = resolve;
        }),

        render: function(build) {
            return window.RtGPreview.ready.then(function() {
                clearPrevious();

                var container = document.createElement('div');
                container.id = 'rtg-preview-container';
                container.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;touch-action:none;';
                document.body.appendChild(container);

                var sceneData = createScene(container);
                var scene = sceneData.scene;
                var camera = sceneData.camera;
                var renderer = sceneData.renderer;

                setupInteraction(container, camera);

                var objects = parseBuild(build);

                var promises = objects.map(function(objData) {
                    return loadModel(scene, objData.type);
                });

                Promise.all(promises).catch(function(err) {
                    console.error('Some models failed to load:', err);
                });

                var resizeHandler = function() {
                    camera.aspect = container.clientWidth / container.clientHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.clientWidth, container.clientHeight);
                };
                window.addEventListener('resize', resizeHandler);

                function animate() {
                    state.animationId = requestAnimationFrame(animate);
                    renderer.render(scene, camera);
                }
                animate();

                state = { container: container, scene: scene, camera: camera, renderer: renderer, animationId: 0, resizeHandler: resizeHandler };
            });
        }
    };

    function bootstrap() {
        loadDependencies()
            .then(function() {
                window.RtGPreview._resolveReady();
            })
            .catch(function(error) {
                console.error('Failed to initialize RtG-Preview:', error);
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootstrap);
    } else {
        bootstrap();
    }
})();
