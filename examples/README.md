# Examples and Experiments

This directory contains real RtG save examples, experiments, and curated minimal builds used for testing, research, and demonstrations.

## General Rules

- Do NOT create or add fabricated saves or experiments.
- Only include files with real provenance and supporting evidence.
- Keep notes and explanations in `README.md` or the appropriate documentation files, not inside `example.json`.

## Examples

Real save/build examples are stored in `examples/json-examples/`.
Examples are intended for demonstrations, testing, and reference.

### Example structure

Each example must have its own folder:

```tree
<name>/
│
├── README.md
├── example.json
└── images-videos/
    ├── presentation.png
    └── ...
```

* `example.json` must contain only the save/build data.
* Put explanations, observations, and other notes in `README.md`.
* Images and videos related to the example go in `images-videos/`.
* Videos must not be longer than 30 seconds.
* If an example cannot be loaded or is otherwise invalid, its folder may be deleted.

## Experiments

Experiments are stored in `examples/experiments/`.
Experiments are research records and must be preserved, including failed or inconclusive experiments.

### Experiment structure

Each experiment must have its own folder:

```tree
<name>/
│
├── README.md
├── objective.md
├── example.json
├── images-videos/
|   ├── presentation.png
|   └── ...
└── other/
    ├── README.md
    └── ...
```

* `example.json` must contain only the relevant save/build data.
* Put the experiment objective in `objective.md`.
* Put results, observations, reproduction notes, and conclusions in `README.md`.
* Additional evidence or files can be placed in `other/`.
* If an experiment cannot be loaded, fails, or produces unexpected results, document the problem in `README.md`.
* Experiments must NOT be deleted. Move failed or unusable experiments to `examples/trash/` instead.
* Images and videos related to the example go in `images-videos/`.
* Videos must not be longer than 30 seconds.

### Trash

See [`trash/README.md`](trash/README.md) for the rules governing preserved failed experiments.

## Examples vs. Experiments

|          | `json-examples/`        | `experiments/`   |
| -------- | ----------------------- | ---------------- |
| Purpose  | Demonstration/reference | Research         |
| Failed   | May be deleted          | Move to `trash/` |
| Evidence | Required                | Required         |
| Results  | Optional                | Required         |

