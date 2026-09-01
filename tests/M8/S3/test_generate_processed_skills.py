#!/usr/bin/env python3
# {Verification IDs: VI-4}
# {Requirement IDs: FR-REPORTING_PROCESSED_SKILLS_JSON}
# Test Type: IMPLEMENTATION_CHECK

"""VI-4: generate_processed_skills creates processed_skills.json mapping names to results."""

import copy
import json
import tempfile
from pathlib import Path

import pytest
from reporting import generate_processed_skills

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


def test_generate_processed_skills_creates_file():
    """VI-4: generate_processed_skills creates processed_skills.json with identity-preserving mapping."""
    results = copy.deepcopy(SYNTHETIC_RESULTS)

    # Create temporary skills directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch

        with patch("reporting.get_skills_directory") as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_processed_skills with results
            generate_processed_skills(results)

            # Verify the file was created
            output_path = mock_skills_dir / "processed_skills.json"
            assert (
                output_path.exists()
            ), f"processed_skills.json not created at {output_path}"

            # Read and parse JSON
            content = output_path.read_text(encoding="utf-8")
            processed_data = json.loads(content)

            # Verify it's a dictionary
            assert isinstance(
                processed_data, dict
            ), "processed_skills.json should be a dictionary"

            # Verify number of keys matches results length
            assert len(processed_data) == len(
                results
            ), "Key count mismatch with results length"

            # Verify all skill names are present as keys
            for skill in results:
                assert (
                    skill["name"] in processed_data
                ), f"Skill {skill['name']} not found in keys"

            # Verify identity-preserving mapping (deep equality)
            for skill in results:
                assert (
                    processed_data[skill["name"]] == skill
                ), f"Value mismatch for skill {skill['name']}"

            # Verify no extra keys were added
            for key in processed_data:
                assert key in [
                    skill["name"] for skill in results
                ], f"Unexpected key {key} in processed data"


def test_generate_processed_skills_empty_results():
    """VI-4 edge case: empty results produces empty JSON object {}."""
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch

        with patch("reporting.get_skills_directory") as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_processed_skills with empty results
            generate_processed_skills([])

            # Verify the file was created
            output_path = mock_skills_dir / "processed_skills.json"
            assert (
                output_path.exists()
            ), "processed_skills.json not created for empty results"

            # Read and parse JSON
            content = output_path.read_text(encoding="utf-8")
            processed_data = json.loads(content)

            # Verify it's an empty dictionary
            assert (
                processed_data == {}
            ), "processed_skills.json should be empty dict for empty results"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
