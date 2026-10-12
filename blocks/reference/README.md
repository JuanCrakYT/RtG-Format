# RtG Block Reference Index

This directory contains structured documentation for all known RtG blocks (objects/parts).

Each block has its own documentation file with:

- Basic identification (name, identifier, model)
- Connection points
- Properties
- Known values
- Relationships
- Confidence level
- Source evidence

## Index by Category

### Building

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [Base](building/Base.md) | `Base` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [Chassis](building/Chassis.md) | `Chassis` | ✅ | 26 | RGB | CONFIRMED | Documented |
| [Hood](building/Hood.md) | `Hood` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Trunk](building/Trunk.md) | `Trunk` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Wheel](building/Wheel.md) | `Wheel` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Tire](building/Tire.md) | `Tire` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Bumper](building/Bumper.md) | `Bumper` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Wing](building/Wing.md) | `Wing` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [ShortStick](building/ShortStick.md) | `ShortStick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [Stick](building/Stick.md) | `Stick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [LongStick](building/LongStick.md) | `LongStick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Spoiler | `Spoiler` | ❓ | 1 | RGB | CONFIRMED | Documented |
| [FuelTank](building/FuelTank.md) | `FuelTank` | ✅ | 1 | RGB | CONFIRMED | Documented |
| [GasCap](building/GasCap.md) | `GasCap` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [Roof](building/Roof.md) | `Roof` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [DoorA](building/DoorA.md) | `DoorA` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| [DoorB](building/DoorB.md) | `DoorB` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| [DoorC](building/DoorC.md) | `DoorC` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| [DoorD](building/DoorD.md) | `DoorD` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |

### Physics

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [Servo](physics/Servo.md) | `Servo` | ✅ | ? | Speed, Rotation, LimitAngle, LimitEnabled, Backwards, Rest, MaxForce, ActivationSpeed, ActivationHeight | CONFIRMED | TODO |
| [Servo_Physics](physics/Servo_Physics.md) | `Servo_Physics` | ✅ | ? | | PARTIALLY CONFIRMED | TODO |
| [SpringJuice](physics/SpringJuice.md) | `SpringJuice` | ✅ | ? | | CONFIRMED | TODO |
| Suspension | `Suspension` | ❓ | ? | | UNKNOWN | TODO |
| [Gyro](physics/Gyro.md) | `Gyro` | ✅ | ? | | CONFIRMED | TODO |
| [SteeringGyro](physics/SteeringGyro.md) | `SteeringGyro` | ✅ | ? | | CONFIRMED | TODO |
| [StaringGyro](physics/StaringGyro.md) | `StaringGyro` | ✅ | ? | | CONFIRMED | TODO |
| [MatchingGyro](physics/MatchingGyro.md) | `MatchingGyro` | ✅ | ? | | CONFIRMED | TODO |
| [Thruster](physics/Thruster.md) | `Thruster` | ✅ | ? | Speed, MaxForce | CONFIRMED | TODO |
| [Propeller](physics/Propeller.md) | `Propeller` | ✅ | ? | Speed | CONFIRMED | TODO |
| Motor | `Motor` | ❓ | ? | | UNKNOWN | TODO |
| Engine | `Engine` | ❓ | ? | | UNKNOWN | TODO |

### Tools

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [ToolGun](tools/ToolGun.md) | `ToolGun` | ✅ | ? | | CONFIRMED | TODO |
| Wrench | `Wrench` | ❓ | ? | | UNKNOWN | TODO |
| PaintTool | `PaintTool` | ❓ | ? | | UNKNOWN | TODO |

### Wiring

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [Wire](wiring/Wire.md) | `Wire` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| [Rope](wiring/Rope.md) | `Rope` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| [Splitter](wiring/Splitter.md) | `Splitter` | ✅ | ? | | CONFIRMED | TODO |
| [Splitter_1](wiring/Splitter_1.md) | `Splitter_1` | ✅ | ? | | CONFIRMED | TODO |
| [Splitter_2](wiring/Splitter_2.md) | `Splitter_2` | ✅ | ? | | CONFIRMED | TODO |
| [Splitter_3](wiring/Splitter_3.md) | `Splitter_3` | ✅ | ? | | CONFIRMED | TODO |
| [Splitter_4](wiring/Splitter_4.md) | `Splitter_4` | ✅ | ? | | CONFIRMED | TODO |
| [Connector](wiring/Connector.md) | `Connector` | ✅ | ? | | CONFIRMED | TODO |
| [ConnectorBall](wiring/ConnectorBall.md) | `ConnectorBall` | ✅ | ? | | CONFIRMED | TODO |
| [HalfConnectorBall](wiring/HalfConnectorBall.md) | `HalfConnectorBall` | ✅ | ? | | CONFIRMED | TODO |
| [Switch](wiring/Switch.md) | `Switch` | ✅ | 2 (input, output) | | CONFIRMED | Documented |
| [Gate-AND](wiring/Gate-AND.md) | `Gate-AND` | ✅ | ? | | CONFIRMED | TODO |
| [Gate-OR](wiring/Gate-OR.md) | `Gate-OR` | ✅ | ? | | CONFIRMED | TODO |
| [Gate-NOT](wiring/Gate-NOT.md) | `Gate-NOT` | ✅ | ? | | CONFIRMED | TODO |
| [InputSensor](wiring/InputSensor.md) | `InputSensor` | ✅ | ? | | CONFIRMED | TODO |
| [EntitySensor](wiring/EntitySensor.md) | `EntitySensor` | ✅ | ? | | CONFIRMED | TODO |
| [VelocitySensor](wiring/VelocitySensor.md) | `VelocitySensor` | ✅ | ? | | CONFIRMED | TODO |
| [AltitudeSensor](wiring/AltitudeSensor.md) | `AltitudeSensor` | ✅ | ? | | CONFIRMED | TODO |
| [PressurePlate](wiring/PressurePlate.md) | `PressurePlate` | ✅ | ? | | CONFIRMED | TODO |
| [Button](wiring/Button.md) | `Button` | ✅ | ? | | CONFIRMED | TODO |
| [RemoteButton](wiring/RemoteButton.md) | `RemoteButton` | ✅ | ? | | CONFIRMED | TODO |
| [Delayer](wiring/Delayer.md) | `Delayer` | ✅ | ? | Delay, DelayDeactivation | CONFIRMED | TODO |
| [Detacher](wiring/Detacher.md) | `Detacher` | ✅ | ? | | CONFIRMED | TODO |
| [Recorder](wiring/Recorder.md) | `Recorder` | ✅ | ? | | CONFIRMED | TODO |

### Miscellaneous

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [Part](miscellaneous/Part.md) | `Part` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [Anchor](miscellaneous/Anchor.md) | `Anchor` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [Balloon](miscellaneous/Balloon.md) | `Balloon` | ✅ | ? | RGB | CONFIRMED | TODO |
| [BeachBall](miscellaneous/BeachBall.md) | `BeachBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| [BouncyBall](miscellaneous/BouncyBall.md) | `BouncyBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| [BowlingBall](miscellaneous/BowlingBall.md) | `BowlingBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| [BallSocket](miscellaneous/BallSocket.md) | `BallSocket` | ✅ | ? | | CONFIRMED | TODO |
| [Bearing](miscellaneous/Bearing.md) | `Bearing` | ✅ | ? | | CONFIRMED | TODO |
| [Board](miscellaneous/Board.md) | `Board` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Body](miscellaneous/Body.md) | `Body` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Briefcase](miscellaneous/Briefcase.md) | `Briefcase` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Camera](miscellaneous/Camera.md) | `Camera` | ✅ | ? | | CONFIRMED | TODO |
| [Canister](miscellaneous/Canister.md) | `Canister` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Cannon](miscellaneous/Cannon.md) | `Cannon` | ✅ | ? | Shooting, Bullets, CanTargetAttached, IgnoreAttached, MaxDistance, ActivationSpeed, ActivationHeight | CONFIRMED | TODO |
| [CannonBall](miscellaneous/CannonBall.md) | `CannonBall` | ✅ | ? | | CONFIRMED | TODO |
| [Carrot](miscellaneous/Carrot.md) | `Carrot` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Cinderblock](miscellaneous/Cinderblock.md) | `Cinderblock` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Drumkit](miscellaneous/Drumkit.md) | `Drumkit` | ✅ | ? | | CONFIRMED | TODO |
| [FishBowl](miscellaneous/FishBowl.md) | `FishBowl` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Fricklet](miscellaneous/Fricklet.md) | `Fricklet` | ✅ | ? | RGB | CONFIRMED | TODO |
| [GoldPotatoEngine](physics/GoldPotatoEngine.md) | `GoldPotatoEngine` | ✅ | ? | | CONFIRMED | TODO |
| [Googie](miscellaneous/Googie.md) | `Googie` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Gramby](miscellaneous/Gramby.md) | `Gramby` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Grenade](miscellaneous/Grenade.md) | `Grenade` | ✅ | ? | | CONFIRMED | TODO |
| [Guitar](miscellaneous/Guitar.md) | `Guitar` | ✅ | ? | | CONFIRMED | TODO |
| [Gun](miscellaneous/Gun.md) | `Gun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| [Head](miscellaneous/Head.md) | `Head` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Jug](miscellaneous/Jug.md) | `Jug` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Keyboard](miscellaneous/Keyboard.md) | `Keyboard` | ✅ | ? | | CONFIRMED | TODO |
| [Leafblower](miscellaneous/Leafblower.md) | `Leafblower` | ✅ | ? | | CONFIRMED | TODO |
| [Leg](miscellaneous/Leg.md) | `Leg` | ✅ | ? | | CONFIRMED | TODO |
| [Light](miscellaneous/Light.md) | `Light` | ✅ | ? | RGB, Volume | CONFIRMED | TODO |
| [Lock](miscellaneous/Lock.md) | `Lock` | ✅ | ? | | CONFIRMED | TODO |
| [Looper](miscellaneous/Looper.md) | `Looper` | ✅ | ? | | CONFIRMED | TODO |
| [Mag](miscellaneous/Mag.md) | `Mag` | ✅ | ? | Quantity, Bullets | CONFIRMED | TODO |
| [MountedGun](miscellaneous/MountedGun.md) | `MountedGun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| [Pipes](miscellaneous/Pipes.md) | `Pipes` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Piston](miscellaneous/Piston.md) | `Piston` | ✅ | ? | | CONFIRMED | TODO |
| [Plunger](miscellaneous/Plunger.md) | `Plunger` | ✅ | ? | | CONFIRMED | TODO |
| [Poop](miscellaneous/Poop.md) | `Poop` | ✅ | ? | RGB | CONFIRMED | TODO |
| [PotatoEngine](physics/PotatoEngine.md) | `PotatoEngine` | ✅ | ? | Speed | CONFIRMED | TODO |
| [Radio](miscellaneous/Radio.md) | `Radio` | ✅ | ? | Volume, Channel, CustomTrack | CONFIRMED | TODO |
| [Ramp](miscellaneous/Ramp.md) | `Ramp` | ✅ | ? | RGB | CONFIRMED | TODO |
| [RiotShield](miscellaneous/RiotShield.md) | `RiotShield` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Rocket](miscellaneous/Rocket.md) | `Rocket` | ✅ | ? | Speed | CONFIRMED | TODO |
| [RockingChair](miscellaneous/RockingChair.md) | `RockingChair` | ✅ | ? | RGB | CONFIRMED | TODO |
| [RPG](miscellaneous/RPG.md) | `RPG` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| [RubberBand](miscellaneous/RubberBand.md) | `RubberBand` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| [Seat](miscellaneous/Seat.md) | `Seat` | ✅ | ? | RGB | CONFIRMED | TODO |
| [ShoppingCart](miscellaneous/ShoppingCart.md) | `ShoppingCart` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Shotgun](miscellaneous/Shotgun.md) | `Shotgun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| [Sledge](miscellaneous/Sledge.md) | `Sledge` | ✅ | ? | RGB | CONFIRMED | TODO |
| [SprayPaint](miscellaneous/SprayPaint.md) | `SprayPaint` | ✅ | ? | RGB | CONFIRMED | TODO |
| [SuperPowerClock](miscellaneous/SuperPowerClock.md) | `SuperPowerClock` | ✅ | ? | | CONFIRMED | TODO |
| [Tooth](miscellaneous/Tooth.md) | `Tooth` | ✅ | 0 | RGB | CONFIRMED | Documented |
| [TripWire](miscellaneous/TripWire.md) | `TripWire` | ✅ | ? | | CONFIRMED | TODO |
| [Trowel](miscellaneous/Trowel.md) | `Trowel` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Trumpet](miscellaneous/Trumpet.md) | `Trumpet` | ✅ | ? | | CONFIRMED | TODO |
| [TV](miscellaneous/TV.md) | `TV` | ✅ | ? | ImageId | CONFIRMED | TODO |
| [Uzi](miscellaneous/Uzi.md) | `Uzi` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| [wad](miscellaneous/wad.md) | `wad` | ✅ | ? | | CONFIRMED | TODO |

### Other

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| [Arm](other/Arm.md) | `Arm` | ✅ | ? | RGB | CONFIRMED | TODO |
| [Banjo](other/Banjo.md) | `Banjo` | ✅ | ? | RGB | CONFIRMED | TODO |
| Teeth | `Teeth` | ❓ | ? | | UNKNOWN | TODO |
| [Banjo](other/Banjo.md) | `Banjo` | ✅ | ? | RGB | CONFIRMED | TODO |

### Uncategorized / Unused

| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| (various) | | | | | UNKNOWN | TODO |

## Category directories

| Category | Purpose | Index |
| --- | --- | --- |
| Building | Vehicle and construction pieces | [Building](building/README.md) |
| Physics | Motion and physics-related blocks | [Physics](physics/README.md) |
| Tools | Tool blocks | [Tools](tools/README.md) |
| Wiring | Signals, gates, and connection logic | [Wiring](wiring/README.md) |
| Miscellaneous | Miscellaneous objects and props | [Miscellaneous](miscellaneous/README.md) |
| Other | Objects not assigned to another category by the generator | [Other](other/README.md) |

## Individual block pages

Each object page lives in the subdirectory matching its category and follows the [block reference template](template.md). The template is a structure guide, not evidence; include only values supported by the relevant model files, save samples, or reproducible experiments.

## Generating Documentation

Run the generation script to create/update block documentation from model JSONs:

```bash
node scripts/generate-block-docs.js
```

## Confidence Definitions

| Level | Definition |
|-------|------------|
| CONFIRMED | Directly observed and reproducible through controlled experiments |
| PARTIALLY CONFIRMED | Some experimental evidence exists but not fully verified |
| UNCONFIRMED | Reported or suspected but lacking sufficient experimental evidence |
| UNKNOWN | No data available in current research |

## Related Documentation

- `blocks/parts/` — Organized Part IDs by category (connection point tables)
- `format/identifiers.md` — Identifier system documentation
- `format/properties.md` — Property behavior documentation
- `SPECIFICATION.md` — Consolidated format specification
- `old-files/` — Historical reverse-engineering evidence
