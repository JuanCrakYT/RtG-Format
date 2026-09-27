"""RtG-CLI — Command-line interface for RtG-Format ecosystem."""

from .application import Application, main
from .arguments import ArgumentParser, ParsedCommandLine
from .configuration import CliConfig, load_config, get_config
from .diagnostics import Diagnostic, DiagnosticHandler, ExitCode, ErrorCategory
from .addons import AddonMetadata, AddonRegistry, ProgramCommandInterface
from .languages import LanguageManager, LanguageAvailability, ALL_LANGUAGES, RTG_AI_LANGUAGES
from .execution import AddonExecutor, InternalCommandExecutor, ExecutionResult
from .help import HelpSystem
from .version import VersionManager, VersionInfo

__version__ = "1.2.0"
__all__ = [
    "Application",
    "main",
    "ArgumentParser",
    "ParsedCommandLine",
    "CliConfig",
    "load_config",
    "get_config",
    "Diagnostic",
    "DiagnosticHandler",
    "ExitCode",
    "ErrorCategory",
    "AddonMetadata",
    "AddonRegistry",
    "ProgramCommandInterface",
    "LanguageManager",
    "LanguageAvailability",
    "ALL_LANGUAGES",
    "RTG_AI_LANGUAGES",
    "AddonExecutor",
    "InternalCommandExecutor",
    "ExecutionResult",
    "HelpSystem",
    "VersionManager",
    "VersionInfo",
]