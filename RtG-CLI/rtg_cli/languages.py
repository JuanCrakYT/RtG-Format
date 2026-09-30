"""Language management for RtG-CLI.

RtG-CLI supports multiple languages across different categories:
- CLI language (startup/void text)
- Help language
- Rules language
- Version-content language
- Addon languages

The 19 supported languages consist of:
- 12 existing languages from RtG-AI: es, en, pt, de, fr, ru, zh, ja, ko, it, tr, pl
- 7 additional languages: zh-TW, ar, hi, nl, sv, cs, hu
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .configuration import CliConfig
from .diagnostics import Diagnostic, err_invalid_language


# RtG-AI existing languages (12)
RTG_AI_LANGUAGES: dict[str, str] = {
    "es": "Español",
    "en": "English",
    "pt": "Português",
    "de": "Deutsch",
    "fr": "Français",
    "ru": "Русский",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
    "it": "Italiano",
    "tr": "Türkçe",
    "pl": "Polski",
}

# Additional languages (7) - using ISO/BCP-47 codes
ADDITIONAL_LANGUAGES: dict[str, str] = {
    "zh-TW": "繁體中文",
    "ar": "العربية",
    "hi": "हिन्दी",
    "nl": "Nederlands",
    "sv": "Svenska",
    "cs": "Čeština",
    "hu": "Magyar",
}

# All 19 languages combined
ALL_LANGUAGES: dict[str, str] = {**RTG_AI_LANGUAGES, **ADDITIONAL_LANGUAGES}


@dataclass(frozen=True)
class LanguageAvailability:
    """Availability of a language across different resource categories."""

    code: str
    name: str
    cli: bool = False
    help: bool = False
    rules: bool = False
    void: bool = False
    version_content: bool = False
    addons: dict[str, bool] = field(default_factory=dict)

    @property
    def any(self) -> bool:
        return any(
            [
                self.cli,
                self.help,
                self.rules,
                self.void,
                self.version_content,
                any(self.addons.values()),
            ]
        )

    def categories(self) -> list[str]:
        cats = []
        if self.cli:
            cats.append("CLI")
        if self.help:
            cats.append("Help")
        if self.rules:
            cats.append("Rules")
        if self.void:
            cats.append("Void")
        if self.version_content:
            cats.append("Version")
        for addon, avail in self.addons.items():
            if avail:
                cats.append(f"Addon/{addon}")
        return cats


class LanguageManager:
    """Manages language availability and selection."""

    def __init__(self, config: CliConfig):
        self.config = config
        self._availability_cache: dict[str, LanguageAvailability] | None = None

    def get_language_name(self, code: str) -> str:
        """Get human-readable name for a language code."""
        return self.config.language_names.get(code, ALL_LANGUAGES.get(code, code))

    def get_all_language_codes(self) -> list[str]:
        """Get all known language codes (19 total)."""
        return sorted(ALL_LANGUAGES.keys())

    def get_supported_language_codes(self) -> list[str]:
        """Get language codes that have at least some content available."""
        return [code for code, avail in self.get_availability().items() if avail.any]

    def get_availability(self) -> dict[str, LanguageAvailability]:
        """Compute language availability across all categories."""
        if self._availability_cache is not None:
            return self._availability_cache

        result: dict[str, LanguageAvailability] = {}

        # Initialize all known languages
        for code in self.get_all_language_codes():
            result[code] = LanguageAvailability(code=code, name=self.get_language_name(code))

        # Check CLI languages (language-names)
        for code in self.config.language_names:
            if code in result:
                result[code] = LanguageAvailability(
                    code=code,
                    name=result[code].name,
                    cli=True,
                    help=result[code].help,
                    rules=result[code].rules,
                    void=result[code].void,
                    version_content=result[code].version_content,
                    addons=result[code].addons,
                )

        # Check help
        for code in self.config.help_paths:
            if code in result:
                result[code] = LanguageAvailability(
                    code=code,
                    name=result[code].name,
                    cli=result[code].cli,
                    help=True,
                    rules=result[code].rules,
                    void=result[code].void,
                    version_content=result[code].version_content,
                    addons=result[code].addons,
                )

        # Check rules
        for code in self.config.rules_paths:
            if code in result:
                result[code] = LanguageAvailability(
                    code=code,
                    name=result[code].name,
                    cli=result[code].cli,
                    help=result[code].help,
                    rules=True,
                    void=result[code].void,
                    version_content=result[code].version_content,
                    addons=result[code].addons,
                )

        # Check void-language
        for code in self.config.void_language_paths:
            if code in result:
                result[code] = LanguageAvailability(
                    code=code,
                    name=result[code].name,
                    cli=result[code].cli,
                    help=result[code].help,
                    rules=result[code].rules,
                    void=True,
                    version_content=result[code].version_content,
                    addons=result[code].addons,
                )

        # Check version-content
        for code in self.config.version_content:
            if code in result:
                result[code] = LanguageAvailability(
                    code=code,
                    name=result[code].name,
                    cli=result[code].cli,
                    help=result[code].help,
                    rules=result[code].rules,
                    void=result[code].void,
                    version_content=True,
                    addons=result[code].addons,
                )

        # Check addon languages
        for addon_id, addon in self.config.addons.items():
            for code in addon.languages:
                if code in result:
                    addons = dict(result[code].addons)
                    addons[addon_id] = True
                    result[code] = LanguageAvailability(
                        code=code,
                        name=result[code].name,
                        cli=result[code].cli,
                        help=result[code].help,
                        rules=result[code].rules,
                        void=result[code].void,
                        version_content=result[code].version_content,
                        addons=addons,
                    )

        self._availability_cache = result
        return result

    def is_language_available(self, code: str, category: str | None = None) -> bool:
        """Check if a language is available, optionally for a specific category."""
        avail = self.get_availability().get(code)
        if not avail:
            return False
        if category is None:
            return avail.any
        category = category.lower()
        if category == "cli":
            return avail.cli
        if category == "help":
            return avail.help
        if category == "rules":
            return avail.rules
        if category == "void":
            return avail.void
        if category == "version":
            return avail.version_content
        if category.startswith("addon/"):
            addon_id = category[6:]
            return avail.addons.get(addon_id, False)
        return False

    def validate_language(self, code: str, category: str | None = None) -> Diagnostic | None:
        """Validate a language code, return diagnostic if invalid."""
        if code not in ALL_LANGUAGES:
            return err_invalid_language(code, {"known_languages": self.get_all_language_codes()})
        if category and not self.is_language_available(code, category):
            return err_invalid_language(
                code,
                {"category": category, "available_categories": self.get_availability()[code].categories()},
            )
        return None

    def get_default_language(self, category: str = "rules") -> str:
        """Get default language for a category."""
        if category == "rules":
            return self.config.get_default_rules_language()
        # For other categories, use first available or default
        for code in self.get_all_language_codes():
            if self.is_language_available(code, category):
                return code
        return self.config.default_language

    def format_language_list(self, category: str | None = None) -> list[str]:
        """Format language list for display."""
        lines = []
        for code in self.get_all_language_codes():
            avail = self.get_availability().get(code)
            if not avail:
                continue
            if category and not self.is_language_available(code, category):
                continue
            if not avail.any:
                continue
            cats = avail.categories()
            if cats:
                lines.append(f"  {avail.name} | {code} [{', '.join(cats)}]")
            else:
                lines.append(f"  {avail.name} | {code}")
        return lines


def get_language_manager(config: CliConfig) -> LanguageManager:
    """Factory for LanguageManager."""
    return LanguageManager(config)


__all__ = [
    "RTG_AI_LANGUAGES",
    "ADDITIONAL_LANGUAGES",
    "ALL_LANGUAGES",
    "LanguageAvailability",
    "LanguageManager",
    "get_language_manager",
]