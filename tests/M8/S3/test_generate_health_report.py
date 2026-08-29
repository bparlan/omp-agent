#!/usr/bin/env python3
# {Verification IDs: VI-3}
# {Requirement IDs: FR-REPORTING_HEALTH_REPORT_JSON}
# Test Type: IMPLEMENTATION_CHECK

"""VI-3: generate_health_report creates health_check_report.json with correct schema."""

import copy
import json
import tempfile
from pathlib import Path
from datetime import datetime

import pytest
from reporting import generate_health_report

# Synthetic fixture results — same as VI-2 for consistency
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


def test_generate_health_report_creates_file():
    """VI-3: generate_health_report creates health_check_report.json with correct schema."""
    results = copy.deepcopy(SYNTHETIC_RESULTS)

    # Create temporary skills directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch
        with patch('reporting.get_skills_directory') as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_health_report with results
            generate_health_report(results)

            # Verify the file was created
            output_path = mock_skills_dir / "health_check_report.json"
            assert output_path.exists(), f"health_check_report.json not created at {output_path}"

            # Read and parse JSON
            content = output_path.read_text(encoding="utf-8")
            report_data = json.loads(content)

            # Verify required keys
            required_keys = [
                "timestamp", "total_skills", "healthy_count", "needs_review_count",
                "error_count", "skipped_count", "skills"
            ]
            for key in required_keys:
                assert key in report_data, f"Missing required key: {key}"

            # Verify timestamp is ISO 8601 format
            try:
                datetime.fromisoformat(report_data["timestamp"].replace("Z", "+00:00"))
            except ValueError:
                pytest.fail(f"Invalid timestamp format: {report_data['timestamp']}")

            # Verify counts are correct
            assert report_data["total_skills"] == len(results), "Incorrect total_skills count"
            assert report_data["healthy_count"] == 1, "Incorrect healthy_count"
            assert report_data["needs_review_count"] == 1, "Incorrect needs_review_count"
            assert report_data["error_count"] == 1, "Incorrect error_count"
            assert report_data["skipped_count"] == 1, "Incorrect skipped_count"

            # Verify skills array preserves order and content
            assert len(report_data["skills"]) == len(results), "Skills array length mismatch"
            for i, (expected, actual) in enumerate(zip(results, report_data["skills"])):
                assert expected["name"] == actual["name"], f"Skill name mismatch at index {i}"


def test_generate_health_report_empty_results():
    """VI-3 edge case: empty results produces all-zero counts."""
    with tempfile.TemporaryDirectory() as temp_dir:
        from unittest.mock import patch
        with patch('reporting.get_skills_directory') as mock_get_dir:
            mock_skills_dir = Path(temp_dir) / "skills"
            mock_skills_dir.mkdir(parents=True)
            mock_get_dir.return_value = mock_skills_dir

            # Call generate_health_report with empty results
            generate_health_report([])

            # Verify the file was created
            output_path = mock_skills_dir / "health_check_report.json"
            assert output_path.exists(), "health_check_report.json not created for empty results"

            # Read and parse JSON
            content = output_path.read_text(encoding="utf-8")
            report_data = json.loads(content)

            # Verify all counts are zero
            assert report_data["total_skills"] == 0, "total_skills should be 0"
            assert report_data["healthy_count"] == 0, "healthy_count should be 0"
            assert report_data["needs_review_count"] == 0, "needs_review_count should be 0"
            assert report_data["error_count"] == 0, "error_count should be 0"
            assert report_data["skipped_count"] == 0, "skipped_count should be 0"

            # Verify skills array is empty
            assert report_data["skills"] == [], "skills array should be empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])