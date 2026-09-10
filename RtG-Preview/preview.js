(function() {
    'use strict';

    var THREE_CDN = 'https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/';
    var resolveReady = null;
    var rejectReady = null;
    var state = null;
    var panelState = { open: false };
    var uiActive = false;
    var virtualCursor = null;
    var cursorX = 0;
    var cursorY = 0;
    var cursorDrag = { active: false, startX: 0, startY: 0, threshold: 6 };
    var lastInput = 'pointer';


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
            audio.onerror = function() {
                console.error('RtG-Preview: Failed to load sound: ' + url);
            };
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

    function injectGlobalStyle(css) {
        try {
            var style = document.createElement('style');
            style.textContent = css;
            document.head.appendChild(style);
        } catch (e) {}
    }

    injectGlobalStyle('#rtg-preview-panel-scroll::-webkit-scrollbar{display:none} #rtg-preview-panel-scroll{scrollbar-width:none;-ms-overflow-style:none;}');

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

    function resolvePreviewAssetUrl(path) {
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
            return path;
        }
        var base = src.replace(/\/RtG-Preview\/preview\.js$/, '/');
        var relative = path;
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

        createAxesHelper(scene);

        return { scene: scene, camera: camera, renderer: renderer, axesHelper: scene.getObjectByName('rtg-axes-helper') };
    }

    function computeBuildStats(build, loadedObjects) {
        var stats = {
            totalBlocks: 0,
            uniqueTypes: 0,
            blockTypes: {},
            repeatedBlocks: {},
            properties: {},
            repeatedProperties: {},
            propertyValues: {},
            connectionsTotal: 0,
            connectedBlocks: 0,
            completelyUnconnected: [],
            partiallyUnconnected: [],
            connectionPointsUsed: {},
            uuidTotal: 0,
            uuidUnique: 0,
            uuidDuplicates: 0,
            emptyNoConnections: 0,
            emptyNoProperties: 0,
            hierarchyMaxDepth: 0,
            buildSize: null,
            buildCenter: null,
            warnings: []
        };

        if (!Array.isArray(build)) {
            stats.warnings.push('Build is not an array');
            return stats;
        }

        stats.totalBlocks = build.length;
        var types = {};
        var objectsWithConnections = 0;
        var objectsWithoutConnections = 0;
        var objectsWithoutProperties = 0;
        var objectsWithValidConnections = 0;
        var objectsWithInvalidConnections = 0;
        var partialConnectionTypes = {};
        var uuidSet = {};
        var uuidList = [];
        var parentMap = {};

        for (var i = 0; i < build.length; i++) {
            var obj = build[i];
            if (!Array.isArray(obj) || obj.length < 1) continue;

            var type = String(obj[0] || '');
            var connections = Array.isArray(obj[1]) ? obj[1] : [];
            var properties = obj[2] && typeof obj[2] === 'object' ? obj[2] : {};

            types[type] = (types[type] || 0) + 1;

            var hasValidConnection = false;
            var hasInvalidConnection = false;

            if (connections.length === 0) {
                objectsWithoutConnections++;
                stats.completelyUnconnected.push(type);
            } else {
                objectsWithConnections++;
                for (var c = 0; c < connections.length; c++) {
                    var conn = connections[c];
                    if (Array.isArray(conn) && conn.length >= 3) {
                        var primaryIndex = conn[2];
                        var indexValid = false;
                        if (primaryIndex !== null && primaryIndex !== undefined) {
                            var numIndex = Number(primaryIndex);
                            if (Number.isInteger(numIndex) && numIndex >= 1 && numIndex <= build.length) {
                                indexValid = true;
                                parentMap[i + 1] = numIndex;
                            }
                        }

                        if (indexValid) {
                            hasValidConnection = true;
                        } else {
                            hasInvalidConnection = true;
                        }

                        var primaryId = String(conn[1] || '');
                        var uuidRegex = /^\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}$/;
                        var isUuid = uuidRegex.test(primaryId);
                        if (isUuid) {
                            stats.uuidTotal++;
                            uuidList.push(primaryId);
                            uuidSet[primaryId] = (uuidSet[primaryId] || 0) + 1;
                            if (!stats.connectionPointsUsed[primaryId]) {
                                stats.connectionPointsUsed[primaryId] = 0;
                            }
                            stats.connectionPointsUsed[primaryId]++;
                        } else {
                            var pointId = String(primaryId || 'numeric');
                            if (!stats.connectionPointsUsed[pointId]) {
                                stats.connectionPointsUsed[pointId] = 0;
                            }
                            stats.connectionPointsUsed[pointId]++;
                        }
                        stats.connectionsTotal++;
                    }
                }
            }

            if (hasValidConnection) {
                objectsWithValidConnections++;
            }
            if (hasInvalidConnection) {
                objectsWithInvalidConnections++;
            }

            if (Object.keys(properties).length === 0) {
                objectsWithoutProperties++;
            }

            for (var prop in properties) {
                if (!properties.hasOwnProperty(prop)) continue;
                stats.properties[prop] = (stats.properties[prop] || 0) + 1;

                if (!stats.propertyValues[prop]) {
                    stats.propertyValues[prop] = {};
                }
                var val = JSON.stringify(properties[prop]);
                stats.propertyValues[prop][val] = (stats.propertyValues[prop][val] || 0) + 1;
            }
        }

        stats.uniqueTypes = Object.keys(types).length;
        stats.blockTypes = types;
        for (var t in types) {
            if (!types.hasOwnProperty(t)) continue;
            if (types[t] > 1) {
                stats.repeatedBlocks[t] = types[t];
            }
        }

        for (var p in stats.properties) {
            if (!stats.properties.hasOwnProperty(p)) continue;
            if (stats.properties[p] > 1) {
                stats.repeatedProperties[p] = stats.properties[p];
            }
        }

        stats.connectedBlocks = objectsWithValidConnections;
        stats.completelyUnconnected = stats.completelyUnconnected.filter(function(v, i, self) {
            return self.indexOf(v) === i;
        });
        stats.emptyNoConnections = objectsWithoutConnections;
        stats.emptyNoProperties = objectsWithoutProperties;

        for (var i4 = 0; i4 < build.length; i4++) {
            var obj4 = build[i4];
            if (!Array.isArray(obj4) || obj4.length < 1) continue;
            var connections4 = Array.isArray(obj4[1]) ? obj4[1] : [];
            if (connections4.length > 0) {
                var hasValid4 = false;
                var hasInvalid4 = false;
                for (var c4 = 0; c4 < connections4.length; c4++) {
                    var conn4 = connections4[c4];
                    if (Array.isArray(conn4) && conn4.length >= 3) {
                        var pi = conn4[2];
                        var num = Number(pi);
                        if (Number.isInteger(num) && num >= 1 && num <= build.length) {
                            hasValid4 = true;
                        } else {
                            hasInvalid4 = true;
                        }
                    }
                }
                if (hasValid4 && hasInvalid4) {
                    stats.partiallyUnconnected.push(String(obj4[0] || ''));
                }
            }
        }
        stats.partiallyUnconnected = stats.partiallyUnconnected.filter(function(v, i, self) {
            return self.indexOf(v) === i;
        });

        var uniqueUuids = Object.keys(uuidSet);
        stats.uuidUnique = uniqueUuids.length;
        stats.uuidDuplicates = uuidList.length - uniqueUuids.length;
        if (stats.uuidDuplicates > 0) {
            stats.warnings.push('Duplicate UUIDs detected: ' + stats.uuidDuplicates);
        }

        var maxDepth = 0;
        function getDepth(index, visited) {
            if (visited && visited[index]) return 0;
            if (!parentMap[index]) return 1;
            var next = getDepth(parentMap[index], visited ? visited.concat([index]) : [index]);
            return 1 + next;
        }
        for (var idx = 1; idx <= build.length; idx++) {
            var depth = getDepth(idx, []);
            if (depth > maxDepth) maxDepth = depth;
        }
        stats.hierarchyMaxDepth = maxDepth;

        if (loadedObjects && loadedObjects.length > 0) {
            var box = new THREE.Box3();
            for (var o = 0; o < loadedObjects.length; o++) {
                box.expandByObject(loadedObjects[o]);
            }
            if (!box.isEmpty()) {
                var center = box.getCenter(new THREE.Vector3());
                var size = box.getSize(new THREE.Vector3());
                stats.buildCenter = { x: center.x, y: center.y, z: center.z };
                stats.buildSize = { x: size.x, y: size.y, z: size.z };
            }
        }

        return stats;
    }

    function createPanel() {
        var panel = document.createElement('div');
        panel.id = 'rtg-preview-panel';
        panel.style.cssText = 'position:fixed;top:0;left:0;height:100%;width:280px;background:rgba(20,20,30,0.95);color:#e0e0e0;font-family:Arial,sans-serif;font-size:12px;z-index:99998;overflow:hidden;pointer-events:auto;transform:translateX(-100%);transition:transform .2s ease;border-right:1px solid rgba(255,255,255,0.1);';

        var header = document.createElement('div');
        header.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:44px;display:flex;align-items:center;justify-content:flex-start;padding:4px 8px;box-sizing:border-box;z-index:2;';

        var toggle = document.createElement('button');
        toggle.id = 'rtg-preview-panel-toggle';
        toggle.style.cssText = 'background:none;border:none;padding:4px;cursor:pointer;pointer-events:auto;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:6px;background:rgba(20,20,30,0.8);position:fixed;top:8px;left:8px;z-index:100001;';
        toggle.setAttribute('aria-label', 'Toggle panel');

        var toggleImg = document.createElement('img');
        toggleImg.id = 'rtg-preview-panel-toggle-img';
        toggleImg.style.cssText = 'width:20px;height:20px;pointer-events:none;';
        toggleImg.src = resolvePreviewAssetUrl('assets/svg/menu-closed.svg');
        toggleImg.onerror = function() {
            if (!toggleImg.dataset.fallback) {
                toggleImg.dataset.fallback = 'true';
                showAlert('Failed to load SVG icon asset', 'error');
                toggleImg.src = 'data:image/svg+xml;base64,' + btoa('<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><line x1="3" y1="5" x2="21" y2="5"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="19" x2="21" y2="19"/></svg>');
            }
        };
        toggle.appendChild(toggleImg);

        toggle.addEventListener('click', function() {
            togglePanel();
        });
        document.body.appendChild(toggle);

        panel.appendChild(header);

        var scrollContainer = document.createElement('div');
        scrollContainer.id = 'rtg-preview-panel-scroll';
        scrollContainer.style.cssText = 'position:absolute;top:44px;left:0;width:100%;bottom:0;overflow-y:auto;overflow-x:hidden;padding-right:14px;box-sizing:border-box;';
        scrollContainer.innerHTML = '<div id="rtg-preview-stats" style="display:flex;flex-direction:column;gap:8px;"></div>' +
            '<div style="margin-bottom:12px;"><div style="opacity:0.8;margin-bottom:4px;">Background</div>' +
            '<input type="color" id="rtg-preview-bg-color" value="#1a1a2e" style="width:100%;height:28px;border:none;background:none;cursor:pointer;" />' +
            '<button id="rtg-preview-bg-reset" style="margin-top:4px;width:100%;padding:4px;background:rgba(255,255,255,0.1);color:white;border:1px solid rgba(255,255,255,0.2);border-radius:4px;cursor:pointer;font-size:11px;">Reset</button></div>';
        panel.appendChild(scrollContainer);

        var scrollbarTrack = document.createElement('div');
        scrollbarTrack.id = 'rtg-preview-scrollbar-track';
        scrollbarTrack.style.cssText = 'position:absolute;top:44px;right:4px;bottom:4px;width:6px;border-radius:3px;background:rgba(255,255,255,0.08);pointer-events:auto;z-index:3;';

        var scrollbarThumb = document.createElement('div');
        scrollbarThumb.id = 'rtg-preview-scrollbar-thumb';
        scrollbarThumb.style.cssText = 'position:absolute;top:0;left:0;width:100%;min-height:18px;border-radius:3px;background:rgba(255,255,255,0.35);pointer-events:auto;';

        scrollbarTrack.appendChild(scrollbarThumb);
        panel.appendChild(scrollbarTrack);

        document.body.appendChild(panel);

        var statsEl = scrollContainer.querySelector('#rtg-preview-stats');

        var bgInput = scrollContainer.querySelector('#rtg-preview-bg-color');
        var bgReset = scrollContainer.querySelector('#rtg-preview-bg-reset');

        bgInput.addEventListener('input', function() {
            if (state && state.scene) {
                state.scene.background = new THREE.Color(bgInput.value);
            }
        });

        bgReset.addEventListener('click', function() {
            bgInput.value = '#1a1a2e';
            if (state && state.scene) {
                state.scene.background = new THREE.Color(0x1a1a2e);
            }
        });

        scrollContainer.addEventListener('scroll', function() {
            syncArtificialScrollbar();
        });
        scrollbarThumb.addEventListener('pointerdown', function(event) {
            event.preventDefault();
            event.stopPropagation();
            var startY = event.clientY;
            var startTop = parseFloat(scrollbarThumb.style.top || '0');
            function onMove(moveEvent) {
                var dy = moveEvent.clientY - startY;
                var trackHeight = scrollContainer.clientHeight;
                var thumbHeight = scrollbarThumb.offsetHeight;
                var maxTop = trackHeight - thumbHeight;
                var newTop = Math.max(0, Math.min(maxTop, startTop + dy));
                scrollbarThumb.style.top = newTop + 'px';
                var maxScroll = scrollContainer.scrollHeight - scrollContainer.clientHeight;
                scrollContainer.scrollTop = maxScroll > 0 ? (newTop / maxTop) * maxScroll : 0;
            }
            function onUp() {
                window.removeEventListener('pointermove', onMove);
                window.removeEventListener('pointerup', onUp);
            }
            window.addEventListener('pointermove', onMove);
            window.addEventListener('pointerup', onUp);
        });
        scrollbarTrack.addEventListener('pointerdown', function(event) {
            event.preventDefault();
            var rect = scrollbarTrack.getBoundingClientRect();
            var y = event.clientY - rect.top;
            var thumbHeight = scrollbarThumb.offsetHeight;
            var targetTop = y - thumbHeight / 2;
            var trackHeight = scrollContainer.clientHeight;
            var maxTop = trackHeight - thumbHeight;
            var newTop = Math.max(0, Math.min(maxTop, targetTop));
            scrollbarThumb.style.top = newTop + 'px';
            var maxScroll = scrollContainer.scrollHeight - scrollContainer.clientHeight;
            scrollContainer.scrollTop = maxScroll > 0 ? (newTop / maxTop) * maxScroll : 0;
        });

        syncArtificialScrollbar();

        return {
            panel: panel,
            toggle: toggle,
            toggleImg: toggleImg,
            scrollContainer: scrollContainer,
            scrollbarTrack: scrollbarTrack,
            scrollbarThumb: scrollbarThumb,
            bgInput: bgInput,
            setOpen: function(isOpen) {
                panelState.open = isOpen;
                if (isOpen) {
                    panel.style.transform = 'translateX(0)';
                    toggleImg.src = resolvePreviewAssetUrl('assets/svg/menu-closed.svg');
                } else {
                    panel.style.transform = 'translateX(-100%)';
                    toggleImg.src = resolvePreviewAssetUrl('assets/svg/menu-opened.svg');
                }
                updateVirtualCursor();
            },
            updateStats: function(stats) {
                var statsEl = scrollContainer.querySelector('#rtg-preview-stats');
                if (!statsEl) return;
                var html = '';

                html += section('Build', 'Total: ' + stats.totalBlocks + ' | Unique types: ' + stats.uniqueTypes);

                if (stats.totalBlocks > 0) {
                    html += section('Block types', formatCounts(stats.blockTypes));
                    html += section('Repeated blocks', formatCounts(stats.repeatedBlocks) || 'None');
                }

                html += section('Properties', Object.keys(stats.properties).join(', ') || 'None');
                html += section('Repeated properties', formatCounts(stats.repeatedProperties) || 'None');

                if (stats.propertyValues && Object.keys(stats.propertyValues).length > 0) {
                    html += '<div style="opacity:0.8;font-size:11px;margin-top:2px;">Property values</div>';
                    for (var p in stats.propertyValues) {
                        if (!stats.propertyValues.hasOwnProperty(p)) continue;
                        html += '<div style="padding-left:8px;margin-top:2px;">' + escapeHtml(p) + '</div>';
                        for (var v in stats.propertyValues[p]) {
                            if (!stats.propertyValues[p].hasOwnProperty(v)) continue;
                            html += '<div style="padding-left:16px;opacity:0.7;">' + escapeHtml(v) + ' x' + stats.propertyValues[p][v] + '</div>';
                        }
                    }
                }

                html += section('Connections', 'Total: ' + stats.connectionsTotal + '<br/>Connected: ' + stats.connectedBlocks + '<br/>Completely unconnected: ' + stats.completelyUnconnected.length + '<br/>Partially unconnected: ' + stats.partiallyUnconnected.length);
                if (stats.completelyUnconnected.length > 0) {
                    html += '<div style="padding-left:8px;opacity:0.7;">' + escapeHtml(stats.completelyUnconnected.join(', ')) + '</div>';
                }
                if (stats.partiallyUnconnected.length > 0) {
                    html += '<div style="padding-left:8px;opacity:0.7;">' + escapeHtml(stats.partiallyUnconnected.join(', ')) + '</div>';
                }

                if (stats.connectionPointsUsed && Object.keys(stats.connectionPointsUsed).length > 0) {
                    html += section('Connection points', formatCounts(stats.connectionPointsUsed));
                }

                if (stats.uuidTotal > 0) {
                    html += section('UUIDs', 'Total: ' + stats.uuidTotal + '<br/>Unique: ' + stats.uuidUnique + '<br/>Duplicates: ' + stats.uuidDuplicates);
                } else {
                    html += section('UUIDs', 'None');
                }

                if (stats.buildSize) {
                    html += section('Build', 'Size: ' + stats.buildSize.x.toFixed(2) + ' x ' + stats.buildSize.y.toFixed(2) + ' x ' + stats.buildSize.z.toFixed(2) + '<br/>Center: (' + stats.buildCenter.x.toFixed(2) + ', ' + stats.buildCenter.y.toFixed(2) + ', ' + stats.buildCenter.z.toFixed(2) + ')');
                }

                if (stats.hierarchyMaxDepth > 0) {
                    html += section('Hierarchy', 'Max depth: ' + stats.hierarchyMaxDepth);
                }

                html += section('Empty data', 'No connections: ' + stats.emptyNoConnections + '<br/>No properties: ' + stats.emptyNoProperties);

                if (stats.warnings.length > 0) {
                    html += section('Warnings', stats.warnings.join('<br/>'));
                } else {
                    html += section('Warnings', '0');
                }

                statsEl.innerHTML = html;
            }
        };

        function section(title, body) {
            return '<div><div style="opacity:0.8;font-size:11px;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px;">' + escapeHtml(title) + '</div><div style="opacity:1;">' + body + '</div></div>';
        }

        function escapeHtml(text) {
            return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        function formatCounts(obj) {
            var keys = Object.keys(obj);
            if (keys.length === 0) return '';
            var parts = [];
            for (var i = 0; i < keys.length; i++) {
                parts.push(escapeHtml(keys[i]) + ' x' + obj[keys[i]]);
            }
            return parts.join('<br/>');
        }
    }

    function togglePanel() {
        if (!state || !state.panel) return;
        panelState.open = !panelState.open;
        uiActive = panelState.open;
        state.panel.setOpen(panelState.open);
        if (panelState.open && lastInput === 'gamepad') {
            cursorX = window.innerWidth / 2;
            cursorY = window.innerHeight / 2;
        }
        updateVirtualCursor();
    }

    function setPanelOpen(isOpen) {
        if (!state || !state.panel) return;
        panelState.open = isOpen;
        uiActive = isOpen;
        state.panel.setOpen(isOpen);
        if (isOpen && lastInput === 'gamepad') {
            cursorX = window.innerWidth / 2;
            cursorY = window.innerHeight / 2;
        }
        updateVirtualCursor();
    }

    function updateVirtualCursor() {
        if (!virtualCursor) return;
        if (uiActive && lastInput === 'gamepad') {
            virtualCursor.style.display = 'block';
            var panelRect = state.panel.panel.getBoundingClientRect();
            cursorX = Math.max(panelRect.left + 8, Math.min(panelRect.right - 8, cursorX));
            cursorY = Math.max(panelRect.top + 8, Math.min(panelRect.bottom - 8, cursorY));
            virtualCursor.style.left = cursorX + 'px';
            virtualCursor.style.top = cursorY + 'px';
        } else {
            virtualCursor.style.display = 'none';
        }
    }

    function syncArtificialScrollbar() {
        if (!state || !state.panel) return;
        var scrollContainer = state.panel.scrollContainer;
        var thumb = state.panel.scrollbarThumb;
        if (!scrollContainer || !thumb) return;

        var scrollHeight = scrollContainer.scrollHeight;
        var clientHeight = scrollContainer.clientHeight;
        if (scrollHeight <= clientHeight) {
            thumb.style.display = 'none';
            return;
        }
        thumb.style.display = 'block';

        var trackHeight = scrollContainer.clientHeight;
        var thumbHeight = Math.max(18, (clientHeight / scrollHeight) * trackHeight);
        thumb.style.height = thumbHeight + 'px';

        var maxScroll = scrollHeight - clientHeight;
        var maxTop = trackHeight - thumbHeight;
        var top = maxScroll > 0 ? (scrollContainer.scrollTop / maxScroll) * maxTop : 0;
        thumb.style.top = top + 'px';
    }

    function createVirtualCursor() {
        var el = document.createElement('div');
        el.id = 'rtg-preview-virtual-cursor';
        el.style.cssText = 'position:fixed;width:16px;height:16px;border-radius:50%;border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.8);pointer-events:none;z-index:100000;display:none;transform:translate(-50%,-50%);transition:opacity .15s ease;';
        el.innerHTML = '<div style="position:absolute;top:50%;left:50%;width:4px;height:4px;background:white;border-radius:50%;transform:translate(-50%,-50%);"></div>';
        document.body.appendChild(el);
        return el;
    }

    function setupInteraction(container, camera, target) {
        var isDragging = false;
        var previousPointerPosition = { x: 0, y: 0 };
        var spherical = { theta: 0, phi: Math.PI / 3, radius: 5 };
        var targetPoint = target || new THREE.Vector3(0, 0, 0);
        var moveState = { forward: false, backward: false, left: false, right: false, up: false, down: false };
        var gamepadMoveState = { forward: false, backward: false, left: false, right: false, up: false, down: false };
        var pinchState = { active: false, lastDistance: 0 };
        var gamepadDeadzone = 0.2;
        var selectWasPressed = false;
        var shiftPressed = false;
        var yPressed = false;
        var rbPressed = false;

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

            gamepadMoveState.forward = false;
            gamepadMoveState.backward = false;
            gamepadMoveState.left = false;
            gamepadMoveState.right = false;
            gamepadMoveState.up = false;
            gamepadMoveState.down = false;

            lastInput = 'gamepad';

            var lx = applyAxis(gp.axes[0]);
            var ly = applyAxis(gp.axes[1]);
            var rx = applyAxis(gp.axes[2]);
            var ry = applyAxis(gp.axes[3]);

            var lt = gp.buttons[6] ? gp.buttons[6].value : 0;
            var rt = gp.buttons[7] ? gp.buttons[7].value : 0;
            var selectPressed = gp.buttons[8] ? gp.buttons[8].pressed : false;
            var aPressed = gp.buttons[0] ? gp.buttons[0].pressed : false;
            yPressed = gp.buttons[3] ? gp.buttons[3].pressed : false;
            rbPressed = gp.buttons[5] ? gp.buttons[5].pressed : false;

            if (selectPressed && !selectWasPressed) {
                togglePanel();
            }
            selectWasPressed = selectPressed;

            if (!uiActive) {
                if (lx > 0.1) gamepadMoveState.right = true;
                if (lx < -0.1) gamepadMoveState.left = true;
                if (ly > 0.1) gamepadMoveState.backward = true;
                if (ly < -0.1) gamepadMoveState.forward = true;
                if (rt > 0.1) gamepadMoveState.up = true;
                if (lt > 0.1) gamepadMoveState.down = true;

                if (Math.abs(rx) > gamepadDeadzone) {
                    spherical.theta -= rx * 0.03;
                    updateCameraPosition();
                }
                if (Math.abs(ry) > gamepadDeadzone) {
                    spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi - ry * 0.03));
                    updateCameraPosition();
                }
            } else if (state && state.panel) {
                var scrollContainer = state.panel.scrollContainer;
                if (scrollContainer) {
                    var scrollSpeed = 1.2;
                    scrollContainer.scrollTop += ry * scrollSpeed;
                    syncArtificialScrollbar();
                }

                var panelRect = state.panel.panel.getBoundingClientRect();
                var moveSpeedX = 1.2;
                var moveSpeedY = 1.2;
                cursorX += lx * moveSpeedX;
                cursorY += ly * moveSpeedY;
                cursorX = Math.max(panelRect.left + 8, Math.min(panelRect.right - 8, cursorX));
                cursorY = Math.max(panelRect.top + 8, Math.min(panelRect.bottom - 8, cursorY));
                updateVirtualCursor();

                if (aPressed && !cursorDrag.active) {
                    cursorDrag.active = true;
                    cursorDrag.startX = cursorX;
                    cursorDrag.startY = cursorY;
                }
                if (!aPressed) {
                    cursorDrag.active = false;
                }
                if (cursorDrag.active) {
                    var dx = cursorX - cursorDrag.startX;
                    var dy = cursorY - cursorDrag.startY;
                    if (Math.abs(dx) > cursorDrag.threshold || Math.abs(dy) > cursorDrag.threshold) {
                        var el = document.elementFromPoint(cursorX, cursorY);
                        if (el && scrollContainer.contains(el)) {
                            scrollContainer.scrollTop += dy * 1.5;
                            syncArtificialScrollbar();
                        }
                    }
                }
            }
        }

        function updateCameraPosition() {
            camera.position.x = targetPoint.x + spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
            camera.position.y = targetPoint.y + spherical.radius * Math.cos(spherical.phi);
            camera.position.z = targetPoint.z + spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
            camera.lookAt(targetPoint);
        }

        function applyKeyboardMovement() {
            var speed = 0.08;
            if (shiftPressed || yPressed || rbPressed) {
                speed *= 3;
            }
            var forward = getForward();
            var right = getRight();
            var delta = new THREE.Vector3();

            var effectiveMoveState = {
                forward: moveState.forward || (!uiActive && gamepadMoveState.forward),
                backward: moveState.backward || (!uiActive && gamepadMoveState.backward),
                left: moveState.left || (!uiActive && gamepadMoveState.left),
                right: moveState.right || (!uiActive && gamepadMoveState.right),
                up: moveState.up || (!uiActive && gamepadMoveState.up),
                down: moveState.down || (!uiActive && gamepadMoveState.down)
            };

            if (effectiveMoveState.forward) delta.add(forward);
            if (effectiveMoveState.backward) delta.sub(forward);
            if (effectiveMoveState.right) delta.add(right);
            if (effectiveMoveState.left) delta.sub(right);

            if (effectiveMoveState.up || effectiveMoveState.down) {
                var up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion).normalize();
                if (effectiveMoveState.up) delta.add(up);
                if (effectiveMoveState.down) delta.sub(up);
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
            lastInput = 'pointer';
            if (virtualCursor) virtualCursor.style.display = 'none';

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
            if (event.pointerType === 'touch' || isDragging) {
                lastInput = 'pointer';
                if (virtualCursor) virtualCursor.style.display = 'none';
            }

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
            lastInput = 'pointer';
            if (virtualCursor) virtualCursor.style.display = 'none';

            if (pinchState.active) {
                pinchState.active = false;
                pinchState.lastDistance = 0;
                return;
            }

            isDragging = false;
            container.releasePointerCapture(event.pointerId);
        });

        container.addEventListener('wheel', function(event) {
            lastInput = 'pointer';
            if (virtualCursor) virtualCursor.style.display = 'none';
            event.preventDefault();
            var zoomSpeed = 0.0015;
            spherical.radius = Math.max(0.5, Math.min(50, spherical.radius * (1 + event.deltaY * zoomSpeed)));
            updateCameraPosition();
        }, { passive: false });

        window.addEventListener('keydown', function(event) {
            var key = event.key.toLowerCase();
            if (key === 'shift') {
                shiftPressed = true;
                lastInput = 'pointer';
            }
            if (key === 'w' || key === 'arrowup') moveState.forward = true;
            if (key === 's' || key === 'arrowdown') moveState.backward = true;
            if (key === 'a' || key === 'arrowleft') moveState.left = true;
            if (key === 'd' || key === 'arrowright') moveState.right = true;
            if (key === 'q') moveState.down = true;
            if (key === 'e') moveState.up = true;
            if (key === 'f' && !event.repeat) togglePanel();
        });

        window.addEventListener('keyup', function(event) {
            var key = event.key.toLowerCase();
            if (key === 'shift') {
                shiftPressed = false;
                lastInput = 'pointer';
            }
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
                gamepadMoveState.forward = false;
                gamepadMoveState.backward = false;
                gamepadMoveState.left = false;
                gamepadMoveState.right = false;
                gamepadMoveState.up = false;
                gamepadMoveState.down = false;
                shiftPressed = false;
                yPressed = false;
                rbPressed = false;
                pinchState.active = false;
                pinchState.lastDistance = 0;
                selectWasPressed = false;
                if (state.keyboardRAF) {
                    cancelAnimationFrame(state.keyboardRAF);
                }
            }
        };
    }

    function arrangeDisconnectedObjects(objects, loadedObjects, objectMap) {
        if (!loadedObjects || loadedObjects.length === 0) return;

        var connected = {};
        for (var i = 0; i < objects.length; i++) {
            if (objectMap[i] === undefined) continue;
            var obj = objects[i];
            for (var c = 0; c < obj.connections.length; c++) {
                var conn = obj.connections[c];
                if (Array.isArray(conn) && conn.length >= 3) {
                    var idx = Number(conn[2]);
                    if (Number.isInteger(idx) && idx >= 1 && idx <= objects.length) {
                        if (objectMap[idx - 1] !== undefined) {
                            connected[i] = true;
                        }
                    }
                }
            }
        }

        var currentX = 0;
        for (var i = 0; i < objects.length; i++) {
            if (connected[i]) continue;
            if (objectMap[i] === undefined) continue;

            var obj3d = loadedObjects[objectMap[i]];
            var box = new THREE.Box3().setFromObject(obj3d);
            var size = box.getSize(new THREE.Vector3());
            var halfWidth = size.x / 2;

            obj3d.position.x = currentX + halfWidth;
            obj3d.position.y = 0;
            obj3d.position.z = 0;

            currentX += size.x + 1;
        }

        if (currentX > 0) {
            var centerX = (currentX - 1) / 2;
            for (var i = 0; i < objects.length; i++) {
                if (connected[i]) continue;
                if (objectMap[i] === undefined) continue;

                loadedObjects[objectMap[i]].position.x -= centerX;
            }
        }
    }

    function createAxesHelper(scene) {
        var group = new THREE.Group();
        group.name = 'rtg-axes-helper';

        var origin = new THREE.Mesh(
            new THREE.SphereGeometry(0.1, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0xffffff })
        );
        group.add(origin);

        var axisLength = 3;
        var colors = { x: 0xff4444, y: 0x44ff44, z: 0x4444ff };
        var dirs = {
            x: new THREE.Vector3(1, 0, 0),
            y: new THREE.Vector3(0, 1, 0),
            z: new THREE.Vector3(0, 0, 1)
        };

        var letters = { x: 'X', y: 'Y', z: 'Z' };

        for (var axis in dirs) {
            var geometry = new THREE.BufferGeometry();
            var vertices = new Float32Array([0, 0, 0, 0, 0, 0]);
            if (axis === 'x') { vertices[3] = axisLength; vertices[4] = 0; vertices[5] = 0; }
            if (axis === 'y') { vertices[3] = 0; vertices[4] = axisLength; vertices[5] = 0; }
            if (axis === 'z') { vertices[3] = 0; vertices[4] = 0; vertices[5] = axisLength; }
            geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
            var material = new THREE.LineBasicMaterial({ color: colors[axis] });
            var line = new THREE.Line(geometry, material);
            group.add(line);

            var canvas = document.createElement('canvas');
            canvas.width = 64;
            canvas.height = 32;
            var ctx = canvas.getContext('2d');
            ctx.fillStyle = colors[axis] === 0xff4444 ? '#ff4444' : colors[axis] === 0x44ff44 ? '#44ff44' : '#4444ff';
            ctx.font = 'bold 16px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(letters[axis], 32, 16);
            var texture = new THREE.CanvasTexture(canvas);
            var spriteMaterial = new THREE.SpriteMaterial({ map: texture, transparent: true });
            var sprite = new THREE.Sprite(spriteMaterial);
            sprite.position.copy(dirs[axis]).multiplyScalar(axisLength + 0.3);
            sprite.scale.set(0.6, 0.3, 1);
            group.add(sprite);
        }

        scene.add(group);
    }

    function parseBuild(build) {
        if (!Array.isArray(build)) {
            showAlert('Error in build: the build must be an array.', 'error');
            return [];
        }

        var result = [];
        for (var i = 0; i < build.length; i++) {
            var obj = build[i];
            var blockIndex = i + 1;

            if (!Array.isArray(obj)) {
                showAlert('Error in block ' + blockIndex + ': invalid structure, expected an array.', 'error');
                continue;
            }

            var type = obj[0];
            if (type === undefined || type === null || type === '') {
                showAlert('Error in block ' + blockIndex + ': missing or empty type.', 'error');
                continue;
            }
            type = String(type);

            var connections = obj[1];
            if (connections !== undefined && connections !== null) {
                if (!Array.isArray(connections)) {
                    showAlert('Error in block ' + blockIndex + ' (' + type + '): connections must be an array.', 'error');
                    connections = [];
                } else {
                    var validConnections = [];
                    for (var c = 0; c < connections.length; c++) {
                        var conn = connections[c];
                        if (!Array.isArray(conn) || conn.length < 3) {
                            showAlert('Error in block ' + blockIndex + ' (' + type + '): connection ' + (c + 1) + ' has invalid format.', 'error');
                        } else {
                            validConnections.push(conn);
                        }
                    }
                    connections = validConnections;
                }
            } else {
                connections = [];
            }

            var properties = obj[2];
            if (properties !== undefined && properties !== null) {
                if (typeof properties !== 'object' || Array.isArray(properties)) {
                    showAlert('Error in block ' + blockIndex + ' (' + type + '): properties must be an object.', 'error');
                    properties = {};
                }
            } else {
                properties = {};
            }

            result.push({
                type: type,
                connections: connections,
                properties: properties
            });
        }

        return result;
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
            if (state.axesHelper && state.axesHelper.parent) {
                state.axesHelper.parent.remove(state.axesHelper);
            }
            if (state.interaction && state.interaction.stop) {
                state.interaction.stop();
            }
            if (state.panel) {
                try { state.panel.panel.parentNode.removeChild(state.panel.panel); } catch (e) {}
                try { state.panel.toggle.parentNode.removeChild(state.panel.toggle); } catch (e) {}
            }
            if (virtualCursor && virtualCursor.parentNode) {
                virtualCursor.parentNode.removeChild(virtualCursor);
            }
            virtualCursor = null;
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

                var panel = createPanel();
                if (!virtualCursor) {
                    virtualCursor = createVirtualCursor();
                }

                var sceneData = createScene(container);
                var scene = sceneData.scene;
                var camera = sceneData.camera;
                var renderer = sceneData.renderer;

                var objects = parseBuild(build);

                var loadedObjects = [];
                var objectMap = new Array(objects.length);
                var promises = objects.map(function(objData, index) {
                    return loadModel(scene, objData.type).then(function(object) {
                        objectMap[index] = loadedObjects.length;
                        loadedObjects.push(object);
                        return object;
                    }).catch(function(err) {
                        showAlert('Failed to load model: ' + objData.type + '.obj', 'error');
                        objectMap[index] = undefined;
                        return null;
                    });
                });

                Promise.all(promises).then(function() {
                    arrangeDisconnectedObjects(objects, loadedObjects, objectMap);
                    var targetPoint = new THREE.Vector3(0, 0, 0);
                    if (loadedObjects.length > 0) {
                        targetPoint = frameBuild(camera, loadedObjects);
                    }
                    state.interaction = setupInteraction(container, camera, targetPoint);
                }).catch(function(err) {
                    state.interaction = setupInteraction(container, camera);
                });

                var stats = computeBuildStats(build, loadedObjects);
                panel.updateStats(stats);

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

                state = { container: container, scene: scene, camera: camera, renderer: renderer, animationId: 0, resizeHandler: resizeHandler, interaction: null, panel: panel, axesHelper: sceneData.axesHelper };
                animate();
            }).catch(function(err) {
                showAlert('Preview initialization failed: ' + err.message, 'error');
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
                showAlert('Failed to load required libraries: ' + error.message, 'error');
                resolveReady();
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
