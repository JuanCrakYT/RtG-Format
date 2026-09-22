# Block: ToolGun

## Identification
- **Name**: ToolGun
- **Identifier**: `ToolGun`
- **Category**: Tools
- **Model Available**: Yes
- **Model Path**: `assets/models/model/ToolGun/ToolGun.obj`
- **Tooltip**: Any creator's dream! Has several modes to aid in building.
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/ToolGun/ToolGun.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Relationships not fully documented. See SPECIFICATION.md for general connection rules.

## Confidence Level
- **Overall**: PARTIALLY CONFIRMED (model exists, properties need verification)

## Source Evidence
- `assets/models/model/ToolGun/ToolGun.json`
- `assets/models/model/ToolGun/ToolGun.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
