# Block: Rope

## Identification
- **Name**: Rope
- **Identifier**: `Rope`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Rope/Rope.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Rope/Rope.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |
| Length | number | Current length | 0-1000 | CONFIRMED |
| MinLength | number | Minimum length | 0-1000 | CONFIRMED |
| MaxLength | number | Maximum length | 0-1000 | CONFIRMED |
| MaxForce | number | Maximum force | 0-10000 | CONFIRMED |


## Relationships
Connects to: Connector, ConnectorBall, Part
Flexible connection

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Rope/Rope.json`
- `assets/models/model/Rope/Rope.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
