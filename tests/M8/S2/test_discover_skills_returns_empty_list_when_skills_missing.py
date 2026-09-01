#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE, FR-SKILL_LISTING_FROM_FIXTURE}
# Test Type: IMPLEMENTATION_CHECK

import pytest
import tempfile
from pathlib import Path


def test_discover_skills_returns_empty_list_when_skills_missing():
    """VI-6: discover_skills returns [] when <project_root>/skills/ is missing."""

    # Import the module under test
    from discovery import discover_skills

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a temporary directory that does NOT contain a skills/ subdirectory
        project_root = Path(tmpdir)

        # Verify skills/ does not exist
        skills_dir = project_root / "skills"
        assert (
            not skills_dir.exists()
        ), f"Skills directory should not exist: {skills_dir}"

        # Run the function under test
        result = discover_skills(project_root)

        # Verify the function returns an empty list
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert result == [], f"Expected empty list, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
