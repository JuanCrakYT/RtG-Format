# Block: Switch

## Identification
- **Name**: Switch
- **Identifier**: `Switch`
- **Category**: Wiring
- **Model Available**: Yes
- **Model Path**: `assets/models/model/Switch/Switch.obj`
- **Tooltip**: Activates its output until switched off
- **Default Scale**: 1

## Connection Points
| Point ID | Name | Position | Rotation | Description | Status |
|----------|------|----------|----------|-------------|--------|
| 2 | Connection 2 | [0, 0.75, 0] | [0, 0, 130] | Branch attachment | CONFIRMED |


*Source: `assets/models/model/Switch/Switch.json` → LocalPoints*

## Branches

| Branch | Point ID | Model Path | Start Position | Start Rotation | Description |
|--------|----------|------------|----------------|----------------|-------------|
| output | 2 | ./split/output.obj | [0, 0.75, 0] | [0, 0, 130] | Attached at point 2 |
| input | NaN | ./split/input.obj | [0, 0.75, 0] | [0, 0, 130] | Free-floating branch |

*Source: `assets/models/model/Switch/Switch.json` → Branches, Branches Start*

## Properties
| Property | Type | Description | Known Values | Status |
|----------|------|-------------|--------------|--------|
| RGB | array[3] | Color (Red, Green, Blue) | [0-255, 0-255, 0-255] | CONFIRMED |
| EphemeralAttachments | object | Attachment points with CFrames | {UUID: {partName, cframe[12]}} | CONFIRMED |


## Relationships
Connects to: Wire, Splitter, Gate-AND, Gate-OR, Gate-NOT, Delayer, Detacher
Input branch (NaN): Receives signal
Output branch (2): Sends signal

## Confidence Level
- **Overall**: CONFIRMED

## Source Evidence
- `assets/models/model/Switch/Switch.json`
- `assets/models/model/Switch/Switch.obj`
- `assets/models/model/Switch/split/` (branch models)
- `old-files/obj_ids-spanish.md` (historical connection point data)
- Experimental saves in `examples/experiments/`

## Notes
Has two branches: input (NaN) and output (point 2). Input branch is free-floating, output attaches at connection point 2.
