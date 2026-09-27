"""Main application class for RtG-CLI."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .arguments import ArgumentParser, ParsedCommandLine, create_parser
from .configuration import CliConfig, get_config, load_config
from .diagnostics import Diagnostic, DiagnosticHandler, ExitCode, err_internal
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
        self.addon_executor = create_addon_executor(self.registry, self.config, self.lang_manager)
        self.internal_executor = create_internal_executor(self.config, self.lang_manager, self.registry)
        self.help_system = create_help_system(self.config, self.lang_manager)
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

        # Handle -language before anything else
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
            from .diagnostics import err_unknown_command

            diag = err_unknown_command(argv[0])
            self.help_system.show_void(parsed.language_selector)
            return self.diagnostic_handler.handle(diag)

        # Default: show void
        self.help_system.show_void(parsed.language_selector)
        return ExitCode.SUCCESS


def main(argv: list[str] | None = None, debug: bool = False) -> int:
    """Main entry point."""
    try:
        config = get_config()
    except Exception as e:
        handler = DiagnosticHandler(debug=debug)
        return handler.handle_exception(e)

    app = Application(config, debug=debug)
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(main())


__all__ = [
    "Application",
    "main",
]