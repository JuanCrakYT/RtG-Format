# Block: MountedGun

## Identification
- **Name**: MountedGun
- **Identifier**: `MountedGun`
- **Category**: Miscellaneous
- **Model Available**: Yes
- **Model Path**: `assets/models/model/MountedGun/MountedGun.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/MountedGun/MountedGun.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |
| Shooting | boolean | Whether firing | true/false | CONFIRMED |
| Bullets | number | Ammo count | 0-100 | CONFIRMED |


## Relationships
Relationships not fully documented. See SPECIFICATION.md for general connection rules.

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/MountedGun/MountedGun.json`
- `assets/models/model/MountedGun/MountedGun.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
