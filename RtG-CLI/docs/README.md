# RtG-CLI Component Documentation

This directory documents the CLI's architecture and command surface. For installation, quick-start usage, and the overall component map, start with the [RtG-CLI README](../README.md).

## Documents

| Document | Purpose |
| --- | --- |
| [Architecture](ARCHITECTURE.md) | Component responsibilities and internal organization |
| [Commands](COMMANDS.md) | Command catalog, arguments, and behavior |

## Maintenance rules

- Keep command names, flags, examples, and implementation behavior synchronized.
- Distinguish commands that are implemented from planned or illustrative commands.
- Link to localized help text in the languages directory rather than duplicating translated output.
- Update this index when adding, removing, or renaming a document.
