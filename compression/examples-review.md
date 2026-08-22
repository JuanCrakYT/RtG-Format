# Compression Experiments Review

This document provides a high-level review of the encoding and compression experiment contained in this directory.

Each entry is intentionally concise. The corresponding example directory contains the complete JSON, input/output data, reproduction steps, observations, and technical evidence.

Do **not** add hypothetical or unverified encoding experiment as factual results.

---

## Experiment structure

Each documented experiment should have its own directory:

```tree
examples/
└── experiments/
    └── <experiment-name>/
        ├── README.md
        ├── objective.md
        ├── input/
        ├── output/
        └── other/
```

The files inside each Experiment contain the detailed evidence. This document only provides the overview.

---

## <ExperimentName>

> One or two sentences explaining what was tested and why the Experiment is relevant to the RtG save/encoding pipeline.

**Experiment:**
`examples/experiments/<experiment-name>/`

### Details

Briefly describe the important result or behavior observed.

Do not reproduce the complete experiment here. Refer the reader to the experiment directory for the full data, decoded JSON, intermediate representations, and reproduction steps.

### Objective

Explain the question this experiment was intended to answer.

### Result

State the final observed result in one or two sentences.

---

## Review criteria

Each experiment should make it possible to determine:

* what input was used;
* what transformation was observed;
* what output was produced;
* whether the result was reproduced successfully;
* what part of the RtG encoding/save pipeline the experiment demonstrates.

If an experiment is incomplete, contradictory, or failed to load, that status must be stated explicitly rather than presenting the experiment as a confirmed format behavior.
