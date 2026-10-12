# Contributing to RtG-Format

Thank you for helping improve RtG-Format. Contributions may include format research, documentation, examples, tooling, previewer improvements, and corrections to existing findings.

## Core principles

1. **Evidence before conclusions.** Do not present guesses as observed format behavior.
2. **Reproducibility.** Explain how a result was obtained so another person can check it.
3. **Traceability.** Link claims to a sample, experiment, source file, test, or documented observation whenever possible.
4. **Preservation.** Do not edit, rename, move, reformat, or delete anything inside `old-files/`. It is a historical archive.
5. **Scope discipline.** Avoid unrelated cleanup in a change intended to solve one specific problem.

## Evidence and confidence labels

Use consistent labels when documenting uncertain findings:

- **Confirmed** — supported by repeatable tests or direct evidence.
- **Partially confirmed** — observed, but important cases or details remain unverified.
- **Unconfirmed** — plausible or reported, but not yet supported by enough evidence.
- **Hypothesis** — an explanation proposed for testing, not an established fact.

When a finding changes, explain what new evidence caused the change. Do not silently erase contradictory observations.

## Where changes belong

| Change | Preferred location |
| --- | --- |
| Main format overview and consolidated interpretation | [`SPECIFICATION.md`](SPECIFICATION.md) |
| Specific JSON fields, identifiers, indexing, properties, and unknown fields | [`format/`](format/) |
| Part IDs and categories | [`blocks/parts/`](blocks/parts/) |
| Research procedure and unresolved questions | [`research/`](research/) |
| Reproducible sample builds and experiments | [`examples/`](examples/) |
| Encoding and compressed save representation | [`compression/`](compression/) |
| Tools and utilities | [`tools/`](tools/) |
| Browser-based 3D previewer | [`RtG-Preview/`](RtG-Preview/) |
| RtG command-line tools | [`RtG-CLI/`](RtG-CLI/) |
| RtG language implementation and examples | [`RtG Language/`](RtG%20Language/) |
| Documentation website source | [`page/`](page/) |

Follow the README or contribution notes inside a component directory when they provide more specific instructions.

## Documenting a format finding

For a new or corrected finding, include as many of the following as apply:

- The exact field, value, identifier, or behavior being described.
- The sample or file used, with a repository-relative path.
- The steps needed to reproduce the observation.
- Expected versus observed behavior, including relevant differences between samples.
- The evidence/confidence label.
- Known limitations and unanswered questions.
- Related specification pages that should be updated together.

Do not include private data or unrelated personal information in sample files.

## Code and generated files

- Keep changes focused and consistent with the surrounding component.
- Do not commit generated output, dependency folders, caches, or temporary files unless the component explicitly requires them as tracked assets.
- If a script generates a manifest or other checked-in file, update it using the documented generator where practical and state which files were generated.
- Preserve existing public interfaces unless the change explicitly intends to revise them.

## Pull request checklist

Before opening a pull request:

- [ ] Explain the problem and the intended change.
- [ ] Link evidence for technical claims.
- [ ] Mark uncertain findings with the labels above.
- [ ] Update related documentation and examples where needed.
- [ ] Run relevant tests or validation; report anything that could not be run.
- [ ] Check internal links and repository-relative paths.
- [ ] Confirm that `old-files/` is unchanged.
- [ ] Keep unrelated changes out of the diff.

## Questions and incomplete research

If evidence is insufficient, document the open question in [`research/unknowns.md`](research/unknowns.md) rather than inventing a definitive answer. A well-described unknown is more useful than an unsupported specification.
