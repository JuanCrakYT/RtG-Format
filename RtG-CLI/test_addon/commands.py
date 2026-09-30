#!/usr/bin/env python3
"""Test addon program command interface for RtG-CLI validation."""

import sys
from typing import Any


def execute(args: list[str]) -> int:
    """Execute the test addon with given arguments."""
    if not args:
        print("Test Addon - No arguments provided")
        print("Available commands: echo, fail, stdout, stderr, help")
        return 0

    command = args[0]
    cmd_args = args[1:]

    if command == "echo":
        return _cmd_echo(cmd_args)
    elif command == "fail":
        return _cmd_fail(cmd_args)
    elif command == "stdout":
        return _cmd_stdout(cmd_args)
    elif command == "stderr":
        return _cmd_stderr(cmd_args)
    elif command == "help":
        return _cmd_help(cmd_args)
    elif command == "exit-code":
        return _cmd_exit_code(cmd_args)
    else:
        print(f"Unknown test command: {command}")
        print("Available commands: echo, fail, stdout, stderr, help, exit-code")
        return 1


def get_commands() -> list[str]:
    """Return list of available commands."""
    return ["echo", "fail", "stdout", "stderr", "help", "exit-code"]


def get_help(command: str, lang: str | None = None) -> str | None:
    """Return help text for a command in given language."""
    help_texts = {
        "echo": {
            "en": "echo <message>\n  Prints the message to stdout.",
            "es": "echo <mensaje>\n  Imprime el mensaje en stdout.",
        },
        "fail": {
            "en": "fail [message]\n  Exits with code 1, optionally printing message to stderr.",
            "es": "fail [mensaje]\n  Sale con código 1, opcionalmente imprimiendo mensaje en stderr.",
        },
        "stdout": {
            "en": "stdout <message>\n  Prints message to stdout.",
            "es": "stdout <mensaje>\n  Imprime mensaje en stdout.",
        },
        "stderr": {
            "en": "stderr <message>\n  Prints message to stderr.",
            "es": "stderr <mensaje>\n  Imprime mensaje en stderr.",
        },
        "exit-code": {
            "en": "exit-code <code>\n  Exits with the specified code (0-255).",
            "es": "exit-code <codigo>\n  Sale con el código especificado (0-255).",
        },
        "help": {
            "en": "help [command]\n  Shows help for a command or lists all commands.",
            "es": "help [comando]\n  Muestra ayuda para un comando o lista todos los comandos.",
        },
    }

    if command in help_texts:
        lang_texts = help_texts[command]
        if lang and lang in lang_texts:
            return lang_texts[lang]
        return lang_texts.get("en")

    return None


def _cmd_echo(args: list[str]) -> int:
    """Echo command - prints arguments to stdout."""
    if args:
        print(" ".join(args))
    else:
        print("(empty)")
    return 0


def _cmd_fail(args: list[str]) -> int:
    """Fail command - exits with code 1."""
    if args:
        print(" ".join(args), file=sys.stderr)
    else:
        print("Test addon failed as requested", file=sys.stderr)
    return 1


def _cmd_stdout(args: list[str]) -> int:
    """Stdout command - prints to stdout."""
    if args:
        print(" ".join(args))
    else:
        print("stdout test")
    return 0


def _cmd_stderr(args: list[str]) -> int:
    """Stderr command - prints to stderr."""
    if args:
        print(" ".join(args), file=sys.stderr)
    else:
        print("stderr test", file=sys.stderr)
    return 0


def _cmd_exit_code(args: list[str]) -> int:
    """Exit code command - exits with specified code."""
    if not args:
        print("Usage: exit-code <code>", file=sys.stderr)
        return 1
    try:
        code = int(args[0])
        if 0 <= code <= 255:
            return code
        print("Exit code must be between 0 and 255", file=sys.stderr)
        return 1
    except ValueError:
        print(f"Invalid exit code: {args[0]}", file=sys.stderr)
        return 1


def _cmd_help(args: list[str]) -> int:
    """Help command."""
    if args:
        help_text = get_help(args[0])
        if help_text:
            print(help_text)
        else:
            print(f"No help available for: {args[0]}")
            return 1
    else:
        print("Test Addon Commands:")
        print("  echo <message>      - Prints message to stdout")
        print("  fail [message]      - Exits with code 1")
        print("  stdout <message>    - Prints to stdout")
        print("  stderr <message>    - Prints to stderr")
        print("  exit-code <code>    - Exits with specified code (0-255)")
        print("  help [command]      - Shows this help or command-specific help")
    return 0


if __name__ == "__main__":
    sys.exit(execute(sys.argv[1:]))