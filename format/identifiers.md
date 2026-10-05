# Identifiers

This document describes the identifier systems observed in the RtG save/build format.
It focuses on what each identifier identifies and how the identifiers relate to each other.
It does not define the complete object catalog or the complete list of connection-point IDs.
Historical identifier research is preserved in [`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md).

---

## 1. Identifier Systems

RtG uses several different kinds of identifiers.

```mermaid
flowchart TD

    ROOT["💾 RtG Save"] --> OBJECT["🧩 Object"]

    OBJECT --> TYPE["🏷️ Object Type"]
    OBJECT --> CONNECTION["🔗 Connection"]

    CONNECTION --> LOCAL["🔧 LocalType"]
    CONNECTION --> POINT["📍 PrimaryID"]
    CONNECTION --> INDEX["🔢 PrimaryIndex"]

    POINT --> NUMERIC["🔢 Numeric Point ID"]
    POINT --> UUID["🆔 UUID"]

    UUID --> ATTACHMENT["📎 EphemeralAttachment"]

    INDEX --> PARENT["👤 Parent Object"]

    classDef root fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef object fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef connection fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef field fill:#edf2f7,color:#1a202c,stroke:#a0aec0;
    classDef point fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef uuid fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;
    classDef attachment fill:#d53f8c,color:#fff,stroke:#97266d,stroke-width:2px;
    classDef parent fill:#319795,color:#fff,stroke:#285e61,stroke-width:2px;

    class ROOT root;
    class OBJECT object;
    class CONNECTION connection;
    class TYPE,LOCAL,POINT,INDEX field;
    class NUMERIC point;
    class UUID uuid;
    class ATTACHMENT attachment;
    class PARENT parent;
```

These identifiers have different purposes and should not be treated as interchangeable.

---

## 2. Object Type

The first value of an object tuple identifies the type of object.

Example:

```json
[
    "Part",
    [],
    {}
]
```

Here:

```js
Type = "Part"
```

The object type is represented by its name in the serialized object tuple.

Examples include:

```text
Base
Part
Servo
Sprite
Chassis
Wheel
Rope
Wire
Connector
```

The complete object catalog is documented separately.

---

## 3. LocalType

`LocalType` is the first value of a connection tuple.

```json
[
    LocalType,
    PrimaryID,
    PrimaryIndex
]
```

Example:

```json
["1", "5", 15]
```

Here:

```js
LocalType = "1"
```

`LocalType` is a numeric identifier associated with the local object type involved in the connection.
The game uses this value to identify/search for the corresponding object type.
The exact internal lookup mechanism is unknown.

### Important

The numeric value of `LocalType` should not currently be interpreted as a semantic code.
For example, knowing that:

```js
LocalType = "1"
```

does not by itself tell us what internal operation the number represents.
The currently observed mappings should therefore be treated as empirical mappings rather than decoded meanings.

---

## 3.1. LocalType Mappings (RtG-AI Analysis)

The following LocalType values were observed across 100+ save files by the RtG-AI pipeline. See [`../old-files/rtg-ai-tokens.md`](../old-files/rtg-ai-tokens.md#3-localtype-mappings) for the complete table.

| Object            | LocalType(s)              |
| ----------------- | ------------------------- |
| AltitudeSensor    | ["2"]                     |
| Anchor            | ["1"]                     |
| Arm               | ["1"]                     |
| BallSocket        | ["1"]                     |
| Balloon           | ["1"]                     |
| Base              | ["3"]                     |
| BeachBall         | ["6"]                     |
| BeachChair        | ["1"]                     |
| Bearing           | ["1"]                     |
| Board             | ["15"]                    |
| BouncyBall        | ["6"]                     |
| BowlingBall       | ["6"]                     |
| BrakeLight        | ["1"]                     |
| Bumper            | ["1"]                     |
| Button            | ["1", "3"]                |
| Camera            | ["1"]                     |
| Canister          | ["1"]                     |
| Cannon            | ["1"]                     |
| CannonBall        | ["1"]                     |
| Carrot            | ["1"]                     |
| Cinderblock       | ["1"]                     |
| Clipboard         | ["1"]                     |
| Cone              | ["3"]                     |
| Connector         | ["5"]                     |
| ConnectorBall     | ["6"]                     |
| Delayer           | ["2"]                     |
| Detacher          | ["1"]                     |
| DoorA             | ["1"]                     |
| DoorB             | ["1"]                     |
| DoorC             | ["1"]                     |
| DoorD             | ["1"]                     |
| EntitySensor      | ["7"]                     |
| FishBowl          | ["1"]                     |
| FuelTank          | ["2"]                     |
| GasCap            | ["1"]                     |
| Gate-AND          | ["4"]                     |
| Gate-NOT          | ["4"]                     |
| Gate-OR           | ["4"]                     |
| GlassBase         | ["3"]                     |
| GoldPotatoEngine  | ["1"]                     |
| Googie            | ["1"]                     |
| Gramby            | ["1"]                     |
| Grenade           | ["1"]                     |
| Gun               | ["2"]                     |
| Gyro              | ["1"]                     |
| HalfConnectorBall | ["6"]                     |
| Hood              | ["1"]                     |
| HulaDoll          | ["1"]                     |
| InputSensor       | ["2"]                     |
| Javelin           | ["1"]                     |
| Joint             | ["1", "2"]                |
| Joust             | ["1"]                     |
| Leafblower        | ["1"]                     |
| Leg               | ["1"]                     |
| Light             | ["1"]                     |
| Lock              | ["1"]                     |
| LongStick         | ["2"]                     |
| Looper            | ["1"]                     |
| Mag               | ["1"]                     |
| MatchingGyro      | ["2", "3"]                |
| MountedGun        | ["1"]                     |
| Note              | ["1"]                     |
| Part              | ["1"]                     |
| Pie               | ["1"]                     |
| Pipes             | ["1"]                     |
| Piston            | ["2"]                     |
| Plunger           | ["1"]                     |
| Poop              | ["1"]                     |
| PotatoEngine      | ["1"]                     |
| PressurePlate     | ["1", "2"]                |
| Propeller         | ["2"]                     |
| RPG               | ["1"]                     |
| Radio             | ["1"]                     |
| Recorder          | ["1"]                     |
| RemoteButton      | ["1", "3"]                |
| Rocket            | ["1"]                     |
| RockingChair      | ["1"]                     |
| Roof              | ["1"]                     |
| Rope              | ["1", "2"]                |
| RubberBand        | ["1", "2"]                |
| Seat              | ["1"]                     |
| Servo             | ["1"]                     |
| Servo_Physics     | ["1"]                     |
| ShortStick        | ["2"]                     |
| Shotgun           | ["2"]                     |
| Sledge            | ["1"]                     |
| Splitter          | ["3"]                     |
| Splitter_1        | ["3", "5"]                |
| Splitter_2        | ["3", "5", "9"]           |
| Splitter_3        | ["3", "5", "7", "9"]      |
| Splitter_4        | ["1", "3", "5", "7", "9"] |
| Spoiler           | ["2"]                     |
| SprayPaint        | ["1"]                     |
| SpringJuice       | ["1"]                     |
| Sprite            | ["1"]                     |
| StaringGyro       | ["1"]                     |
| SteeringGyro      | ["1"]                     |
| SteeringWheel     | ["1"]                     |
| Stick             | ["2"]                     |
| Switch            | ["1", "3"]                |
| Thruster          | ["1"]                     |
| Tire              | ["1"]                     |
| Toilet            | ["1"]                     |
| TripWire          | ["1", "3"]                |
| Trunk             | ["1"]                     |
| Uzi               | ["2"]                     |
| VelocitySensor    | ["2"]                     |
| Wheel             | ["1"]                     |
| Wing              | ["1"]                     |
| Wire              | ["1", "3"]                |
| WoodenChair       | ["2"]                     |
| YibYib            | ["2"]                     |

### Objects with NO LocalType
```
Chassis, Fricklet, wad
```

> **Important:** `noLocalType` is an **OBSERVATION OF THE DATASET**, not an absolute rule about the format.
> It means: "This object has not been observed in the child position (with connections) within the analyzed JSON dataset."
> It does **NOT** automatically mean: "This object can never have connections."
> The documentation must distinguish clearly between what was observed in the available examples and what is known about the format.

---

## 4. Connection Point IDs

A connection can use a numeric identifier to select a predefined connection point on the parent object.

Example:

```json
["1", "24", 15]
```

Here:

```js
LocalType   = "1"
PrimaryID  = "24"
PrimaryIndex = 15
```

The value:

```js
"24"
```

is a numeric connection-point identifier.

The identifier refers to a predefined point associated with the parent object's model.

Conceptually:

```mermaid
flowchart LR

    CHILD["🧩 Child"] --> CONNECTION["🔗 Connection"]

    CONNECTION --> INDEX["🔢 PrimaryIndex"]
    INDEX --> PARENT["👤 Parent Object"]

    CONNECTION --> POINT["📍 PrimaryID = Numeric ID"]
    POINT --> MOUNT["📌 Predefined Connection Point"]

    classDef child fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef connection fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef index fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef parent fill:#319795,color:#fff,stroke:#285e61,stroke-width:2px;
    classDef point fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef mount fill:#d69e2e,color:#744210,stroke:#975a16,stroke-width:2px;

    class CHILD child;
    class CONNECTION connection;
    class INDEX index;
    class PARENT parent;
    class POINT point;
    class MOUNT mount;
```

The meaning of individual numeric point IDs is documented in the historical object-ID research.

---

## 5. PrimaryID

`PrimaryID` is the name used by this documentation for the second value of a connection tuple.

It identifies the connection location/reference on the parent.

The field can contain different kinds of identifiers.

```mermaid
flowchart TD

    POINT["📍 PrimaryID"]

    POINT --> NUMERIC["🔢 Numeric Point ID"]
    POINT --> UUID["🆔 UUID"]

    classDef point fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef numeric fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef uuid fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;

    class POINT point;
    class NUMERIC numeric;
    class UUID uuid;
```

Therefore, `PrimaryID` should not be interpreted as being exclusively a numeric connection-point ID.

---

## 6. UUID

A connection can use a UUID instead of a predefined numeric connection-point ID.

Example:

```json
[
    "1",
    "{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}",
    1
]
```

Here:

```js
LocalType   = "1"
PrimaryID  = UUID
PrimaryIndex = 1
```

The UUID acts as a reference to an `EphemeralAttachment`.

It does not itself contain the attachment's spatial information.

Conceptually:

```mermaid
flowchart TD

    POINT["📍 PrimaryID"] --> UUID["🆔 UUID"]
    UUID --> ATTACHMENT["📎 EphemeralAttachment"]
    ATTACHMENT --> CFRAME["📐 CFrame"]

    classDef point fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef uuid fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef attachment fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef cframe fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;

    class POINT point;
    class UUID uuid;
    class ATTACHMENT attachment;
    class CFRAME cframe;
```

---

## 7. EphemeralAttachment UUIDs

An `EphemeralAttachment` is stored in the `Properties` dictionary of an object.

Example:

```json
{
    "EphemeralAttachments": {
        "{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}": {
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

The UUID is the key of the attachment dictionary.

Therefore:

```mermaid
flowchart TD

    UUID["🆔 UUID"]
    UUID --> ATTACHMENTS["📎 EphemeralAttachments [UUID]"]

    ATTACHMENTS --> PARTNAME["🧩 partName"]
    ATTACHMENTS --> CFRAME["📐 cframe"]

    classDef uuid fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef attachment fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef property fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;

    class UUID uuid;
    class ATTACHMENTS attachment;
    class PARTNAME,CFRAME property;
```

---

## 8. UUID and CFrame

The UUID itself does not encode the position of the attachment.
The spatial information is stored in its `cframe`.

```mermaid
flowchart LR
    UUID["UUID"] --> ATTACHMENT["EphemeralAttachment"]
    ATTACHMENT --> CFRAME["cframe"]
    CFRAME --> POSITION["Position"]
    CFRAME --> ROTATION["Rotation"]
```

The observed `cframe` contains 12 numeric values:

```json
[
    X, Y, Z,   // Position
    R1, R2, R3,   // 3x3 rotation matrix
    R4, R5, R6,
    R7, R8, R9
]
```

The first three values represent position.
The remaining nine values form the observed 3×3 rotation matrix.
The spatial position is relative to the coordinate system of the object hosting the attachment.

---

## 9. Synthetic UUIDs

The UUID does not appear to require a UUID generated specifically by Roblox.
Historical experiments demonstrated that externally generated UUIDs can be accepted when they follow the expected GUID format.

Example:

```json
{99999999-9999-4999-8999-999999999999}
```

This demonstrates that the UUID functions primarily as an identifier/reference key rather than as a cryptographic value tied to the original save.

---

## 9.1. LocalIDs — Connection Point IDs Per Object (RtG-AI Analysis)

The following connection point IDs (PrimaryID / PuntoPadre) were observed when each object type is used as a **parent** in connections. These are the numeric point IDs that child objects reference when connecting to these objects.

See [`../old-files/rtg-ai-tokens.md`](../old-files/rtg-ai-tokens.md#4-localids-connection-point-ids-per-object) for the complete table.

| Object            | LocalIDs                                                                                                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AltitudeSensor    | ["1"]                                                                                                                                                                  |
| Anchor            | ["2", "3", "4", "5"]                                                                                                                                                   |
| BallSocket        | ["2"]                                                                                                                                                                  |
| Base              | ["1", "2", "4", "5", "6"]                                                                                                                                              |
| BeachBall         | ["1", "3", "7", "8", "9", "10", "12", "14", "15", "17", "18"]                                                                                                          |
| Bearing           | ["2"]                                                                                                                                                                  |
| Board             | ["1", "2", "3", "7", "13", "14"]                                                                                                                                       |
| BouncyBall        | ["1", "7", "8", "9", "11", "12", "13", "14", "18"]                                                                                                                     |
| BowlingBall       | ["1", "2", "3", "4", "5", "7", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]                                                                              |
| Briefcase         | ["2", "3"]                                                                                                                                                             |
| Bumper            | ["2"]                                                                                                                                                                  |
| Button            | ["2"]                                                                                                                                                                  |
| Cannon            | ["2"]                                                                                                                                                                  |
| Chassis           | ["1", "2", "3", "4", "5", "6", "7", "8", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "26", "27", "28", "29", "30", "31"] |
| Cinderblock       | ["2"]                                                                                                                                                                  |
| Cone              | ["2"]                                                                                                                                                                  |
| Connector         | ["1", "2", "3", "4", "6"]                                                                                                                                              |
| ConnectorBall     | ["1", "2", "3", "4", "5", "7", "8", "9", "10", "11", "12", "13", "14", "16", "17", "18"]                                                                               |
| Delayer           | ["1"]                                                                                                                                                                  |
| Detacher          | ["2"]                                                                                                                                                                  |
| EntitySensor      | ["1", "2", "3", "4", "5", "6"]                                                                                                                                         |
| FuelTank          | ["1"]                                                                                                                                                                  |
| Gate-AND          | ["1", "2", "3"]                                                                                                                                                        |
| Gate-NOT          | ["1", "2"]                                                                                                                                                             |
| Gate-OR           | ["1", "2", "3"]                                                                                                                                                        |
| GlassBase         | ["1", "2", "4"]                                                                                                                                                        |
| Gun               | ["1"]                                                                                                                                                                  |
| HalfConnectorBall | ["2", "3", "4", "5", "7", "10", "11", "13", "14", "15", "16", "17", "18"]                                                                                              |
| Hood              | ["2"]                                                                                                                                                                  |
| InputSensor       | ["1"]                                                                                                                                                                  |
| LongStick         | ["1"]                                                                                                                                                                  |
| Looper            | ["2", "4", "5"]                                                                                                                                                        |
| MatchingGyro      | ["1", "4", "5", "6", "7", "8"]                                                                                                                                         |
| Part              | ["2", "3", "4", "5", "6"]                                                                                                                                              |
| Pipes             | ["2", "3", "4", "5"]                                                                                                                                                   |
| Piston            | ["1", "3", "4"]                                                                                                                                                        |
| PressurePlate     | ["3"]                                                                                                                                                                  |
| Propeller         | ["1"]                                                                                                                                                                  |
| RPG               | ["2"]                                                                                                                                                                  |
| RemoteButton      | ["2"]                                                                                                                                                                  |
| Roof              | ["7"]                                                                                                                                                                  |
| Servo             | ["2", "3", "4"]                                                                                                                                                        |
| Servo_Physics     | ["2", "3", "4"]                                                                                                                                                        |
| ShoppingCart      | ["1", "2", "4", "6", "7", "9", "14"]                                                                                                                                   |
| ShortStick        | ["1"]                                                                                                                                                                  |
| Shotgun           | ["1"]                                                                                                                                                                  |
| Splitter          | ["4"]                                                                                                                                                                  |
| Splitter_1        | ["4", "6"]                                                                                                                                                             |
| Splitter_2        | ["4", "6", "10"]                                                                                                                                                       |
| Splitter_3        | ["4", "6", "8", "10"]                                                                                                                                                  |
| Splitter_4        | ["2", "4", "6", "8", "10"]                                                                                                                                             |
| Spoiler           | ["2"]                                                                                                                                                                  |
| StaringGyro       | ["2"]                                                                                                                                                                  |
| Stick             | ["1"]                                                                                                                                                                  |
| Switch            | ["2"]                                                                                                                                                                  |
| Tire              | ["2"]                                                                                                                                                                  |
| TripWire          | ["2"]                                                                                                                                                                  |
| Trunk             | ["2"]                                                                                                                                                                  |
| Uzi               | ["1"]                                                                                                                                                                  |
| VelocitySensor    | ["1"]                                                                                                                                                                  |
| Wheel             | ["2"]                                                                                                                                                                  |
| Wing              | ["2"]                                                                                                                                                                  |
| Wire              | ["2", "4"]                                                                                                                                                             |
| YibYib            | ["2"]                                                                                                                                                                  |

### Objects with NO LocalIDs
```
wad, Fricklet
```

> **Important:** `noLocalIds` is an **OBSERVATION OF THE DATASET**, not an absolute rule about the format.
> It means: "This object has not been observed in the parent position (with connection points) within the analyzed JSON dataset."
> It does **NOT** automatically mean: "This object can never be a connection parent."
> The documentation must distinguish clearly between what was observed in the available examples and what is known about the format.

These objects cannot be used as connection parents (no predefined connection points).

---

## 10. PrimaryIndex

`PrimaryIndex` is the third value of a connection tuple.

```json
[
    LocalType,
    PrimaryID,
    PrimaryIndex
]
```

It identifies the parent object in the root object array.
RtG uses a **1-based logical object index**.

Example:

```json
[
    ["Base", [], {}],
    ["Part", [["1", "5", 1]], {}]
]
```

The connection contains:

```js
PrimaryIndex = 1
```

which refers to the first logical object:

```js
1 = "Base"
```

The detailed indexing rules are documented in [`indexing.md`](indexing.md).

---

## 11. Identifier Relationships

A complete connection can therefore be understood as:

```mermaid
flowchart TD

    CONNECTION["🔗 Connection"] --> LOCAL["🔧 LocalType"]
    CONNECTION --> POINT["📍 PrimaryID"]
    CONNECTION --> INDEX["🔢 PrimaryIndex"]

    LOCAL --> TYPE["🏷️ Local Object Type"]

    POINT --> NUMERIC["🔢 Numeric Point ID"]
    POINT --> UUID["🆔 UUID"]

    NUMERIC --> PREDEFINED["📌 Predefined Connection Point"]

    UUID --> ATTACHMENT["📎 EphemeralAttachment"]
    ATTACHMENT --> CFRAME["📐 CFrame"]

    INDEX --> PARENT["👤 Parent Object"]

    classDef connection fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef field fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef type fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef numeric fill:#d69e2e,color:#744210,stroke:#975a16,stroke-width:2px;
    classDef uuid fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef attachment fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:2px;
    classDef cframe fill:#319795,color:#fff,stroke:#285e61,stroke-width:2px;
    classDef parent fill:#d53f8c,color:#fff,stroke:#97266d,stroke-width:2px;

    class CONNECTION connection;
    class LOCAL,POINT,INDEX field;
    class TYPE type;
    class NUMERIC,PREDEFINED numeric;
    class UUID uuid;
    class ATTACHMENT attachment;
    class CFRAME cframe;
    class PARENT parent;
```

The three connection fields answer different questions:

```mermaid
flowchart TD

    CONNECTION["🔗 Connection"]

    CONNECTION --> LOCAL["🔧 LocalType"]
    LOCAL --> LOCAL_DESC["❓ What type of local object is involved?"]

    CONNECTION --> POINT["📍 PrimaryID"]
    POINT --> POINT_DESC["❓ What connection point/reference on the parent is used?"]

    CONNECTION --> INDEX["🔢 PrimaryIndex"]
    INDEX --> INDEX_DESC["❓ Which object is the parent?"]

    classDef connection fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef field fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef description fill:#edf2f7,color:#1a202c,stroke:#a0aec0,stroke-width:2px;

    class CONNECTION connection;
    class LOCAL,POINT,INDEX field;
    class LOCAL_DESC,POINT_DESC,INDEX_DESC description;
```

---

## 12. What Each Identifier Does Not Mean

### LocalType

Does **not** currently have a fully decoded semantic meaning.
It is an observed numeric identifier used by the game to identify/search for the local object type.

### PrimaryID

Is **not always a numeric connection-point ID**.
It can contain a UUID referencing an `EphemeralAttachment`.

### UUID

Does **not** directly encode the spatial position.
The position is stored in the referenced attachment's `cframe`.

### PrimaryIndex

Is **not a UUID or object ID stored independently**.
It is a 1-based logical reference to an object in the root array.

---

## 13. Historical Identifier Research

The historical research contains the most extensive catalog of observed connection-point IDs.

See:

[`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md)

That document contains:

* observed object types;
* connection-point IDs;
* descriptive names;
* experimental descriptions;
* methodology used to identify points;
* unresolved and incomplete mappings.

Additional connection point IDs from RtG-AI analysis are documented in [`../old-files/rtg-ai-tokens.md`](../old-files/rtg-ai-tokens.md#4-localids-connection-point-ids-per-object).

The historical file should be consulted before declaring an identifier mapping unknown or inventing a new mapping.

---

## 14. Evidence Status

The identifier system currently has the following confidence levels:

| Identifier                           | Status             | Meaning                                                                    |
| ------------------------------------ | ------------------ | -------------------------------------------------------------------------- |
| Object Type                          | Confirmed          | Identifies the serialized object type                                      |
| LocalType                            | Confirmed behavior | Used to identify/search for the local object type; internal lookup unknown |
| Numeric connection-point ID          | Confirmed behavior | References a predefined connection point                                   |
| PrimaryID                            | Confirmed          | Second connection field; can contain numeric ID or UUID                    |
| PrimaryIndex                         | Confirmed          | 1-based logical parent-object reference                                    |
| UUID                                 | Confirmed          | References an `EphemeralAttachment`                                        |
| UUID → CFrame                        | Confirmed          | Attachment lookup provides the spatial transform                           |
| Exact internal UUID implementation   | Unknown            | Game implementation not available                                          |
| Semantic meaning of every numeric ID | Incomplete         | Not every mapping has been fully verified                                  |

---

## Related Documentation

* [`../SPECIFICATION.md`](../SPECIFICATION.md) — Complete format specification.
* [`json-structure.md`](json-structure.md) — JSON structure.
* [`indexing.md`](indexing.md) — Object indexing and parent references.
* [`properties.md`](properties.md) — Object properties.
* [`../blocks/`](../blocks/) — Object and Part documentation.
* [`../examples/experiments/`](../examples/experiments/) — Experimental saves and evidence.
* [`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md) — Historical identifier research.
