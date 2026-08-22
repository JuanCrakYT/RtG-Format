# Discoveries

Each entry should include: Discovery, Evidence, Confidence, Notes.

Confirmed entries (extracted from historical material)

## 1. Save representation as JSON array
> **Discovery:** Top-level JSON array where each element is:
```json
[
    <Type>,
    <Connections>,
    <Properties>
]
```
> **Evidence:** Multiple observed exports and `old-files/RtG_Save_Format_Specification-spanish.md`.
> **Confidence:** CONFIRMED

## 2. Connection tuple semantics
> **Discovery:** Each connection is:
```json
[
    <LocalType>,
    <PrimaryID>,
    <PrimaryIndex>
]
```
The third value is the index of the parent in the top-level array.
> **Evidence:** Examples and experiments in historical files.
> **Confidence:** CONFIRMED

## 3. EphemeralAttachments and UUID linking
> **Discovery:** `EphemeralAttachments` stored in `Properties` map UUID -> {partName, cframe}; connections may reference `{UUID}` to resolve transforms.
> **Evidence:** Observed examples and injection experiments.
> **Confidence:** CONFIRMED / PARTIALLY CONFIRMED (behavior of multiple references needs more testing)

Further items should be added with reproducible evidence and links to the raw saves used.
