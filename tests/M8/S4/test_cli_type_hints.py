#!/usr/bin/env python3
# {Verification IDs: VI-12}
# {Requirement IDs: NFR-CLI_TYPE_HINTS}
# Test Type: IMPLEMENTATION_CHECK

"""VI-12: All public functions carry Python type hints.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import typing

import pytest

REQUIRED_FUNCTIONS = [
    "parse_arguments",
    "validate_single_skill",
    "process_all_skills",
    "run_health_check",
    "print_help",
    "generate_all_reports",
]


def test_all_functions_have_type_hints():
    """VI-12: All six public functions have type annotations."""
    import cli

    for func_name in REQUIRED_FUNCTIONS:
        func = getattr(cli, func_name)
        hints = typing.get_type_hints(func)
        assert isinstance(
            hints, dict
        ), f"{func_name}: get_type_hints returned {type(hints)}"
        assert len(hints) > 0, f"{func_name} has no type annotations"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
