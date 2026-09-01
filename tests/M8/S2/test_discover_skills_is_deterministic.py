#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DETERMINISTIC_SORT_ORDER}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_discover_skills_is_deterministic():
    """VI-11: discover_skills is deterministic across repeated invocations."""

    # Import the module under test
    from discovery import discover_skills

    # Verify preconditions - fixture directory exists
    fixture_root = Path("tests/fixtures/discovery/synthetic_project")
    assert fixture_root.exists(), f"Fixture directory {fixture_root} does not exist"

    # Run the function twice with the same Path argument
    result1 = discover_skills(fixture_root)
    result2 = discover_skills(fixture_root)

    # Verify both results are lists of strings
    assert isinstance(result1, list), f"Expected list, got {type(result1)}"
    assert isinstance(result2, list), f"Expected list, got {type(result2)}"

    assert all(
        isinstance(item, str) for item in result1
    ), f"Expected all strings, got {[type(item) for item in result1]}"
    assert all(
        isinstance(item, str) for item in result2
    ), f"Expected all strings, got {[type(item) for item in result2]}"

    # Verify both results are equal (byte-equal comparison)
    assert (
        result1 == result2
    ), f"Results differ: first call {result1}, second call {result2}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
