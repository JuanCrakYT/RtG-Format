# Documentation Standards

These standards apply to maintained documentation outside `old-files/`. They are intended to make the repository easier to navigate, review, and maintain as research evolves.

## Document structure

Use this order when it fits the document's purpose:

1. A single descriptive H1 title.
2. A short purpose statement.
3. Scope, status, or prerequisites where useful.
4. Main content in a predictable H2/H3 hierarchy.
5. Examples and supporting evidence.
6. Limitations, open questions, and related links.

Not every page needs every section. Avoid boilerplate that adds no information.

## Technical accuracy

- Separate direct observations from interpretation.
- Use the repository's established confidence labels consistently.
- Identify whether code/data is an observed sample, a reduced reproduction, or a synthetic illustration.
- Link to experiments or source material when available.
- Record conflicting observations instead of hiding them.
- Do not copy an unverified hypothesis into the consolidated specification as a fact.

## Examples and code

- Use fenced code blocks with a language identifier, such as ```json or ```python.
- Keep examples minimal enough to explain one concept.
- State when an example is illustrative and not a literal game-generated sample.
- Do not include secrets, personal data, or unrelated save contents.
- Keep examples synchronized with the behavior documented by the relevant tool or specification.

## Links and navigation

- Prefer relative links for files within this repository.
- Use descriptive link text instead of phrases such as “click here”.
- Check links after moving or renaming a file.
- Link to the canonical reference rather than duplicating a long technical explanation.
- Keep the root README focused on orientation and entry points.

## Naming and terminology

- Preserve established paths where changing them would break consumers or external references.
- For new general documentation, prefer lowercase names with hyphens.
- Use consistent names for the same field or concept throughout the maintained documentation.
- Explain specialized terms at first use when they are not obvious to the intended audience.

## Review checklist

Before merging a documentation change:

- [ ] Claims are supported by evidence or explicitly marked uncertain.
- [ ] Related specification and reference pages agree.
- [ ] Internal links and code examples have been checked.
- [ ] The change does not duplicate an existing canonical explanation.
- [ ] Any generated content is identified and handled through its documented process.
- [ ] `old-files/` is unchanged.


## Standard templates

Use the matching starter document when creating a new page:

- [Reference or schema page](templates/reference.md)
- [Research note](templates/research-note.md)
- [Experiment or example](templates/experiment.md)
- [Tool or component guide](templates/tool-guide.md)

Templates are starting points, not mandatory boilerplate. Remove sections that do not apply and never fill gaps with invented technical claims.

## Markdown style contract

- Use a single descriptive H1 title, followed by H2 sections and H3 subsections.
- Prefer ATX headings (for example, `## Structure`) over underline-style headings.
- Add blank lines around headings and between separate paragraphs, lists, and tables.
- Use language-tagged fenced code blocks where the language is known.
- Keep source language for translated CLI help; do not translate identifiers, command flags, file paths, or serialized keys.
- Preserve meaningful Markdown hard breaks and code-block whitespace.
- End the file with a newline.
- Check relative links after moving or renaming any document.
- Do not edit, move, rename, or reformat `old-files/`; do not normalize third-party files in dependency directories.
