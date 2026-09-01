#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-TYPE_DEFS-001}
# {Requirement IDs: FR-TYPE_DEFS}
# Test Type: IMPLEMENTATION_CHECK

import sys
import os

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.artifact_types import (
    CanonicalArtifactType,
    _ARTIFACT_TYPE_DEFINITIONS,
    _RAW_ARTIFACT_TYPE_DEFINITIONS,
    get_artifact_type,
)


def test_type_definitions():
    sample = get_artifact_type("specification")
    assert sample is not None, "get_artifact_type('specification') returned None"
    assert isinstance(
        sample, CanonicalArtifactType
    ), "Expected CanonicalArtifactType instance"

    expected_types = [
        "specification",
        "verification",
        "test",
        "implementation",
        "milestone",
        "review",
        "evaluation",
        "documentation",
    ]
    for expected_type in expected_types:
        assert (
            expected_type in _ARTIFACT_TYPE_DEFINITIONS
        ), f"_ARTIFACT_TYPE_DEFINITIONS missing type: {expected_type}"
        assert (
            expected_type in _RAW_ARTIFACT_TYPE_DEFINITIONS
        ), f"_RAW_ARTIFACT_TYPE_DEFINITIONS missing type: {expected_type}"

    for type_name, type_def in _RAW_ARTIFACT_TYPE_DEFINITIONS.items():
        assert isinstance(
            type_def, dict
        ), f"Type definition for {type_name} is not a dictionary"
        assert (
            "machine_identifier" in type_def
        ), f"Type definition for {type_name} missing 'machine_identifier'"
        assert (
            "canonical_storage_location" in type_def
        ), f"Type definition for {type_name} missing 'canonical_storage_location'"
        assert (
            "required_metadata" in type_def
        ), f"Type definition for {type_name} missing 'required_metadata'"

    print(
        "PASS: Type definitions module contains CanonicalArtifactType and all expected artifact types"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(test_type_definitions())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
