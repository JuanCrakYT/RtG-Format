#!/usr/bin/env python3
"""Check repository-local Markdown links without rewriting any files."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git"}
SKIP_PREFIXES = ("old-files/",)
LINK = re.compile(r"!??\[[^\]]*\]\((<[^>]+>|[^)]+)\)")


def is_scanned(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return not rel.startswith(SKIP_PREFIXES) and not any(
        part in SKIP_PARTS for part in path.relative_to(ROOT).parts
    )


def resolve_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0] if target else ""
    if not target:
        return None
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or target.startswith("#"):
        return None
    path_text = unquote(parts.path)
    if not path_text:
        return None
    if path_text.startswith("/"):
        return ROOT / path_text.lstrip("/")
    return source.parent / path_text


def main() -> int:
    failures: list[str] = []
    documents = sorted(path for path in ROOT.rglob("*.md") if is_scanned(path))
    for source in documents:
        text = source.read_text(encoding="utf-8", errors="replace")
        in_fence = False
        fence_char = ""
        for line_no, line in enumerate(text.splitlines(), start=1):
            fence = re.match(r"^\s*(\x60{3,}|~{3,})", line)
            if fence:
                marker = fence.group(1)[0]
                if not in_fence:
                    in_fence, fence_char = True, marker
                elif marker == fence_char:
                    in_fence = False
                continue
            if in_fence:
                continue
            for match in LINK.finditer(line):
                destination = match.group(1)
                resolved = resolve_target(source, destination)
                if resolved is None or resolved.exists():
                    continue
                if not resolved.suffix and (
                    (resolved / "README.md").exists()
                    or (resolved / "index.md").exists()
                ):
                    continue
                rel_source = source.relative_to(ROOT).as_posix()
                rel_target = (
                    resolved.relative_to(ROOT).as_posix()
                    if resolved.is_relative_to(ROOT)
                    else str(resolved)
                )
                failures.append(
                    f"{rel_source}:{line_no}: missing target {destination!r} "
                    f"(resolved to {rel_target})"
                )
    print(f"Scanned {len(documents)} maintained Markdown documents.")
    if failures:
        print("\n".join(failures))
        print(f"\nFound {len(failures)} broken local Markdown link(s).", file=sys.stderr)
        return 1
    print("All repository-local Markdown links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
