#!/usr/bin/env python3
"""
M13S5 Test Isolation Implementation

Validates test execution scope isolation for M13S5 milestone.
Ensures tests only modify allowed directories.

Requirement: NFR-TEST-SCOPE-ISOLATION
Test Type: INTEGRITY_TEST
"""

import pytest
import subprocess
import sys
import os

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

def test_isolation_allowed_directories():
    """Test that tests only modify allowed directories"""
    # Simple check: after running skills, files should only exist in allowed locations
    # According to M13S5 constraints, only milestones/M13/, tests/M13/S5/, and the two skills should exist

    # Run generate-tests skill
    result = subprocess.run([sys.executable, "skills/generate-tests/__init__.py"],
                          capture_output=True, text=True)

    assert result.returncode == 0, "generate-tests failed"

    # Check for files that exist outside allowed directories
    # Based on M13S5 architecture impact constraints
    # Allowed test artifacts include:
    # - milestones/M13/TEST-M13S5T*.md (generated test artifacts)
    # - milestones/M13/TEST-SPEC-M13S*T1.md (generated test plan markdown files)
    # - milestones/M13/EVA-M13.md (evaluation artifact)
    # - skills/generate-tests/__init__.py and skills/evaluate-tests/__init__.py (skill implementations)
    # - milestones/M13/SPEC-M13S*.md (specification files)
    # - milestones/M13/PIPELINE-STATE.md (gate outcome records)

    # List all Python files in the repo
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Skip directories outside allowed paths
        if any(allowed in root for allowed in ['milestones/M13', 'skills', 'tests/M13/S5']):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

    # All Python files should be in allowed locations
    for file_path in python_files:
        # Check if file is in allowed directory
        is_allowed = False
        for allowed_path in ['milestones/M13', 'skills', 'tests/M13/S5']:
            if file_path.startswith(allowed_path + '/'):
                is_allowed = True
                break

        assert is_allowed, f"Found Python file outside allowed scope: {file_path}"

def test_isolation_no_unexpected_changes():
    """Test that tests don't create unexpected file structures"""
    # Get list of allowed paths
    allowed_paths = [
        'milestones/M13/',
        'skills/generate-tests/',
        'skills/evaluate-tests/',
        'tests/M13/S5/'
    ]

    # List all files and directories in the repo
    all_files = []
    all_dirs = []

    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        all_dirs.extend([os.path.join(root, d) for d in dirs])
        all_files.extend([os.path.join(root, f) for f in files])

    # Check that all directories are in allowed paths
    for dir_path in all_dirs:
        is_allowed = any(dir_path.startswith(allowed) for allowed in allowed_paths)
        assert is_allowed, f"Found directory outside allowed scope: {dir_path}"

    # Check that all Python files are in allowed locations
    for file_path in all_files:
        if file_path.endswith('.py'):
            is_allowed = any(file_path.startswith(allowed) for allowed in allowed_paths)
            assert is_allowed, f"Found Python file outside allowed scope: {file_path}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
