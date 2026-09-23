# RtG-Preview

**RtG-Preview** is a lightweight browser-based 3D preview renderer for **RtG-Format** builds.

It allows RtG build data to be rendered interactively in a web browser without requiring a separate application. The renderer is designed to work directly with the existing **[RtG-Format](../README.md)** structure and does not introduce a separate build format.

## Features

* Render RtG builds as interactive 3D scenes.
* Load 3D models from the repository's [`assets/models/`](../assets/models/) directory.
* Support multiple objects in the same build.
* Interactive mouse and touch camera controls.
* Keyboard camera movement.
* Gamepad/controller support.
* Background color controls.
* Build statistics panel.
* Error and notification alerts.
* SVG-based interface controls.
* Can be loaded directly from a CDN such as jsDelivr.
* Can be embedded into external HTML pages.
* **Works locally via `file://` protocol** (no local server required).
* **Supports current RtG-Format structure**: connections with `LocalType`, `PrimaryID`, `PrimaryIndex`, UUIDs, `EphemeralAttachments`, CFrames.

## How It Works

RtG-Preview receives a normal **RtG-Format build** and creates a 3D representation of it.

The basic flow is:

```ms
RtG-Format build
       │
       ▼
 RtG-Preview
       │
       ├── Object type → 3D model
       │
       ├── Build data → Scene objects (connections, properties, attachments)
       │
       └── Controls → Interactive camera
       │
       ▼
 Interactive 3D preview
```

The renderer uses the object's internal type name to determine which model should be loaded.

For example:

```ms
"Tooth"
   │
   ▼
assets/models/model/Tooth/Tooth.obj
```

This means that the model filename should correspond to the object's type name.

### Supported Build Structure

RtG-Preview works with the current RtG-Format JSON structure:

```json
[
  ["Type", Connections, Properties],
  ["Type", Connections, Properties]
]
```

Where:
- **Type**: Object type name (e.g., "Part", "Servo", "Connector")
- **Connections**: Array of `[LocalType, PrimaryID, PrimaryIndex]` tuples
  - `LocalType`: Numeric identifier for local connection type
  - `PrimaryID`: Numeric connection point ID or UUID referencing an `EphemeralAttachment`
  - `PrimaryIndex`: 1-based logical index of parent object in the array
- **Properties**: Object properties dictionary, may include `EphemeralAttachments` with CFrames

Example with attachment:

```json
[
  ["Base", [], {"EphemeralAttachments": {"{uuid}": {"partName": "Base", "cframe": [...]}}}],
  ["Sprite", [["1", "{uuid}", 1]], {"ImageId": 12345}]
]
```

## Usage

RtG-Preview exposes a simple global API:

```js
RtGPreview.render(build);
RtGPreview.render(build, { container: HTMLElement });
```

### Fullscreen (default)

The default behavior renders a fullscreen preview attached to `document.body`. This is unchanged from previous versions.

```html
<script src="https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js"></script>

<script>
  RtGPreview.render([
    ["Part", [], {}],
    ["Anchor", [], {}],
    ["Tooth", [], {}]
  ]);
</script>
```

### Embedded (custom container)

Pass a `container` option to mount the preview inside a specific element. The preview will size itself to the container and track its size changes via `ResizeObserver`. This is useful for side panels, drawers, or inline embeds.

```html
<div id="my-preview" style="width: 400px; height: 300px; border: 1px solid #444;"></div>

<script src="https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js"></script>

<script>
  var preview = RtGPreview.render([
    ["Tooth", [], {}],
    ["Fricklet", [], {}]
  ], { container: document.getElementById('my-preview') });

  // Later, when the panel/drawer closes:
  preview.dispose();
</script>
```

**Return value:** `render()` returns a Promise that resolves to an object with a `dispose()` method. Call `dispose()` to clean up the render loop, resize observers, Three.js renderer, and DOM elements. This is required when using a custom container to avoid memory leaks when opening/closing the preview repeatedly.

Replace `COMMIT` with the desired RtG-Format commit.
It is recommended not to add the `COMMIT` if the project hasn't had updates for a long time (like 3 or more days).
For a regular user, the `COMMIT` shouldn't be used.

### Using Multiple Objects

A build can contain multiple objects:

```js
RtGPreview.render([
  ["Tooth", [], {}],
  ["Fricklet", [], {}]
]);
```

Each object is resolved using its RtG object type.

For example:

```md
Tooth     → assets/models/model/Tooth/Tooth.obj
Fricklet  → assets/models/model/Fricklet/Fricklet.obj
```

### With Connections and Attachments

```js
RtGPreview.render([
  ["Base", [], {"EphemeralAttachments": {"{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}": {"partName": "Base", "cframe": [0,0,0, 1,0,0, 0,1,0, 0,0,1]}}}],
  ["Part", [["1", "5", 1]], {"RGB": [255, 0, 0]}],
  ["Sprite", [["1", "{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}", 1]], {"ImageId": 12345}]
]);
```

## Local Usage (file:// protocol)

RtG-Preview can be used directly from the local filesystem without running a web server.

To use locally:

1. Open `RtG-Preview/test-preview.html` directly in your browser, OR
2. Create your own HTML file that includes the required scripts:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>RtG Preview</title>
</head>
<body>
  <!-- Load embedded manifest first (enables file:// support) -->
  <script src="models-manifest.js"></script>
  <!-- Load model registry and preview -->
  <script src="model-registry.js"></script>
  <script src="preview.js"></script>
  <script>
    RtGPreview.render([
      ["Part", [], {}],
      ["Anchor", [], {}],
      ["Tooth", [], {}]
    ]);
  </script>
</body>
</html>
```

**Note**: For local use, you must include `models-manifest.js` before `model-registry.js`. This file contains the embedded model manifest that allows loading models without HTTP requests.

When served via HTTP/HTTPS (CDN, local server, etc.), the manifest is loaded automatically via XHR and `models-manifest.js` is not required.

## Controls

RtG-Preview supports several input methods.

### Mouse

* Drag to rotate the camera.
* Use the available mouse controls to interact with the preview.

### Keyboard

Keyboard controls allow the camera to move around the scene.

* `W` / `S` — Move forward/backward.
* `A` / `D` — Move left/right.
* `Q` / `E` — Move vertically.

Arrow keys can also be used for horizontal camera movement.

### Gamepad

A compatible gamepad can be used for camera movement and rotation.

* Left stick — Camera movement.
* Right stick — Camera rotation.
* `SELECT` — Toggle the preview panel.

### Touch

Touch and pointer input can be used on devices without a physical mouse or keyboard.

## Preview Panel

RtG-Preview includes an optional information panel that can be opened and closed through the interface.

The panel can be toggled using:

* The SVG menu button.
* `F` on a keyboard.
* `SELECT` on a gamepad.

The panel provides information about the currently rendered build.

### Build Statistics

Statistics are calculated when `RtGPreview.render(build)` receives a build.

The panel can display information such as:

* Total blocks.
* Block types.
* Repeated block types.
* Properties.
* Connections.
* Connected blocks.
* Completely unconnected blocks.
* Partially unconnected blocks.
* Connection points.
* UUID information.
* Other build-related information.

Statistics are associated with the loaded build and are **not recalculated every animation frame**.

## Assets

RtG-Preview uses assets stored outside the renderer itself.

### 3D Models

Models are stored in:

[`../assets/models/model/`](../assets/models/model/)

The renderer currently uses Wavefront OBJ models with accompanying JSON metadata.

Example:

```text
assets/models/model/Tooth/Tooth.obj
assets/models/model/Tooth/Tooth.json
assets/models/model/Fricklet/Fricklet.obj
assets/models/model/Fricklet/Fricklet.json
```

Models with branches (e.g., `Switch`, `Splitter_2`, `Gate-AND`, `DoorA-D`) include additional `.obj` files in a `split/` subdirectory.

### Sounds

Interface sounds are stored in:

[`../assets/sounds/`](../assets/sounds/)

These include:

```text
error.mp3
notification.mp3
```

### SVG

Interface graphics are stored in:

[`../assets/svg/`](../assets/svg/)

Current menu icons include:

```text
menu-closed.svg
menu-opened.svg
```

See the main [`assets/README.md`](../assets/README.md) for a complete description of the asset structure.

## External Usage

RtG-Preview is designed to be usable outside the repository.

Because the renderer can be distributed through a CDN, an external HTML page can load a specific version directly.

Example:

```html
<script src="https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js"></script>
```

The build data can then be passed directly to the renderer:

```js
RtGPreview.render([
  ["Tooth", [], {}]
]);
```

This makes it possible for other websites, tools, applications, or services to provide RtG previews without copying the renderer into their own project.

For external CDN usage, the model manifest is loaded automatically via HTTP. No additional setup required.

## Versioning

During development, commit-pinned CDN URLs are recommended:

```text
https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js
```

Using a specific commit makes the loaded renderer deterministic and prevents a test page from unexpectedly changing when the repository is updated.

For example:

```text
@28b7ea34c93663cb37153471c511e442ad1b0033
```

A branch-based URL may be used when always loading the latest version is desired, but commit-pinned URLs are preferred when reproducibility matters.

## Relationship With RtG-Format

RtG-Preview is part of the **RtG-Format** repository.

It does not define an alternative format for builds.

The source of truth for:

* Build structure.
* Object data.
* Connections.
* Properties.
* IDs.
* UUIDs.
* Other RtG-specific data.

remains the RtG-Format specification and implementation in the repository.

RtG-Preview is only responsible for turning that data into an interactive visual representation.

## Development

The main renderer is located at:

```text
RtG-Preview/
├── preview.js
├── model-registry.js
├── models.json (HTTP manifest)
├── models-manifest.js (embedded manifest for file://)
└── test-preview.html
```

Assets used by the renderer are stored under:

```text
assets/
├── models/
│   └── model/
├── sounds/
└── svg/
```

A local test page can be used to verify the renderer:

```text
RtG-Preview/
└── test-preview.html
```

**For local testing**: Open `test-preview.html` directly in your browser (file:// protocol supported).
**For HTTP testing**: Serve the `RtG-Preview` directory and open the served URL.

### Regenerating Model Manifest

When adding or updating models, regenerate the manifest:

```bash
node ../scripts/generate-manifest.js
```

This updates both `models.json` (for HTTP) and `models-manifest.js` (for file://).

## Project Status

RtG-Preview is an evolving component of RtG-Format.

The renderer currently focuses on providing a functional and lightweight 3D preview while progressively adding support for more RtG-specific behavior.

Features that are not yet implemented should not be assumed to be represented visually by the preview.

## Related Documentation

* [`../README.md`](../README.md) — Main RtG-Format documentation.
* [`../assets/README.md`](../assets/README.md) — Documentation for repository assets.
* [`../structure.md`](../structure.md) — Repository structure.
* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current format specification.
* [`../format/`](../format/) — Detailed format documentation.
* [`../examples/`](../examples/) — Build examples.