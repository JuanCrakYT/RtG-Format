"""Abstract Syntax Tree nodes for RtG-Language 2.0."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Union
from pathlib import Path

from ..diagnostics import SourceLocation


@dataclass(frozen=True, kw_only=True)
class ASTNode:
    """Base class for all AST nodes."""
    location: SourceLocation = field(default_factory=lambda: SourceLocation("<unknown>", 0, 0, 0))


@dataclass(frozen=True, kw_only=True)
class File(ASTNode):
    """Root AST node for a .rtg file."""
    version: str
    schema: Optional["SchemaDecl"] = None
    objects: tuple["ObjectDecl", ...] = field(default_factory=tuple)
    output: Optional["OutputDecl"] = None


@dataclass(frozen=True, kw_only=True)
class SchemaDecl(ASTNode):
    """Schema declaration."""
    source: str


@dataclass(frozen=True, kw_only=True)
class ObjectDecl(ASTNode):
    """Object section declaration."""
    name: str
    properties: Optional["PropertiesDecl"] = None
    attachments: tuple["AttachmentDecl", ...] = field(default_factory=tuple)
    instances: tuple["InstanceDecl", ...] = field(default_factory=tuple)
    connections: tuple["ConnectionDecl", ...] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class PropertiesDecl(ASTNode):
    """Properties block declaration."""
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class AttachmentDecl(ASTNode):
    """Attachment declaration."""
    uuid: str
    parent: str  # identifier of the instance this attachment is on
    part_name: str
    cframe: tuple[float, ...]


@dataclass(frozen=True, kw_only=True)
class InstanceDecl(ASTNode):
    """Instance declaration."""
    type_name: str  # RtG block type (e.g., "Chassis", "Wheel")
    identifier: str  # Language identifier (e.g., "chassis", "frontLeft")
    properties: Optional[PropertiesDecl] = None


@dataclass(frozen=True, kw_only=True)
class ConnectionDecl(ASTNode):
    """Connection declaration."""
    child: str  # identifier of child instance
    parent: str  # identifier of parent instance
    local_type: int
    point: Union[int, str]  # integer point ID or UUID string


@dataclass(frozen=True, kw_only=True)
class OutputDecl(ASTNode):
    """Output declaration."""
    file: str
    source: Optional[str] = None  # optional schema source override


# Type aliases for convenience
PointRef = Union[int, str]  # integer point ID or UUID string

# JSON value types
JSONValue = Union[str, int, float, bool, None, list[Any], dict[str, Any]]