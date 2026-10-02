"""Main public API for RtG-Language compiler."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path
import json

from .lexer import tokenize, Token
from .parser import parse, File as ASTFile
from .resolver import resolve, ResolvedFile
from .compiler import compile_resolved, CompileResult
from .cache import Cache
from .schema import load_schema, create_default_schema, Schema
from .diagnostics import (
    DiagnosticCollector,
    Diagnostic,
    Severity,
    SourceLocation,
    Codes,
    make_diagnostic,
)


@dataclass
class CompileOptions:
    """Options for compilation."""
    schema_dir: Optional[Path] = None
    cache_dir: Optional[Path] = None
    use_cache: bool = True
    output_path: Optional[Path] = None


@dataclass
class CompileResultFull:
    """Complete compilation result."""
    success: bool
    build: Optional[list] = None
    diagnostics: DiagnosticCollector = None
    ast: Optional[ASTFile] = None
    resolved: Optional[ResolvedFile] = None
    cache_used: bool = False


def compile_file(
    source_path: Path,
    options: Optional[CompileOptions] = None,
) -> CompileResultFull:
    """Compile a .rtg file to RtG-Format."""
    options = options or CompileOptions()

    # Read source
    try:
        source = source_path.read_text(encoding='utf-8')
    except OSError as e:
        diagnostics = DiagnosticCollector()
        diagnostics.add(make_diagnostic(
            Codes.IO_FILE_NOT_FOUND,
            f"Failed to read source file: {e}",
            Severity.ERROR,
        ))
        return CompileResultFull(success=False, diagnostics=diagnostics)

    return compile_text(source, source_path, options)


def compile_text(
    source: str,
    source_path: Path,
    options: Optional[CompileOptions] = None,
) -> CompileResultFull:
    """Compile .rtg source text to RtG-Format."""
    options = options or CompileOptions()
    all_diagnostics = DiagnosticCollector()

    # Phase 1: Lexing
    tokens, lex_diagnostics = tokenize(source, str(source_path))
    all_diagnostics.diagnostics.extend(lex_diagnostics.diagnostics)
    if lex_diagnostics.has_errors():
        return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=None)

    # Phase 2: Parsing
    ast, parse_diagnostics = parse(source, str(source_path))
    all_diagnostics.diagnostics.extend(parse_diagnostics.diagnostics)
    if parse_diagnostics.has_errors() or ast is None:
        return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=None)

    # Phase 3: Schema loading
    schema = None
    schema_file = None
    if ast.schema:
        try:
            # Resolve schema path relative to source file directory
            schema_file = source_path.parent / ast.schema.source
            schema = load_schema(schema_file)
        except Exception as e:
            all_diagnostics.add(make_diagnostic(
                Codes.SCHEMA_MISSING,
                f"Failed to load schema: {e}",
                Severity.ERROR,
                ast.schema.location,
            ))
    elif options.schema_dir:
        # Try to load default schema from schema_dir
        try:
            schema_file = options.schema_dir / "schema.json"
            if schema_file.exists():
                schema = load_schema(schema_file)
            else:
                # Use built-in default schema
                schema = create_default_schema()
        except Exception as e:
            all_diagnostics.add(make_diagnostic(
                Codes.SCHEMA_MISSING,
                f"Failed to load default schema: {e}",
                Severity.WARNING,
            ))
            schema = create_default_schema()
    else:
        # Use built-in default schema if no schema_dir provided
        schema = create_default_schema()

    # Phase 4: Cache check
    cache_used = False
    cache = None
    cached_build = None
    if options.use_cache and options.cache_dir:
        cache_path = options.cache_dir / ".rtgcache"
        cache = Cache(cache_path)
        if schema_file:
            cached = cache.load(source_path, schema_file)
        else:
            cached = cache.load(source_path, None)
        if cached:
            # Use cached result
            all_diagnostics.diagnostics.extend(cached.diagnostics.diagnostics)
            cached_build = cached.build
            cache_used = True

    if cached_build is not None:
        # Write output if requested, even when using cache
        if options.output_path:
            try:
                output_path = options.output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with output_path.open('w', encoding='utf-8') as f:
                    json.dump(cached_build, f, ensure_ascii=False, indent=2)
            except OSError as e:
                all_diagnostics.add(make_diagnostic(
                    Codes.IO_FILE_NOT_FOUND,
                    f"Failed to write output: {e}",
                    Severity.ERROR,
                ))
                return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=ast)

        return CompileResultFull(
            success=True,
            build=cached_build,
            diagnostics=all_diagnostics,
            ast=ast,
            cache_used=True,
        )

    # Phase 5: Resolving
    resolved, resolve_diagnostics = resolve(ast, schema=schema)
    all_diagnostics.diagnostics.extend(resolve_diagnostics.diagnostics)
    if resolve_diagnostics.has_errors() or resolved is None:
        return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=ast)

    # Phase 6: Compilation
    compile_result = compile_resolved(resolved)
    all_diagnostics.diagnostics.extend(compile_result.diagnostics.diagnostics)
    if compile_result.diagnostics.has_errors():
        return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=ast, resolved=resolved)

    # Phase 7: Save cache
    if cache:
        cache.save(source_path, schema_file, compile_result)

    # Phase 8: Write output if requested
    if options.output_path:
        try:
            output_path = options.output_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(compile_result.build, f, ensure_ascii=False, indent=2)
        except OSError as e:
            all_diagnostics.add(make_diagnostic(
                Codes.IO_FILE_NOT_FOUND,
                f"Failed to write output: {e}",
                Severity.ERROR,
            ))
            return CompileResultFull(success=False, diagnostics=all_diagnostics, ast=ast, resolved=resolved)

    return CompileResultFull(
        success=True,
        build=compile_result.build,
        diagnostics=all_diagnostics,
        ast=ast,
        resolved=resolved,
    )


def compile_string(source: str, file_name: str = "<string>") -> CompileResultFull:
    """Compile source string (for testing)."""
    from pathlib import Path
    return compile_text(source, Path(file_name))


__version__ = "0.1.0"

__all__ = [
    "compile_file",
    "compile_text",
    "compile_string",
    "CompileOptions",
    "CompileResultFull",
    "DiagnosticCollector",
    "Diagnostic",
    "Severity",
    "SourceLocation",
    "Codes",
    "Cache",
    "Schema",
    "load_schema",
    "create_default_schema",
    "Token",
    "tokenize",
    "parse",
    "resolve",
    "compile_resolved",
]