#!/usr/bin/env python3
"""Tests for language management."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rtg_cli.configuration import get_config
from rtg_cli.languages import (
    get_language_manager,
    ALL_LANGUAGES,
    RTG_AI_LANGUAGES,
    ADDITIONAL_LANGUAGES,
    LanguageAvailability,
)


class TestLanguages(unittest.TestCase):
    """Test language management."""

    @classmethod
    def setUpClass(cls):
        cls.config = get_config()
        cls.lang_manager = get_language_manager(cls.config)

    def test_all_languages_count(self):
        """Test total language count is 19."""
        self.assertEqual(len(ALL_LANGUAGES), 19)

    def test_rtg_ai_languages_count(self):
        """Test RtG-AI languages count is 12."""
        self.assertEqual(len(RTG_AI_LANGUAGES), 12)

    def test_additional_languages_count(self):
        """Test additional languages count is 7."""
        self.assertEqual(len(ADDITIONAL_LANGUAGES), 7)

    def test_rtg_ai_languages_present(self):
        """Test all RtG-AI languages are present."""
        expected = {"es", "en", "pt", "de", "fr", "ru", "zh", "ja", "ko", "it", "tr", "pl"}
        self.assertEqual(set(RTG_AI_LANGUAGES.keys()), expected)

    def test_additional_languages_present(self):
        """Test additional languages are present."""
        expected = {"zh-TW", "ar", "hi", "nl", "sv", "cs", "hu"}
        self.assertEqual(set(ADDITIONAL_LANGUAGES.keys()), expected)

    def test_get_language_name(self):
        """Test getting language names."""
        self.assertEqual(self.lang_manager.get_language_name("es"), "Español")
        self.assertEqual(self.lang_manager.get_language_name("en"), "English")
        self.assertEqual(self.lang_manager.get_language_name("zh-TW"), "繁體中文")
        self.assertEqual(self.lang_manager.get_language_name("unknown"), "unknown")

    def test_get_all_language_codes(self):
        """Test getting all language codes."""
        codes = self.lang_manager.get_all_language_codes()
        self.assertEqual(len(codes), 19)
        self.assertIn("es", codes)
        self.assertIn("zh-TW", codes)

    def test_get_supported_language_codes(self):
        """Test getting supported language codes."""
        codes = self.lang_manager.get_supported_language_codes()
        self.assertIsInstance(codes, list)
        self.assertGreater(len(codes), 0)

    def test_availability_computed(self):
        """Test availability is computed for all languages."""
        avail = self.lang_manager.get_availability()
        self.assertEqual(len(avail), 19)
        for code in ALL_LANGUAGES:
            self.assertIn(code, avail)
            self.assertIsInstance(avail[code], LanguageAvailability)

    def test_is_language_available(self):
        """Test language availability check."""
        self.assertTrue(self.lang_manager.is_language_available("es"))
        self.assertTrue(self.lang_manager.is_language_available("en"))
        self.assertFalse(self.lang_manager.is_language_available("xx"))

    def test_is_language_available_category(self):
        """Test language availability for specific category."""
        self.assertTrue(self.lang_manager.is_language_available("es", "rules"))
        self.assertTrue(self.lang_manager.is_language_available("en", "help"))

    def test_validate_language_valid(self):
        """Test validation passes for valid language."""
        diag = self.lang_manager.validate_language("es")
        self.assertIsNone(diag)

    def test_validate_language_invalid(self):
        """Test validation fails for invalid language."""
        diag = self.lang_manager.validate_language("xx")
        self.assertIsNotNone(diag)
        self.assertEqual(diag.category, "language")

    def test_validate_language_category_unavailable(self):
        """Test validation fails for unavailable category."""
        diag = self.lang_manager.validate_language("es", "nonexistent")
        self.assertIsNotNone(diag)

    def test_default_language_rules(self):
        """Test default language for rules."""
        default = self.lang_manager.get_default_language("rules")
        self.assertEqual(default, "es")  # First in rules object

    def test_format_language_list(self):
        """Test language list formatting."""
        lines = self.lang_manager.format_language_list()
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

    def test_format_language_list_category(self):
        """Test language list formatting with category filter."""
        lines = self.lang_manager.format_language_list("rules")
        self.assertIsInstance(lines, list)


if __name__ == "__main__":
    unittest.main()