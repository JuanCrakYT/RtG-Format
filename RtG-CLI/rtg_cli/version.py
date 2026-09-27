"""Version management for RtG-CLI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .configuration import CliConfig
from .languages import LanguageManager


@dataclass(frozen=True)
class VersionInfo:
    """Version information for RtG-CLI and its components."""

    cli_version: str
    cli_version_date: str
    cli_version_content: dict[str, str]
    addon_versions: dict[str, dict[str, Any]]


class VersionManager:
    """Manages version information display."""

    def __init__(self, config: CliConfig, lang_manager: LanguageManager):
        self.config = config
        self.lang_manager = lang_manager

    def get_version_info(self) -> VersionInfo:
        """Get complete version information."""
        addon_versions = {}
        for addon_id, addon in self.config.addons.items():
            addon_versions[addon_id] = {
                "name": addon.name,
                "version": addon.version,
                "version_date": addon.version_date,
                "version_content": addon.version_content,
            }

        return VersionInfo(
            cli_version=self.config.version,
            cli_version_date=self.config.version_date,
            cli_version_content=self.config.version_content,
            addon_versions=addon_versions,
        )

    def show_cli_version(self) -> None:
        """Show RtG-CLI version with multi-language content."""
        print(self.config.version)
        if self.config.version_content:
            print()
            for lang, content in self.config.version_content.items():
                name = self.lang_manager.get_language_name(lang)
                print(f"--- {name} ({lang}) ---")
                print(content, end="")
                print()

    def show_all_versions(self) -> None:
        """Show versions for CLI and all addons."""
        self.show_cli_version()
        print()

        for addon_id, addon in self.config.addons.items():
            if addon.version or addon.version_content:
                print(f"Addon: {addon.name} ({addon_id})")
                if addon.version:
                    print(f"  Version: {addon.version}")
                if addon.version_date:
                    print(f"  Date: {addon.version_date}")
                if addon.version_content:
                    print("  Content:")
                    for lang, content in addon.version_content.items():
                        name = self.lang_manager.get_language_name(lang)
                        print(f"    --- {name} ({lang}) ---")
                        for line in content.strip().split("\n"):
                            print(f"    {line}")
                print()

    def show_addon_version(self, addon_id: str) -> bool:
        """Show version for a specific addon. Returns True if found."""
        addon = self.config.addons.get(addon_id)
        if not addon:
            return False

        print(f"{addon.name} ({addon_id})")
        if addon.version:
            print(f"Version: {addon.version}")
        if addon.version_date:
            print(f"Date: {addon.version_date}")
        if addon.version_content:
            print("Content:")
            for lang, content in addon.version_content.items():
                name = self.lang_manager.get_language_name(lang)
                print(f"  --- {name} ({lang}) ---")
                for line in content.strip().split("\n"):
                    print(f"  {line}")
        return True


def create_version_manager(config: CliConfig, lang_manager: LanguageManager) -> VersionManager:
    return VersionManager(config, lang_manager)


__all__ = [
    "VersionInfo",
    "VersionManager",
    "create_version_manager",
]