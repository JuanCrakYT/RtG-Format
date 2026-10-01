"""Formal argument parser for RtG-CLI.

Parses command line arguments into structured representation
supporting commands, subcommands, options, positional arguments,
and addon argument separation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .diagnostics import Diagnostic, err_invalid_argument, err_unknown_option, err_usage
from .languages import LanguageManager


class ArgType(Enum):
    """Classification of argument types."""

    COMMAND = "command"
    SUBCOMMAND = "subcommand"
    OPTION = "option"
    POSITIONAL = "positional"
    ADDON_ARG = "addon_arg"
    LANGUAGE_SELECTOR = "language_selector"


@dataclass(frozen=True)
class ParsedArgument:
    """A single parsed argument with its classification."""

    raw: str
    arg_type: ArgType
    name: str | None = None
    value: str | None = None
    is_addon_owned: bool = False


@dataclass
class ParsedCommandLine:
    """Complete parsed command line."""

    cli_options: dict[str, str | bool] = field(default_factory=dict)
    command: str | None = None
    subcommand: str | None = None
    positional_args: list[str] = field(default_factory=list)
    addon_identifier: str | None = None
    addon_args: list[str] = field(default_factory=list)
    language_selector: str | None = None
    raw_args: list[str] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def has_errors(self) -> bool:
        return len(self.diagnostics) > 0

    def get_first_error(self) -> Diagnostic | None:
        return self.diagnostics[0] if self.diagnostics else None


class ArgumentParser:
    """Formal argument parser for RtG-CLI."""

    # System options that belong to RtG-CLI (single hyphen)
    SYSTEM_SHORT_OPTIONS = {
        "v": "version",
        "h": "help",
        "l": "lang",
        "r": "rules",
        "c": "commands",
        "a": "addons",
    }

    # System options that belong to RtG-CLI (double hyphen)
    SYSTEM_LONG_OPTIONS = {
        "version": "version",
        "help": "help",
        "lang": "lang",
        "rules": "rules",
        "commands": "commands",
        "addons": "addons",
        "language": "language",
        "usage": "usage",
    }

    # Options that take a value
    OPTIONS_WITH_VALUE = {
        "language",
    }

    # Options that can have language suffix: -u-es, --usage-es, etc.
    OPTIONS_WITH_LANG_SUFFIX = {
        "u": "usage",
        "usage": "usage",
    }

    def __init__(self, config, language_manager: LanguageManager):
        self.config = config
        self.lang_manager = language_manager
        self.addon_identifiers = set(config.addons.keys())
        self.internal_commands = {"help"} | set(config.internal.command_list)

    def parse(self, argv: list[str]) -> ParsedCommandLine:
        """Parse command line arguments."""
        if not argv:
            return ParsedCommandLine(raw_args=argv)

        result = ParsedCommandLine(raw_args=argv)
        i = 0
        addon_identified = False

        while i < len(argv):
            arg = argv[i]

            # Check for -language <value> (must be before addon identification)
            if arg == "-language" and not addon_identified:
                i += 1
                if i < len(argv):
                    lang = argv[i]
                    diag = self.lang_manager.validate_language(lang, "void")
                    if diag:
                        result.diagnostics.append(diag)
                    else:
                        result.language_selector = lang
                        result.cli_options["language"] = lang
                else:
                    result.diagnostics.append(err_invalid_argument("-language", "requires a value"))
                i += 1
                continue

            # Check for system long options (--option)
            if arg.startswith("--") and not addon_identified:
                opt_name = arg[2:]
                
                # Check for language suffix on long options (e.g., --usage-es)
                lang_suffix = None
                for opt_base, canonical in self.OPTIONS_WITH_LANG_SUFFIX.items():
                    if opt_name.startswith(opt_base + "-"):
                        lang_suffix = opt_name[len(opt_base) + 1:]
                        opt_name = opt_base
                        break
                
                if opt_name in self.SYSTEM_LONG_OPTIONS:
                    canonical = self.SYSTEM_LONG_OPTIONS[opt_name]
                    if canonical in self.OPTIONS_WITH_VALUE:
                        i += 1
                        if i < len(argv):
                            result.cli_options[canonical] = argv[i]
                        else:
                            result.diagnostics.append(err_invalid_argument(arg, "requires a value"))
                    else:
                        result.cli_options[canonical] = True
                    
                    # Handle language suffix
                    if lang_suffix:
                        diag = self.lang_manager.validate_language(lang_suffix, "void")
                        if diag:
                            result.diagnostics.append(diag)
                        else:
                            result.cli_options[f"{canonical}_lang"] = lang_suffix
                else:
                    result.diagnostics.append(err_unknown_option(arg))
                i += 1
                continue

            # Check for system short options (-x) before addon
            if arg.startswith("-") and not arg.startswith("--") and not addon_identified:
                opt_char = arg[1:]
                
                # Check for language suffix on short options (e.g., -u-es)
                lang_suffix = None
                base_opt = opt_char
                if "-" in opt_char:
                    base_opt, lang_suffix = opt_char.split("-", 1)
                
                # Check if it's a single-char system option
                if len(base_opt) == 1 and base_opt in self.SYSTEM_SHORT_OPTIONS:
                    canonical = self.SYSTEM_SHORT_OPTIONS[base_opt]
                    result.cli_options[canonical] = True
                # Check if it's a short option with language suffix (e.g., -u-es)
                elif base_opt in self.OPTIONS_WITH_LANG_SUFFIX:
                    canonical = self.OPTIONS_WITH_LANG_SUFFIX[base_opt]
                    result.cli_options[canonical] = True
                    if lang_suffix:
                        diag = self.lang_manager.validate_language(lang_suffix, "void")
                        if diag:
                            result.diagnostics.append(diag)
                        else:
                            result.cli_options[f"{canonical}_lang"] = lang_suffix
                # Check if it's a language selector (e.g., -en, -es)
                elif self.lang_manager.is_language_available(opt_char):
                    result.language_selector = opt_char
                    result.cli_options["lang_selector"] = opt_char
                else:
                    result.diagnostics.append(err_unknown_option(arg))
                i += 1
                continue

            # Check for help command (special case - can appear anywhere)
            if arg == "help" and not addon_identified:
                if result.command is None:
                    result.command = "help"
                    i += 1
                    # Parse remaining args as help command args
                    while i < len(argv):
                        help_arg = argv[i]
                        if help_arg == "-lang":
                            result.cli_options["lang"] = True
                        elif help_arg in ("-u", "--usage", "-usage"):
                            result.cli_options["usage"] = True
                        elif help_arg.startswith("--usage-"):
                            # Handle --usage-<lang>
                            lang_code = help_arg[len("--usage-"):]
                            result.cli_options["usage"] = True
                            if self.lang_manager.is_language_available(lang_code):
                                result.cli_options["usage_lang"] = lang_code
                        elif help_arg.startswith("-u-"):
                            # Handle -u-<lang>
                            lang_code = help_arg[len("-u-"):]
                            result.cli_options["usage"] = True
                            if self.lang_manager.is_language_available(lang_code):
                                result.cli_options["usage_lang"] = lang_code
                        elif help_arg.startswith("-") and not help_arg.startswith("--"):
                            # Language selector like -en, -es
                            lang_code = help_arg[1:]
                            if self.lang_manager.is_language_available(lang_code):
                                result.language_selector = lang_code
                                result.cli_options["lang_selector"] = lang_code
                            else:
                                result.positional_args.append(help_arg)
                        else:
                            result.positional_args.append(help_arg)
                        i += 1
                    break
                else:
                    # help after addon is an addon argument
                    if addon_identified:
                        result.addon_args.append(arg)
                    else:
                        result.positional_args.append(arg)
                    i += 1
                continue

            # Identify addon (only if no command has been identified yet)
            if not addon_identified and not result.command and arg in self.addon_identifiers:
                result.addon_identifier = arg
                addon_identified = True
                i += 1
                # Remaining args go to addon
                result.addon_args = argv[i:]
                break

            # Identify internal command
            if not addon_identified and arg in self.internal_commands:
                if result.command is None:
                    result.command = arg
                elif result.subcommand is None:
                    result.subcommand = arg
                else:
                    result.positional_args.append(arg)
                i += 1
                continue

            # Positional argument before addon
            if not addon_identified and not arg.startswith("-"):
                if result.command is None:
                    result.command = arg
                elif result.subcommand is None:
                    result.subcommand = arg
                else:
                    result.positional_args.append(arg)
                i += 1
                continue

            # Unknown option before addon
            if not addon_identified and arg.startswith("-"):
                result.diagnostics.append(err_unknown_option(arg))
                i += 1
                continue

            # Should not reach here, but handle gracefully
            if not addon_identified:
                result.positional_args.append(arg)
                i += 1

        return result

    def parse_addon_args(self, addon_identifier: str, argv: list[str]) -> tuple[dict[str, Any], list[str]]:
        """Parse arguments after addon identification.

        Returns (cli_options, addon_args) where cli_options are single-hyphen
        options that belong to RtG-CLI, and addon_args are passed to the addon.
        """
        cli_options: dict[str, Any] = {}
        addon_args: list[str] = []

        for arg in argv:
            if arg.startswith("-") and not arg.startswith("--"):
                # Single hyphen - check if it's a CLI option
                opt_char = arg[1:]
                if len(opt_char) == 1 and opt_char in self.SYSTEM_SHORT_OPTIONS:
                    canonical = self.SYSTEM_SHORT_OPTIONS[opt_char]
                    cli_options[canonical] = True
                    continue
                # Check if it's a language selector
                elif self.lang_manager.is_language_available(opt_char, f"addon/{addon_identifier}"):
                    cli_options["lang_selector"] = opt_char
                    continue
                # Unknown single-hyphen option
                cli_options["unknown"] = arg
            else:
                # No hyphen or double hyphen - belongs to addon
                addon_args.append(arg)

        return cli_options, addon_args


def create_parser(config, language_manager: LanguageManager) -> ArgumentParser:
    """Factory for ArgumentParser."""
    return ArgumentParser(config, language_manager)


__all__ = [
    "ArgType",
    "ParsedArgument",
    "ParsedCommandLine",
    "ArgumentParser",
    "create_parser",
]