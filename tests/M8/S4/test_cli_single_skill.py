#!/usr/bin/env python3
# {Verification IDs: VI-3}
# {Requirement IDs: FR-CLI_SINGLE_SKILL_MODE}
# Test Type: IMPLEMENTATION_CHECK

"""VI-3: validate_single_skill() returns result dict for valid skill, None for missing.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

FIXTURE_DIR = Path("tests/fixtures/cli/synthetic_skills")


def _load_fixture_content(skill_name: str) -> str:
    """Load SKILL.md content from fixture directory."""
    skill_file = FIXTURE_DIR / skill_name / "SKILL.md"
    assert skill_file.exists(), f"Fixture missing: {skill_file}"
    return skill_file.read_text(encoding="utf-8")


def _capture_stdout_stderr(func, *args, **kwargs):
    """Run func with args and capture stdout/stderr separately."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_buf = StringIO()
    stderr_buf = StringIO()
    sys.stdout = stdout_buf
    sys.stderr = stderr_buf
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    return result, stdout_buf.getvalue(), stderr_buf.getvalue()


def test_validate_single_skill_nonexistent_returns_none():
    """VI-3: Nonexistent skill returns None and writes to stderr."""
    from cli import validate_single_skill

    with patch("cli.discover_skills", return_value=["skill_alpha", "skill_beta"]):
        result, stdout, stderr = _capture_stdout_stderr(
            validate_single_skill, "nonexistent_skill_xyz"
        )

    assert result is None, f"Expected None for missing skill, got {result}"
    assert "nonexistent_skill_xyz" in stderr, f"stderr missing skill name: {stderr}"
    assert "not found" in stderr.lower(), f"stderr missing 'not found': {stderr}"


def test_validate_single_skill_valid_returns_result_dict():
    """VI-3: Valid skill returns result dict with correct schema."""
    from cli import validate_single_skill

    skill_name = "skill_alpha"
    content = _load_fixture_content(skill_name)

    with patch("cli.discover_skills", return_value=["skill_alpha", "skill_beta"]):
        with patch("builtins.open", side_effect=lambda p, **kw: StringIO(content)):
            result, stdout, stderr = _capture_stdout_stderr(
                validate_single_skill, skill_name
            )

    assert result is not None, "Expected result dict for valid skill"
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"
    assert "score" in result, "Missing 'score' key"
    assert "status" in result, "Missing 'status' key"
    assert "fields_checked" in result, "Missing 'fields_checked' key"
    assert "field_results" in result, "Missing 'field_results' key"
    assert "errors" in result, "Missing 'errors' key"
    assert "stable_suffix_detected" in result, "Missing 'stable_suffix_detected' key"
    assert isinstance(result["score"], (int, float)), "score must be numeric"
    assert 0.0 <= result["score"] <= 1.0, "score out of range"
    assert result["status"] in ("PASS", "FAIL"), f"Invalid status: {result['status']}"
    assert isinstance(result["fields_checked"], list), "fields_checked must be list"
    assert isinstance(result["field_results"], dict), "field_results must be dict"
    assert isinstance(result["errors"], list), "errors must be list"
    assert isinstance(
        result["stable_suffix_detected"], bool
    ), "stable_suffix_detected must be bool"


def test_validate_single_skill_valid_prints_status_line():
    """VI-3: Valid skill prints status line to stdout."""
    from cli import validate_single_skill

    skill_name = "skill_alpha"
    content = _load_fixture_content(skill_name)

    with patch("cli.discover_skills", return_value=["skill_alpha"]):
        with patch("builtins.open", side_effect=lambda p, **kw: StringIO(content)):
            result, stdout, stderr = _capture_stdout_stderr(
                validate_single_skill, skill_name
            )

    assert f"Checking {skill_name}" in stdout, f"stdout missing status line: {stdout}"
    assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
