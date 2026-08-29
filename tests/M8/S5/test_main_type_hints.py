#!/usr/bin/env python3
# V-005
# FR-MAIN_TYPE_HINTS
# Test Type: SPECIFICATION_CHECK

"""Static analysis test for main.py type hints (V-005).

Pre-implementation: main.py does not exist.
Expected VALID_INITIAL_FAILURE: test error with exit code 1.
"""

import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MAIN_PY = PROJECT_ROOT / "main.py"


def test_main_py_type_hints_complete():
    """V-005: All public functions in main.py must have complete type annotations."""
    assert MAIN_PY.is_file(), f"main.py not found at {MAIN_PY}"

    source = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(source)

    # Find top-level function definitions (public interface)
    public_functions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            public_functions.append(node)

    assert public_functions, "main.py must define at least one public function"

    # Check each public function has complete annotations
    for func in public_functions:
        # Check return annotation
        assert func.returns is not None, (
            f"Public function '{func.name}' missing return type annotation"
        )

        # Check all parameters have annotations (excluding 'self' for methods)
        args = func.args
        all_args = args.posonlyargs + args.args + args.kwonlyargs
        vararg = args.vararg
        kwarg = args.kwarg

        for arg in all_args:
            if arg.arg != "self":
                assert arg.annotation is not None, (
                    f"Parameter '{arg.arg}' in function '{func.name}' missing type annotation"
                )

        if vararg and vararg.arg != "self":
            assert vararg.annotation is not None, (
                f"Variadic parameter '{vararg.arg}' in function '{func.name}' missing type annotation"
            )

        if kwarg:
            assert kwarg.annotation is not None, (
                f"Keyword parameter '{kwarg.arg}' in function '{func.name}' missing type annotation"
            )


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
