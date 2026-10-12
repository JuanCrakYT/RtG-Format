#!/usr/bin/env python3
"""Normalize safe Markdown structure without rewriting prose or code examples."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "node_modules"}
SKIP_PREFIXES = ("old-files/",)
FENCE = re.compile(r"^\s*(\x60{3,}|~{3,})")
SETEXT = re.compile(r"^\s*(=+|-{3,})\s*$")


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith(SKIP_PREFIXES) or any(
        part in SKIP_PARTS for part in path.relative_to(ROOT).parts
    )


def can_be_heading(line: str) -> bool:
    candidate = line.lstrip("\ufeff").strip()
    if not candidate or candidate.startswith(("#", ">", "|", "`", "- ", "* ", "+ ")):
        return False
    if re.match(r"^\d+[.)]\s", candidate):
        return False
    return True


def normalize(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    output: list[str] = []
    in_fence = False
    fence_char = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        marker = FENCE.match(line)
        if marker:
            char = marker.group(1)[0]
            if not in_fence:
                in_fence, fence_char = True, char
            elif char == fence_char:
                in_fence = False
            output.append(line)
            i += 1
            continue
        if not in_fence and i + 1 < len(lines):
            underline = SETEXT.match(lines[i + 1])
            if underline and can_be_heading(line):
                title = line.lstrip("\ufeff").strip()
                bom = "\ufeff" if line.startswith("\ufeff") else ""
                level = "#" if underline.group(1).startswith("=") else "##"
                output.append(f"{bom}{level} {title}")
                i += 2
                continue
        output.append(line)
        i += 1
    return "\n".join(output).rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report files that would change without writing them",
    )
    args = parser.parse_args()
    changed = scanned = 0
    changed_paths: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        if should_skip(path):
            continue
        scanned += 1
        original = path.read_text(encoding="utf-8")
        normalized = normalize(original)
        if normalized != original:
            changed += 1
            changed_paths.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_text(normalized, encoding="utf-8", newline="\\n")
    action = "would normalize" if args.check else "normalized"
    print(f"Scanned {scanned} maintained Markdown documents; {action} {changed}.")
    if args.check and changed_paths:
        print("\\n".join(changed_paths))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
