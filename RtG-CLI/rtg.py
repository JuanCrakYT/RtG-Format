#!/usr/bin/env python3
"""RtG-CLI — general-purpose CLI for RtG-Format programs.

Configuration lives in assets.json (next to this script).
All program paths in assets.json are resolved relative to this
directory so the tool is portable across machines.

New programs can be added simply by appending entries to assets.json;
no code changes are required.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets.json")
VERSION = json.load(open(ASSETS_PATH, encoding="utf-8"))[0]["version"]


def load_assets():
    """Load and return the parsed contents of assets.json."""
    with open(ASSETS_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_path(relative_path):
    """Resolve a path relative to the RtG-CLI directory."""
    return os.path.normpath(os.path.join(BASE_DIR, relative_path))


def get_programs(assets):
    """Return program names discovered dynamically from assets.json.

    Any key in the 'text' section other than 'help' is treated as a
    program name.  This allows new programs to be added without
    modifying the CLI code.
    """
    text_section = assets[0].get("text", {})
    return [key for key in text_section if key != "help"]


def show_usage(assets):
    """Print the default usage text stored in the 'void' field."""
    print(assets[0]["void"], end="")


def show_help(assets, program=None):
    """Print help text, optionally for a specific program."""
    if program is None:
        show_usage(assets)
        return

    help_texts = assets[0].get("text", {}).get("help", {})
    if program in help_texts:
        print(help_texts[program], end="")
    else:
        print(f"Unknown command: {program}\n")
        show_usage(assets)


def show_version():
    """Print the RtG-CLI version."""
    print(VERSION)


def show_program_info(assets, program):
    """Print a stub with creator / version info for a program.

    The full functionality of external programs is not implemented yet;
    this simply acknowledges the command and displays metadata read from
    assets.json so the data-driven design is visible.
    """
    info = assets[0].get("text", {}).get(program, {})

    print(f"\n{program}")
    print("-" * len(program))

    creators = info.get("creators", {})
    if creators:
        print("\nCreators:")
        for creator, notes in creators.items():
            for note in notes:
                print(f"  {note} ({creator})")

    version_paths = info.get("-v", [])
    if version_paths:
        print(f"\nVersion: {version_paths[0]}")

    print("\nThis command is not yet implemented.")
    print()


def main(argv=None):
    """Entry point — returns an exit code."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        assets = load_assets()
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading assets.json: {e}", file=sys.stderr)
        return 1

    if not argv:
        show_usage(assets)
        return 0

    arg = argv[0]

    if arg in ("-h", "--help"):
        show_usage(assets)
    elif arg == "help":
        show_help(assets, argv[1] if len(argv) > 1 else None)
    elif arg in ("-v", "--version"):
        show_version()
    elif arg in get_programs(assets):
        show_program_info(assets, arg)
    else:
        print(f"Unknown command: {arg}\n")
        show_usage(assets)

    return 0


if __name__ == "__main__":
    sys.exit(main())
