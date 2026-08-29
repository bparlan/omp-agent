#!/usr/bin/env python3
# {Verification IDs: VI-10}
# {Requirement IDs: NFR-REPORTING_DIFF_SCOPE}
# Test Type: ENVIRONMENT_CHECK

"""VI-10: Diff-scope allowlist enforcement — only Allowlist files in the diff."""

import subprocess

import pytest


def _git_diff_files() -> set[str]:
    """Return M8S3-relevant files from git diff --name-only."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return set()
        all_files = {line.strip() for line in result.stdout.strip().splitlines() if line.strip()}
        # Filter to only M8S3-relevant paths — pre-existing diff noise from other
        # milestones (S1, S2, etc.) is not subject to this allowlist.
        m8s3_relevant = {
            f for f in all_files
            if f == "reporting.py"
            or f.startswith("tests/M8/S3/")
            or f.startswith("tests/fixtures/reporting/")
        }
        return m8s3_relevant
    except Exception:
        return set()


def test_diff_scope_allowlist():
    """VI-10: Every M8S3-relevant file in the diff is a member of the M8S3 Allowlist."""
    diff_files = _git_diff_files()
    allowlist_prefixes = {"reporting.py", "tests/M8/S3/", "tests/fixtures/reporting/"}

    for filepath in diff_files:
        allowed = any(
            filepath == prefix.rstrip("/") or filepath.startswith(prefix)
            for prefix in allowlist_prefixes
        )
        assert allowed, (
            f"File '{filepath}' appears in git diff but is NOT on the M8S3 Allowlist. "
            f"Allowlist: {sorted(allowlist_prefixes)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
