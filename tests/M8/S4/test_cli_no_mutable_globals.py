#!/usr/bin/env python3
# {Verification IDs: VI-11}
# {Requirement IDs: NFR-CLI_NO_MUTABLE_GLOBALS}
# Test Type: IMPLEMENTATION_CHECK

"""VI-11: cli.py has no module-level mutable global state.

Pre-implementation: FileNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import ast
from pathlib import Path

import pytest

CLI_PY = Path("cli.py")


def _find_mutable_globals(filepath: Path) -> list[str]:
    """Find module-level assignments with mutable values (list, dict, set literals or calls)."""
    source = filepath.read_text(encoding="utf-8")
    tree = ast.parse(source)

    mutable_types = (ast.List, ast.Dict, ast.Set)
    mutable_nodes: list[str] = []

    for node in tree.body:
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
                ast.Import,
                ast.ImportFrom,
            ),
        ):
            continue

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and isinstance(
                    node.value, mutable_types
                ):
                    mutable_nodes.append(f"{target.id} = {type(node.value).__name__}")

        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and isinstance(
                node.value, mutable_types
            ):
                mutable_nodes.append(
                    f"{node.target.id}: ... = {type(node.value).__name__}"
                )

        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                mutable_nodes.append(f"{node.target.id} {type(node.op).__name__}=")

    return mutable_nodes


def test_no_mutable_globals():
    """VI-11: cli.py has zero module-level mutable bindings.

    Pre-implementation: FileNotFoundError is the expected VALID_INITIAL_FAILURE.
    """
    mutable = _find_mutable_globals(CLI_PY)
    assert len(mutable) == 0, f"Module-level mutable globals found: {mutable}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
