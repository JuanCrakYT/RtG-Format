# GasCap

Herramienta experimental para generar una representación de **GasCap** compatible con el formato de builds utilizado por RtG.

Esta carpeta contiene un pequeño conversor en Python y sus archivos de salida.

## Estructura

```text
GasCap/
├─ output/
│  ├─ GasCap.json
│  └─ GasCap.txt
├─ main.py
└─ README.md
```

### `main.py`

Script principal de la herramienta.

Se encarga de generar la representación RtG y producir los archivos de salida.

### `output/GasCap.json`

Salida en formato JSON legible.

Contiene la estructura de bloques RtG generada por el conversor.

### `output/GasCap.txt`

Salida codificada en **Base64** a partir de la representación generada.

### `README.md`

Documentación de esta herramienta.

---

## Objetivo

El objetivo de esta herramienta es representar un modelo de `GasCap` utilizando bloques RtG, manteniendo la estructura necesaria para que las conexiones mediante UUID sean válidas.

La estructura conceptual utilizada es:

```text
Part
└─ EphemeralAttachments
   ├─ UUID_A → GasCap
   ├─ UUID_B → GasCap
   └─ UUID_C → GasCap
```

Cada `GasCap` referencia uno de esos UUID mediante una conexión.

Esto es necesario porque los `EphemeralAttachments` pertenecen a un objeto anfitrión. En este caso, `Part` actúa como el objeto que contiene los attachments.

---

## Estructura RtG

La salida sigue la estructura general:

```text
[
    [
        TipoDelBloque,
        Conexiones,
        Propiedades
    ],
    ...
]
```

Para un `GasCap`, la conexión tiene la forma:

```text
[
    TipoLocal,
    UUID,
    IndicePadre
]
```

El UUID utilizado en la conexión debe coincidir exactamente con la clave del `EphemeralAttachments` correspondiente dentro del `Part`.

Por ejemplo:

```json
[
    "GasCap",
    [
        [
            "1",
            "{UUID}",
            1
        ]
    ],
    []
]
```

El `Part` contiene el attachment:

```json
{
    "EphemeralAttachments": {
        "{UUID}": {
            "partName": "Part",
            "cframe": [
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                1,
                0,
                0,
                0,
                1
            ]
        }
    },
    "RGB": [
        0,
        0,
        0
    ]
}
```

El mismo `{UUID}` aparece en ambos lugares.

---

## ¿Por qué existe `Part`?

`GasCap` no se utiliza como contenedor de los `EphemeralAttachments`.

Los UUID necesitan estar asociados a un objeto anfitrión, por lo que la estructura utiliza un `Part` como raíz:

```text
Part
│
├── Attachment UUID 1
│       └── GasCap
│
├── Attachment UUID 2
│       └── GasCap
│
└── Attachment UUID 3
        └── GasCap
```

Esto permite que varios `GasCap` utilicen distintos attachments sin intentar conectar un `GasCap` directamente con otro.

---

## UUID

Los UUID se generan como identificadores opacos.

El mismo UUID debe conservarse en:

1. La clave de `EphemeralAttachments`.
2. La conexión del bloque `GasCap`.

Ejemplo:

```text
{5a54f1d6-0357-4dae-9a1d-f7600d9c2094}
```

No se debe intentar deducir o reproducir un algoritmo interno de generación de UUID del juego.

Para esta herramienta basta con generar UUID válidos y utilizar el mismo valor en todas las referencias correspondientes.

---

## CFrame

Cada `EphemeralAttachment` contiene un `cframe` de 12 valores:

```text
[x, y, z,
 r00, r01, r02,
 r10, r11, r12,
 r20, r21, r22]
```

Los primeros tres valores representan la posición y los nueve restantes representan la matriz de rotación.

Ejemplo de una transformación identidad en el origen:

```json
[
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    1,
    0,
    0,
    0,
    1
]
```

La transformación utilizada debe representar la posición y orientación que corresponda al attachment del `GasCap`.

---

## Sobre el modelo `.obj`

El modelo `.obj` utilizado durante el desarrollo sirve principalmente como **referencia visual / vista previa**.

No se considera que la geometría arbitraria del OBJ pueda convertirse directamente en bloques RtG.

En particular, esta herramienta **no voxeliza**, triangula ni intenta aproximar polígonos arbitrarios utilizando bloques.

La estrategia utilizada es la de representar unidades discretas que ya correspondan a instancias que puedan expresarse mediante bloques RtG.

Por lo tanto:

```text
OBJ
 │
 ├─ instancia 1 → UUID 1 → GasCap
 ├─ instancia 2 → UUID 2 → GasCap
 └─ instancia N → UUID N → GasCap
```

y no:

```text
OBJ
 │
 └─ polígonos
      └─ voxelización
           └─ miles de bloques
```

La segunda estrategia no es apropiada para este formato.

---

## Relación con RtG-Format y RtG-AI

Esta herramienta utiliza como referencia la información disponible en:

- **RtG-Format** — definición, documentación y modelos del formato.
- **RtG-AI** — implementación/proyecto más reciente relacionado con la interpretación y generación de datos RtG.

Cuando exista una diferencia entre documentación histórica y el comportamiento más reciente de RtG-AI, se debe comprobar primero la implementación actual antes de asumir que una regla histórica sigue siendo válida.

No se deben inventar propiedades, conexiones o tipos locales que no estén respaldados por el formato.

---

## Salida

La herramienta genera:

```text
output/
├─ GasCap.json
└─ GasCap.txt
```

### JSON

`GasCap.json` contiene la representación estructurada.

Ejemplo conceptual:

```json
[
    [
        "Part",
        [],
        {
            "EphemeralAttachments": {
                "{UUID}": {
                    "partName": "Part",
                    "cframe": [
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        0,
                        0,
                        1
                    ]
                }
            },
            "RGB": [
                0,
                0,
                0
            ]
        }
    ],
    [
        "GasCap",
        [
            [
                "1",
                "{UUID}",
                1
            ]
        ],
        []
    ]
]
```

Los UUID mostrados son únicamente ilustrativos.

---

## Base64

`GasCap.txt` contiene la representación de salida codificada en Base64.

La finalidad de este archivo es disponer de una representación textual compacta que pueda ser utilizada por herramientas que trabajen con datos RtG codificados.

El JSON y el Base64 deben representar exactamente los mismos datos.

```text
GasCap.json
     │
     │ UTF-8
     ▼
 JSON
     │
     │ Base64
     ▼
GasCap.txt
```

---

## Uso

Ejecutar:

```powershell
python main.py
```

La herramienta genera o actualiza los archivos dentro de:

```text
output/
```

Si `main.py` admite un archivo de entrada mediante argumentos, la ruta deberá apuntar al recurso que la herramienta utilice como fuente de instancias.

```powershell
python main.py --input "ruta/al/archivo.obj"
```

---

## Principios del conversor

Esta herramienta sigue estas reglas:

- `Part` funciona como host de los `EphemeralAttachments`.
- Cada attachment tiene un UUID único.
- El UUID de un attachment y el UUID utilizado por su conexión deben ser idénticos.
- `GasCap` referencia al attachment mediante una conexión.
- No se conectan `GasCap` entre sí mediante puntos que no existan.
- No se generan bloques a partir de polígonos arbitrarios.
- No se realiza voxelización del modelo.
- No se intenta reconstruir un algoritmo interno de generación de UUID.
- El `.obj` de referencia no determina por sí mismo la estructura RtG.
- La implementación actual debe prevalecer sobre suposiciones basadas únicamente en documentación histórica.
- Las propiedades o conexiones no documentadas no deben inventarse.

---

## Estado

Esta herramienta es experimental y forma parte de los `tools` utilizados durante el desarrollo de RtG-AI/RtG-Format.

La estructura puede cambiar conforme se compruebe el comportamiento real del formato y de RtG-AI.