#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-SKILL_FIXTURE_PATH_RESOLUTION}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_SKILLS_DIR_NAME_constant():
    """VI-12: SKILLS_DIR_NAME constant is \"skills\" and is importable."""

    # Import the module under test
    from discovery import SKILLS_DIR_NAME

    # Verify the constant is importable
    assert isinstance(SKILLS_DIR_NAME, str), f"Expected string, got {type(SKILLS_DIR_NAME)}"

    # Verify the constant equals \"skills\"
    assert SKILLS_DIR_NAME == "skills", f"Expected 'skills', got {SKILLS_DIR_NAME}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
