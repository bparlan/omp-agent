#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_MODULE_EXPORTS}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_discover_skills_accepts_path_and_str_equivalently():
    """VI-2: discover_skills accepts both Path and str equivalently."""

    # Import the module under test
    from discovery import discover_skills

    # Verify preconditions - fixture directory exists
    fixture_root = Path("tests/fixtures/discovery/synthetic_project")
    assert fixture_root.exists(), f"Fixture directory {fixture_root} does not exist"

    # Run the function under test with Path argument
    path_result = discover_skills(fixture_root)

    # Run the function under test with str argument
    str_result = discover_skills(str(fixture_root))

    # Verify both invocations return equal lists
    assert path_result == str_result, f"Path result {path_result} differs from str result {str_result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
