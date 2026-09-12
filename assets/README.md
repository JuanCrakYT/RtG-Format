# Assets

This directory contains the visual and media assets used by **RtG-Format**, including project branding, logos, banners, 3D models, interface graphics, and audio used by **RtG-Preview**.

## Directory Structure

```tree
assets/
├─ images/
│  ├─ logo/
│  │  ├─ official-banners/
│  │  │  ├─ RtG-1.webp
│  │  │  ├─ RtG-2.webp
│  │  │  ├─ RtG-3.webp
│  │  │  ├─ RtG-4.webp
│  │  │  └─ RtG-5.webp
│  │  ├─ versions/
│  │  │  ├─ shape-v1/
│  │  │  │  └─ RtG-Format-Shape-ToFInish.png
│  │  │  └─ v1/
│  │  │     ├─ RtG-Format-v1.png
│  │  │     └─ RtG-Format-v1.svg
│  │  ├─ RtG-Format-Background.svg
│  │  ├─ RtG-Format-Shape-light.svg
│  │  ├─ RtG-Format-Shape.svg
│  │  ├─ RtG-Format.png
│  │  └─ RtG-Format.svg
│  ├─ banner.jpeg
│  ├─ banner.png
│  ├─ banner.svg
│  └─ RtG.png
├─ models/
│  ├─ AltitudeSensor/
│  ├─ Anchor/
│  ├─ Arm/
│  ├─ Balloon/
│  ├─ BallSocket/
│  ├─ Banjo/
│  ├─ Base/
│  ├─ BeachBall/
│  ├─ Bearing/
│  ├─ Board/
│  ├─ Body/
│  ├─ BouncyBall/
│  ├─ BowlingBall/
│  ├─ BrakeLight/
│  ├─ Briefcase/
│  ├─ Bumper/
│  ├─ Button/
│  ├─ Camera/
│  ├─ Canister/
│  ├─ Cannon/
│  ├─ CannonBall/
│  ├─ Carrot/
│  ├─ Chassis/
│  ├─ Cinderblock/
│  ├─ Connector/
│  ├─ ConnectorBall/
│  ├─ Delayer/
│  ├─ Detacher/
│  ├─ DoorA/
│  ├─ DoorB/
│  ├─ DoorC/
│  ├─ DoorD/
│  ├─ Drumkit/
│  ├─ EntitySensor/
│  ├─ FishBowl/
│  ├─ Fricklet/
│  ├─ FuelTank/
│  ├─ GasCap/
│  ├─ Gate-AND/
│  ├─ Gate-NOT/
│  ├─ Gate-OR/
│  ├─ GoldPotatoEngine/
│  ├─ Googie/
│  ├─ Gramby/
│  ├─ Grenade/
│  ├─ Guitar/
│  ├─ Gun/
│  ├─ Gyro/
│  ├─ HalfConnectorBall/
│  ├─ Head/
│  ├─ Hood/
│  ├─ InputSensor/
│  ├─ Joint/
│  ├─ Joust/
│  ├─ Jug/
│  ├─ Keyboard/
│  ├─ Leafblower/
│  ├─ Leg/
│  ├─ Light/
│  ├─ Lock/
│  ├─ LongStick/
│  ├─ Looper/
│  ├─ Mag/
│  ├─ MatchingGyro/
│  ├─ MountedGun/
│  ├─ Part/
│  ├─ Pie/
│  ├─ Pipes/
│  ├─ Piston/
│  ├─ Plunger/
│  ├─ Poop/
│  ├─ PotatoEngine/
│  ├─ PressurePlate/
│  ├─ Propeller/
│  ├─ Radio/
│  ├─ Ramp/
│  ├─ Recorder/
│  ├─ RemoteButton/
│  ├─ RiotShield/
│  ├─ Rocket/
│  ├─ RockingChair/
│  ├─ Roof/
│  ├─ Rope/
│  ├─ RPG/
│  ├─ RubberBand/
│  ├─ Seat/
│  ├─ Servo/
│  ├─ Servo_Physics/
│  ├─ ShoppingCart/
│  ├─ ShortStick/
│  ├─ Shotgun/
│  ├─ Sledge/
│  ├─ Splitter/
│  ├─ Splitter_1/
│  ├─ Splitter_2/
│  ├─ Splitter_3/
│  ├─ Splitter_4/
│  ├─ SprayPaint/
│  ├─ SpringJuice/
│  ├─ StaringGyro/
│  ├─ SteeringGyro/
│  ├─ SteeringWheel/
│  ├─ Stick/
│  ├─ SuperPowerClock/
│  ├─ Switch/
│  ├─ Thruster/
│  ├─ Tire/
│  ├─ ToolGun/
│  ├─ Tooth/
│  ├─ TripWire/
│  ├─ Trowel/
│  ├─ Trumpet/
│  ├─ Trunk/
│  ├─ TV/
│  ├─ Uzi/
│  ├─ VelocitySensor/
│  ├─ wad/
│  ├─ Wheel/
│  ├─ Wing/
│  ├─ Wire/
│  │
│  ├─ ALL.blend
│  ├─ ALL.blend1
│  ├─ blend_json.py
│  ├─ blend.py
│  └─ README.md
├─ sounds/
│  ├─ error.mp3
│  ├─ notification.mp3
│  ├─ slider.mp3
│  └─ tap.mp3
├─ svg/
│  ├─ menu-closed_light.svg
│  ├─ menu-closed.svg
│  ├─ menu-opened_light.svg
│  └─ menu-opened.svg
└─ README.md
```

## Images

The [`images/`](images/) directory contains visual resources used throughout the repository.

### Banners

The root-level banner files are general project banner assets:

* [`banner.svg`](images/banner.svg) — SVG banner asset.
* [`banner.png`](images/banner.png) — PNG version of the banner.
* [`banner.jpeg`](images/banner.jpeg) — JPEG version of the banner.

### Current RtG-Format Logo

The current project logo is maintained in [`images/logo/`](images/logo/).

* [`RtG-Format.svg`](images/logo/RtG-Format.svg) — Main vector version of the RtG-Format logo.
* [`RtG-Format.png`](images/logo/RtG-Format.png) — Raster version of the RtG-Format logo.
* [`RtG-Format-Shape.svg`](images/logo/RtG-Format-Shape.svg) — Logo shape/isotype without the full wordmark.
* [`RtG-Format-Background.svg`](images/logo/RtG-Format-Background.svg) — Extended logo/banner artwork with its background.

These files represent the current project branding.

### Official RtG Banners

[`images/logo/official-banners/`](images/logo/official-banners/) contains Road To Gramby's banner images used as backgrounds or visual references for project presentation.

The files are numbered for convenience:

* [`RtG-1.webp`](images/logo/official-banners/RtG-1.webp)
* [`RtG-2.webp`](images/logo/official-banners/RtG-2.webp)
* [`RtG-3.webp`](images/logo/official-banners/RtG-3.webp)
* [`RtG-4.webp`](images/logo/official-banners/RtG-4.webp)
* [`RtG-5.webp`](images/logo/official-banners/RtG-5.webp)

The `RtG-#` naming scheme allows additional banner variations to be added without changing the organization of the directory.

### Historical Logo Versions

[`images/logo/versions/`](images/logo/versions/) contains older logo versions preserved for historical reference.

The current historical version is stored under [`images/logo/versions/v1/`](images/logo/versions/v1/):

* [`RtG-Format-v1.svg`](images/logo/versions/v1/RtG-Format-v1.svg)
* [`RtG-Format-v1.png`](images/logo/versions/v1/RtG-Format-v1.png)

These files are **obsolete** and should not be used for new project materials or branding.

## RtG-Preview

The `RtG-Preview` assets provide the external resources required by the **RtG-Preview** renderer.

These assets are separated by their purpose so that models, interface graphics, and audio can be maintained independently from the renderer itself.

**### Models**

The [`models/`](models/) directory contains the 3D models and their metadata used by **RtG-Preview**.

Each model is stored inside its own directory. The directory name, the main OBJ filename, and the JSON metadata filename use the model's internal RtG object type name.

The general structure is:

```text
models/
├── Model/
│   ├── Model.obj
│   └── Model.json
├── AnotherModel/
│   ├── AnotherModel.obj
│   └── AnotherModel.json
└── BranchedModel/
    ├── BranchedModel.obj
    ├── BranchedModel.json
    └── split/
        ├── branch.obj
        └── anotherBranch.obj
```

Models use the **Wavefront OBJ** format.

For example:

```text
models/
├── Fricklet/
│   ├── Fricklet.obj
│   └── Fricklet.json
│
├── Tooth/
│   ├── Tooth.obj
│   └── Tooth.json
│
└── Switch/
    ├── Switch.obj
    ├── Switch.json
    └── split/
        ├── input.obj
        └── output.obj
```

RtG-Preview resolves the main model using the object's internal RtG type name:

```text
"Tooth"     → assets/models/Tooth/Tooth.obj
"Fricklet"  → assets/models/Fricklet/Fricklet.obj
"Switch"    → assets/models/Switch/Switch.obj
```

The model directory also contains a JSON metadata file:

```text
assets/models/<Model>/<Model>.json
```

This metadata describes information such as the model's tooltip, local connection points, branches, branch origins, preview settings, and other RtG-Format data.

### Branched Models

Some models contain multiple OBJ files.

The complete model is stored in:

```text
<Model>/<Model>.obj
```

Individual branches are stored inside:

```text
<Model>/split/
```

For example:

```text
Switch/
├── Switch.obj
├── Switch.json
└── split/
    ├── input.obj
    └── output.obj
```

The complete model represents the entire object, while the files inside `split/` represent its individual branches.

Branch information and the corresponding branch origins are described in the model's JSON metadata.

### Blender Source

The Blender source used to generate a model may also be stored in its model directory when applicable:

```text
<Model>/
├── <Model>.blend
├── <Model>.obj
└── <Model>.json
```

The Blender scene follows the model structure documented in [`models/README.md`](models/README.md).

For models without branches:

```text
Model
└── Model
    └── start.Model
```

For models with branches:

```text
Model
├── Model
├── branch
│   └── start.Model.branch
└── branch
    └── start.Model.branch
```

Empty objects such as `start.*` and `Point_X` are metadata markers and are not exported as OBJ geometry.

Additional details about model creation, Blender hierarchy, branches, `start` objects, `Point_X` objects, and JSON metadata are documented in [`models/README.md`](models/README.md).


### Sounds

The [`sounds/`](sounds/) directory contains audio feedback used by RtG-Preview.

* [`error.mp3`](sounds/error.mp3) — Played when an error or failure is reported by the preview interface.
* [`notification.mp3`](sounds/notification.mp3) — Used for general interface notifications.

These sounds are optional interface feedback and are not part of the RtG build format itself.

### SVG

The [`svg/`](svg/) directory contains SVG graphics used by the RtG-Preview interface.

* [`menu-closed.svg`](svg/menu-closed.svg) — Menu button icon used when the preview panel is open.
* [`menu-opened.svg`](svg/menu-opened.svg) — Menu button icon used when the preview panel is closed.

These graphics are used by the preview's panel toggle control and are intended to remain lightweight, scalable interface assets.

## Asset Guidelines

When adding or modifying project assets:

* Keep general visual assets inside [`images/`](images/).
* Keep current RtG-Format branding inside [`images/logo/`](images/logo/).
* Keep official Road To Gramby's banner references inside [`images/logo/official-banners/`](images/logo/official-banners/).
* Keep obsolete logo versions inside [`images/logo/versions/`](images/logo/versions/).
* Keep RtG-Preview 3D models inside [`models/`](models/).
* Keep RtG-Preview audio inside [`sounds/`](sounds/).
* Keep RtG-Preview interface SVGs inside [`svg/`](svg/).
* Do not use files under `versions/` as current branding.
* Prefer SVG for logos and other graphics that need to scale cleanly.
* Use PNG or JPEG when a raster format is specifically required.
* Use WebP for the official banner images stored in `official-banners/`.
* Use OBJ for RtG-Preview 3D models unless the renderer explicitly adds support for another format.
* When replacing an asset, preserve older versions when they are useful for historical reference instead of silently overwriting them.
* Keep asset filenames consistent with the names expected by the code that loads them.

## Related Documentation

* [`../README.md`](../README.md) — Main project documentation.
* [`../structure.md`](../structure.md) — Repository structure.
* [`images/`](images/) — Image assets used throughout the repository.
* [`models/`](models/) — 3D models used by RtG-Preview.
* [`sounds/`](sounds/) — Audio feedback used by RtG-Preview.
* [`svg/`](svg/) — Interface graphics used by RtG-Preview.
