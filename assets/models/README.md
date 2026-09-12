# RtG Models

This folder contains the Road To Gramby's models used by RtG-Format.

The current model files are stored in the `model` folder:

```tree
assets/models/
├── model/
│   └── Model/
│       ├── Model.obj
│       ├── Model.json
│       └── split/
│           ├── branch.obj
│           └── branch2.obj
└── deprecated/
    └── [deprecated scripts]
```

* `model/` contains the current RtG model assets.
* `deprecated/` contains deprecated scripts and older tools related to model generation.

Each model has its own folder:

```tree
assets/models/model/
└── Model/
    ├── Model.obj
    └── Model.json
```

Models with branches use a `split` folder:

```tree
assets/models/model/
└── Model/
    ├── Model.obj
    ├── Model.json
    └── split/
        ├── branch.obj
        └── branch2.obj
```

---

## Blender Structure

Models must be organized in Blender according to whether they have branches.

### No Branches

A model without branches uses the root MESH itself as the main MESH:

```tree
Model
└── start.Model
```

* `Model`: root object and main MESH of the model.
* `start.Model`: Empty that defines the model's origin.
* The Empty must be inside the main MESH hierarchy.
* There must not be a second MESH named `Model`.
* The root MESH represents the entire model geometry.

---

### With Branches

A model with branches uses the root MESH as the main model and direct MESH children as branches:

```tree
Model
├── branch
│   └── start.Model.branch
└── branch
    ├── start.Model.branch
    └── Point_X
```

* `Model`: root MESH and main MESH of the model.
* Each `branch`: direct child MESH corresponding to a branch.
* Each branch must have exactly one `start.Model.branch` Empty.
* `Point_X` objects belong to the branch within whose hierarchy they are located.
* Child MESH objects without a corresponding `start` are not considered branches.

For example:

```tree
Switch
├── input
│   └── start.Switch.input
└── output
    ├── start.Switch.output
    └── Point_2
```

In this example:

* `Switch` is the main MESH.
* `input` is a branch.
* `output` is another branch.
* `Point_2` belongs to `output`.

---

## `start`

`start.*` objects are **Empty** objects used to define the local origin of models and branches.

They are not part of the geometry and must never appear in `.obj` files.

### Model Without Branches

```text
Model
└── start.Model
```

`start.Model` defines the origin of the main model.

### Model With Branches

```tree
Model
├── branch
│   └── start.Model.branch
└── branch
    └── start.Model.branch
```

Each `start.Model.branch` defines the local origin of its respective branch.

The geometry of a branch is exported relative to its own `start`.

---

## `Point_X`

Connection points use Empty objects with names such as:

```text
Point_1
Point_2
Point_3
...
```

A `Point_X` belongs to the branch within whose hierarchy it is located.

For example:

```tree
Switch
├── input
│   └── start.Switch.input
└── output
    ├── start.Switch.output
    └── Point_2
```

This means that `Point_2` belongs to `output`.

Therefore, the `output` branch is registered in the JSON as:

```json
"Branches": {
    "2": "./split/output.obj"
}
```

A `Point_X` must belong to exactly one branch.

---

## Branches Without `Point_X`

A branch that does not contain any `Point_X` uses:

```json
"NaN": "./split/branch.obj"
```

For example:

```json
"Branches": {
    "NaN": "./split/input.obj",
    "2": "./split/output.obj"
}
```

`NaN` means that the branch is not associated with any `Point_X`.

---

## OBJ Files

The main MESH is always exported as:

```text
./Model.obj
```

Branches are exported inside `split/`:

```text
./split/branch.obj
./split/branch2.obj
```

The main file contains **only the geometry of the main MESH**.

Each file inside `split/` contains **only the geometry of its respective branch**.

For example:

```tree
assets/models/model/Switch/
├── Switch.obj
├── Switch.json
└── split/
    ├── input.obj
    └── output.obj
```

`Switch.obj` contains only the geometry of the `Switch` MESH.

`input.obj` contains only the geometry of the `input` MESH.

`output.obj` contains only the geometry of the `output` MESH.

Empty objects (`start.*` and `Point_X`) are never exported as geometry.

---

## JSON

Each model has a:

```text
Model.json
```

Branch information uses:

```json
"Branches": {
    "NaN": "./split/input.obj",
    "2": "./split/output.obj"
}
```

The positions of branch `start` objects are stored in:

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

The main model uses:

```json
"Default Branch": [
    "./Model.obj"
]
```

`Default Branch` is located at the same level as `Name`, `Tooltip`, `LocalPoints`, and `Branches`.

---

## Deprecated Scripts

Deprecated model-generation scripts are stored separately in:

```text
assets/models/deprecated/
```

These scripts are kept for reference and historical purposes and are not part of the current model asset structure.

Current model assets should be stored exclusively under:

```text
assets/models/model/
```

---

## Rules

1. Current model assets must be stored under `assets/models/model/`.
2. Each model must have its own folder inside `assets/models/model/`.
3. The model folder must have the same name as the model.
4. Deprecated scripts must be stored under `assets/models/deprecated/`.
5. The root MESH must have the same name as the model.
6. The root MESH itself is the main MESH.
7. A model without branches must have exactly one `start.Model`.
8. A model with branches must have exactly one `start.Model.branch` for each branch.
9. Direct child MESH objects of the ROOT are considered branches only if they have exactly one corresponding `start`.
10. Child MESH objects without a corresponding `start` must be ignored.
11. `start.*` names must follow the convention:
    * Without branches: `start.Model`
    * With branches: `start.
