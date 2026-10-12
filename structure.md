# Repository Architecture

This document defines the responsibility of each maintained repository area. It is a navigation and maintenance guide, not a complete file-by-file inventory: the repository changes more frequently than a manually enumerated tree can remain accurate.

## Top-level layout

| Path | Responsibility | Maintenance guidance |
| --- | --- | --- |
| `README.md` | Public entry point, project status, and navigation | Keep concise; link to canonical detail pages |
| `SPECIFICATION.md` | Consolidated interpretation of the save/build format | Change only when evidence and supporting references justify it |
| `docs/` | Introductory and cross-cutting guides | Prefer links to canonical references over duplicated technical prose |
| `format/` | Detailed format field and structure reference | Keep field names, examples, confidence, and limitations explicit |
| `blocks/` | Block/part identifiers and related reference material | Distinguish observed IDs from inferred meanings |
| `research/` | Methodology, discoveries, and unresolved questions | Preserve reproducibility and contradictory evidence |
| `compression/` | Encoding and compression layer | Separate observed transformations from hypotheses |
| `examples/` | Sample data and experiments | Document source, purpose, and reproduction steps |
| `assets/` | Models, images, and other supporting assets | Keep asset provenance and intended use clear |
| `tools/` | Supporting utilities and research scripts | Document usage, inputs, outputs, and limitations |
| `RtG-CLI/` | Command-line tool | Keep its own README and component-specific docs current |
| `RtG-Preview/` | Browser-based 3D previewer | Document supported input shape and known limitations |
| `RtG Language/` | RtG language implementation and examples | Treat its local specification as component-specific |
| `page/` | Documentation website source | Keep navigation aligned with maintained docs |
| `dev/`, `scripts/` | Development and automation support | Identify generated files and repeatable commands |
| `old-files/` | Historical archive | **Immutable for routine maintenance: do not edit, rename, move, reformat, or delete its contents** |

## Documentation authority

Use this hierarchy to prevent contradictory copies of the same information:

1. **`SPECIFICATION.md`** — consolidated statement of the current documented understanding.
2. **`format/` and related reference directories** — detailed field, identifier, and encoding pages.
3. **`research/` and `examples/`** — evidence, experiments, limitations, and open questions supporting those statements.
4. **`docs/` and `README.md`** — navigation and explanation for readers; these should link to the canonical technical pages instead of maintaining competing specifications.
5. **`old-files/`** — historical material only; useful for provenance, not automatically authoritative for current conclusions.

If sources conflict, do not silently choose one. Record the conflict, link the evidence, and label the current interpretation as unresolved until it is tested.

## File and writing conventions

- Prefer descriptive, stable names in lowercase with hyphens for new general documentation files.
- Preserve established names where renaming would break public links, tooling, scripts, or external references.
- Use one clear title per Markdown document, followed by a predictable heading hierarchy.
- Explain abbreviations on first use when the intended audience may not know them.
- Use fenced code blocks with language identifiers for code and data examples.
- Label examples as illustrative or observed; do not let synthetic examples appear to be extracted game data.
- Use repository-relative links for files inside this repository.
- Do not duplicate long explanations across README files; provide a short summary and link to the canonical page.
- Mark confidence and unresolved behavior explicitly.
- Do not introduce a dependency, generator, workflow, or badge unless its purpose and maintenance cost are understood.

## Safe repository changes

Before moving or deleting a file, search for references in Markdown, code, workflows, website navigation, and external-facing examples. Update every affected link in the same change. Never remove files solely because they look old or redundant without checking their provenance and consumers.

The `old-files/` directory is explicitly excluded from restructuring and cleanup. Its contents must remain byte-for-byte and path-for-path unchanged.
