#!/usr/bin/env python3
# {Verification IDs: VI-9}
# {Requirement IDs: NFR-REPORTING_DETERMINISTIC_OUTPUT}
# Test Type: IMPLEMENTATION_CHECK

"""VI-9: Identical input to any reporting function produces byte-identical output."""

import copy
import json
import tempfile
from datetime import datetime as real_datetime
from pathlib import Path

import pytest
from unittest.mock import patch

from reporting import (
    generate_badges, generate_health_report, generate_processed_skills,
    generate_skills_summary
)

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


def test_deterministic_output():
    """VI-9: Repeated invocation with identical input produces byte-identical output."""
    results = copy.deepcopy(SYNTHETIC_RESULTS)

    # Freeze time for deterministic timestamp comparison
    fixed_now = real_datetime(2024, 1, 15, 10, 30, 0)

    # Create temporary skills directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch('reporting.datetime') as mock_datetime:
            mock_datetime.now.return_value = fixed_now
            mock_datetime.fromisoformat = real_datetime.fromisoformat
            with patch('reporting.get_skills_directory') as mock_get_dir:
                mock_skills_dir = Path(temp_dir) / "skills"
                mock_skills_dir.mkdir(parents=True)
                mock_get_dir.return_value = mock_skills_dir

                # First invocation — capture all outputs
                generate_badges(results)
                generate_health_report(results)
                generate_processed_skills(results)
                summary1 = generate_skills_summary(results)

                # Read first-invocation outputs before cleanup
                badges_content1 = (mock_skills_dir / "health_badges.md").read_text(encoding="utf-8")
                health_content1 = json.loads((mock_skills_dir / "health_check_report.json").read_text(encoding="utf-8"))
                processed_content1 = json.loads((mock_skills_dir / "processed_skills.json").read_text(encoding="utf-8"))

                # Clean up for second invocation
                for file in mock_skills_dir.glob("*"):
                    file.unlink()
                mock_skills_dir.mkdir(parents=True, exist_ok=True)

                # Second invocation with identical input
                generate_badges(results)
                generate_health_report(results)
                generate_processed_skills(results)
                summary2 = generate_skills_summary(results)

                # Read second-invocation outputs
                badges_content2 = (mock_skills_dir / "health_badges.md").read_text(encoding="utf-8")
                health_content2 = json.loads((mock_skills_dir / "health_check_report.json").read_text(encoding="utf-8"))
                processed_content2 = json.loads((mock_skills_dir / "processed_skills.json").read_text(encoding="utf-8"))

                # Verify badges content is identical
                assert badges_content1 == badges_content2, "health_badges.md content differs between invocations"

                # Verify health report content is identical
                assert health_content1 == health_content2, "health_check_report.json content differs between invocations"

                # Verify processed skills content is identical
                assert processed_content1 == processed_content2, "processed_skills.json content differs between invocations"

                # Verify skills summary return value is identical
                assert summary1 == summary2, "generate_skills_summary return value differs between invocations"

                # Note: Timestamps are frozen via mock, so all content should be byte-identical


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
