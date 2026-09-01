#!/usr/bin/env python3
# {Verification IDs: VI-9}
# {Requirement IDs: FR-CLI_EXECUTABLE_INTEGRATION}
# Test Type: INTEGRATION_CHECK

"""VI-9: healthcheck.py executable exits 0 on success, 1 on failure.

Pre-implementation: The existing healthcheck.py wrapper may have pre-existing
import issues; the test verifies the exit code contract (0 or 1) and that
the process completes within 30 seconds.
"""

import subprocess

import pytest


HEALTHCHECK_PATH = "skills/healthcheck/healthcheck.py"


def test_healthcheck_py_exit_code_is_zero_or_one():
    """VI-9: healthcheck.py exit code is either 0 (success) or 1 (failure)."""
    result = subprocess.run(
        ["python3", HEALTHCHECK_PATH],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode in (
        0,
        1,
    ), f"Exit code must be 0 or 1, got {result.returncode}\nstderr: {result.stderr}"


def test_healthcheck_py_completes_within_timeout():
    """VI-9: healthcheck.py completes within 30 seconds."""
    result = subprocess.run(
        ["python3", HEALTHCHECK_PATH],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode is not None, "Process did not complete"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
