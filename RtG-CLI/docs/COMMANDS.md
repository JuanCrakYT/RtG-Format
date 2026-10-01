# RtG-CLI Commands Reference

## Internal Commands

These commands are built into RtG-CLI and always available.

### `help` / `-h` / `--help`

Shows general help or help for a specific command.

```bash
rtg help                    # General help
rtg help <command>          # Help for specific command/addon
rtg help <command> -<lang>  # Help in specific language
rtg help <command> -lang    # List available languages for command
```

**Examples:**
```bash
rtg help
rtg help image
rtg help image -en
rtg help image -lang
```

### `version` / `-v` / `--version`

Shows RtG-CLI version and version content in all available languages.

```bash
rtg -v
rtg --version
```

### `rules` / `-r` / `--rules`

Shows RtG-CLI rules. Uses the first language defined in `rules` (Spanish by default).

```bash
rtg -r
rtg --rules
rtg -r -<lang>   # Rules in specific language
```

**Examples:**
```bash
rtg -r
rtg --rules -en
```

### `lang` / `-l` / `--lang`

Lists all available languages for RtG-CLI organized by category.

```bash
rtg -l
rtg --lang
```

Output categories:
- Version (version-content)
- Rules
- Help
- Void (startup text)
- Addons (per addon)

### `commands` / `-c` / `--commands`

Lists exclusively RtG-CLI internal commands with descriptions.

```bash
rtg -c
rtg --commands
```

**Output:**
```
RtG-CLI internal commands:
  help        | Muestra la ayuda general o la ayuda de un comando específico.
  -h          | Muestra la ayuda general (versión corta).
  --help      | Muestra la ayuda general (versión larga).
  -v          | Muestra la versión de RtG-CLI (versión corta).
  --version   | Muestra la versión de RtG-CLI con contenido multiidioma.
  -r          | Muestra las reglas de RtG-CLI (versión corta).
  --rules     | Muestra las reglas de RtG-CLI.
  -l          | Lista los idiomas disponibles en RtG-CLI (versión corta).
  --lang      | Lista los idiomas disponibles en RtG-CLI.
  -language   | Selecciona el idioma del texto de inicio (void).
  -c          | Lista los comandos internos de RtG-CLI (versión corta).
  --commands  | Lista los comandos internos de RtG-CLI.
  -a          | Lista los addons con documentación disponible (versión corta).
  --addons    | Lista los addons con documentación disponible.
  -u          | Muestra la información de uso común del sistema (versión corta).
  --usage     | Muestra la información de uso común del sistema.
```

### `addons` / `-a` / `--addons`

Lists addons that have user-visible documentation/help available.

```bash
rtg -a
rtg --addons
```

**Output:**
```
Available addons (with documentation):
  image      |  RtG Image
  preview    |  RtG Preview
  test-addon |  RtG Test Addon
```

### `usage` / `-u` / `--usage`

Shows common usage patterns and the most commonly used commands.

```bash
rtg -u
rtg --usage
rtg -u-<lang>   # Usage in specific language (e.g., -u-es, -u-en)
rtg --usage-<lang>  # Usage in specific language (e.g., --usage-es, --usage-en)
```

The language must exist in `void-language` in assets.json.

### `language` / `-language <language>`

Selects the language for the startup (void) text displayed when running `rtg` with no arguments.

```bash
rtg -language en
rtg -language es
```

The language must exist in `void-language` in assets.json.

## Addon Commands

Addons are external programs integrated through the program command interface.

### `image`

Image converter powered by RtG Image.

```bash
rtg image                    # Shows addon info
rtg image <args>             # Passes args to addon program
rtg image -lang              # Shows addon languages
rtg image -<lang>            # Passes language selector to addon
```

### `preview`

Opens HTML preview for RtG-Format builds (RtG Preview).

```bash
rtg preview                  # Shows addon info
rtg preview <args>           # Passes args to addon program
rtg preview -lang            # Shows addon languages
```

### `test-addon`

Test addon for CLI validation.

```bash
rtg test-addon                          # Shows help
rtg test-addon echo <message>           # Prints message to stdout
rtg test-addon fail [message]           # Exits with code 1
rtg test-addon stdout <message>         # Prints to stdout
rtg test-addon stderr <message>         # Prints to stderr
rtg test-addon exit-code <code>         # Exits with specified code (0-255)
rtg test-addon help [command]           # Shows help
rtg test-addon -lang                    # Shows addon languages
```

## Help Command with Usage

The `help` command now supports showing usage information:

```bash
rtg help -u                    # Shows usage (short)
rtg help --usage               # Shows usage
rtg help -u-<lang>             # Shows usage in specific language (e.g., -u-es)
rtg help --usage-<lang>        # Shows usage in specific language (e.g., --usage-es)
rtg help usage                 # Alternative syntax
```

## Argument Ownership Rules

After an addon is identified, argument ownership is determined by prefix:

| Prefix | Owner | Example |
|--------|-------|---------|
| (none) | Addon | `convert`, `file.png` |
| `--`   | Addon | `--width`, `--output` |
| `-`    | RtG-CLI | `-lang`, `-en` |

**Examples:**
```bash
rtg image convert file.png        # convert, file.png → addon
rtg image --width 128             # --width 128 → addon
rtg image -lang                   # -lang → RtG-CLI (shows addon languages)
rtg image -en                     # -en → RtG-CLI (language selector)
```

## Language Selectors

Language selectors use a single hyphen followed by the language code:

```bash
rtg help image -en    # English help
rtg help image -es    # Spanish help
rtg -r -en            # English rules
rtg -language en      # English void text
```

The `-language` option (double hyphen) is only recognized before addon identification and sets the void text language.

## Command Structure Summary

```text
rtg [system-options] [command] [command-options] [arguments]

System options (before command):
  -v, --version       Show version
  -h, --help          Show help
  -l, --lang          List CLI languages
  -r, --rules         Show rules
  -c, --commands      List internal commands
  -a, --addons        List documented addons
  -u, --usage         Show common usage
  -u-<lang>           Show usage in specific language
  --usage-<lang>      Show usage in specific language
  -language <lang>    Set void text language

Commands:
  help [target] [opts]    Help system (supports -u, --usage, -u-<lang>, --usage-<lang>)
  version                 Show version
  rules [opts]            Show rules
  lang                    List languages
  commands                List internal commands
  addons                  List addons
  <addon> [args]          Execute addon
  -language <lang>        Set void language (no command)
```