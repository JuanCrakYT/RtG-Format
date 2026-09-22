# Block: Servo_Physics

## Identification
- **Name**: Servo_Physics
- **Identifier**: `Servo_Physics`
- **Category**: Physics
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Servo_Physics/Servo_Physics.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Servo_Physics/Servo_Physics.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |
| Speed | number | Rotation speed | 0-1000 | CONFIRMED |
| Rotation | number | Target rotation | degrees | CONFIRMED |


## Relationships
Relationships not fully documented. See SPECIFICATION.md for general connection rules.

## Confidence Level
- **Overall**: PARTIALLY CONFIRMED (model exists, properties need verification)

## Source Evidence
- `assets/models/model/Servo_Physics/Servo_Physics.json`
- `assets/models/model/Servo_Physics/Servo_Physics.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
