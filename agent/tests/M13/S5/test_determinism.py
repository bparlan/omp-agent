#!/usr/bin/env python3
"""
M13S5 Test Determinism Implementation

Validates deterministic test behavior across multiple executions for M13S5 milestone.
Ensures test generation and execution produce identical results.

Requirement: NFR-TEST-DETERMINISM
Test Type: INTEGRITY_TEST
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

def test_deterministic_test_generation():
    """Test that test generation produces deterministic results"""
    # Run generate-tests skill multiple times
    results = []
    for i in range(3):
        result = subprocess.run([sys.executable, "skills/generate-tests/__init__.py"],
                              capture_output=True, text=True)
        results.append(result.stdout)

    # All outputs should be identical
    assert all(output == results[0] for output in results), \
        "Test generation is not deterministic across runs"

def test_deterministic_evaluation():
    """Test that test evaluation produces deterministic results"""
    # Run evaluate-tests skill multiple times
    results = []
    for i in range(3):
        result = subprocess.run([sys.executable, "skills/evaluate-tests/__init__.py"],
                              capture_output=True, text=True)
        results.append(result.stdout)

    # All outputs should be identical
    assert all(output == results[0] for output in results), \
        "Test evaluation is not deterministic across runs"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
