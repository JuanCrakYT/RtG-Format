# Block: Servo

## Identification
- **Name**: Servo
- **Identifier**: `Servo`
- **Category**: Physics
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Servo/Servo.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Servo/Servo.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |
| Speed | number | Rotation speed | 0-1000 | CONFIRMED |
| Rotation | number | Target rotation | degrees | CONFIRMED |
| LimitAngle | number | Angle limit | degrees | CONFIRMED |
| LimitEnabled | boolean | Whether limit is active | true/false | CONFIRMED |
| Backwards | boolean | Reverse direction | true/false | CONFIRMED |
| Rest | number | Rest position | degrees | CONFIRMED |
| MaxForce | number | Maximum force | 0-10000 | CONFIRMED |


## Relationships
Connects to: Part, Chassis, Body
Rotational joint

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Servo/Servo.json`
- `assets/models/model/Servo/Servo.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
