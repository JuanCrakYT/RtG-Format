(function() {
    'use strict';

    var THREE_CDN = 'https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/';
    var resolveReady = null;
    var rejectReady = null;
    var state = null;

    function fatal(message) {
        try {
            var el = document.createElement('div');
            el.style.cssText = 'position:fixed;top:0;left:0;width:100%;padding:12px;background:#b00020;color:white;font-family:Arial,sans-serif;font-size:14px;z-index:99999;white-space:pre-wrap;';
            el.textContent = 'RtG-Preview: ' + message;
            document.body.appendChild(el);
        } catch (e) {}
        console.error('RtG-Preview: ' + message);
    }

    var alertContainer = null;
    var alertAudioContext = null;

    function resolveSoundUrl(name) {
        var src = '';
        if (document.currentScript && document.currentScript.src) {
            src = document.currentScript.src;
        } else {
            var scripts = document.getElementsByTagName('script');
            for (var i = scripts.length - 1; i >= 0; i--) {
                if (scripts[i].src && scripts[i].src.indexOf('RtG-Preview/preview.js') !== -1) {
                    src = scripts[i].src;
                    break;
                }
            }
        }
        if (!src) {
            return 'assets/sounds/' + name + '.mp3';
        }
        var base = src.replace(/\/RtG-Preview\/preview\.js$/, '/');
        var relative = 'assets/sounds/' + name + '.mp3';
        try {
            return new URL(relative, base).href;
        } catch (e) {
            return relative;
        }
    }

    function playAlertSound(type) {
        try {
            var url = resolveSoundUrl(type === 'error' ? 'error' : 'notification');
            var audio = new Audio(url);
            audio.volume = 0.6;
            audio.play().catch(function() {});
        } catch (e) {}
    }

    function showAlert(message, type) {
        type = type || 'notification';
        playAlertSound(type);

        try {
            if (!alertContainer) {
                alertContainer = document.createElement('div');
                alertContainer.id = 'rtg-preview-alerts';
                alertContainer.style.cssText = 'position:fixed;bottom:0;left:0;max-width:100%;padding:8px;z-index:99999;display:flex;flex-direction:column;gap:6px;pointer-events:none;';
                document.body.appendChild(alertContainer);
            }

            var item = document.createElement('div');
            item.style.cssText = 'pointer-events:auto;padding:10px 12px;border-radius:6px;color:white;font-family:Arial,sans-serif;font-size:13px;opacity:0;transform:translateY(8px);transition:opacity .25s ease,transform .25s ease;';
            item.textContent = message;

            if (type === 'error') {
                item.style.background = 'rgba(176,0,32,0.9)';
            } else {
                item.style.background = 'rgba(30,30,40,0.85)';
            }

            alertContainer.appendChild(item);

            requestAnimationFrame(function() {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            });

            setTimeout(function() {
                item.style.opacity = '0';
                item.style.transform = 'translateY(8px)';
                setTimeout(function() {
                    if (item.parentNode) {
                        item.parentNode.removeChild(item);
                    }
                }, 260);
            }, 4000);
        } catch (e) {
            console.error('RtG-Preview alert error:', e);
        }
    }

    function loadScript(url) {
        return new Promise(function(resolve, reject) {
            var script = document.createElement('script');
            script.src = url;
            script.onload = resolve;
            script.onerror = function() { reject(new Error('Failed to load: ' + url)); };
            document.head.appendChild(script);
        });
    }

    function resolveAssetUrl(type, extension) {
        var src = '';
        if (document.currentScript && document.currentScript.src) {
            src = document.currentScript.src;
        } else {
            var scripts = document.getElementsByTagName('script');
            for (var i = scripts.length - 1; i >= 0; i--) {
                if (scripts[i].src && scripts[i].src.indexOf('RtG-Preview/preview.js') !== -1) {
                    src = scripts[i].src;
                    break;
                }
            }
        }
        if (!src) {
            return 'assets/models/' + type + '.' + extension;
        }
        var base = src.replace(/\/RtG-Preview\/preview\.js$/, '/');
        var relative = 'assets/models/' + type + '.' + extension;
        try {
            return new URL(relative, base).href;
        } catch (e) {
            return relative;
        }
    }

    function fitObjectToView(object) {
        var box = new THREE.Box3().setFromObject(object);
        var center = box.getCenter(new THREE.Vector3());
        var size = box.getSize(new THREE.Vector3());
        var maxDim = Math.max(size.x, size.y, size.z);

        if (!isFinite(maxDim) || maxDim === 0) return;

        var targetSize = 3;
        var scale = targetSize / maxDim;

        object.position.set(-center.x, -center.y, -center.z);
        object.scale.set(scale, scale, scale);
    }

    function frameBuild(camera, objects) {
        var box = new THREE.Box3();
        for (var i = 0; i < objects.length; i++) {
            box.expandByObject(objects[i]);
        }
        if (box.isEmpty()) return new THREE.Vector3(0, 0, 0);

        var center = box.getCenter(new THREE.Vector3());
        var size = box.getSize(new THREE.Vector3());
        var maxDim = Math.max(size.x, size.y, size.z);

        if (!isFinite(maxDim) || maxDim === 0) return center;

        var fov = camera.fov * (Math.PI / 180);
        var distance = maxDim / (2 * Math.tan(fov / 2));
        distance *= 1.8;

        var direction = new THREE.Vector3().copy(camera.position).normalize();
        camera.position.copy(center).add(direction.multiplyScalar(distance));
        camera.lookAt(center);

        return center;
    }

    function createScene(container) {
        var width = container.clientWidth || 1;
        var height = container.clientHeight || 1;

        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0x1a1a2e);

        var camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
        camera.position.set(0, 2, 5);

        var renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(width, height);
        renderer.setPixelRatio(window.devicePixelRatio || 1);
        container.appendChild(renderer.domElement);

        var ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        var directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 7);
        scene.add(directionalLight);

        return { scene: scene, camera: camera, renderer: renderer };
    }

    function setupInteraction(container, camera, target) {
        var isDragging = false;
        var previousPointerPosition = { x: 0, y: 0 };
        var spherical = { theta: 0, phi: Math.PI / 3, radius: 5 };
        var targetPoint = target || new THREE.Vector3(0, 0, 0);
        var moveState = { forward: false, backward: false, left: false, right: false, up: false, down: false };
        var pinchState = { active: false, lastDistance: 0 };
        var gamepadDeadzone = 0.2;

        function getForward() {
            var forward = new THREE.Vector3();
            camera.getWorldDirection(forward);
            return forward.normalize();
        }

        function getRight() {
            var forward = getForward();
            return new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), forward).normalize().multiplyScalar(-1);
        }

        function applyAxis(value) {
            if (Math.abs(value) < gamepadDeadzone) return 0;
            return value;
        }

        function updateFromGamepad() {
            var gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
            var gp = null;
            for (var i = 0; i < gamepads.length; i++) {
                if (gamepads[i]) {
                    gp = gamepads[i];
                    break;
                }
            }
            if (!gp) return;

            moveState.forward = false;
            moveState.backward = false;
            moveState.left = false;
            moveState.right = false;
            moveState.up = false;
            moveState.down = false;

            var lx = applyAxis(gp.axes[0]);
            var ly = applyAxis(gp.axes[1]);
            var rx = applyAxis(gp.axes[2]);
            var ry = applyAxis(gp.axes[3]);

            if (lx > 0.1) moveState.right = true;
            if (lx < -0.1) moveState.left = true;
            if (ly > 0.1) moveState.forward = true;
            if (ly < -0.1) moveState.backward = true;

            if (Math.abs(rx) > gamepadDeadzone) {
                spherical.theta -= rx * 0.03;
            }
            if (Math.abs(ry) > gamepadDeadzone) {
                spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi - ry * 0.03));
            }

            var lt = gp.buttons[6] ? gp.buttons[6].value : 0;
            var rt = gp.buttons[7] ? gp.buttons[7].value : 0;

            if (rt > 0.1) moveState.up = true;
            if (lt > 0.1) moveState.down = true;
        }

        function updateCameraPosition() {
            camera.position.x = targetPoint.x + spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.position.y = targetPoint.y + spherical.radius * Math.cos(spherical.phi);
            camera.position.z = targetPoint.z + spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.lookAt(targetPoint);
        }

        function applyKeyboardMovement() {
            var speed = 0.08;
            var forward = getForward();
            var right = getRight();
            var delta = new THREE.Vector3();

            if (moveState.forward) delta.add(forward);
            if (moveState.backward) delta.sub(forward);
            if (moveState.right) delta.add(right);
            if (moveState.left) delta.sub(right);

            if (moveState.up || moveState.down) {
                var up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion).normalize();
                if (moveState.up) delta.add(up);
                if (moveState.down) delta.sub(up);
            }

            if (delta.length() > 0) {
                delta.normalize().multiplyScalar(speed);
                targetPoint.add(delta);
                updateCameraPosition();
            }
        }

        function getTouchDistance(event) {
            if (event.touches && event.touches.length === 2) {
                var dx = event.touches[0].clientX - event.touches[1].clientX;
                var dy = event.touches[0].clientY - event.touches[1].clientY;
                return Math.sqrt(dx * dx + dy * dy);
            }
            return 0;
        }

        container.addEventListener('pointerdown', function(event) {
            if (event.pointerType === 'touch' && event.isPrimary === false) {
                return;
            }

            if (event.pointerType === 'touch' && getTouchDistance(event) > 0) {
                pinchState.active = true;
                pinchState.lastDistance = getTouchDistance(event);
                return;
            }

            isDragging = true;
            previousPointerPosition = { x: event.clientX, y: event.clientY };
            container.setPointerCapture(event.pointerId);
        });

        container.addEventListener('pointermove', function(event) {
            if (pinchState.active) {
                var distance = getTouchDistance(event);
                if (pinchState.lastDistance > 0 && distance > 0) {
                    var scale = pinchState.lastDistance / distance;
                    spherical.radius = Math.max(0.5, Math.min(50, spherical.radius * scale));
                    updateCameraPosition();
                }
                pinchState.lastDistance = distance;
                return;
            }

            if (!isDragging) return;

            var deltaX = event.clientX - previousPointerPosition.x;
            var deltaY = event.clientY - previousPointerPosition.y;

            spherical.theta -= deltaX * 0.01;
            spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi - deltaY * 0.01));

            updateCameraPosition();
            previousPointerPosition = { x: event.clientX, y: event.clientY };
        });

        container.addEventListener('pointerup', function(event) {
            if (pinchState.active) {
                pinchState.active = false;
                pinchState.lastDistance = 0;
                return;
            }

            isDragging = false;
            container.releasePointerCapture(event.pointerId);
        });

        container.addEventListener('wheel', function(event) {
            event.preventDefault();
            var zoomSpeed = 0.0015;
            spherical.radius = Math.max(0.5, Math.min(50, spherical.radius * (1 + event.deltaY * zoomSpeed)));
            updateCameraPosition();
        }, { passive: false });

        window.addEventListener('keydown', function(event) {
            var key = event.key.toLowerCase();
            if (key === 'w' || key === 'arrowup') moveState.forward = true;
            if (key === 's' || key === 'arrowdown') moveState.backward = true;
            if (key === 'a' || key === 'arrowleft') moveState.left = true;
            if (key === 'd' || key === 'arrowright') moveState.right = true;
            if (key === 'q') moveState.down = true;
            if (key === 'e') moveState.up = true;
        });

        window.addEventListener('keyup', function(event) {
            var key = event.key.toLowerCase();
            if (key === 'w' || key === 'arrowup') moveState.forward = false;
            if (key === 's' || key === 'arrowdown') moveState.backward = false;
            if (key === 'a' || key === 'arrowleft') moveState.left = false;
            if (key === 'd' || key === 'arrowright') moveState.right = false;
            if (key === 'q') moveState.down = false;
            if (key === 'e') moveState.up = false;
        });

        updateCameraPosition();

        function animateWithKeyboard() {
            updateFromGamepad();
            applyKeyboardMovement();
            state.keyboardRAF = requestAnimationFrame(animateWithKeyboard);
        }
        animateWithKeyboard();

        return {
            stop: function() {
                moveState.forward = false;
                moveState.backward = false;
                moveState.left = false;
                moveState.right = false;
                moveState.up = false;
                moveState.down = false;
                pinchState.active = false;
                pinchState.lastDistance = 0;
                if (state.keyboardRAF) {
                    cancelAnimationFrame(state.keyboardRAF);
                }
            }
        };
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
                        try {
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
                        } catch (err) {
                            reject(err);
                        }
                    } else {
                        reject(new Error('HTTP ' + xhr.status + ' for ' + url));
                    }
                }
            };

            xhr.onerror = function() {
                reject(new Error('Network error loading ' + url));
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
            if (state.interaction && state.interaction.stop) {
                state.interaction.stop();
            }
        }
    }

    window.RtGPreview = {
        ready: new Promise(function(resolve, reject) {
            resolveReady = resolve;
            rejectReady = reject;
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

                var objects = parseBuild(build);

                var loadedObjects = [];
                var promises = objects.map(function(objData) {
                    return loadModel(scene, objData.type).then(function(object) {
                        loadedObjects.push(object);
                        return object;
                    }).catch(function(err) {
                        fatal('Failed to load model "' + objData.type + '": ' + err.message);
                        throw err;
                    });
                });

                Promise.all(promises).then(function() {
                    var targetPoint = new THREE.Vector3(0, 0, 0);
                    if (loadedObjects.length > 0) {
                        targetPoint = frameBuild(camera, loadedObjects);
                    }
                    state.interaction = setupInteraction(container, camera, targetPoint);
                }).catch(function(err) {
                    state.interaction = setupInteraction(container, camera);
                });

                var hasPhysicalKeyboard = false;
                try {
                    var mouseCoarse = window.matchMedia('(pointer: coarse)').matches;
                    var hoverNone = window.matchMedia('(hover: none)').matches;
                    var maxTouch = navigator.maxTouchPoints || 0;
                    hasPhysicalKeyboard = !(mouseCoarse && hoverNone && maxTouch > 0);
                } catch (e) {}

                if (!hasPhysicalKeyboard) {
                    showAlert('WASD controls are unavailable on this device. Use touch or mouse to control the camera.', 'notification');
                }

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

                state = { container: container, scene: scene, camera: camera, renderer: renderer, animationId: 0, resizeHandler: resizeHandler, interaction: null };
                animate();
            }).catch(function(err) {
                fatal('Initialization failed: ' + err.message);
            });
        }
    };

    function bootstrap() {
        loadDependencies()
            .then(function() {
                resolveReady();
            })
            .catch(function(error) {
                console.error('Failed to initialize RtG-Preview:', error);
                fatal('Initialization failed: ' + error.message);
                rejectReady(error);
            });
    }

    function loadDependencies() {
        return loadScript(THREE_CDN + 'build/three.min.js')
            .then(function() {
                return loadScript(THREE_CDN + 'examples/js/loaders/OBJLoader.js');
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootstrap);
    } else {
        bootstrap();
    }
})();
