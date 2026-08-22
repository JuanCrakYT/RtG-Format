# RtG Save Format Specification

> **Status:** Partially documented

## Summary
- This document is the canonical, technical reference for the observed RtG save/build format. It contains only information that is present in repository evidence or explicitly marked as hypothesis/unknown.

## High-level confirmed facts
> **CONFIRMED:** RtG save files are represented as a top-level JSON Array where each element is a 3-element tuple:
```json
[
    <Type>,
    <Connections>,
    <Properties>
]
```
> **CONFIRMED:** Each element index functions as a positional reference; the loader resolves parent/child relationships by integer indices (indexing details in `format/indexing.md`).
> **CONFIRMED:** The second element `Connections` is an array of 3-element connection tuples: 
```json
[
    <LocalType>,
    <PrimaryID>,
    <PrimaryIndex>
]
```
> **CONFIRMED:** The `Properties` element is an open dictionary; unknown keys are tolerated and ignored by the loader when unrecognized.

## Structure
- See `format/json-structure.md` for the observed JSON layout and examples.

### Identifiers and indexing
- See `format/indexing.md` and `format/identifiers.md`.

### Attachments and UUIDs
- See `research/discoveries.md` and `format/identifiers.md` for EphemeralAttachments and UUID linking behavior.

## Unknowns
- See `research/unknowns.md` and `format/unknown-fields.md` for fields and behaviors that remain unconfirmed.

## Change history
- See `CHANGELOG.md` and the `old-files/` folder for historical documents (do not treat them as authoritative without verification).
