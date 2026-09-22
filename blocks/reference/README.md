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
| Base | `Base` | ✅ | 0 | RGB | CONFIRMED | Documented |
| Chassis | `Chassis` | ✅ | 26 | RGB | CONFIRMED | Documented |
| Hood | `Hood` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Trunk | `Trunk` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Wheel | `Wheel` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Tire | `Tire` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Bumper | `Bumper` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Wing | `Wing` | ✅ | 1 | RGB | CONFIRMED | Documented |
| ShortStick | `ShortStick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Stick | `Stick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| LongStick | `LongStick` | ✅ | 1 | RGB | CONFIRMED | Documented |
| Spoiler | `Spoiler` | ❓ | 1 | RGB | CONFIRMED | Documented |
| FuelTank | `FuelTank` | ✅ | 1 | RGB | CONFIRMED | Documented |
| GasCap | `GasCap` | ✅ | 0 | RGB | CONFIRMED | Documented |
| Roof | `Roof` | ✅ | 0 | RGB | CONFIRMED | Documented |
| DoorA | `DoorA` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| DoorB | `DoorB` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| DoorC | `DoorC` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |
| DoorD | `DoorD` | ✅ | ? | RGB | PARTIALLY CONFIRMED | TODO |

### Physics
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| Servo | `Servo` | ✅ | ? | Speed, Rotation, LimitAngle, LimitEnabled, Backwards, Rest, MaxForce, ActivationSpeed, ActivationHeight | CONFIRMED | TODO |
| Servo_Physics | `Servo_Physics` | ✅ | ? | | PARTIALLY CONFIRMED | TODO |
| SpringJuice | `SpringJuice` | ✅ | ? | | CONFIRMED | TODO |
| Suspension | `Suspension` | ❓ | ? | | UNKNOWN | TODO |
| Gyro | `Gyro` | ✅ | ? | | CONFIRMED | TODO |
| SteeringGyro | `SteeringGyro` | ✅ | ? | | CONFIRMED | TODO |
| StaringGyro | `StaringGyro` | ✅ | ? | | CONFIRMED | TODO |
| MatchingGyro | `MatchingGyro` | ✅ | ? | | CONFIRMED | TODO |
| Thruster | `Thruster` | ✅ | ? | Speed, MaxForce | CONFIRMED | TODO |
| Propeller | `Propeller` | ✅ | ? | Speed | CONFIRMED | TODO |
| Motor | `Motor` | ❓ | ? | | UNKNOWN | TODO |
| Engine | `Engine` | ❓ | ? | | UNKNOWN | TODO |

### Tools
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| ToolGun | `ToolGun` | ✅ | ? | | CONFIRMED | TODO |
| Wrench | `Wrench` | ❓ | ? | | UNKNOWN | TODO |
| PaintTool | `PaintTool` | ❓ | ? | | UNKNOWN | TODO |

### Wiring
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| Wire | `Wire` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| Rope | `Rope` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| Splitter | `Splitter` | ✅ | ? | | CONFIRMED | TODO |
| Splitter_1 | `Splitter_1` | ✅ | ? | | CONFIRMED | TODO |
| Splitter_2 | `Splitter_2` | ✅ | ? | | CONFIRMED | TODO |
| Splitter_3 | `Splitter_3` | ✅ | ? | | CONFIRMED | TODO |
| Splitter_4 | `Splitter_4` | ✅ | ? | | CONFIRMED | TODO |
| Connector | `Connector` | ✅ | ? | | CONFIRMED | TODO |
| ConnectorBall | `ConnectorBall` | ✅ | ? | | CONFIRMED | TODO |
| HalfConnectorBall | `HalfConnectorBall` | ✅ | ? | | CONFIRMED | TODO |
| Switch | `Switch` | ✅ | 2 (input, output) | | CONFIRMED | Documented |
| Gate-AND | `Gate-AND` | ✅ | ? | | CONFIRMED | TODO |
| Gate-OR | `Gate-OR` | ✅ | ? | | CONFIRMED | TODO |
| Gate-NOT | `Gate-NOT` | ✅ | ? | | CONFIRMED | TODO |
| InputSensor | `InputSensor` | ✅ | ? | | CONFIRMED | TODO |
| EntitySensor | `EntitySensor` | ✅ | ? | | CONFIRMED | TODO |
| VelocitySensor | `VelocitySensor` | ✅ | ? | | CONFIRMED | TODO |
| AltitudeSensor | `AltitudeSensor` | ✅ | ? | | CONFIRMED | TODO |
| PressurePlate | `PressurePlate` | ✅ | ? | | CONFIRMED | TODO |
| Button | `Button` | ✅ | ? | | CONFIRMED | TODO |
| RemoteButton | `RemoteButton` | ✅ | ? | | CONFIRMED | TODO |
| Delayer | `Delayer` | ✅ | ? | Delay, DelayDeactivation | CONFIRMED | TODO |
| Detacher | `Detacher` | ✅ | ? | | CONFIRMED | TODO |
| Recorder | `Recorder` | ✅ | ? | | CONFIRMED | TODO |

### Miscellaneous
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| Part | `Part` | ✅ | 0 | RGB | CONFIRMED | Documented |
| Anchor | `Anchor` | ✅ | 0 | RGB | CONFIRMED | Documented |
| Balloon | `Balloon` | ✅ | ? | RGB | CONFIRMED | TODO |
| BeachBall | `BeachBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| BouncyBall | `BouncyBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| BowlingBall | `BowlingBall` | ✅ | ? | RGB | CONFIRMED | TODO |
| BallSocket | `BallSocket` | ✅ | ? | | CONFIRMED | TODO |
| Bearing | `Bearing` | ✅ | ? | | CONFIRMED | TODO |
| Board | `Board` | ✅ | ? | RGB | CONFIRMED | TODO |
| Body | `Body` | ✅ | ? | RGB | CONFIRMED | TODO |
| Briefcase | `Briefcase` | ✅ | ? | RGB | CONFIRMED | TODO |
| Camera | `Camera` | ✅ | ? | | CONFIRMED | TODO |
| Canister | `Canister` | ✅ | ? | RGB | CONFIRMED | TODO |
| Cannon | `Cannon` | ✅ | ? | Shooting, Bullets, CanTargetAttached, IgnoreAttached, MaxDistance, ActivationSpeed, ActivationHeight | CONFIRMED | TODO |
| CannonBall | `CannonBall` | ✅ | ? | | CONFIRMED | TODO |
| Carrot | `Carrot` | ✅ | ? | RGB | CONFIRMED | TODO |
| Cinderblock | `Cinderblock` | ✅ | ? | RGB | CONFIRMED | TODO |
| Drumkit | `Drumkit` | ✅ | ? | | CONFIRMED | TODO |
| FishBowl | `FishBowl` | ✅ | ? | RGB | CONFIRMED | TODO |
| Fricklet | `Fricklet` | ✅ | ? | RGB | CONFIRMED | TODO |
| GoldPotatoEngine | `GoldPotatoEngine` | ✅ | ? | | CONFIRMED | TODO |
| Googie | `Googie` | ✅ | ? | RGB | CONFIRMED | TODO |
| Gramby | `Gramby` | ✅ | ? | RGB | CONFIRMED | TODO |
| Grenade | `Grenade` | ✅ | ? | | CONFIRMED | TODO |
| Guitar | `Guitar` | ✅ | ? | | CONFIRMED | TODO |
| Gun | `Gun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| Head | `Head` | ✅ | ? | RGB | CONFIRMED | TODO |
| Jug | `Jug` | ✅ | ? | RGB | CONFIRMED | TODO |
| Keyboard | `Keyboard` | ✅ | ? | | CONFIRMED | TODO |
| Leafblower | `Leafblower` | ✅ | ? | | CONFIRMED | TODO |
| Leg | `Leg` | ✅ | ? | | CONFIRMED | TODO |
| Light | `Light` | ✅ | ? | RGB, Volume | CONFIRMED | TODO |
| Lock | `Lock` | ✅ | ? | | CONFIRMED | TODO |
| Looper | `Looper` | ✅ | ? | | CONFIRMED | TODO |
| Mag | `Mag` | ✅ | ? | Quantity, Bullets | CONFIRMED | TODO |
| MountedGun | `MountedGun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| Pipes | `Pipes` | ✅ | ? | RGB | CONFIRMED | TODO |
| Piston | `Piston` | ✅ | ? | | CONFIRMED | TODO |
| Plunger | `Plunger` | ✅ | ? | | CONFIRMED | TODO |
| Poop | `Poop` | ✅ | ? | RGB | CONFIRMED | TODO |
| PotatoEngine | `PotatoEngine` | ✅ | ? | Speed | CONFIRMED | TODO |
| Radio | `Radio` | ✅ | ? | Volume, Channel, CustomTrack | CONFIRMED | TODO |
| Ramp | `Ramp` | ✅ | ? | RGB | CONFIRMED | TODO |
| RiotShield | `RiotShield` | ✅ | ? | RGB | CONFIRMED | TODO |
| Rocket | `Rocket` | ✅ | ? | Speed | CONFIRMED | TODO |
| RockingChair | `RockingChair` | ✅ | ? | RGB | CONFIRMED | TODO |
| RPG | `RPG` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| RubberBand | `RubberBand` | ✅ | ? | Length, MinLength, MaxLength, MaxForce | CONFIRMED | TODO |
| Seat | `Seat` | ✅ | ? | RGB | CONFIRMED | TODO |
| ShoppingCart | `ShoppingCart` | ✅ | ? | RGB | CONFIRMED | TODO |
| Shotgun | `Shotgun` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| Sledge | `Sledge` | ✅ | ? | RGB | CONFIRMED | TODO |
| SprayPaint | `SprayPaint` | ✅ | ? | RGB | CONFIRMED | TODO |
| SuperPowerClock | `SuperPowerClock` | ✅ | ? | | CONFIRMED | TODO |
| Tooth | `Tooth` | ✅ | 0 | RGB | CONFIRMED | Documented |
| TripWire | `TripWire` | ✅ | ? | | CONFIRMED | TODO |
| Trowel | `Trowel` | ✅ | ? | RGB | CONFIRMED | TODO |
| Trumpet | `Trumpet` | ✅ | ? | | CONFIRMED | TODO |
| TV | `TV` | ✅ | ? | ImageId | CONFIRMED | TODO |
| Uzi | `Uzi` | ✅ | ? | Shooting, Bullets | CONFIRMED | TODO |
| wad | `wad` | ✅ | ? | | CONFIRMED | TODO |

### Other
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| Arm | `Arm` | ✅ | ? | RGB | CONFIRMED | TODO |
| Banjo | `Banjo` | ✅ | ? | RGB | CONFIRMED | TODO |
| Teeth | `Teeth` | ❓ | ? | | UNKNOWN | TODO |
| Banjo | `Banjo` | ✅ | ? | RGB | CONFIRMED | TODO |

### Uncategorized / Unused
| Block | Identifier | Model | Connection Points | Properties | Confidence | Status |
|-------|------------|-------|-------------------|------------|------------|--------|
| (various) | | | | | UNKNOWN | TODO |

## Documentation Template

Each block should have a file in `blocks/reference/` following this template:

```markdown
# Block: [Display Name]

## Identification
- **Name**: [Display name]
- **Identifier**: [Internal identifier used in JSON]
- **Category**: [Building/Physics/Tools/Wiring/Miscellaneous/Other/Uncategorized]
- **Model Available**: Yes/No
- **Model Path**: `assets/models/model/[Name]/[Name].obj`

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| 1 | MountPoint | [x,y,z] | [rx,ry,rz] | Main connection point | CONFIRMED |

*Source: `assets/models/model/[Name]/[Name].json` → LocalPoints*

## Branches (if applicable)
| Branch | Point ID | Model Path | Start Transform | Description |
|--------|----------|------------|-----------------|-------------|
| output | 2 | ./split/output.obj | [pos], [rot] | Output branch |

*Source: `assets/models/model/[Name]/[Name].json` → Branches, Branches Start*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color | [0-255, 0-255, 0-255] | CONFIRMED |
| Speed | number | Movement speed | 0-1000 | CONFIRMED |

## Relationships
- **Connects to**: [List of block types this commonly connects to]
- **Parent of**: [Blocks typically parented to this]
- **Child of**: [Blocks typically parent to this]

## Confidence Level
- **CONFIRMED**: Directly observed, reproducible
- **PARTIALLY CONFIRMED**: Some evidence, not fully verified
- **UNCONFIRMED**: Reported but lacking evidence
- **UNKNOWN**: No data available

## Source Evidence
- `assets/models/model/[Name]/[Name].json`
- `assets/models/model/[Name]/[Name].obj`
- `old-files/obj_ids-spanish.md`
- Experimental saves in `examples/experiments/`

## Notes
[Any additional observations, hypotheses, or unresolved questions]
```

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