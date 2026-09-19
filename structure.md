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
│   
├── RtG-Preview/
│   ├─ models/
│   └─ preview.js
│   
├── page/
│   │
│   ├── index.html
│   │
│   ├── css/
│   │   ├── main.css
│   │   ├── layout.css
│   │   └── markdown.css
│   │
│   ├── js/
│   │   ├── app.js
│   │   ├── router.js
│   │   ├── github.js
│   │   ├── markdown.js
│   │   ├── mermaid.js
│   │   ├── base64.js
│   │   ├── navigation.js
│   │   └── utils.js
│   │
│   └── assets/
│       ├── logo.png
│       └── icons/
│
├── assets/
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
│   │           └── v1/
│   │               ├── RtG-Format-v1.svg
│   │               └── RtG-Format-v1.png
│   │
│   ├── models/
│   │   ├─ model/
│   │   │  ├─ AltitudeSensor/
│   │   │  │  ├─ AltitudeSensor.json
│   │   │  │  └─ AltitudeSensor.obj
│   │   │  ├─ Anchor/
│   │   │  │  ├─ Anchor.json
│   │   │  │  └─ Anchor.obj
│   │   │  ├─ Arm/
│   │   │  │  ├─ Arm.json
│   │   │  │  └─ Arm.obj
│   │   │  ├─ Balloon/
│   │   │  │  ├─ Balloon.json
│   │   │  │  └─ Balloon.obj
│   │   │  ├─ BallSocket/
│   │   │  │  ├─ BallSocket.json
│   │   │  │  └─ BallSocket.obj
│   │   │  ├─ Banjo/
│   │   │  │  ├─ Banjo.json
│   │   │  │  └─ Banjo.obj
│   │   │  ├─ Base/
│   │   │  │  ├─ Base.json
│   │   │  │  ├─ Base.obj
│   │   │  │  └─ README.md
│   │   │  ├─ BeachBall/
│   │   │  │  ├─ BeachBall.json
│   │   │  │  └─ BeachBall.obj
│   │   │  ├─ Bearing/
│   │   │  │  ├─ Bearing.json
│   │   │  │  └─ Bearing.obj
│   │   │  ├─ Board/
│   │   │  │  ├─ Board.json
│   │   │  │  └─ Board.obj
│   │   │  ├─ Body/
│   │   │  │  ├─ Body.json
│   │   │  │  └─ Body.obj
│   │   │  ├─ BouncyBall/
│   │   │  │  ├─ BouncyBall.json
│   │   │  │  └─ BouncyBall.obj
│   │   │  ├─ BowlingBall/
│   │   │  │  ├─ BowlingBall.json
│   │   │  │  └─ BowlingBall.obj
│   │   │  ├─ BrakeLight/
│   │   │  │  ├─ BrakeLight.json
│   │   │  │  └─ BrakeLight.obj
│   │   │  ├─ Briefcase/
│   │   │  │  ├─ Briefcase.json
│   │   │  │  └─ Briefcase.obj
│   │   │  ├─ Bumper/
│   │   │  │  ├─ Bumper.json
│   │   │  │  └─ Bumper.obj
│   │   │  ├─ Button/
│   │   │  │  ├─ Button.json
│   │   │  │  └─ Button.obj
│   │   │  ├─ Camera/
│   │   │  │  ├─ Camera.json
│   │   │  │  └─ Camera.obj
│   │   │  ├─ Canister/
│   │   │  │  ├─ Canister.json
│   │   │  │  └─ Canister.obj
│   │   │  ├─ Cannon/
│   │   │  │  ├─ Cannon.json
│   │   │  │  └─ Cannon.obj
│   │   │  ├─ CannonBall/
│   │   │  │  ├─ CannonBall.json
│   │   │  │  └─ CannonBall.obj
│   │   │  ├─ Carrot/
│   │   │  │  ├─ Carrot.json
│   │   │  │  └─ Carrot.obj
│   │   │  ├─ Chassis/
│   │   │  │  ├─ Chassis.json
│   │   │  │  └─ Chassis.obj
│   │   │  ├─ Cinderblock/
│   │   │  │  ├─ Cinderblock.json
│   │   │  │  └─ Cinderblock.obj
│   │   │  ├─ Connector/
│   │   │  │  ├─ Connector.json
│   │   │  │  └─ Connector.obj
│   │   │  ├─ ConnectorBall/
│   │   │  │  ├─ ConnectorBall.json
│   │   │  │  └─ ConnectorBall.obj
│   │   │  ├─ Delayer/
│   │   │  │  ├─ Delayer.json
│   │   │  │  └─ Delayer.obj
│   │   │  ├─ Detacher/
│   │   │  │  ├─ Detacher.json
│   │   │  │  └─ Detacher.obj
│   │   │  ├─ DoorA/
│   │   │  │  ├─ DoorA.json
│   │   │  │  └─ DoorA.obj
│   │   │  ├─ DoorB/
│   │   │  │  ├─ DoorB.json
│   │   │  │  └─ DoorB.obj
│   │   │  ├─ DoorC/
│   │   │  │  ├─ DoorC.json
│   │   │  │  └─ DoorC.obj
│   │   │  ├─ DoorD/
│   │   │  │  ├─ DoorD.json
│   │   │  │  └─ DoorD.obj
│   │   │  ├─ Drumkit/
│   │   │  │  ├─ Drumkit.json
│   │   │  │  └─ Drumkit.obj
│   │   │  ├─ EntitySensor/
│   │   │  │  ├─ EntitySensor.json
│   │   │  │  └─ EntitySensor.obj
│   │   │  ├─ FishBowl/
│   │   │  │  ├─ FishBowl.json
│   │   │  │  └─ FishBowl.obj
│   │   │  ├─ Fricklet/
│   │   │  │  ├─ Fricklet.json
│   │   │  │  └─ Fricklet.obj
│   │   │  ├─ FuelTank/
│   │   │  │  ├─ FuelTank.json
│   │   │  │  └─ FuelTank.obj
│   │   │  ├─ GasCap/
│   │   │  │  ├─ GasCap.json
│   │   │  │  └─ GasCap.obj
│   │   │  ├─ Gate-AND/
│   │   │  │  ├─ Gate-AND.json
│   │   │  │  └─ Gate-AND.obj
│   │   │  ├─ Gate-NOT/
│   │   │  │  ├─ Gate-NOT.json
│   │   │  │  └─ Gate-NOT.obj
│   │   │  ├─ Gate-OR/
│   │   │  │  ├─ Gate-OR.json
│   │   │  │  └─ Gate-OR.obj
│   │   │  ├─ GoldPotatoEngine/
│   │   │  │  ├─ GoldPotatoEngine.json
│   │   │  │  └─ GoldPotatoEngine.obj
│   │   │  ├─ Googie/
│   │   │  │  ├─ Googie.json
│   │   │  │  └─ Googie.obj
│   │   │  ├─ Gramby/
│   │   │  │  ├─ Gramby.json
│   │   │  │  └─ Gramby.obj
│   │   │  ├─ Grenade/
│   │   │  │  ├─ Grenade.json
│   │   │  │  └─ Grenade.obj
│   │   │  ├─ Guitar/
│   │   │  │  ├─ Guitar.json
│   │   │  │  └─ Guitar.obj
│   │   │  ├─ Gun/
│   │   │  │  ├─ Gun.json
│   │   │  │  └─ Gun.obj
│   │   │  ├─ Gyro/
│   │   │  │  ├─ Gyro.json
│   │   │  │  └─ Gyro.obj
│   │   │  ├─ HalfConnectorBall/
│   │   │  │  ├─ HalfConnectorBall.json
│   │   │  │  └─ HalfConnectorBall.obj
│   │   │  ├─ Head/
│   │   │  │  ├─ Head.json
│   │   │  │  └─ Head.obj
│   │   │  ├─ Hood/
│   │   │  │  ├─ Hood.json
│   │   │  │  └─ Hood.obj
│   │   │  ├─ InputSensor/
│   │   │  │  ├─ InputSensor.json
│   │   │  │  └─ InputSensor.obj
│   │   │  ├─ Joint/
│   │   │  │  ├─ Joint.json
│   │   │  │  └─ Joint.obj
│   │   │  ├─ Joust/
│   │   │  │  ├─ Joust.json
│   │   │  │  └─ Joust.obj
│   │   │  ├─ Jug/
│   │   │  │  ├─ Jug.json
│   │   │  │  └─ Jug.obj
│   │   │  ├─ Keyboard/
│   │   │  │  ├─ Keyboard.json
│   │   │  │  └─ Keyboard.obj
│   │   │  ├─ Leafblower/
│   │   │  │  ├─ Leafblower.json
│   │   │  │  └─ Leafblower.obj
│   │   │  ├─ Leg/
│   │   │  │  ├─ Leg.json
│   │   │  │  └─ Leg.obj
│   │   │  ├─ Light/
│   │   │  │  ├─ Light.json
│   │   │  │  └─ Light.obj
│   │   │  ├─ Lock/
│   │   │  │  ├─ Lock.json
│   │   │  │  └─ Lock.obj
│   │   │  ├─ LongStick/
│   │   │  │  ├─ LongStick.json
│   │   │  │  └─ LongStick.obj
│   │   │  ├─ Looper/
│   │   │  │  ├─ Looper.json
│   │   │  │  └─ Looper.obj
│   │   │  ├─ Mag/
│   │   │  │  ├─ Mag.json
│   │   │  │  └─ Mag.obj
│   │   │  ├─ MatchingGyro/
│   │   │  │  ├─ MatchingGyro.json
│   │   │  │  └─ MatchingGyro.obj
│   │   │  ├─ MountedGun/
│   │   │  │  ├─ MountedGun.json
│   │   │  │  └─ MountedGun.obj
│   │   │  ├─ Part/
│   │   │  │  ├─ Part.json
│   │   │  │  └─ Part.obj
│   │   │  ├─ Pie/
│   │   │  │  ├─ Pie.json
│   │   │  │  └─ Pie.obj
│   │   │  ├─ Pipes/
│   │   │  │  ├─ Pipes.json
│   │   │  │  └─ Pipes.obj
│   │   │  ├─ Piston/
│   │   │  │  ├─ Piston.json
│   │   │  │  └─ Piston.obj
│   │   │  ├─ Plunger/
│   │   │  │  ├─ Plunger.json
│   │   │  │  └─ Plunger.obj
│   │   │  ├─ Poop/
│   │   │  │  ├─ Poop.json
│   │   │  │  └─ Poop.obj
│   │   │  ├─ PotatoEngine/
│   │   │  │  ├─ PotatoEngine.json
│   │   │  │  └─ PotatoEngine.obj
│   │   │  ├─ PressurePlate/
│   │   │  │  ├─ PressurePlate.json
│   │   │  │  └─ PressurePlate.obj
│   │   │  ├─ Propeller/
│   │   │  │  ├─ Propeller.json
│   │   │  │  └─ Propeller.obj
│   │   │  ├─ Radio/
│   │   │  │  ├─ Radio.json
│   │   │  │  └─ Radio.obj
│   │   │  ├─ Ramp/
│   │   │  │  ├─ Ramp.json
│   │   │  │  └─ Ramp.obj
│   │   │  ├─ Recorder/
│   │   │  │  ├─ Recorder.json
│   │   │  │  └─ Recorder.obj
│   │   │  ├─ RemoteButton/
│   │   │  │  ├─ RemoteButton.json
│   │   │  │  └─ RemoteButton.obj
│   │   │  ├─ RiotShield/
│   │   │  │  ├─ RiotShield.json
│   │   │  │  └─ RiotShield.obj
│   │   │  ├─ Rocket/
│   │   │  │  ├─ Rocket.json
│   │   │  │  └─ Rocket.obj
│   │   │  ├─ RockingChair/
│   │   │  │  ├─ RockingChair.json
│   │   │  │  └─ RockingChair.obj
│   │   │  ├─ Roof/
│   │   │  │  ├─ Roof.json
│   │   │  │  └─ Roof.obj
│   │   │  ├─ Rope/
│   │   │  │  ├─ Rope.json
│   │   │  │  └─ Rope.obj
│   │   │  ├─ RPG/
│   │   │  │  ├─ RPG.json
│   │   │  │  └─ RPG.obj
│   │   │  ├─ RubberBand/
│   │   │  │  ├─ RubberBand.json
│   │   │  │  └─ RubberBand.obj
│   │   │  ├─ Seat/
│   │   │  │  ├─ Seat.json
│   │   │  │  └─ Seat.obj
│   │   │  ├─ Servo/
│   │   │  │  ├─ Servo.json
│   │   │  │  └─ Servo.obj
│   │   │  ├─ Servo_Physics/
│   │   │  │  ├─ Servo_Physics.json
│   │   │  │  └─ Servo_Physics.obj
│   │   │  ├─ ShoppingCart/
│   │   │  │  ├─ ShoppingCart.json
│   │   │  │  └─ ShoppingCart.obj
│   │   │  ├─ ShortStick/
│   │   │  │  ├─ ShortStick.json
│   │   │  │  └─ ShortStick.obj
│   │   │  ├─ Shotgun/
│   │   │  │  ├─ Shotgun.json
│   │   │  │  └─ Shotgun.obj
│   │   │  ├─ Sledge/
│   │   │  │  ├─ Sledge.json
│   │   │  │  └─ Sledge.obj
│   │   │  ├─ Splitter/
│   │   │  │  ├─ Splitter.json
│   │   │  │  └─ Splitter.obj
│   │   │  ├─ Splitter_1/
│   │   │  │  ├─ Splitter_1.json
│   │   │  │  └─ Splitter_1.obj
│   │   │  ├─ Splitter_2/
│   │   │  │  ├─ Splitter_2.json
│   │   │  │  └─ Splitter_2.obj
│   │   │  ├─ Splitter_3/
│   │   │  │  ├─ Splitter_3.json
│   │   │  │  └─ Splitter_3.obj
│   │   │  ├─ Splitter_4/
│   │   │  │  ├─ Splitter_4.json
│   │   │  │  └─ Splitter_4.obj
│   │   │  ├─ SprayPaint/
│   │   │  │  ├─ SprayPaint.json
│   │   │  │  └─ SprayPaint.obj
│   │   │  ├─ SpringJuice/
│   │   │  │  ├─ SpringJuice.json
│   │   │  │  └─ SpringJuice.obj
│   │   │  ├─ StaringGyro/
│   │   │  │  ├─ StaringGyro.json
│   │   │  │  └─ StaringGyro.obj
│   │   │  ├─ SteeringGyro/
│   │   │  │  ├─ SteeringGyro.json
│   │   │  │  └─ SteeringGyro.obj
│   │   │  ├─ SteeringWheel/
│   │   │  │  ├─ SteeringWheel.json
│   │   │  │  └─ SteeringWheel.obj
│   │   │  ├─ Stick/
│   │   │  │  ├─ Stick.json
│   │   │  │  └─ Stick.obj
│   │   │  ├─ SuperPowerClock/
│   │   │  │  ├─ SuperPowerClock.json
│   │   │  │  └─ SuperPowerClock.obj
│   │   │  ├─ Switch/
│   │   │  │  ├─ split/
│   │   │  │  │  ├─ input.obj
│   │   │  │  │  └─ output.obj
│   │   │  │  ├─ Switch.json
│   │   │  │  └─ Switch.obj
│   │   │  ├─ Teeth/
│   │   │  ├─ Thruster/
│   │   │  │  ├─ Thruster.json
│   │   │  │  └─ Thruster.obj
│   │   │  ├─ Tire/
│   │   │  │  ├─ Tire.json
│   │   │  │  └─ Tire.obj
│   │   │  ├─ ToolGun/
│   │   │  │  ├─ ToolGun.json
│   │   │  │  └─ ToolGun.obj
│   │   │  ├─ Tooth/
│   │   │  │  ├─ Tooth.json
│   │   │  │  └─ Tooth.obj
│   │   │  ├─ TripWire/
│   │   │  │  ├─ TripWire.json
│   │   │  │  └─ TripWire.obj
│   │   │  ├─ Trowel/
│   │   │  │  ├─ Trowel.json
│   │   │  │  └─ Trowel.obj
│   │   │  ├─ Trumpet/
│   │   │  │  ├─ Trumpet.json
│   │   │  │  └─ Trumpet.obj
│   │   │  ├─ Trunk/
│   │   │  │  ├─ Trunk.json
│   │   │  │  └─ Trunk.obj
│   │   │  ├─ TV/
│   │   │  │  ├─ TV.json
│   │   │  │  └─ TV.obj
│   │   │  ├─ Uzi/
│   │   │  │  ├─ Uzi.json
│   │   │  │  └─ Uzi.obj
│   │   │  ├─ VelocitySensor/
│   │   │  │  ├─ VelocitySensor.json
│   │   │  │  └─ VelocitySensor.obj
│   │   │  ├─ wad/
│   │   │  │  ├─ wad.json
│   │   │  │  └─ wad.obj
│   │   │  ├─ Wheel/
│   │   │  │  ├─ Wheel.json
│   │   │  │  └─ Wheel.obj
│   │   │  ├─ Wing/
│   │   │  │  ├─ Wing.json
│   │   │  │  └─ Wing.obj
│   │   │  └─ Wire/
│   │   │     ├─ Wire.json
│   │   │     └─ Wire.obj
│   │   ├─ textures/
│   │   │  ├─ 5302791622.png
│   │   │  └─ 5808635679.jpeg
│   │   ├─ ALL.blend
│   │   ├─ ALL.blend1
│   │   └─ README.md
│   │
│   ├── sounds/
│   │   ├── error.mp3
│   │   └── notification.mp3
│   │
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
├── format/
│   ├── README.md
│   ├── json-structure.md
│   ├── indexing.md
│   ├── properties.md
│   ├── identifiers.md
│   └── unknown-fields.md
│
├── compression/
│   ├── README.md
│   ├── overview.md
│   ├── encoding.md
│   └── examples-template.md
│
├── examples/
│   ├── README.md
│   ├── experiments/
│   │    ├── README.md
│   │    └── ...
│   ├── json-examples/
│   │    ├── README.md
│   │    └── ...
│   └── trash/
│        ├── README.md
│        └── ...
│
├── tools/
│   ├── README.md
│   ├── dedicated-structure/
│   │    ├── README.md
│   │    └── RtG-Image.tree
│   ├── RtG-Image/
│   │    └── ...
│   ├── RtG-AI/
│   │    └── ...
│   └── agent/
│        ├── README.md
│        ├── parts_diff.py
│        └── regenerate_parts.py
│
├── research/
│   ├── README.md
│   ├── methodology.md
│   ├── discoveries.md
│   └── unknowns.md
│
├── old-files/
│   ├── README.md
│   ├── obj_ids-spanish.md
│   └── RtG_Save_Format_Specification-spanish.md
│
└── docs/
    ├── README.md
    ├── getting-started.md
    ├── save-anatomy.md
    ├── building-system.md
    └── faq.md
```

## READ STRUCTURE

```tree
READ STRUCTURE
│
├── README.md
│   ├── # RtG Save Format — Reverse-Engineered Documentation
│   ├── ## What is RtG-Format?
│   │   └── ### What can you find here?
│   ├── ## Quick Start
│   ├── ## How the RtG Save System Works
│   ├── ## Documentation
│   │   ├── ### Format
│   │   ├── ### Blocks and Parts
│   │   ├── ### Compression and Encoding
│   │   ├── ### Examples
│   │   ├── ### Research
│   │   ├── ### Tools
│   │   └── ### Status
│   ├── ## Research Status
│   ├── ## Project Status
│   ├── ## Historical Documentation
│   ├── ## Attribution
│   ├── ## Credits
│   ├── ## Web Documentation
│   ├── ## Link Reference
│   └── ## Repository
│
├── SPECIFICATION.md
│   ├── # RtG Save Format Specification
│   ├── ## 1. Overview
│   ├── ## 2. Root Structure
│   ├── ## 3. Object Type
│   ├── ## 4. Connections
│   │   ├── ### 4.1 `LocalType`
│   │   ├── ### 4.2 `PrimaryID`
│   │   │   ├── #### Numeric connection point
│   │   │   └── #### UUID attachment reference
│   │   └── ### 4.3 `PrimaryIndex`
│   ├── ## 5. Object Ordering
│   ├── ## 6. Spatial Reconstruction
│   ├── ## 7. EphemeralAttachments
│   ├── ## 8. UUID Linking
│   ├── ## 9. Synthetic UUIDs
│   ├── ## 10. CFrame
│   ├── ## 11. Properties
│   │   └── ### 11.1 Property Categories
│   ├── ## 12. Missing Properties
│   ├── ## 13. Observed Properties
│   ├── ## 14. Loader Behavior
│   ├── ## 15. Validation and Failure Behavior
│   ├── ## 16. Coordinate and Attachment Behavior
│   ├── ## 17. Confirmed Discoveries
│   ├── ## 18. Hypotheses and Reconstructed Behavior
│   │   ├── ### 18.1 Loader Pipeline
│   │   └── ### 18.2 Sprite CFrame Behavior
│   ├── ## 19. Historical First Save (Optional)
│   ├── ## 20. Evidence and Confidence
│   │   ├── ### CONFIRMED
│   │   ├── ### OBSERVED
│   │   ├── ### PROBABLE
│   │   ├── ### HYPOTHESIS
│   │   └── ### UNKNOWN
│   └── ## 21. Related Documentation
│       └── ### Historical / Technical Reference
│
├── CHANGELOG.md
│   └── [headings]
│
├── CONTRIBUTING.md
│   └── [headings]
│
├── assets/
│   └── README.md
│       └── # Assets
│           ├── ## Directory Structure
│           ├── ## Images
│           │   ├── ### Banners
│           │   ├── ### Current RtG-Format Logo
│           │   ├── ### Official RtG Banners
│           │   └── ### Historical Logo Versions
│           ├── ## RtG-Preview
│           │   ├── ### Models
│           │   ├── ### Sounds
│           │   └── ### SVG
│           ├── ## Asset Guidelines
│           └── ## Related Documentation
│
├── page/
│   └── [no Markdown structure]
│
├── blocks/
│   ├── README.md
│   │   └── [headings]
│   │
│   └── parts/
│       ├── building/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── miscellaneous/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── other/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── physics/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── tools/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── uncategorized/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       ├── unused/
│       │   ├── README.md
│       │   │   └── [headings]
│       │   └── parts-id.md
│       │       └── [headings]
│       │
│       └── wiring/
│           ├── README.md
│           │   └── [headings]
│           └── parts-id.md
│               └── [headings]
│
├── format/
│   ├── README.md
│   │   ├── # Format Documentation
│   │   ├── ## Documents
│   │   ├── ## How These Documents Relate
│   │   ├── ## Related Documentation
│   │   └── ## Scope
│   ├── json-structure.md
│   │   └── [pending...]
│   ├── indexing.md
│   │   └── [pending...]
│   ├── properties.md
│   │   └── [pending...]
│   ├── identifiers.md
│   │   └── [pending...]
│   └── unknown-fields.md
│       └── [pending...]
│
├── compression/
│   ├── README.md
│   │   └── [pending...]
│   ├── overview.md
│   │   └── [pending...]
│   ├── encoding.md
│   │   └── [pending...]
│   └── examples-template.md
│       └── [pending...]
│
├── examples/
│   ├── README.md
│   │   └── [pending...]
│   ├── experiments/
│   │   └── README.md
│   │       └── [pending...]
│   ├── json-examples/
│   │   └── README.md
│   │       └── [pending...]
│   └── trash/
│       └── README.md
│           └── [pending...]
│
├── tools/
│   └── README.md
│       └── [pending...]
│
├── research/
│   ├── README.md
│   │   └── [pending...]
│   ├── methodology.md
│   │   └── [pending...]
│   ├── discoveries.md
│   │   └── [pending...]
│   └── unknowns.md
│       └── [pending...]
│
├── old-files/
│   ├── README.md
│   │   └── [headings]
│   ├── obj_ids-spanish.md
│   │   └── [headings]
│   └── RtG_Save_Format_Specification-spanish.md
│       └── [headings]
│
└── docs/
    ├── README.md
    │   ├── # Documentation
    │   └── ## Start Here
    │
    ├── getting-started.md
    │   ├── # Getting Started
    │   ├── ## Recommended Reading Order
    │   ├── ## After the Basics
    │   ├── ## Contributing
    │   └── ## Important Distinction
    │
    ├── save-anatomy.md
    │   ├── # Save Anatomy
    │   ├── ## Basic Structure
    │   │   ├── ### Type
    │   │   ├── ### Connections
    │   │   └── ### Properties
    │   ├── ## Object Relationships
    │   ├── ## Attachments and UUIDs
    │   ├── ## Encoding
    │   └── ## Where to Continue
    │
    ├── building-system.md
    │   ├── # Building System
    │   ├── ## Main Concepts
    │   ├── ## Parts and Object IDs
    │   ├── ## Format Representation
    │   ├── ## Attachments and Spatial Data
    │   └── ## Important Distinction
    │
    └── faq.md
        ├── # FAQ
        ├── ## What is this repository?
        ├── ## What is the current source of truth?
        ├── ## Why are there historical files?
        ├── ## Where are the Part IDs?
        ├── ## Where are the experiments?
        ├── ## Can I add an example JSON file?
        ├── ## Can experiments be deleted?
        ├── ## Where is encoding and compression documented?
        ├── ## Where are the tools?
        └── ## Is the project affiliated with Road To Gramby's?
```
