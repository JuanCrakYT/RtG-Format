#!/usr/bin/env python3
"""Tests for addon and program command execution."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import get_config
from rtg_cli.languages import get_language_manager
from rtg_cli.arguments import create_parser
from rtg_cli.execution import create_addon_executor, create_internal_executor
from rtg_cli.addons import create_addon_registry


class TestExecution(unittest.TestCase):
    """Test execution functionality."""

    @classmethod
    def setUpClass(cls):
        cls.config = get_config()
        cls.lang_manager = get_language_manager(cls.config)
        cls.parser = create_parser(cls.config, cls.lang_manager)
        cls.registry = create_addon_registry(cls.config, cls.lang_manager)
        cls.addon_executor = create_addon_executor(cls.registry, cls.config, cls.lang_manager)
        cls.internal_executor = create_internal_executor(cls.config, cls.lang_manager, cls.registry)

    def _parse_and_execute_addon(self, argv: list[str]) -> int:
        """Parse and execute addon command."""
        parsed = self.parser.parse(argv)
        if parsed.has_errors():
            return parsed.get_first_error().exit_code
        return self.addon_executor.execute(parsed).exit_code

    def test_test_addon_no_args(self):
        """Test test-addon with no arguments."""
        result = self._parse_and_execute_addon(["test-addon"])
        self.assertEqual(result, 0)

    def test_test_addon_echo(self):
        """Test test-addon echo command."""
        result = self._parse_and_execute_addon(["test-addon", "echo", "hello world"])
        self.assertEqual(result, 0)

    def test_test_addon_fail(self):
        """Test test-addon fail command."""
        result = self._parse_and_execute_addon(["test-addon", "fail"])
        self.assertEqual(result, 1)

    def test_test_addon_fail_with_message(self):
        """Test test-addon fail with message."""
        result = self._parse_and_execute_addon(["test-addon", "fail", "error message"])
        self.assertEqual(result, 1)

    def test_test_addon_stdout(self):
        """Test test-addon stdout command."""
        result = self._parse_and_execute_addon(["test-addon", "stdout", "test output"])
        self.assertEqual(result, 0)

    def test_test_addon_stderr(self):
        """Test test-addon stderr command."""
        result = self._parse_and_execute_addon(["test-addon", "stderr", "error output"])
        self.assertEqual(result, 0)

    def test_test_addon_exit_code(self):
        """Test test-addon exit-code command."""
        result = self._parse_and_execute_addon(["test-addon", "exit-code", "42"])
        self.assertEqual(result, 42)

    def test_test_addon_help(self):
        """Test test-addon help command."""
        result = self._parse_and_execute_addon(["test-addon", "help"])
        self.assertEqual(result, 0)

    def test_test_addon_help_specific(self):
        """Test test-addon help for specific command."""
        result = self._parse_and_execute_addon(["test-addon", "help", "echo"])
        self.assertEqual(result, 0)

    def test_test_addon_unknown_command(self):
        """Test test-addon unknown command."""
        result = self._parse_and_execute_addon(["test-addon", "unknown"])
        self.assertEqual(result, 1)

    def test_test_addon_exit_code_invalid(self):
        """Test test-addon exit-code with invalid value."""
        result = self._parse_and_execute_addon(["test-addon", "exit-code", "invalid"])
        self.assertEqual(result, 1)

    def test_test_addon_exit_code_out_of_range(self):
        """Test test-addon exit-code out of range."""
        result = self._parse_and_execute_addon(["test-addon", "exit-code", "300"])
        self.assertEqual(result, 1)

    def test_addon_lang_option(self):
        """Test addon -lang option shows languages."""
        result = self._parse_and_execute_addon(["test-addon", "-lang"])
        self.assertEqual(result, 0)

    def test_image_addon_no_interface(self):
        """Test image addon without program interface shows info."""
        result = self._parse_and_execute_addon(["image"])
        self.assertEqual(result, 0)

    def test_preview_addon_no_interface(self):
        """Test preview addon without program interface shows info."""
        result = self._parse_and_execute_addon(["preview"])
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()