#!/usr/bin/env python3
# {Verification IDs: VI-7}
# {Requirement IDs: NFR-REPORTING_MODULAR_INDEPENDENCE}
# Test Type: IMPLEMENTATION_CHECK

"""VI-7: reporting.py and its test file import only stdlib + discovery."""

import ast
from pathlib import Path

import pytest

# Forbidden imports for reporting.py (self-import 'reporting' excluded)
FORBIDDEN_MODULES = {"cli", "main", "core", "core.validation", "healthcheck"}

REPORTING_PY = Path("reporting.py")
TEST_FILE = Path(__file__).resolve()


def _extract_imports(filepath: Path) -> set[str]:
    """Parse a Python file and return the set of top-level import module names."""
    source = filepath.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_level = alias.name.split(".")[0]
                imports.add(top_level)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                top_level = node.module.split(".")[0]
                imports.add(top_level)
    return imports


def test_reporting_py_import_audit():
    """VI-7: reporting.py contains no forbidden imports.

    Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
    """
    import reporting

    imports = _extract_imports(REPORTING_PY)
    forbidden_found = imports & FORBIDDEN_MODULES
    assert not forbidden_found, f"Forbidden imports in reporting.py: {forbidden_found}"


def test_test_file_import_audit():
    """VI-7: This test file contains no forbidden imports."""
    imports = _extract_imports(TEST_FILE)
    forbidden_found = imports & FORBIDDEN_MODULES
    assert not forbidden_found, f"Forbidden imports in test file: {forbidden_found}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
