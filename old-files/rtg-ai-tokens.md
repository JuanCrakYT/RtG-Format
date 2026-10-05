# Datos de análisis de tokens de RtG-AI

> **Fuente:** `tools/RtG-AI/dev/tokens.json`  
> **Generado por:** análisis del pipeline de RtG-AI sobre más de 100 archivos de guardado  
> **Fecha de actualización:** 5/10/2026
> **Versión de la Especificación:** v1.02
> **Estado:** Documento Experimental / No Oficial

Este documento conserva los datos de clasificación de tokens e identificadores extraídos por el pipeline de análisis de RtG-AI. Estos datos complementan la investigación histórica de `obj_ids-spanish.md` y proporcionan clasificaciones adicionales de tipos de propiedades e IDs de puntos de conexión que no estaban documentados anteriormente.

---

## 1. Catálogo de nombres de objetos

Los siguientes objetos fueron identificados en todos los guardados analizados (126 objetos únicos):

```text
AltitudeSensor, Anchor, Arm, BallSocket, Balloon, Base, BeachBall,
BeachChair, Bearing, Board, Body, BouncyBall, BowlingBall, BrakeLight,
Briefcase, Bumper, Button, Camera, Canister, Cannon, CannonBall, Carrot,
Chassis, Cinderblock, Clipboard, Cone, Connector, ConnectorBall, Delayer,
Detacher, DoorA, DoorB, DoorC, DoorD, EntitySensor, FishBowl, Fricklet,
FuelTank, GasCap, Gate-AND, Gate-NOT, Gate-OR, GlassBase, GoldPotatoEngine,
Googie, Gramby, Grenade, Gun, Gyro, HalfConnectorBall, Head, Hood,
HulaDoll, InputSensor, Javelin, Joint, Joust, Jug, Keyboard, Leafblower,
Leg, Light, Lock, LongStick, Looper, Mag, MatchingGyro, MountedGun, Note,
Part, Pie, Pipes, Piston, Plunger, PolaroidCamera, PolaroidPhoto, Poop,
PotatoEngine, PressurePlate, Propeller, RPG, Radio, Ramp, Recorder,
RemoteButton, RiotShield, Rocket, RockingChair, Roof, Rope, RubberBand,
Seat, Servo, Servo_Physics, ShoppingCart, ShortStick, Shotgun, Sledge,
Splitter, Splitter_1, Splitter_2, Splitter_3, Splitter_4, Spoiler,
SprayPaint, SpringJuice, Sprite, StaringGyro, SteeringGyro, SteeringWheel,
Stick, Successor, SuperPowerClock, Switch, Thruster, Tire, Toilet, ToolGun,
Tooth, TripWire, Trunk, Uzi, VelocitySensor, Wheel, Wing, Wire, WoodenChair,
YibYib, wad
```

**Nota:** `Chassis`, `Fricklet` y `wad` aparecen en la lista de objetos, pero tienen un tratamiento especial (sin `LocalType`).

---

## 2. Clasificación de tipos de propiedades

Propiedades observadas en todos los guardados, clasificadas según el tipo de valor JSON:

### 2.1 Propiedades de tipo String

```text
ActivationKey, MeshId, Mode, Name, Phrase, Text, TextureID, TextureId,
className, objectId, partName, serializedType
```

### 2.2 Propiedades de tipo Number

```text
ActivationHeight, ActivationSpeed, Channel, Delay, ItemTurn, Length,
LimitAngle, MaxDistance, MaxForce, MaxLength, MinLength, OrientationX,
OrientationY, OrientationZ, Rotation, Speed, Transparency, Volume
```

### 2.3 Propiedades de tipo Boolean

```text
Activated, Backwards, CanTargetAttached, Deactivated, DelayDeactivation,
DisabledInput, Forwards, IgnoreAttached, LimitEnabled, On, Rest, Reverse,
Shooting, Visible
```

### 2.4 Propiedades de tipo Integer

```text
Bullets, CustomTrack, ImageId, Quantity
```

### 2.5 Propiedades de tipo Array

```text
RGB, cframe, children, data, sceneCullObjects, sceneUpdateObjects
```

### 2.6 Propiedades de tipo Object

```text
CFrame, Color, EphemeralAttachments, Material, MeshType, Offset, PhotoData,
Scale, Shape, Size, cameraCF, props, sceneNewObjects
```

---

## 3. Mapeos de LocalType

Valores de `LocalType` (`TipoLocal`) observados para cada tipo de objeto:

| Objeto            | LocalType(s)              |
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

### Objetos SIN LocalType

```text
Chassis, Fricklet, wad
```

> **Importante:** `noLocalType` es una **OBSERVACIÓN DEL CONJUNTO DE DATOS**, no una afirmación absoluta sobre el formato.
> Significa: "No se ha observado este objeto en posición de hijo (con conexiones) dentro del conjunto de JSON analizados".
> **NO significa automáticamente:** "Este objeto nunca puede tener conexiones".
> La documentación debe distinguir claramente entre lo observado en los ejemplos disponibles y lo que conocemos del formato.

---

## 4. LocalIDs (IDs de puntos de conexión por objeto)

IDs de puntos de conexión observados (`PrimaryID` / `PuntoPadre`) para cada tipo de objeto. Estos son los IDs numéricos de punto utilizados al realizar conexiones **HACIA estos objetos como padres**.

| Objeto            | LocalIDs                                                                                                                                                               |
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

### Objetos SIN LocalIDs

```text
wad, Fricklet
```

> **Importante:** `noLocalIds` es una **OBSERVACIÓN DEL CONJUNTO DE DATOS**, no una afirmación absoluta sobre el formato.
> Significa: "No se ha observado este objeto en posición de padre (con puntos de conexión propios) dentro del conjunto de JSON analizados".
> **NO significa automáticamente:** "Este objeto nunca puede ser padre de conexiones".
> La documentación debe distinguir claramente entre lo observado en los ejemplos disponibles y lo que conocemos del formato.

---

## 5. Tokens especiales (tokenizador T5)

### 5.1 Tokens de secuencia

```text
<pad>  - Token de relleno para el procesamiento por lotes
</s>   - Marcador de fin de secuencia
Ġ      - Carácter Unicode de espacio (G con punto arriba), cubre cualquier carácter fuera del vocabulario
```

**Nota:** T5 requiere estos tres tokens como mínimo. `</s>` marca el final de la secuencia, `<pad>` rellena los lotes y `Ġ` cubre cualquier carácter fuera del vocabulario que se filtre.

---

## 6. Vocabulario de caracteres

### 6.1 Caracteres hexadecimales

```text
a, b, c, d, e, f, A, B, C, D, E, F
```

### 6.2 Números

```text
1, 2, 3, 4, 5, 6, 7, 8, 9, 0
```

### 6.3 Símbolos

```text
-, .
```

### 6.4 Caracteres estructurales de JSON

```text
", {, }, [, ], :, ,
```

---

## 7. Notas sobre la evidencia

- Datos extraídos de más de 100 archivos de guardado en `tools/RtG-AI/dev/json/`
- Los tipos de propiedades se infirieron a partir de los tipos de valores JSON presentes en todas las muestras
- `LocalType` y `LocalIDs` se observaron a partir de las tuplas de conexión presentes en los guardados
- Algunos objetos tienen múltiples valores de `LocalType` (por ejemplo, `Button: ["1","3"]` y las variantes de `Splitter`)
- Los IDs de puntos de conexión son representaciones de números como strings en el JSON
- Estos datos deben cruzarse con `obj_ids-spanish.md` para su validación

---

## 8. Comparación con los datos históricos

### Coincidencias confirmadas (`obj_ids-spanish.md`, tabla final)

- La mayoría de los valores de `LocalType` coinciden con la columna histórica "TipoLocal"
- Los nombres de objetos coinciden con el catálogo histórico

### Nuevos datos provenientes de RtG-AI

- Clasificación de tipos de propiedades (`String`/`Number`/`Boolean`/`Integer`/`Array`/`Object`)
- `LocalIDs` completos para cada objeto (puntos de conexión cuando se utilizan como padre)
- Listas `noLocalType` y `noLocalIds`
- `SpecialTokens` para el tokenizador T5
- Desglose del vocabulario de caracteres

### Discrepancias que deben investigarse

- **Múltiples LocalTypes por objeto:** varios objetos tienen múltiples valores de `LocalType` en los datos de RtG-AI, pero solo un `TipoLocal` en la documentación histórica (por ejemplo: `Button: ["1","3"]`, `Switch: ["1","3"]`, `Wire: ["1","3"]`, `RemoteButton: ["1","3"]`, `TripWire: ["1","3"]`, `Splitter_1: ["3","5"]`, `Splitter_2: ["3","5","9"]`, `Splitter_3: ["3","5","7","9"]`, `Splitter_4: ["1","3","5","7","9"]`, `Joint: ["1","2"]`, `Rope: ["1","2"]`, `RubberBand: ["1","2"]`, `MatchingGyro: ["2","3"]`, `PressurePlate: ["1","2"]`).
- **`LocalIDs` proporciona IDs de puntos de conexión** que no estaban completamente catalogados en la investigación histórica.
- **Objetos sin LocalType en los datos históricos pero con LocalType en RtG-AI:** `GasCap` (histórico: "—", RtG-AI: `"1"`), `PressurePlate` (no aparece en la tabla histórica, RtG-AI: `["1","2"]`), `Javelin` (no aparece en la tabla histórica, RtG-AI: `"1"`).
- **Objetos con LocalType en los datos históricos pero presentes en `noLocalType` en RtG-AI:** `ShoppingCart` (histórico: "—", RtG-AI: `noLocalType`), `SuperPowerClock` (histórico: "—", RtG-AI: `noLocalType`), `Successor` (histórico: `"2"`, RtG-AI: `["2"]`), `YibYib` (histórico: "—", RtG-AI: `["2"]`).
- **`EntitySensor`** tiene `LocalType "7"` en ambos conjuntos (coincidencia).
- **`Board`** tiene `LocalType "15"` en ambos conjuntos (coincidencia).