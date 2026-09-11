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
│   │   ├─ AltitudeSensor/
│   │   │  └─ AltitudeSensor.obj
│   │   ├─ Anchor/
│   │   │  └─ Anchor.obj
│   │   ├─ Arm/
│   │   │  └─ Arm.obj
│   │   ├─ Balloon/
│   │   │  └─ Balloon.obj
│   │   ├─ BallSocket/
│   │   │  └─ BallSocket.obj
│   │   ├─ Banjo/
│   │   │  └─ Banjo.obj
│   │   ├─ Base/
│   │   │  └─ Base.obj
│   │   ├─ BeachBall/
│   │   │  └─ BeachBall.obj
│   │   ├─ Bearing/
│   │   │  └─ Bearing.obj
│   │   ├─ Board/
│   │   │  └─ Board.obj
│   │   ├─ Body/
│   │   │  └─ Body.obj
│   │   ├─ BouncyBall/
│   │   │  └─ BouncyBall.obj
│   │   ├─ BowlingBall/
│   │   │  └─ BowlingBall.obj
│   │   ├─ BrakeLight/
│   │   │  └─ BrakeLight.obj
│   │   ├─ Briefcase/
│   │   │  └─ Briefcase.obj
│   │   ├─ Bumper/
│   │   │  └─ Bumper.obj
│   │   ├─ Button/
│   │   │  └─ Button.obj
│   │   ├─ Camera/
│   │   │  └─ Camera.obj
│   │   ├─ Canister/
│   │   │  └─ Canister.obj
│   │   ├─ Cannon/
│   │   │  └─ Cannon.obj
│   │   ├─ CannonBall/
│   │   │  └─ CannonBall.obj
│   │   ├─ Carrot/
│   │   │  └─ Carrot.obj
│   │   ├─ Chassis/
│   │   │  └─ Chassis.obj
│   │   ├─ Cinderblock/
│   │   │  └─ Cinderblock.obj
│   │   ├─ Connector/
│   │   │  └─ Connector.obj
│   │   ├─ ConnectorBall/
│   │   │  └─ ConnectorBall.obj
│   │   ├─ Delayer/
│   │   │  └─ Delayer.obj
│   │   ├─ Detacher/
│   │   │  └─ Detacher.obj
│   │   ├─ DoorA/
│   │   │  └─ DoorA.obj
│   │   ├─ DoorB/
│   │   │  └─ DoorB.obj
│   │   ├─ DoorC/
│   │   │  └─ DoorC.obj
│   │   ├─ DoorD/
│   │   │  └─ DoorD.obj
│   │   ├─ Drumkit/
│   │   │  └─ Drumkit.obj
│   │   ├─ EntitySensor/
│   │   │  └─ EntitySensor.obj
│   │   ├─ FishBowl/
│   │   │  └─ FishBowl.obj
│   │   ├─ Fricklet/
│   │   │  └─ Fricklet.obj
│   │   ├─ FuelTank/
│   │   │  └─ FuelTank.obj
│   │   ├─ GasCap/
│   │   │  └─ GasCap.obj
│   │   ├─ Gate-AND/
│   │   │  └─ Gate-AND.obj
│   │   ├─ Gate-NOT/
│   │   │  └─ Gate-NOT.obj
│   │   ├─ Gate-OR/
│   │   │  └─ Gate-OR.obj
│   │   ├─ GoldPotatoEngine/
│   │   │  └─ GoldPotatoEngine.obj
│   │   ├─ Googie/
│   │   │  └─ Googie.obj
│   │   ├─ Gramby/
│   │   │  └─ Gramby.obj
│   │   ├─ Grenade/
│   │   │  └─ Grenade.obj
│   │   ├─ Guitar/
│   │   │  └─ Guitar.obj
│   │   ├─ Gun/
│   │   │  └─ Gun.obj
│   │   ├─ Gyro/
│   │   │  └─ Gyro.obj
│   │   ├─ HalfConnectorBall/
│   │   │  └─ HalfConnectorBall.obj
│   │   ├─ Head/
│   │   │  └─ Head.obj
│   │   ├─ Hood/
│   │   │  └─ Hood.obj
│   │   ├─ InputSensor/
│   │   │  └─ InputSensor.obj
│   │   ├─ Joint/
│   │   │  └─ Joint.obj
│   │   ├─ Joust/
│   │   │  └─ Joust.obj
│   │   ├─ Jug/
│   │   │  └─ Jug.obj
│   │   ├─ Keyboard/
│   │   │  └─ Keyboard.obj
│   │   ├─ Leafblower/
│   │   │  └─ Leafblower.obj
│   │   ├─ Leg/
│   │   │  └─ Leg.obj
│   │   ├─ Light/
│   │   │  └─ Light.obj
│   │   ├─ Lock/
│   │   │  └─ Lock.obj
│   │   ├─ LongStick/
│   │   │  └─ LongStick.obj
│   │   ├─ Looper/
│   │   │  └─ Looper.obj
│   │   ├─ Mag/
│   │   │  └─ Mag.obj
│   │   ├─ MatchingGyro/
│   │   │  └─ MatchingGyro.obj
│   │   ├─ MountedGun/
│   │   │  └─ MountedGun.obj
│   │   ├─ Part/
│   │   │  └─ Part.obj
│   │   ├─ Pie/
│   │   │  └─ Pie.obj
│   │   ├─ Pipes/
│   │   │  └─ Pipes.obj
│   │   ├─ Piston/
│   │   │  └─ Piston.obj
│   │   ├─ Plunger/
│   │   │  └─ Plunger.obj
│   │   ├─ Poop/
│   │   │  └─ Poop.obj
│   │   ├─ PotatoEngine/
│   │   │  └─ PotatoEngine.obj
│   │   ├─ PressurePlate/
│   │   │  └─ PressurePlate.obj
│   │   ├─ Propeller/
│   │   │  └─ Propeller.obj
│   │   ├─ Radio/
│   │   │  └─ Radio.obj
│   │   ├─ Ramp/
│   │   │  └─ Ramp.obj
│   │   ├─ Recorder/
│   │   │  └─ Recorder.obj
│   │   ├─ RemoteButton/
│   │   │  └─ RemoteButton.obj
│   │   ├─ RiotShield/
│   │   │  └─ RiotShield.obj
│   │   ├─ Rocket/
│   │   │  └─ Rocket.obj
│   │   ├─ RockingChair/
│   │   │  └─ RockingChair.obj
│   │   ├─ Roof/
│   │   │  └─ Roof.obj
│   │   ├─ Rope/
│   │   │  └─ Rope.obj
│   │   ├─ RPG/
│   │   │  └─ RPG.obj
│   │   ├─ RubberBand/
│   │   │  └─ RubberBand.obj
│   │   ├─ Seat/
│   │   │  └─ Seat.obj
│   │   ├─ Servo/
│   │   │  └─ Servo.obj
│   │   ├─ Servo_Physics/
│   │   │  └─ Servo_Physics.obj
│   │   ├─ ShoppingCart/
│   │   │  └─ ShoppingCart.obj
│   │   ├─ ShortStick/
│   │   │  └─ ShortStick.obj
│   │   ├─ Shotgun/
│   │   │  └─ Shotgun.obj
│   │   ├─ Sledge/
│   │   │  └─ Sledge.obj
│   │   ├─ Splitter/
│   │   │  └─ Splitter.obj
│   │   ├─ Splitter_1/
│   │   │  └─ Splitter_1.obj
│   │   ├─ Splitter_2/
│   │   │  └─ Splitter_2.obj
│   │   ├─ Splitter_3/
│   │   │  └─ Splitter_3.obj
│   │   ├─ Splitter_4/
│   │   │  └─ Splitter_4.obj
│   │   ├─ SprayPaint/
│   │   │  └─ SprayPaint.obj
│   │   ├─ SpringJuice/
│   │   │  └─ SpringJuice.obj
│   │   ├─ StaringGyro/
│   │   │  └─ StaringGyro.obj
│   │   ├─ SteeringGyro/
│   │   │  └─ SteeringGyro.obj
│   │   ├─ SteeringWheel/
│   │   │  └─ SteeringWheel.obj
│   │   ├─ Stick/
│   │   │  └─ Stick.obj
│   │   ├─ SuperPowerClock/
│   │   │  └─ SuperPowerClock.obj
│   │   ├─ Switch/
│   │   │  └─ Switch.obj
│   │   ├─ Thruster/
│   │   │  └─ Thruster.obj
│   │   ├─ Tire/
│   │   │  └─ Tire.obj
│   │   ├─ ToolGun/
│   │   │  └─ ToolGun.obj
│   │   ├─ Tooth/
│   │   │  └─ Tooth.obj
│   │   ├─ TripWire/
│   │   │  └─ TripWire.obj
│   │   ├─ Trowel/
│   │   │  └─ Trowel.obj
│   │   ├─ Trumpet/
│   │   │  └─ Trumpet.obj
│   │   ├─ Trunk/
│   │   │  └─ Trunk.obj
│   │   ├─ TV/
│   │   │  └─ TV.obj
│   │   ├─ Uzi/
│   │   │  └─ Uzi.obj
│   │   ├─ VelocitySensor/
│   │   │  └─ VelocitySensor.obj
│   │   ├─ wad/
│   │   │  └─ wad.obj
│   │   ├─ Wheel/
│   │   │  └─ Wheel.obj
│   │   ├─ Wing/
│   │   │  └─ Wing.obj
│   │   ├─ Wire/
│   │   │  └─ Wire.obj
│   │   └─ ALL.blend
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
