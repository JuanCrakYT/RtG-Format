"""Structured diagnostics for RtG-Language."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from pathlib import Path


class Severity(str, Enum):
    """Diagnostic severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class SourceLocation:
    """Source code location."""
    file: str
    line: int
    column: int
    offset: int
    length: int = 1

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Diagnostic:
    """Structured diagnostic message."""
    code: str
    message: str
    severity: Severity
    location: Optional[SourceLocation] = None
    hints: tuple[str, ...] = field(default_factory=tuple)
    context: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        loc = f"{self.location}: " if self.location else ""
        hints_str = "\n  ".join(self.hints) if self.hints else ""
        hint_prefix = f"\n  {hints_str}" if hints_str else ""
        return f"[{self.severity.value.upper()}] {self.code}: {loc}{self.message}{hint_prefix}"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
            "location": {
                "file": self.location.file,
                "line": self.location.line,
                "column": self.location.column,
                "offset": self.location.offset,
                "length": self.location.length,
            } if self.location else None,
            "hints": list(self.hints),
            "context": self.context,
        }


class DiagnosticCollector:
    """Collects diagnostics during compilation phases."""

    def __init__(self):
        self.diagnostics: list[Diagnostic] = []

    def add(self, diagnostic: Diagnostic) -> None:
        self.diagnostics.append(diagnostic)

    def add_error(self, code: str, message: str, location: Optional[SourceLocation] = None, hints: tuple[str, ...] = (), context: Optional[dict[str, Any]] = None) -> None:
        self.add(Diagnostic(code, message, Severity.ERROR, location, hints, context or {}))

    def add_warning(self, code: str, message: str, location: Optional[SourceLocation] = None, hints: tuple[str, ...] = (), context: Optional[dict[str, Any]] = None) -> None:
        self.add(Diagnostic(code, message, Severity.WARNING, location, hints, context or {}))

    def add_info(self, code: str, message: str, location: Optional[SourceLocation] = None, hints: tuple[str, ...] = (), context: Optional[dict[str, Any]] = None) -> None:
        self.add(Diagnostic(code, message, Severity.INFO, location, hints, context or {}))

    def has_errors(self) -> bool:
        return any(d.severity == Severity.ERROR for d in self.diagnostics)

    def get_errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == Severity.ERROR]

    def clear(self) -> None:
        self.diagnostics.clear()

    def __len__(self) -> int:
        return len(self.diagnostics)

    def __iter__(self):
        return iter(self.diagnostics)


# Standard diagnostic codes
class Codes:
    # Lexer errors
    LEX_INVALID_CHAR = "LEX001"
    LEX_UNTERMINATED_STRING = "LEX002"
    LEX_INVALID_NUMBER = "LEX003"
    LEX_UNTERMINATED_COMMENT = "LEX004"

    # Parser errors
    PARSE_UNEXPECTED_TOKEN = "PARSE001"
    PARSE_EXPECTED_TOKEN = "PARSE002"
    PARSE_INVALID_SYNTAX = "PARSE003"
    PARSE_DUPLICATE_IDENTIFIER = "PARSE004"
    PARSE_UNEXPECTED_EOF = "PARSE005"
    PARSE_INVALID_UUID = "PARSE006"
    PARSE_INVALID_CFRAME = "PARSE007"

    # Resolver errors
    RESOLVE_UNDEFINED_IDENTIFIER = "RES001"
    RESOLVE_DUPLICATE_DEFINITION = "RES002"
    RESOLVE_INVALID_CONNECTION = "RES003"
    RESOLVE_INVALID_LOCALTYPE = "RES004"
    RESOLVE_INVALID_POINT = "RES005"
    RESOLVE_MISSING_SCHEMA = "RES006"
    RESOLVE_SCHEMA_VALIDATION = "RES007"
    RESOLVE_CYCLIC_REFERENCE = "RES008"
    RESOLVE_UNDEFINED_UUID = "RES009"

    # Compiler errors
    COMPILE_INVALID_OUTPUT = "COMP001"
    COMPILE_INDEX_OUT_OF_RANGE = "COMP002"
    COMPILE_MISSING_REQUIRED_FIELD = "COMP003"
    COMPILE_PROPERTY_CONFLICT = "COMP004"

    # Schema errors
    SCHEMA_MISSING = "SCHEMA001"
    SCHEMA_INVALID = "SCHEMA002"
    SCHEMA_VERSION_MISMATCH = "SCHEMA003"
    SCHEMA_UNKNOWN_TYPE = "SCHEMA004"

    # Cache errors
    CACHE_CORRUPT = "CACHE001"
    CACHE_VERSION_MISMATCH = "CACHE002"
    CACHE_SCHEMA_MISMATCH = "CACHE003"
    CACHE_SOURCE_MISMATCH = "CACHE004"

    # IO errors
    IO_FILE_NOT_FOUND = "IO001"
    IO_PERMISSION_DENIED = "IO002"
    IO_INVALID_ENCODING = "IO003"


def make_diagnostic(
    code: str,
    message: str,
    severity: Severity = Severity.ERROR,
    location: Optional[SourceLocation] = None,
    hints: tuple[str, ...] = (),
    **context: Any,
) -> Diagnostic:
    """Factory function for creating diagnostics."""
    return Diagnostic(code, message, severity, location, hints, context)