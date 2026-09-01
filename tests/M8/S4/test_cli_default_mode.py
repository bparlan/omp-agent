#!/usr/bin/env python3
# {Verification IDs: VI-5}
# {Requirement IDs: FR-CLI_DEFAULT_MODE}
# Test Type: IMPLEMENTATION_CHECK

"""VI-5: run_health_check() dispatches correctly to single, batch, and default modes.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

FIXTURE_DIR = Path("tests/fixtures/cli/synthetic_skills")


def _load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name / "SKILL.md").read_text(encoding="utf-8")


def _capture_stdout(func, *args, **kwargs):
    old = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout = old
    return result, buf.getvalue()


def test_run_health_check_single_skill_mode():
    """VI-5: skill_name='valid_skill' delegates to single-skill mode."""
    from cli import run_health_check

    skill_name = "skill_alpha"
    content = _load_fixture(skill_name)

    def _open_impl(path, *args, **kwargs):
        path_str = str(path)
        if skill_name in path_str or "SKILL.md" in path_str:
            return StringIO(content)
        return StringIO("")

    with patch("cli.discover_skills", return_value=["skill_alpha"]):
        with patch("builtins.open", side_effect=_open_impl):
            results, _ = _capture_stdout(run_health_check, skill_name=skill_name)

    assert isinstance(results, list), f"Expected list, got {type(results)}"
    # Single skill mode: returns result from validate_single_skill (1 item)
    assert len(results) == 1, f"Expected 1 result for single skill, got {len(results)}"


def test_run_health_check_batch_mode():
    """VI-5: all_flag=True delegates to batch mode."""
    from cli import process_all_skills, run_health_check

    skill_names = [
        "skill_alpha",
        "skill_beta",
        "skill_gamma",
        "skill_delta",
        "skill_epsilon",
        "skill_zeta",
    ]

    contents = {}
    for name in skill_names:
        contents[name] = _load_fixture(name)

    def _open_impl(path, *args, **kwargs):
        path_str = str(path)
        for name in skill_names:
            if name in path_str or str(FIXTURE_DIR / name / "SKILL.md") == path_str:
                return StringIO(contents[name])
        return StringIO("")

    # Measure batch mode result length
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=_open_impl):
            batch_results, _ = _capture_stdout(process_all_skills)

    # Measure run_health_check with all_flag=True
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=_open_impl):
            run_results, _ = _capture_stdout(
                run_health_check, skill_name=None, all_flag=True
            )

    assert len(run_results) == len(batch_results), (
        f"Batch mode and run_health_check(all_flag=True) length mismatch: "
        f"{len(run_results)} vs {len(batch_results)}"
    )


def test_run_health_check_default_mode():
    """VI-5: No args → default mode, list length equals discovery count, no batch headers."""
    from cli import run_health_check

    skill_names = [
        "skill_alpha",
        "skill_beta",
        "skill_gamma",
        "skill_delta",
        "skill_epsilon",
        "skill_zeta",
    ]

    contents = {}
    for name in skill_names:
        contents[name] = _load_fixture(name)

    def _open_impl(path, *args, **kwargs):
        path_str = str(path)
        for name in skill_names:
            if name in path_str or str(FIXTURE_DIR / name / "SKILL.md") == path_str:
                return StringIO(contents[name])
        return StringIO("")

    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=_open_impl):
            results, stdout = _capture_stdout(run_health_check)

    assert len(results) == len(
        skill_names
    ), f"Default mode: expected {len(skill_names)} results, got {len(results)}"
    assert "BATCH" not in stdout, "Default mode should not contain batch headers"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
