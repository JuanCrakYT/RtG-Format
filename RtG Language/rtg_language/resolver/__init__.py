"""Resolver for RtG-Language 2.0 - semantic validation and reference resolution."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path
import json
import hashlib

from ..parser.ast import (
    File, SchemaDecl, ObjectDecl, PropertiesDecl,
    AttachmentDecl, InstanceDecl, ConnectionDecl, OutputDecl,
)
from ..diagnostics import (
    DiagnosticCollector,
    Codes,
    SourceLocation,
    Severity,
    make_diagnostic,
)
from ..lexer import Token, TokenType
from ..schema import Schema, load_schema


@dataclass
class ResolvedInstance:
    """Fully resolved instance with all references."""
    type_name: str
    identifier: str
    properties: dict[str, Any]
    global_properties: dict[str, Any]
    object_name: str
    index: int  # 1-based index in final output


@dataclass
class ResolvedAttachment:
    """Fully resolved attachment."""
    uuid: str
    parent_instance: str  # identifier of parent instance
    part_name: str
    cframe: tuple[float, ...]


@dataclass
class ResolvedConnection:
    """Fully resolved connection."""
    child: ResolvedInstance
    parent: ResolvedInstance
    local_type: int
    point: Union[int, str]  # point ID or UUID


@dataclass
class ResolvedObject:
    """Fully resolved object section."""
    name: str
    global_properties: dict[str, Any]
    instances: list[ResolvedInstance]
    attachments: list[ResolvedAttachment]
    connections: list[ResolvedConnection]


@dataclass
class ResolvedFile:
    """Fully resolved file ready for compilation."""
    version: str
    schema: Optional[Schema]
    objects: list[ResolvedObject]
    output: Optional[OutputDecl]
    instance_order: list[ResolvedInstance]  # All instances in creation order


class Resolver:
    """Semantic resolver for RtG-Language AST."""

    def __init__(self, schema_dir: Optional[Path] = None):
        self.schema_dir = schema_dir or Path.cwd()
        self.diagnostics = DiagnosticCollector()
        self._instance_map: dict[str, ResolvedInstance] = {}  # identifier -> instance
        self._object_instances: dict[str, list[ResolvedInstance]] = {}  # object_name -> instances
        self._attachment_map: dict[str, ResolvedAttachment] = {}  # uuid -> attachment
        self._current_object: Optional[ResolvedObject] = None
        self._instance_counter = 0

    def resolve(self, ast: File, schema: Optional[Schema] = None) -> tuple[Optional[ResolvedFile], DiagnosticCollector]:
        """Resolve AST to semantic model."""
        self.diagnostics = DiagnosticCollector()
        self._instance_map = {}
        self._object_instances = {}
        self._attachment_map = {}
        self._instance_counter = 0

        # Use provided schema or load if declared
        if schema is None and ast.schema:
            schema = self._load_schema(ast.schema.source)

        # First pass: collect all instances across all objects
        for obj in ast.objects:
            self._collect_instances(obj)

        # Second pass: resolve attachments
        for obj in ast.objects:
            self._resolve_attachments(obj, schema)

        # Third pass: resolve connections
        resolved_objects = []
        for obj in ast.objects:
            resolved_obj = self._resolve_object(obj, schema)
            resolved_objects.append(resolved_obj)

        # Build global instance order (creation order)
        instance_order = []
        for obj in resolved_objects:
            instance_order.extend(obj.instances)

        # Assign 1-based indices
        for idx, inst in enumerate(instance_order, 1):
            inst.index = idx

        resolved_file = ResolvedFile(
            version=ast.version,
            schema=schema,
            objects=resolved_objects,
            output=ast.output,
            instance_order=instance_order,
        )

        # Final validation
        self._validate_resolved(resolved_file)

        return (resolved_file if not self.diagnostics.has_errors() else None), self.diagnostics

    def _collect_instances(self, obj: ObjectDecl) -> None:
        """Collect all instances in an object section."""
        obj_instances = []
        global_props = obj.properties.properties if obj.properties else {}

        for inst in obj.instances:
            if inst.identifier in self._instance_map:
                self.diagnostics.add(make_diagnostic(
                    Codes.RESOLVE_DUPLICATE_DEFINITION,
                    f"Duplicate instance identifier: {inst.identifier}",
                    Severity.ERROR,
                    inst.location,
                    ("Use a unique identifier for each instance",)
                ))
                continue

            inst_props = inst.properties.properties if inst.properties else {}

            resolved = ResolvedInstance(
                type_name=inst.type_name,
                identifier=inst.identifier,
                properties=inst_props,
                global_properties=global_props,
                object_name=obj.name,
                index=0,  # Will be assigned later
            )

            self._instance_map[inst.identifier] = resolved
            obj_instances.append(resolved)

        self._object_instances[obj.name] = obj_instances

    def _resolve_attachments(self, obj: ObjectDecl, schema: Optional[Schema]) -> None:
        """Resolve attachment declarations."""
        obj_instances = self._object_instances.get(obj.name, [])
        instance_by_id = {inst.identifier: inst for inst in obj_instances}

        for att in obj.attachments:
            if att.uuid in self._attachment_map:
                self.diagnostics.add(make_diagnostic(
                    Codes.RESOLVE_DUPLICATE_DEFINITION,
                    f"Duplicate attachment UUID: {att.uuid}",
                    Severity.ERROR,
                    att.location,
                ))
                continue

            # Find parent instance
            parent = instance_by_id.get(att.parent)
            if not parent:
                self.diagnostics.add(make_diagnostic(
                    Codes.RESOLVE_UNDEFINED_IDENTIFIER,
                    f"Attachment references unknown instance: {att.parent}",
                    Severity.ERROR,
                    att.location,
                    (f"Available instances in '{obj.name}': {', '.join(instance_by_id.keys())}",)
                ))
                continue

            resolved = ResolvedAttachment(
                uuid=att.uuid,
                parent_instance=att.parent,
                part_name=att.part_name,
                cframe=att.cframe,
            )
            self._attachment_map[att.uuid] = resolved

    def _resolve_object(self, obj: ObjectDecl, schema: Optional[Schema]) -> ResolvedObject:
        """Resolve a single object section."""
        self._current_object = ResolvedObject(
            name=obj.name,
            global_properties=obj.properties.properties if obj.properties else {},
            instances=[],
            attachments=[],
            connections=[],
        )
        obj_instances = self._object_instances.get(obj.name, [])

        # Add instances to object
        for inst in obj_instances:
            self._current_object.instances.append(inst)

        # Add attachments for this object
        for att in obj.attachments:
            if att.uuid in self._attachment_map:
                self._current_object.attachments.append(self._attachment_map[att.uuid])

        # Resolve connections
        for conn in obj.connections:
            resolved_conn = self._resolve_connection(conn, schema)
            if resolved_conn:
                self._current_object.connections.append(resolved_conn)

        return self._current_object

    def _resolve_connection(self, conn: ConnectionDecl, schema: Optional[Schema]) -> Optional[ResolvedConnection]:
        """Resolve a connection declaration."""
        child = self._instance_map.get(conn.child)
        if not child:
            self.diagnostics.add(make_diagnostic(
                Codes.RESOLVE_UNDEFINED_IDENTIFIER,
                f"Connection references unknown child instance: {conn.child}",
                Severity.ERROR,
                conn.location,
                ("Declare the instance before connecting it",)
            ))
            return None

        parent = self._instance_map.get(conn.parent)
        if not parent:
            self.diagnostics.add(make_diagnostic(
                Codes.RESOLVE_UNDEFINED_IDENTIFIER,
                f"Connection references unknown parent instance: {conn.parent}",
                Severity.ERROR,
                conn.location,
            ))
            return None

        # Validate localType against schema if available
        if schema:
            # Could validate localType against schema's known types
            pass

        # Validate point reference
        if isinstance(conn.point, str):
            # UUID reference - check attachment exists
            if conn.point not in self._attachment_map:
                self.diagnostics.add(make_diagnostic(
                    Codes.RESOLVE_UNDEFINED_UUID,
                    f"Connection references unknown attachment UUID: {conn.point}",
                    Severity.ERROR,
                    conn.location,
                ))
                return None
        else:
            # Numeric point ID - could validate against schema
            if conn.point <= 0:
                self.diagnostics.add(make_diagnostic(
                    Codes.RESOLVE_INVALID_POINT,
                    f"Point ID must be positive (1-based), got {conn.point}",
                    Severity.ERROR,
                    conn.location,
                ))
                return None

        return ResolvedConnection(
            child=child,
            parent=parent,
            local_type=conn.local_type,
            point=conn.point,
        )

    def _validate_resolved(self, resolved: ResolvedFile) -> None:
        """Perform final validation on resolved model."""
        # Check for unused instances (optional warning)
        used_as_child = {c.child.identifier for obj in resolved.objects for c in obj.connections}
        used_as_parent = {c.parent.identifier for obj in resolved.objects for c in obj.connections}

        for inst in resolved.instance_order:
            if inst.identifier not in used_as_child and inst.identifier not in used_as_parent:
                # Root instance - could be valid (e.g., Base)
                pass

        # Validate output
        if resolved.output and not resolved.output.file:
            self.diagnostics.add(make_diagnostic(
                Codes.COMPILE_INVALID_OUTPUT,
                "Output declaration missing file path",
                Severity.ERROR,
                resolved.output.location,
            ))

    def _load_schema(self, source: str) -> Optional[Schema]:
        """Load schema from file."""
        try:
            schema_path = self.schema_dir / source
            if not schema_path.is_absolute():
                schema_path = self.schema_dir / source
            return load_schema(schema_path)
        except Exception as e:
            self.diagnostics.add(make_diagnostic(
                Codes.SCHEMA_MISSING,
                f"Failed to load schema from {source}: {e}",
                Severity.ERROR,
            ))
            return None


def resolve(ast: File, schema_dir: Optional[Path] = None, schema: Optional[Schema] = None) -> tuple[Optional[ResolvedFile], DiagnosticCollector]:
    """Resolve AST to semantic model."""
    resolver = Resolver(schema_dir)
    return resolver.resolve(ast, schema)