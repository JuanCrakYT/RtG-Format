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
RTG_CLI_PATH = os.path.join(BASE_DIR, "rtg-cli.json")
VERSION = json.load(open(ASSETS_PATH, encoding="utf-8"))[0]["version"]


def load_assets():
    """Load and return the parsed contents of assets.json."""
    with open(ASSETS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_rtg_cli():
    """Load and return the parsed contents of rtg-cli.json.

    Returns ``None`` when the file is missing or invalid so the CLI
    can degrade gracefully.
    """
    try:
        with open(RTG_CLI_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


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


def find_program_meta(rtg_cli, command):
    """Find a program's metadata entry in rtg-cli.json by command name.

    Returns the matching dict or ``None`` when no entry matches.
    """
    if not rtg_cli:
        return None
    for entry in rtg_cli:
        if entry.get("command") == command:
            return entry
    return None


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


def show_program_info(assets, rtg_cli, program):
    """Print metadata for a program from assets.json and rtg-cli.json.

    Full external-program functionality is not implemented yet; this
    displays the metadata discovered from both configuration files.
    """
    info = assets[0].get("text", {}).get(program, {})
    meta = find_program_meta(rtg_cli, program)

    content_lines = []

    print(f"\n{program}\n")
    print("-" * len(program))

    creators = info.get("creators", {})
    if creators:
        print("\nCreators:")
        print()
        for creator, notes in creators.items():
            for note in notes:
                line = f"    {note} ({creator})"
                print(line)
                content_lines.append(line)

    if meta:
        langs = meta.get("lang", [])
        if langs:
            print("\nLanguages:")
            print()
            for lang in langs:
                line = f"    {lang}"
                print(line)
                content_lines.append(line)

    print("\nVersion:")
    print()
    print("    Content:")
    if meta and meta.get("version"):
        line = f"        VERSION {meta['version']}"
        print(line)
        content_lines.append(line)
    else:
        line = f"        [Error] No metadata found for '{program}'"
        print(line)
        content_lines.append(line)

    content_lines.append(" Run Output")
    frame_width = max(len(s) for s in content_lines)

    print()
    print("|" + "-" * frame_width + "|")
    print("|" + " Run Output".ljust(frame_width) + "|")
    print("|" + "-" * frame_width + "|")


def main(argv=None):
    """Entry point — returns an exit code."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        assets = load_assets()
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading assets.json: {e}", file=sys.stderr)
        return 1

    rtg_cli = load_rtg_cli()

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
        show_program_info(assets, rtg_cli, arg)
    else:
        print(f"Unknown command: {arg}\n")
        show_usage(assets)

    return 0


if __name__ == "__main__":
    sys.exit(main())
