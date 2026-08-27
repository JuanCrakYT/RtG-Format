# Getting Started

This directory provides the recommended entry points for understanding the RtG save/build format.

## Choose Your Path

You do not need to read the entire repository in order. Choose the path that best matches what you want to understand.

### 🟢 Beginner

Start here if you are new to the RtG save/build format and want to understand the basics before reading the technical details.

1. [`../README.md`](../README.md) — Project overview and documentation map.
2. [`save-anatomy.md`](save-anatomy.md) — Basic anatomy of an RtG save.
3. [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current consolidated technical reference.

After these, you should have enough context to begin exploring the technical documentation.

### 🔵 Technical

Use this path if you want to understand the structure and behavior of the format itself.

1. [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current consolidated technical reference.
2. [`../format/json-structure.md`](../format/json-structure.md) — Structure of the decoded JSON data.
3. [`../format/indexing.md`](../format/indexing.md) — Parent references and indexing behavior.
4. [`../format/properties.md`](../format/properties.md) — Object properties.
5. [`../format/identifiers.md`](../format/identifiers.md) — Identifiers and UUIDs.
6. [`../format/unknown-fields.md`](../format/unknown-fields.md) — Unknown or incompletely understood fields.
7. [`../blocks/README.md`](../blocks/README.md) — Part categories and ID references.
8. [`../compression/README.md`](../compression/README.md) — Encoding and compression research.

### 🟣 Research

Use this path if you are interested in how the format was discovered, tested, and documented.

1. [`../research/methodology.md`](../research/methodology.md) — How reverse-engineering observations are investigated and recorded.
2. [`../examples/`](../examples/) — Real examples and preserved experiments.
3. [`../research/`](../research/) — Discoveries, methodology, and unresolved questions.
4. [`../compression/`](../compression/) — Encoding and compression behavior and related experiments.

This path is intended for understanding the research process and evidence behind the documented format.

## Recommended Reading Order

If you prefer a single gradual introduction instead of choosing a path, the following order is recommended:

1. [`../README.md`](../README.md) — Project overview and documentation map.
2. [`save-anatomy.md`](save-anatomy.md) — Basic anatomy of an RtG save.
3. [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current consolidated technical reference.
4. [`../format/json-structure.md`](../format/json-structure.md) — Structure of the decoded JSON data.
5. [`../format/indexing.md`](../format/indexing.md) — Parent references and indexing behavior.
6. [`../blocks/README.md`](../blocks/README.md) — Part categories and ID references.
7. [`../compression/README.md`](../compression/README.md) — Encoding and compression research.
8. [`../research/methodology.md`](../research/methodology.md) — How reverse-engineering observations are investigated and recorded.

## After the Basics

Use these sections according to what you are investigating:

* [`../format/`](../format/) — JSON structure, properties, identifiers, indexing, and unknown fields.
* [`../blocks/`](../blocks/) — Parts, object IDs, categories, and connection-point references.
* [`../examples/`](../examples/) — Real examples and preserved experiments.
* [`../research/`](../research/) — Discoveries, methodology, and unresolved questions.
* [`../compression/`](../compression/) — Encoding and compression behavior and related experiments.
* [`../tools/`](../tools/) — Utilities and automation currently maintained in the repository.
* [`../old-files/`](../old-files/) — Historical reverse-engineering material preserved for provenance.

`old-files/` is not required for understanding the current format. It contains historical material that can be consulted when investigating previous findings or discrepancies with the current interpretation.

## Contributing

Before changing the documentation or adding research:

* Read [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
* Follow the evidence and confidence rules in [`../research/methodology.md`](../research/methodology.md).
* Add reproducible experiments to [`../examples/experiments/`](../examples/experiments/), not to `research/`.
* Update [`../SPECIFICATION.md`](../SPECIFICATION.md) and the relevant `format/` documents when a confirmed format behavior changes.

## Important Distinction

`docs/` is an introductory and navigational layer. It explains where information belongs and provides conceptual explanations.

The technical format itself is documented under [`../format/`](../format/) and [`../SPECIFICATION.md`](../SPECIFICATION.md).

Historical evidence is preserved under [`../old-files/`](../old-files/).
