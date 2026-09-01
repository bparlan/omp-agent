#!/usr/bin/env python3
# {Verification IDs: VI-10}
# {Requirement IDs: NFR-CLI_FILE_SCOPE}
# Test Type: IMPLEMENTATION_CHECK

"""VI-10: cli.py imports only allowed modules.

Pre-implementation: FileNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import ast
from pathlib import Path

import pytest

CLI_PY = Path("cli.py")

FORBIDDEN_MODULES = {"main", "index.js", "healthcheck", "healthcheck.py"}


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


def test_cli_py_no_forbidden_imports():
    """VI-10: cli.py contains no forbidden imports.

    Pre-implementation: FileNotFoundError is the expected VALID_INITIAL_FAILURE.
    """
    imports = _extract_imports(CLI_PY)
    forbidden_found = imports & FORBIDDEN_MODULES
    assert not forbidden_found, f"Forbidden imports in cli.py: {forbidden_found}"


FORBIDDEN_TEST_IMPORTS = {"main", "index.js", "healthcheck", "healthcheck.py"}

ALLOWED_TEST_IMPORTS = {
    "cli",
    "pytest",
    "ast",
    "sys",
    "pathlib",
    "typing",
    "unittest",
    "mock",
    "io",
    "json",
    "subprocess",
}

TEST_DIR = Path("tests/M8/S4")


def test_test_files_no_forbidden_imports():
    """VI-13: Test files in tests/M8/S4/ contain no forbidden imports."""
    test_files = sorted(TEST_DIR.glob("test_*.py"))
    assert len(test_files) > 0, f"No test files found in {TEST_DIR}"

    for test_file in test_files:
        imports = _extract_imports(test_file)
        forbidden_found = imports & FORBIDDEN_TEST_IMPORTS
        assert (
            not forbidden_found
        ), f"Forbidden imports in {test_file}: {forbidden_found}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
