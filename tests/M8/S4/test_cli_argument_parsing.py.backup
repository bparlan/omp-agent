#!/usr/bin/env python3
# {Verification IDs: VI-2}
# {Requirement IDs: FR-CLI_ARGUMENT_PARSING}
# Test Type: IMPLEMENTATION_CHECK

"""VI-2: parse_arguments() produces correct namespace for all invocation patterns.

Pre-implementation: ModuleNotFoundError is the expected VALID_INITIAL_FAILURE.
"""

import sys

import pytest


def _invoke_parse(argv):
    """Invoke parse_arguments with overridden sys.argv and return vars()."""
    old_argv = sys.argv
    try:
        sys.argv = argv
        from cli import parse_arguments
        return vars(parse_arguments())
    finally:
        sys.argv = old_argv


def test_parse_arguments_no_args():
    """VI-2: No args → skill_name=None, all_flag=False, help_flag=False."""
    result = _invoke_parse(["healthcheck.py"])
    assert result["skill_name"] is None
    assert result["all_flag"] is False
    assert result["help_flag"] is False


def test_parse_arguments_skill_name():
    """VI-2: 'my_skill' positional → skill_name='my_skill'."""
    result = _invoke_parse(["healthcheck.py", "my_skill"])
    assert result["skill_name"] == "my_skill"
    assert result["all_flag"] is False
    assert result["help_flag"] is False


def test_parse_arguments_all_flag():
    """VI-2: '--all' → all_flag=True, skill_name=None."""
    result = _invoke_parse(["healthcheck.py", "--all"])
    assert result["skill_name"] is None
    assert result["all_flag"] is True
    assert result["help_flag"] is False


def test_parse_arguments_help_flag():
    """VI-2: '--help' triggers SystemExit(0)."""
    with pytest.raises(SystemExit) as exc_info:
        _invoke_parse(["healthcheck.py", "--help"])
    assert exc_info.value.code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
