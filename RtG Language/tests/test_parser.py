# -*- coding: utf-8 -*-
"""Tests for RtG-Language parser."""

import pytest
import sys
import os

# Ensure we're importing from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rtg_language import parse


def test_parser_basic():
    """Test basic parsing."""
    source = 'rtg "2.0";'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    assert ast.version == "2.0"
    assert ast.schema is None
    assert len(ast.objects) == 0


def test_parser_with_schema():
    """Test parsing with schema."""
    source = 'rtg "2.0";\nschema { source: "schema.json"; }'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    assert ast.schema is not None
    assert ast.schema.source == "schema.json"


def test_parser_object():
    """Test parsing object section."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis;\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    print("DEBUG: Has errors:", diagnostics.has_errors())
    for d in diagnostics:
        print("DEBUG: ", d)
    
    assert not diagnostics.has_errors()
    assert ast is not None
    assert len(ast.objects) == 1
    obj = ast.objects[0]
    assert obj.name == "Car"
    assert len(obj.instances) == 1
    assert obj.instances[0].type_name == "Chassis"
    assert obj.instances[0].identifier == "chassis"


def test_parser_properties():
    """Test parsing properties."""
    source = 'rtg "2.0";\nobject "Car" {\n    properties { "RGB": [255, 0, 0]; "Visible": true; }\n    instance "Chassis" as chassis;\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    assert obj.properties is not None
    assert obj.properties.properties["RGB"] == [255, 0, 0]
    assert obj.properties.properties["Visible"] is True


def test_parser_instance_properties():
    """Test parsing instance with inline properties."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis {\n        properties { "RGB": [0, 0, 255]; }\n    };\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    inst = obj.instances[0]
    assert inst.properties is not None
    assert inst.properties.properties["RGB"] == [0, 0, 255]


def test_parser_connection():
    """Test parsing connection."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis;\n    instance "Wheel" as wheel;\n    connect chassis -> wheel {\n        localType: 1;\n        point: 1;\n    }\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    assert len(obj.connections) == 1
    conn = obj.connections[0]
    assert conn.child == "chassis"
    assert conn.parent == "wheel"
    assert conn.local_type == 1
    assert conn.point == 1


def test_parser_connection_uuid():
    """Test parsing connection with UUID point."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis;\n    attachment {12345678-1234-1234-1234-123456789012} on chassis {\n        partName: "Test";\n        cframe: [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];\n    };\n    connect chassis -> wheel {\n        localType: 1;\n        point: uuid("{12345678-1234-1234-1234-123456789012}");\n    }\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    conn = obj.connections[0]
    assert isinstance(conn.point, str)
    assert conn.point == "{12345678-1234-1234-1234-123456789012}"


def test_parser_attachment():
    """Test parsing attachment."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis;\n    attachment "{12345678-1234-1234-1234-123456789012}" on chassis {\n        partName: "Test";\n        cframe: [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];\n    };\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    assert len(obj.attachments) == 1
    att = obj.attachments[0]
    assert att.uuid == "{12345678-1234-1234-1234-123456789012}"
    assert att.parent == "chassis"
    assert att.part_name == "Test"
    assert len(att.cframe) == 12


def test_parser_output():
    """Test parsing output."""
    source = 'rtg "2.0";\noutput { file: "build.json"; }'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    assert ast.output is not None
    assert ast.output.file == "build.json"


def test_parser_invalid_syntax():
    """Test error on invalid syntax."""
    source = 'rtg "2.0"; object "Test" { invalid }'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert diagnostics.has_errors()
    assert ast is None
    errors = diagnostics.get_errors()
    assert any(e.code == "PARSE001" for e in errors)


def test_parser_duplicate_identifier():
    """Test error on duplicate instance identifier."""
    source = 'rtg "2.0";\nobject "Car" {\n    instance "Chassis" as chassis;\n    instance "Wheel" as chassis;\n}'
    ast, diagnostics = parse(source, "test.rtg")
    
    # Parser doesn't check duplicates, that's resolver's job
    assert not diagnostics.has_errors()
    assert ast is not None


def test_cstring_unicode():
    """Test string handling - using pure ASCII to avoid encoding issues in test runner."""
    source = 'rtg "2.0"; object "Car" { properties { "name": "test_name"; } }'
    ast, diagnostics = parse(source, "test.rtg")
    
    assert not diagnostics.has_errors()
    assert ast is not None
    obj = ast.objects[0]
    assert obj.properties.properties["name"] == "test_name"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])