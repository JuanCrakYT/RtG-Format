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
    """Cached compilation result for a single source file."""
    metadata: CacheMetadata
    resolved_file: dict  # Serialized ResolvedFile
    build: list  # Serialized RtG-Format build array


@dataclass
class ProjectCache:
    """Project-level cache containing entries for multiple source files."""
    format_version: int
    version: int
    compiler_version: str
    entries: dict[str, CacheEntry]  # source_hash -> CacheEntry


class Cache:
    """Manages .rtgcache file for a project, supporting multiple source files."""

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

    def _load_project_cache(self) -> Optional[ProjectCache]:
        """Load the entire project cache."""
        if not self.cache_path.exists():
            return None

        try:
            with self.cache_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self.diagnostics.add(make_diagnostic(
                Codes.CACHE_CORRUPT,
                f"Failed to read cache: {e}",
                Severity.WARNING,
            ))
            return None

        # Validate cache format version
        if data.get("format_version") != CACHE_FORMAT_VERSION:
            return None

        if data.get("version") != CACHE_VERSION:
            return None

        # Check compiler version
        if data.get("compiler_version") != self.compiler_version:
            return None

        # Reconstruct entries
        entries = {}
        for source_hash, entry_data in data.get("entries", {}).items():
            metadata = CacheMetadata(**entry_data["metadata"])
            entry = CacheEntry(
                metadata=metadata,
                resolved_file=entry_data.get("resolved_file", {}),
                build=entry_data.get("build", []),
            )
            entries[source_hash] = entry

        return ProjectCache(
            format_version=data["format_version"],
            version=data["version"],
            compiler_version=data["compiler_version"],
            entries=entries,
        )

    def _save_project_cache(self, project_cache: ProjectCache) -> bool:
        """Save the entire project cache atomically."""
        try:
            # Convert entries to serializable format
            entries_data = {}
            for source_hash, entry in project_cache.entries.items():
                entries_data[source_hash] = {
                    "metadata": asdict(entry.metadata),
                    "resolved_file": entry.resolved_file,
                    "build": entry.build,
                }

            data = {
                "format_version": project_cache.format_version,
                "version": project_cache.version,
                "compiler_version": project_cache.compiler_version,
                "entries": entries_data,
            }

            # Write atomically
            temp_path = self.cache_path.with_suffix('.tmp')
            with temp_path.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            temp_path.replace(self.cache_path)
            return True

        except Exception as e:
            self.diagnostics.add(make_diagnostic(
                Codes.CACHE_CORRUPT,
                f"Failed to write cache: {e}",
                Severity.WARNING,
            ))
            return False

    def is_valid(self, source_file: Path, schema_file: Optional[Path] = None) -> bool:
        """Check if cache has a valid entry for given source and schema."""
        project_cache = self._load_project_cache()
        if not project_cache:
            return False

        source_hash = self._compute_file_hash(source_file)
        entry = project_cache.entries.get(source_hash)
        if not entry:
            return False

        metadata = entry.metadata

        # Check source hash
        if metadata.source_hash != source_hash:
            return False

        # Check schema hash if provided
        if schema_file and schema_file.exists():
            schema_hash = self._compute_file_hash(schema_file)
            if metadata.schema_hash != schema_hash:
                return False
        elif metadata.schema_hash:
            # Schema was used before but not now
            return False

        return True

    def load(self, source_file: Path, schema_file: Optional[Path] = None) -> Optional[CompileResult]:
        """Load cached compilation result for a source file."""
        project_cache = self._load_project_cache()
        if not project_cache:
            return None

        source_hash = self._compute_file_hash(source_file)
        entry = project_cache.entries.get(source_hash)
        if not entry:
            return None

        # Validate schema hash
        if schema_file and schema_file.exists():
            schema_hash = self._compute_file_hash(schema_file)
            if entry.metadata.schema_hash != schema_hash:
                return None
        elif entry.metadata.schema_hash:
            # Schema was used before but not now
            return None

        build = entry.build
        result = CompileResult(build=build, diagnostics=DiagnosticCollector())
        return result

    def save(self, source_file: Path, schema_file: Optional[Path], result: CompileResult) -> bool:
        """Save compilation result to cache."""
        try:
            project_cache = self._load_project_cache()
            if not project_cache:
                # Create new project cache
                project_cache = ProjectCache(
                    format_version=CACHE_FORMAT_VERSION,
                    version=CACHE_VERSION,
                    compiler_version=self.compiler_version,
                    entries={},
                )

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

            project_cache.entries[source_hash] = entry

            return self._save_project_cache(project_cache)

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

    def invalidate_source(self, source_file: Path) -> bool:
        """Remove a specific source file from cache."""
        project_cache = self._load_project_cache()
        if not project_cache:
            return False

        source_hash = self._compute_file_hash(source_file)
        if source_hash in project_cache.entries:
            del project_cache.entries[source_hash]
            return self._save_project_cache(project_cache)
        return False