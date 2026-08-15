# Experiments

Use this file to list reproducible experiments. Template:

## Experiment title
Objective:
Input (raw save or diff):
Procedure:
Observation:
Result:
Confidence:
Follow-up:

Do not publish experiments without including the raw input (or a link to it) used for the test.

## Experiment: Indexing Convention

### Objective
Determine whether RtG resolves parent references in connection tuples using 0-1-based indice (or if behavior differs by context).

### Existing Evidence
- `old-files/RtG_Save_Format_Specification-spanish.md` contains JSON examples with connection indice `1` (example: a `Part` referencing `0`) which suggests 0-based indexing in those samples.
- `format/indexing.md` notes that historical documents sometimes mention 1-based indexing but advises confirmation from raw saves.
- `research/discoveries.md` confirms the third element of connection tuples is a parent index but does not fix the base.

### Input Data
Files added (synthetic test inputs; intended for reproducible in-game testing):
- `examples/experiments/chain/simple_parent.json` — Base + Part where Part references index `1` (matches historical sample).

Contents (human-readable) — simple_parent.json
```json
[
	["Base", [], {}],
	["Part", [["1","5",0]], {"RGB":[255,0,0]}]
]
```

### Controlled Modifications
- Each variant modifies only the numeric index in the connection tuple(s). No other fields are changed.

### Expected result 1-based
- `examples/experiments/chain/simple_parent.json` (with index `1`) → would attach to the first element (`Base`), producing the intended parent-child relation.

### Observations
- Record for each file: whether the build loads, any error messages, whether the child object is visually attached to the intended parent, and any differences in physics or position.

### Results
- Fill after running the tests.

### Conclusion
- Fill after running the tests.

### Confidence
- Aim to reproduce with both `simple_parent` and `chain` variants. If both point to the same convention, confidence increases.

### Reproducibility
- Include the exact raw JSON files used (they are included under `examples/experiments/`) and the sequence of import actions and any in-game logs or screenshots.
