# RtG Models

Esta carpeta contiene los modelos de Road To Gramby's utilizados por RtG-Format.

Cada modelo tiene su propia carpeta:

```text
assets/models/
└── Model/
    ├── Model.obj
    └── Model.json
```

Los modelos con ramas utilizan una carpeta `split`:

```text
assets/models/
└── Model/
    ├── Model.obj
    ├── Model.json
    └── split/
        ├── branch.obj
        └── branch2.obj
```

---

## Estructura en Blender

Los modelos deben organizarse dentro de Blender de acuerdo con si tienen o no ramas.

### Sin ramas

Un modelo sin ramas debe tener un MESH principal con un Empty `start.Model`:

```text
Model
└── Model
    └── start.Model
```

* `Model` superior: objeto raíz/contenedor.
* `Model` inferior: MESH principal.
* `start.Model`: Empty que define el origen del modelo.
* El Empty debe ser hijo del MESH principal.
* El nombre `start.Model` evita conflictos con otros objetos `start` dentro de Blender.

---

### Con ramas

Un modelo con ramas utiliza un MESH principal y un MESH independiente para cada rama:

```text
Model
├── Model
├── branch
│   └── start.Model.branch
└── branch
    └── start.Model.branch
```

* `Model` superior: objeto raíz/contenedor.
* `Model` inferior: MESH completo del modelo.
* Cada `branch`: MESH correspondiente a una rama.
* Cada rama debe tener exactamente un Empty `start.Model.branch`.
* El nombre identifica tanto al modelo como a la rama.

Por ejemplo:

```text
Switch
├── Switch
├── input
│   └── start.Switch.input
└── output
    ├── start.Switch.output
    └── Point_2
```

---

## `start`

Los objetos `start.*` son **Empty** utilizados como puntos de origen para exportar los modelos.

No son parte de la geometría y nunca deben aparecer en los archivos `.obj`.

### Modelo sin ramas

```text
Model
└── Model
    └── start.Model
```

`start.Model` define el origen del modelo principal.

### Modelo con ramas

```text
Model
├── Model
├── branch
│   └── start.Model.branch
└── branch
    └── start.Model.branch
```

Cada `start.Model.branch` define el origen de su respectiva rama.

La geometría de una rama se exporta relativa a su propio `start`.

---

## `Point_X`

Los puntos de conexión utilizan Empty con nombres:

```text
Point_1
Point_2
Point_3
...
```

El `Point_X` pertenece a la rama dentro de cuya jerarquía se encuentre.

Por ejemplo:

```text
Switch
├── Switch
├── input
│   └── start.Switch.input
└── output
    ├── start.Switch.output
    └── Point_2
```

Esto significa que `Point_2` pertenece a `output`.

Por lo tanto, la rama `output` se registra en el JSON como:

```json
"Branches": {
    "2": "./split/output.obj"
}
```

Un `Point_X` debe pertenecer a una única rama.

---

## Ramas sin `Point_X`

Una rama que no contiene ningún `Point_X` utiliza:

```json
"NaN": "./split/branch.obj"
```

Por ejemplo:

```json
"Branches": {
    "NaN": "./split/input.obj",
    "2": "./split/output.obj"
}
```

`NaN` significa que esa rama no está asociada a ningún punto `Point_X`.

---

## Archivos OBJ

El MESH principal siempre se exporta como:

```text
./Model.obj
```

Las ramas se exportan dentro de `split/`:

```text
./split/branch.obj
./split/branch2.obj
```

El archivo principal contiene el modelo completo.

Los archivos de `split/` contienen las geometrías individuales de las ramas.

Los Empty (`start.*` y `Point_X`) nunca se exportan como geometría.

---

## JSON

Cada modelo tiene un archivo:

```text
Model.json
```

La información de las ramas utiliza:

```json
"Branches": {
    "NaN": "./split/input.obj",
    "2": "./split/output.obj"
}
```

Las posiciones de los `start` de las ramas se almacenan en:

```json
"Branches Start": {
    "./split/input.obj": [
        [x, y, z],
        [rx, ry, rz]
    ],
    "./split/output.obj": [
        [x, y, z],
        [rx, ry, rz]
    ]
}
```

El modelo principal utiliza:

```json
"Default Branch": [
    "./Model.obj"
]
```

`Default Branch` se encuentra al mismo nivel que `Name`, `Tooltip`, `LocalPoints` y `Branches`.

---

## Reglas

1. La carpeta del modelo debe tener el mismo nombre que el modelo.
2. El MESH principal debe tener el mismo nombre que el modelo.
3. Un modelo sin ramas debe tener exactamente un `start.Model`.
4. Un modelo con ramas debe tener exactamente un `start.Model.branch` por cada rama.
5. Los nombres `start.*` deben seguir la convención:
   * Sin ramas: `start.Model`
   * Con ramas: `start.Model.branch`

6. Los puntos de conexión deben llamarse `Point_X`.
7. Un `Point_X` pertenece a la rama dentro de cuya jerarquía se encuentre.
8. Una rama sin `Point_X` utiliza `"NaN"` en `Branches`.
9. Los Empty no se exportan al OBJ.
10. El `start` de una rama representa el origen local de esa rama.
11. El MESH principal representa el modelo completo.
12. Las ramas individuales se almacenan dentro de `split/`.
13. `Default Branch` debe apuntar al OBJ principal.
14. Los datos existentes del JSON que no sean generados por el exportador deben conservarse.
15. Los nombres de los `start` deben ser únicos y descriptivos para evitar conflictos de nombres dentro de Blender.
