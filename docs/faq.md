# FAQ

## What is this repository?

This repository documents reverse-engineering research into the Road To Gramby's (RtG) save/build format.
It separates confirmed observations, experiments, historical records, and unresolved questions.

## What is the current source of truth?

Use [`../SPECIFICATION.md`](../SPECIFICATION.md) together with the relevant documents under [`../format/`](../format/) for the current consolidated technical reference.

Historical files under [`../old-files/`](../old-files/) have priority as historical evidence when a discrepancy exists. They must be checked before changing or rejecting the current documentation.

In other words:

```mermaid
flowchart TD
    RtG-Format["RtG Format Repository"] --> OLD
    RtG-Format --> RESEARCH
    RtG-Format --> FORMAT
    RtG-Format --> SPEC

    OLD["📁 old-files/"] --> OLD_DESC["📜 Priority Historical Evidence"]

    RESEARCH --> RESEARCH_DESC["🔬 Verified Discoveries<br/>and Unresolved Questions"]

    FORMAT --> FORMAT_DESC["📘 Organized Technical Documentation"]

    SPEC --> SPEC_DESC["✅ Current Consolidated Presentation"]

    classDef folder fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef description fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef spec fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;
    classDef final fill:#d69e2e,color:#744210,stroke:#975a16,stroke-width:2px;

    class OLD,RESEARCH,FORMAT folder;
    class OLD_DESC,RESEARCH_DESC,FORMAT_DESC description;
    class SPEC spec;
    class SPEC_DESC final;
```

The current documentation organizes and explains the format, while `old-files/` preserves the historical evidence from which it was derived.


## Why are there historical files?

The files under `old-files/` preserve earlier research, observations, and versions of the specification.
They provide evidence for how the format was discovered and documented.

## Where are the Part IDs?

Start with [`../blocks/`](../blocks/).

The historical object ID research is preserved in [`../old-files/obj_ids-spanish.md`](../old-files/obj_ids-spanish.md).

The organized Part reference is [`../blocks/parts/parts-id.md`](../blocks/parts/parts-id.md).

## Where are the experiments?

Reproducible experiments are stored under [`../examples/experiments/`](../examples/experiments/).

Failed or inconclusive experiments should be preserved rather than deleted. See the rules in [`../examples/README.md`](../examples/README.md).

## Can I add an example JSON file?

Yes, but only if the example has real provenance and supporting evidence.
Do not create fabricated saves.

See [`../examples/json-examples/README.md`](../examples/json-examples/README.md).

## Can experiments be deleted?

No.

Experiments are research records and should be preserved, including failed or inconclusive results.
Failed experiments should be moved to [`../examples/trash/`](../examples/trash/) according to the rules for experiments.

## Where is encoding and compression documented?

See [`../compression/`](../compression/).

The main entry point is [`../compression/README.md`](../compression/README.md).

## Where are the tools?

See [`../tools/`](../tools/).
The current tool structure and development status are documented in [`../tools/README.md`](../tools/README.md).

## Is the project affiliated with Road To Gramby's?

No.

This is an independent reverse-engineering project and is not affiliated with or endorsed by the creators of Road To Gramby's or the Road To Gramby's Wiki.
