"""Schema loading and validation for RtG-Language."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import json


@dataclass
class SchemaType:
    """Schema definition for an RtG block type."""
    name: str
    local_types: list[int] = field(default_factory=list)
    connection_points: dict[int, str] = field(default_factory=dict)  # point_id -> name
    properties: dict[str, str] = field(default_factory=dict)  # prop_name -> type
    required_properties: list[str] = field(default_factory=list)
    can_host_attachments: bool = True


@dataclass
class Schema:
    """RtG-Language schema container."""
    version: str
    types: dict[str, SchemaType] = field(default_factory=dict)

    def get_type(self, name: str) -> Optional[SchemaType]:
        return self.types.get(name)

    def validate_local_type(self, type_name: str, local_type: int) -> bool:
        stype = self.get_type(type_name)
        if not stype:
            return True  # Unknown type, allow
        if not stype.local_types:
            return True  # No restrictions
        return local_type in stype.local_types

    def validate_connection_point(self, type_name: str, point: Union[int, str]) -> bool:
        if isinstance(point, str):
            # UUID - always valid if it exists in attachments
            return True
        stype = self.get_type(type_name)
        if not stype or not stype.connection_points:
            return True  # No restrictions
        return point in stype.connection_points

    def get_property_type(self, type_name: str, prop: str) -> Optional[str]:
        stype = self.get_type(type_name)
        if not stype:
            return None
        return stype.properties.get(prop)


def load_schema(path: Path) -> Schema:
    """Load schema from JSON file."""
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    schema = Schema(version=data.get("version", "1.0"))

    for type_data in data.get("types", []):
        stype = SchemaType(
            name=type_data["name"],
            local_types=type_data.get("localTypes", []),
            connection_points=type_data.get("connectionPoints", {}),
            properties=type_data.get("properties", {}),
            required_properties=type_data.get("requiredProperties", []),
            can_host_attachments=type_data.get("canHostAttachments", True),
        )
        schema.types[stype.name] = stype

    return schema


def create_default_schema() -> Schema:
    """Create a default schema with known RtG types."""
    schema = Schema(version="1.0")

    # Known types from RtG-Format specification
    known_types = {
        "Base": {"localTypes": [3], "points": {1: "Left", 2: "Right", 4: "Front", 5: "Top", 6: "Bottom"}},
        "Part": {"localTypes": [1], "points": {1: "Center", 2: "Top", 3: "Bottom", 4: "Front", 5: "Back", 6: "Left", 7: "Right"}},
        "Chassis": {"localTypes": [], "points": {1: "Wheel_FL", 2: "PassengerSteering", 3: "Hood", 4: "Wheel_FR", 5: "Wheel_BL", 6: "Wheel_BR", 7: "Roof"}},
        "Wheel": {"localTypes": [1, 2], "points": {1: "ChassisMount"}},
        "Servo": {"localTypes": [1], "points": {2: "RotationAxis", 3: "Side_Red", 4: "Side_Blue"}},
        "Connector": {"localTypes": [5], "points": {1: "MountPoint"}},
        "Sprite": {"localTypes": [1], "points": {}},
        "Splitter_1": {"localTypes": [3], "points": {}},
        "Splitter_2": {"localTypes": [3], "points": {}},
        "Splitter_3": {"localTypes": [3], "points": {}},
        "Splitter_4": {"localTypes": [1], "points": {}},
        "Wire": {"localTypes": [3], "points": {2: "Left", 4: "Right"}},
        "Rope": {"localTypes": [1], "points": {}},
        "Seat": {"localTypes": [1, 2], "points": {}},
        "Gyro": {"localTypes": [1], "points": {}},
    }

    for name, info in known_types.items():
        stype = SchemaType(
            name=name,
            local_types=info["localTypes"],
            connection_points=info["points"],
            properties={},  # Open properties dictionary
        )
        schema.types[name] = stype

    return schema