# RtG Save Format — Reverse-Engineered Documentation

Independent technical documentation of the save/build format used by **Road To Gramby's (RtG)** on Roblox.


## Overview

In simple terms, the RtG save system can be understood as a pipeline:

1. A build is represented internally as a collection of objects and their relationships.
2. The building system converts those objects into structured save data.
3. That data is represented as JSON containing the objects, connections, and properties.
4. The resulting data is encoded/compressed into the final save output used by the game.

This repository documents each stage of that process, from the building system to the final save output.
The documentation covers:
```md
- Save/build data structure
- JSON representation
- Building-system behavior relevant to serialization
- Save final output
- Object and Part IDs
- Connection points
- Parent/connection references
- Object properties
- Identifiers and UUIDs
- `EphemeralAttachments`
- CFrame data
- Encoding and compression
- Known and unknown fields
- Research methodology and experimental results
```

## Documentation
### Start here

- [`docs/getting-started.md`](docs/getting-started.md) — Recommended reading path
- [`docs/save-anatomy.md`](docs/save-anatomy.md) — Anatomy of an RtG save
- [`docs/building-system.md`](docs/building-system.md) — Building-system concepts
- [`docs/faq.md`](docs/faq.md) — Frequently asked questions


### Format

- [`SPECIFICATION.md`](SPECIFICATION.md) — Main technical specification
- [`format/json-structure.md`](format/json-structure.md) — JSON structure
- [`format/indexing.md`](format/indexing.md) — Indexing and references
- [`format/properties.md`](format/properties.md) — Object properties
- [`format/identifiers.md`](format/identifiers.md) — Identifiers and UUIDs
- [`format/unknown-fields.md`](format/unknown-fields.md) — Unknown or incompletely understood fields

### Blocks and Parts
See [`blocks/`](blocks/) for the documented object/Part IDs and their categories.
The historical reverse-engineering ID research is preserved separately in [`old-files/`](old-files/).

### Compression and encoding
See [`compression/`](compression/) for documentation of the encoding/compression layers.

### Examples
See [`examples/`](examples/) for real and reproducible save/build examples and experiments.

### Research
See [`research/`](research/) for methodology, discoveries, and unresolved questions.

### Tools
See [`tools/`](tools/) for utilities related to decoding, encoding, conversion, and inspection.


## Status
**Specification:** Unreleased
The repository currently contains a consolidated specification derived from the project's reverse-engineering research.
Historical development records, including earlier specification versions such as **v0.406**, are preserved in [`old-files/`](old-files/).

## Research status
The documentation distinguishes between:
```md
- **Confirmed** — Supported by reproducible observations or direct evidence.
- **Partially confirmed** — Supported by observations but not completely verified.
- **Unconfirmed** — Reported or suspected but lacking sufficient evidence.
```
Historical observations are preserved rather than silently rewritten.

## Historical documentation
`old-files/` contains historical research material preserved for reference.
These files document the development of the research and should not be treated as the current consolidated specification.
For the current reference, use [`SPECIFICATION.md`](SPECIFICATION.md).

## Project files
- CONTRIBUTING.md — Contribution rules
- CHANGELOG.md — Project history and version changes
- structure.md — Repository structure
- LICENSE — License information

## Credits
```md
- **JuanCrakYT** — Reverse engineering, research, documentation, and maintenance.
- **Road To Gramby's Wiki** — Reference for game objects, terminology, and categorization.
- **Road To Gramby's** — Original game and save/build system documented by this project.
```
This is an independent reverse-engineering project and is not affiliated with or endorsed by the creators of Road To Gramby's or the Road To Gramby's Wiki.

## Link Reference
**Road To Gramby's Wiki:**
```md
https://road-to-grambys.fandom.com/wiki/Road_to_Gramby%27s_%F0%9F%91%B5_Wiki
```