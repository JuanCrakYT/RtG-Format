# Physics Parts — Connection Point IDs

> Source: `old-files/obj_ids-spanish.md`
> Category classification: Road to Gramby's Wiki (used for organization only)
> This document reorganizes historical reverse-engineering data. It does not replace the historical source.

## Anchor

| ID  | Name        | Side         | Description                                                 | Status              | Source / Evidence                           |
| --- | ----------- | ------------ | ----------------------------------------------------------- | ------------------- | ------------------------------------------- |
| 2   | TopLeft     | Top Left     | Punto de conexión ubicado arriba a la izquierda del Anchor. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Anchor table |
| 3   | TopRight    | Top Right    | Punto de conexión ubicado arriba a la derecha del Anchor.   | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Anchor table |
| 4   | BottomLeft  | Bottom Left  | Punto de conexión ubicado abajo a la izquierda del Anchor.  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Anchor table |
| 5   | BottomRight | Bottom Right | Punto de conexión ubicado abajo a la derecha del Anchor.    | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Anchor table |

## BallSocket

| ID  | Name       | Side    | Description                                                    | Status              | Source / Evidence                               |
| --- | ---------- | ------- | -------------------------------------------------------------- | ------------------- | ----------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión de la articulación esférica con otro objeto. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — BallSocket table |

## Bearing

| ID  | Name         | Side   | Description                                                                  | Status              | Source / Evidence                            |
| --- | ------------ | ------ | ---------------------------------------------------------------------------- | ------------------- | -------------------------------------------- |
| 1   | RotationAxis | Center | Punto de conexión utilizado para colocar un spinner en un sistema de ruedas. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Bearing table |

## Propeller

| ID  | Name       | Side    | Description                                     | Status              | Source / Evidence                              |
| --- | ---------- | ------- | ----------------------------------------------- | ------------------- | ---------------------------------------------- |
| 1   | MountPoint | Unknown | Punto de conexión de la hélice con otro objeto. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Propeller table |

## Piston

| ID  | Name      | Side  | Description                                           | Status              | Source / Evidence                           |
| --- | --------- | ----- | ----------------------------------------------------- | ------------------- | ------------------------------------------- |
| 1   | PushEnd   | Front | Punto donde el pistón realiza el empuje o movimiento. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Piston table |
| 3   | Side_Red  | Back  | Punto de conexión del lado rojo del pistón.           | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Piston table |
| 4   | Side_Blue | Front | Punto de conexión del lado azul del pistón.           | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Piston table |

## Servo / Servo_Physics

| ID  | Name         | Side   | Description                                            | Status              | Source / Evidence                          |
| --- | ------------ | ------ | ------------------------------------------------------ | ------------------- | ------------------------------------------ |
| 2   | RotationAxis | Center | Punto del eje de giro del servo.                       | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Servo table |
| 3   | Side_Red     | Left   | Punto lateral del servo identificado por el lado rojo. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Servo table |
| 4   | Side_Blue    | Right  | Punto lateral del servo identificado por el lado azul. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Servo table |

## StaringGyro

| ID  | Name  | Side  | Description                                  | Status              | Source / Evidence                                |
| --- | ----- | ----- | -------------------------------------------- | ------------------- | ------------------------------------------------ |
| 2   | Front | Front | Punto de conexión delantero del StaringGyro. | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — StaringGyro table |
| 3   | Back  | Back  | Punto de conexión trasero del StaringGyro.   | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — StaringGyro table |

## Category index (Physics)

The following items are classified under "Physics" per the Road to Gramby's Wiki. Each row notes whether the historical file includes a detailed table of connection IDs or only a mention.

| Name                            | Historical detail                                      | Status              | Source / Evidence                                  |
| ------------------------------- | ------------------------------------------------------ | ------------------- | -------------------------------------------------- |
| Anchor                          | Detailed table (IDs 2-5)                               | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Anchor table        |
| BallSocket                      | Detailed table (ID 1)                                  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — BallSocket table    |
| Balloon                         | Listed as no own connection points historically        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Cannon                          | Detailed table (ID 1)                                  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Cannon table        |
| Gyro                            | Listed historically as using other points (no own IDs) | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Homemade Pie / Pie              | Listed historically (no own IDs)                       | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Joint                           | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| MatchingGyro                    | Detailed table (multiple IDs)                          | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — MatchingGyro table  |
| Piston                          | Detailed table (IDs 1,3,4)                             | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Piston table        |
| Propeller                       | Detailed table (ID 1)                                  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Propeller table     |
| RockingChair                    | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Rope                            | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| RubberBand                      | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Servo                           | Detailed table (IDs 2,3,4)                             | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Servo table         |
| Servo_Physics (Simulated Servo) | Detailed table (IDs 2,3,4)                             | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Servo_Physics table |
| Sledge                          | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| Spinner                         | Mentioned historically (behavioral)                    | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |
| StaringGyro                     | Detailed table (IDs 2,3)                               | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — StaringGyro table   |
| Wing                            | Detailed table (ID 1)                                  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Wing table          |
| Wheel                           | Detailed table (ID 1)                                  | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — Wheel table         |
| Thruster                        | Listed historically as no own connection points        | PARTIALLY CONFIRMED | old-files/obj_ids-spanish.md — objects list        |

