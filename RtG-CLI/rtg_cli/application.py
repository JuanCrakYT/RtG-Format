"""Main application class for RtG-CLI."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .arguments import ArgumentParser, ParsedCommandLine, create_parser
from .configuration import CliConfig, get_config, load_config
from .diagnostics import Diagnostic, DiagnosticHandler, ExitCode, err_internal, err_unknown_command
from .execution import AddonExecutor, InternalCommandExecutor, create_addon_executor, create_internal_executor
from .addons import AddonRegistry, create_addon_registry
from .languages import LanguageManager, get_language_manager
from .help import HelpSystem, create_help_system
from .version import VersionManager, create_version_manager


class Application:
    """Main RtG-CLI application."""

    def __init__(self, config: CliConfig | None = None, debug: bool = False):
        self.config = config or get_config()
        self.debug = debug
        self.diagnostic_handler = DiagnosticHandler(debug=debug)

        # Initialize subsystems
        self.lang_manager = get_language_manager(self.config)
        self.registry = create_addon_registry(self.config, self.lang_manager)
        self.parser = create_parser(self.config, self.lang_manager)
        self.help_system = create_help_system(self.config, self.lang_manager)
        self.addon_executor = create_addon_executor(self.registry, self.config, self.lang_manager)
        self.internal_executor = create_internal_executor(self.config, self.lang_manager, self.registry, self.help_system)
        self.version_manager = create_version_manager(self.config, self.lang_manager)

    def run(self, argv: list[str] | None = None) -> int:
        """Run the application with given arguments."""
        if argv is None:
            argv = sys.argv[1:]

        try:
            parsed = self.parser.parse(argv)
        except Exception as e:
            return self.diagnostic_handler.handle_exception(e)

        if parsed.has_errors():
            return self.diagnostic_handler.handle(parsed.get_first_error())

        # Handle system CLI options first (version, help, rules, lang, commands, addons, language)
        if parsed.cli_options.get("version"):
            self.version_manager.show_cli_version()
            return ExitCode.SUCCESS

        if parsed.cli_options.get("help"):
            self.help_system.show_general_help(parsed.cli_options.get("lang_selector"))
            return ExitCode.SUCCESS

        if parsed.cli_options.get("rules"):
            lang = parsed.cli_options.get("lang_selector")
            self.help_system.show_rules(lang)
            return ExitCode.SUCCESS

        if parsed.cli_options.get("lang"):
            self.help_system.show_cli_languages()
            return ExitCode.SUCCESS

        if parsed.cli_options.get("commands"):
            self.help_system.show_commands_list()
            return ExitCode.SUCCESS

        if parsed.cli_options.get("addons"):
            self.help_system.show_addons_list()
            return ExitCode.SUCCESS

        if "language" in parsed.cli_options:
            lang = parsed.cli_options["language"]
            self.help_system.show_void(lang)
            return ExitCode.SUCCESS

        if parsed.cli_options.get("usage"):
            lang = parsed.cli_options.get("usage_lang") or parsed.cli_options.get("lang_selector")
            self.help_system.show_usage(lang)
            return ExitCode.SUCCESS

        # Handle -language before anything else (legacy)
        if parsed.language_selector and not parsed.addon_identifier and not parsed.command:
            self.help_system.show_void(parsed.language_selector)
            return ExitCode.SUCCESS

        # No arguments - show void
        if not argv:
            self.help_system.show_void()
            return ExitCode.SUCCESS

        # Execute addon if identified
        if parsed.addon_identifier:
            return self.addon_executor.execute(parsed).exit_code

        # Execute internal command
        if parsed.command:
            return self.internal_executor.execute(parsed).exit_code

        # Unknown command
        if argv:
            diag = err_unknown_command(argv[0])
            self.help_system.show_void(parsed.language_selector)
            return self.diagnostic_handler.handle(diag)

        # Default: show void
        self.help_system.show_void(parsed.language_selector)
        return ExitCode.SUCCESS


def main(argv: list[str] | None = None, debug: bool = False) -> int:
    """Main entry point."""
    # Configure UTF-8 encoding for stdout/stderr on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    try:
        config = get_config()
    except Exception as e:
        handler = DiagnosticHandler(debug=debug)
        return handler.handle_exception(e)

    app = Application(config, debug=debug)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())