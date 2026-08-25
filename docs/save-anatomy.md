# Save Anatomy

An RtG save contains a serialized representation of a build.
At a high level, the decoded build is represented as a JSON array. Each element represents one object in the build.

## Basic Structure

```mermaid
flowchart TD
    A["📦 Save (JSON Array)"] --> B["Element 0"]
    A --> C["Element 1"]
    A --> D["⋮"]

    B --> B1["Type"]
    B --> B2["Connections"]
    B --> B3["Properties"]

    C --> C1["Type"]
    C --> C2["Connections"]
    C --> C3["Properties"]

    classDef root fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef element fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef field fill:#edf2f7,color:#1a202c,stroke:#a0aec0;
    classDef more fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px;

    class A root;
    class B,C element;
    class D more;
    class B1,B2,B3,C1,C2,C3 field;
```

Each object follows the general structure:

```json
[
    Type,
    Connections,
    Properties
]
```

### Type

`Type` identifies the kind of RtG object represented by the element.

Examples include:

```text
Base
Part
Servo
Sprite
Connector
Wire
```

The currently documented object and Part IDs are organized under [`../blocks/`](../blocks/).

### Connections

`Connections` describes the relationships between the current object and other objects.

A connection uses the general structure:

```json
[
    LocalType,
    PrimaryID,
    PrimaryIndex
]
```

The exact meaning of these fields is documented in [`../format/indexing.md`](../format/indexing.md) and the relevant format documentation.

### Properties

`Properties` is an open JSON object containing data associated with the object.

Examples include:

```json
{
    "RGB": [255, 0, 0]
}
```

or:

```json
{
    "Speed": 72,
    "Rotation": 45
}
```

Property behavior is documented in [`../format/properties.md`](../format/properties.md).

## Object Relationships

Object references are used to reconstruct relationships between objects during loading.

Conceptually:

```mermaid
flowchart TD

    P["🟣 Parent Object"] --> C["🔵 Child Object"]
    C --> C1["🔗 Connection"]
    C1 --> R["📌 Parent Reference"]

    classDef parent fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef child fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef connection fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef reference fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;

    class P parent;
    class C child;
    class C1 connection;
    class R reference;
```

The loader uses these references to reconstruct the build structure.

## Attachments and UUIDs

Some spatial relationships use UUID-based references and `EphemeralAttachments`.

Conceptually:

```mermaid
flowchart TD

    A["🔗 Object Connection"] --> B["🆔 UUID"]
    B --> C["📎 EphemeralAttachment"]
    C --> D["📐 CFrame"]
    D --> E["🌐 Spatial Transformation"]

    classDef connection fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef uuid fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef attachment fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef cframe fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef spatial fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:3px;

    class A connection;
    class B uuid;
    class C attachment;
    class D cframe;
    class E spatial;
```

For the detailed behavior, see [`../format/identifiers.md`](../format/identifiers.md) and [`../research/discoveries.md`](../research/discoveries.md).

## Encoding

The structured build data is separate from the final encoded save representation.

The encoding research is documented under [`../compression/`](../compression/).

## Where to Continue

* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Current technical reference.
* [`../format/json-structure.md`](../format/json-structure.md) — Detailed JSON structure.
* [`../format/indexing.md`](../format/indexing.md) — Indexing and references.
* [`../format/properties.md`](../format/properties.md) — Properties.
* [`../format/identifiers.md`](../format/identifiers.md) — Identifiers and UUIDs.
* [`../blocks/`](../blocks/) — Object and Part IDs.
* [`../compression/`](../compression/) — Encoding and compression.
