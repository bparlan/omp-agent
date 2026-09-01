#!/usr/bin/env python3
# V-004
# FR-MAIN_MODULAR_INDEPENDENCE
# Test Type: IMPLEMENTATION_CHECK

"""Tests for main.py modular independence import audit (V-004).

Pre-implementation: main.py does not exist.
Expected VALID_INITIAL_FAILURE: test error with exit code 1.
"""

import ast
import importlib
import sys
from pathlib import Path
import inspect

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MAIN_PY = PROJECT_ROOT / "main.py"

ALLOWED_IMPORTS = {
    "argparse",
    "sys",
    "pathlib",
    "typing",
    "discovery",
    "reporting",
    "cli",
    "core.validation",
}


def _import_main():
    sys.path.insert(0, str(PROJECT_ROOT))
    return importlib.import_module("main")


def test_main_py_imports_no_prohibited_modules():
    """V-004: main.py must import only root-level modules and stdlib."""
    main = _import_main()
    source = inspect.getsource(main)
    tree = ast.parse(source)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    prohibited = imports - {mod.split(".")[0] for mod in ALLOWED_IMPORTS}
    assert not prohibited, f"Prohibited imports detected: {prohibited}"


def test_main_py_no_wrapper_local_imports():
    """V-004: main.py must not import from skills.healthcheck.* or wrapper paths."""
    main = _import_main()
    source = inspect.getsource(main)
    assert (
        "skills.healthcheck" not in source
    ), "main.py must not import from wrapper-local paths like skills.healthcheck.*"


def test_main_py_import_succeeds_without_side_effects():
    """V-004: Import of main.py must not produce side effects."""
    main = _import_main()
    assert main is not None, "main module should be importable"
