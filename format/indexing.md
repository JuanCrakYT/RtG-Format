# Indexing

This document describes how RtG indexes objects and how those indices are used by references.

The most important distinction is between:

- JSON array positions.
- RtG logical object indices.
- Tuple field positions.

---

## 1. Two Different Index Systems

RtG uses normal JSON arrays, which programming languages generally access using zero-based positions.

However, object references inside the RtG save/build format use **1-based logical indices**.

These are not the same thing.
---
| JSON array position | RtG logical object index |
| ------------------- | ------------------------ |
| 0                   | 1                        |
| 1                   | 2                        |
| 2                   | 3                        |
| 3                   | 4                        |
| ...                 | ...                      |
---
For example:

```json
[
    ["Base", [], {}],
    ["Part", [], {}],
    ["Part", [], {}]
]
```

The programming-language positions are:

```js
position 0 = Base
position 1 = first Part
position 2 = second Part
```

The RtG logical indices are:

```js
index 1 = Base
index 2 = first Part
index 3 = second Part
```

---

## 2. Logical Object Index

The logical object index identifies an object within the top-level save array.
The first object has logical index `1`.
The second object has logical index `2`.

And so on.

```mermaid
flowchart TD

    ROOT["📦 Root Array"]

    ROOT --> OBJ1["1️⃣ Logical index 1 → Object 1"]
    ROOT --> OBJ2["2️⃣ Logical index 2 → Object 2"]
    ROOT --> OBJ3["3️⃣ Logical index 3 → Object 3"]
    ROOT --> MORE["⋮"]

    classDef root fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef object fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef more fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px;

    class ROOT root;
    class OBJ1,OBJ2,OBJ3 object;
    class MORE more;
```

This indexing is used by `PrimaryIndex`.

---

## 3. PrimaryIndex

The third value of a connection tuple is `PrimaryIndex`.

```json
[
    LocalType,
    PrimaryID,
    PrimaryIndex
]
```

Example:

```json
["1", "5", 1]
```

Here:

```js
PrimaryIndex = 1
```

means:

> The parent is the object with logical index `1`.

For example:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}]
]
```

The connection of the `Part` points to:

```mermaid
flowchart TD
    INDEX["PrimaryIndex = 1"]
    INDEX --> OBJECT["Object 1"]
    OBJECT --> BASE["Base"]

    classDef index fill:#fefcbf,color:#744210,stroke:#d69e2e,stroke-width:2px;
    classDef object fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef type fill:#edf2f7,color:#1a202c,stroke:#a0aec0,stroke-width:2px;

    class INDEX index;
    class OBJECT object;
    class BASE type;
```

---

## 4. Parent References

A connection therefore establishes a relationship between an object and another object in the root array.

```mermaid
flowchart TD

    CHILD["🧩 Child"] --> CONNECTION["🔗 Connection"]
    CONNECTION --> INDEX["🔢 PrimaryIndex"]
    INDEX --> PARENT["👤 Parent Object"]

    classDef child fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef connection fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef index fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef parent fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;

    class CHILD child;
    class CONNECTION connection;
    class INDEX index;
    class PARENT parent;
```

Example:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}],
    ["Part", [["1", "5", 2]], {}]
]
```

Logical relationships:

```mermaid
flowchart TD

    OBJ1["🧩 Object 1"] --> BASE["🏠 Base"]

    OBJ2["🧩 Object 2"] --> PARENT1["🔢 Parent 1"]
    PARENT1 --> BASE

    OBJ3["🧩 Object 3"] --> PARENT2["🔢 Parent 2"]
    PARENT2 --> OBJ2

    classDef object fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef parent fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef base fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;

    class OBJ1,OBJ2,OBJ3 object;
    class PARENT1,PARENT2 parent;
    class BASE base;
```

Therefore the structure is:

```mermaid
flowchart TD

    BASE["🏠 Base"]
    PART1["🧩 Part"]
    PART2["🧩 Part"]

    BASE --> PART1
    PART1 --> PART2

    classDef base fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;
    classDef part fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;

    class BASE base;
    class PART1,PART2 part;
```

---

## 5. Object Order Matters

Because references point to logical object indices, changing the order of objects can change what a reference points to.

Original:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}]
]
```

Relationship:

```mermaid
flowchart LR

    PART["🧩 Part"] --> BASE["🏠 Base"]

    classDef part fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef base fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;

    class PART part;
    class BASE base;
```

If the objects are reordered:

```json
[
    ["Part", [["1", "5", 1]], {}],
    ["Base", [], {}]
]
```

the same `PrimaryIndex = 1` now refers to the `Part` itself rather than the `Base`.
The reference has therefore changed meaning.
This is why the order of the root array must be preserved when modifying an existing save.

---

## 6. Object Tuple Positions Are Different

The `0-based` positions used inside an object tuple must not be confused with the `1-based` logical object indices.

An object is:

```json
[
    Type,
    Connections,
    Properties
]
```

Its fields are:

```js
object[0] = Type
object[1] = Connections
object[2] = Properties
```

These positions are zero-based because they are ordinary JSON array positions.

They are unrelated to the logical index used to reference the object.

---

## 7. Connection Tuple Positions

The same distinction applies to connection tuples.

A connection is:

```json
[
    LocalType,
    PrimaryID,
    PrimaryIndex
]
```

Its fields are:

```js
connection[0] = LocalType
connection[1] = PrimaryID
connection[2] = PrimaryIndex
```

Again, these are zero-based JSON positions.
Only the **value of `PrimaryIndex`** represents a 1-based logical object index.

---

## 8. Index Conversion

When parsing an RtG save using a zero-based programming language, the logical index can be converted to an array position by subtracting `1`.

```js
array_position = PrimaryIndex - 1
```

Example:

```js
PrimaryIndex = 1
array position = 0
```

```js
PrimaryIndex = 15
array position = 14
```

When generating a reference from a zero-based array position:

```js
PrimaryIndex = array_position + 1
```

Example:

```js
array position = 0
PrimaryIndex = 1
```

```js
array position = 14
PrimaryIndex = 15
```

---

## 9. Example

Consider:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}],
    ["Servo", [["1", "7", 2]], {}],
    ["Part", [["1", "5", 3]], {}]
]
```

Logical indices:

```js
1 = Base
2 = Part
3 = Servo
4 = Part
```

Connections:

```mermaid
flowchart TD

    OBJ2["🧩 Object 2"] --> INDEX1["🔢 PrimaryIndex = 1"]
    INDEX1 --> BASE["🏠 Base"]

    OBJ3["🧩 Object 3"] --> INDEX2["🔢 PrimaryIndex = 2"]
    INDEX2 --> PART["🧩 Part"]

    OBJ4["🧩 Object 4"] --> INDEX3["🔢 PrimaryIndex = 3"]
    INDEX3 --> SERVO["⚙️ Servo"]

    classDef object fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef index fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef base fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef part fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef servo fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;

    class OBJ2,OBJ3,OBJ4 object;
    class INDEX1,INDEX2,INDEX3 index;
    class BASE base;
    class PART part;
    class SERVO servo;
```

The resulting hierarchy is:

```mermaid
flowchart TD

    BASE["🏠 Base"] --> PART1["🧩 Part"]
    PART1 --> SERVO["⚙️ Servo"]
    SERVO --> PART2["🧩 Part"]

    classDef base fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;
    classDef part fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef servo fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;

    class BASE base;
    class PART1,PART2 part;
    class SERVO servo;
```

---

## 10. Indexing and UUIDs

`PrimaryIndex` and UUID references solve different parts of a connection.

A connection such as:

```json
["1", "5", 2]
```

uses:

```js
PrimaryID  = "5"
PrimaryIndex = 2
```

The `PrimaryIndex` identifies **which object is the parent**.
The `PrimaryID` identifies **where on that parent the connection is made**.

For a UUID-based connection:

```json
[
    "1",
    "{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}",
    2
]
```

the roles remain separate:

```mermaid
flowchart TD
    INDEX["PrimaryIndex"] --> PARENT["👤 Parent Object"]
    POINT["PrimaryID"] --> EPHEMERAL["📎 EphemeralAttachment<br/>belonging to that parent"]

    classDef index fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef point fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef parent fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef attachment fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;

    class INDEX index;
    class POINT point;
    class PARENT parent;
    class EPHEMERAL attachment;
```

The UUID does not replace `PrimaryIndex`.

---

## 11. Index Validity

A parent index must resolve to an object in the root array.
For a root array containing `N` objects, the normal valid logical range is:

```text
1 ... N
```

A reference outside this range cannot identify an object in the save.
Historical experiments indicate that invalid structural references are not automatically repaired by the loader and can result in a loading failure.

---

## 12. Summary

```mermaid
flowchart TD
    TITLE["RtG Indexing"]

    TITLE --> JSON["JSON"]
    JSON --> JSON_ARRAY["Array positions<br/>0-based"]
    JSON --> OBJECT_TUPLE["Object tuple positions<br/>0-based"]
    JSON --> CONNECTION_TUPLE["Connection tuple positions<br/>0-based"]

    TITLE --> RTG["RtG logical references"]
    RTG --> OBJECT_INDEX["Logical object index<br/>1-based"]
    RTG --> PARENT_INDEX["PrimaryIndex<br/>1-based"]

    classDef title fill:#4a5568,color:#fff,stroke:#2d3748,stroke-width:3px;
    classDef category fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef info fill:#edf2f7,color:#1a202c,stroke:#a0aec0;

    class TITLE title;
    class JSON,RTG category;
    class JSON_ARRAY,OBJECT_TUPLE,CONNECTION_TUPLE,OBJECT_INDEX,PARENT_INDEX info;
```

The most important rule is:

> **`PrimaryIndex` uses a 1-based logical object index, even though the JSON array itself is accessed using zero-based positions by normal programming languages.**

---

## Related Documentation

* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Complete format specification.
* [`json-structure.md`](json-structure.md) — JSON structure.
* [`identifiers.md`](identifiers.md) — Object identifiers and connection references.
* [`../examples/experiments/`](../examples/experiments/) — Experimental saves and evidence.
* [`../old-files/`](../old-files/) — Historical reverse-engineering records.
