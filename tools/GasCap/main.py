from __future__ import annotations

import argparse
import base64
import json
import sys
import uuid
from pathlib import Path


# ============================================================
# Paths
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"

JSON_OUTPUT = OUTPUT_DIR / "GasCap.json"
BASE64_OUTPUT = OUTPUT_DIR / "GasCap.txt"


# ============================================================
# OBJ parsing
# ============================================================

def parse_obj_objects(input_path: Path) -> list[str]:
    """
    Read the OBJ and return the names of its declared objects.

    Only OBJ object declarations (`o`) are relevant here.
    Geometry, vertices and faces are deliberately ignored.

    The OBJ is a source for identifying discrete model
    instances, not something that gets copied into RtG.
    """

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Input path is not a file: {input_path}"
        )

    objects: list[str] = []

    with input_path.open(
        "r",
        encoding="utf-8",
        errors="replace",
    ) as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if not line.startswith("o "):
                continue

            name = line[2:].strip()

            if name:
                objects.append(name)

    return objects


def is_gascap_object(object_name: str) -> bool:
    """
    Determine whether an OBJ object represents a GasCap.

    Supported names include:

        GasCap
        GasCap.001
        GasCap.002
        ...

    Matching is case-insensitive.
    """

    normalized = object_name.strip().lower()

    return (
        normalized == "gascap"
        or normalized.startswith("gascap.")
    )


def find_gascap_instances(
    object_names: list[str],
) -> list[str]:
    """
    Return only OBJ objects identified as GasCap instances.
    """

    return [
        name
        for name in object_names
        if is_gascap_object(name)
    ]


# ============================================================
# UUID / CFrame
# ============================================================

def generate_uuid() -> str:
    """
    Generate an opaque UUID for an EphemeralAttachment.
    """

    return "{" + str(uuid.uuid4()) + "}"


def identity_cframe() -> list[float]:
    """
    Identity CFrame at the origin.

    RtG layout:

        [x, y, z,
         r00, r01, r02,
         r10, r11, r12,
         r20, r21, r22]
    """

    return [
        0.0,
        0.0,
        0.0,

        1.0,
        0.0,
        0.0,

        0.0,
        1.0,
        0.0,

        0.0,
        0.0,
        1.0,
    ]


# ============================================================
# RtG generation
# ============================================================

def create_build(
    gascap_instances: list[str],
) -> list:
    """
    Create the preliminary RtG GasCap build.

    Structure:

        Part
        ├── EphemeralAttachment UUID A
        │       └── GasCap
        ├── EphemeralAttachment UUID B
        │       └── GasCap
        └── ...

    Each GasCap receives its own UUID.

    IMPORTANT:
    The OBJ geometry is NOT written into the RtG build.
    """

    if not gascap_instances:
        raise ValueError(
            "No GasCap instances were found in the input OBJ."
        )

    attachments: dict[str, dict] = {}
    gascap_blocks: list[list] = []

    for _instance_name in gascap_instances:
        attachment_uuid = generate_uuid()

        attachments[attachment_uuid] = {
            "partName": "Part",
            "cframe": identity_cframe(),
        }

        gascap_blocks.append(
            [
                "GasCap",
                [
                    [
                        "1",
                        attachment_uuid,
                        1,
                    ]
                ],
                [],
            ]
        )

    part_block = [
        "Part",
        [],
        {
            "EphemeralAttachments": attachments,
            "RGB": [
                0,
                0,
                0,
            ],
        },
    ]

    return [
        part_block,
        *gascap_blocks,
    ]


# ============================================================
# Validation
# ============================================================

def validate_build(build: list) -> None:
    """
    Validate the structural invariants produced by this tool.
    """

    if not isinstance(build, list):
        raise ValueError(
            "Build must be a list."
        )

    if len(build) < 2:
        raise ValueError(
            "Build must contain Part and at least one GasCap."
        )

    # --------------------------------------------------------
    # Part
    # --------------------------------------------------------

    part = build[0]

    if not isinstance(part, list) or len(part) != 3:
        raise ValueError(
            "Invalid Part structure."
        )

    if part[0] != "Part":
        raise ValueError(
            "The first block must be Part."
        )

    if part[1] != []:
        raise ValueError(
            "Part must not have parent connections."
        )

    part_properties = part[2]

    if not isinstance(part_properties, dict):
        raise ValueError(
            "Part properties must be an object."
        )

    attachments = part_properties.get(
        "EphemeralAttachments"
    )

    if not isinstance(attachments, dict):
        raise ValueError(
            "Part is missing EphemeralAttachments."
        )

    # --------------------------------------------------------
    # GasCaps
    # --------------------------------------------------------

    referenced_uuids: set[str] = set()

    for block_index, block in enumerate(
        build[1:],
        start=1,
    ):
        if not isinstance(block, list) or len(block) != 3:
            raise ValueError(
                f"Invalid block #{block_index}."
            )

        block_type, connections, properties = block

        if block_type != "GasCap":
            raise ValueError(
                f"Block #{block_index} is not GasCap."
            )

        if properties != []:
            raise ValueError(
                f"GasCap #{block_index} has unexpected properties."
            )

        if not isinstance(connections, list):
            raise ValueError(
                f"GasCap #{block_index} connections are invalid."
            )

        if len(connections) != 1:
            raise ValueError(
                f"GasCap #{block_index} must have exactly one connection."
            )

        connection = connections[0]

        if not isinstance(connection, list) or len(connection) != 3:
            raise ValueError(
                f"GasCap #{block_index} connection is invalid."
            )

        tipo_local, attachment_uuid, parent_index = connection

        if tipo_local != "1":
            raise ValueError(
                f"GasCap #{block_index} has invalid TipoLocal: "
                f"{tipo_local!r}"
            )

        if parent_index != 1:
            raise ValueError(
                f"GasCap #{block_index} has invalid parent index: "
                f"{parent_index!r}"
            )

        if attachment_uuid not in attachments:
            raise ValueError(
                f"GasCap #{block_index} references a UUID "
                f"that does not exist in EphemeralAttachments: "
                f"{attachment_uuid}"
            )

        if attachment_uuid in referenced_uuids:
            raise ValueError(
                f"UUID {attachment_uuid} is referenced more than once."
            )

        referenced_uuids.add(attachment_uuid)

    if referenced_uuids != set(attachments):
        raise ValueError(
            "EphemeralAttachment UUIDs and GasCap references "
            "do not match."
        )


# ============================================================
# Output
# ============================================================

def serialize_pretty_json(build: list) -> str:
    """
    Create the human-readable JSON output.
    """

    return json.dumps(
        build,
        indent=4,
        ensure_ascii=False,
    )


def serialize_compact_json(build: list) -> str:
    """
    Create the compact one-line JSON representation.

    This is the JSON that gets encoded into Base64.
    """

    return json.dumps(
        build,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def write_outputs(build: list) -> None:
    """
    Write:

        output/GasCap.json
        output/GasCap.txt

    GasCap.json:
        Pretty JSON.

    GasCap.txt:
        Base64 encoding of compact one-line JSON.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Human-readable JSON
    # --------------------------------------------------------

    pretty_json = serialize_pretty_json(build)

    JSON_OUTPUT.write_text(
        pretty_json + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Compact JSON -> Base64
    # --------------------------------------------------------

    compact_json = serialize_compact_json(build)

    encoded = base64.b64encode(
        compact_json.encode("utf-8")
    ).decode("ascii")

    BASE64_OUTPUT.write_text(
        encoded + "\n",
        encoding="ascii",
    )


# ============================================================
# CLI
# ============================================================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an RtG GasCap build from an OBJ model."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the input OBJ file.",
    )

    return parser.parse_args()


# ============================================================
# Main
# ============================================================

def main() -> int:
    args = parse_arguments()

    input_path = args.input.expanduser().resolve()

    try:
        print(f"Reading OBJ: {input_path}")

        object_names = parse_obj_objects(input_path)

        print(
            f"OBJ objects detected: {len(object_names)}"
        )

        if object_names:
            for index, name in enumerate(
                object_names,
                start=1,
            ):
                print(
                    f"  [{index}] {name}"
                )
        else:
            print("  No OBJ objects declared.")

        gascap_instances = find_gascap_instances(
            object_names
        )

        print()
        print(
            f"GasCap instances detected: "
            f"{len(gascap_instances)}"
        )

        if not gascap_instances:
            raise ValueError(
                "The input OBJ contains no objects identified "
                "as GasCap. No output was generated."
            )

        build = create_build(
            gascap_instances
        )

        validate_build(build)

        write_outputs(build)

        print()
        print("Conversion completed successfully.")
        print()
        print(
            f"GasCaps generated: "
            f"{len(gascap_instances)}"
        )
        print(
            f"JSON output:       {JSON_OUTPUT}"
        )
        print(
            f"Base64 output:     {BASE64_OUTPUT}"
        )

        return 0

    except (OSError, ValueError) as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())