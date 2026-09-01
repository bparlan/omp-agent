#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-VALIDATION_INTEGRATION-1}
# {Requirement IDs: FR-HEALTHCENTER-VALIDATION_INTEGRATION}
# Test Type: UNIT_TEST

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from core.validation import validate_artifact

def main():
    # Test valid health-check artifact metadata
    valid_metadata = {
        "id": "HC-valid-1",
        "type": "health-check",
        "title": "Health Check Artifact",
        "milestone_id": "M9",
        "status": "healthy",
        "derived_from": "SKILL-skill",
        "template_version": "1.3.0",
        "skill_id": "skill_a",
        "validation_score": 100,
        "timestamp": "2024-01-01T00:00:00Z",
        "insights": [],
        "recommendations": [],
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "artifact_identity": "HC-skill_a-1",
            "artifact_type": "health-check"
        }
    }

    # Test invalid health-check artifact metadata
    invalid_metadata = {
        "id": "HC-invalid-1",
        "type": "invalid",  # Wrong type
        "title": "Invalid Health Check Artifact",
        "milestone_id": "M9",
        "status": "healthy",
        "derived_from": "SKILL-skill",
        "template_version": "1.3.0",
        "skill_id": "skill_a",
        "validation_score": 101,  # Score > 100
        "timestamp": "2024-01-01T00:00:00Z",
        "insights": [],
        "recommendations": [],
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "artifact_identity": "HC-skill_a-1",
            "artifact_type": "health-check"
        }
    }

    # Test valid artifact
    valid_result = validate_artifact(valid_metadata)
    if not valid_result.get("valid"):
        print(f"FAIL: Valid artifact rejected: {valid_result}")
        sys.exit(1)

    # Test invalid artifact
    invalid_result = validate_artifact(invalid_metadata)
    if invalid_result.get("valid"):
        print(f"FAIL: Invalid artifact accepted: {invalid_result}")
        sys.exit(1)

    # Check that validation errors are structured
    if not invalid_result.get("errors"):
        print("FAIL: Invalid artifact missing error structure")
        sys.exit(1)

    print("PASS: Validation correctly validates health-check artifacts")
    sys.exit(0)

if __name__ == "__main__":
    main()
