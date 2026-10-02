"""Tests for RtG-Language cache."""

import pytest
import tempfile
import os
from pathlib import Path

from rtg_language import compile_file, CompileOptions
from rtg_language.cache import Cache


def test_cache_basic():
    """Test basic cache functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        
        # First compilation - no cache
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=True,
        )
        result1 = compile_file(source_file, options)
        assert result1.success
        assert not result1.cache_used
        
        # Second compilation - should use cache
        result2 = compile_file(source_file, options)
        assert result2.success
        assert result2.cache_used
        assert result1.build == result2.build


def test_cache_invalidation_on_source_change():
    """Test cache is invalidated when source changes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=True,
        )
        
        # First compilation
        result1 = compile_file(source_file, options)
        assert result1.success
        assert not result1.cache_used
        
        # Modify source
        source_file.write_text('rtg "2.0"; object "Car" { instance "Wheel" as wheel; }', encoding="utf-8")
        
        # Should not use cache
        result2 = compile_file(source_file, options)
        assert result2.success
        assert not result2.cache_used
        assert result1.build != result2.build


def test_cache_invalidation_on_schema_change():
    """Test cache is invalidated when schema changes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; schema { source: "schema.json"; } object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        # Schema file in same directory as source file (new behavior)
        schema_file = tmpdir / "schema.json"
        schema_file.write_text('{"version": "1.0", "types": []}', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=True,
        )
        
        # First compilation
        result1 = compile_file(source_file, options)
        assert result1.success
        assert not result1.cache_used
        
        # Modify schema
        schema_file.write_text('{"version": "2.0", "types": []}', encoding="utf-8")
        
        # Should not use cache
        result2 = compile_file(source_file, options)
        assert result2.success
        assert not result2.cache_used


def test_cache_no_cache_option():
    """Test --no-cache disables cache."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=False,
        )
        
        result1 = compile_file(source_file, options)
        assert result1.success
        assert not result1.cache_used
        
        result2 = compile_file(source_file, options)
        assert result2.success
        assert not result2.cache_used


def test_cache_corrupt_handling():
    """Test handling of corrupt cache file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        cache_file = cache_dir / ".rtgcache"
        cache_file.write_text("invalid json", encoding="utf-8")
        
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=True,
        )
        
        # Should not crash, just recompile
        result = compile_file(source_file, options)
        assert result.success
        assert not result.cache_used


def test_cache_atomic_write():
    """Test cache is written atomically."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        source_file = tmpdir / "test.rtg"
        source_file.write_text('rtg "2.0"; object "Car" { instance "Chassis" as chassis; }', encoding="utf-8")
        
        cache_dir = tmpdir / "cache"
        cache_dir.mkdir()
        
        options = CompileOptions(
            cache_dir=cache_dir,
            use_cache=True,
        )
        
        result = compile_file(source_file, options)
        assert result.success
        
        cache_file = cache_dir / ".rtgcache"
        assert cache_file.exists()
        
        # Verify it's valid JSON with new project cache format
        import json
        with cache_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "format_version" in data
        assert "version" in data
        assert "compiler_version" in data
        assert "entries" in data
        assert data["format_version"] == 1
        assert len(data["entries"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])