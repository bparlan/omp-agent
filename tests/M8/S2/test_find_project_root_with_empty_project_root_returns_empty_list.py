#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_find_project_root_with_empty_project_root_returns_empty_list():
    """VI-18: discover_skills against a non-existent project root returns []."""

    # Import the module under test
    from discovery import discover_skills

    # Create a non-existent project root
    non_existent_project_root = Path("/nonexistent/path/unique-marker-abc")

    # Run the function under test
    result = discover_skills(non_existent_project_root)

    # Verify the function returns an empty list
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert result == [], f"Expected empty list, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
