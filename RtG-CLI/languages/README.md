# RtG-CLI Localized Documentation

This directory stores locale-specific Markdown text used by RtG-CLI. Keep each language's files inside its locale directory and preserve the filenames because scripts or loaders may refer to them directly.

## File types

| File pattern        | Purpose                               |
| ------------------- | ------------------------------------- |
| `help.<locale>.md`  | Localized help text                   |
| `rules.<locale>.md` | Localized rules and guidance          |
| `void.<locale>.md`  | Localized startup or empty-state text |

The files are runtime content as well as documentation. When editing them, preserve command names, flags, serialized identifiers, code examples, and required formatting tokens. Do not mechanically translate code-facing values.

## Available locales

| Locale                        | Help                        | Rules                         | Startup text                   |
| ----------------------------- | --------------------------- | ----------------------------- | ------------------------------ |
| Arabic (`ar`)                 | [Help](ar/help.ar.md)       | [Rules](ar/rules.ar.md)       | [Startup](ar/void.ar.md)       |
| Czech (`cs`)                  | [Help](cs/help.cs.md)       | [Rules](cs/rules.cs.md)       | [Startup](cs/void.cs.md)       |
| German (`de`)                 | [Help](de/help.de.md)       | [Rules](de/rules.de.md)       | [Startup](de/void.de.md)       |
| English (`en`)                | [Help](en/help.en.md)       | [Rules](en/rules.en.md)       | [Startup](en/void.en.md)       |
| Spanish (`es`)                | [Help](es/help.es.md)       | [Rules](es/rules.es.md)       | [Startup](es/void.es.md)       |
| French (`fr`)                 | [Help](fr/help.fr.md)       | [Rules](fr/rules.fr.md)       | [Startup](fr/void.fr.md)       |
| Hindi (`hi`)                  | [Help](hi/help.hi.md)       | [Rules](hi/rules.hi.md)       | [Startup](hi/void.hi.md)       |
| Hungarian (`hu`)              | [Help](hu/help.hu.md)       | [Rules](hu/rules.hu.md)       | [Startup](hu/void.hu.md)       |
| Italian (`it`)                | [Help](it/help.it.md)       | [Rules](it/rules.it.md)       | [Startup](it/void.it.md)       |
| Japanese (`ja`)               | [Help](ja/help.ja.md)       | [Rules](ja/rules.ja.md)       | [Startup](ja/void.ja.md)       |
| Korean (`ko`)                 | [Help](ko/help.ko.md)       | [Rules](ko/rules.ko.md)       | [Startup](ko/void.ko.md)       |
| Dutch (`nl`)                  | [Help](nl/help.nl.md)       | [Rules](nl/rules.nl.md)       | [Startup](nl/void.nl.md)       |
| Polish (`pl`)                 | [Help](pl/help.pl.md)       | [Rules](pl/rules.pl.md)       | [Startup](pl/void.pl.md)       |
| Portuguese (`pt`)             | [Help](pt/help.pt.md)       | [Rules](pt/rules.pt.md)       | [Startup](pt/void.pt.md)       |
| Russian (`ru`)                | [Help](ru/help.ru.md)       | [Rules](ru/rules.ru.md)       | [Startup](ru/void.ru.md)       |
| Swedish (`sv`)                | [Help](sv/help.sv.md)       | [Rules](sv/rules.sv.md)       | [Startup](sv/void.sv.md)       |
| Turkish (`tr`)                | [Help](tr/help.tr.md)       | [Rules](tr/rules.tr.md)       | [Startup](tr/void.tr.md)       |
| Traditional Chinese (`zh-TW`) | [Help](zh-TW/help.zh-TW.md) | [Rules](zh-TW/rules.zh-TW.md) | [Startup](zh-TW/void.zh-TW.md) |
| Chinese (`zh`)                | [Help](zh/help.zh.md)       | [Rules](zh/rules.zh.md)       | [Startup](zh/void.zh.md)       |

## Maintenance rules

- Keep all three files together for each locale.
- Match terminology and command behavior to the canonical CLI implementation.
- Preserve the source language of each locale; normalization must not replace translations with English.
- If a locale is incomplete, document the missing content rather than copying another language and presenting it as translated.
- Verify the corresponding CLI command or loader after changing filenames or formatting.
