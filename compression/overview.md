# Compression and Encoding Overview

This document provides an overview of the encoding and compression research related to the RtG save system.

The purpose of this folder is to document how the structured build data represented by RtG is transformed into the data stored or transmitted by the game.

This research is separate from the structural format documentation under `format/`.

---

## Scope

The compression and encoding research focuses on the layers between the structured build data and the final save representation.

Conceptually, the process can be represented as:

```text
RtG Build
    │
    ▼
Structured Build Data
    │
    ▼
JSON Representation
    │
    ▼
Encoding / Compression
    │
    ▼
Final Save Representation
```

The exact implementation of each stage should only be considered confirmed when supported by direct evidence or reproducible experiments.

---

## What This Folder Documents

This folder may contain documentation about:

* encoding methods;
* compression behavior;
* transformations applied to save data;
* relationships between encoded data and decoded build JSON;
* known characteristics of the final save representation;
* experiments investigating unknown or suspected encoding layers.

The folder should not be used to redefine the structure of the decoded build data. That information belongs under `format/`.

---

## Current Knowledge

The historical reverse-engineering research established that RtG save data can appear as Base64-encoded text containing the build's JSON representation.

The Base64 layer itself is **not** the RtG build format.

The structured build data revealed after decoding is documented separately under `format/`.

Additional compression or transformation layers must not be treated as confirmed unless they are supported by evidence.

For detailed evidence regarding the known encoding process, see [`encoding.md`](encoding.md).

---

## Confidence and Evidence

Encoding and compression findings should use the project's confidence terminology:

* **CONFIRMED** — Supported by direct evidence or reproducible observations.
* **PARTIALLY CONFIRMED** — Supported by evidence, but some details remain unverified.
* **UNCONFIRMED** — Observed or suspected, but insufficiently verified.
* **HYPOTHESIS** — A proposed explanation that has not yet been demonstrated.

Do not present a hypothesis or unverified algorithm as a confirmed part of the RtG save format.

Experiments should include enough information to reproduce the observation and evaluate the evidence independently.

---

## Experiments

Reproducible encoding and compression experiments are stored under:

[`examples/experiments/`](examples/experiments)

The experiment documentation should contain the relevant input, output, observations, reproduction steps, and evidence.

The file [`examples-template.md`](examples-template.md) provides a template for documenting experiments related to this area.

Failed or inconclusive experiments are still valuable research records and should be preserved according to the rules in `examples/experiments/`.

---

## Related Documentation

* [`encoding.md`](encoding.md) — Detailed documentation of the currently understood encoding process.
* [`examples-template.md`](examples-template.md) — Template for documenting encoding/compression experiments.
* [`../format/json-structure.md`](../format/json-structure.md) — Structure of the decoded JSON build data.
* [`../format/indexing.md`](../format/indexing.md) — Indexing and references within the build data.
* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current consolidated specification.
* [`../examples/experiments/`](../examples/experiments/) — Repository of reproducible experiments and evidence.
* [`../old-files/`](../old-files/) — Historical reverse-engineering records.

---

## Important Distinction

This directory describes the **representation and transformation of save data**.

The `format/` directory describes the **structure and meaning of the build data itself**.

In simple terms:

```text
format/
    What the build data contains
```
```text
compression/
    How that data is represented or transformed
```

Keeping these two areas separate helps prevent observations about encoding or compression from being confused with the actual structure of the RtG save format.
