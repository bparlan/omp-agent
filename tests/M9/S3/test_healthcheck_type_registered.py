#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-STORAGE_COMPLIANCE-1}
# {Requirement IDs: FR-HEALTHCENTER-STORAGE_COMPLIANCE}
# Test Type: UNIT_TEST

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from core.artifacts.artifact_types import get_artifact_type


def main():
    # Test health-check artifact type registration
    healthcheck_type = get_artifact_type("health-check")
    if healthcheck_type is None:
        print("FAIL: health-check artifact type is not registered")
        sys.exit(1)

    # Check type definition completeness
    expected_fields = ["canonical_storage_location", "required_metadata"]
    for field in expected_fields:
        if not hasattr(healthcheck_type, field):
            print(f"FAIL: health-check artifact type missing field: {field}")
            sys.exit(1)

    # Verify storage location follows canonical pattern
    expected_location = "<M_ID>/<M_ID>-health-check-<SKILL_NAME>.md"
    if healthcheck_type.canonical_storage_location != expected_location:
        print(
            "FAIL: Unexpected storage location: "
            f"{healthcheck_type.canonical_storage_location}"
        )
        sys.exit(1)

    # Verify required metadata
    required = ["created_at", "updated_at", "artifact_identity", "artifact_type"]
    missing = [key for key in required if key not in healthcheck_type.required_metadata]
    if missing:
        print(f"FAIL: Missing required metadata keys: {missing}")
        sys.exit(1)

    print("PASS: health-check artifact type is registered with canonical storage rules")
    sys.exit(0)


if __name__ == "__main__":
    main()
