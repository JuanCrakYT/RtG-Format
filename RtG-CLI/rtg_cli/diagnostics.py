"""Diagnostics and error handling for RtG-CLI."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class ExitCode(IntEnum):
    """Standard exit codes for RtG-CLI."""

    SUCCESS = 0
    USAGE_ERROR = 1
    UNKNOWN_COMMAND = 2
    UNKNOWN_OPTION = 3
    INVALID_ARGUMENT = 4
    ADDON_NOT_FOUND = 5
    ADDON_UNAVAILABLE = 6
    ADDON_EXECUTION_FAILURE = 7
    PROGRAM_COMMAND_NOT_FOUND = 8
    PROGRAM_EXECUTION_FAILURE = 9
    INVALID_CONFIGURATION = 10
    INVALID_LANGUAGE = 11
    INTERNAL_ERROR = 12
    FILE_ERROR = 13
    INTERRUPTED = 130


class ErrorCategory(str):
    """Error category identifiers."""

    USAGE = "usage"
    COMMAND = "command"
    OPTION = "option"
    ARGUMENT = "argument"
    ADDON = "addon"
    PROGRAM = "program"
    CONFIGURATION = "configuration"
    LANGUAGE = "language"
    INTERNAL = "internal"
    FILE = "file"
    INTERRUPT = "interrupt"


@dataclass(frozen=True)
class Diagnostic:
    """Structured diagnostic message."""

    message: str
    category: str
    exit_code: int
    debug_info: dict[str, Any] | None = None

    def to_stderr(self, debug: bool = False) -> str:
        """Format for stderr output."""
        if debug and self.debug_info:
            import json

            debug_str = json.dumps(self.debug_info, indent=2, ensure_ascii=False)
            return f"[{self.category}] {self.message}\nDebug info:\n{debug_str}"
        return f"[{self.category}] {self.message}"


def make_diagnostic(
    message: str,
    category: str,
    exit_code: ExitCode,
    debug_info: dict[str, Any] | None = None,
) -> Diagnostic:
    """Factory for creating diagnostics."""
    return Diagnostic(message=message, category=category, exit_code=int(exit_code), debug_info=debug_info)


# Pre-defined common diagnostics
def err_usage(message: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(message, ErrorCategory.USAGE, ExitCode.USAGE_ERROR, debug_info)


def err_unknown_command(command: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Unknown command: {command}",
        ErrorCategory.COMMAND,
        ExitCode.UNKNOWN_COMMAND,
        debug_info or {"command": command},
    )


def err_unknown_option(option: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Unknown option: {option}",
        ErrorCategory.OPTION,
        ExitCode.UNKNOWN_OPTION,
        debug_info or {"option": option},
    )


def err_invalid_argument(arg: str, reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Invalid argument '{arg}': {reason}",
        ErrorCategory.ARGUMENT,
        ExitCode.INVALID_ARGUMENT,
        debug_info or {"argument": arg, "reason": reason},
    )


def err_addon_not_found(addon: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Addon not found: {addon}",
        ErrorCategory.ADDON,
        ExitCode.ADDON_NOT_FOUND,
        debug_info or {"addon": addon},
    )


def err_addon_unavailable(addon: str, reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Addon unavailable: {addon} ({reason})",
        ErrorCategory.ADDON,
        ExitCode.ADDON_UNAVAILABLE,
        debug_info or {"addon": addon, "reason": reason},
    )


def err_addon_execution_failure(addon: str, reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Addon execution failed: {addon} ({reason})",
        ErrorCategory.ADDON,
        ExitCode.ADDON_EXECUTION_FAILURE,
        debug_info or {"addon": addon, "reason": reason},
    )


def err_program_command_not_found(program: str, command: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Program command not found: {command} (in {program})",
        ErrorCategory.PROGRAM,
        ExitCode.PROGRAM_COMMAND_NOT_FOUND,
        debug_info or {"program": program, "command": command},
    )


def err_program_execution_failure(program: str, reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Program execution failed: {program} ({reason})",
        ErrorCategory.PROGRAM,
        ExitCode.PROGRAM_EXECUTION_FAILURE,
        debug_info or {"program": program, "reason": reason},
    )


def err_invalid_configuration(reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Invalid configuration: {reason}",
        ErrorCategory.CONFIGURATION,
        ExitCode.INVALID_CONFIGURATION,
        debug_info or {"reason": reason},
    )


def err_invalid_language(lang: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Invalid or unavailable language: {lang}",
        ErrorCategory.LANGUAGE,
        ExitCode.INVALID_LANGUAGE,
        debug_info or {"language": lang},
    )


def err_internal(message: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"Internal error: {message}",
        ErrorCategory.INTERNAL,
        ExitCode.INTERNAL_ERROR,
        debug_info or {"message": message},
    )


def err_file(reason: str, debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        f"File error: {reason}",
        ErrorCategory.FILE,
        ExitCode.FILE_ERROR,
        debug_info or {"reason": reason},
    )


def err_interrupted(debug_info: dict[str, Any] | None = None) -> Diagnostic:
    return make_diagnostic(
        "Interrupted",
        ErrorCategory.INTERRUPT,
        ExitCode.INTERRUPTED,
        debug_info,
    )


class DiagnosticHandler:
    """Handles diagnostic output and program termination."""

    def __init__(self, debug: bool = False, stderr=None):
        self.debug = debug
        self.stderr = stderr or sys.stderr

    def handle(self, diagnostic: Diagnostic) -> int:
        """Print diagnostic and return exit code."""
        print(diagnostic.to_stderr(self.debug), file=self.stderr)
        return diagnostic.exit_code

    def handle_exception(self, exc: Exception) -> int:
        """Handle an uncaught exception."""
        if self.debug:
            import traceback

            traceback.print_exc(file=self.stderr)
            return ExitCode.INTERNAL_ERROR
        return self.handle(err_internal(str(exc), {"exception": type(exc).__name__}))

    def exit(self, diagnostic: Diagnostic) -> None:
        """Print diagnostic and exit."""
        sys.exit(self.handle(diagnostic))


__all__ = [
    "ExitCode",
    "ErrorCategory",
    "Diagnostic",
    "DiagnosticHandler",
    "make_diagnostic",
    "err_usage",
    "err_unknown_command",
    "err_unknown_option",
    "err_invalid_argument",
    "err_addon_not_found",
    "err_addon_unavailable",
    "err_addon_execution_failure",
    "err_program_command_not_found",
    "err_program_execution_failure",
    "err_invalid_configuration",
    "err_invalid_language",
    "err_internal",
    "err_file",
    "err_interrupted",
]