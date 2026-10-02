"""Tests for RtG-Language resolver."""

import pytest
from rtg_language import compile_string


def test_resolver_basic():
    """Test basic resolving."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    assert result.resolved is not None
    assert len(result.resolved.instance_order) == 1
    inst = result.resolved.instance_order[0]
    assert inst.identifier == "chassis"
    assert inst.type_name == "Chassis"
    assert inst.index == 1


def test_resolver_global_properties():
    """Test global properties are applied."""
    source = '''
    rtg "2.0";
    object "Car" {
        properties { "RGB": [255, 0, 0]; "Visible": true; }
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    # Both instances should have global properties
    for entry in build:
        props = entry[2]
        assert props["RGB"] == [255, 0, 0]
        assert props["Visible"] is True


def test_resolver_instance_overrides_global():
    """Test instance properties override global."""
    source = '''
    rtg "2.0";
    object "Car" {
        properties { "RGB": [255, 0, 0]; }
        instance "Chassis" as chassis;
        instance "Wheel" as wheel {
            properties { "RGB": [0, 0, 255]; }
        };
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    # Find chassis (index 1)
    chassis_entry = next(e for e in build if e[0] == "Chassis")
    assert chassis_entry[2]["RGB"] == [255, 0, 0]  # global
    
    # Find wheel (index 2)
    wheel_entry = next(e for e in build if e[0] == "Wheel")
    assert wheel_entry[2]["RGB"] == [0, 0, 255]  # overridden


def test_resolver_connection():
    """Test connection resolution."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
        connect wheel -> chassis {
            localType: 1;
            point: 1;
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    # Wheel should have connection to chassis
    wheel_entry = next(e for e in build if e[0] == "Wheel")
    connections = wheel_entry[1]
    assert len(connections) == 1
    conn = connections[0]
    assert conn[0] == "1"  # localType as string
    assert conn[1] == "1"  # point ID
    assert conn[2] == 1    # parent index (chassis is 1)


def test_resolver_undefined_reference():
    """Test error on undefined reference."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        connect wheel -> chassis {
            localType: 1;
            point: 1;
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    errors = result.diagnostics.get_errors()
    assert any(e.code == "RES001" for e in errors)


def test_resolver_duplicate_identifier():
    """Test error on duplicate identifier."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as chassis;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    errors = result.diagnostics.get_errors()
    assert any(e.code == "RES002" for e in errors)


def test_resolver_invalid_point():
    """Test error on invalid point (0 or negative)."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
        connect wheel -> chassis {
            localType: 1;
            point: 0;
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    errors = result.diagnostics.get_errors()
    assert any(e.code == "RES005" for e in errors)


def test_resolver_negative_point():
    """Test error on negative point."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
        connect wheel -> chassis {
            localType: 1;
            point: -1;
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    errors = result.diagnostics.get_errors()
    assert any(e.code == "RES005" for e in errors)


def test_resolver_attachment():
    """Test attachment resolution."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        attachment "{12345678-1234-1234-1234-123456789012}" on chassis {
            partName: "Test";
            cframe: [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
        };
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    chassis_entry = next(e for e in build if e[0] == "Chassis")
    props = chassis_entry[2]
    assert "EphemeralAttachments" in props
    att = props["EphemeralAttachments"]["{12345678-1234-1234-1234-123456789012}"]
    assert att["partName"] == "Test"
    assert len(att["cframe"]) == 12


def test_resolver_undefined_attachment():
    """Test error on undefined attachment UUID."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
        connect wheel -> chassis {
            localType: 1;
            point: uuid("{12345678-1234-1234-1234-123456789012}");
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert not result.success
    errors = result.diagnostics.get_errors()
    assert any(e.code == "RES009" for e in errors)


def test_resolver_cross_object_connection():
    """Test connection between objects."""
    source = '''
    rtg "2.0";
    object "CarBody" {
        instance "Chassis" as chassis;
    }
    object "Seats" {
        instance "Seat" as seat;
        connect seat -> chassis {
            localType: 1;
            point: 1;
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    # chassis is index 1, seat is index 2
    seat_entry = next(e for e in build if e[0] == "Seat")
    connections = seat_entry[1]
    assert len(connections) == 1
    conn = connections[0]
    assert conn[2] == 1  # chassis index


if __name__ == "__main__":
    pytest.main([__file__, "-v"])