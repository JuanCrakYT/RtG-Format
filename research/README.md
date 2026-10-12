# Research

This directory records the process and results of reverse-engineering the RtG save/build format. It is intended to answer three separate questions: **how was it investigated, what is supported by evidence, and what remains unresolved?**

## Documents

| Document | Purpose |
| --- | --- |
| [`methodology.md`](methodology.md) | Experimental design, variable isolation, evidence recording, and evaluation |
| [`discoveries.md`](discoveries.md) | Findings supported by the observations described in the research |
| [`unknowns.md`](unknowns.md) | Open questions, partially understood behavior, and hypotheses still needing tests |

## Recommended workflow

1. State a specific question and the behavior that would distinguish possible explanations.
2. Create a minimal test build and preserve the original sample.
3. Change one relevant variable at a time.
4. Compare the resulting data and record the exact observed differences.
5. Repeat the experiment or test additional cases.
6. State the conclusion, confidence level, limitations, and reproduction steps.
7. Update the consolidated [specification](../SPECIFICATION.md) and relevant [format reference](../format/README.md) only when the evidence supports doing so.

## Evidence discipline

- Distinguish direct observations from interpretations.
- Do not describe an untested explanation as confirmed behavior.
- Preserve contradictory results and explain what remains uncertain.
- Link experiments or sample files when available.
- Keep historical material under [`old-files/`](../old-files/) unchanged.

Research is not complete merely because an explanation is plausible. The goal is a traceable, reproducible account of what the available evidence supports.
