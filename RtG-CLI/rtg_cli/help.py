"""Help system for RtG-CLI.

Manages external help files and provides formatted help output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .configuration import CliConfig
from .languages import LanguageManager


class HelpSystem:
    """Manages help content loading and display."""

    def __init__(self, config: CliConfig, lang_manager: LanguageManager):
        self.config = config
        self.lang_manager = lang_manager

    def show_general_help(self, lang: str | None = None) -> None:
        """Show general help text."""
        help_paths = self.config.help_paths
        if not help_paths:
            print("Help not available.")
            return

        langs = list(help_paths.keys())
        target_lang = lang or langs[0]

        if target_lang in help_paths:
            path = self.config.asset_paths.resolve_help(target_lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read help file: {help_paths[target_lang]}")
        else:
            print(f"Language not available for help: {target_lang}")

    def show_command_help(
        self,
        command: str,
        lang: str | None = None,
        list_langs: bool = False,
    ) -> None:
        """Show help for a specific command or addon."""
        internal_help = self.config.internal.help_texts.get(command)

        if internal_help:
            if list_langs:
                print("Available languages:")
                print()
                for l in internal_help:
                    print(f"  {l}")
                return

            if lang and lang in internal_help:
                print(internal_help[lang], end="")
            else:
                first = next(iter(internal_help))
                print(internal_help[first], end="")
            return

        # Check if it's an addon
        addon = self.config.addons.get(command)
        if addon:
            if list_langs:
                self._show_addon_languages(addon)
                return

            # Try internal help first
            if command in self.config.internal.help_texts:
                internal_help = self.config.internal.help_texts[command]
                if lang and lang in internal_help:
                    print(internal_help[lang], end="")
                else:
                    first = next(iter(internal_help))
                    print(internal_help[first], end="")
            else:
                print(f"No internal help available for '{command}'.")
                print(f"Addon: {addon.name}")
            return

        print(f"Unknown command: {command}\n")
        self.show_void(lang)

    def show_addon_info(self, addon_id: str) -> None:
        """Show addon metadata and info frame."""
        addon = self.config.addons.get(addon_id)
        if not addon:
            print(f"Unknown command: {addon_id}")
            print()
            self.show_void()
            return

        content_lines = []

        print(f"\n{addon_id}\n")
        print("-" * len(addon_id))

        if addon.creators:
            print("\nCreators:")
            print()
            for creator, notes in addon.creators.items():
                for note in notes:
                    line = f"    {note} ({creator})"
                    print(line)
                    content_lines.append(line)

        if addon.languages:
            print("\nLanguages:")
            print()
            for lang in addon.languages:
                name = self.lang_manager.get_language_name(lang)
                line = f"    {name} | {lang}"
                print(line)
                content_lines.append(line)

        print("\nVersion:")
        print()
        print("    Content:")
        if addon.version:
            line = f"        VERSION {addon.version}"
        else:
            line = "        [No version information]"
        print(line)
        content_lines.append(line)

        content_lines.append(" Run Output")
        frame_width = max(len(s) for s in content_lines)

        print()
        print("|" + "-" * frame_width + "|")
        print("|" + " Run Output".ljust(frame_width) + "|")
        print("|" + "-" * frame_width + "|")

    def show_addons_list(self) -> None:
        """List documented addons."""
        addons_with_help = {
            k: v for k, v in self.config.addons.items()
            if v.languages or k in self.config.internal.help_texts
        }
        if not addons_with_help:
            print("No addons with documentation available.")
            return

        print("Available addons (with documentation):")
        print()
        for key, addon in addons_with_help.items():
            print(f"  {key}  |  {addon.name}")

    def show_commands_list(self) -> None:
        """List internal commands."""
        print("RtG-CLI internal commands:")
        print()
        for cmd in self.config.internal.command_list:
            print(f"  {cmd}")

    def show_void(self, lang: str | None = None) -> None:
        """Show startup/void text."""
        if lang:
            void_lang = self.config.void_language_paths
            if lang in void_lang:
                path = self.config.asset_paths.resolve_void(lang)
                if path:
                    print(path, end="")
                else:
                    print(f"Language not available: {lang}\n")
                    print(self.config.void_text, end="")
            else:
                print(f"Language not available: {lang}\n")
                print(self.config.void_text, end="")
        else:
            print(self.config.void_text, end="")

    def show_version(self) -> None:
        """Show version with multi-language content."""
        print(self.config.version)
        if self.config.version_content:
            print()
            for lang, content in self.config.version_content.items():
                name = self.lang_manager.get_language_name(lang)
                print(f"--- {name} ({lang}) ---")
                print(content, end="")
                print()

    def show_rules(self, lang: str | None = None) -> None:
        """Show rules file."""
        rules = self.config.rules_paths
        if not rules:
            print("Rules not available.")
            return

        if lang and lang in rules:
            path = self.config.asset_paths.resolve_rules(lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read rules file: {rules[lang]}")
        else:
            default_lang = self.config.get_default_rules_language()
            path = self.config.asset_paths.resolve_rules(default_lang)
            if path and path.exists():
                print(path.read_text(encoding="utf-8"), end="")
            else:
                print(f"Could not read rules file: {rules[default_lang]}")

    def show_cli_languages(self) -> None:
        """Show languages available for RtG-CLI organized by category."""
        lang_names = self.config.language_names
        void_langs = sorted(self.config.void_language_paths.keys())
        help_langs = sorted(self.config.help_paths.keys())
        rules_langs = sorted(self.config.rules_paths.keys())
        version_langs = sorted(self.config.version_content.keys())

        def fmt(codes):
            return [f"  {lang_names.get(c, c)} | {c}" for c in codes]

        categories = [
            ("Version", version_langs),
            ("Rules", rules_langs),
            ("Help", help_langs),
        ]

        if void_langs:
            categories.append(("Void", void_langs))

        print("Available languages for RtG-CLI:")
        print()

        for category, codes in categories:
            if codes:
                print(f"  [{category}]")
                for line in fmt(codes):
                    print(line)
                print()

        for addon_id, addon in self.config.addons.items():
            addon_langs = sorted(addon.languages)
            if addon_langs:
                print(f"  [Addons / {addon_id}] ({addon.name})")
                for line in fmt(addon_langs):
                    print(line)
                print()

    def _show_addon_languages(self, addon) -> None:
        print("Available languages:")
        print()
        for lang in addon.languages:
            name = self.lang_manager.get_language_name(lang)
            print(f"  {name} | {lang}")


def create_help_system(config: CliConfig, lang_manager: LanguageManager) -> HelpSystem:
    return HelpSystem(config, lang_manager)


__all__ = [
    "HelpSystem",
    "create_help_system",
]