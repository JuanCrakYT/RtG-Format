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
Determine whether RtG resolves parent references in connection tuples using 0-based or 1-based indices (or if behavior differs by context).

### Existing Evidence
- `old-files/RtG_Save_Format_Specification-spanish.md` contains JSON examples with connection indices `0` and `1` (example: a `Part` referencing `0`) which suggests 0-based indexing in those samples.
- `format/indexing.md` notes that historical documents sometimes mention 1-based indexing but advises confirmation from raw saves.
- `research/discoveries.md` confirms the third element of connection tuples is a parent index but does not fix the base.

### Test Setup
- Two minimal test scenarios (single-parent and a parent chain). Each scenario has three variants: `original`, `index-minus-one`, `index-plus-one`.
- Place the test JSON files into `examples/experiments/indexing/` and import them into RtG using the game's save/import workflow.
- Record the game's observable behavior (object positions, load success/failure, any error messages such as "Build inválida").

### Input Data
Files added (synthetic test inputs; intended for reproducible in-game testing):
- `examples/experiments/indexing/simple_parent/original.json` — Base + Part where Part references index `0` (matches historical sample).
- `examples/experiments/indexing/simple_parent/index-minus-one.json` — same as original but reference changed to `-1`.
- `examples/experiments/indexing/simple_parent/index-plus-one.json` — same as original but reference changed to `1`.

- `examples/experiments/indexing/chain/original.json` — Base, PartA referencing Base, PartB referencing PartA (indices `0` and `1`).
- `examples/experiments/indexing/chain/index-minus-one.json` — same as chain original but each child index decremented by 1.
- `examples/experiments/indexing/chain/index-plus-one.json` — same as chain original but each child index incremented by 1.

Contents (human-readable) — simple_parent/original.json
```
[
	["Base", [], {}],
	["Part", [["1","5",0]], {"RGB":[255,0,0]}]
]
```

`index-minus-one.json` changes the `0` to `-1`.

`index-plus-one.json` changes the `0` to `1`.

Chain example (human-readable) — chain/original.json
```
[
	["Base", [], {}],
	["Part", [["1","5",0]], {"RGB":[255,0,0]}],
	["Part", [["1","5",1]], {"RGB":[0,255,0]}]
]
```

### Controlled Modifications
- Each variant modifies only the numeric index in the connection tuple(s). No other fields are changed.

### Expected result if 0-based
- `original.json` → objects load and child attaches to the intended parent (e.g., red `Part` attached to `Base`).
- `index-minus-one.json` → invalid/out-of-range reference; expected load error or child disconnected.
- `index-plus-one.json` → reference points to next element (often self or sibling) and should not attach to intended parent; expected different topology or load failure.

### Expected result if 1-based
- `original.json` (with index `0`) → reference out-of-range; expected load failure or child disconnected.
- `index-plus-one.json` (with index `1`) → would attach to the first element (`Base`), producing the intended parent-child relation.
- `index-minus-one.json` → still out-of-range (negative) and invalid.

### Observations
- Record for each file: whether the build loads, any error messages, whether the child object is visually attached to the intended parent, and any differences in physics or position.

### Results
- Fill after running the tests.

### Conclusion
- Fill after running the tests.

### Confidence
- Aim to reproduce with both `simple_parent` and `chain` variants. If both point to the same convention, confidence increases.

### Reproducibility
- Include the exact raw JSON files used (they are included under `examples/experiments/indexing/`) and the sequence of import actions and any in-game logs or screenshots.

