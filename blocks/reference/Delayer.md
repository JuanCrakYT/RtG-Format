# Block: Delayer

## Identification
- **Name**: Delayer
- **Identifier**: `Delayer`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Delayer/Delayer.obj`
- **Tooltip**: '
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Delayer/Delayer.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |
| Delay | number | Activation delay | seconds | CONFIRMED |
| DelayDeactivation | number | Deactivation delay | seconds | CONFIRMED |


## Relationships
Relationships not fully documented. See SPECIFICATION.md for general connection rules.

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Delayer/Delayer.json`
- `assets/models/model/Delayer/Delayer.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
