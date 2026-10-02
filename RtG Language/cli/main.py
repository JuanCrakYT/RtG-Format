"""CLI entry point for RtG-Language compiler."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import from parent package
sys.path.insert(0, str(Path(__file__).parent.parent))

from rtg_language import compile_file, CompileOptions, DiagnosticCollector


def main(argv: list[str] | None = None) -> int:
    """Main entry point for rtg-language compiler."""
    parser = argparse.ArgumentParser(
        prog="rtg-language",
        description="RtG-Language 2.0 compiler - compiles .rtg files to RtG-Format JSON",
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input .rtg file",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output JSON file",
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        help="Directory containing schema files",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Directory for cache files (default: project root)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable cache",
    )
    parser.add_argument(
        "--ast",
        action="store_true",
        help="Print AST as JSON",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="RtG-Language 0.1.0",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args(argv)

    options = CompileOptions(
        schema_dir=args.schema_dir,
        cache_dir=args.cache_dir or args.input.parent,
        use_cache=not args.no_cache,
        output_path=args.output,
    )

    result = compile_file(args.input, options)

    # Print diagnostics
    for diag in result.diagnostics:
        print(diag, file=sys.stderr)

    if args.ast and result.ast:
        import json
        print(json.dumps(result.ast, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o), indent=2, ensure_ascii=False))

    if not result.success:
        return 1

    if result.build and not args.output:
        # Print to stdout if no output file specified
        import json
        print(json.dumps(result.build, ensure_ascii=False, indent=2))

    if args.verbose:
        cache_status = " (from cache)" if result.cache_used else ""
        print(f"Compiled successfully{cache_status}. {len(result.build)} objects.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())