"""Configuration loading and validation for RtG-CLI."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .diagnostics import Diagnostic, err_invalid_configuration, err_file


@dataclass(frozen=True)
class AssetPaths:
    """Resolved absolute paths for asset files."""

    base_dir: Path
    help: dict[str, Path] = field(default_factory=dict)
    rules: dict[str, Path] = field(default_factory=dict)
    void_language: dict[str, Path] = field(default_factory=dict)
    version_content: dict[str, str] = field(default_factory=dict)
    addon_program_commands: dict[str, list[Path]] = field(default_factory=dict)

    def resolve_help(self, lang: str) -> Path | None:
        return self.help.get(lang)

    def resolve_rules(self, lang: str) -> Path | None:
        return self.rules.get(lang)

    def resolve_void(self, lang: str) -> str | None:
        return self.void_language.get(lang)

    def resolve_version_content(self, lang: str) -> str | None:
        return self.version_content.get(lang)

    def resolve_addon_commands(self, addon: str) -> list[Path]:
        return self.addon_program_commands.get(addon, [])


@dataclass(frozen=True)
class AddonConfig:
    """Configuration for a single addon."""

    identifier: str
    name: str
    languages: list[str]
    version: str | None
    version_date: str | None
    version_content: dict[str, str]
    creators: dict[str, list[str]]
    program_commands: list[str]
    raw: dict[str, Any]

    @property
    def has_documentation(self) -> bool:
        return bool(self.languages) or bool(self.raw.get("internal_help"))


@dataclass(frozen=True)
class InternalCommandConfig:
    """Configuration for internal CLI commands."""

    help_texts: dict[str, dict[str, str]] = field(default_factory=dict)
    command_list: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CliConfig:
    """Complete parsed CLI configuration."""

    version: str
    version_date: str
    language_names: dict[str, str]
    default_language: str
    void_text: str
    help_paths: dict[str, str]
    rules_paths: dict[str, str]
    void_language_paths: dict[str, str]
    version_content: dict[str, str]
    addons: dict[str, AddonConfig]
    internal: InternalCommandConfig
    raw: dict[str, Any]
    asset_paths: AssetPaths

    def get_available_languages(self) -> list[str]:
        """Get all language codes available across all resources."""
        langs = set()
        langs.update(self.language_names.keys())
        langs.update(self.help_paths.keys())
        langs.update(self.rules_paths.keys())
        langs.update(self.void_language_paths.keys())
        langs.update(self.version_content.keys())
        for addon in self.addons.values():
            langs.update(addon.languages)
        return sorted(langs)

    def get_default_rules_language(self) -> str:
        """Get the default language for rules (first key in rules)."""
        if self.rules_paths:
            return next(iter(self.rules_paths))
        return self.default_language


def load_assets_json(path: str | Path) -> dict[str, Any]:
    """Load and parse assets.json."""
    path = Path(path)
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except OSError as e:
        raise err_file(f"Cannot read {path}: {e}")
    except json.JSONDecodeError as e:
        raise err_invalid_configuration(f"Invalid JSON in {path}: {e}")
    if not isinstance(data, list) or not data:
        raise err_invalid_configuration("assets.json must be a non-empty array")
    return data[0]


def resolve_relative_paths(base_dir: Path, relative_paths: dict[str, str]) -> dict[str, Path]:
    """Resolve relative paths to absolute paths."""
    result = {}
    for key, rel_path in relative_paths.items():
        result[key] = (base_dir / rel_path).resolve()
    return result


def parse_addon_config(base_dir: Path, identifier: str, raw: dict[str, Any]) -> AddonConfig:
    """Parse a single addon configuration."""
    program_commands = raw.get("program commands", [])
    resolved_commands = []
    for cmd in program_commands:
        resolved_commands.append((base_dir / cmd).resolve())

    return AddonConfig(
        identifier=identifier,
        name=raw.get("name", identifier),
        languages=list(raw.get("lang", [])),
        version=raw.get("version"),
        version_date=raw.get("version-date"),
        version_content=raw.get("version-content", {}),
        creators=raw.get("creators", {}),
        program_commands=program_commands,
        raw=raw,
    )


def parse_internal_config(raw: dict[str, Any]) -> InternalCommandConfig:
    """Parse internal commands configuration."""
    internal = raw.get("internal", {})
    help_texts = internal.get("help", {})
    command_list = raw.get("internal-list", [])
    return InternalCommandConfig(help_texts=help_texts, command_list=command_list)


def build_asset_paths(base_dir: Path, raw: dict[str, Any]) -> AssetPaths:
    """Build resolved asset paths."""
    return AssetPaths(
        base_dir=base_dir,
        help=resolve_relative_paths(base_dir, raw.get("help", {})),
        rules=resolve_relative_paths(base_dir, raw.get("rules", {})),
        void_language=resolve_relative_paths(base_dir, raw.get("void-language", {})),
        version_content=raw.get("version-content", {}),
        addon_program_commands={
            addon_id: [(base_dir / cmd).resolve() for cmd in addon.get("program commands", [])]
            for addon_id, addon in raw.get("addons", {}).items()
        },
    )


def load_config(assets_path: str | Path) -> CliConfig:
    """Load and parse complete CLI configuration."""
    base_dir = Path(assets_path).parent.resolve()
    raw = load_assets_json(assets_path)

    # Required fields
    required = ["version", "language-names", "help", "rules", "void"]
    for field_name in required:
        if field_name not in raw:
            raise err_invalid_configuration(f"Missing required field: {field_name}")

    language_names = raw["language-names"]
    if not language_names:
        raise err_invalid_configuration("language-names cannot be empty")

    default_language = next(iter(language_names))

    addons = {}
    for addon_id, addon_raw in raw.get("addons", {}).items():
        addons[addon_id] = parse_addon_config(base_dir, addon_id, addon_raw)

    internal = parse_internal_config(raw)
    asset_paths = build_asset_paths(base_dir, raw)

    return CliConfig(
        version=raw["version"],
        version_date=raw.get("version-date", ""),
        language_names=language_names,
        default_language=default_language,
        void_text=raw["void"],
        help_paths=raw.get("help", {}),
        rules_paths=raw.get("rules", {}),
        void_language_paths=raw.get("void-language", {}),
        version_content=raw.get("version-content", {}),
        addons=addons,
        internal=internal,
        raw=raw,
        asset_paths=asset_paths,
    )


def get_config() -> CliConfig:
    """Load configuration from default location."""
    base_dir = Path(__file__).parent.parent.parent.resolve()
    assets_path = base_dir / "assets.json"
    return load_config(assets_path)


__all__ = [
    "AssetPaths",
    "AddonConfig",
    "InternalCommandConfig",
    "CliConfig",
    "load_config",
    "get_config",
    "load_assets_json",
    "parse_addon_config",
    "parse_internal_config",
    "build_asset_paths",
]