# RtG Build Format

> **Hecho por:** @JuanCrakYT
> **Documento:** Especificación Técnica de Formato de Guardado (Ingeniería Inversa)  
> **Juego Objetivo:** Road To Gramby's (Roblox)  
> **Versión de la Especificación:** v1.02
> **Estado:** Documento Experimental / No Oficial  

# Catálogo de IDs de Puntos de Conexión
> **Hecho por:** @JuanCrakYT
Este documento cataloga el significado del **IDdelPunto** de las conexiones de cada objeto.

Formato de una conexión:
```json
["TipoDelBloque", "IDdelPunto", ÍndicePadre]
```
Ejemplo:
```json
["1", "24", 15]
```
donde:

- TipoDelBloque = Categoría de conexión.
- IDdelPunto = ID del punto de conexión del objeto padre.
- ÍndicePadre = Índice del objeto al que está conectado.

---

## Objetivo

Asignar un nombre y una posición a cada ID de conexión de cada objeto.

Esto permitirá:

- Crear builds automáticamente.
- Conectar piezas sin Roblox Studio.
- Generar vehículos completos.
- Crear un editor visual.
- Detectar conexiones inválidas.

---

## Convenciones
> **Hecho por:** @JuanCrakYT
Cada objeto tendrá su propia sección.

Cada punto deberá documentarse con:

| ID  | Nombre | Descripción |
| --- | ------ | ----------- |

Si el nombre oficial no existe, utilizar uno descriptivo.

Ejemplo:

| ID  | Nombre            | Descripción               |
| --- | ----------------- | ------------------------- |
| 1   | Front Left Wheel  | Rueda delantera izquierda |
| 2   | Front Right Wheel | Rueda delantera derecha   |

### Convenciones 1.1

#### ID
Número utilizado por RtG para identificar un punto de conexión.

#### Nombre
Nombre descriptivo del punto de conexión.

Ejemplos:

- Wheel_FL
- Wheel_FR
- Roof
- Hood
- Engine
- Seat_Driver

#### Lado

Utilizar únicamente los siguientes valores:

- Front
- Back
- Left
- Right
- Front Left
- Front Right
- Back Left
- Back Right
- Side Left
- Side Right
- Top
- Top Left
- Top Right
- Bottom
- Bottom Left
- Bottom Right
- Center
- Inside
- Outside
- Unknown

#### Descripción

Explica brevemente qué objeto suele conectarse ahí.

Ejemplo:

"Conecta la rueda delantera izquierda."

---

## Metodología
> **Hecho por:** @JuanCrakYT
Para identificar un ID:

1. Pintar el objeto con un color único.
2. Exportar la build.
3. Asociar el color con el ID observado.
4. Repetir para todos los IDs del objeto.
5. Confirmar el resultado reconstruyendo la build.
6. Validar el ID conectando el objeto a diferentes padres compatibles para confirmar que el punto pertenece al objeto y no al padre.

Cuando existan objetos simétricos (ruedas, luces, asientos, etc.), utilizar colores distintos para identificar izquierda, derecha, delantero y trasero.

---

## Lista de todos los objetos:
> **Hecho por:** @JuanCrakYT
1. AltitudeSensor
2. Anchor
3. Arm
4. Balloon
5. BallSocket
6. Base
7. BeachBall
8. BeachChair
9. Bearing
10. Board
11. BouncyBall
12. BowingBall
13. BrakeLight
14. Briefcase
15. Bumper
16. Button
17. Camera
18. Cannon
19. CannonBall
20. Canister
21. Carrot
22. Chassis
23. Cinderblock
24. Clipboard
25. Cone
26. Connector
27. ConnectorBall
28. Delayer
29. Detacher
30. DoorA
31. DoorB
32. DoorC
33. DoorD
34. EntitySensor
35. FishBowl
36. FuelTank
37. GasCap
38. Gate-AND
39. Gate-NOT
40. Gate-OR
41. GlassBase
42. GoldPotatoEngine
43. Googie
44. Gramby
45. Grenade
46. Guitar
47. Gyro
48. HalfConnectorBall
49. Hood
50. HulaDoll
51. InputSensor
52. Joint
53. Joust
54. Jug
55. Keyboard
56. Leafblower
57. Leg
58. Light
59. Lock
60. Looper
61. LongStick
62. Mag
63. MatchingGyro
64. MountedGun
65. Note
66. Part
67. Pie
68. Pipes
69. Piston
70. Plunger
71. Poop
72. PotatoEngine
73. PressurePlate
74. Propeller
75. Radio
76. Ramp
77. Recorder
78. RemoteButton
79. RPG
80. RiotShield
81. RockingChair
82. Rocket
83. Roof
84. Rope
85. RubberBand
86. Seat
87. Servo
88. Servo_Physics
89. ShortStick
90. ShoppingCart
91. Shotgun
92. Sledge
93. SprayPaint
94. Sprite
95. Spoiler
96. SpringJuice
97. Splitter_1
98.  Splitter_2
99.  Splitter_3
100. Splitter_4
101. StaringGyro
102. SteeringGyro
103. SteeringWheel
104. Stick
105. Switch
106. Thruster
107. Tire
108. Toilet
109. ToolGun
110. Tooth
111. TripWire
112. Trunk
113. Uzi
114. VelocitySensor
115. Wheel
116. Wire
117. WoodenChair
118. Wad
119. Head
120. Body
121. Fricklet
122. SuperPowerClock
123. YibYib
---

## Objetos con puntos de conexión propios
> Aquí encontraras el "IDdelPunto" de cada objeto
> **Hecho por:** @JuanCrakYT

### 1. Chassis

Cantidad de IDs encontrados: 26

| ID  | Nombre            | Lado         | Descripción                                   |
| --- | ----------------- | ------------ | --------------------------------------------- |
| 1   | Wheel_FL          | Front Left   | Anclaje de la rueda delantera izquierda.      |
| 2   | PassengerSteering | Front Right  | Punto para un volante en el asiento copiloto. |
| 3   | Hood              | Front        | Anclaje del capó.                             |
| 4   | Wheel_FR          | Front Right  | Anclaje de la rueda delantera derecha.        |
| 5   | Wheel_BL          | Back Left    | Anclaje de la rueda trasera izquierda.        |
| 6   | Wheel_BR          | Back Right   | Anclaje de la rueda trasera derecha.          |
| 7   | Roof              | Top          | Anclaje del techo.                            |
| 8   | Headlight_R       | Front Right  | Anclaje de la luz delantera derecha.          |
| 9   | SideAux_B         | Side Right   | Punto auxiliar ubicado en un lateral.         |
| 10  | SteeringWheel     | Front Center | Anclaje del volante.                          |
| 11  | BrakeLight_R      | Back Right   | Anclaje de la luz trasera derecha.            |
| 12  | Trunk             | Back Center  | Anclaje del maletero.                         |
| 13  | DriverSeat        | Front Left   | Asiento del conductor.                        |
| 14  | PassengerSeat     | Front Right  | Asiento del copiloto.                         |
| 15  | BrakeLight_L      | Back Left    | Anclaje de la luz trasera izquierda.          |
| 16  | SideAux_A         | Side Left    | Punto auxiliar ubicado en un lateral.         |
| 17  | Headlight_L       | Front Left   | Anclaje de la luz delantera izquierda.        |
| 18  | RearSeat_L        | Back Left    | Asiento trasero izquierdo.                    |
| 19  | TrunkAux_A        | Back Left    | Punto auxiliar ubicado en el maletero.        |
| 20  | GasCap            | Back Left    | Anclaje de la tapa del combustible.           |
| 21  | TrunkAux_B        | Back Right   | Punto auxiliar ubicado en el maletero.        |
| 22  | RearBumper        | Back         | Anclaje del parachoques trasero.              |
| 23  | FrontBumper       | Front        | Anclaje del parachoques delantero.            |
| 24  | Engine            | Front Center | Anclaje del motor.                            |
| 25  | RearSeat_R        | Back Right   | Asiento trasero derecho.                      |
| 26  | Gyro              | Center       | Anclaje del giroscopio (Gyro).                |

### 2. Wheel

Cantidad de IDs encontrados: 1

| ID  | Nombre       | Lado   | Descripción                                  |
| --- | ------------ | ------ | -------------------------------------------- |
| 1   | ChassisMount | Center | Punto de conexión de la rueda con el chasis. |

---

### 3. Tire

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado   | Descripción                                                 |
| --- | ---------- | ------ | ----------------------------------------------------------- |
| 1   | WheelMount | Center | Punto de conexión de la llanta con una rueda u otro objeto. |

---

### 4. Bumper

Cantidad de IDs encontrados: 1

| ID  | Nombre       | Lado | Descripción                                      |
| --- | ------------ | ---- | ------------------------------------------------ |
| 1   | ChassisMount | Top  | Punto de conexión del parachoques con el chasis. |

---

### 5. Hood

Cantidad de IDs encontrados: 1

| ID  | Nombre       | Lado  | Descripción                               |
| --- | ------------ | ----- | ----------------------------------------- |
| 1   | ChassisMount | Front | Punto de conexión del capó con el chasis. |

---

### 6. Trunk

Cantidad de IDs encontrados: 1

| ID  | Nombre       | Lado  | Descripción                                   |
| --- | ------------ | ----- | --------------------------------------------- |
| 1   | ChassisMount | Front | Punto de conexión del maletero con el chasis. |

### 7. Cannon

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado | Descripción                                  |
| --- | ---------- | ---- | -------------------------------------------- |
| 1   | MountPoint | Top  | Punto de conexión del cañón con otro objeto. |

---

### 8. Propeller

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                     |
| --- | ---------- | ------- | ----------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión de la hélice con otro objeto. |

---

### 9. Bearing

Cantidad de IDs encontrados: 1

| ID  | Nombre       | Lado   | Descripción                                                                  |
| --- | ------------ | ------ | ---------------------------------------------------------------------------- |
| 1   | RotationAxis | Center | Punto de conexión utilizado para colocar un spinner en un sistema de ruedas. |

---

### 10. Wing

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                |
| --- | ---------- | ------- | ------------------------------------------ |
| 1   | MountPoint | Unknown | Punto de conexión del ala con otro objeto. |

### 11. ShortStick

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado | Descripción                                       |
| --- | ---------- | ---- | ------------------------------------------------- |
| 1   | MountPoint | Top  | Punto de conexión del palo corto con otro objeto. |

---

### 12. Stick

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado | Descripción                                 |
| --- | ---------- | ---- | ------------------------------------------- |
| 1   | MountPoint | Top  | Punto de conexión del palo con otro objeto. |

---

### 13. LongStick

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado | Descripción                                       |
| --- | ---------- | ---- | ------------------------------------------------- |
| 1   | MountPoint | Top  | Punto de conexión del palo largo con otro objeto. |

---

### ???

Cantidad de IDs encontrados: ???

---

### 15. Spoiler

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                    |
| --- | ---------- | ------- | ---------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión del spoiler con otro objeto. |

---

### 16. Leg

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                     |
| --- | ---------- | ------- | ----------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión de la pierna con otro objeto. |

---

### 17. Button

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                  |
| --- | ------ | ------- | -------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del botón con otro objeto. |

---

### 18. InputSensor

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                              |
| --- | ------ | ------- | -------------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del sensor de entrada con otro objeto. |

---

### 19. AltitudeSensor

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                             |
| --- | ------ | ------- | ------------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del sensor de altura con otro objeto. |

---

### 20. VelocitySensor

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                                |
| --- | ------ | ------- | ---------------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del sensor de velocidad con otro objeto. |

---

### 21. Switch

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                        |
| --- | ------ | ------- | -------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del interruptor con otro objeto. |

---

### 22. TripWire

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                         |
| --- | ---------- | ------- | --------------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión del cable trampa con otro objeto. |

---

### 23. RemoteButton

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                         |
| --- | ------ | ------- | --------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión del botón remoto con otro objeto. |

---

### 24. PressurePlate

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado    | Descripción                                               |
| --- | ------ | ------- | --------------------------------------------------------- |
| 1   | Output | Unknown | Punto de conexión de la placa de presión con otro objeto. |

---

### 25. Detacher

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                      |
| --- | ---------- | ------- | ------------------------------------------------ |
| 1   | MountPoint | Unknown | Punto de conexión del separador con otro objeto. |

---

### 26. RPG

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                |
| --- | ---------- | ------- | ------------------------------------------ |
| 1   | MountPoint | Unknown | Punto de conexión del RPG con otro objeto. |

### 27. StaringGyro

Cantidad de IDs encontrados: 2

| ID  | Nombre | Lado  | Descripción                                  |
| --- | ------ | ----- | -------------------------------------------- |
| 2   | Front  | Front | Punto de conexión delantero del StaringGyro. |
| 3   | Back   | Back  | Punto de conexión trasero del StaringGyro.   |

### 28. Piston

Cantidad de IDs encontrados: 3

| ID  | Nombre    | Lado  | Descripción                                           |
| --- | --------- | ----- | ----------------------------------------------------- |
| 1   | PushEnd   | Front | Punto donde el pistón realiza el empuje o movimiento. |
| 3   | Side_Red  | Back  | Punto de conexión del lado rojo del pistón.           |
| 4   | Side_Blue | Front | Punto de conexión del lado azul del pistón.           |

> Nota:

>> El color verde parece ser el extremo móvil (`PushEnd`), no una entrada.
>> Los puntos 3 y 4 son los extremos fijos/entradas del pistón y tienen orientación opuesta.

### 29. Servo

Cantidad de IDs encontrados: 3

| ID  | Nombre       | Lado   | Descripción                                            |
| --- | ------------ | ------ | ------------------------------------------------------ |
| 2   | RotationAxis | Center | Punto del eje de giro del servo.                       |
| 3   | Side_Red     | Left   | Punto lateral del servo identificado por el lado rojo. |
| 4   | Side_Blue    | Right  | Punto lateral del servo identificado por el lado azul. |

> Notas:

>> El ID 2 parece ser el punto funcional principal, ya que está asociado al eje que gira.
>> Los IDs 3 y 4 parecen ser puntos de montaje opuestos, similares a los del `Piston`.

### 30. Servo_Physics

Cantidad de IDs encontrados: 3

| ID  | Nombre       | Lado   | Descripción                                                   |
| --- | ------------ | ------ | ------------------------------------------------------------- |
| 2   | RotationAxis | Center | Punto del eje de movimiento del servo físico.                 |
| 3   | Side_Red     | Left   | Punto lateral del servo físico identificado por el lado rojo. |
| 4   | Side_Blue    | Right  | Punto lateral del servo físico identificado por el lado azul. |

> Notas:

>> Tiene la misma distribución que `Servo`.
>>> La diferencia es que `Servo_Physics` utiliza simulación física (`Backwards`, `Forwards`, `Rest`) mientras que `Servo` parece ser el servo estándar.
>>El ID 2 corresponde al elemento que gira/mueve.
>>>Los IDs 3 y 4 son los puntos de montaje laterales.

### 31. Anchor

Cantidad de IDs encontrados: 4

| ID  | Nombre      | Lado         | Descripción                                                 |
| --- | ----------- | ------------ | ----------------------------------------------------------- |
| 2   | TopLeft     | Top Left     | Punto de conexión ubicado arriba a la izquierda del Anchor. |
| 3   | TopRight    | Top Right    | Punto de conexión ubicado arriba a la derecha del Anchor.   |
| 4   | BottomLeft  | Bottom Left  | Punto de conexión ubicado abajo a la izquierda del Anchor.  |
| 5   | BottomRight | Bottom Right | Punto de conexión ubicado abajo a la derecha del Anchor.    |

> Notas:

>> El `Anchor` utiliza una distribución de 4 puntos formando una matriz de esquinas.
>>> No tiene un punto central.

### 32. BallSocket

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                                    |
| --- | ---------- | ------- | -------------------------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión de la articulación esférica con otro objeto. |

> Notas:

>> `BallSocket` solo tiene un punto propio confirmado.
>> El punto parece funcionar como el punto principal donde se conecta la articulación, similar a `Joint`, pero con movimiento esférico.

### 33. MatchingGyro

Cantidad de IDs encontrados: 5

| ID  | Nombre      | Lado   | Descripción                                                                  |
| --- | ----------- | ------ | ---------------------------------------------------------------------------- |
| 1   | HandleMount | Center | Punto de conexión donde se coloca el mango o eje principal del MatchingGyro. |
| 4   | Right       | Right  | Punto de conexión ubicado en el lado derecho del MatchingGyro.               |
| 5   | Top         | Top    | Punto de conexión ubicado en la parte superior del MatchingGyro.             |
| 6   | Left        | Left   | Punto de conexión ubicado en el lado izquierdo del MatchingGyro.             |
| 7   | Back        | Back   | Punto de conexión ubicado en la parte trasera del MatchingGyro.              |
| 8   | Front       | Front  | Punto de conexión ubicado en la parte delantera del MatchingGyro.            |


> Notas:

>> Los nombres técnicos utilizados son: `HandleMount`, `Right`, `Top`, `Back` y `Front`.
>> El ID 1 corresponde al mango donde se monta el MatchingGyro.

### 34. Uzi

Cantidad de IDs encontrados: 1

| ID  | Nombre   | Lado    | Descripción                                 |
| --- | -------- | ------- | ------------------------------------------- |
| 1   | MagInput | Unknown | Punto donde se conecta el cargador (`Mag`). |

> Notas:

>> La `Uzi` utiliza un único punto de conexión para el cargador.
>> El objeto `Mag` se conecta al ID 1 de la `Uzi`.
>> No se han identificado otros puntos de conexión propios.

### 35. Briefcase

Cantidad de IDs encontrados: 4

| ID  | Nombre | Lado   | Descripción                                                 |
| --- | ------ | ------ | ----------------------------------------------------------- |
| 1   | Front  | Front  | Punto de conexión ubicado en la parte frontal del maletín.  |
| 2   | Center | Center | Punto de conexión ubicado en el centro del maletín.         |
| 3   | Left   | Left   | Punto de conexión ubicado en el lado izquierdo del maletín. |
| 4   | Right  | Right  | Punto de conexión ubicado en el lado derecho del maletín.   |

> Notas:

>> `Briefcase` posee cuatro puntos de conexión distribuidos alrededor del objeto.
>> El ID 2 corresponde al punto central, mientras que los demás representan las caras frontal, izquierda y derecha.

### 36. FuelTank

Cantidad de IDs encontrados: 1

| ID  | Nombre     | Lado    | Descripción                                             |
| --- | ---------- | ------- | ------------------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión del tanque de fluido con otro objeto. |

> Notas:

>> `FuelTank` posee un único punto de conexión propio.
>> Se utiliza para montar el tanque sobre otro objeto.

### 37. EntitySensor

Cantidad de IDs encontrados: 6

| ID  | Nombre      | Lado        | Descripción                                                         |
| --- | ----------- | ----------- | ------------------------------------------------------------------- |
| 1   | BackLeft    | Back Left   | Punto de conexión ubicado en la parte trasera izquierda del sensor. |
| 2   | BackRight   | Back Right  | Punto de conexión ubicado en la parte trasera derecha del sensor.   |
| 3   | BackCenter  | Back        | Punto de conexión ubicado en la parte trasera central del sensor.   |
| 4   | FrontCenter | Front       | Punto de conexión ubicado en la parte frontal central del sensor.   |
| 5   | FrontRight  | Front Right | Punto de conexión ubicado en la parte frontal derecha del sensor.   |
| 6   | FrontLeft   | Front Left  | Punto de conexión ubicado en la parte frontal izquierda del sensor. |

> Notas:

>> `EntitySensor` posee seis puntos de conexión distribuidos en dos filas (frontal y trasera).
>> La disposición es simétrica: tres puntos al frente y tres en la parte trasera.

### 38. Looper

Cantidad de IDs encontrados: 4

| ID  | Nombre | Lado  | Descripción                                                |
| --- | ------ | ----- | ---------------------------------------------------------- |
| 2   | Top    | Top   | Punto de conexión ubicado en la parte superior del Looper. |
| 3   | Right  | Right | Punto de conexión ubicado en el lado derecho del Looper.   |
| 4   | Left   | Left  | Punto de conexión ubicado en el lado izquierdo (ruedita).  |
| 5   | Front  | Front | Punto de conexión ubicado en la parte frontal del Looper.  |

> Notas:

>> El `Looper` posee cuatro puntos de conexión distribuidos alrededor del bloque.
>> El lado izquierdo corresponde al lado donde se encuentra la rueda/perilla de ajuste.
>> No hay un punto de conexión en la parte trasera ni en la parte inferior.

### 39. Gate-AND

Cantidad de IDs encontrados: 3

| ID  | Nombre | Lado  | Descripción                                 |
| --- | ------ | ----- | ------------------------------------------- |
| 1   | Output | Front | Punto de salida de la compuerta lógica AND. |
| 2   | InputA | Left  | Primera entrada de la compuerta lógica AND. |
| 3   | InputB | Right | Segunda entrada de la compuerta lógica AND. |

> Notas:

>> `Gate-AND` posee dos entradas (`InputA` e `InputB`) y una salida (`Output`).
>> El punto de salida se encuentra en la parte frontal del bloque.

### 40. Gate-OR

Cantidad de IDs encontrados: 3

| ID  | Nombre | Lado  | Descripción                                |
| --- | ------ | ----- | ------------------------------------------ |
| 1   | Output | Front | Punto de salida de la compuerta lógica OR. |
| 2   | InputA | Left  | Primera entrada de la compuerta lógica OR. |
| 3   | InputB | Right | Segunda entrada de la compuerta lógica OR. |

> Notas:

>> `Gate-OR` posee la misma distribución de puntos de conexión que `Gate-AND`.
>> La única diferencia corresponde a la operación lógica implementada por el bloque.

### 41. Gate-NOT

Cantidad de IDs encontrados: 2

| ID  | Nombre | Lado  | Descripción                                  |
| --- | ------ | ----- | -------------------------------------------- |
| 1   | Output | Right | Punto de salida de la compuerta lógica NOT.  |
| 2   | Input  | Left  | Punto de entrada de la compuerta lógica NOT. |

### 42. Wire

Cantidad de IDs encontrados: 2

| ID  | Nombre | Lado  | Descripción                                     |
| --- | ------ | ----- | ----------------------------------------------- |
| 2   | Left   | Left  | Punto de conexión ubicado en el lado izquierdo. |
| 4   | Right  | Right | Punto de conexión ubicado en el lado derecho.   |

> Notas:

>> `Wire` posee dos puntos de conexión, uno en cada extremo del bloque.
>> El ID 2 corresponde al extremo izquierdo y el ID 4 al extremo derecho.

### 43. Body

Cantidad de IDs encontrados: 5

| ID  | Nombre    | Lado         | Descripción                               |
| --- | --------- | ------------ | ----------------------------------------- |
| 1   | Arm_Right | Right        | Punto de conexión del brazo derecho.      |
| 2   | Arm_Left  | Left         | Punto de conexión del brazo izquierdo.    |
| 3   | Head      | Top          | Punto de conexión de la cabeza.           |
| 4   | Leg_Right | Bottom Right | Punto de conexión de la pierna derecha.   |
| 5   | Leg_Left  | Bottom Left  | Punto de conexión de la pierna izquierda. |

> Notas:

>> `Body` posee cinco puntos de conexión correspondientes a las extremidades y la cabeza.
>> Los IDs 1 y 2 corresponden a los brazos derecho e izquierdo respectivamente.
>> El ID 3 corresponde a la cabeza.
>> Los IDs 4 y 5 corresponden a las piernas derecha e izquierda respectivamente.
>> `Body` NO se puede cargar mediante el menu de Spawn, puede ser internamente con:
```json
[["Body", [], []]]
```
>>> o formato Base64:
`W1siQm9keSIsIFtdLCBbXV1d`

### 44. YibYib

Cantidad de IDs encontrados: 1

| ID  | Nombre | Lado | Descripción                                       |
| --- | ------ | ---- | ------------------------------------------------- |
| 2   | Hands  | Top  | Punto de conexión donde el YibYib agarra objetos. |
---

## Objetos sin puntos de conexión propios
> **Hecho por:** @JuanCrakYT
Los siguientes objetos no poseen IDs de puntos de conexión propios.
Estos objetos utilizan puntos de conexión definidos por otros objetos.

1. Seat
2. PotatoEngine
3. GoldPotatoEngine
4. Radio
5. BrakeLight
6. Light
7. SteeringWheel
8. Gyro
9. GasCap
10. FishBowl
11. SpringJuice
12. Balloon
13. Pie
14. Joint
15. Thruster
16. RockingChair
17. Rope
18. RubberBand
19. Sledge
20. SteeringGyro
21. Siren
22. Note
23. Sprite
24. HulaDoll
25. Toilet
26. Tooth
27. Jug
28. Lock
29. Poop
30. Wad
> El objeto `Wad` presenta un comportamiento diferente.
- Puede cargarse correctamente en una build.
- No puede guardarse mediante el sistema normal de guardado.
- No posee IDs de puntos de conexión propios conocidos.
- No puede colocarse en puntos de conexión definidos por otros objetos
- Su aparición en el formato puede depender de estados internos del juego.
31. Recorder
32. Canister
33. CannonBall
34. Gramby
35. DoorA
36. DoorB
37. DoorC
38. DoorD
39. TV
> El objeto `TV` presenta un comportamiento diferente.
- Puede cargarse correctamente en una build.
- No puede guardarse mediante el sistema normal de guardado.
- No posee IDs de puntos de conexión propios conocidos.
- No puede colocarse en puntos de conexión definidos por otros objetos
- Su aparición en el formato puede depender de estados internos del juego.

40.   Camera
41.   Carrot
42.   Guitar
> El objeto `Guitar` presenta un comportamiento diferente.
- Puede cargarse correctamente en una build.
- No puede guardarse mediante el sistema normal de guardado.
- No posee IDs de puntos de conexión propios conocidos.
- No puede colocarse en puntos de conexión definidos por otros objetos
- Su aparición en el formato puede depender de estados internos del juego.
  
43.   MountedGun
44.   Plunger
45.   Joust
46.   SprayPaint
47.   Trowl
48.   Trumpet
49.   Banjo
50.   Drums
51.   Grenade
52.   Mag
53.   Leafblower
54.   RiotShield
55.   ToolGun
> El objeto `RiotShield` presenta un comportamiento diferente.
- Puede cargarse correctamente en una build.
- No puede guardarse mediante el sistema normal de guardado.
- No puede colocarse en puntos de conexión definidos por otros objetos
- No posee IDs de puntos de conexión propios conocidos.
- Su aparición en el formato puede depender de estados internos del juego.
56.    Keyboard
> El objeto `Keyboard` presenta un comportamiento diferente.
- Puede cargarse correctamente en una build.
- No puede guardarse mediante el sistema normal de guardado.
- No puede colocarse en puntos de conexión definidos por otros objetos
- No posee IDs de puntos de conexión propios conocidos.
- Su aparición en el formato puede depender de estados internos del juego.
57.    Head
> El objeto `Head` presenta un comportamiento diferente.
- Puede cargarse mediante una build. 
- No aparece en el panel normal de spawn.
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
58.    PolaroidCamera
> El objeto `PolaroidCamera` presenta un comportamiento diferente.
- Puede cargarse mediante una build.
- No aparece en el panel normal de spawn.
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
59.    PolaroidPhoto
> El objeto `PolaroidPhoto` presenta un comportamiento diferente.
- Puede cargarse mediante una build.
- No aparece en el panel normal de spawn.
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
60.    Fricklet
> El objeto `Fricklet` presenta un comportamiento diferente.
- Puede cargarse mediante una build.
- No aparece en el panel normal de spawn.
- No puede colocarse en puntos de conexión definidos por otros objetos
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
61.    SuperPowerClock
> El objeto `SuperPowerClock` presenta un comportamiento diferente.
- Puede cargarse mediante una build.
- No puede guardarse mediante el sistema normal de guardado.
- No aparece en el panel normal de spawn.
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
62.    Successor
> El objeto `Successor` presenta un comportamiento diferente.
- Puede cargarse mediante una build.
- No aparece en el panel normal de spawn.
- Debe cargarse internamente mediante el formato de build.
- No posee IDs de puntos de conexión propios.
