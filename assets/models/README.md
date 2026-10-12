# RtG Models

This directory contains the model assets and JSON metadata used by RtG-Format and RtG-Preview.

## Directory Structure

```text
assets/models/
├── README.md
├── model/
│   ├── Switch/
│   │   ├── Switch.json
│   │   ├── Switch.obj
│   │   └── split/
│   │       ├── input.obj
│   │       └── output.obj
│   └── Model/
│       ├── Model.json
│       └── Model.obj
└── deprecated/
    └── [deprecated files]
```

- `model/` contains the current model assets.
- Each model has its own directory named after the model.
- `deprecated/` contains obsolete scripts and tools. It is not part of the active model asset structure.
- `.obj` files contain model geometry.
- `.json` files contain model metadata, connection points, branch definitions, and preview settings.
- `split/` contains individual branch geometry files when a model has branches.

## Model Files

Each model directory contains a JSON metadata file and its main OBJ file.

For example:

```text
assets/models/model/Switch/
├── Switch.json
├── Switch.obj
└── split/
    ├── input.obj
    └── output.obj
```

The main OBJ file contains the main model geometry. Each OBJ file inside `split/` contains only the geometry of its corresponding branch.

Models without branches do not need a `split/` directory.

## JSON Structure

Each model JSON file is an array containing a model object.

```json
[
    {
        "RtG-Format": {
            "RtG-Format Data": {
                "Release Date": "",
                "Creator": "JuanCrakYT",
                "Notes": "",
                "Extra Files": []
            },
            "RtG-Preview": {
                "Size": {
                    "default": 1
                }
            },
            "Page": {}
        },
        "Name": "Model",
        "Tooltip": "",
        "LocalPoints": {},
        "Branches": {},
        "Branches Start": {},
        "Default Branch": [
            "./Model.obj"
        ],
        "AssetID": {
            "ID": "",
            "CreatorLink": "",
            "RbxAssetID": ""
        }
    }
]
```

The structure shown above is a template. Model-specific values must be supplied where applicable.

### `RtG-Format`

Contains format-level metadata and data used by related tools.

#### `RtG-Format Data`

| Field | Description |
|---|---|
| `Release Date` | Date associated with the creation of the file. |
| `Creator` | Creator of the file. |
| `Notes` | Additional notes. |
| `Extra Files` | Paths to additional documentation files. |

`Release Date` uses the specified English date format, `dd`.

`Extra Files` is an array of paths to documentation or other supplementary files.

#### `RtG-Preview`

Contains settings used by RtG-Preview.

##### `Size`

`Size` is an object containing the default scale and optional per-file scale overrides.

```json
"Size": {
    "default": 1,
    "./split/output.obj": 1.25
}
```

- `default` defines the default scale for the model and files without an override.
- A file path defines a scale override for that specific OBJ file.
- File paths must correspond to the paths used by the model JSON.
- Scale values must be finite numbers.

The example above assigns a default scale of `1` and a scale of `1.25` to `./split/output.obj`.

#### `Page`

Reserved for page-related data. It is currently an empty object and does not require any fields.

### `Name`

The model's name. It should match the model directory name and the main OBJ filename, excluding the extension.

Example:

```json
"Name": "Switch"
```

### `Tooltip`

A short description of the model.

Example:

```json
"Tooltip": "Activates its output until switched off"
```

### `LocalPoints`

Defines the local connection points used by the model.

Each key identifies a connection point. Its value contains a position and rotation:

```json
"LocalPoints": {
    "2": [
        [0, 0.75, 0],
        [0, 0, 130]
    ]
}
```

The first array contains the position coordinates `[x, y, z]`. The second contains the rotation `[rx, ry, rz]`.

Connection-point identifiers are represented as JSON object keys and are therefore strings.

### `Branches`

Maps local connection identifiers to the relative paths of branch OBJ files.

```json
"Branches": {
    "NaN": "./split/input.obj",
    "2": "./split/output.obj"
}
```

- The key identifies the local connection associated with the branch.
- The value is the branch OBJ path relative to the model JSON.
- `"NaN"` identifies a branch that is not associated with a numbered local connection point.

A branch path must correspond to an existing OBJ file.

### `Branches Start`

Defines the local position and rotation of each branch.

The keys are the same file paths used in `Branches`.

```json
"Branches Start": {
    "./split/input.obj": [
        [0, -0.144053, 0],
        [0, 0, 0]
    ],
    "./split/output.obj": [
        [-0.000911, -0.099412, 0.002375],
        [0, 0, 0]
    ]
}
```

Each value contains:

1. Position: `[x, y, z]`.
2. Rotation: `[rx, ry, rz]`.

The preview must associate a branch's transform with its file path. It must not infer the transform from the branch's name or array order.

### `Default Branch`

Defines the main model OBJ file.

```json
"Default Branch": [
    "./Switch.obj"
]
```

This field belongs at the model object's root level, alongside `Name`, `Tooltip`, `LocalPoints`, `Branches`, and `Branches Start`.

It must not be moved inside `RtG-Format` or `RtG-Preview`.

The first path identifies the main OBJ file used by the current preview loader.

### `AssetID`

Contains Roblox asset identification data.

```json
"AssetID": {
    "ID": "",
    "CreatorLink": "",
    "RbxAssetID": ""
}
```

- `ID`: asset identifier.
- `CreatorLink`: Roblox Creator Store URL.
- `RbxAssetID`: Roblox asset URI.

These fields must be preserved even when a tool does not currently use them.

## File Paths

Model asset paths are relative to the model's JSON file.

For a model named `Switch`:

| Purpose | Path |
|---|---|
| Metadata | `./Switch.json` |
| Main geometry | `./Switch.obj` |
| Input branch | `./split/input.obj` |
| Output branch | `./split/output.obj` |

The directory containing the JSON file is the base directory for these paths.

Tools must not assume that every model has a `split/` directory or that every model contains branches.

## RtG-Preview Compatibility

RtG-Preview must read the model JSON as the authoritative source for model metadata.

It must:

1. Parse the JSON array and use the model object it contains.
2. Read `Name`, `Tooltip`, `LocalPoints`, `Branches`, `Branches Start`, and `Default Branch` from the model object's root level.
3. Read preview settings from `RtG-Format.RtG-Preview`.
4. Read the default scale from `Size.default`.
5. Apply a path-specific `Size` override when one exists.
6. Load the main OBJ from `Default Branch`.
7. Load each branch OBJ from the corresponding `Branches` value.
8. Match each branch with its transform in `Branches Start` using the file path.
9. Preserve metadata such as `RtG-Format Data`, `Page`, and `AssetID`.

The preview must not require Blender, Blender objects, or deprecated scripts to load a model.

## Rules

1. Active model assets belong under `assets/models/model/`.
2. Deprecated scripts and tools belong under `assets/models/deprecated/`.
3. Each model has its own directory named after the model.
4. The model JSON filename must match the model name.
5. `Default Branch` must point to the main OBJ file.
6. `Branches` maps connection identifiers to branch OBJ paths.
7. `Branches Start` uses the same OBJ paths as keys.
8. `LocalPoints` stores connection positions and rotations.
9. `RtG-Format.RtG-Preview.Size.default` defines the default scale.
10. Other `Size` entries may override the scale for individual OBJ paths.
11. Paths in the model JSON are relative to the model directory.
12. Branch geometry must be stored separately from main model geometry.
13. Models without branches do not require a `split/` directory.
14. `AssetID` and other metadata must not be discarded merely because a tool does not use them.
15. The documented JSON structure takes precedence over assumptions made by tools or older files.
16. Blender and deprecated scripts are not part of the current model asset workflow.