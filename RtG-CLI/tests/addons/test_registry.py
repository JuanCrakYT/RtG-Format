#!/usr/bin/env python3
"""Tests for addon discovery and registry."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import get_config
from rtg_cli.languages import get_language_manager
from rtg_cli.addons import create_addon_registry, AddonMetadata


class TestAddonRegistry(unittest.TestCase):
    """Test addon registry functionality."""

    @classmethod
    def setUpClass(cls):
        cls.config = get_config()
        cls.lang_manager = get_language_manager(cls.config)
        cls.registry = create_addon_registry(cls.config, cls.lang_manager)

    def test_registry_contains_image(self):
        """Test image addon is registered."""
        addon = self.registry.get("image")
        self.assertIsNotNone(addon)
        self.assertEqual(addon.identifier, "image")
        self.assertEqual(addon.name, "RtG Image")

    def test_registry_contains_preview(self):
        """Test preview addon is registered."""
        addon = self.registry.get("preview")
        self.assertIsNotNone(addon)
        self.assertEqual(addon.identifier, "preview")
        self.assertEqual(addon.name, "RtG Preview")

    def test_registry_contains_test_addon(self):
        """Test test-addon is registered."""
        addon = self.registry.get("test-addon")
        self.assertIsNotNone(addon)
        self.assertEqual(addon.identifier, "test-addon")
        self.assertEqual(addon.name, "RtG Test Addon")

    def test_documented_addons_only(self):
        """Test documented addons filter."""
        documented = self.registry.get_documented()
        self.assertIn("image", documented)
        self.assertIn("preview", documented)
        self.assertIn("test-addon", documented)

    def test_addon_has_languages(self):
        """Test addons have languages defined."""
        for addon in self.registry.get_all().values():
            self.assertIsInstance(addon.languages, list)
            self.assertGreater(len(addon.languages), 0)

    def test_addon_has_version(self):
        """Test addons have version info."""
        for addon in self.registry.get_all().values():
            self.assertIsNotNone(addon.version)

    def test_addon_has_creators(self):
        """Test addons have creators."""
        for addon in self.registry.get_all().values():
            self.assertIsInstance(addon.creators, dict)
            self.assertGreater(len(addon.creators), 0)

    def test_addon_has_program_commands(self):
        """Test addons have program command paths."""
        for addon in self.registry.get_all().values():
            self.assertIsInstance(addon.program_command_paths, list)
            self.assertGreater(len(addon.program_command_paths), 0)

    def test_validate_existing_addon(self):
        """Test validation passes for existing addon."""
        diag = self.registry.validate_addon("image")
        self.assertIsNone(diag)

    def test_validate_nonexistent_addon(self):
        """Test validation fails for nonexistent addon."""
        diag = self.registry.validate_addon("nonexistent")
        self.assertIsNotNone(diag)
        self.assertEqual(diag.category, "addon")
        self.assertEqual(diag.exit_code, 5)


if __name__ == "__main__":
    unittest.main()