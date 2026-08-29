#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_MODULE_EXPORTS, FR-SKILL_LISTING_FROM_FIXTURE, FR-DETERMINISTIC_SORT_ORDER}
# Test Type: IMPLEMENTATION_CHECK

import pytest
from pathlib import Path


def test_discover_skills_returns_sorted_skill_basenames():
    """VI-1: discover_skills returns a sorted list of skill basenames."""

    # Import the module under test
    from discovery import discover_skills

    # Verify preconditions - fixture directory exists
    fixture_root = Path("tests/fixtures/discovery/synthetic_project")
    assert fixture_root.exists(), f"Fixture directory {fixture_root} does not exist"

    # Verify the skills directory exists
    skills_dir = fixture_root / "skills"
    assert skills_dir.exists(), f"Skills directory {skills_dir} does not exist"

    # Count subdirectories that contain SKILL.md files
    expected_skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_md_file = skill_dir / "SKILL.md"
            if skill_md_file.exists():
                expected_skills.append(skill_dir.name)

    # Sort expected skills for deterministic comparison
    expected_skills.sort()

    # Ensure we have at least 2 skills for the test to be meaningful
    assert len(expected_skills) >= 2, f"Need at least 2 skills with SKILL.md, found {len(expected_skills)}"

    # Run the function under test
    result = discover_skills(fixture_root)

    # Verify result is a list of strings
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert all(isinstance(item, str) for item in result), f"Expected all strings, got {[type(item) for item in result]}"

    # Verify result length matches expectation
    assert len(result) == len(expected_skills), f"Expected {len(expected_skills)} skills, got {len(result)}"

    # Verify all expected skills are present
    assert set(result) == set(expected_skills), f"Skill sets differ: expected {expected_skills}, got {result}"

    # Verify result is lexicographically sorted (deterministic order)
    assert result == sorted(result), f"Result {result} is not sorted; sorted would be {sorted(result)}"

    # Verify each result entry matches expected skill basename
    assert result == expected_skills, f"Result {result} does not match expected skills {expected_skills}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
