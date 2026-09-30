#!/usr/bin/env python3
"""Tests for argument parsing."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import get_config
from rtg_cli.languages import get_language_manager
from rtg_cli.arguments import create_parser, ParsedCommandLine


class TestArgumentParsing(unittest.TestCase):
    """Test argument parser functionality."""

    @classmethod
    def setUpClass(cls):
        cls.config = get_config()
        cls.lang_manager = get_language_manager(cls.config)
        cls.parser = create_parser(cls.config, cls.lang_manager)

    def test_empty_argv(self):
        """Test empty arguments returns empty parsed result."""
        result = self.parser.parse([])
        self.assertIsInstance(result, ParsedCommandLine)
        self.assertEqual(result.raw_args, [])

    def test_version_flag(self):
        """Test --version flag."""
        result = self.parser.parse(["--version"])
        self.assertTrue(result.cli_options.get("version"))
        self.assertFalse(result.has_errors())

    def test_version_short(self):
        """Test -v flag."""
        result = self.parser.parse(["-v"])
        self.assertTrue(result.cli_options.get("version"))

    def test_help_flag(self):
        """Test --help flag."""
        result = self.parser.parse(["--help"])
        self.assertTrue(result.cli_options.get("help"))

    def test_help_short(self):
        """Test -h flag."""
        result = self.parser.parse(["-h"])
        self.assertTrue(result.cli_options.get("help"))

    def test_lang_flag(self):
        """Test --lang flag."""
        result = self.parser.parse(["--lang"])
        self.assertTrue(result.cli_options.get("lang"))

    def test_lang_short(self):
        """Test -l flag."""
        result = self.parser.parse(["-l"])
        self.assertTrue(result.cli_options.get("lang"))

    def test_rules_flag(self):
        """Test --rules flag."""
        result = self.parser.parse(["--rules"])
        self.assertTrue(result.cli_options.get("rules"))

    def test_rules_short(self):
        """Test -r flag."""
        result = self.parser.parse(["-r"])
        self.assertTrue(result.cli_options.get("rules"))

    def test_commands_flag(self):
        """Test --commands flag."""
        result = self.parser.parse(["--commands"])
        self.assertTrue(result.cli_options.get("commands"))

    def test_commands_short(self):
        """Test -c flag."""
        result = self.parser.parse(["-c"])
        self.assertTrue(result.cli_options.get("commands"))

    def test_addons_flag(self):
        """Test --addons flag."""
        result = self.parser.parse(["--addons"])
        self.assertTrue(result.cli_options.get("addons"))

    def test_addons_short(self):
        """Test -a flag."""
        result = self.parser.parse(["-a"])
        self.assertTrue(result.cli_options.get("addons"))

    def test_language_option(self):
        """Test -language option with value."""
        result = self.parser.parse(["-language", "en"])
        self.assertEqual(result.cli_options.get("language"), "en")
        self.assertEqual(result.language_selector, "en")

    def test_language_selector_single_hyphen(self):
        """Test language selector with single hyphen (e.g., -en)."""
        result = self.parser.parse(["-en"])
        self.assertEqual(result.cli_options.get("lang_selector"), "en")
        self.assertEqual(result.language_selector, "en")

    def test_help_command(self):
        """Test help command."""
        result = self.parser.parse(["help"])
        self.assertEqual(result.command, "help")

    def test_help_command_with_target(self):
        """Test help command with target."""
        result = self.parser.parse(["help", "image"])
        self.assertEqual(result.command, "help")
        self.assertEqual(result.positional_args, ["image"])

    def test_help_command_with_language(self):
        """Test help command with language selector."""
        result = self.parser.parse(["help", "image", "-en"])
        self.assertEqual(result.command, "help")
        self.assertEqual(result.positional_args, ["image"])
        self.assertEqual(result.cli_options.get("lang_selector"), "en")

    def test_help_command_list_langs(self):
        """Test help command with -lang to list languages."""
        result = self.parser.parse(["help", "image", "-lang"])
        self.assertEqual(result.command, "help")
        self.assertTrue(result.cli_options.get("lang"))

    def test_addon_identification(self):
        """Test addon identification."""
        result = self.parser.parse(["image"])
        self.assertEqual(result.addon_identifier, "image")

    def test_addon_with_args(self):
        """Test addon with arguments."""
        result = self.parser.parse(["image", "convert", "file.png"])
        self.assertEqual(result.addon_identifier, "image")
        self.assertEqual(result.addon_args, ["convert", "file.png"])

    def test_addon_with_double_hyphen_args(self):
        """Test addon with double-hyphen arguments."""
        result = self.parser.parse(["image", "--width", "128"])
        self.assertEqual(result.addon_identifier, "image")
        self.assertEqual(result.addon_args, ["--width", "128"])

    def test_addon_with_cli_option_after(self):
        """Test addon with CLI option after identification (-lang)."""
        result = self.parser.parse(["image", "-lang"])
        self.assertEqual(result.addon_identifier, "image")
        self.assertEqual(result.addon_args, ["-lang"])

    def test_unknown_command(self):
        """Test unknown command is treated as potential addon identifier (legacy behavior)."""
        result = self.parser.parse(["nonexistent"])
        self.assertFalse(result.has_errors())
        self.assertEqual(result.command, "nonexistent")
        self.assertIsNone(result.addon_identifier)

    def test_unknown_option_before_addon(self):
        """Test unknown option before addon produces error."""
        result = self.parser.parse(["--unknown-option"])
        self.assertTrue(result.has_errors())
        self.assertEqual(result.get_first_error().category, "option")

    def test_language_option_missing_value(self):
        """Test -language without value produces error."""
        result = self.parser.parse(["-language"])
        self.assertTrue(result.has_errors())
        self.assertEqual(result.get_first_error().category, "argument")


if __name__ == "__main__":
    unittest.main()