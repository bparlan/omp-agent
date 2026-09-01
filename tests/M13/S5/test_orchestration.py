#!/usr/bin/env python3
"""
M13S5 Test Orchestration Implementation

Validates the evaluate-tests skill functionality for M13S5 milestone.
Tests the orchestration of generated test suites and evaluation artifact production.

Requirement: FR-VALIDATION-ORCHESTRATION-CONTRACT
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

def test_evaluate_tests_skill_exists():
    """Test that the evaluate-tests skill exists and is executable"""
    skill_path = Path("skills/evaluate-tests/__init__.py")
    assert skill_path.exists(), "evaluate-tests skill does not exist"
    assert skill_path.stat().st_mode & 0o111, "evaluate-tests skill is not executable"

def test_evaluate_tests_creates_evaluation_report():
    """Test that evaluate-tests skill creates evaluation reports"""
    # Run the evaluate-tests skill
    result = subprocess.run([sys.executable, "skills/evaluate-tests/__init__.py"],
                          capture_output=True, text=True)

    assert result.returncode == 0, f"evaluate-tests skill failed with exit code {{result.returncode}}"
    assert "Evaluation report written:" in result.stdout, "No evaluation report was reported as generated"
    assert "EVA-M13S5.md" in result.stdout, "EVA-M13S5.md evaluation artifact not found"

def test_test_orchestration_specification_compliance():
    """Test specification compliance for test orchestration"""
    # Check that EVAL-M13S5.md exists
    eval_file = Path("milestones/M13/EVA-M13S5.md")
    assert eval_file.exists(), "EVA-M13S5.md evaluation artifact does not exist"

    # Read evaluation content
    content = eval_file.read_text()

    # Check for required markers
    assert "spec_id" in content.lower(), "EVA-M13S5.md missing spec_id"
    assert "passed_tests" in content.lower(), "EVA-M13S5.md missing passed_tests"
    assert "total_tests" in content.lower(), "EVA-M13S5.md missing total_tests"
    assert "passed_tests == total_tests" in content.lower(), "EVA-M13S5.md must have passed_tests == total_tests"

    # Check that test plan ledger exists
    test_plan_file = Path("milestones/M13/M13S5T1.md")
    assert test_plan_file.exists(), "M13S5 test plan ledger does not exist"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
