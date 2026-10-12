#!/usr/bin/env python3
"""Rewrite Markdown links after moving block references into category folders."""
from __future__ import annotations
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "node_modules"}
SKIP_PREFIXES = ("old-files/",)
LINK = re.compile(r"(?P<start>!?\[[^\]]*\]\()(?P<dest><[^>]+>|[^)\s]+)(?P<tail>(?:\s+[^)]*)?\))")
REFERENCE = re.compile(r"^(?P<start>\s*\[[^\]]+\]:\s*)(?P<dest><[^>]+>|[^ \t]+)(?P<tail>.*)$")


def encode_path(value: str) -> str:
    return "/".join(quote(part, safe="-._~") for part in value.split("/"))


def is_skipped(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith(SKIP_PREFIXES) or any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)


def canonical_block_target(path: Path, old_to_new: dict[str, str]) -> Path | None:
    try:
        rel = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return None
    target = old_to_new.get(rel)
    return ROOT / target if target else None


def rewrite_destination(source: Path, raw: str, old_base: Path, old_to_new: dict[str, str]) -> str:
    wrapped = raw.startswith("<") and raw.endswith(">")
    target = raw[1:-1] if wrapped else raw
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith("#") or not parts.path:
        return raw
    decoded = unquote(parts.path)
    original_target = (ROOT / decoded.lstrip("/")) if decoded.startswith("/") else (old_base / decoded)
    original_target = original_target.resolve()
    mapped = canonical_block_target(original_target, old_to_new)
    destination = mapped if mapped is not None else original_target
    if mapped is None and not original_target.exists():
        return raw
    try:
        rel = os.path.relpath(destination, source.parent)
    except ValueError:
        return raw
    replacement = urlunsplit(("", "", encode_path(Path(rel).as_posix()), parts.query, parts.fragment))
    return "<" + replacement + ">" if wrapped else replacement


def main() -> int:
    old_to_new: dict[str, str] = {}
    for path in ROOT.glob("blocks/reference/*/*.md"):
        if path.name.lower() in {"readme.md", "template.md"}:
            continue
        old_to_new["blocks/reference/" + path.name] = path.relative_to(ROOT).as_posix()

    changed = scanned = 0
    for path in sorted(ROOT.rglob("*.md")):
        if is_skipped(path):
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        moved_block = rel.startswith("blocks/reference/") and len(path.relative_to(ROOT).parts) == 4 and path.name.lower() not in {"readme.md", "template.md"}
        old_base = ROOT / "blocks" / "reference" if moved_block else path.parent
        original = path.read_text(encoding="utf-8", errors="replace")
        lines = original.splitlines(keepends=True)
        output = []
        in_fence = False
        fence_char = ""
        for line in lines:
            fence = re.match(r"^\\s*(\x60{3,}|~{3,})", line)
            if fence:
                marker = fence.group(1)[0]
                if not in_fence:
                    in_fence, fence_char = True, marker
                elif marker == fence_char:
                    in_fence = False
                output.append(line)
                continue
            if in_fence:
                output.append(line)
                continue
            line = LINK.sub(lambda m: m.group("start") + rewrite_destination(path, m.group("dest"), old_base, old_to_new) + m.group("tail"), line)
            match = REFERENCE.match(line.rstrip("\r\n"))
            if match:
                rewritten = match.group("start") + rewrite_destination(path, match.group("dest"), old_base, old_to_new) + match.group("tail")
                newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
                line = rewritten + newline
            output.append(line)
        updated = "".join(output)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="")
            changed += 1
    print("Scanned " + str(scanned) + " maintained Markdown documents; rewrote links in " + str(changed) + ".")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
