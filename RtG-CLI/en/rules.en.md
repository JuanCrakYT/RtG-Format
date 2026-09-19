# RtG-CLI Help

RtG-CLI is the intermediary between the user and RtG addons.

## Usage

```text
rtg [options] <command> [<arguments>]
```

The first argument identifies the command or addon that will be used.

Examples:

```text
rtg image

rtg preview

rtg help image
```

## Main Commands

```text
rtg help <command>
```

Displays help for a command or addon.

```text
rtg help <command> -<language>
```

Displays the command's help in a specific language.

```text
rtg help <command> -lang
```

Displays the languages available for that addon.

## System Options

```text
-v, --version    Displays the RtG-CLI version.

-h, --help       Displays the help.

-l, --lang       Queries the languages available for RtG-CLI.

-r, --rules      Displays the RtG-CLI rules.
```

Examples:

```text
rtg --version

rtg -h

rtg --lang

rtg --rules
```

## Languages

Languages are indicated using a single hyphen (`-`).

```text
rtg help image -es

rtg help image -en
```

The selected language does not change the command name.

To query the languages available for an addon:

```text
rtg help image -lang
```

The meaning of `-lang` depends on its position.

Before the addon:

`rtg --lang`

`rtg -l`

queries the languages available for RtG-CLI.

After the addon:

`rtg image -lang`

queries the languages available for the addon.

## Addon Arguments

After an addon has been identified, arguments are separated according to their prefix:

```text
no hyphen      → addon

--argument     → addon

-argument      → RtG-CLI
```

Examples:

```text
rtg image convert

rtg image --width 128

rtg image -lang
```

In:

```text
rtg image --width 128
```

`image` identifies the addon, and `--width 128` is passed to the addon for processing.

In:

```text
rtg image -lang
```

`-lang` belongs to RtG-CLI and queries the languages available for the addon.

## Arguments with Spaces

Arguments containing spaces must be written inside quotes.

Example:

```text
rtg image "my image.png"
```

RtG-CLI preserves addon arguments and passes them in the same order in which they were written.

## Rules

To view the complete rules:

```text
rtg -r

rtg --rules
```

A language can also be specified:

```text
rtg -r -es

rtg --rules -en
```

If no language is specified, the first language defined in `assets.json` will be used.

## More Information

To get help for a specific addon:

```text
rtg help <command>
```

To query its available languages:

```text
rtg help <command> -lang
```
