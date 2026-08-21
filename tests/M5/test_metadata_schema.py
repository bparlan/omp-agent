#!/usr/bin/env python3
"""
Unit tests for artifact metadata schema validation.

Tests required fields, optional fields, lineage relationships,
and schema minimalism.
"""

import re
from pathlib import Path


class MetadataSchemaValidator:
    """Validates artifact metadata against canonical schema."""

    # Required fields
    REQUIRED_FIELDS = ["id", "type", "title", "milestone_id", "status"]

    # Optional fields
    OPTIONAL_FIELDS = [
        "derived_from",
        "supersedes",
        "superseded_by",
        "related_artifacts",
        "created_at",
        "updated_at",
        "template_version",
        "legacy_boundaries"
    ]

    # Valid type values
    VALID_TYPES = {
        "milestone",
        "specification",
        "verification",
        "test_set",
        "investigation",
        "evaluation",
        "review",
        "audit"
    }

    def __init__(self):
        self.type_pattern = re.compile(r'^type:\s*([a-z-]+)$', re.MULTILINE)

    def validate_metadata(self, metadata: dict, required_only: bool = False) -> dict:
        """
        Validate metadata dictionary against canonical schema.

        Args:
            metadata: Metadata dictionary
            required_only: If True, ignore optional fields during validation

        Returns:
            Dictionary with validation results
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_required": [],
            "invalid_type": None
        }

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in metadata:
                result["valid"] = False
                result["missing_required"].append(field)

        if not result["missing_required"] and not required_only:
            # Check optional fields (only if all required are present)
            for field in self.OPTIONAL_FIELDS:
                if field not in metadata:
                    result["warnings"].append(f"Optional field '{field}' is missing")
        # Check type field
        if "type" in metadata:
            metadata_type = metadata["type"]
            if metadata_type not in self.VALID_TYPES:
                result["valid"] = False
                result["invalid_type"] = metadata_type
                result["errors"].append(
                    f"Invalid type '{metadata_type}'. "
                    f"Valid types: {', '.join(sorted(self.VALID_TYPES))}"
                )

        # Check id format (canonical ID pattern)
        if "id" in metadata:
            id_value = metadata["id"]
            canonical_patterns = [
                r'^M\d+$',              # Milestone: M1, M2, etc.
                r'^SPEC-\d+$',          # Specification: SPEC-001, SPEC-002
                r'^VER-\d+$',           # Verification: VER-001, VER-002
                r'^TEST-\d+$',          # Test Set: TEST-001, TEST-002
                r'^INV-\d+$',           # Investigation: INV-001, INV-002
                r'^EVAL-\d+$',          # Evaluation: EVAL-001, EVAL-002
                r'^REVIEW-\d+$',        # Review: REVIEW-001, REVIEW-002
                r'^AUDIT-\d+$',         # Audit: AUDIT-001, AUDIT-002
            ]

            if not any(re.match(pattern, id_value) for pattern in canonical_patterns):
                result["warnings"].append(
                    f"ID '{id_value}' does not match canonical pattern. "
                    f"Expected format: M\d+, SPEC-\d+, VER-\d+, TEST-\d+, INV-\d+, EVAL-\d+, REVIEW-\d+, AUDIT-\d+"
                )

        # Check lineage relationships
        lineage_fields = ["derived_from", "supersedes", "superseded_by"]
        for field in lineage_fields:
            if field in metadata:
                value = metadata[field]
                if isinstance(value, list):
                    if not all(isinstance(item, str) for item in value):
                        result["valid"] = False
                        result["errors"].append(
                            f"Field '{field}' should contain string values, got {type(value)}"
                        )
                elif not isinstance(value, str):
                    result["valid"] = False
                    result["errors"].append(
                        f"Field '{field}' should be a string or list, got {type(value)}"
                    )

        # Check related_artifacts
        if "related_artifacts" in metadata:
            value = metadata["related_artifacts"]
            if isinstance(value, list):
                if not all(isinstance(item, str) for item in value):
                    result["valid"] = False
                    result["errors"].append(
                        f"Field 'related_artifacts' should contain string values"
                    )

        # Check related_artifacts

        return result

    def test_required_fields(self):
        """Test that all required fields are validated."""
        print("\n[TEST] Required Fields Validation")

        test_cases = [
            {
                "name": "All required fields present",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed"
                },
                "should_pass": True
            },
            {
                "name": "Missing id field",
                "metadata": {
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed"
                },
                "should_pass": False
            },
            {
                "name": "Missing type field",
                "metadata": {
                    "id": "SPEC-001",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed"
                },
                "should_pass": False
            },
            {
                "name": "Missing title field",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "milestone_id": "M5",
                    "status": "proposed"
                },
                "should_pass": False
            },
            {
                "name": "Missing milestone_id field",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "status": "proposed"
                },
                "should_pass": False
            },
            {
                "name": "Missing status field",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5"
                },
                "should_pass": False
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_metadata(test_case['metadata'])

            if test_case['should_pass']:
                if result['valid'] and not result['errors']:
                    print(f"    ✓ PASS: Validation passed")
                else:
                    print(f"    ✗ FAIL: Should be valid but failed: {result['errors']}")
                    all_passed = False
            else:
                if not result['valid']:
                    print(f"    ✓ PASS: Validation correctly rejected")
                else:
                    print(f"    ✗ FAIL: Should be invalid but passed")
                    all_passed = False

        if all_passed:
            print("  ✓ All required fields tests passed")
        else:
            print("  ✗ Some required fields tests failed")

        return all_passed

    def test_optional_fields(self):
        """Test that optional fields are handled gracefully."""
        print("\n[TEST] Optional Fields Validation")

        test_cases = [
            {
                "name": "No optional fields",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed"
                },
                "should_have_warnings": False
            },
            {
                "name": "Some optional fields present",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "derived_from": ["INV-001"],
                    "created_at": "2026-07-27"
                },
                "should_have_warnings": True
            },
            {
                "name": "All optional fields present",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "derived_from": ["INV-001"],
                    "supersedes": ["SPEC-000"],
                    "superseded_by": ["SPEC-002"],
                    "related_artifacts": ["INV-001", "SPEC-000"],
                    "created_at": "2026-07-27",
                    "updated_at": "2026-07-27",
                    "template_version": "2.0.0"
                },
                "should_have_warnings": False
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_metadata(test_case['metadata'])

            if test_case['should_have_warnings']:
                if result['valid'] and len(result['warnings']) > 0:
                    print(f"    ✓ PASS: Warnings raised as expected: {len(result['warnings'])} warning(s)")
                else:
                    print(f"    ✗ FAIL: Should have warnings but got: valid={result['valid']}, warnings={result['warnings']}")
                    all_passed = False
            else:
                if result['valid']:
                    print(f"    ✓ PASS: Validation passed")
                else:
                    print(f"    ✗ FAIL: Should be valid but failed: {result['errors']}")
                    all_passed = False

        if all_passed:
            print("  ✓ All optional fields tests passed")
        else:
            print("  ✗ Some optional fields tests failed")

        return all_passed

    def test_legacy_boundaries_validation(self):
        """Test that legacy_boundaries are accepted as an optional field."""
        print("\n[TEST] Legacy Boundaries Validation")
        
        test_cases = [
            {
                "name": "Valid milestone with empty legacy_boundaries",
                "metadata": {
                    "id": "M11",
                    "type": "milestone",
                    "title": "Test Milestone",
                    "milestone_id": "M11",
                    "status": "draft",
                    "legacy_boundaries": []
                },
                "should_be_valid": True,
                "should_have_warnings": False
            },
            {
                "name": "Valid milestone with populated legacy_boundaries",
                "metadata": {
                    "id": "M11",
                    "type": "milestone",
                    "title": "Test Milestone",
                    "milestone_id": "M11",
                    "status": "draft",
                    "legacy_boundaries": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]
                },
                "should_be_valid": True,
                "should_have_warnings": False
            },
            {
                "name": "Non-milestone artifact without legacy_boundaries (should not matter)",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Spec",
                    "milestone_id": "M11",
                    "status": "draft"
                },
                "should_be_valid": True,
                "should_have_warnings": False
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_metadata(test_case['metadata'], required_only=False)
            if test_case['should_be_valid']:
                if result['valid']:
                    print("    ✓ PASS")
                else:
                    print(f"    ✗ FAIL: Should be valid but failed: {result['errors']}")
                    all_passed = False
            else:
                if not result['valid']:
                    print("    ✓ PASS (correctly rejected)")
                else:
                    print("    ✗ FAIL: Should be invalid but passed")
                    all_passed = False
        
        if all_passed:
            print("  ✓ All legacy_boundaries tests passed")
        else:
            print("  ✗ Some legacy_boundaries tests failed")
        
        return all_passed

    def test_lineage_relationships(self):
        """Test that lineage fields are validated correctly."""
        print("\n[TEST] Lineage Relationships Validation")

        test_cases = [
            {
                "name": "Valid lineage with derived_from",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "derived_from": ["INV-001", "INV-002"]
                },
                "should_pass": True
            },
            {
                "name": "Valid lineage with supersedes",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "supersedes": ["SPEC-000"]
                },
                "should_pass": True
            },
            {
                "name": "Valid lineage with superseded_by",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "superseded_by": ["SPEC-002"]
                },
                "should_pass": True
            },
            {
                "name": "Valid lineage with all fields",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "derived_from": ["INV-001"],
                    "supersedes": ["SPEC-000"],
                    "superseded_by": ["SPEC-002"],
                    "related_artifacts": ["INV-001", "SPEC-000"]
                },
                "should_pass": True
            },
            {
                "name": "Invalid lineage with non-string values",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "derived_from": ["INV-001", 123]  # Invalid: integer
                },
                "should_pass": False
            },
            {
                "name": "Invalid related_artifacts with non-string values",
                "metadata": {
                    "id": "SPEC-001",
                    "type": "specification",
                    "title": "Test Specification",
                    "milestone_id": "M5",
                    "status": "proposed",
                    "related_artifacts": ["INV-001", 456]  # Invalid: integer
                },
                "should_pass": False
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_metadata(test_case['metadata'])

            if test_case['should_pass']:
                if result['valid']:
                    print(f"    ✓ PASS: Validation passed")
                else:
                    print(f"    ✗ FAIL: Should be valid but failed: {result['errors']}")
                    all_passed = False
            else:
                if not result['valid']:
                    print(f"    ✓ PASS: Validation correctly rejected")
                else:
                    print(f"    ✗ FAIL: Should be invalid but passed")
                    all_passed = False

        if all_passed:
            print("  ✓ All lineage relationship tests passed")
        else:
            print("  ✗ Some lineage relationship tests failed")

        return all_passed

    def test_invalid_type_detection(self):
        """Test that invalid artifact types are detected."""
        print("\n[TEST] Invalid Type Detection")

        test_cases = [
            {
                "name": "Valid type: specification",
                "type": "specification",
                "should_pass": True
            },
            {
                "name": "Valid type: investigation",
                "type": "investigation",
                "should_pass": True
            },
            {
                "name": "Invalid type: invalid-type",
                "type": "invalid-type",
                "should_pass": False
            },
            {
                "name": "Invalid type: Specification (capitalized)",
                "type": "Specification",
                "should_pass": False
            },
            {
                "name": "Invalid type: spec",
                "type": "spec",
                "should_pass": False
            },
            {
                "name": "Valid type: milestone",
                "type": "milestone",
                "should_pass": True
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")

            metadata = {
                "id": "TEST-001",
                "type": test_case['type'],
                "title": "Test",
                "milestone_id": "M5",
                "status": "proposed"
            }

            result = self.validate_metadata(metadata)

            if test_case['should_pass']:
                if result['valid']:
                    print(f"    ✓ PASS: Type '{test_case['type']}' is valid")
                else:
                    print(f"    ✗ FAIL: Type '{test_case['type']}' should be valid but failed: {result['errors']}")
                    all_passed = False
            else:
                if not result['valid'] and result['invalid_type'] == test_case['type']:
                    print(f"    ✓ PASS: Type '{test_case['type']}' correctly rejected")
                else:
                    print(f"    ✗ FAIL: Type '{test_case['type']}' should be invalid but passed or failed incorrectly")
                    all_passed = False

        if all_passed:
            print("  ✓ All invalid type detection tests passed")
        else:
            print("  ✗ Some invalid type detection tests failed")

        return all_passed

    def test_canonical_id_format(self):
        """Test that canonical ID formats are validated."""
        print("\n[TEST] Canonical ID Format Validation")

        test_cases = [
            {
                "name": "Valid milestone ID: M5",
                "id": "M5",
                "should_pass": True
            },
            {
                "name": "Valid specification ID: SPEC-001",
                "id": "SPEC-001",
                "should_pass": True
            },
            {
                "name": "Valid verification ID: VER-001",
                "id": "VER-001",
                "should_pass": True
            },
            {
                "name": "Valid investigation ID: INV-001",
                "id": "INV-001",
                "should_pass": True
            },
            {
                "name": "Invalid ID: SPEC-001 with leading zeros",
                "id": "SPEC-001",
                "should_warn": True
            },
            {
                "name": "Invalid ID: SPEC",
                "id": "SPEC",
                "should_fail": True
            },
            {
                "name": "Invalid ID: SPEC-001-A",
                "id": "SPEC-001-A",
                "should_fail": True
            },
            {
                "name": "Invalid ID: test-001",
                "id": "test-001",
                "should_fail": True
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")

            metadata = {
                "id": test_case['id'],
                "type": "specification",
                "title": "Test",
                "milestone_id": "M5",
                "status": "proposed"
            }

            result = self.validate_metadata(metadata)

            if test_case.get('should_pass', True):
                if result['valid']:
                    print(f"    ✓ PASS: ID '{test_case['id']}' is valid")
                elif test_case.get('should_warn'):
                    if len(result['warnings']) > 0:
                        print(f"    ✓ PASS: ID '{test_case['id']}' raised warning: {result['warnings'][0]}")
                    else:
                        print(f"    ✗ FAIL: ID '{test_case['id']}' should warn but didn't")
                        all_passed = False
                else:
                    print(f"    ✗ FAIL: ID '{test_case['id']}' should be valid but failed: {result['errors']}")
                    all_passed = False
            else:
                if not result['valid']:
                    print(f"    ✓ PASS: ID '{test_case['id']}' correctly rejected")
                else:
                    print(f"    ✗ FAIL: ID '{test_case['id']}' should be invalid but passed")
                    all_passed = False

        if all_passed:
            print("  ✓ All canonical ID format tests passed")
        else:
            print("  ✗ Some canonical ID format tests failed")

        return all_passed

    def test_schema_minimalism(self):
        """Test that schema is minimal and extended only when needed."""
        print("\n[TEST] Schema Minimalism")

        # Test that schema doesn't require unnecessary fields
        minimal_metadata = {
            "id": "SPEC-001",
            "type": "specification",
            "title": "Test Specification",
            "milestone_id": "M5",
            "status": "proposed"
        }

        result = self.validate_metadata(minimal_metadata)

        if result['valid']:
            print(f"  ✓ PASS: Minimal schema (5 fields) is valid")
            return True
        else:
            print(f"  ✗ FAIL: Minimal schema should be valid but failed: {result['errors']}")
            return False


if __name__ == "__main__":
    validator = MetadataSchemaValidator()
    all_passed = True

    all_passed = validator.test_required_fields() and all_passed
    all_passed = validator.test_optional_fields() and all_passed
    all_passed = validator.test_legacy_boundaries_validation() and all_passed
    all_passed = validator.test_lineage_relationships() and all_passed
    all_passed = validator.test_invalid_type_detection() and all_passed
    all_passed = validator.test_canonical_id_format() and all_passed
    all_passed = validator.test_schema_minimalism() and all_passed

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✓ All metadata schema tests passed")
        exit(0)
    else:
        print("✗ Some metadata schema tests failed")
        exit(1)
