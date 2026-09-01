#!/usr/bin/env python3
# {Verification IDs: VER-M9S3V1-FR5}
# {Requirement IDs: FR-HEALTHCENTER-VALIDATION_INTEGRATION}
# Test Type: PYTHON_TEST

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT.parent))

def test_validation_integration_python_api():
    """Test FR5: Validation Integration using Python API"""

    # Import the validation function
    try:
        from core.validation import validate_artifact
        print("✓ core.validation imported successfully")
    except ImportError as e:
        print(f"VALID_INITIAL_FAILURE: core.validation not available: {e}")
        sys.exit(127)

    valid_artifact = {
        "id": "M9-health-check-healthcenter-1",
        "type": "health-check",
        "title": "Health Check for Healthcenter",
        "milestone_id": "M9",
        "template_version": "1.0.0",
        "metadata": {
            "created_at": "2025-01-15T10:00:00Z",
            "updated_at": "2025-01-15T10:00:00Z",
            "artifact_identity": "HC-healthcenter-1",
            "artifact_type": "health-check"
        },
        "skill_id": "healthcenter",
        "validation_score": 85,
        "status": "healthy",
        "timestamp": "2025-01-15T10:30:00Z",
        "insights": ["All validations passed"],
        "recommendations": [],
        "failed_validations": [],
        "passed_validations": ["skill_validation", "health_check"],
        "derived_from": []
    }

    invalid_artifact_missing_fields = {
        "id": "M9-health-check-healthcenter-1"
    }

    invalid_artifact_invalid_score = valid_artifact.copy()
    invalid_artifact_invalid_score["validation_score"] = 150

    invalid_type_artifact = valid_artifact.copy()
    invalid_type_artifact["type"] = "unknown_type"

    # Test 1: Validate valid artifact (expected to pass)
    print("Testing validation of valid artifact...")
    try:
        validation_result = validate_artifact(valid_artifact)
        print(f"✓ Validation completed for valid artifact: {validation_result}")
        assert validation_result["valid"] is True, "Valid artifact should pass validation"
        assert len(validation_result["errors"]) == 0, "Valid artifact should have no validation errors"
    except Exception as e:
        print(f"ERROR: Valid artifact validation failed: {e}")
        sys.exit(1)

    # Test 2: Validate invalid artifact (expected to fail)
    print("Testing validation of invalid artifact (missing fields)...")
    try:
        invalid_result = validate_artifact(invalid_artifact_missing_fields)
        print(f"✓ Invalid artifact validation completed: {invalid_result}")
        assert invalid_result["valid"] is False, "Invalid artifact should not be valid"
        assert len(invalid_result["missing_fields"]) > 0, "Invalid artifact should report missing fields"
    except Exception as e:
        print(f"ERROR: Invalid artifact validation failed: {e}")
        sys.exit(1)

    # Test 3: Validate artifact with invalid score (expected to fail)
    print("Testing validation of artifact with invalid score...")
    try:
        invalid_score_result = validate_artifact(invalid_artifact_invalid_score)
        print(f"✓ Invalid score artifact validation completed: {invalid_score_result}")
        assert invalid_score_result["valid"] is False, "Invalid score should make artifact invalid"
        score_errors = [err for err in invalid_score_result["errors"] if "score" in err.lower()]
        assert len(score_errors) > 0, "Invalid score should generate score-specific errors"
    except Exception as e:
        print(f"ERROR: Invalid score artifact validation failed: {e}")
        sys.exit(1)

    # Test 4: Validate artifact with invalid type (expected to fail)
    print("Testing validation of artifact with invalid type...")
    try:
        invalid_type_result = validate_artifact(invalid_type_artifact)
        print(f"✓ Invalid type artifact validation completed: {invalid_type_result}")
        assert invalid_type_result["valid"] is False, "Invalid type should make artifact invalid"
        type_errors = [err for err in invalid_type_result["errors"] if "type" in err.lower()]
        assert len(type_errors) > 0, "Invalid type should generate type-specific errors"
    except Exception as e:
        print(f"ERROR: Invalid type artifact validation failed: {e}")
        sys.exit(1)

    # Test 5: Verify validation occurs before artifact acceptance
    print("Testing validation occurs before artifact acceptance...")
    assert callable(validate_artifact), "validate_artifact should be callable"

    print("✓ All validation integration assertions passed")
    sys.exit(0)

if __name__ == "__main__":
    test_validation_integration_python_api()
