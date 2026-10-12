# RtG Model Assets

This directory contains the model assets consumed by **RtG-Format** and **RtG-Preview**. Model geometry is stored as OBJ files and model metadata is stored as JSON.

Blender is **not part of the current asset workflow**. The OBJ and JSON files are the source of truth; the deprecated directory is retained only for historical tools and scripts.

## Directory layout

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
│   └── ModelName/
│       ├── ModelName.json
│       ├── ModelName.obj
│       └── split/             # Optional; used when the model has branches
│           └── branch.obj
└── deprecated/                # Historical scripts and tools; not used by preview
```

### Folder rules

- Keep active model assets under `assets/models/model/`.
- Give each model its own directory.
- The directory name and JSON filename should match the model name: `ModelName/ModelName.json`.
- Put the main OBJ beside the JSON.
- Put branch OBJ files in the model's `split/` directory.
- Paths stored in JSON are relative to that model's directory and normally begin with `./`.
- Keep retired scripts and tools under `assets/models/deprecated/`; do not treat them as part of the active model format.

## Model JSON format

Each model JSON file is a JSON array containing the model object as its first item:

```json
[
  {
    "RtG-Format": {
      "RtG-Format Data": {
        "Release Date": "",
        "Creator": "CreatorName",
        "Notes": "",
        "Extra Files": []
      },
      "RtG-Preview": {
        "Size": {
          "default": 1,
          "./split/branch.obj": 1
        }
      },
      "Page": {}
    },
    "Name": "ModelName",
    "Tooltip": "Short description",
    "LocalPoints": {},
    "Branches": {},
    "Branches Start": {},
    "Default Branch": ["./ModelName.obj"],
    "AssetID": {
      "ID": "",
      "CreatorLink": "",
      "RbxAssetID": ""
    }
  }
]
```

The example is illustrative: optional metadata can be empty, and models without branches can use empty `LocalPoints`, `Branches`, and `Branches Start` objects. Preserve the structure and field placement used by the actual model JSON.

## Field reference

### `RtG-Format`

Container for RtG-Format-specific metadata.

- **`RtG-Format Data`**: descriptive metadata such as release date, creator, notes, and extra files.
- **`RtG-Preview`**: preview configuration.
- **`Page`**: page-related metadata.

### `RtG-Preview.Size`

A map of scale values used by RtG-Preview.

- **`default`** applies to the main model and is the fallback for branches without a specific value.
- A key matching a branch OBJ path, such as `"./split/output.obj"`, overrides the fallback for that branch.
- A size can be a scalar (uniform scale) or a three-number array `[x, y, z]` (per-axis scale).

Example:

```json
"Size": {
  "default": 1,
  "./split/input.obj": 0.75,
  "./split/output.obj": [1, 1.25, 1]
}
```

### Root-level model fields

These fields belong beside `Name` and `Tooltip`, **not** inside `RtG-Format.RtG-Preview`.

- **`Name`**: model name.
- **`Tooltip`**: short description shown by tools that display model information.
- **`Default Branch`**: main OBJ path, normally represented as an array such as `["./ModelName.obj"]`.
- **`LocalPoints`**: connection-point data keyed by point ID. Each point contains a position vector and a rotation vector.
- **`Branches`**: map from connection-point ID to branch OBJ path.
- **`Branches Start`**: map from branch OBJ path to its local position and rotation, in the form `[[x, y, z], [rx, ry, rz]]`. RtG-Preview interprets the rotation values as degrees.
- **`AssetID`**: optional asset identification metadata, including `ID`, `CreatorLink`, and `RbxAssetID`.

### Branches and connection points

A model with separate branch geometry can define entries like:

```json
"LocalPoints": {
  "2": [[0, 0.75, 0], [0, 0, 130]]
},
"Branches": {
  "NaN": "./split/input.obj",
  "2": "./split/output.obj"
},
"Branches Start": {
  "./split/input.obj": [[0, 0.75, 0], [0, 0, 130]],
  "./split/output.obj": [[0, 0.75, 0], [0, 0, 130]]
}
```

- A numeric-looking key such as `"2"` associates the branch with that local point ID.
- `"NaN"` is used for a branch that is not associated with a numbered local point.
- Each path in `Branches` should refer to an OBJ file that exists in that model's directory.
- Each branch transform is keyed by the exact OBJ path used in `Branches`.

## OBJ asset rules

- The main geometry is stored in `ModelName.obj`.
- Each branch geometry is stored in a separate file under `split/`.
- OBJ paths in the JSON must match the actual filenames and relative directory structure, including letter case.
- The main OBJ should contain the main model geometry; branch OBJ files should contain only their respective branch geometry.
- Do not rely on Blender objects, empties, or export-time scene structure at preview runtime. RtG-Preview reads the exported OBJ geometry and JSON metadata directly.

## RtG-Preview model loading

RtG-Preview resolves a model from its type name and reads its metadata and OBJ files directly from `assets/models/model/<type>/`. There is no generated model index or manifest to maintain.

When adding a model, place its JSON metadata and default OBJ in a matching folder, and keep any branch OBJ files in the paths referenced by that model's JSON. Test the preview over HTTP so browsers can request the JSON and OBJ assets.
