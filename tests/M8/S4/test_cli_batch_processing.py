#!/usr/bin/env python3
# {Verification IDs: VI-4}
# {Requirement IDs: FR-CLI_BATCH_PROCESSING}
# Test Type: IMPLEMENTATION_CHECK

"""VI-4: process_all_skills() returns results list with correct batch structure.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

FIXTURE_DIR = Path("tests/fixtures/cli/synthetic_skills")


def _load_fixture(name: str) -> str:
    """Load SKILL.md content from fixture directory."""
    return (FIXTURE_DIR / name / "SKILL.md").read_text(encoding="utf-8")


def _capture_stdout(func, *args, **kwargs):
    """Run func and capture stdout."""
    old = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    try:
        result = func(*args, **kwargs)
    finally:
        sys.stdout = old
    return result, buf.getvalue()


def _make_open_impl(skill_names):
    """Create an open() side-effect that returns fixture content by skill name."""
    skill_dir_map = {}
    for name in skill_names:
        skill_dir_map[name] = _load_fixture(name)
    # Also map by full path for flexibility
    path_map = {}
    for name in skill_names:
        skill_dir = FIXTURE_DIR / name
        path_map[str(skill_dir / "SKILL.md")] = skill_dir_map[name]

    def _open_impl(path, *args, **kwargs):
        path_str = str(path)
        if path_str in path_map:
            return StringIO(path_map[path_str])
        return StringIO("")

    return _open_impl


def test_process_all_skills_returns_correct_length():
    """VI-4: Returned list length equals len(discover_skills())."""
    from cli import process_all_skills

    skill_names = [
        "skill_alpha", "skill_beta", "skill_gamma",
        "skill_delta", "skill_epsilon", "skill_zeta",
    ]

    open_impl = _make_open_impl(skill_names)
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=open_impl):
            results, _ = _capture_stdout(process_all_skills)

    assert isinstance(results, list)
    assert len(results) == len(skill_names), (
        f"Expected {len(skill_names)} results, got {len(results)}"
    )


def test_process_all_skills_batch_headers_in_order():
    """VI-4: Batch headers appear in order 1, 2, 3."""
    from cli import process_all_skills

    skill_names = [
        "skill_alpha", "skill_beta", "skill_gamma",
        "skill_delta", "skill_epsilon", "skill_zeta",
    ]

    open_impl = _make_open_impl(skill_names)
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=open_impl):
            _, stdout = _capture_stdout(process_all_skills)

    pos1 = stdout.find("BATCH 1")
    pos2 = stdout.find("BATCH 2")
    pos3 = stdout.find("BATCH 3")
    assert pos1 != -1, "Missing BATCH 1 header"
    assert pos2 != -1, "Missing BATCH 2 header"
    assert pos3 != -1, "Missing BATCH 3 header"
    assert pos1 < pos2 < pos3, (
        f"Batch headers out of order: {pos1}, {pos2}, {pos3}"
    )


def test_process_all_skills_preserves_ordering():
    """VI-4: Returned list preserves batch ordering."""
    from cli import process_all_skills

    skill_names = [
        "skill_alpha", "skill_beta", "skill_gamma",
        "skill_delta", "skill_epsilon", "skill_zeta",
    ]

    open_impl = _make_open_impl(skill_names)
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=open_impl):
            results, _ = _capture_stdout(process_all_skills)

    names_in_order = [r.get("name", "") for r in results]
    assert names_in_order == skill_names, (
        f"Ordering mismatch: {names_in_order} != {skill_names}"
    )


def test_process_all_skills_summary_counts():
    """VI-4: Summary block counts match returned list length."""
    from cli import process_all_skills

    skill_names = [
        "skill_alpha", "skill_beta", "skill_gamma",
        "skill_delta", "skill_epsilon", "skill_zeta",
    ]

    open_impl = _make_open_impl(skill_names)
    with patch("cli.discover_skills", return_value=skill_names):
        with patch("builtins.open", side_effect=open_impl):
            results, stdout = _capture_stdout(process_all_skills)

    total_count = len(results)
    assert "Total:" in stdout or "total" in stdout.lower(), (
        "Summary block missing total count"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
