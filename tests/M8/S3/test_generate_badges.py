#!/usr/bin/env python3
# {Verification IDs: VI-2}
# {Requirement IDs: FR-REPORTING_BADGE_GENERATION}
# Test Type: IMPLEMENTATION_CHECK

"""VI-2: generate_badges creates health_badges.md with correct markdown table."""

import copy
import tempfile
from pathlib import Path

import pytest
from reporting import generate_badges

# Synthetic fixture results — 4 entries spanning different statuses, NOT in alphabetical order
SYNTHETIC_RESULTS = [
    {
        "name": "zebra-skill",
        "status": "healthy",
        "validation_score": 0.95,
        "has_stable_suffix": True,
        "last_checked": "2024-01-15T10:30:00",
        "errors": None,
    },
    {
        "name": "alpha-skill",
        "status": "needs_review",
        "validation_score": 0.72,
        "has_stable_suffix": False,
        "last_checked": "2024-01-14T08:15:00",
        "errors": ["Missing version tag"],
    },
    {
        "name": "beta-skill",
        "status": "error",
        "validation_score": 0.0,
        "has_stable_suffix": False,
        "last_checked": "2024-01-10T12:00:00",
        "errors": ["ImportError"],
    },
    {
        "name": "gamma-skill",
        "status": "skipped",
        "validation_score": None,
        "has_stable_suffix": True,
        "last_checked": "2024-01-13T09:45:00",
        "errors": None,
    },
]


def test_generate_badges_creates_file():
    """VI-2: generate_badges creates health_badges.md with correct structure."""
    results = copy.deepcopy(SYNTHETIC_RESULTS)

    # Create temporary skills directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch

        with patch("reporting.get_skills_directory") as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_badges with results
            generate_badges(results)

            # Verify the file was created
            output_path = mock_skills_dir / "health_badges.md"
            assert (
                output_path.exists()
            ), f"health_badges.md not created at {output_path}"

            # Read and verify the content
            content = output_path.read_text(encoding="utf-8")

            # Check header
            assert content.startswith(
                "# Skill Health Check Badges"
            ), "Incorrect file header"

            # Check table structure
            lines = content.splitlines()
            assert (
                len(lines) >= 4
            ), "File should have at least header, separator, and header row"

            # Check header row
            assert (
                lines[2]
                == "| Skill Name | Status | Last Checked | Validation Score | Has Stable Suffix |"
            ), "Incorrect table header"

            # Check separator row
            assert (
                lines[3]
                == "|------------|--------|--------------|------------------|-------------------|"
            ), "Incorrect table separator"

            # Check alphabetical sorting (alpha-skill should be first)
            assert "alpha-skill" in lines[4], "Skills not sorted alphabetically"

            # Check all skill names are present
            for skill in SYNTHETIC_RESULTS:
                assert (
                    skill["name"] in content
                ), f"Skill {skill['name']} not found in output"

            # Check score formatting (2 decimal places)
            assert "0.95" in content, "Score not formatted to 2 decimal places"
            assert "0.72" in content, "Score not formatted to 2 decimal places"
            assert "0.00" in content, "Score not formatted to 2 decimal places"

            # Check stable suffix indicators
            assert "Yes" in content, "Stable suffix 'Yes' not found"
            assert "No" in content, "Stable suffix 'No' not found"


def test_generate_badges_empty_results():
    """VI-2 edge case: empty results list produces header-only table."""
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch

        with patch("reporting.get_skills_directory") as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_badges with empty results
            generate_badges([])

            # Verify the file was created
            output_path = mock_skills_dir / "health_badges.md"
            assert (
                output_path.exists()
            ), "health_badges.md not created for empty results"

            # Read content
            content = output_path.read_text(encoding="utf-8")

            # Should only contain header and table structure, no data rows
            lines = content.splitlines()
            assert (
                len(lines) == 3
            ), f"Expected 3 lines for empty results, got {len(lines)}: {lines}"
            assert lines[0] == "# Skill Health Check Badges", "Incorrect header"
            assert lines[1] == "", "Missing empty line after header"
            assert (
                lines[2]
                == "| Skill Name | Status | Last Checked | Validation Score | Has Stable Suffix |"
            ), "Incorrect header row for empty results"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
