# Block: AltitudeSensor

## Identification
- **Name**: AltitudeSensor
- **Identifier**: `AltitudeSensor`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/AltitudeSensor/AltitudeSensor.obj`
- **Tooltip**: N/A
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| 1 | Connection 1 | [0, 2, 0] | [0, 0, 0] | Standard connection | CONFIRMED |


*Source: `assets/models/model/AltitudeSensor/AltitudeSensor.json` → LocalPoints*

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
- `assets/models/model/AltitudeSensor/AltitudeSensor.json`
- `assets/models/model/AltitudeSensor/AltitudeSensor.obj`
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
Standard block. Connection points and properties per model JSON. See SPECIFICATION.md for format details.
