# Examples and Experiments

This directory contains real RtG save examples, experiments, and curated minimal builds used for testing, research, and demonstrations.

## General Rules

- Do NOT create or add fabricated saves or experiments.
- Only include files with real provenance and supporting evidence.
- Keep notes and explanations in `README.md` or the appropriate documentation files, not inside `example.json`.

## Examples

This directory contains examples and experimental material related to the RtG save/build format.

The contents are separated by purpose:

- `experiments/` — Reproducible experiments and controlled tests.
- `json-examples/` — JSON examples used to demonstrate or inspect the format.
- `trash/` — Discarded, invalid, obsolete, or otherwise non-authoritative material.

## Experiments

[`experiments/`](experiments/) contains reproducible experiments used to investigate specific behaviors of the RtG save/build format.

Experiments should document:

- What was tested.
- How it was tested.
- What was changed or observed.
- The resulting behavior.
- Any relevant conclusions or limitations.

This directory is intended for **reproducible research**, not for permanently discarded material.

### JSON Examples

[`json-examples/`](json-examples/) contains JSON examples that help demonstrate the structure and behavior of RtG save/build data.

These examples may be useful when studying:

- Object structure.
- Connections.
- Properties.
- References.
- Attachments.
- Other documented format behavior.

Examples should not be treated as authoritative specifications by themselves. Confirmed format behavior belongs in the relevant documentation under `format/` or in `SPECIFICATION.md`.

### Trash

[`trash/`](trash/) contains material that is no longer considered useful as active documentation or examples.

This may include:

- Invalid experiments.
- Failed tests.
- Obsolete examples.
- Superseded data.
- Temporary research material.

Files in `trash/` are preserved for historical or investigative purposes, but they should **not** be used as current evidence or technical references unless explicitly stated.

### Related Documentation

- [`../format/`](../format/) — Current technical documentation of the RtG save/build format.
- [`../SPECIFICATION.md`](../SPECIFICATION.md) — Consolidated format specification.
- [`../research/`](../research/) — Research, discoveries, methodology, and unknowns.
- [`../blocks/`](../blocks/) — Object and part references.

## Examples vs. Experiments
---
|          | `json-examples/`        | `experiments/`   |
| -------- | ----------------------- | ---------------- |
| Purpose  | Demonstration/reference | Research         |
| Failed   | May be deleted          | Move to `trash/` |
| Evidence | Required                | Required         |
| Results  | Optional                | Required         |
---
