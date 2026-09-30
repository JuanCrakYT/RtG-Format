#!/usr/bin/env python3
"""Tests for configuration loading and validation."""

import sys
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import load_config, CliConfig, load_assets_json, get_config, exc_invalid_configuration


class TestConfiguration(unittest.TestCase):
    """Test configuration loading."""

    def test_load_default_config(self):
        """Test loading default configuration."""
        config = get_config()
        self.assertIsInstance(config, CliConfig)
        self.assertEqual(config.version, "RtG-CLI v1.2.0")

    def test_config_has_required_fields(self):
        """Test config has all required fields."""
        config = get_config()
        self.assertIsNotNone(config.version)
        self.assertIsNotNone(config.language_names)
        self.assertIsNotNone(config.help_paths)
        self.assertIsNotNone(config.rules_paths)
        self.assertIsNotNone(config.void_text)
        self.assertIsNotNone(config.addons)
        self.assertIsNotNone(config.internal)

    def test_config_language_names(self):
        """Test config has 19 language names."""
        config = get_config()
        self.assertEqual(len(config.language_names), 19)

    def test_config_addons(self):
        """Test config has expected addons."""
        config = get_config()
        self.assertIn("image", config.addons)
        self.assertIn("preview", config.addons)
        self.assertIn("test-addon", config.addons)

    def test_config_internal_commands(self):
        """Test config has internal commands."""
        config = get_config()
        self.assertIn("help", config.internal.command_list)
        self.assertIn("--version", config.internal.command_list)
        self.assertIn("--addons", config.internal.command_list)

    def test_asset_paths_resolved(self):
        """Test asset paths are resolved."""
        config = get_config()
        self.assertTrue(config.asset_paths.base_dir.exists())

    def test_get_available_languages(self):
        """Test getting all available languages."""
        config = get_config()
        langs = config.get_available_languages()
        self.assertEqual(len(langs), 19)

    def test_get_default_rules_language(self):
        """Test default rules language."""
        config = get_config()
        default = config.get_default_rules_language()
        self.assertEqual(default, "es")

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json")
            temp_path = f.name

        try:
            with self.assertRaises(Exception) as cm:
                load_assets_json(temp_path)
            self.assertIn("Invalid JSON", str(cm.exception))
        finally:
            Path(temp_path).unlink()

    def test_load_missing_required_field(self):
        """Test loading config with missing required field."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([{"version": "1.0"}], f)
            temp_path = f.name

        try:
            with self.assertRaises(Exception) as cm:
                load_config(temp_path)
            self.assertIn("Missing required field", str(cm.exception))
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()