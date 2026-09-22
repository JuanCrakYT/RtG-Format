# Block: Splitter_3

## Identification
- **Name**: Splitter_3
- **Identifier**: `Splitter_3`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Splitter_3/Splitter_3.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Splitter_3/Splitter_3.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Connects to: Wire, Splitter
Signal distribution (3 out)

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Splitter_3/Splitter_3.json`
- `assets/models/model/Splitter_3/Splitter_3.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
Signal splitter with multiple outputs. Connection points need verification from model JSON.

No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
