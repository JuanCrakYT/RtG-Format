"""Integration tests for .rtg -> RtG-Format compilation."""

import pytest
from pathlib import Path
from rtg_language import compile_file, CompileOptions


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def test_example_basic():
    """Test basic.rtg compiles successfully."""
    source = EXAMPLES_DIR / "basic.rtg"
    assert source.exists()
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result.success
    assert result.build is not None
    assert len(result.build) == 1
    assert result.build[0][0] == "Chassis"


def test_example_connections():
    """Test connections.rtg compiles successfully."""
    source = EXAMPLES_DIR / "connections.rtg"
    assert source.exists()
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result.success
    assert result.build is not None
    assert len(result.build) >= 2  # At least chassis and wheel


def test_example_properties():
    """Test properties.rtg compiles successfully."""
    source = EXAMPLES_DIR / "properties.rtg"
    assert source.exists()
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result.success
    assert result.build is not None
    # Check global properties applied
    for entry in result.build:
        props = entry[2]
        assert "RGB" in props
        assert "Visible" in props


def test_example_attachments():
    """Test attachments.rtg compiles successfully."""
    source = EXAMPLES_DIR / "attachments.rtg"
    assert source.exists()
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result.success
    assert result.build is not None
    # Check attachment in output
    chassis_entry = next(e for e in result.build if e[0] == "Chassis")
    props = chassis_entry[2]
    assert "EphemeralAttachments" in props


def test_example_complete():
    """Test complete.rtg compiles successfully."""
    source = EXAMPLES_DIR / "complete.rtg"
    assert source.exists()
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result.success
    assert result.build is not None
    assert len(result.build) == 3  # 1 chassis + 2 seats


def test_roundtrip_consistency():
    """Test that compiling same file twice gives same result."""
    source = EXAMPLES_DIR / "complete.rtg"
    
    result1 = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    result2 = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        use_cache=False,
    ))
    
    assert result1.success
    assert result2.success
    assert result1.build == result2.build


def test_output_file_writing(tmp_path):
    """Test output file is written correctly."""
    source = EXAMPLES_DIR / "basic.rtg"
    output = tmp_path / "output.json"
    
    result = compile_file(source, CompileOptions(
        schema_dir=EXAMPLES_DIR.parent / "schema",
        output_path=output,
        use_cache=False,
    ))
    
    assert result.success
    assert output.exists()
    
    import json
    with output.open('r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert data == result.build


def test_invalid_example_fails():
    """Test that invalid syntax fails appropriately."""
    source = "rtg \"2.0\"; object \"Test\" { invalid syntax }"
    
    from rtg_language import compile_string
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    assert result.diagnostics.has_errors()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])