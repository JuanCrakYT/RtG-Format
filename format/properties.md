# Properties

This document describes the observed `Properties` dictionary stored in RtG object tuples.

The `Properties` field is an open JSON object. Different object types interpret different properties, while other properties may be stored without being actively used.

Historical evidence for these observations is preserved in:

- [`../old-files/RtG_Save_Format_Specification-spanish.md`](../old-files/RtG_Save_Format_Specification-spanish.md)
- [`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md)

---

## 1. Structure

The third field of every object tuple is the `Properties` dictionary:

```json
[
    Type,
    Connections,
    Properties
]
```

Example:

```json
[
    "Part",
    [],
    {
        "RGB": [255, 0, 0]
    }
]
```

The dictionary can contain zero or more key/value pairs.
An empty properties dictionary is valid:

```json
[
    "Base",
    [],
    {}
]
```

---

## 2. Open Dictionary

The `Properties` object is an open dictionary.
Additional keys can be present without necessarily making the JSON structurally invalid.

Example:

```json
{
    "RGB": [255, 0, 0],
    "DatoInventado": 123
}
```

Historical experiments demonstrated that additional properties can be inserted into objects without preventing the save from loading.

This does **not** mean that every property is understood or used by every object.

---

## 3. Property States

A property observed in a save can be classified by how the object handles it.

```mermaid
flowchart TD

    JSON["📦 Property in JSON"] --> STORED["💾 Stored"]
    JSON --> INTERPRETED["🧠 Interpreted"]
    JSON --> IGNORED["🚫 Ignored"]

    STORED --> PRESENT["🔑 Key/value exists in the save"]
    INTERPRETED --> USED["⚙️ Object logic uses the value"]
    IGNORED --> UNUSED["🗑️ Object logic does not use the value"]

    classDef root fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef stored fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef interpreted fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef ignored fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;
    classDef detail fill:#edf2f7,color:#1a202c,stroke:#a0aec0,stroke-width:2px;

    class JSON root;
    class STORED stored;
    class INTERPRETED interpreted;
    class IGNORED ignored;
    class PRESENT,USED,UNUSED detail;
```

### Stored

The property exists in the JSON object.
Its presence alone does not prove that the object actively uses it.

### Interpreted

The object's logic reads the property and uses it to affect behavior, appearance, or another part of its state.

Examples observed historically include:

```mermaid
flowchart LR

    PART["🧩 Part"] --> RGB["🎨 RGB"]

    SERVO["⚙️ Servo"] --> SPEED["💨 Speed"]
    SERVO --> ROTATION["🔄 Rotation"]

    SPRITE["🖼️ Sprite"] --> IMAGEID["🆔 ImageId"]

    classDef part fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef servo fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;
    classDef sprite fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:2px;
    classDef property fill:#edf2f7,color:#1a202c,stroke:#a0aec0,stroke-width:2px;

    class PART part;
    class SERVO servo;
    class SPRITE sprite;
    class RGB,SPEED,ROTATION,IMAGEID property;
```

### Ignored

The property exists in the JSON but is not used by the object's logic.

Historical experiments demonstrated that extra keys can be present without causing a syntax or loading error.

---

## 4. Additional Properties

A property dictionary may contain keys that do not correspond to the normal properties expected by an object.

For example:

```json
{
    "RGB": [255, 0, 0],
    "Speed": 100,
    "UnknownProperty": 123
}
```

Historical testing showed that adding extra keys to objects such as `Servo` and `Sprite` did not prevent them from loading.

Therefore:

> An unknown property is not automatically an invalid property.

Whether an unknown property is ignored, preserved, or interpreted is object-dependent and must be determined experimentally.

---

## 5. Missing Properties

Historical testing also showed that some missing properties may be created automatically when the object requires them.

The loader may use an empty or default value.

Conceptually:

```mermaid
flowchart TD

    MISSING["⚠️ Property missing"]
    MISSING --> REQUIRES{"❓ Object requires it?"}

    REQUIRES -->|No| ABSENT["🚫 Remains absent"]
    REQUIRES -->|Yes| DEFAULT["🧩 Default / empty value<br/>may be created"]

    classDef missing fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:3px;
    classDef decision fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:2px;
    classDef absent fill:#718096,color:#fff,stroke:#4a5568,stroke-width:2px;
    classDef default fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;

    class MISSING missing;
    class REQUIRES decision;
    class ABSENT absent;
    class DEFAULT default;
```

The exact default behavior is object-specific and has not been completely catalogued.

---

## 6. Universal / Cross-Object Properties

Some properties have been observed across multiple object types.

### `RGB`

Represents color information as an array of three values:

```json
{
    "RGB": [255, 0, 0]
}
```

Observed form:

```json
[R, G, B]
```

The historical research records `RGB` as an observed property.
It was also present in the first `SprayPaint` save that started the reverse-engineering investigation.

### `EphemeralAttachments`

Stores attachment data indexed by UUID:

```json
{
    "EphemeralAttachments": {
        "{UUID}": {
            "partName": "Part",
            "cframe": [
                5.0, 5.0, 0.0,
                0.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0
            ]
        }
    }
}
```

`EphemeralAttachments` can be hosted by objects throughout the format.

Detailed UUID and attachment behavior is documented in [`identifiers.md`](identifiers.md) and `SPECIFICATION.md`.

---

## 7. Observed Property Catalog

The historical specification records the following properties.
This is an **observed catalog**, not a claim that these are the only properties used by RtG.

### General

| Property               | Observed type   | Example         |
| ---------------------- | --------------- | --------------- |
| `RGB`                  | Array `[R,G,B]` | `[255,0,0]`     |
| `EphemeralAttachments` | Object          | `{UUID: {...}}` |
| `Mode`                 | String          | `"..."`         |
| `Visible`              | Boolean         | `true`          |

### Servo / Mechanical

| Property       | Observed type | Example |
| -------------- | ------------- | ------- |
| `Rotation`     | Number        | `0`     |
| `Speed`        | Number        | `72`    |
| `LimitEnabled` | Boolean       | `true`  |
| `LimitAngle`   | Number        | `80.9`  |
| `Rest`         | Boolean       | `true`  |
| `Forwards`     | Boolean       | `false` |
| `Backwards`    | Boolean       | `false` |
| `MinLength`    | Number        | `0`     |
| `MaxLength`    | Number        | `0`     |
| `MaxForce`     | Number        | `0`     |
| `Length`       | Number        | `0`     |

### Sensors

| Property            | Observed type | Example |
| ------------------- | ------------- | ------- |
| `Activated`         | Boolean       | `true`  |
| `ActivationSpeed`   | Number        | `10`    |
| `ActivationHeight`  | Number        | `5`     |
| `MaxDistance`       | Number        | `10`    |
| `CanTargetAttached` | Boolean       | `true`  |
| `IgnoreAttached`    | Boolean       | `true`  |

### Logic / Timing

| Property            | Observed type | Example |
| ------------------- | ------------- | ------- |
| `Delay`             | Number        | `1`     |
| `DelayDeactivation` | Boolean       | `true`  |

### Weapons / Inventory

| Property   | Observed type | Example |
| ---------- | ------------- | ------- |
| `Shooting` | Boolean       | `true`  |
| `Bullets`  | Integer       | `10`    |
| `Quantity` | Integer       | `1`     |

### Text / Media / Radio

| Property      | Observed type | Example     |
| ------------- | ------------- | ----------- |
| `Text`        | String        | `"Hello"`   |
| `ImageId`     | Integer       | `123456789` |
| `Volume`      | Number        | `1`         |
| `Channel`     | Number        | `1`         |
| `CustomTrack` | String        | `"..."`     |
| `On`          | Boolean       | `true`      |
| `Phrase`      | String        | `"..."`     |

---

## 8. Object-Specific Examples

The same property name may have meaning only for certain object types.

### Part

Example observed property:

```json
{
    "RGB": [255, 0, 0]
}
```

### Servo

Historical research observed:

```json
{
    "Rotation": 0,
    "Speed": 72,
    "LimitEnabled": true,
    "LimitAngle": 80.9,
    "Rest": true,
    "Forwards": false,
    "Backwards": false
}
```

### Sensors

Historical research observed properties including:

```json
{
    "ActivationKey": "W",
    "ActivationHeight": 5,
    "ActivationSpeed": 10
}
```

### Sprite

Historical research observed:

```json
{
    "ImageId": 6767676767
}
```

An invalid or nonexistent `ImageId` was observed to produce a `Sprite` that can still exist in the build while remaining invisible.

---

## 9. Property Validation

Properties are treated more permissively than structural references.

Historical testing demonstrated that additional unknown properties can be inserted without necessarily causing `Build inválida`.

This differs from structural fields such as:

* `TipoLocal`
* `ÍndicePadre`
* UUID references

which can cause loading failures when invalid.

Therefore:

```mermaid
flowchart TD

    UNKNOWN["❓ Unknown Property"] --> NOT_EQUAL["≠"]
    INVALID["⚠️ Invalid Structural Reference"] --> NOT_EQUAL

    classDef unknown fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef invalid fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;
    classDef symbol fill:#205ad5,color:#fff,stroke:#253c9a,stroke-width:3px;

    class UNKNOWN unknown;
    class INVALID invalid;
    class NOT_EQUAL symbol;
```

---

## 10. Evidence Status

The catalog in this document is based on historical observations.

The following distinctions are important:

### CONFIRMED / OBSERVED

The property and its behavior have been directly observed in a save or experiment.

### PARTIALLY DOCUMENTED

The property has been observed, but its complete behavior or value range is not yet known.

### UNKNOWN

The available evidence does not establish the property's exact behavior.

Do not infer a property's meaning solely from its name.

---

## 11. Related Documentation

* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Complete format specification.
* [`json-structure.md`](json-structure.md) — JSON object structure.
* [`identifiers.md`](identifiers.md) — IDs, UUIDs, and references.
* [`../examples/experiments/`](../examples/experiments/) — Reproducible experiments.
* [`../old-files/RtG_Save_Format_Specification-spanish.md`](../old-files/RtG_Save_Format_Specification-spanish.md) — Historical specification.
* [`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md) — Historical object research.
