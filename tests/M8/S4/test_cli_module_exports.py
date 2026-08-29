#!/usr/bin/env python3
# {Verification IDs: VI-1, VI-14}
# {Requirement IDs: FR-CLI_MODULE_EXPORTS}
# Test Type: IMPLEMENTATION_CHECK

"""VI-1: cli module imports and exports all six functions.
VI-14: __all__ tuple defined and lists all six exports.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import pytest

REQUIRED_FUNCTIONS = [
    "parse_arguments",
    "validate_single_skill",
    "process_all_skills",
    "run_health_check",
    "print_help",
    "generate_all_reports",
]


def test_cli_module_importable():
    """VI-1: cli.py can be imported without side effects."""
    import cli  # noqa: F401


def test_cli_exports_all_functions():
    """VI-1: All six required functions are present and callable."""
    import cli

    for func_name in REQUIRED_FUNCTIONS:
        assert hasattr(cli, func_name), f"cli module missing '{func_name}'"
        func = getattr(cli, func_name)
        assert callable(func), f"'{func_name}' is not callable"


def test_cli_all_tuple_complete():
    """VI-14: __all__ contains exactly the six public exports."""
    import cli

    assert hasattr(cli, "__all__"), "cli module missing __all__ tuple"
    all_list = list(cli.__all__)
    assert len(all_list) == 6, f"__all__ has {len(all_list)} entries, expected 6"
    for func_name in REQUIRED_FUNCTIONS:
        assert func_name in all_list, f"'{func_name}' missing from __all__"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
