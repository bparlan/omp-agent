#!/usr/bin/env python3
# {Verification IDs: VI-7}
# {Requirement IDs: FR-CLI_HELP_DISPLAY}
# Test Type: IMPLEMENTATION_CHECK

"""VI-7: print_help() writes required substrings to stdout; --help exits 0.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys
from io import StringIO

import pytest


def test_print_help_contains_required_substrings():
    """VI-7: print_help() stdout contains all required substrings."""
    from cli import print_help

    old_stdout = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    try:
        print_help()
    finally:
        sys.stdout = old_stdout
    help_text = buf.getvalue()

    required_substrings = [
        "healthcheck.py [skill_name]",
        "healthcheck.py --all",
        "healthcheck.py --help",
        "Required fields: name, version, description, tools, userInvocable",
        "-stable suffix",
        "health_badges.md",
        "health_check_report.json",
        "processed_skills.json",
    ]

    for substring in required_substrings:
        assert substring in help_text, (
            f"Help text missing required substring: '{substring}'"
        )


def test_help_flag_exits_zero():
    """VI-7: --help invocation raises SystemExit(0)."""
    import cli

    old_argv = sys.argv
    try:
        sys.argv = ["healthcheck.py", "--help"]
        with pytest.raises(SystemExit) as exc_info:
            cli.parse_arguments()
        assert exc_info.value.code == 0
    finally:
        sys.argv = old_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
