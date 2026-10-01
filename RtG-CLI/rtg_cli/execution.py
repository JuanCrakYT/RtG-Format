"""Execution engine for addons and program commands."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .addons import AddonRegistry, ProgramCommandInterface
from .arguments import ArgumentParser, ParsedCommandLine
from .configuration import CliConfig
from .diagnostics import (
    Diagnostic,
    ExitCode,
    err_addon_execution_failure,
    err_addon_not_found,
    err_addon_unavailable,
    err_program_execution_failure,
)
from .languages import LanguageManager


@dataclass(frozen=True)
class ExecutionResult:
    """Result of an execution."""

    exit_code: int
    stdout: str = ""
    stderr: str = ""
    diagnostic: Diagnostic | None = None


class AddonExecutor:
    """Executes addons via their program command interface."""

    def __init__(self, registry: AddonRegistry, config: CliConfig, lang_manager: LanguageManager):
        self.registry = registry
        self.config = config
        self.lang_manager = lang_manager

    def execute(self, parsed: ParsedCommandLine) -> ExecutionResult:
        """Execute an addon based on parsed command line."""
        addon_id = parsed.addon_identifier
        if not addon_id:
            return ExecutionResult(
                exit_code=ExitCode.USAGE_ERROR,
                diagnostic=err_addon_not_found(""),
            )

        addon = self.registry.get(addon_id)
        if not addon:
            return ExecutionResult(
                exit_code=ExitCode.ADDON_NOT_FOUND,
                diagnostic=err_addon_not_found(addon_id),
            )

        if not addon.has_documentation:
            return ExecutionResult(
                exit_code=ExitCode.ADDON_UNAVAILABLE,
                diagnostic=err_addon_unavailable(addon_id, "No documentation or languages available"),
            )

        interface = self.registry.get_interface(addon_id)
        if not interface:
            # Fallback: show addon info
            return self._show_addon_info(addon_id, parsed.addon_args)

        # Parse addon-specific CLI options (single hyphen = CLI, others = addon)
        cli_opts, addon_args = self._parse_addon_args(addon_id, parsed.addon_args)

        # Handle CLI options after addon
        if cli_opts.get("lang"):
            self._show_addon_languages(addon)
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        if cli_opts.get("unknown"):
            from .diagnostics import err_unknown_option

            return ExecutionResult(
                exit_code=ExitCode.UNKNOWN_OPTION,
                diagnostic=err_unknown_option(cli_opts["unknown"]),
            )

        # Execute the addon
        try:
            exit_code = interface.execute(addon_args)
            return ExecutionResult(exit_code=exit_code)
        except Exception as e:
            return ExecutionResult(
                exit_code=ExitCode.ADDON_EXECUTION_FAILURE,
                diagnostic=err_addon_execution_failure(addon_id, str(e)),
            )

    def _parse_addon_args(self, addon_id: str, args: list[str]) -> tuple[dict[str, Any], list[str]]:
        """Parse arguments after addon identification."""
        cli_options: dict[str, Any] = {}
        addon_args: list[str] = []

        for arg in args:
            if arg.startswith("-") and not arg.startswith("--"):
                opt_char = arg[1:]
                # Check if it's a single-char system option
                if len(opt_char) == 1 and opt_char in ("l", "h", "v", "r", "c", "a"):
                    cli_options[opt_char] = True
                    continue
                # Check if it's a multi-char option like -lang
                elif opt_char == "lang":
                    cli_options["lang"] = True
                    continue
                # Check if it's a language selector
                elif self.lang_manager.is_language_available(opt_char, f"addon/{addon_id}"):
                    cli_options["lang_selector"] = opt_char
                    continue
                # Unknown single-hyphen option
                cli_options["unknown"] = arg
            else:
                # No hyphen or double hyphen - belongs to addon
                addon_args.append(arg)

        return cli_options, addon_args

    def _show_addon_info(self, addon_id: str, addon_args: list[str]) -> ExecutionResult:
        """Fallback: show addon info when no program interface available."""
        addon = self.registry.get(addon_id)
        if not addon:
            return ExecutionResult(exit_code=ExitCode.ADDON_NOT_FOUND, diagnostic=err_addon_not_found(addon_id))

        lines = [f"\n{addon.name}\n", "-" * len(addon.name)]

        if addon.creators:
            lines.append("\nCreators:")
            for creator, notes in addon.creators.items():
                for note in notes:
                    lines.append(f"    {note} ({creator})")

        if addon.languages:
            lines.append("\nLanguages:")
            for lang in addon.languages:
                name = self.lang_manager.get_language_name(lang)
                lines.append(f"    {name} | {lang}")

        lines.append("\nVersion:")
        lines.append("    Content:")
        if addon.version:
            lines.append(f"        VERSION {addon.version}")
        else:
            lines.append("        [No version information]")

        content_width = max(len(line) for line in lines)
        lines.append("")
        lines.append("|" + "-" * content_width + "|")
        lines.append("|" + " Run Output".ljust(content_width) + "|")
        lines.append("|" + "-" * content_width + "|")

        output = "\n".join(lines)
        print(output)

        if addon_args:
            name = addon.name
            print()
            print(f"Arguments for {name}:")
            for arg in addon_args:
                print(f"  {arg}")

        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _show_addon_languages(self, addon) -> None:
        """Show languages available for an addon."""
        print("Available languages:")
        print()
        for lang in addon.languages:
            name = self.lang_manager.get_language_name(lang)
            print(f"  {name} | {lang}")


class InternalCommandExecutor:
    """Executes internal CLI commands."""

    def __init__(self, config: CliConfig, lang_manager: LanguageManager, registry: AddonRegistry, help_system):
        self.config = config
        self.lang_manager = lang_manager
        self.registry = registry
        self.help_system = help_system

    def execute(self, parsed: ParsedCommandLine) -> ExecutionResult:
        """Execute an internal command."""
        command = parsed.command

        # Handle system CLI options first (these come from cli_options, not command)
        if parsed.cli_options.get("version"):
            return self._execute_version(parsed)
        if parsed.cli_options.get("help"):
            return self._execute_help(parsed)
        if parsed.cli_options.get("rules"):
            return self._execute_rules(parsed)
        if parsed.cli_options.get("lang"):
            return self._execute_lang(parsed)
        if parsed.cli_options.get("commands"):
            return self._execute_commands(parsed)
        if parsed.cli_options.get("addons"):
            return self._execute_addons(parsed)
        if "language" in parsed.cli_options:
            return self._execute_language(parsed)

        # No command - show void (legacy behavior)
        if not command:
            self._show_void(parsed.cli_options.get("language"))
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        if command in ("version", "v"):
            return self._execute_version(parsed)
        elif command in ("help", "h"):
            return self._execute_help(parsed)
        elif command in ("rules", "r"):
            return self._execute_rules(parsed)
        elif command in ("lang", "l"):
            return self._execute_lang(parsed)
        elif command in ("commands", "c"):
            return self._execute_commands(parsed)
        elif command in ("addons", "a"):
            return self._execute_addons(parsed)
        elif command == "language":
            return self._execute_language(parsed)
        else:
            # Unknown command - show void (legacy behavior)
            self._show_void(parsed.cli_options.get("language"))
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_version(self, parsed: ParsedCommandLine) -> ExecutionResult:
        print(self.config.version)
        if self.config.version_content:
            print()
            for lang, content in self.config.version_content.items():
                name = self.lang_manager.get_language_name(lang)
                print(f"--- {name} ({lang}) ---")
                print(content, end="")
                print()
        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_help(self, parsed: ParsedCommandLine) -> ExecutionResult:
        target = parsed.positional_args[0] if parsed.positional_args else None
        lang = parsed.cli_options.get("lang_selector")
        list_langs = parsed.cli_options.get("lang", False)
        
        # Check for usage_lang option (from -u-es, --usage-es, etc.)
        usage_lang = parsed.cli_options.get("usage_lang")

        # Handle help --usage / -u / --usage-<lang> / -u-<lang>
        if target in ("--usage", "-u", "usage"):
            self.help_system.show_usage(usage_lang or lang)
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        if target is None:
            if list_langs:
                self._show_cli_languages()
            else:
                self._show_help_file(lang)
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        # Check if target is an internal command
        if target in self.config.internal.command_list:
            internal_help = self.config.internal.help_texts.get(target, {})
            if list_langs:
                print("Available languages:")
                print()
                for l in internal_help:
                    print(f"  {l}")
            elif lang and lang in internal_help:
                print(internal_help[lang], end="")
            else:
                if internal_help:
                    first = next(iter(internal_help))
                    print(internal_help[first], end="")
                else:
                    print(f"No help available for '{target}'.")
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        # Check if target is an addon
        addon = self.registry.get(target)
        if addon:
            if list_langs:
                self._show_addon_languages(addon)
            elif target in self.config.internal.help_texts:
                internal_help = self.config.internal.help_texts[target]
                if lang and lang in internal_help:
                    print(internal_help[lang], end="")
                else:
                    first = next(iter(internal_help))
                    print(internal_help[first], end="")
            else:
                interface = self.registry.get_interface(target)
                if interface:
                    help_text = interface.get_help(target, lang)
                    if help_text:
                        print(help_text, end="")
                    else:
                        self.show_addon_info(target)
                else:
                    self.show_addon_info(target)
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        # Unknown command
        print(f"Unknown command: {target}\n")
        self._show_void(parsed.cli_options.get("language"))
        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def show_addon_info(self, addon_id: str) -> None:
        """Show addon metadata and info frame (fallback when no interface)."""
        addon = self.registry.get(addon_id)
        if not addon:
            print(f"Unknown command: {addon_id}")
            print()
            self._show_void()
            return

        print(f"\n{addon.name}\n")
        print("-" * len(addon.name))

        if addon.creators:
            print("\nCreators:")
            print()
            for creator, notes in addon.creators.items():
                for note in notes:
                    print(f"    {note} ({creator})")

        if addon.languages:
            print("\nLanguages:")
            print()
            for lang in addon.languages:
                name = self.lang_manager.get_language_name(lang)
                print(f"    {name} | {lang}")

        print("\nVersion:")
        print()
        print("    Content:")
        if addon.version:
            print(f"        VERSION {addon.version}")
        else:
            print("        [No version information]")

        print()
        print("|" + "-" * 40 + "|")
        print("|" + " Run Output".ljust(40) + "|")
        print("|" + "-" * 40 + "|")

    def _execute_rules(self, parsed: ParsedCommandLine) -> ExecutionResult:
        lang = parsed.cli_options.get("lang_selector")
        rules = self.config.rules_paths

        if not rules:
            print("Rules not available.")
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        if lang and lang in rules:
            path = self.config.asset_paths.resolve_rules(lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read rules file: {rules[lang]}")
        else:
            default_lang = self.config.get_default_rules_language()
            path = self.config.asset_paths.resolve_rules(default_lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read rules file: {rules[default_lang]}")

        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_lang(self, parsed: ParsedCommandLine) -> ExecutionResult:
        self._show_cli_languages()
        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_commands(self, parsed: ParsedCommandLine) -> ExecutionResult:
        internal = self.config.internal
        command_list = internal.command_list
        internal_list_raw = self.config.raw.get("internal-list", [])

        if not command_list:
            print("No internal commands available.")
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        # Build a map of command -> description
        cmd_descriptions = {}
        for item in internal_list_raw:
            if isinstance(item, list) and len(item) >= 2:
                cmd, desc = item[0], item[1]
                cmd_descriptions[cmd] = desc

        # Print header
        print("RtG-CLI internal commands:")

        # Calculate column widths
        max_cmd_len = max(len(cmd) for cmd in command_list)
        col1_width = max(max_cmd_len, len("Comando"))

        # Print each command with description
        for cmd in command_list:
            desc = cmd_descriptions.get(cmd, "")
            # Group aliases (e.g., -h / --help)
            print(f"  {cmd.ljust(col1_width)}  | {desc}")

        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_addons(self, parsed: ParsedCommandLine) -> ExecutionResult:
        documented = self.registry.get_documented()
        if not documented:
            print("No addons with documentation available.")
            return ExecutionResult(exit_code=ExitCode.SUCCESS)

        print("Available addons (with documentation):")
        print()
        for key, addon in documented.items():
            print(f"  {key}  |  {addon.name}")
        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _execute_language(self, parsed: ParsedCommandLine) -> ExecutionResult:
        lang = parsed.cli_options.get("language")
        self._show_void(lang)
        return ExecutionResult(exit_code=ExitCode.SUCCESS)

    def _show_cli_languages(self) -> None:
        lang_names = self.config.language_names
        void_langs = sorted(self.config.void_language_paths.keys())
        help_langs = sorted(self.config.help_paths.keys())
        rules_langs = sorted(self.config.rules_paths.keys())
        version_langs = sorted(self.config.version_content.keys())

        def fmt(codes):
            return [f"  {lang_names.get(c, c)} | {c}" for c in codes]

        categories = [
            ("Version", version_langs),
            ("Rules", rules_langs),
            ("Help", help_langs),
        ]

        if void_langs:
            categories.append(("Void", void_langs))

        print("Available languages for RtG-CLI:")
        print()

        for category, codes in categories:
            if codes:
                print(f"  [{category}]")
                for line in fmt(codes):
                    print(line)
                print()

        addons = self.registry.get_all()
        for addon_id, addon in addons.items():
            addon_langs = sorted(addon.languages)
            if addon_langs:
                print(f"  [Addons / {addon_id}] ({addon.name})")
                for line in fmt(addon_langs):
                    print(line)
                print()

    def _show_help_file(self, lang: str | None) -> None:
        help_paths = self.config.help_paths
        if not help_paths:
            print("Help not available.")
            return

        langs = list(help_paths.keys())
        if lang and lang in help_paths:
            path = self.config.asset_paths.resolve_help(lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read help file: {help_paths[lang]}")
        else:
            path = self.config.asset_paths.resolve_help(langs[0])
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read help file: {help_paths[langs[0]]}")

    def _show_void(self, lang: str | None) -> None:
        if lang:
            void_lang = self.config.void_language_paths
            if lang in void_lang:
                path = self.config.asset_paths.resolve_void(lang)
                if path:
                    print(path, end="")
                else:
                    print(f"Language not available: {lang}\n")
                    print(self.config.void_text, end="")
            else:
                print(f"Language not available: {lang}\n")
                print(self.config.void_text, end="")
        else:
            print(self.config.void_text, end="")

    def _show_addon_languages(self, addon) -> None:
        print("Available languages:")
        print()
        for lang in addon.languages:
            name = self.lang_manager.get_language_name(lang)
            print(f"  {name} | {lang}")


def create_addon_executor(registry: AddonRegistry, config: CliConfig, lang_manager: LanguageManager) -> AddonExecutor:
    return AddonExecutor(registry, config, lang_manager)


def create_internal_executor(config: CliConfig, lang_manager: LanguageManager, registry: AddonRegistry, help_system) -> InternalCommandExecutor:
    return InternalCommandExecutor(config, lang_manager, registry, help_system)


__all__ = [
    "ExecutionResult",
    "AddonExecutor",
    "InternalCommandExecutor",
    "create_addon_executor",
    "create_internal_executor",
]