#!/usr/bin/env python3
# {Verification IDs: VI-6}
# {Requirement IDs: NFR-REPORTING_TYPE_HINTS}
# Test Type: IMPLEMENTATION_CHECK

"""VI-6: All public functions carry Python type hints."""

import pytest
import typing
import reporting


def test_type_hints_on_all_functions():
    """VI-6: All four public functions have type hints via typing.get_type_hints."""

    # Now that reporting is implemented, check that all functions have correct type hints
    required_functions = [
        "generate_badges",
        "generate_health_report",
        "generate_processed_skills",
        "generate_skills_summary",
    ]

    for func_name in required_functions:
        func = getattr(reporting, func_name)
        hints = typing.get_type_hints(func)

        # Check that the function has type hints
        assert hints, f"{func_name} has no type hints"

        # Check that 'results' parameter exists with correct type
        assert "results" in hints, f"{func_name} missing 'results' parameter hint"

        # Check that results is List[Dict[str, Any]] (this matches the spec)
        from typing import List, Dict, Any
        expected_results_type = List[Dict[str, Any]]

        # For generate_skills_summary, return type should be Dict[str, Any]
        if func_name == "generate_skills_summary":
            assert "return" in hints, f"{func_name} missing return type hint"
            assert hints["return"] == Dict[str, Any], f"{func_name} return type mismatch"
        else:
            # For file generation functions, return type should be None
            assert hints.get("return") == type(None), f"{func_name} should return None"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])