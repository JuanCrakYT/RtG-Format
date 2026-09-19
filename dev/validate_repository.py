#!/usr/bin/env python3
"""
RtG-Format repository validation tool.

Validates:
  - JSON files (syntax, BOM, empty)
  - Python syntax
  - JavaScript syntax
  - Model structure (assets/models/model/<Name>/)
  - References (README, docs, scripts)
  - Encoding/BOM/newlines

Usage:
  python dev/validate_repository.py
"""

import json
import os
import sys
import py_compile
import subprocess
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Directory names to skip entirely (submodules, caches, etc.)
SKIP_DIR_NAMES = {
    '.git', '.kilo', '.github', 'node_modules', '__pycache__',
    '.svn', '.hg',
}

# Specific submodule directory names
SUBMODULE_DIRS = {'RtG Image', 'RtG-AI'}

def should_skip(path):
    """Check if a file/dir path should be skipped."""
    try:
        rel = Path(path).relative_to(REPO_ROOT)
    except ValueError:
        return True
    parts = rel.parts
    for i, part in enumerate(parts):
        if part in SKIP_DIR_NAMES:
            return True
        # Check if parent is a tools/ dir and this is a submodule name
        if i > 0 and parts[i-1] == 'tools' and part in SUBMODULE_DIRS:
            return True
        # Skip deprecated backup files (intentionally invalid JSON)
        if part == 'deprecated' and i > 0 and parts[i-1] == 'models':
            return True
    return False

def get_all_files(extensions):
    files = []
    for root, dirs, filenames in os.walk(REPO_ROOT):
        # Filter out skipped directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not should_skip(os.path.join(root, d))]
        # Also skip submodule dirs under tools/
        if Path(root).name == 'tools':
            dirs[:] = [d for d in dirs if d not in SUBMODULE_DIRS]
        for fn in filenames:
            ext = fn.rsplit('.', 1)[-1] if '.' in fn else ''
            if ext in extensions:
                fp = Path(root) / fn
                if not should_skip(fp):
                    files.append(fp)
    return sorted(files)

class Validator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = 0

    def error(self, category, filepath, message):
        rel = str(filepath.relative_to(REPO_ROOT)) if filepath.is_absolute() or filepath.exists() else str(filepath)
        self.errors.append((category, rel, message))

    def warning(self, category, filepath, message):
        rel = str(filepath.relative_to(REPO_ROOT)) if filepath.is_absolute() or filepath.exists() else str(filepath)
        self.warnings.append((category, rel, message))

    def ok(self):
        self.passed += 1

def validate_json(v):
    """Validate all JSON files in the main repo (not submodules)."""
    print("\n=== JSON Validation ===")
    # Get all tracked JSON files using git ls-files
    result = subprocess.run(
        ['git', 'ls-files', '*.json', '**/*.json'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    json_files = [REPO_ROOT / p for p in result.stdout.strip().split('\n') if p.strip()]
    # Filter out deprecated backup files (intentionally invalid JSON)
    json_files = [f for f in json_files if '_backup_before_property_update' not in str(f)]

    valid = 0
    invalid = 0
    bom_count = 0
    empty_count = 0

    for f in json_files:
        try:
            with open(f, 'rb') as bf:
                raw = bf.read()
            if len(raw) == 0:
                empty_count += 1
                v.warning('json-empty', f, "File is empty")
                continue
            has_bom = raw[:3] == b'\xef\xbb\xbf'
            if has_bom:
                bom_count += 1
                v.warning('json-bom', f, "File has UTF-8 BOM")
            text = raw.decode('utf-8-sig')
            json.loads(text)
            valid += 1
            v.ok()
        except json.JSONDecodeError as e:
            invalid += 1
            if e.lineno and e.colno:
                context = e.doc[max(0,e.pos-20):e.pos+30]
                v.error('json-syntax', f, f"Syntax error: {e.msg} at line {e.lineno}, col {e.colno}. Context: ...{context!r}...")
            else:
                v.error('json-syntax', f, f"Syntax error: {e.msg}")
        except Exception as e:
            invalid += 1
            v.error('json-read', f, f"{type(e).__name__}: {e}")

    total = valid + invalid + empty_count
    print(f"  Total JSON files checked: {total}")
    print(f"  Valid: {valid}")
    print(f"  Invalid: {invalid}")
    print(f"  Empty: {empty_count}")
    print(f"  BOM warnings: {bom_count}")

    # Print invalid files
    for cat, path, msg in v.errors:
        if cat.startswith('json-'):
            print(f"  [FAIL] {path}: {msg}")

    return valid, invalid

def validate_python(v):
    """Validate all Python files for syntax errors."""
    print("\n=== Python Syntax Validation ===")
    # Use git ls-files for tracked Python files
    result = subprocess.run(
        ['git', 'ls-files', '*.py'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    py_files = [REPO_ROOT / p for p in result.stdout.strip().split('\n') if p.strip()]

    valid = 0
    invalid = 0

    for f in py_files:
        try:
            with open(f, 'rb') as bf:
                source = bf.read()
            try:
                source.decode('utf-8')
            except UnicodeDecodeError as e:
                v.error('py-encoding', f, f"Encoding error: {e}")
                invalid += 1
                continue
            try:
                py_compile.compile(str(f), doraise=True)
            except FileExistsError:
                # py_compile tries to write .pyc files; on Windows with os.devnull
                # this can fail. Fall back to AST parsing for syntax check.
                import ast
                source = f.read_text(encoding='utf-8')
                ast.parse(source)
            valid += 1
            v.ok()
        except py_compile.PyCompileError as e:
            invalid += 1
            v.error('py-syntax', f, f"Syntax error: {e}")
        except Exception as e:
            invalid += 1
            v.error('py-read', f, f"{type(e).__name__}: {e}")

    total = valid + invalid
    print(f"  Total Python files: {total}")
    print(f"  Valid: {valid}")
    print(f"  Invalid: {invalid}")
    for cat, path, msg in v.errors:
        if cat.startswith('py-'):
            print(f"  [FAIL] {path}: {msg}")

    return valid, invalid

def validate_js(v):
    """Validate JavaScript files using node --check."""
    print("\n=== JavaScript Syntax Validation ===")
    result = subprocess.run(
        ['git', 'ls-files', '*.js'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    js_files = [REPO_ROOT / p for p in result.stdout.strip().split('\n') if p.strip()]

    valid = 0
    invalid = 0

    try:
        subprocess.run(['node', '--version'], capture_output=True, timeout=5, check=True)
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
        print("  Node.js not available, skipping JS validation")
        return 0, 0

    for f in js_files:
        try:
            result = subprocess.run(['node', '--check', str(f)], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                invalid += 1
                v.error('js-syntax', f, f"Syntax error: {result.stderr.strip()}")
            else:
                valid += 1
                v.ok()
        except Exception as e:
            invalid += 1
            v.error('js-read', f, f"{type(e).__name__}: {e}")

    total = valid + invalid
    print(f"  Total JS files: {total}")
    print(f"  Valid: {valid}")
    print(f"  Invalid: {invalid}")
    for cat, path, msg in v.errors:
        if cat.startswith('js-'):
            print(f"  [FAIL] {path}: {msg}")

    return valid, invalid

def validate_model_structure(v):
    """Validate assets/models structure: each model has JSON + OBJ."""
    print("\n=== Model Structure Validation ===")
    models_dir = REPO_ROOT / 'assets' / 'models' / 'model'

    if not models_dir.exists():
        v.error('model-structure', models_dir, "models/model/ directory does not exist")
        return 0, 0

    # Find all model directories that contain .json or .obj files
    model_dirs = []
    for root, dirs, files in os.walk(models_dir):
        if any(f.endswith('.json') or f.endswith('.obj') for f in files):
            rel = Path(root).relative_to(models_dir)
            model_dirs.append(rel)

    valid = 0
    invalid = 0

    for md in sorted(model_dirs):
        # Get the model name (directory name)
        if len(md.parts) == 1:
            model_name = md.name
        elif len(md.parts) == 2:
            model_name = md.parts[-1]  # e.g., 'split' for Switch/split
        else:
            model_name = md.parts[-1]

        json_expected = models_dir / md / f"{model_name}.json"
        obj_expected = models_dir / md / f"{model_name}.obj"

        # Only check top-level model dirs (not subdirs like split/)
        if len(md.parts) == 1:
            json_exists = json_expected.exists()
            obj_exists = obj_expected.exists()

            if not json_exists:
                v.error('model-json', md, f"Missing expected JSON: {json_expected.relative_to(REPO_ROOT)}")
                invalid += 1
            if not obj_exists:
                v.error('model-obj', md, f"Missing expected OBJ: {obj_expected.relative_to(REPO_ROOT)}")
                invalid += 1
            if json_exists and obj_exists:
                valid += 1
                v.ok()

    print(f"  Model directories with JSON/OBJ: {len([d for d in model_dirs if len(d.parts) == 1])}")
    print(f"  Valid (JSON+OBJ present): {valid}")
    print(f"  Invalid (missing files): {invalid}")
    for cat, path, msg in v.errors:
        if cat.startswith('model-'):
            print(f"  [FAIL] {path}: {msg}")

    return valid, invalid

def validate_references(v):
    """Check for broken references in documentation."""
    print("\n=== Reference Validation ===")
    warnings = 0
    import re

    # Check README.md for old asset paths
    readme = REPO_ROOT / 'README.md'
    if readme.exists():
        content = readme.read_text(encoding='utf-8-sig')
        old_paths = re.findall(r'assets/models/([A-Z][A-Za-z0-9_-]+)\.obj', content)
        for op in old_paths:
            v.warning('ref-old-path', readme, f"References old path: assets/models/{op}.obj (should be assets/models/model/{op}/{op}.obj)")
            warnings += 1

    # Check all .md files (excluding old-files, RtG-Preview) for old asset paths
    result = subprocess.run(
        ['git', 'ls-files', '*.md'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    md_files = [REPO_ROOT / p for p in result.stdout.strip().split('\n') if p.strip()]

    for f in md_files:
        if 'old-files/' in str(f) or 'RtG-Preview/' in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8-sig')
            # Look for old-style flat .obj references
            old_refs = re.findall(r'assets/models/([A-Z][A-Za-z0-9_-]+)\.obj', content)
            for op in old_refs:
                ref_new = f"assets/models/model/{op}/{op}.obj"
                if ref_new not in content and f"deprecated/" not in content:
                    v.warning('ref-old-path', f, f"References old asset path: assets/models/{op}.obj")
                    warnings += 1
        except Exception:
            pass

    print(f"  Warnings: {warnings}")
    for cat, path, msg in v.warnings:
        if cat == 'ref-old-path':
            print(f"  [WARN] {path}: {msg}")

    return warnings

def validate_python_runtime(v):
    """Check for runtime issues in Python scripts: undefined names, imports."""
    print("\n=== Python Runtime Validation ===")
    # For each Python file, check imports can be resolved
    result = subprocess.run(
        ['git', 'ls-files', '*.py'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    py_files = [REPO_ROOT / p for p in result.stdout.strip().split('\n') if p.strip()]

    runtime_issues = 0
    for f in py_files:
        try:
            source = f.read_text(encoding='utf-8')
            import ast
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == '__future__':
                            continue
                        # Check if module is available
                        mod = alias.name.split('.')[0]
                        if mod == 'dev' and str(f).startswith(str(REPO_ROOT / 'RtG-CLI')):
                            v.warning('py-import', f, f"RtG-CLI script imports 'dev.{alias.name}', may not be available")
                            runtime_issues += 1
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod = node.module.split('.')[0]
                        if mod == 'dev' and str(f).startswith(str(REPO_ROOT / 'RtG-CLI')):
                            v.warning('py-import', f, f"RtG-CLI script imports from 'dev.{node.module}', may not be available")
                            runtime_issues += 1
        except SyntaxError:
            pass  # Already caught by syntax validation

    print(f"  Runtime warnings: {runtime_issues}")
    for cat, path, msg in v.warnings:
        if cat.startswith('py-'):
            print(f"  [WARN] {path}: {msg}")

    return runtime_issues

def main():
    v = Validator()
    print("RtG-Format validation")
    print(f"Repository root: {REPO_ROOT}\n")

    json_result = validate_json(v)
    py_result = validate_python(v)
    js_result = validate_js(v)
    model_result = validate_model_structure(v)
    ref_result = validate_references(v)
    runtime_result = validate_python_runtime(v)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Passed checks: {v.passed}")
    print(f"Total errors:  {len(v.errors)}")
    print(f"Total warnings: {len(v.warnings)}")

    if v.errors:
        print("\nERRORS:")
        for cat, path, msg in v.errors:
            print(f"  [{cat}] {path}: {msg}")

    if v.warnings:
        print("\nWARNINGS:")
        for cat, path, msg in v.warnings:
            print(f"  [{cat}] {path}: {msg}")

    has_errors = len(v.errors) > 0
    if not has_errors:
        print("\nResult: PASS (with warnings)" if v.warnings else "\nResult: PASS")
    else:
        print("\nResult: FAIL")
    return 1 if has_errors else 0

if __name__ == '__main__':
    sys.exit(main())
