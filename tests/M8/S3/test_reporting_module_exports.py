#!/usr/bin/env python3
# {Verification IDs: VI-1}
# {Requirement IDs: FR-REPORTING_MODULE_EXPORTS}
# Test Type: IMPLEMENTATION_CHECK

"""VI-1: reporting module imports and exports all four functions."""

import pytest


def test_reporting_module_importable():
    """Verify reporting.py can be imported without side effects."""
    # Import the module under test — ModuleNotFoundError is the expected
    # pre-implementation failure (VALID_INITIAL_FAILURE).
    import reporting  # noqa: F401


def test_reporting_exports_four_functions():
    """Verify all four required functions are present and callable."""
    import reporting

    required_functions = [
        "generate_badges",
        "generate_health_report",
        "generate_processed_skills",
        "generate_skills_summary",
    ]

    for func_name in required_functions:
        assert hasattr(reporting, func_name), f"reporting module missing '{func_name}'"
        func = getattr(reporting, func_name)
        assert callable(func), f"'{func_name}' is not callable"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
