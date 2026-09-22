# Block: Tooth

## Identification
- **Name**: Tooth
- **Identifier**: `Tooth`
- **Category**: Miscellaneous
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Tooth/Tooth.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Tooth/Tooth.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Relationships not fully documented. See SPECIFICATION.md for general connection rules.

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Tooth/Tooth.json`
- `assets/models/model/Tooth/Tooth.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
Standard block. Connection points and properties per model JSON. See SPECIFICATION.md for format details.
