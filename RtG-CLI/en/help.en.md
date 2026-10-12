# RtG-CLI Command Rules

## 1. General structure

An RtG-CLI command consists of a main command and, optionally, arguments.
General format:

`rtg <command> [<arguments>]`

The first argument after `rtg` determines which command or addon will be executed.
Examples:

`rtg image`
`rtg preview`
`rtg help image`

---

## 2. Registered commands

Main commands must be registered in the RtG-CLI configuration.
A command is identified by its internal key.

Example:

`image`

The `image` key identifies the corresponding addon, regardless of the name displayed to the user.

Example:

`image` → `RtG Image`
`preview` → `RtG Preview`

The displayed name must not be used as the command identifier.

---

## 3. RtG-CLI commands and addon commands

RtG-CLI and addons may have their own commands and arguments.

Before an addon is identified, commands and arguments belong to RtG-CLI.
After an addon is identified, the prefix determines who each argument belongs to:

- No hyphen (`-`) → belongs to the addon.
- Two hyphens (`--`) → belongs to the addon.
- One hyphen (`-`) → belongs to RtG-CLI.

Example:

`rtg image convert`

- `image` → addon.
- `convert` → addon command.

Example:

`rtg image --width 128`

- `image` → addon.
- `--width` → addon argument.
- `128` → value of the addon argument.

Example:

`rtg image -lang`

- `image` → addon.
- `-lang` → RtG-CLI argument.

---

## 4. System arguments

Before an addon is identified, RtG-CLI uses its own syntax rules.
Long system options use two hyphens:

`rtg --version`
`rtg --help`

System abbreviations use one hyphen:

`rtg -v`
`rtg -h`
`rtg -l`

After an addon is identified, an option beginning with a single hyphen (`-`) belongs to RtG-CLI.

Example:

`rtg image -lang`
`rtg image -en`

---

## 5. Arguments before and after the addon

RtG-CLI arguments may have a different meaning depending on whether they appear before or after an addon has been identified.

Before an addon is identified, arguments belong to RtG-CLI.

For example:

`rtg --lang`

Displays the languages available for RtG-CLI.
After an addon is identified, arguments are interpreted according to the ownership rules established for addons.

For example:

`rtg image -lang`

Queries the languages available for the `image` addon.

In this way, the position of the argument determines its context and prevents global RtG-CLI arguments from being confused with arguments used after an addon has been identified.

---

## 6. Position of system arguments

System arguments must not appear before the command or addon they affect when the argument depends on that command.

Correct example:

`rtg help image -en`

Incorrect example:

`rtg help -en image`

In these two examples, the system command `help` uses this structure, which is why the second example is incorrect:

`help <target> <options>`

The position must clearly determine which command receives the argument.

---

## 7. Addon commands and arguments

Commands are written as individual terminal arguments.
A command must not contain spaces unless it is enclosed in quotes.

The following arguments may be used by the addon according to its own interface.

For example:

`rtg image convert image`

can be interpreted as:

- `image` → addon
- `convert` → addon command
- `image` → command argument

---

## 8. Use of hyphens in addon commands

After an addon has been identified:

- Arguments without a hyphen belong to the addon.
- Arguments with two or more hyphens (`--`) belong to the addon.
- Arguments with a single hyphen (`-`) belong to RtG-CLI.

Examples:

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Addon command interface

The commands specific to an addon are defined by the addon program itself.
RtG-CLI uses the addon configuration to locate its command interface through the `program commands` property.

This property contains the paths to the files that provide the program's command interface.

Example:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI may use this interface to discover or execute the commands available to the addon, but it must not assume or modify the meaning of its internal commands.

An addon may define additional commands that are not directly registered as RtG-CLI commands.

The internal implementation of the program may differ between addons, as long as it provides an interface compatible with the RtG-CLI rules.

---

## 10. Languages

The languages available for an addon are defined through its configuration.

Example:

`lang: ["es", "en"]`

Translated texts are identified using the corresponding language code.

Example:

`content.es`
`content.en`

The language selector used by RtG-CLI must be considered a system argument.

Example:

`rtg help image -en`

---

## 11. Default language

If `-<language>` is not specified, RtG-CLI will use the first language defined in `rules`.
If `-<language>` is specified, RtG-CLI will use that language if it is available.

The first language defined in the `rules` object of `assets.json` is the default language for the rules.

When the user requests the rules without specifying a language, RtG-CLI must use that first language.

For example:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

In this case:

`rtg -r`

and

`rtg --rules`

will display the rules in Spanish because `es` is the first language defined.

To request another language, its corresponding selector must be used:

`rtg -r -en`

The order of the languages inside `rules` only determines which language is the default. It does not change the available languages.

This rule also applies to other language selectors such as:

`rtg help image -es`

---

## 12. Language does not change the command

Changing the language only modifies the text displayed by RtG-CLI.
It does not change the internal command name.

Example:

`rtg help image -es`

and

`rtg help image -en`

still refer to the same command:

`image`

---

## 13. Help

General help is obtained with:

`rtg help`

Help for a specific command is obtained with:

`rtg help <command>`

Help can be requested in a specific language:

`rtg help <command> -<language>`

Example:

`rtg help image -en`

---

## 14. Language query

The languages available for an addon can be queried with:

`rtg help <command> -lang`

Example:

`rtg help image -lang`

This option belongs to RtG-CLI and not to the addon.

---

## 15. Addons must not modify system rules

An addon may define its own commands and arguments, but it cannot redefine the meaning of arguments reserved by RtG-CLI.

For example, an addon must not use `-h` to give a different meaning to system help.
Names reserved by RtG-CLI have priority over addon commands.

Commands and options reserved by RtG-CLI must be explicitly defined by the CLI interface.
An addon cannot redefine the behavior of a reserved option.

---

## 16. Separation between identifier and name

The internal key of an addon is used to identify it.
The addon name is only used as descriptive information or to display it to the user.

Example:

`image` → internal identifier

`RtG Image` → displayed name

It must not be assumed that the displayed name can be used as a command.

---

## 17. Commands must be deterministic

RtG-CLI must be able to determine whether an argument belongs to the system or to the addon without depending on the descriptive name of the program.

The interpretation must be based on the command structure and rules.

Example:

`rtg help image -en`

must always be interpreted in the same way:

`rtg` → CLI

`help` → CLI command

`image` → addon

`-en` → CLI option

---

## 18. Unknown arguments

After identifying an addon, RtG-CLI must determine the ownership of each argument according to its prefix.

* An argument without a hyphen belongs to the addon.
* An argument with two or more hyphens (`--`) belongs to the addon.
* An argument with a single hyphen (`-`) belongs to RtG-CLI.

If RtG-CLI receives an unknown system argument, it must report that the option does not exist.

Addon arguments must be passed to the addon without RtG-CLI attempting to interpret their meaning.

---

## 19. Do not assume unregistered commands

RtG-CLI must not consider a command valid merely because a related folder, file, or program exists.

The command must be defined in the corresponding configuration.

---

## 20. Compatibility

Addons must follow the RtG-CLI syntax rules in order to integrate correctly.
An addon may have a completely different internal implementation, but its command interface must follow the rules established by RtG-CLI.

---

## 21. Priority rule

After an addon has been identified, a single hyphen (`-`) is reserved for RtG-CLI.

An addon cannot use arguments that begin with a single hyphen.
Arguments that begin with two or more hyphens (`--`) or that do not begin with a hyphen belong to the addon.

---

## 22. Addon arguments

Once the addon has been identified, RtG-CLI must not assume the meaning of addon-specific arguments.

Arguments belonging to the addon must be passed to the addon program so that it can process them.

Example:

`rtg image --width 128`

RtG-CLI identifies `image` as the addon.

`--width 128` belongs to the RtG Image interface and must be processed by that addon.

---

## 23. Arguments containing spaces

Arguments containing spaces must be enclosed in quotes so that the terminal treats them as a single argument.

Example:

`rtg image "C:\Users\User\Downloads\my image.png" "C:\Users\User\Downloads\output.json"`

The complete path must be received as a single argument.

---

## 24. Addon arguments must be preserved

RtG-CLI must not modify, remove, or reinterpret arguments intended for the addon, unless an explicit system rule states otherwise.

Arguments must be passed to the addon in the same order in which they were provided by the user.

---

## 25. Complete examples

Addon command:

`rtg image`

Help:

`rtg help image`

Help in English:

`rtg help image -en`

Query languages:

`rtg help image -lang`

CLI version:

`rtg --version`

CLI help:

`rtg --help`

An addon-specific option:

`rtg image --width 128`

An addon-specific option with a value:

`rtg image --output file.json`

A combination:

`rtg image image.png --output output.json`

In this example:

* `image` identifies the addon.
* `image.png` is an addon argument.
* `--output` is an addon option.
* `output.json` is the value of that option.
* None of these arguments should be interpreted as a system option.

## 26. Startup text language

`rtg -language <language>` selects the language of the startup text displayed by RtG-CLI.

The language must exist inside `void-language`.

Example:

`rtg -language en`

displays the text defined in:

`void-language.en`

If `-language` is not specified, RtG-CLI uses `void`.

If the requested language is not available, RtG-CLI must report that the language is not available.
