#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-VALIDATOR_INIT-001}
# {Requirement IDs: FR-VALIDATOR_INIT}
# Test Type: IMPLEMENTATION_CHECK

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.getcwd()))

from core.validation import validate_metadata


def test_validator_cli():
    invalid_path = os.path.join(
        "tests", "fixtures", "synthetic_metadata_invalid", "missing_id.md"
    )
    invalid_result = validate_metadata(invalid_path)
    if not isinstance(invalid_result, dict):
        print("FAIL: validate_metadata must return a dictionary")
        return 1
    if invalid_result.get("valid") is not False:
        print("FAIL: validate_metadata returned valid for invalid fixture")
        print(invalid_result)
        return 1

    valid_frontmatter = """---
id: SPEC-M9S1-TVALID
type: specification
title: "Temporary Valid Artifact"
milestone_id: M9
status: draft
derived_from: []
template_version: 1.0.0
metadata:
  created_at: "2025-01-01T00:00:00Z"
  updated_at: "2025-01-01T00:00:00Z"
  artifact_identity: SPEC-M9S1-TVALID
  artifact_type: specification
---
# Body
"""
    fd, valid_path = tempfile.mkstemp(suffix=".md", prefix="valid_artifact_")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(valid_frontmatter)
        valid_result = validate_metadata(valid_path)
        if not isinstance(valid_result, dict):
            print("FAIL: validate_metadata must return a dictionary for valid input")
            return 1
        if valid_result.get("valid") is not True:
            print("FAIL: validate_metadata returned invalid for valid artifact")
            print(valid_result)
            return 1
    finally:
        try:
            os.remove(valid_path)
        except OSError:
            pass

    print(
        "PASS: Validator API returns valid for valid artifact and invalid for invalid artifact"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(test_validator_cli())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
