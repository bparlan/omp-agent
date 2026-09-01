#!/usr/bin/env python3
# V-007
# FR-MAIN_BACKWARD_COMPAT
# Test Type: INTEGRATION_CHECK

"""Integration test for wrapper scripts delegating to root modules (V-007).

Pre-implementation: main.py does not exist.
Expected VALID_INITIAL_FAILURE: test error with exit code 1.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def _run_command(cmd, cwd=None):
    """Run a command and return the result."""
    if cwd is None:
        cwd = PROJECT_ROOT
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        shell=isinstance(cmd, str),
    )
    return result


def test_wrapper_healthcheck_py_delegates_to_root():
    """V-007: skills/healthcheck/healthcheck.py must delegate to root cli.py."""
    wrapper_path = PROJECT_ROOT / "skills" / "healthcheck" / "healthcheck.py"
    assert wrapper_path.is_file(), f"Wrapper not found at {wrapper_path}"

    source = wrapper_path.read_text(encoding="utf-8")

    # Verify wrapper imports from root-level modules
    assert (
        "from cli import" in source or "import cli" in source
    ), "Wrapper must import from root-level cli module"

    # Verify wrapper does NOT import from wrapper-local modules
    assert (
        "from skills.healthcheck.cli import" not in source
    ), "Wrapper must not import from wrapper-local cli module"

    # Execute wrapper and verify it works
    result = _run_command([sys.executable, str(wrapper_path), "--help"])
    assert result.returncode == 0, (
        f"Wrapper execution failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_wrapper_index_js_delegates_to_python():
    """V-007: skills/healthcheck/index.js must delegate to healthcheck.py."""
    wrapper_path = PROJECT_ROOT / "skills" / "healthcheck" / "index.js"
    assert wrapper_path.is_file(), f"Wrapper not found at {wrapper_path}"

    source = wrapper_path.read_text(encoding="utf-8")

    # Verify wrapper references the Python script
    assert (
        "healthcheck.py" in source
    ), "Node wrapper must reference healthcheck.py script"

    # Verify wrapper does NOT duplicate CLI logic
    assert "argparse" not in source, "Node wrapper must not duplicate CLI parsing logic"


def test_wrapper_integration_consistency():
    """V-007: Wrapper output must align with root module behavior."""
    wrapper_path = PROJECT_ROOT / "skills" / "healthcheck" / "healthcheck.py"
    main_path = PROJECT_ROOT / "main.py"

    # Execute wrapper
    wrapper_result = _run_command([sys.executable, str(wrapper_path), "--help"])

    # Execute root main.py
    main_result = _run_command([sys.executable, str(main_path), "--help"])

    # Both should succeed
    assert (
        wrapper_result.returncode == 0
    ), f"Wrapper failed with exit code {wrapper_result.returncode}"
    assert (
        main_result.returncode == 0
    ), f"Root main.py failed with exit code {main_result.returncode}"

    # Both should produce similar help output
    assert (
        "healthcheck" in wrapper_result.stdout.lower()
    ), "Wrapper help output must mention 'healthcheck'"
    assert (
        "healthcheck" in main_result.stdout.lower()
    ), "Root main.py help output must mention 'healthcheck'"


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
