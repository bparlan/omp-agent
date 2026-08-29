#!/usr/bin/env python3
# {Verification IDs: VI-5}
# {Requirement IDs: FR-REPORTING_SKILL_SUMMARY_FUNCTION}
# Test Type: IMPLEMENTATION_CHECK

"""VI-5: generate_skills_summary returns correct summary dictionary."""

import copy
import json
import tempfile
from pathlib import Path
from datetime import datetime

import pytest
from reporting import generate_skills_summary

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


def test_generate_skills_summary_returns_dict():
    """VI-5: generate_skills_summary returns dict with required top-level keys."""
    results = copy.deepcopy(SYNTHETIC_RESULTS)

    # Call generate_skills_summary with results
    summary = generate_skills_summary(results)

    # Verify it's a dictionary
    assert isinstance(summary, dict), "generate_skills_summary should return a dict"

    # Verify required top-level keys
    required_keys = ["summary", "skills", "status_distribution"]
    for key in required_keys:
        assert key in summary, f"Missing required top-level key: {key}"

    # Verify summary section
    summary_section = summary["summary"]
    required_summary_keys = [
        "total_skills", "healthy_count", "needs_review_count", "error_count",
        "skipped_count", "stable_ready_count", "generation_timestamp"
    ]
    for key in required_summary_keys:
        assert key in summary_section, f"Missing required summary key: {key}"

    # Verify counts are correct
    assert summary_section["total_skills"] == len(results), "total_skills count mismatch"
    assert summary_section["healthy_count"] == 1, "healthy_count should be 1"
    assert summary_section["needs_review_count"] == 1, "needs_review_count should be 1"
    assert summary_section["error_count"] == 1, "error_count should be 1"
    assert summary_section["skipped_count"] == 1, "skipped_count should be 1"
    assert summary_section["stable_ready_count"] == 2, "stable_ready_count should be 2 (alpha and gamma)"

    # Verify timestamp is valid ISO 8601 format
    try:
        datetime.fromisoformat(summary_section["generation_timestamp"].replace("Z", "+00:00"))
    except ValueError:
        pytest.fail(f"Invalid timestamp format: {summary_section['generation_timestamp']}")

    # Verify skills array matches input (order preserved)
    assert summary["skills"] == results, "skills array should match input results"

    # Verify status_distribution structure and content
    status_dist = summary["status_distribution"]
    assert isinstance(status_dist, dict), "status_distribution should be a dict"

    # Verify each status category has correct skills
    expected_distribution = {
        "healthy": ["zebra-skill"],
        "needs_review": ["alpha-skill"],
        "error": ["beta-skill"],
        "skipped": ["gamma-skill"]
    }

    for status, expected_skills in expected_distribution.items():
        assert status in status_dist, f"Missing status in distribution: {status}"
        assert set(status_dist[status]) == set(expected_skills), f"Incorrect skills for status {status}"


def test_generate_skills_summary_empty_results():
    """VI-5 edge case: empty results produces zero counts and empty distributions."""
    # Call generate_skills_summary with empty results
    summary = generate_skills_summary([])

    # Verify structure
    assert isinstance(summary, dict), "Should return dict"
    assert "summary" in summary, "Missing summary key"
    assert "skills" in summary, "Missing skills key"
    assert "status_distribution" in summary, "Missing status_distribution key"

    # Verify empty results handling
    assert summary["summary"]["total_skills"] == 0, "total_skills should be 0"
    assert summary["summary"]["healthy_count"] == 0, "healthy_count should be 0"
    assert summary["summary"]["needs_review_count"] == 0, "needs_review_count should be 0"
    assert summary["summary"]["error_count"] == 0, "error_count should be 0"
    assert summary["summary"]["skipped_count"] == 0, "skipped_count should be 0"
    assert summary["summary"]["stable_ready_count"] == 0, "stable_ready_count should be 0"

    assert summary["skills"] == [], "skills should be empty list"
    assert summary["status_distribution"] == {}, "status_distribution should be empty dict"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])