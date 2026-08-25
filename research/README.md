# Research

This folder contains the research documentation produced during the reverse-engineering of the RtG save format.

The documents here focus on **how the format was investigated, what has been discovered, and what is still unknown**.

Research is based primarily on reproducible experiments using real RtG saves.

---

## Documents

### [`discoveries.md`](discoveries.md)

Records the major discoveries made during the reverse-engineering process.
It contains conclusions that are supported by experimental evidence, while avoiding implementation details that have not been confirmed.

Use this file to see **what has been discovered**.

---

### [`unknowns.md`](unknowns.md)

Records questions and behaviors that are still unknown, partially understood, or under investigation.
A subject should remain here until sufficient evidence exists to document it confidently elsewhere.

Use this file to see **what is still unknown**.

---

### [`methodology.md`](methodology.md)

Documents the methodology used to perform the reverse-engineering experiments.
It explains how experiments should be designed, how evidence should be recorded, how variables should be isolated, and how conclusions should be evaluated.

Use this file to see **how discoveries are made and verified**.

---

## Research Workflow

The research process can be summarized as:

```mermaid
flowchart TD

    QUESTION["❓ Question"] --> MINIMAL["🧪 Minimal Test Build"]
    MINIMAL --> ORIGINAL["💾 Original Save"]
    ORIGINAL --> MODIFICATION["🔧 Controlled Modification"]
    MODIFICATION --> DIFF["🔍 Raw JSON Diff"]
    DIFF --> LOAD["🎮 Load in RtG"]
    LOAD --> OBSERVE["👁️ Observe Behavior"]
    OBSERVE --> REPEAT["🔁 Repeat / Verify"]
    REPEAT --> CONCLUSION["📋 Conclusion"]

    CONCLUSION --> DECISION{"🔬 Evidence Sufficient?"}

    DECISION -->|"Yes"| CONFIRMED["✅ Confirmed Discovery"]
    CONFIRMED --> DISCOVERIES["📚 discoveries.md"]

    DECISION -->|"No"| UNRESOLVED["❓ Still Unresolved"]
    UNRESOLVED --> UNKNOWNS["❔ unknowns.md"]

    classDef question fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef experiment fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:2px;
    classDef evidence fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef load fill:#38a169,color:#fff,stroke:#276749,stroke-width:2px;
    classDef observation fill:#319795,color:#fff,stroke:#285e61,stroke-width:2px;
    classDef conclusion fill:#d69e2e,color:#744210,stroke:#975a16,stroke-width:2px;
    classDef decision fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef confirmed fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;
    classDef unresolved fill:#e53e3e,color:#fff,stroke:#9b2c2c,stroke-width:3px;
    classDef docs fill:#edf2f7,color:#1a202c,stroke:#a0aec0,stroke-width:2px;

    class QUESTION question;
    class MINIMAL,MODIFICATION experiment;
    class ORIGINAL,DIFF evidence;
    class LOAD load;
    class OBSERVE,REPEAT observation;
    class CONCLUSION conclusion;
    class DECISION decision;
    class CONFIRMED confirmed;
    class UNRESOLVED unresolved;
    class DISCOVERIES,UNKNOWNS docs;
```

The detailed procedure is documented in [`methodology.md`](methodology.md).

---

## Evidence

Research should be based on evidence whenever possible.

Relevant experimental evidence is stored under:

```md
examples/experiments/
```

Historical research is preserved under:

```md
old-files/
```

The historical files are important references, but current documentation should distinguish between:

* historical observations;
* reproducible experimental results;
* confirmed conclusions;
* hypotheses;
* unresolved questions.

---

## Relationship With Other Documentation

The `research/` folder is not intended to replace the technical documentation.

Instead, the project is organized approximately as:

```mermaid
flowchart TD

    RESEARCH["🔬 research/"] --> METHODOLOGY["📋 methodology.md"]
    RESEARCH --> DISCOVERIES["💡 discoveries.md"]
    RESEARCH --> UNKNOWNS["❓ unknowns.md"]

    METHODOLOGY --> EXPERIMENTAL["🧪 Experimental Research"]
    DISCOVERIES --> EXPERIMENTAL
    UNKNOWNS --> EXPERIMENTAL

    EXPERIMENTAL --> FORMAT["📁 format/"]
    FORMAT --> SPEC["📘 SPECIFICATION.md"]

    classDef research fill:#805ad5,color:#fff,stroke:#553c9a,stroke-width:3px;
    classDef researchFile fill:#2b6cb0,color:#fff,stroke:#2c5282,stroke-width:2px;
    classDef experimental fill:#dd6b20,color:#fff,stroke:#9c4221,stroke-width:3px;
    classDef format fill:#319795,color:#fff,stroke:#285e61,stroke-width:2px;
    classDef spec fill:#38a169,color:#fff,stroke:#276749,stroke-width:3px;

    class RESEARCH research;
    class METHODOLOGY,DISCOVERIES,UNKNOWNS researchFile;
    class EXPERIMENTAL experimental;
    class FORMAT format;
    class SPEC spec;
```

### `research/`

Explains the **investigation and evidence**.

### `format/`

Explains the **current understanding of individual parts of the format**.

### `SPECIFICATION.md`

Provides the **consolidated technical specification**.

### `examples/experiments/`

Contains the **actual experimental saves and their results**.

### `old-files/`

Preserves the **historical reverse-engineering record**.

---

## Important Rule

> **Research documents should describe what the evidence supports, not what the format merely appears to mean.**

When new evidence contradicts an existing conclusion, the documentation should be updated rather than forcing the new evidence to fit the old interpretation.
