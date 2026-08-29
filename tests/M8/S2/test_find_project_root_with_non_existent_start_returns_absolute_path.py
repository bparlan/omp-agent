#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE, FR-PROJECT_ROOT_DETECTION}
# Test Type: IMPLEMENTATION_CHECK

import pytest
import tempfile
from pathlib import Path


def test_find_project_root_with_non_existent_start_returns_absolute_path():
    """VI-17: find_project_root with non-existent start returns absolute path without raising."""

    # Import the module under test
    from discovery import find_project_root

    # Create a non-existent path
    non_existent_path = Path("/nonexistent/path/that/does/not/exist/anywhere/unique-marker-xyz")

    # Run the function under test
    result = find_project_root(non_existent_path)

    # Verify the function does not raise

    # Verify returned value is a Path
    assert isinstance(result, Path), f"Expected Path, got {type(result)}"

    # Verify the returned path is absolute
    assert result.is_absolute(), f"Expected absolute path, got {result}"

    # Verify the returned path resolves to the input path
    expected_path = non_existent_path.resolve()
    assert result == expected_path, f"Expected {expected_path}, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
