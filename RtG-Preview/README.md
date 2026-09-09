# RtG-Preview

**RtG-Preview** is a lightweight browser-based 3D preview renderer for **RtG-Format** builds.

It allows RtG build data to be rendered interactively in a web browser without requiring a separate application. The renderer is designed to work directly with the existing **RtG-Format** structure and does not introduce a separate build format.

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

## How It Works

RtG-Preview receives a normal **RtG-Format build** and creates a 3D representation of it.

The basic flow is:

```text
RtG-Format build
       │
       ▼
 RtG-Preview
       │
       ├── Object type → 3D model
       │
       ├── Build data → Scene objects
       │
       └── Controls → Interactive camera
       │
       ▼
 Interactive 3D preview
```

The renderer uses the object's internal type name to determine which model should be loaded.

For example:

```text
"Teeth"
   │
   ▼
assets/models/Teeth.obj
```

This means that the model filename should correspond to the object's type name.

## Usage

RtG-Preview exposes a simple global API:

```js
RtGPreview.render(build);
```

A minimal example:

```html
<script src="https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js"></script>

<script>
  RtGPreview.render([
    ["Teeth", [], {}]
  ]);
</script>
```

Replace `COMMIT` with the desired RtG-Format commit.

## Using Multiple Objects

A build can contain multiple objects:

```js
RtGPreview.render([
  ["Teeth", [], {}],
  ["Fricklet", [], {}]
]);
```

Each object is resolved using its RtG object type.

For example:

```text
Teeth     → assets/models/Teeth.obj
Fricklet  → assets/models/Fricklet.obj
```

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

[`../assets/models/`](../assets/models/)

The renderer currently uses Wavefront OBJ models.

Example:

```text
assets/models/Teeth.obj
assets/models/Fricklet.obj
```

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
  ["Teeth", [], {}]
]);
```

This makes it possible for other websites, tools, applications, or services to provide RtG previews without copying the renderer into their own project.

## Versioning

During development, commit-pinned CDN URLs are recommended:

```text
https://cdn.jsdelivr.net/gh/JuanCrakYT/RtG-Format@COMMIT/RtG-Preview/preview.js
```

Using a specific commit makes the loaded renderer deterministic and prevents a test page from unexpectedly changing when the repository is updated.

For example:

```text
@7b29a02f6da673692abe68af21ffd05bbc72e523
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
└── preview.js
```

Assets used by the renderer are stored under:

```text
assets/
├── models/
├── sounds/
└── svg/
```

A local test page can be used to verify the renderer:

```text
RtG-Preview/
└── test-preview.html
```

When testing changes, it is recommended to use a local HTTP server or an HTTPS/CDN URL rather than opening the HTML file directly with `file://`.

## Project Status

RtG-Preview is an evolving component of RtG-Format.

The renderer currently focuses on providing a functional and lightweight 3D preview while progressively adding support for more RtG-specific behavior.

Features that are not yet implemented should not be assumed to be represented visually by the preview.

## Related Documentation

* [`../README.md`](../README.md) — Main RtG-Format documentation.
* [`../assets/README.md`](../assets/README.md) — Documentation for repository assets.
* [`../structure.md`](../structure.md) — Repository structure.
* [`../src/`](../src/) — RtG-Format source code.
* [`../tests/`](../tests/) — Tests for the project.
