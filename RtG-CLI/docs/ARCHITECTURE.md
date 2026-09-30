# RtG-CLI Architecture

## Overview

RtG-CLI is a modular command-line interface for the RtG-Format ecosystem. It provides a stable foundation for executing addons, managing languages, and serving as an integration point for future tools like RtG-Language.

## Component Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                        rtg.py (Entry Point)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Application (application.py)                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ Configuration│ │  Arguments  │ │   Languages │ │Diagnostics│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │   Addons    │ │ Execution   │ │    Help     │ │  Version  │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Command Dispatch                             │
│  ┌──────────────────┐         ┌────────────────────────────┐   │
│  │ Internal Commands│         │         Addons             │   │
│  │  - help          │         │  - image                   │   │
│  │  - version       │         │  - preview                 │   │
│  │  - rules         │         │  - test-addon              │   │
│  │  - lang          │         │                            │   │
│  │  - commands      │         │  Program Command Interface │   │
│  │  - addons        │         │  ┌──────────────────────┐  │   │
│  │  - language      │         │  │ Python (.py)         │  │   │
│  └──────────────────┘         │  │ JavaScript (.js)     │  │   │
│                               │  └──────────────────────┘  │   │
│                               └────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Module Responsibilities

### `application.py`
Main application class that orchestrates all subsystems. Entry point for the CLI.

### `configuration.py`
- Loads and validates `assets.json`
- Resolves relative paths to absolute paths
- Provides typed configuration objects (`CliConfig`, `AddonConfig`, `AssetPaths`)
- Validates required fields and structure

### `arguments.py`
- Formal argument parser supporting:
  - Commands and subcommands
  - Short (`-x`) and long (`--option`) options
  - Options with values
  - Positional arguments
  - Language selectors (`-en`, `-es`, etc.)
  - Addon argument separation (single hyphen = CLI, double hyphen/no hyphen = addon)
- Returns structured `ParsedCommandLine` with diagnostics

### `languages.py`
- Manages 19 languages (12 from RtG-AI + 7 additional)
- Tracks availability per category: CLI, Help, Rules, Void, Version, Addons
- Provides validation, default selection, and formatted listing
- Language codes follow ISO/BCP-47

### `diagnostics.py`
- Structured error system with categories and exit codes
- `Diagnostic` dataclass with message, category, exit code, debug info
- Pre-defined error factories for common cases
- `DiagnosticHandler` for consistent output and exit handling
- No tracebacks by default; debug mode available

### `addons.py`
- `AddonRegistry`: Discovers, validates, and manages addons
- Distinguishes registered vs documented addons
- `ProgramCommandInterface` abstraction for Python/JS execution
- Loads program command interfaces from configured paths

### `execution.py`
- `AddonExecutor`: Executes addons via their program command interface
- `InternalCommandExecutor`: Executes internal CLI commands
- Handles argument separation after addon identification
- Manages stdout/stderr/exit code propagation

### `help.py`
- Loads help content from external Markdown files
- Supports multiple languages
- Separates help from rules content
- Provides formatted output for commands, addons, languages

### `version.py`
- Manages version information for CLI and addons
- Multi-language version content support
- Single source of truth for version data

## Data Flow

```text
argv → ArgumentParser → ParsedCommandLine
                    ↓
         ┌──────────┴──────────┐
         ▼                     ▼
   Internal Command        Addon Identified
         ▼                     ▼
   InternalExecutor      AddonExecutor
         ▼                     ▼
   Program Interface ←───── Program Commands
         ▼                     ▼
      Exit Code ──────────► Exit Code
```

## Extension Points

1. **New Internal Commands**: Add to `internal-list` in assets.json, implement in `InternalCommandExecutor`
2. **New Addons**: Add to `addons` in assets.json with program command paths
3. **New Languages**: Add to `language-names` and provide help/rules/void files
4. **New Program Command Interfaces**: Implement `ProgramCommandInterface` for new languages

## Design Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Configuration-Driven**: Behavior defined in assets.json, not code
- **Formal Contracts**: Explicit interfaces between components
- **No Implicit Behavior**: All argument ownership rules are explicit
- **Extensible**: New commands/addons/languages without core changes