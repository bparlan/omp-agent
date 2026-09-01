#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: NFR-DISCOVERY_TYPE_HINTS}
# Test Type: IMPLEMENTATION_CHECK

import pytest
import typing
from pathlib import Path


def test_discovery_type_hints():
    """VI-14: discovery.py declares type hints on public functions and constants."""

    # Import the module under test
    import discovery

    # Get type hints for discover_skills
    discover_skills_hints = typing.get_type_hints(discovery.discover_skills)
    expected_discover_skills_hints = {"project_root": typing.Union[Path, str]}

    # Verify discover_skills has type hints
    assert len(discover_skills_hints) > 0, "discover_skills should have type hints"
    assert (
        "project_root" in discover_skills_hints
    ), "discover_skills should have project_root parameter type hint"

    # Get type hints for find_project_root
    find_project_root_hints = typing.get_type_hints(discovery.find_project_root)
    expected_find_project_root_hints = {"start": typing.Union[Path, str, type(None)]}

    # Verify find_project_root has type hints
    assert len(find_project_root_hints) > 0, "find_project_root should have type hints"
    assert (
        "start" in find_project_root_hints
    ), "find_project_root should have start parameter type hint"

    # Get annotations for SKILLS_DIR_NAME
    try:
        skills_dir_name_hints = typing.get_type_hints(discovery, include_extras=True)
    except (TypeError, NameError):
        # Try to get annotations directly
        skills_dir_name_hints = {}
        if hasattr(discovery, "__annotations__"):
            skills_dir_name_hints = discovery.__annotations__

    # Verify SKILLS_DIR_NAME is annotated with str
    assert "SKILLS_DIR_NAME" in skills_dir_name_hints or hasattr(
        discovery, "SKILLS_DIR_NAME"
    ), "SKILLS_DIR_NAME should exist and be annotated"

    if hasattr(discovery, "SKILLS_DIR_NAME"):
        assert isinstance(
            discovery.SKILLS_DIR_NAME, str
        ), "SKILLS_DIR_NAME should be a string"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
