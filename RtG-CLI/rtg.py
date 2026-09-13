#!/usr/bin/env python3
"""RtG-CLI — general-purpose CLI for RtG-Format programs.

All configuration, help text, rules, and addon metadata are read from
assets.json.  Paths referenced in assets.json are resolved relative
to this directory so the tool is portable across machines.

New programs can be added simply by appending entries to assets.json;
no code changes are required.
"""

import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_PATH = os.path.join(BASE_DIR, "assets.json")


def load_assets():
    """Load and return the parsed contents of assets.json."""
    with open(ASSETS_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_path(relative_path):
    """Resolve a path relative to the RtG-CLI directory."""
    return os.path.normpath(os.path.join(BASE_DIR, relative_path))


def read_text_file(relative_path):
    """Read a text file whose path is relative to the RtG-CLI directory."""
    full_path = resolve_path(relative_path)
    try:
        with open(full_path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


# ---------------------------------------------------------------------------
# Data accessors (all driven by assets.json)
# ---------------------------------------------------------------------------

def get_addons(assets):
    """Return the dict of addon configurations."""
    return assets[0].get("addons", {})


def get_addon(assets, command):
    """Return the config for a specific addon command, or None."""
    return get_addons(assets).get(command)


def get_internal_list(assets):
    """Return the list of recognised system/internal commands."""
    return assets[0].get("internal-list", [])


def get_available_langs(assets):
    """Return the set of all recognised language codes."""
    langs = set(assets[0].get("void-language", {}).keys())
    langs.update(assets[0].get("help", {}).keys())
    langs.update(assets[0].get("rules", {}).keys())
    langs.add("en")
    return langs


# ---------------------------------------------------------------------------
# Argument classification helpers
# ---------------------------------------------------------------------------

def is_single_hyphen(arg):
    """True when *arg* starts with exactly one hyphen (not ``--``)."""
    return len(arg) > 1 and arg.startswith("-") and not arg.startswith("--")


def is_lang_selector(arg, assets):
    """True when a single-hyphen arg is a language code (e.g. ``-en``)."""
    if not is_single_hyphen(arg):
        return False
    return arg[1:] in get_available_langs(assets)


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

def show_void(assets, lang=None):
    """Print the startup/usage text, optionally translated."""
    if lang:
        void_lang = assets[0].get("void-language", {})
        if lang in void_lang:
            print(void_lang[lang], end="")
        else:
            print(f"Language not available: {lang}\n")
            print(assets[0]["void"], end="")
    else:
        print(assets[0]["void"], end="")


def show_version(assets):
    """Print the RtG-CLI version."""
    print(assets[0]["version"])


def show_rules(assets, lang=None):
    """Print the rules file, in *lang* or the default language."""
    rules = assets[0].get("rules", {})
    if not rules:
        print("Rules not available.")
        return
    langs = list(rules.keys())
    if lang:
        if lang in rules:
            content = read_text_file(rules[lang])
            if content:
                print(content, end="")
            else:
                print(f"Could not read rules file: {rules[lang]}")
        else:
            print(f"Language not available for rules: {lang}")
    else:
        content = read_text_file(rules[langs[0]])
        if content:
            print(content, end="")
        else:
            print(f"Could not read rules file: {rules[langs[0]]}")


def show_commands(assets):
    """Print the list of recognised internal/system commands."""
    internal_list = get_internal_list(assets)
    print("The most commonly used rtg commands are:")
    print()
    for cmd in internal_list:
        print(f"  {cmd}")


def show_cli_langs(assets):
    """Print the languages available for RtG-CLI itself."""
    print("Available languages for RtG-CLI:")
    print()
    print("  void")
    for lang in sorted(assets[0].get("void-language", {}).keys()):
        print(f"  {lang}")


def show_addon_langs(addon):
    """Print the languages available for a specific addon."""
    langs = addon.get("lang", [])
    print("Available languages:")
    print()
    for lang in langs:
        print(f"  {lang}")


def show_help_file(assets, lang=None):
    """Print the general help file, in *lang* or the default language."""
    help_paths = assets[0].get("help", {})
    if not help_paths:
        print("Help not available.")
        return
    langs = list(help_paths.keys())
    if lang:
        if lang in help_paths:
            content = read_text_file(help_paths[lang])
            if content:
                print(content, end="")
            else:
                print(f"Could not read help file: {help_paths[lang]}")
        else:
            print(f"Language not available for help: {lang}")
    else:
        content = read_text_file(help_paths[langs[0]])
        if content:
            print(content, end="")
        else:
            print(f"Could not read help file: {help_paths[langs[0]]}")


def show_help_for_command(assets, target, lang=None, list_langs=False):
    """Print help for *target*, optionally in *lang* or listing languages."""
    if target is None:
        if list_langs:
            show_cli_langs(assets)
        else:
            show_help_file(assets, lang)
        return

    internal_help = assets[0].get("internal", {}).get("help", {})
    addon = get_addon(assets, target)

    if addon:
        if list_langs:
            show_addon_langs(addon)
        elif target in internal_help:
            help_texts = internal_help[target]
            if lang:
                if lang in help_texts:
                    print(help_texts[lang], end="")
                else:
                    print(f"Language not available: {lang}\n")
                    _print_help_fallback(help_texts, target)
            else:
                _print_help_fallback(help_texts, target)
        else:
            name = addon.get("name", target)
            print(f"No internal help available for '{target}'.")
            print(f"Addon: {name}")
        return

    if target in internal_help:
        help_texts = internal_help[target]
        if list_langs:
            print("Available languages:")
            print()
            for l in help_texts:
                print(f"  {l}")
        elif lang:
            if lang in help_texts:
                print(help_texts[lang], end="")
            else:
                print(f"Language not available: {lang}\n")
                _print_help_fallback(help_texts, target)
        else:
            _print_help_fallback(help_texts, target)
        return

    print(f"Unknown command: {target}\n")
    show_void(assets)


def _print_help_fallback(help_texts, target):
    if help_texts:
        first = list(help_texts.keys())[0]
        print(help_texts[first], end="")
    else:
        print(f"No help available for '{target}'.")


def show_addon_info(assets, addon_key):
    """Print addon metadata and a dynamic-width Run Output frame."""
    addon = get_addon(assets, addon_key)
    if not addon:
        print(f"Unknown command: {addon_key}")
        print()
        show_void(assets)
        return

    content_lines = []

    print(f"\n{addon_key}\n")
    print("-" * len(addon_key))

    creators = addon.get("creators", {})
    if creators:
        print("\nCreators:")
        print()
        for creator, notes in creators.items():
            for note in notes:
                line = f"    {note} ({creator})"
                print(line)
                content_lines.append(line)

    langs = addon.get("lang", [])
    if langs:
        print("\nLanguages:")
        print()
        for lang in langs:
            line = f"    {lang}"
            print(line)
            content_lines.append(line)

    version = addon.get("version")
    print("\nVersion:")
    print()
    print("    Content:")
    if version:
        line = f"        VERSION {version}"
    else:
        line = "        [No version information]"
    print(line)
    content_lines.append(line)

    content_lines.append(" Run Output")
    frame_width = max(len(s) for s in content_lines)

    print()
    print("|" + "-" * frame_width + "|")
    print("|" + " Run Output".ljust(frame_width) + "|")
    print("|" + "-" * frame_width + "|")


# ---------------------------------------------------------------------------
# Command dispatchers
# ---------------------------------------------------------------------------

def dispatch_help(assets, args):
    """Handle the ``help`` system command."""
    target = None
    lang = None
    list_langs = False

    for a in args:
        if a in ("-lang", "--lang"):
            list_langs = True
        elif is_single_hyphen(a) and is_lang_selector(a, assets):
            lang = a[1:]
        elif target is None and not is_single_hyphen(a):
            target = a

    show_help_for_command(assets, target, lang, list_langs)
    return 0


def dispatch_rules(assets, args):
    """Handle the ``-r`` / ``--rules`` system command."""
    lang = None
    for a in args:
        if is_single_hyphen(a) and is_lang_selector(a, assets):
            lang = a[1:]
    show_rules(assets, lang)
    return 0


def dispatch_addon(assets, addon_key, args):
    """Handle a command after an addon has been identified.

    Applies the prefix rules:
      * no hyphen or ``--``  → addon argument
      * single ``-``          → RtG-CLI option
    """
    addon = get_addon(assets, addon_key)
    if not addon:
        print(f"Unknown command: {addon_key}")
        print()
        show_void(assets)
        return 0

    cli_args = []
    addon_args = []

    for a in args:
        if is_single_hyphen(a):
            cli_args.append(a)
        else:
            addon_args.append(a)

    for a in cli_args:
        if a in ("-lang", "--lang"):
            show_addon_langs(addon)
            return 0
        elif is_lang_selector(a, assets):
            pass
        else:
            print(f"Unknown system option after addon: {a}", file=sys.stderr)

    show_addon_info(assets, addon_key)

    if addon_args:
        name = addon.get("name", addon_key)
        print()
        print(f"Arguments for {name}:")
        for arg in addon_args:
            print(f"  {arg}")

    return 0


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main(argv=None):
    """Parse arguments and dispatch to the appropriate handler."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        assets = load_assets()
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading assets.json: {e}", file=sys.stderr)
        return 1

    if not argv:
        show_void(assets)
        return 0

    addons = get_addons(assets)
    i = 0
    selected_lang = None

    while i < len(argv):
        arg = argv[i]

        if arg == "-language":
            i += 1
            if i < len(argv):
                selected_lang = argv[i]
            else:
                print("Error: -language requires a value", file=sys.stderr)
                return 1

        elif arg in ("-v", "--version"):
            show_version(assets)
            return 0

        elif arg in ("-h", "--help"):
            show_help_file(assets, selected_lang)
            return 0

        elif arg == "help":
            remaining = argv[i + 1:]
            return dispatch_help(assets, remaining)

        elif arg in ("-l", "--lang"):
            show_cli_langs(assets)
            return 0

        elif arg in ("-r", "--rules"):
            remaining = argv[i + 1:]
            return dispatch_rules(assets, remaining)

        elif arg in ("-c", "--commands"):
            show_commands(assets)
            return 0

        elif arg in addons:
            remaining = argv[i + 1:]
            return dispatch_addon(assets, arg, remaining)

        else:
            print(f"Unknown command: {arg}")
            print()
            show_void(assets, selected_lang)
            return 0

        i += 1

    show_void(assets, selected_lang)
    return 0


if __name__ == "__main__":
    sys.exit(main())
