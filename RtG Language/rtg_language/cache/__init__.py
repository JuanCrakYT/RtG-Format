"""Cache system for RtG-Language - .rtgcache file."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Optional
from pathlib import Path
import json
import hashlib
import time

from ..compiler import CompileResult
from ..diagnostics import (
    DiagnosticCollector,
    Codes,
    Severity,
    make_diagnostic,
)


CACHE_VERSION = 1
CACHE_FORMAT_VERSION = 1


@dataclass
class CacheMetadata:
    """Cache file metadata."""
    version: int
    format_version: int
    compiler_version: str
    source_hash: str
    schema_hash: Optional[str]
    timestamp: float
    source_file: str


@dataclass
class CacheEntry:
    """Cached compilation result."""
    metadata: CacheMetadata
    resolved_file: dict  # Serialized ResolvedFile
    build: list  # Serialized RtG-Format build array


class Cache:
    """Manages .rtgcache file for a project."""

    def __init__(self, cache_path: Path, compiler_version: str = "0.1.0"):
        self.cache_path = cache_path
        self.compiler_version = compiler_version
        self.diagnostics = DiagnosticCollector()

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _compute_file_hash(self, path: Path) -> str:
        """Compute hash of file content."""
        with path.open('r', encoding='utf-8') as f:
            return self._compute_hash(f.read())

    def is_valid(self, source_file: Path, schema_file: Optional[Path] = None) -> bool:
        """Check if cache is valid for given source and schema."""
        if not self.cache_path.exists():
            return False

        try:
            with self.cache_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self.diagnostics.add(make_diagnostic(
                Codes.CACHE_CORRUPT,
                f"Failed to read cache: {e}",
                Severity.WARNING,
            ))
            return False

        # Validate cache format version
        metadata = data.get("metadata", {})
        if metadata.get("format_version") != CACHE_FORMAT_VERSION:
            return False

        if metadata.get("version") != CACHE_VERSION:
            return False

        # Check compiler version
        if metadata.get("compiler_version") != self.compiler_version:
            return False

        # Check source hash
        source_hash = self._compute_file_hash(source_file)
        if metadata.get("source_hash") != source_hash:
            return False

        # Check schema hash if provided
        if schema_file and schema_file.exists():
            schema_hash = self._compute_file_hash(schema_file)
            if metadata.get("schema_hash") != schema_hash:
                return False
        elif metadata.get("schema_hash"):
            # Schema was used before but not now
            return False

        return True

    def load(self, source_file: Path, schema_file: Optional[Path] = None) -> Optional[CompileResult]:
        """Load cached compilation result."""
        if not self.is_valid(source_file, schema_file):
            return None

        try:
            with self.cache_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        build = data.get("build", [])
        # We don't fully reconstruct ResolvedFile, just return the build
        result = CompileResult(build=build, diagnostics=DiagnosticCollector())
        return result

    def save(self, source_file: Path, schema_file: Optional[Path], result: CompileResult) -> bool:
        """Save compilation result to cache."""
        try:
            source_hash = self._compute_file_hash(source_file)
            schema_hash = None
            if schema_file and schema_file.exists():
                schema_hash = self._compute_file_hash(schema_file)

            metadata = CacheMetadata(
                version=CACHE_VERSION,
                format_version=CACHE_FORMAT_VERSION,
                compiler_version=self.compiler_version,
                source_hash=source_hash,
                schema_hash=schema_hash,
                timestamp=time.time(),
                source_file=str(source_file),
            )

            entry = CacheEntry(
                metadata=metadata,
                resolved_file={},  # Not storing full resolved file for now
                build=result.build,
            )

            # Write atomically
            temp_path = self.cache_path.with_suffix('.tmp')
            with temp_path.open('w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, ensure_ascii=False, indent=2)

            temp_path.replace(self.cache_path)
            return True

        except Exception as e:
            self.diagnostics.add(make_diagnostic(
                Codes.CACHE_CORRUPT,
                f"Failed to write cache: {e}",
                Severity.WARNING,
            ))
            return False

    def invalidate(self) -> None:
        """Remove cache file."""
        if self.cache_path.exists():
            try:
                self.cache_path.unlink()
            except OSError:
                pass