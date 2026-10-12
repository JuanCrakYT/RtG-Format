# Documentation Guide

This directory contains introductory and cross-cutting guides. The canonical technical reference is the root [`SPECIFICATION.md`](../SPECIFICATION.md); this index helps readers choose the right path through the repository.

## Recommended reading paths

- [Getting started](getting-started.md) — choose a beginner, technical, or tooling path.
- [Maintained Markdown inventory](documentation-inventory.md) — browse every maintained Markdown document individually.
- [Documentation taxonomy](documentation-taxonomy.md) — document types, ownership, naming, and migration rules.

### New to RtG-Format

1. [Project overview](../README.md)
2. [Save anatomy](save-anatomy.md)
3. [Building-system concepts](building-system.md)
4. [Current format specification](../SPECIFICATION.md)
5. [Frequently asked questions](faq.md)

### Investigating the format

1. Read the relevant section of the [specification](../SPECIFICATION.md).
2. Check the detailed pages in [`format/`](../format/README.md).
3. Review supporting observations in [`research/`](../research/README.md).
4. Compare reproducible material in [`examples/`](../examples/README.md).
5. Record unresolved questions in the research documentation rather than treating assumptions as facts.

### Working on tools

- [RtG-CLI](../RtG-CLI/README.md) — command-line interface and its component documentation.
- [RtG-Preview](../RtG-Preview/README.md) — browser-based build previewer.
- [RtG Language](../RtG%20Language/README.md) — language implementation and examples.
- [Tools directory](../tools) — utility and research tooling.

## Reference areas

| Area | Purpose |
| --- | --- |
| [Format reference](../format/README.md) | Field-level documentation and structure |
| [Block/part reference](../blocks/README.md) | Identifiers and block-related information |
| [Compression](../compression/README.md) | Encoding and final save representation |
| [Research](../research/README.md) | Methods, findings, and open questions |
| [Examples](../examples/README.md) | Sample data and reproducible experiments |
| [Assets](../assets/README.md) | Models, images, and supporting files |
| [Repository structure](repository-structure.md) | Directory responsibilities and maintenance rules |
| [Documentation standards](documentation-standards.md) | Structure, evidence, examples, and review checklist |
| [Documentation taxonomy](documentation-taxonomy.md) | Document types, ownership, naming, and migration rules |
| [Local link checker](../scripts/check_markdown_links.py) | Repeatable validation of repository-local Markdown links |
| [Maintained Markdown inventory](documentation-inventory.md) | Individually indexed maintained Markdown documents and their roles |
| [Templates](templates/README.md) | Reusable structures for new reference, research, experiment, and tool documents |

## How to read technical claims

Reverse-engineering conclusions can have different levels of certainty. Check the evidence and confidence label attached to a claim, and follow links to the underlying experiment where available. A plausible interpretation is not a confirmed format rule.

Historical material under [`old-files/`](../old-files) is preserved for provenance. It is not part of the maintained documentation workflow and must not be edited as part of ordinary cleanup.
