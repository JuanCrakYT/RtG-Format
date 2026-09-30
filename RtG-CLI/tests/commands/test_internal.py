#!/usr/bin/env python3
"""Tests for internal commands."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import get_config
from rtg_cli.languages import get_language_manager
from rtg_cli.arguments import create_parser
from rtg_cli.execution import create_internal_executor
from rtg_cli.addons import create_addon_registry
from rtg_cli.help import create_help_system


class TestInternalCommands(unittest.TestCase):
    """Test internal command execution."""

    @classmethod
    def setUpClass(cls):
        cls.config = get_config()
        cls.lang_manager = get_language_manager(cls.config)
        cls.parser = create_parser(cls.config, cls.lang_manager)
        cls.registry = create_addon_registry(cls.config, cls.lang_manager)
        cls.help_system = create_help_system(cls.config, cls.lang_manager)
        cls.executor = create_internal_executor(cls.config, cls.lang_manager, cls.registry, cls.help_system)

    def _execute(self, argv: list[str]) -> int:
        """Parse and execute command."""
        parsed = self.parser.parse(argv)
        if parsed.has_errors():
            return parsed.get_first_error().exit_code
        return self.executor.execute(parsed).exit_code

    def test_version_command(self):
        """Test version command."""
        result = self._execute(["--version"])
        self.assertEqual(result, 0)

    def test_version_short(self):
        """Test -v command."""
        result = self._execute(["-v"])
        self.assertEqual(result, 0)

    def test_help_command(self):
        """Test help command."""
        result = self._execute(["help"])
        self.assertEqual(result, 0)

    def test_help_short(self):
        """Test -h command."""
        result = self._execute(["-h"])
        self.assertEqual(result, 0)

    def test_help_with_target(self):
        """Test help with command target."""
        result = self._execute(["help", "image"])
        self.assertEqual(result, 0)

    def test_help_with_language(self):
        """Test help with language selector."""
        result = self._execute(["help", "image", "-en"])
        self.assertEqual(result, 0)

    def test_help_list_langs(self):
        """Test help -lang lists languages."""
        result = self._execute(["help", "image", "-lang"])
        self.assertEqual(result, 0)

    def test_rules_command(self):
        """Test rules command."""
        result = self._execute(["--rules"])
        self.assertEqual(result, 0)

    def test_rules_short(self):
        """Test -r command."""
        result = self._execute(["-r"])
        self.assertEqual(result, 0)

    def test_rules_with_language(self):
        """Test rules with language selector."""
        result = self._execute(["--rules", "-en"])
        self.assertEqual(result, 0)

    def test_lang_command(self):
        """Test lang command."""
        result = self._execute(["--lang"])
        self.assertEqual(result, 0)

    def test_lang_short(self):
        """Test -l command."""
        result = self._execute(["-l"])
        self.assertEqual(result, 0)

    def test_commands_command(self):
        """Test commands command."""
        result = self._execute(["--commands"])
        self.assertEqual(result, 0)

    def test_commands_short(self):
        """Test -c command."""
        result = self._execute(["-c"])
        self.assertEqual(result, 0)

    def test_addons_command(self):
        """Test addons command."""
        result = self._execute(["--addons"])
        self.assertEqual(result, 0)

    def test_addons_short(self):
        """Test -a command."""
        result = self._execute(["-a"])
        self.assertEqual(result, 0)

    def test_language_command(self):
        """Test -language command."""
        result = self._execute(["-language", "en"])
        self.assertEqual(result, 0)

    def test_void_default(self):
        """Test default void output."""
        result = self._execute([])
        self.assertEqual(result, 0)

    def test_unknown_command_shows_void(self):
        """Test unknown command shows void and returns 0 (legacy behavior)."""
        result = self._execute(["unknowncmd"])
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()