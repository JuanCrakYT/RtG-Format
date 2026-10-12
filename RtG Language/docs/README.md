# RtG-Language Documentation Index

This directory contains the detailed language and implementation notes for RtG-Language. The root [README](../README.md) describes the project's goals and overall status; use these pages for topic-specific details.

## Documents

| Document                          | Scope                                        |
| --------------------------------- | -------------------------------------------- |
| [Language overview](LANGUAGE.md)  | Language goals, concepts, and overall model  |
| [Syntax](SYNTAX.md)               | Source-level syntax conventions              |
| [Grammar](GRAMMAR.md)             | Formal grammar and production rules          |
| [Compiler](COMPILER.md)           | Compilation stages and output generation     |
| [Cache](CACHE.md)                 | Cache design and related behavior            |
| [VS Code integration](VS-CODE.md) | Editor integration and its intended behavior |

## Reading and maintenance rules

- Treat the root language README and implementation as the context for these notes; do not infer implemented behavior from a design goal alone.
- Keep grammar, syntax, and compiler descriptions aligned when language rules change.
- Mark planned behavior as planned until code or tests demonstrate it.
- Preserve existing filenames and links unless every reference is updated in the same change.
- Use examples that match the current implementation; label illustrative syntax when it is not yet executable.
