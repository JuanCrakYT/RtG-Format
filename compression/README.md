# Encoding and Compression

This directory documents the representation of RtG build data in the final save output. It covers a different layer from the decoded structure described in [`format/`](../format/README.md).

## Documentation

| Document | Purpose |
| --- | --- |
| [`overview.md`](overview.md) | Scope and current state of the investigation |
| [`encoding.md`](encoding.md) | Observed encoding steps and final save representation |
| [`examples-template.md`](examples-template.md) | Template for recording an encoding/compression experiment |

## Evidence and terminology

Use the confidence labels consistently:

- **CONFIRMED** — supported by direct evidence or repeatable observations.
- **PARTIALLY CONFIRMED** — supported by evidence, but some details or cases remain unverified.
- **UNCONFIRMED** — observed or suspected, but not adequately verified.
- **HYPOTHESIS** — a proposed explanation that has not yet been demonstrated.

Base64 is an encoding method, not the build format itself. Do not infer a compression algorithm merely from the appearance of encoded output. Describe the observed transformation and its limits, and link to reproducible experiments under [`examples/experiments/`](../examples/experiments/).

The structural representation and the final save representation should be documented separately so that changes in one layer do not create confusion about the other.
