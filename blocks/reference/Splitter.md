# Block: Splitter

## Identification
- **Name**: Splitter
- **Identifier**: `Splitter`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Splitter/Splitter.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| (none) | | | | No predefined connection points | |


*Source: `assets/models/model/Splitter/Splitter.json` → LocalPoints*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Connects to: Wire, Splitter
Signal distribution

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Splitter/Splitter.json`
- `assets/models/model/Splitter/Splitter.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
Signal splitter with multiple outputs. Connection points need verification from model JSON.

No predefined connection points (LocalPoints empty). May use UUID/EphemeralAttachments for connections.
