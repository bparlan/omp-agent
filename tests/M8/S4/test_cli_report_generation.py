#!/usr/bin/env python3
# {Verification IDs: VI-6}
# {Requirement IDs: FR-CLI_REPORT_GENERATION}
# Test Type: IMPLEMENTATION_CHECK

"""VI-6: generate_all_reports() creates report files and prints summary.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import json
import sys
from io import StringIO
from unittest.mock import patch

from pathlib import Path

import pytest
def _capture_stdout(func, *args, **kwargs):
    old = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout = old
    return result, buf.getvalue()
def test_generate_all_reports_creates_files(tmp_path):
    """VI-6: All three report files are created in skills directory."""
    from cli import generate_all_reports

    fake_skills_dir = tmp_path / "skills"
    fake_skills_dir.mkdir()

    results = [
        {
            "name": "skill_alpha",
            "score": 0.95,
            "status": "PASS",
            "fields_checked": ["name", "version", "description", "tools", "userInvocable"],
            "field_results": {"name": True, "version": True, "description": True, "tools": True, "userInvocable": True},
            "errors": [],
            "stable_suffix_detected": False,
        },
        {
            "name": "skill_beta",
            "score": 0.5,
            "status": "FAIL",
            "fields_checked": ["name"],
            "field_results": {"name": True},
            "errors": ["error"],
            "stable_suffix_detected": False,
        },
    ]

    with patch("cli.get_skills_directory", return_value=fake_skills_dir):
        _, stdout = _capture_stdout(generate_all_reports, results)

    badges_file = fake_skills_dir / "health_badges.md"
    health_file = fake_skills_dir / "health_check_report.json"
    processed_file = fake_skills_dir / "processed_skills.json"

    assert badges_file.exists(), "health_badges.md not created"
    assert health_file.exists(), "health_check_report.json not created"
    assert processed_file.exists(), "processed_skills.json not created"

    badge_content = badges_file.read_text()
    assert "# Skill Health Check Badges" in badge_content, "Badge file missing header"

    health_data = json.loads(health_file.read_text())
    assert isinstance(health_data, dict), "health_check_report.json must be dict"
    processed_data = json.loads(processed_file.read_text())
    assert isinstance(processed_data, dict), "processed_skills.json must be dict"
    assert len(processed_data) == len(results), "processed_skills.json key count mismatch"
def test_generate_all_reports_summary_counts():
    """VI-6: Summary block contains correct counts."""
    from cli import generate_all_reports

    results = [
        {
            "name": "skill_alpha",
            "score": 1.0,
            "status": "PASS",
            "fields_checked": ["name", "version", "description", "tools", "userInvocable"],
            "field_results": {"name": True, "version": True, "description": True, "tools": True, "userInvocable": True},
            "errors": [],
            "stable_suffix_detected": False,
        },
        {
            "name": "skill_beta",
            "score": 0.5,
            "status": "FAIL",
            "fields_checked": ["name", "version"],
            "field_results": {"name": True, "version": False},
            "errors": ["version check failed"],
            "stable_suffix_detected": False,
        },
    ]

    with patch("cli.get_skills_directory", return_value=Path("skills")):
        _, stdout = _capture_stdout(generate_all_reports, results)

    assert "Report Summary:" in stdout, "Summary block missing"
    assert "Total skills: 2" in stdout, "Total count mismatch"
    assert "Healthy: 1 (50.0%)" in stdout, "Healthy count mismatch"
    assert "Needs review: 1 (50.0%)" in stdout, "Needs review count mismatch"
    assert "Errors: 1 (50.0%)" in stdout, "Errors count mismatch"
if __name__ == "__main__":
    pytest.main([__file__, "-v"])