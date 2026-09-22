# Block: Chassis

## Identification
- **Name**: Chassis
- **Identifier**: `Chassis`
- **Category**: Building
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Chassis/Chassis.obj`
- **Tooltip**: The root of all cars
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Chassis/Chassis.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Connects to: Wheel, Hood, Trunk, Engine, Seat, SteeringWheel, GasCap, Roof, Bumper, Headlight, BrakeLight
Parent of: Wheel, Hood, Trunk, Engine, Seat
Child of: Base

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Chassis/Chassis.json`
- `assets/models/model/Chassis/Chassis.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
