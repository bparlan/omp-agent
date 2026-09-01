#!/usr/bin/env python3
# {Verification IDs: VI-8}
# {Requirement IDs: FR-CLI_ERROR_HANDLING}
# Test Type: IMPLEMENTATION_CHECK

"""VI-8: Exceptions during validation are caught; KeyboardInterrupt handled.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys
from io import StringIO

import pytest


def test_generic_exception_caught_returns_empty_list():
    """VI-8: Generic exception during validation returns empty list, prints to stderr."""
    from cli import run_health_check
    from unittest.mock import patch

    with patch("cli.discover_skills", return_value=["skill_alpha"]):
        with patch("cli.validate_single_skill", side_effect=RuntimeError("test error")):
            old_stderr = sys.stderr
            stderr_buf = StringIO()
            sys.stderr = stderr_buf
            try:
                results = run_health_check(skill_name="skill_alpha")
            finally:
                sys.stderr = old_stderr

    assert isinstance(results, list), f"Expected list, got {type(results)}"
    assert len(results) == 0, f"Expected empty list on error, got {results}"
    assert (
        "test error" in stderr_buf.getvalue()
    ), f"stderr missing error message: {stderr_buf.getvalue()}"


def test_keyboard_interrupt_handled():
    """VI-8: KeyboardInterrupt prints message and returns empty list."""
    from cli import run_health_check
    from unittest.mock import patch

    with patch("cli.discover_skills", return_value=["skill_alpha"]):
        with patch("cli.validate_single_skill", side_effect=KeyboardInterrupt):
            old_stderr = sys.stderr
            stderr_buf = StringIO()
            sys.stderr = stderr_buf
            try:
                results = run_health_check(skill_name="skill_alpha")
            finally:
                sys.stderr = old_stderr

    assert isinstance(results, list), f"Expected list, got {type(results)}"
    assert (
        "Operation interrupted by user" in stderr_buf.getvalue()
    ), f"stderr missing interrupt message: {stderr_buf.getvalue()}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
