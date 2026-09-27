"""Temporary CLI boundary; compilation is intentionally not implemented yet."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rtg-language")
    parser.add_argument("--version", action="version", version="RtG-Language 0.1.0")
    parser.parse_args(argv)
    parser.error("the RtG-Language 2.0 compiler is not implemented yet")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
