# Format Documentation

This directory contains detailed documentation of the **RtG save/build format**.

The documents here describe specific parts of the format in greater detail. They complement the consolidated [`../SPECIFICATION.md`](../SPECIFICATION.md), which is the main reference for the project's current interpretation of the format.

## Documents

### JSON Structure

[`json-structure.md`](json-structure.md) — Describes the structural layout of the JSON representation of an RtG save, including objects, connections, properties, and their relationships.

### Indexing

[`indexing.md`](indexing.md) — Documents RtG's object indexing behavior, including the distinction between JSON array positions and the 1-based logical indices used by references.

### Properties

[`properties.md`](properties.md) — Documents object properties and observed property behavior within the save data.

### Identifiers

[`identifiers.md`](identifiers.md) — Documents identifiers used by the format, including object types, connection identifiers, `LocalType`, `PrimaryID`, and UUID-related references.

### Unknown Fields

[`unknown-fields.md`](unknown-fields.md) — Documents fields whose meaning or behavior is currently unknown, incomplete, or not fully verified.

## How These Documents Relate

The documents in this directory are intentionally separated by topic:

```tree
SPECIFICATION.md
└── Current consolidated interpretation
    │
    └── format/
        ├── json-structure.md
        ├── indexing.md
        ├── properties.md
        ├── identifiers.md
        └── unknown-fields.md
```

[`../SPECIFICATION.md`](../SPECIFICATION.md) should be used as the starting point for the current overall understanding of the format.

Use the documents in this directory when you need more detailed information about a specific part of that format.

## Related Documentation

* [`../docs/`](../docs/) — Introductory and navigational documentation.
* [`../blocks/`](../blocks/) — Object and Part IDs, categories, and connection-point references.
* [`../compression/`](../compression/) — Encoding, compression, and final save representation.
* [`../examples/`](../examples/) — Real examples and reproducible experiments.
* [`../research/`](../research/) — Research methodology, discoveries, and unresolved questions.
* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Main consolidated technical reference.
* [`../old-files/`](../old-files/) — Historical reverse-engineering material preserved for research provenance.

## Scope

This directory focuses on the **structure and behavior of the format itself**.

It does not replace the research records, historical material, or compression documentation. When a topic belongs to one of those areas, follow the corresponding documentation instead.
