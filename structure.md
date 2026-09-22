# Repository Structure
This document describes the current structure of the RtG-Format repository.

The tree below reflects the repository's current organization and is intended to help contributors and readers understand where documentation, research, assets, examples, tools, and website files are located.

## Text/Tree Format
```tree
RtG-Format/
│
├── README.md
├── SPECIFICATION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── structure.md
├── owner-todo.md
├── rtg-format.cff
├── .hintrc
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
│
├── RtG-CLI/
│   ├── rtg.py
│   ├── rtg.cmd
│   ├── assets.json
│   ├── en/
│   │   ├── help.en.md
│   │   └── rules.en.md
│   └── es/
│       ├── help.es.md
│       └── rules.es.md
│
├── RtG-Preview/
│   ├── preview.js
│   ├── model-registry.js
│   ├── models.json
│   ├── models-manifest.js
│   ├── README.md
│   ├── saving.md
│   ├── splash.json
│   └── test-preview.html
│
├── RtG Language/
│   ├── rtg_lang.py
│   ├── data.json
│   ├── RTG-LANG-SPEC-spanish.md
│   └── examples/
│       ├── example.rtg
│       ├── example_completo.rtg
│       └── example2_compacto.rtg
│
├── assets/
│   ├── README.md
│   ├── images/
│   │   ├── banner.jpeg
│   │   ├── banner.png
│   │   ├── banner.svg
│   │   └── logo/
│   │       ├── RtG-Format.svg
│   │       ├── RtG-Format.png
│   │       ├── RtG-Format-Shape.svg
│   │       ├── RtG-Format-Background.svg
│   │       ├── official-banners/
│   │       │   ├── RtG-1.webp
│   │       │   ├── RtG-2.webp
│   │       │   ├── RtG-3.webp
│   │       │   ├── RtG-4.webp
│   │       │   └── RtG-5.webp
│   │       └── versions/
│   │           ├── shape-v1/
│   │           │   └── RtG-Format-Shape-ToFInish.png
│   │           └── v1/
│   │               ├── RtG-Format-v1.svg
│   │               └── RtG-Format-v1.png
│   ├── models/
│   │   ├── README.md
│   │   ├── model/
│   │   │   ├── AltitudeSensor/
│   │   │   │   ├── AltitudeSensor.json
│   │   │   │   └── AltitudeSensor.obj
│   │   │   ├── Anchor/
│   │   │   │   ├── Anchor.json
│   │   │   │   └── Anchor.obj
│   │   │   ├── Arm/
│   │   │   │   ├── Arm.json
│   │   │   │   └── Arm.obj
│   │   │   ├── Balloon/
│   │   │   │   ├── Balloon.json
│   │   │   │   └── Balloon.obj
│   │   │   ├── BallSocket/
│   │   │   │   ├── BallSocket.json
│   │   │   │   └── BallSocket.obj
│   │   │   ├── Banjo/
│   │   │   │   ├── Banjo.json
│   │   │   │   └── Banjo.obj
│   │   │   ├── Base/
│   │   │   │   ├── Base.json
│   │   │   │   ├── Base.obj
│   │   │   │   └── README.md
│   │   │   ├── BeachBall/
│   │   │   │   ├── BeachBall.json
│   │   │   │   └── BeachBall.obj
│   │   │   ├── Bearing/
│   │   │   │   ├── Bearing.json
│   │   │   │   └── Bearing.obj
│   │   │   ├── Board/
│   │   │   │   ├── Board.json
│   │   │   │   └── Board.obj
│   │   │   ├── Body/
│   │   │   │   ├── Body.json
│   │   │   │   └── Body.obj
│   │   │   ├── BouncyBall/
│   │   │   │   ├── BouncyBall.json
│   │   │   │   └── BouncyBall.obj
│   │   │   ├── BowlingBall/
│   │   │   │   ├── BowlingBall.json
│   │   │   │   └── BowlingBall.obj
│   │   │   ├── BrakeLight/
│   │   │   │   ├── BrakeLight.json
│   │   │   │   └── BrakeLight.obj
│   │   │   ├── Briefcase/
│   │   │   │   ├── Briefcase.json
│   │   │   │   └── Briefcase.obj
│   │   │   ├── Bumper/
│   │   │   │   ├── Bumper.json
│   │   │   │   └── Bumper.obj
│   │   │   ├── Button/
│   │   │   │   ├── Button.json
│   │   │   │   └── Button.obj
│   │   │   ├── Camera/
│   │   │   │   ├── Camera.json
│   │   │   │   └── Camera.obj
│   │   │   ├── Canister/
│   │   │   │   ├── Canister.json
│   │   │   │   └── Canister.obj
│   │   │   ├── Cannon/
│   │   │   │   ├── Cannon.json
│   │   │   │   └── Cannon.obj
│   │   │   ├── CannonBall/
│   │   │   │   ├── CannonBall.json
│   │   │   │   └── CannonBall.obj
│   │   │   ├── Carrot/
│   │   │   │   ├── Carrot.json
│   │   │   │   └── Carrot.obj
│   │   │   ├── Chassis/
│   │   │   │   ├── Chassis.json
│   │   │   │   └── Chassis.obj
│   │   │   ├── Cinderblock/
│   │   │   │   ├── Cinderblock.json
│   │   │   │   └── Cinderblock.obj
│   │   │   ├── Connector/
│   │   │   │   ├── Connector.json
│   │   │   │   └── Connector.obj
│   │   │   ├── ConnectorBall/
│   │   │   │   ├── ConnectorBall.json
│   │   │   │   └── ConnectorBall.obj
│   │   │   ├── Delayer/
│   │   │   │   ├── Delayer.json
│   │   │   │   └── Delayer.obj
│   │   │   ├── Detacher/
│   │   │   │   ├── Detacher.json
│   │   │   │   └── Detacher.obj
│   │   │   ├── DoorA/
│   │   │   │   ├── DoorA.json
│   │   │   │   └── DoorA.obj
│   │   │   ├── DoorB/
│   │   │   │   ├── DoorB.json
│   │   │   │   └── DoorB.obj
│   │   │   ├── DoorC/
│   │   │   │   ├── DoorC.json
│   │   │   │   └── DoorC.obj
│   │   │   ├── DoorD/
│   │   │   │   ├── DoorD.json
│   │   │   │   └── DoorD.obj
│   │   │   ├── Drumkit/
│   │   │   │   ├── Drumkit.json
│   │   │   │   └── Drumkit.obj
│   │   │   ├── EntitySensor/
│   │   │   │   ├── EntitySensor.json
│   │   │   │   └── EntitySensor.obj
│   │   │   ├── FishBowl/
│   │   │   │   ├── FishBowl.json
│   │   │   │   └── FishBowl.obj
│   │   │   ├── Fricklet/
│   │   │   │   ├── Fricklet.json
│   │   │   │   └── Fricklet.obj
│   │   │   ├── FuelTank/
│   │   │   │   ├── FuelTank.json
│   │   │   │   └── FuelTank.obj
│   │   │   ├── GasCap/
│   │   │   │   ├── GasCap.json
│   │   │   │   └── GasCap.obj
│   │   │   ├── Gate-AND/
│   │   │   │   ├── Gate-AND.json
│   │   │   │   └── Gate-AND.obj
│   │   │   ├── Gate-NOT/
│   │   │   │   ├── Gate-NOT.json
│   │   │   │   └── Gate-NOT.obj
│   │   │   ├── Gate-OR/
│   │   │   │   ├── Gate-OR.json
│   │   │   │   └── Gate-OR.obj
│   │   │   ├── GoldPotatoEngine/
│   │   │   │   ├── GoldPotatoEngine.json
│   │   │   │   └── GoldPotatoEngine.obj
│   │   │   ├── Googie/
│   │   │   │   ├── Googie.json
│   │   │   │   └── Googie.obj
│   │   │   ├── Gramby/
│   │   │   │   ├── Gramby.json
│   │   │   │   └── Gramby.obj
│   │   │   ├── Grenade/
│   │   │   │   ├── Grenade.json
│   │   │   │   └── Grenade.obj
│   │   │   ├── Guitar/
│   │   │   │   ├── Guitar.json
│   │   │   │   └── Guitar.obj
│   │   │   ├── Gun/
│   │   │   │   ├── Gun.json
│   │   │   │   └── Gun.obj
│   │   │   ├── Gyro/
│   │   │   │   ├── Gyro.json
│   │   │   │   └── Gyro.obj
│   │   │   ├── HalfConnectorBall/
│   │   │   │   ├── HalfConnectorBall.json
│   │   │   │   └── HalfConnectorBall.obj
│   │   │   ├── Head/
│   │   │   │   ├── Head.json
│   │   │   │   └── Head.obj
│   │   │   ├── Hood/
│   │   │   │   ├── Hood.json
│   │   │   │   └── Hood.obj
│   │   │   ├── InputSensor/
│   │   │   │   ├── InputSensor.json
│   │   │   │   └── InputSensor.obj
│   │   │   ├── Joint/
│   │   │   │   ├── Joint.json
│   │   │   │   └── Joint.obj
│   │   │   ├── Joust/
│   │   │   │   ├── Joust.json
│   │   │   │   └── Joust.obj
│   │   │   ├── Jug/
│   │   │   │   ├── Jug.json
│   │   │   │   └── Jug.obj
│   │   │   ├── Keyboard/
│   │   │   │   ├── Keyboard.json
│   │   │   │   └── Keyboard.obj
│   │   │   ├── Leafblower/
│   │   │   │   ├── Leafblower.json
│   │   │   │   └── Leafblower.obj
│   │   │   ├── Leg/
│   │   │   │   ├── Leg.json
│   │   │   │   └── Leg.obj
│   │   │   ├── Light/
│   │   │   │   ├── Light.json
│   │   │   │   └── Light.obj
│   │   │   ├── Lock/
│   │   │   │   ├── Lock.json
│   │   │   │   └── Lock.obj
│   │   │   ├── LongStick/
│   │   │   │   ├── LongStick.json
│   │   │   │   └── LongStick.obj
│   │   │   ├── Looper/
│   │   │   │   ├── Looper.json
│   │   │   │   └── Looper.obj
│   │   │   ├── Mag/
│   │   │   │   ├── Mag.json
│   │   │   │   └── Mag.obj
│   │   │   ├── MatchingGyro/
│   │   │   │   ├── MatchingGyro.json
│   │   │   │   └── MatchingGyro.obj
│   │   │   ├── MountedGun/
│   │   │   │   ├── MountedGun.json
│   │   │   │   └── MountedGun.obj
│   │   │   ├── Part/
│   │   │   │   ├── Part.json
│   │   │   │   └── Part.obj
│   │   │   ├── Pie/
│   │   │   │   ├── Pie.json
│   │   │   │   └── Pie.obj
│   │   │   ├── Pipes/
│   │   │   │   ├── Pipes.json
│   │   │   │   └── Pipes.obj
│   │   │   ├── Piston/
│   │   │   │   ├── Piston.json
│   │   │   │   └── Piston.obj
│   │   │   ├── Plunger/
│   │   │   │   ├── Plunger.json
│   │   │   │   └── Plunger.obj
│   │   │   ├── Poop/
│   │   │   │   ├── Poop.json
│   │   │   │   └── Poop.obj
│   │   │   ├── PotatoEngine/
│   │   │   │   ├── PotatoEngine.json
│   │   │   │   └── PotatoEngine.obj
│   │   │   ├── PressurePlate/
│   │   │   │   ├── PressurePlate.json
│   │   │   │   └── PressurePlate.obj
│   │   │   ├── Propeller/
│   │   │   │   ├── Propeller.json
│   │   │   │   └── Propeller.obj
│   │   │   ├── Radio/
│   │   │   │   ├── Radio.json
│   │   │   │   └── Radio.obj
│   │   │   ├── Ramp/
│   │   │   │   ├── Ramp.json
│   │   │   │   └── Ramp.obj
│   │   │   ├── Recorder/
│   │   │   │   ├── Recorder.json
│   │   │   │   └── Recorder.obj
│   │   │   ├── RemoteButton/
│   │   │   │   ├── RemoteButton.json
│   │   │   │   └── RemoteButton.obj
│   │   │   ├── RiotShield/
│   │   │   │   ├── RiotShield.json
│   │   │   │   └── RiotShield.obj
│   │   │   ├── Rocket/
│   │   │   │   ├── Rocket.json
│   │   │   │   └── Rocket.obj
│   │   │   ├── RockingChair/
│   │   │   │   ├── RockingChair.json
│   │   │   │   └── RockingChair.obj
│   │   │   ├── Roof/
│   │   │   │   ├── Roof.json
│   │   │   │   └── Roof.obj
│   │   │   ├── Rope/
│   │   │   │   ├── Rope.json
│   │   │   │   └── Rope.obj
│   │   │   ├── RPG/
│   │   │   │   ├── RPG.json
│   │   │   │   └── RPG.obj
│   │   │   ├── RubberBand/
│   │   │   │   ├── RubberBand.json
│   │   │   │   └── RubberBand.obj
│   │   │   ├── Seat/
│   │   │   │   ├── Seat.json
│   │   │   │   └── Seat.obj
│   │   │   ├── Servo/
│   │   │   │   ├── Servo.json
│   │   │   │   └── Servo.obj
│   │   │   ├── Servo_Physics/
│   │   │   │   ├── Servo_Physics.json
│   │   │   │   └── Servo_Physics.obj
│   │   │   ├── ShoppingCart/
│   │   │   │   ├── ShoppingCart.json
│   │   │   │   └── ShoppingCart.obj
│   │   │   ├── ShortStick/
│   │   │   │   ├── ShortStick.json
│   │   │   │   └── ShortStick.obj
│   │   │   ├── Shotgun/
│   │   │   │   ├── Shotgun.json
│   │   │   │   └── Shotgun.obj
│   │   │   ├── Sledge/
│   │   │   │   ├── Sledge.json
│   │   │   │   └── Sledge.obj
│   │   │   ├── Splitter/
│   │   │   │   ├── Splitter.json
│   │   │   │   └── Splitter.obj
│   │   │   ├── Splitter_1/
│   │   │   │   ├── Splitter_1.json
│   │   │   │   └── Splitter_1.obj
│   │   │   ├── Splitter_2/
│   │   │   │   ├── Splitter_2.json
│   │   │   │   └── Splitter_2.obj
│   │   │   ├── Splitter_3/
│   │   │   │   ├── Splitter_3.json
│   │   │   │   └── Splitter_3.obj
│   │   │   ├── Splitter_4/
│   │   │   │   ├── Splitter_4.json
│   │   │   │   └── Splitter_4.obj
│   │   │   ├── SprayPaint/
│   │   │   │   ├── SprayPaint.json
│   │   │   │   └── SprayPaint.obj
│   │   │   ├── SpringJuice/
│   │   │   │   ├── SpringJuice.json
│   │   │   │   └── SpringJuice.obj
│   │   │   ├── StaringGyro/
│   │   │   │   ├── StaringGyro.json
│   │   │   │   └── StaringGyro.obj
│   │   │   ├── SteeringGyro/
│   │   │   │   ├── SteeringGyro.json
│   │   │   │   └── SteeringGyro.obj
│   │   │   ├── SteeringWheel/
│   │   │   │   ├── SteeringWheel.json
│   │   │   │   └── SteeringWheel.obj
│   │   │   ├── Stick/
│   │   │   │   ├── Stick.json
│   │   │   │   └── Stick.obj
│   │   │   ├── SuperPowerClock/
│   │   │   │   ├── SuperPowerClock.json
│   │   │   │   └── SuperPowerClock.obj
│   │   │   ├── Switch/
│   │   │   │   ├── split/
│   │   │   │   │   ├── input.obj
│   │   │   │   │   └── output.obj
│   │   │   │   ├── Switch.json
│   │   │   │   └── Switch.obj
│   │   │   ├── Teeth/
│   │   │   ├── Thruster/
│   │   │   │   ├── Thruster.json
│   │   │   │   └── Thruster.obj
│   │   │   ├── Tire/
│   │   │   │   ├── Tire.json
│   │   │   │   └── Tire.obj
│   │   │   ├── ToolGun/
│   │   │   │   ├── ToolGun.json
│   │   │   │   └── ToolGun.obj
│   │   │   ├── Tooth/
│   │   │   │   ├── Tooth.json
│   │   │   │   └── Tooth.obj
│   │   │   ├── TripWire/
│   │   │   │   ├── TripWire.json
│   │   │   │   └── TripWire.obj
│   │   │   ├── Trowel/
│   │   │   │   ├── Trowel.json
│   │   │   │   └── Trowel.obj
│   │   │   ├── Trumpet/
│   │   │   │   ├── Trumpet.json
│   │   │   │   └── Trumpet.obj
│   │   │   ├── Trunk/
│   │   │   │   ├── Trunk.json
│   │   │   │   └── Trunk.obj
│   │   │   ├── TV/
│   │   │   │   ├── TV.json
│   │   │   │   └── TV.obj
│   │   │   ├── Uzi/
│   │   │   │   ├── Uzi.json
│   │   │   │   └── Uzi.obj
│   │   │   ├── VelocitySensor/
│   │   │   │   ├── VelocitySensor.json
│   │   │   │   └── VelocitySensor.obj
│   │   │   ├── wad/
│   │   │   │   ├── wad.json
│   │   │   │   └── wad.obj
│   │   │   ├── Wheel/
│   │   │   │   ├── Wheel.json
│   │   │   │   └── Wheel.obj
│   │   │   ├── Wing/
│   │   │   │   ├── Wing.json
│   │   │   │   └── Wing.obj
│   │   │   └── Wire/
│   │   │       ├── Wire.json
│   │   │       └── Wire.obj
│   │   ├── deprecated/
│   │   │   ├── __pycache__/
│   │   │   ├── _backup_before_property_update/
│   │   │   ├── blend.py
│   │   │   ├── blend_json.py
│   │   │   └── blend_root.py
│   │   ├── textures/
│   │   │   ├── 5302791622.png
│   │   │   └── 5808635679.jpeg
│   │   ├── ALL.blend
│   │   └── ALL.blend1
│   ├── sounds/
│   │   ├── error.mp3
│   │   └── notification.mp3
│   └── svg/
│       ├── menu-closed_light.svg
│       ├── menu-closed.svg
│       ├── menu-opened_light.svg
│       └── menu-opened.svg
│
├── blocks/
│   ├── README.md
│   └── parts/
│        ├── building/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── miscellaneous/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── other/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── physics/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── tools/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── uncategorized/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        ├── unused/
│        │    ├── imgs/
│        │    ├── parts-id.md
│        │    └── README.md
│        └── wiring/
│             ├── imgs/
│             ├── parts-id.md
│             └── README.md
│
├── compression/
│   ├── README.md
│   ├── overview.md
│   ├── encoding.md
│   └── examples-template.md
│
├── dev/
│   ├── __pycache__/
│   ├── organize_polaroid.py
│   ├── Photos/
│   │   ├── 1.json
│   │   ├── 1org.json
│   │   ├── 2.json
│   │   ├── 2org.json
│   │   ├── 3.json
│   │   ├── 3org.json
│   │   └── new.json
│   ├── PolaroidPhoto.json
│   ├── PolaroidPhoto_Organized.json
│   └── scripts/
│       ├── assets/
│       │   └── AssetID.json
│       ├── launcher.py
│       ├── openAssetID.py
│       ├── textures/
│       │   ├── openTexturesID.py
│       │   └── TextureId.py
│       └── textureIDs.json
│
├── docs/
│   ├── README.md
│   ├── getting-started.md
│   ├── save-anatomy.md
│   ├── building-system.md
│   └── faq.md
│
├── examples/
│   ├── README.md
│   ├── experiments/
│   │    ├── README.md
│   ├── json-examples/
│   │    ├── README.md
│   └── trash/
│        ├── README.md
│
├── format/
│   ├── README.md
│   ├── json-structure.md
│   ├── indexing.md
│   ├── properties.md
│   ├── identifiers.md
│   └── unknown-fields.md
│
├── old-files/
│   ├── README.md
│   ├── obj_ids-spanish.md
│   ├── PolaroidPhoto-spanish.md
│   └── RtG_Save_Format_Specification-spanish.md
│
├── page/
│   ├── index.html
│   ├── css/
│   │   ├── layout.css
│   │   ├── main.css
│   │   └── markdown.css
│   ├── js/
│   │   ├── app.js
│   │   ├── base64.js
│   │   ├── code-blocks.js
│   │   ├── github.js
│   │   ├── markdown.js
│   │   ├── mermaid.js
│   │   ├── navigation.js
│   │   ├── router.js
│   │   └── utils.js
│   └── assets/
│       ├── logo.png
│       ├── RtG-Format-Shape.svg
│       ├── banner.svg
│       └── icons/
│
├── research/
│   ├── README.md
│   ├── methodology.md
│   ├── discoveries.md
│   └── unknowns.md
│
├── scripts/
│   ├── fix-json.js
│   └── generate-manifest.js
│
└── tools/
    ├── README.md
    ├── agent/
    │   ├── __pycache__/
    │   ├── parts_diff.py
    │   ├── README.md
    │   └── regenerate_parts.py
    ├── dedicated-structure/
    │   ├── README.md
    │   ├── RtG-AI.md
    │   └── RtG Image.tree
    ├── RtG Image/
    │   └── ...
    └── RtG-AI/
        └── ...
```

## Component Overview

| Component | Purpose | Type |
|-----------|---------|------|
| `RtG-CLI/` | Command-line interface for RtG tools | Python code |
| `RtG-Preview/` | Browser-based 3D preview renderer | JavaScript code |
| `RtG Language/` | Custom language for RtG builds | Python code + spec |
| `assets/` | 3D models, images, sounds, SVGs | Binary assets |
| `blocks/` | Documented block/part IDs by category | Documentation |
| `format/` | Detailed format specification docs | Documentation |
| `compression/` | Encoding/compression research | Documentation |
| `examples/` | Real and experimental build examples | JSON data |
| `research/` | Research methodology and findings | Documentation |
| `old-files/` | Historical reverse-engineering records | Historical evidence |
| `docs/` | Introductory documentation | Documentation |
| `scripts/` | Utility scripts | JavaScript/Node.js |
| `tools/` | Development tools and sub-projects | Mixed code |
| `page/` | GitHub Pages documentation website | Web files |
| `delete/` | Deprecated/removed model data | Historical data |

## Key Relationships

- `RtG-CLI` reads `RtG-CLI/assets.json` for configuration and delegates to addons via `program commands` paths
- `RtG-Preview` loads models from `assets/models/model/` via `models.json` (HTTP) or `models-manifest.js` (file://)
- `RtG-AI` uses `RtG-Preview` for build visualization and `RtG-Format` specification for build structure
- `format/` documents provide detailed specification referenced by `SPECIFICATION.md`
- `blocks/parts/` contains organized Part ID documentation by category
- `old-files/` has priority as evidence when discrepancies exist with current docs
- `scripts/generate-manifest.js` generates both `RtG-Preview/models.json` and `models-manifest.js`