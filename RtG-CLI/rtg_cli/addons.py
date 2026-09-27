"""Addon discovery, registry, and metadata management."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .configuration import AddonConfig, CliConfig
from .diagnostics import Diagnostic, err_addon_not_found, err_addon_unavailable, err_internal
from .languages import LanguageManager


@dataclass(frozen=True)
class AddonMetadata:
    """Complete metadata for an addon."""

    identifier: str
    name: str
    languages: list[str]
    version: str | None
    version_date: str | None
    version_content: dict[str, str]
    creators: dict[str, list[str]]
    program_command_paths: list[str]
    has_documentation: bool
    internal_help: dict[str, str] | None = None


class ProgramCommandInterface(ABC):
    """Abstract interface for program command execution."""

    @abstractmethod
    def execute(self, args: list[str]) -> int:
        """Execute the program with arguments. Returns exit code."""
        pass

    @abstractmethod
    def get_commands(self) -> list[str]:
        """Return list of available program commands."""
        pass

    @abstractmethod
    def get_help(self, command: str, lang: str | None) -> str | None:
        """Return help text for a command in given language."""
        pass


class PythonProgramInterface(ProgramCommandInterface):
    """Program interface for Python modules."""

    def __init__(self, module_path: Path):
        self.module_path = module_path
        self._module = None
        self._load_module()

    def _load_module(self) -> None:
        try:
            spec = importlib.util.spec_from_file_location("addon_program", self.module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self._module = module
        except Exception as e:
            raise err_internal(f"Failed to load Python module {self.module_path}: {e}")

    def execute(self, args: list[str]) -> int:
        if self._module and hasattr(self._module, "execute"):
            return self._module.execute(args)
        raise err_internal(f"Module {self.module_path} has no execute function")

    def get_commands(self) -> list[str]:
        if self._module and hasattr(self._module, "get_commands"):
            return self._module.get_commands()
        return []

    def get_help(self, command: str, lang: str | None) -> str | None:
        if self._module and hasattr(self._module, "get_help"):
            return self._module.get_help(command, lang)
        return None


class JavaScriptProgramInterface(ProgramCommandInterface):
    """Program interface for JavaScript (Node.js) files."""

    def __init__(self, script_path: Path, cwd: Path):
        self.script_path = script_path
        self.cwd = cwd

    def _run_node(self, args: list[str]) -> tuple[int, str, str]:
        try:
            result = subprocess.run(
                ["node", str(self.script_path)] + args,
                capture_output=True,
                text=True,
                cwd=self.cwd,
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            raise err_internal("Node.js not found. Required for JavaScript addons.")
        except Exception as e:
            raise err_internal(f"Error executing JavaScript: {e}")

    def execute(self, args: list[str]) -> int:
        code, stdout, stderr = self._run_node(args)
        if stdout:
            print(stdout, end="")
        if stderr:
            print(stderr, end="", file=sys.stderr)
        return code

    def get_commands(self) -> list[str]:
        code, stdout, stderr = self._run_node(["--commands"])
        if code == 0 and stdout.strip():
            return [line.strip() for line in stdout.strip().split("\n") if line.strip()]
        return []

    def get_help(self, command: str, lang: str | None) -> str | None:
        args = ["--help", command]
        if lang:
            args.extend(["--lang", lang])
        code, stdout, stderr = self._run_node(args)
        if code == 0 and stdout.strip():
            return stdout
        return None


def create_program_interface(
    addon_config: AddonConfig, base_dir: Path
) -> ProgramCommandInterface | None:
    """Create program interface from addon configuration."""
    for cmd_path in addon_config.program_commands:
        full_path = (base_dir / cmd_path).resolve()
        if not full_path.exists():
            continue

        if full_path.suffix == ".py":
            return PythonProgramInterface(full_path)
        elif full_path.suffix == ".js":
            return JavaScriptProgramInterface(full_path, base_dir)

    return None


class AddonRegistry:
    """Registry of discovered and validated addons."""

    def __init__(self, config: CliConfig, language_manager: LanguageManager):
        self.config = config
        self.lang_manager = language_manager
        self._addons: dict[str, AddonMetadata] = {}
        self._interfaces: dict[str, ProgramCommandInterface] = {}
        self._build_registry()

    def _build_registry(self) -> None:
        base_dir = self.config.asset_paths.base_dir
        for addon_id, addon_config in self.config.addons.items():
            internal_help = self.config.internal.help_texts.get(addon_id)
            has_docs = bool(addon_config.languages) or bool(internal_help)

            metadata = AddonMetadata(
                identifier=addon_id,
                name=addon_config.name,
                languages=addon_config.languages,
                version=addon_config.version,
                version_date=addon_config.version_date,
                version_content=addon_config.version_content,
                creators=addon_config.creators,
                program_command_paths=addon_config.program_commands,
                has_documentation=has_docs,
                internal_help=internal_help,
            )
            self._addons[addon_id] = metadata

            # Try to load program interface
            interface = create_program_interface(addon_config, base_dir)
            if interface:
                self._interfaces[addon_id] = interface

    def get_all(self) -> dict[str, AddonMetadata]:
        """Get all registered addons (including undocumented)."""
        return dict(self._addons)

    def get_documented(self) -> dict[str, AddonMetadata]:
        """Get only addons with user-visible documentation."""
        return {k: v for k, v in self._addons.items() if v.has_documentation}

    def get(self, identifier: str) -> AddonMetadata | None:
        """Get addon by identifier."""
        return self._addons.get(identifier)

    def get_interface(self, identifier: str) -> ProgramCommandInterface | None:
        """Get program command interface for addon."""
        return self._interfaces.get(identifier)

    def has_interface(self, identifier: str) -> bool:
        return identifier in self._interfaces

    def validate_addon(self, identifier: str) -> Diagnostic | None:
        """Validate that an addon exists and is available."""
        if identifier not in self._addons:
            return err_addon_not_found(identifier)
        addon = self._addons[identifier]
        if not addon.has_documentation:
            return err_addon_unavailable(identifier, "No documentation or languages available")
        return None


def create_addon_registry(config: CliConfig, language_manager: LanguageManager) -> AddonRegistry:
    """Factory for AddonRegistry."""
    return AddonRegistry(config, language_manager)


__all__ = [
    "AddonMetadata",
    "ProgramCommandInterface",
    "PythonProgramInterface",
    "JavaScriptProgramInterface",
    "AddonRegistry",
    "create_program_interface",
    "create_addon_registry",
]