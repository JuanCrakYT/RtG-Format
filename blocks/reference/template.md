# Block Reference Template

Use this template when adding or substantially restructuring a page in this directory. Keep only fields supported by evidence; delete inapplicable sections instead of filling them with guesses.

# Block: [Display Name]

## Identification

- **Name**: [Display name]
- **Identifier**: [Internal identifier used in JSON]
- **Category**: [Building/Physics/Tools/Wiring/Miscellaneous/Other/Uncategorized]
- **Model Available**: Yes/No
- **Model Path**: `assets/models/model/[Name]/[Name].obj`

## Connection Points

| Point ID | Name       | Position | Rotation   | Description           | Status    |
| -------- | ---------- | -------- | ---------- | --------------------- | --------- |
| 1        | MountPoint | [x,y,z]  | [rx,ry,rz] | Main connection point | CONFIRMED |

*Source: `assets/models/model/[Name]/[Name].json` → LocalPoints*

## Branches (if applicable)

| Branch | Point ID | Model Path         | Start Transform | Description   |
| ------ | -------- | ------------------ | --------------- | ------------- |
| output | 2        | ./split/output.obj | [pos], [rot]    | Output branch |

*Source: `assets/models/model/[Name]/[Name].json` → Branches, Branches Start*

## Properties

| Property | Type     | Description    | Known Values          | Status    |
| -------- | -------- | -------------- | --------------------- | --------- |
| RGB      | array[3] | Color          | [0-255, 0-255, 0-255] | CONFIRMED |
| Speed    | number   | Movement speed | 0-1000                | CONFIRMED |

## Relationships

- **Connects to**: [List of block types this commonly connects to]
- **Parent of**: [Blocks typically parented to this]
- **Child of**: [Blocks typically parent to this]

## Confidence Level

- **CONFIRMED**: Directly observed, reproducible
- **PARTIALLY CONFIRMED**: Some evidence, not fully verified
- **UNCONFIRMED**: Reported but lacking evidence
- **UNKNOWN**: No data available

## Source Evidence

- `assets/models/model/[Name]/[Name].json`
- `assets/models/model/[Name]/[Name].obj`
- `old-files/obj_ids-spanish.md`
- Experimental saves in `examples/experiments/`

## Notes

[Any additional observations, hypotheses, or unresolved questions]

## Authoring rules

- Preserve the exact object identifier and filename spelling.
- Use `unknown` or an explicit not-yet-inspected state when data is missing; do not convert missing evidence into zero, an empty list, or a confirmed claim.
- Cite the actual evidence available for this object. Do not list a source file or experiment merely because it is mentioned by a generic template.
- Use the shared confidence labels defined in [documentation standards](../../docs/documentation-standards.md).
- Keep one page per object and link to the [reference index](README.md).
