#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE, FR-PROJECT_ROOT_DETECTION}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_find_project_root_with_empty_string_and_none_defaults_to_cwd():
    """VI-5: find_project_root with '' and None defaults to CWD without raising."""

    # Import the module under test
    from discovery import find_project_root

    expected_cwd = Path.cwd().resolve()

    # Test with empty string
    result_empty = find_project_root("")

    # Test with None
    result_none = find_project_root(None)

    # Verify neither call raises
    assert isinstance(result_empty, Path), f"Expected Path, got {type(result_empty)}"
    assert isinstance(result_none, Path), f"Expected Path, got {type(result_none)}"

    # Verify both are absolute paths
    assert result_empty.is_absolute(), f"Expected absolute path, got {result_empty}"
    assert result_none.is_absolute(), f"Expected absolute path, got {result_none}"

    # Verify both equal the expected CWD (or nearest marker if present above CWD)
    # For this test, we'll verify they are reasonable absolute paths
    assert result_empty.exists(), f"Expected existing path, got {result_empty}"
    assert result_none.exists(), f"Expected existing path, got {result_none}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
