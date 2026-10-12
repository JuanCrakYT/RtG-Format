# Examples and Experiments

This directory contains example data and experimental material used to inspect, explain, and test the RtG save/build format.

## Directory guide

| Path | Purpose |
| --- | --- |
| [`experiments/`](experiments/) | Controlled tests and reproducible investigations |
| [`json-examples/`](json-examples/) | JSON examples for studying the structured representation |
| [`trash/`](trash/) | Discarded or non-authoritative material retained separately |

Material in `trash/` must not be treated as a current example or authoritative source.

## Requirements for new material

Do not fabricate a save and present it as a real game-generated sample. Examples should have clear provenance and should state whether they are observed data, a reduced reproduction, or an illustrative/synthetic example.

For an experiment, document:

- **Question:** what behavior is being investigated?
- **Setup:** what build, file, or environment was used?
- **Procedure:** what was changed, and how can the test be repeated?
- **Observation:** what changed in the output or in-game behavior?
- **Conclusion:** what does the evidence support?
- **Limitations:** what remains untested or uncertain?

Keep explanations in the relevant README or experiment notes rather than inserting prose into raw data files. Examples illustrate evidence; they do not replace the canonical [specification](../SPECIFICATION.md) or [format reference](../format/README.md).
