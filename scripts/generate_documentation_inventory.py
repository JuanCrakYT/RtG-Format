#!/usr/bin/env python3
"""Generate or verify the maintained Markdown inventory."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "documentation-inventory.md"
SKIP_PARTS = {".git", "node_modules"}
SKIP_PREFIXES = ("old-files/",)
BT = chr(96)


def documents() -> list[str]:
    paths = []
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP_PREFIXES) or any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        paths.append(rel)
    return sorted(paths, key=lambda value: value.lower())


def group_for(path: str) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "Root documentation and project policies"
    if parts[0] == "docs":
        return "Guides, standards, and templates"
    if parts[0] == "blocks" and len(parts) > 1 and parts[1] == "reference":
        return "Block reference pages"
    if parts[0] == "blocks" and len(parts) > 1 and parts[1] == "parts":
        return "Part and connection-point catalogs"
    if parts[0] == "RtG-CLI" and len(parts) > 1 and parts[1] == "languages":
        return "Localized RtG-CLI runtime content"
    if parts[0] == "RtG-CLI":
        return "RtG-CLI documentation"
    if parts[0] == "RtG Language":
        return "RtG Language documentation"
    if parts[0] == "RtG-Preview":
        return "RtG-Preview documentation"
    return {
        "format": "Format reference",
        "research": "Research",
        "examples": "Examples and experiments",
        "compression": "Encoding and compression",
        "assets": "Assets",
        "tools": "Tooling",
        "blocks": "Block documentation",
    }.get(parts[0], "Documentation: " + parts[0])


def description_for(path: str) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "Project entry point, policy, specification, or planning document"
    if parts[0] == "RtG-CLI" and len(parts) > 2 and parts[1] == "languages":
        return "Localized CLI text used by the application"
    if parts[-1].lower() == "readme.md":
        return "Directory index and maintenance guide"
    if parts[0] == "blocks" and len(parts) > 2 and parts[1] == "reference" and parts[-1].lower() != "template.md":
        return "Individual block/object reference"
    if parts[0] == "docs" and len(parts) > 1 and parts[1] == "templates":
        return "Reusable documentation template"
    if parts[0] == "docs":
        return "Cross-cutting guide or documentation standard"
    return "Component-specific or subject-specific documentation"


def render(paths: list[str]) -> str:
    groups: dict[str, list[str]] = {}
    for path in paths:
        groups.setdefault(group_for(path), []).append(path)
    lines = [
        "# Maintained Markdown Inventory",
        "",
        "This catalog is generated from the repository tree by [" + BT + "scripts/generate_documentation_inventory.py" + BT + "](../scripts/generate_documentation_inventory.py). It lists maintained Markdown documents individually so readers can locate each page and contributors can classify its role before editing.",
        "",
        "**Scope:** all repository Markdown files except " + BT + "old-files/" + BT + " (immutable historical archive) and vendored/generated " + BT + "node_modules/" + BT + ". Inclusion here does not imply that every technical claim has been independently re-verified.",
        "",
        "**Documents indexed:** " + str(len(paths)),
        "",
        "## Directory summary",
        "",
        "| Area | Documents |",
        "| --- | ---: |",
    ]
    for group, entries in sorted(groups.items(), key=lambda item: item[0].casefold()):
        lines.append("| " + group + " | " + str(len(entries)) + " |")
    lines.extend(["", "## Individual documents"])
    for group, entries in sorted(groups.items(), key=lambda item: item[0].casefold()):
        lines.extend(["", "### " + group, ""])
        for path in sorted(entries, key=str.casefold):
            target = "/".join(quote(part, safe="-._~") for part in path.split("/"))
            lines.append("- [" + BT + path + BT + "](../" + target + ") — " + description_for(path))
    lines.extend([
        "",
        "---",
        "",
        "Update this page by running " + BT + "python scripts/generate_documentation_inventory.py" + BT + ". The " + BT + "--check" + BT + " option verifies that the generated inventory is current without writing files.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the inventory is stale")
    args = parser.parse_args()
    expected = render(documents())
    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if args.check:
        if current != expected:
            print("Documentation inventory is stale. Run python scripts/generate_documentation_inventory.py.", file=sys.stderr)
            return 1
        print("Documentation inventory is current (" + str(len(documents())) + " documents).")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print("Generated docs/documentation-inventory.md (" + str(len(documents())) + " documents).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
