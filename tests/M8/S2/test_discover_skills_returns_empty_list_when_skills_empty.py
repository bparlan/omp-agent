#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-SKILL_LISTING_FROM_FIXTURE, FR-DISCOVERY_ERROR_TOLERANCE}
# Test Type: IMPLEMENTATION_CHECK

import pytest
import tempfile
from pathlib import Path


def test_discover_skills_returns_empty_list_when_skills_empty():
    """VI-7: discover_skills returns [] when skills/ is empty."""

    # Import the module under test
    from discovery import discover_skills

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a temporary directory with an empty skills/ subdirectory
        project_root = Path(tmpdir)
        skills_dir = project_root / "skills"
        skills_dir.mkdir()

        # Verify skills/ directory exists but is empty
        skill_subdirs = list(skills_dir.iterdir())
        assert (
            len(skill_subdirs) == 0
        ), f"Skills directory should be empty: {skill_subdirs}"

        # Run the function under test
        result = discover_skills(project_root)

        # Verify the function returns an empty list
        assert isinstance(result, list), f"Expected list, got {type(result)}"
        assert result == [], f"Expected empty list, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
