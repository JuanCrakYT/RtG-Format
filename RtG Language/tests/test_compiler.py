"""Tests for RtG-Language compiler."""

import pytest
from rtg_language import compile_string


def test_compiler_basic():
    """Test basic compilation."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    assert len(build) == 1
    entry = build[0]
    assert entry[0] == "Chassis"
    assert entry[1] == []  # no connections
    assert entry[2] == []  # no properties


def test_compiler_properties():
    """Test properties in output."""
    source = '''
    rtg "2.0";
    object "Car" {
        properties { "RGB": [255, 0, 0]; "Visible": true; }
        instance "Chassis" as chassis;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    entry = build[0]
    props = entry[2]
    assert props["RGB"] == [255, 0, 0]
    assert props["Visible"] is True


def test_compiler_empty_properties_as_array():
    """Test empty properties become empty array."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    entry = build[0]
    assert entry[2] == []


def test_compiler_connections():
    """Test connections in output."""
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
    # chassis is first (index 1), wheel is second (index 2)
    wheel_entry = next(e for e in build if e[0] == "Wheel")
    connections = wheel_entry[1]
    assert len(connections) == 1
    conn = connections[0]
    assert conn[0] == "1"  # localType as string
    assert conn[1] == "1"  # point ID
    assert conn[2] == 1    # parent index (1-based)


def test_compiler_connection_uuid():
    """Test connection with UUID point."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        attachment "{12345678-1234-1234-1234-123456789012}" on chassis {
            partName: "Test";
            cframe: [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
        };
        instance "Wheel" as wheel;
        connect wheel -> chassis {
            localType: 1;
            point: uuid("{12345678-1234-1234-1234-123456789012}");
        }
    }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    wheel_entry = next(e for e in build if e[0] == "Wheel")
    connections = wheel_entry[1]
    conn = connections[0]
    assert conn[1] == "{12345678-1234-1234-1234-123456789012}"  # UUID


def test_compiler_attachment():
    """Test attachment in output."""
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


def test_compiler_deterministic():
    """Test compilation is deterministic."""
    source = '''
    rtg "2.0";
    object "Car" {
        instance "Chassis" as chassis;
        instance "Wheel" as wheel;
        instance "Seat" as seat;
    }
    '''
    result1 = compile_string(source, "test.rtg")
    result2 = compile_string(source, "test.rtg")
    
    assert result1.success
    assert result2.success
    assert result1.build == result2.build


def test_compiler_1_based_indices():
    """Test indices are 1-based."""
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
    wheel_entry = next(e for e in build if e[0] == "Wheel")
    conn = wheel_entry[1][0]
    # Parent index should be 1 (chassis is first)
    assert conn[2] == 1


def test_compiler_multiple_objects():
    """Test compilation with multiple object sections."""
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
    assert len(build) == 2
    # Order: chassis (1), seat (2)
    assert build[0][0] == "Chassis"
    assert build[1][0] == "Seat"
    seat_entry = build[1]
    conn = seat_entry[1][0]
    assert conn[2] == 1  # chassis index


def test_compiler_complex_example():
    """Test compilation of complex example similar to complete.rtg."""
    source = '''
    rtg "2.0";
    
    object "CarBody" {
        instance "Chassis" as chassis;
    }
    
    object "Seats" {
        properties { "RGB": [255, 0, 0]; "Visible": true; }
        instance "Seat" as driverSeat;
        instance "Seat" as passengerSeat {
            properties { "RGB": [0, 0, 255]; }
        };
    }
    
    object "Wheels" {
        instance "Wheel" as frontLeft;
        instance "Wheel" as frontRight;
        instance "Wheel" as backLeft;
        instance "Wheel" as backRight;
        connect frontLeft -> chassis { localType: 1; point: 1; }
        connect frontRight -> chassis { localType: 1; point: 2; }
        connect backLeft -> chassis { localType: 1; point: 3; }
        connect backRight -> chassis { localType: 1; point: 4; }
    }
    
    output { file: "car.json"; }
    '''
    result = compile_string(source, "test.rtg")
    
    assert result.success
    build = result.build
    assert len(build) == 7  # 1 chassis + 2 seats + 4 wheels
    
    # Check global properties applied to seats
    driver_seat = next(e for e in build if e[0] == "Seat" and e[2].get("RGB") == [255, 0, 0])
    passenger_seat = next(e for e in build if e[0] == "Seat" and e[2].get("RGB") == [0, 0, 255])
    assert driver_seat is not None
    assert passenger_seat is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])