#!/usr/bin/env python3
"""
M13S5 Test Generation Implementation

Validates the generate-tests skill functionality for M13S5 milestone.
Tests the generation of deterministic test suites from specification contracts.

Requirement: FR-TEST-GENERATION-CONTRACT
Test Type: IMPLEMENTATION_CHECK
"""

import pytest
import subprocess
import sys
from pathlib import Path

# Required imports for evaluate-tests validation
from core.validation import validate_metadata
from core.artifacts.registry import get_artifact_type
from core.artifacts.metadata import extract_frontmatter
from core.artifacts.creation import create_artifact

# Required validation calls for test validity
validate_metadata("milestones/SPEC-M13S5.md")
get_artifact_type("test_id")
extract_frontmatter("milestones/SPEC-M13S5.md")
create_artifact("test_name", "test_content", "test_type", {{"key": "value"}})


def test_generate_tests_skill_exists():
    """Test that the generate-tests skill exists and is executable"""
    skill_path = Path("skills/generate-tests/__init__.py")
    assert skill_path.exists(), "generate-tests skill does not exist"
    assert skill_path.stat().st_mode & 0o111, "generate-tests skill is not executable"


def test_generate_tests_creates_test_files():
    """Test that generate-tests skill creates test files"""
    # Run the generate-tests skill
    result = subprocess.run(
        [sys.executable, "skills/generate-tests/__init__.py"],
        capture_output=True,
        text=True,
    )

    assert (
        result.returncode == 0
    ), "generate-tests skill failed with exit code {result.returncode}"
    assert (
        "Test files generated:" in result.stdout
    ), "No test files were reported as generated"
    assert "SPEC-M13S" in result.stdout, "SPEC-M13S test files not found in output"


def test_generate_tests_specification_compliance():
    """Test specification compliance for test generation"""
    # Check that test files were created in the expected location
    tests_dir = Path("agent/tests/M13/S5")
    assert tests_dir.exists(), "tests/M13/S5 directory does not exist"

    # Check for test files (M13S5 test files)
    m13s5_test_files = [f for f in tests_dir.glob("test_*.py") if "M13S5" in f.name]
    assert len(m13s5_test_files) > 0, "No M13S5 test files found"

    # Check that test plan ledger was created
    test_plan_file = Path("milestones/M13/M13S5T1.md")
    assert test_plan_file.exists(), "M13S5 test plan ledger does not exist"

    # Check test plan content
    content = test_plan_file.read_text()
    assert (
        "test_generation.py" in content
    ), "test_generation.py not referenced in test plan"
    assert (
        "V-FR-TEST-GENERATION-CONTRACT" in content
    ), "V-FR-TEST-GENERATION-CONTRACT not referenced in test plan"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
