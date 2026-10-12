# Documentation Taxonomy and Information Architecture

This document defines the role, location, and maintenance rules for each class of Markdown document in RtG-Format. It formalizes the repository's information architecture; it does not change the meaning of the save format or promote an unverified observation to a fact.

## 1. Documentation layers

| Layer | Canonical location | Purpose | Change policy |
| --- | --- | --- | --- |
| Project entry point | `README.md` | Explain the project and route readers to maintained references | Keep concise; link to detailed pages |
| Consolidated specification | `SPECIFICATION.md` | Present the current consolidated interpretation of the format | Require evidence and references for technical claims |
| Cross-cutting guides | `docs/` | Explain concepts, reading paths, repository organization, and contribution conventions | Avoid duplicating detailed reference content |
| Format reference | `format/` | Describe structure, indexing, identifiers, properties, and unknown fields | Keep one canonical page per topic |
| Object/block reference | `blocks/reference/<Identifier>.md` | Document one object's observed identifiers, properties, connections, and evidence | Preserve identifier spelling; distinguish missing data from zero or none |
| Part ID catalog | `blocks/parts/<category>/parts-id.md` | Organize observed point/part IDs by category | Keep source provenance and category scope visible |
| Research synthesis | `research/` | Record methodology, supported findings, and unresolved questions | Preserve uncertainty and contradictory results |
| Experiments and samples | `examples/` | Store source samples, reduced reproductions, and controlled experiments | Record provenance and whether data is observed or illustrative |
| Encoding/compression | `compression/` | Describe transformations between structured data and stored output | Separate encoding, compression, and unknown steps |
| Supporting assets | `assets/` | Index models and other files used by research or tools | Do not infer behavior from an asset's filename alone |
| Component documentation | A component's own directory, e.g. `RtG-CLI/` | Explain that component's installation, usage, architecture, and limits | Keep instructions close to the component they describe |
| Localized documentation | `RtG-CLI/languages/<locale>/` | Maintain locale-specific material | Preserve locale and meaning; do not overwrite translations with English |
| Templates | `docs/templates/` | Provide starting structures for recurring document types | Templates must remain generic and must not assert format facts |
| Historical archive | `old-files/` | Preserve earlier research and documentation as historical evidence | **Immutable: never edit, rename, move, reformat, or delete its contents** |
| Third-party dependencies | `node_modules/` | Vendored/generated dependency material | Not project-authored documentation; exclude from documentation migrations and linting |

## 2. Authority and evidence

The location of a document describes its role, not the truth of every statement in it.

1. `SPECIFICATION.md` is the consolidated maintained interpretation.
2. Topic-specific pages in `format/` and maintained reference directories provide detail and should link to supporting evidence.
3. `research/` and `examples/` record the observations, experiments, and uncertainty that justify or challenge an interpretation.
4. `old-files/` is a historical source archive. It is preserved unchanged; historical claims should be compared with current evidence rather than silently copied or discarded.
5. Tool documentation describes implemented behavior and limitations of that tool. It does not independently prove the game's internal format.

When sources disagree, record the discrepancy and investigate it. Do not resolve a conflict solely by which file is newer, longer, or located higher in the directory tree.

## 3. Naming and placement

- Use descriptive `kebab-case.md` names for general prose pages, such as `save-anatomy.md`.
- Preserve exact game identifiers and established code-facing names in object reference filenames, such as `Servo_Physics.md`, where spelling is part of the identifier.
- Keep component-specific usage instructions beside the component rather than copying them into the root guide.
- Use a directory `README.md` as its index when a directory contains a navigable collection.
- Prefer one canonical page per subject. Other pages should summarize briefly and link to it instead of maintaining duplicate explanations.
- Keep language-specific material inside its locale directory.
- Do not move a file merely to make the tree look uniform. Move it only when its role is clear, then update all relative links, indexes, scripts, and references in the same change.

## 4. Document contracts

Choose the contract that matches the document rather than forcing every page into one template.

### Guide

A guide normally contains a descriptive H1, audience/purpose, prerequisites if needed, ordered steps or concepts, expected outcome, limitations, and related links.

### Technical reference

A reference normally contains a descriptive H1, scope, observed structure or behavior, examples, evidence/provenance, confidence where relevant, limitations, and related references. Omit sections that would contain no useful information.

### Research note or experiment

A research document records the question, setup, controlled variables, procedure, observations, interpretation, confidence, reproduction steps, and open questions as applicable. Distinguish raw observations from explanations.

### Tool documentation

Tool documentation identifies supported platform/runtime, installation, commands or API, inputs/outputs, examples, errors or limitations, and links to the component's implementation or tests when available.

### Index

An index lists only paths that exist and explains why a reader would open each destination. It should not repeat the full contents of the linked pages.

## 5. Shared terminology

Use the following confidence labels consistently when a confidence label is useful:

- **CONFIRMED** — direct evidence or repeatable observations support the claim within the stated scope.
- **PARTIALLY CONFIRMED** — evidence supports part of the claim, but cases or details remain unverified.
- **UNCONFIRMED** — a possible interpretation or observation that has not been adequately verified.
- **HYPOTHESIS** — an explanatory proposal that still needs a discriminating test.

Do not use `none`, `0`, `unknown`, `not inspected`, and `not applicable` interchangeably. Explain the distinction when it affects interpretation.

## 6. Migration protocol

For a document move, rename, split, or merge:

1. Identify the document's role and canonical destination.
2. Search the repository for links and references to the old path.
3. Move or create the destination and preserve the useful content.
4. Update all affected relative links and directory indexes in the same commit.
5. Keep a compatibility pointer when it protects a known entry point and does not create a second source of truth.
6. Check for duplicate pages, orphaned documents, and references into `old-files/`.
7. Confirm that no path under `old-files/` was changed.

Bulk formatting is not a substitute for this per-document classification and link review.
