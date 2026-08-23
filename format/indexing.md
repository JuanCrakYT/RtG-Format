# Indexing

## Top-Level Object Indices

**Confirmed**

RtG uses **1-based logical indices** for objects in the top-level JSON array when resolving references such as `PrimaryIndex` / `ÍndicePadre`.

For example:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}],
    ["Part", [["1", "5", 2]], {}]
]
````

The logical object indices are:

```text
Base → 1
Part → 2
Part → 3
```

Therefore, the connection in the second element referencing `1` refers to the `Base`, and the connection in the third element referencing `2` refers to the first `Part`.

## Internal Tuple Positions

The three fields inside each object tuple have the following positions:

```text
0 → Type
1 → Connections
2 → Properties
```

These positions are zero-based.

This is separate from the logical object indices used by RtG references.

## Array Order

The order of objects in the top-level array is significant because references use their logical indices.

Reordering objects without updating their references can break the build.

## Important Distinction

There are two different indexing systems in the format:

```text
Top-level object references → 1-based
Object tuple fields         → 0-based
```

Do not confuse the physical array position used by a programming language with the logical object index stored in RtG connection references.

## References

* [`../SPECIFICATION.md`](../SPECIFICATION.md)
* [`json-structure.md`](json-structure.md)
* [`identifiers.md`](identifiers.md)
* [`../old-files/RtG_Save_Format_Specification-spanish.md`](../old-files/RtG_Save_Format_Specification-spanish.md)
