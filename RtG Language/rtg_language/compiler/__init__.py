"""Compiler for RtG-Language - produces RtG-Format output."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path
import json
import hashlib
from collections import defaultdict

from ..resolver import ResolvedFile, ResolvedInstance, ResolvedConnection, ResolvedAttachment
from ..diagnostics import (
    DiagnosticCollector,
    Codes,
    SourceLocation,
    Severity,
    make_diagnostic,
)


@dataclass
class CompileResult:
    """Result of compilation."""
    build: list[list]  # RtG-Format build array
    diagnostics: DiagnosticCollector


class Compiler:
    """Compiles resolved RtG-Language to RtG-Format."""

    def __init__(self):
        self.diagnostics = DiagnosticCollector()
        self._instance_to_index: dict[str, int] = {}  # identifier -> 1-based index

    def compile(self, resolved: ResolvedFile) -> CompileResult:
        """Compile resolved model to RtG-Format build array."""
        self.diagnostics = DiagnosticCollector()
        self._instance_to_index = {}

        # Assign 1-based indices in creation order
        for idx, inst in enumerate(resolved.instance_order, 1):
            self._instance_to_index[inst.identifier] = idx

        # Collect attachments per parent instance
        attachments_by_parent: dict[str, list[ResolvedAttachment]] = defaultdict(list)
        for obj in resolved.objects:
            for att in obj.attachments:
                attachments_by_parent[att.parent_instance].append(att)

        # Build output array
        build = []

        for inst in resolved.instance_order:
            entry = self._compile_instance(inst, resolved, attachments_by_parent.get(inst.identifier, []))
            build.append(entry)

        return CompileResult(build=build, diagnostics=self.diagnostics)

    def _compile_instance(
        self,
        inst: ResolvedInstance,
        resolved: ResolvedFile,
        attachments: list[ResolvedAttachment],
    ) -> list:
        """Compile a single instance to RtG-Format entry."""
        # [Type, Connections, Properties]

        # Type
        type_name = inst.type_name

        # Connections
        connections = []
        for obj in resolved.objects:
            for conn in obj.connections:
                if conn.child.identifier == inst.identifier:
                    parent_idx = self._instance_to_index.get(conn.parent.identifier)
                    if parent_idx is None:
                        self.diagnostics.add(make_diagnostic(
                            Codes.COMPILE_INDEX_OUT_OF_RANGE,
                            f"Parent instance {conn.parent.identifier} not found in index",
                            Severity.ERROR,
                            inst.location,
                        ))
                        continue

                    # Connection format: [LocalType, PrimaryID, PrimaryIndex]
                    # LocalType as string per RtG-Format spec
                    local_type = str(conn.local_type)

                    # PrimaryID: either numeric point ID or UUID
                    if isinstance(conn.point, str):
                        primary_id = conn.point  # UUID
                    else:
                        primary_id = str(conn.point)  # Numeric point ID

                    connections.append([local_type, primary_id, parent_idx])

        # Properties: merge global + instance (instance overrides global)
        properties = {}
        properties.update(inst.global_properties)
        properties.update(inst.properties)

        # Add EphemeralAttachments if this instance has any
        if attachments:
            ephemeral = {}
            for att in attachments:
                ephemeral[att.uuid] = {
                    "partName": att.part_name,
                    "cframe": list(att.cframe),
                }
            properties["EphemeralAttachments"] = ephemeral

        # If empty, use empty array per RtG-Format spec
        if not properties:
            properties = []

        return [type_name, connections, properties]


def compile_resolved(resolved: ResolvedFile) -> CompileResult:
    """Compile resolved model to RtG-Format."""
    compiler = Compiler()
    return compiler.compile(resolved)