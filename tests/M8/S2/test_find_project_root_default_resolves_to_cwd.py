#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE, FR-PROJECT_ROOT_DETECTION}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_find_project_root_default_resolves_to_cwd():
    """VI-4: find_project_root default argument resolves to absolute Path.cwd()."""

    # Import the module under test
    from discovery import find_project_root

    # Test with no arguments
    result_no_args = find_project_root()

    # Test with None argument
    result_none_args = find_project_root(None)

    # Verify both return the same absolute path
    expected_cwd = Path.cwd().resolve()

    assert isinstance(
        result_no_args, Path
    ), f"Expected Path, got {type(result_no_args)}"
    assert isinstance(
        result_none_args, Path
    ), f"Expected Path, got {type(result_none_args)}"

    assert result_no_args.is_absolute(), f"Expected absolute path, got {result_no_args}"
    assert (
        result_none_args.is_absolute()
    ), f"Expected absolute path, got {result_none_args}"

    assert (
        result_no_args == expected_cwd
    ), f"Expected {expected_cwd}, got {result_no_args}"
    assert (
        result_none_args == expected_cwd
    ), f"Expected {expected_cwd}, got {result_none_args}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
