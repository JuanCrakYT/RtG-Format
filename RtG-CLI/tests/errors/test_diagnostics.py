#!/usr/bin/env python3
"""Tests for error handling and diagnostics."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.diagnostics import (
    Diagnostic,
    DiagnosticHandler,
    ExitCode,
    ErrorCategory,
    err_usage,
    err_unknown_command,
    err_unknown_option,
    err_invalid_argument,
    err_addon_not_found,
    err_addon_unavailable,
    err_addon_execution_failure,
    err_program_command_not_found,
    err_program_execution_failure,
    err_invalid_configuration,
    err_invalid_language,
    err_internal,
    err_file,
    err_interrupted,
)


class TestDiagnostics(unittest.TestCase):
    """Test diagnostic system."""

    def test_exit_codes(self):
        """Test exit codes are defined."""
        self.assertEqual(ExitCode.SUCCESS, 0)
        self.assertEqual(ExitCode.USAGE_ERROR, 1)
        self.assertEqual(ExitCode.UNKNOWN_COMMAND, 2)
        self.assertEqual(ExitCode.UNKNOWN_OPTION, 3)
        self.assertEqual(ExitCode.INVALID_ARGUMENT, 4)
        self.assertEqual(ExitCode.ADDON_NOT_FOUND, 5)
        self.assertEqual(ExitCode.ADDON_UNAVAILABLE, 6)
        self.assertEqual(ExitCode.ADDON_EXECUTION_FAILURE, 7)
        self.assertEqual(ExitCode.PROGRAM_COMMAND_NOT_FOUND, 8)
        self.assertEqual(ExitCode.PROGRAM_EXECUTION_FAILURE, 9)
        self.assertEqual(ExitCode.INVALID_CONFIGURATION, 10)
        self.assertEqual(ExitCode.INVALID_LANGUAGE, 11)
        self.assertEqual(ExitCode.INTERNAL_ERROR, 12)
        self.assertEqual(ExitCode.FILE_ERROR, 13)
        self.assertEqual(ExitCode.INTERRUPTED, 130)

    def test_diagnostic_creation(self):
        """Test diagnostic creation."""
        diag = Diagnostic(
            message="Test error",
            category="test",
            exit_code=1,
            debug_info={"key": "value"},
        )
        self.assertEqual(diag.message, "Test error")
        self.assertEqual(diag.category, "test")
        self.assertEqual(diag.exit_code, 1)
        self.assertEqual(diag.debug_info, {"key": "value"})

    def test_diagnostic_to_stderr(self):
        """Test diagnostic stderr formatting."""
        diag = Diagnostic(
            message="Test error",
            category="test",
            exit_code=1,
        )
        output = diag.to_stderr()
        self.assertEqual(output, "[test] Test error")

    def test_diagnostic_to_stderr_debug(self):
        """Test diagnostic stderr formatting with debug."""
        diag = Diagnostic(
            message="Test error",
            category="test",
            exit_code=1,
            debug_info={"key": "value"},
        )
        output = diag.to_stderr(debug=True)
        self.assertIn("[test] Test error", output)
        self.assertIn("Debug info:", output)
        self.assertIn("key", output)

    def test_factory_functions(self):
        """Test diagnostic factory functions."""
        diag = err_usage("Usage error")
        self.assertEqual(diag.category, "usage")
        self.assertEqual(diag.exit_code, 1)

        diag = err_unknown_command("badcmd")
        self.assertEqual(diag.category, "command")
        self.assertEqual(diag.exit_code, 2)
        self.assertEqual(diag.debug_info["command"], "badcmd")

        diag = err_unknown_option("--bad")
        self.assertEqual(diag.category, "option")
        self.assertEqual(diag.exit_code, 3)

        diag = err_invalid_argument("arg", "reason")
        self.assertEqual(diag.category, "argument")
        self.assertEqual(diag.exit_code, 4)

        diag = err_addon_not_found("badaddon")
        self.assertEqual(diag.category, "addon")
        self.assertEqual(diag.exit_code, 5)

        diag = err_addon_unavailable("addon", "reason")
        self.assertEqual(diag.category, "addon")
        self.assertEqual(diag.exit_code, 6)

        diag = err_addon_execution_failure("addon", "reason")
        self.assertEqual(diag.category, "addon")
        self.assertEqual(diag.exit_code, 7)

        diag = err_program_command_not_found("prog", "cmd")
        self.assertEqual(diag.category, "program")
        self.assertEqual(diag.exit_code, 8)

        diag = err_program_execution_failure("prog", "reason")
        self.assertEqual(diag.category, "program")
        self.assertEqual(diag.exit_code, 9)

        diag = err_invalid_configuration("reason")
        self.assertEqual(diag.category, "configuration")
        self.assertEqual(diag.exit_code, 10)

        diag = err_invalid_language("xx")
        self.assertEqual(diag.category, "language")
        self.assertEqual(diag.exit_code, 11)

        diag = err_internal("reason")
        self.assertEqual(diag.category, "internal")
        self.assertEqual(diag.exit_code, 12)

        diag = err_file("reason")
        self.assertEqual(diag.category, "file")
        self.assertEqual(diag.exit_code, 13)

        diag = err_interrupted()
        self.assertEqual(diag.category, "interrupt")
        self.assertEqual(diag.exit_code, 130)

    def test_diagnostic_handler(self):
        """Test diagnostic handler."""
        handler = DiagnosticHandler(debug=False)
        diag = err_usage("Test error")
        # Just test it doesn't crash
        code = handler.handle(diag)
        self.assertEqual(code, 1)

    def test_diagnostic_handler_debug(self):
        """Test diagnostic handler with debug."""
        handler = DiagnosticHandler(debug=True)
        diag = err_usage("Test error", {"debug": "info"})
        code = handler.handle(diag)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()