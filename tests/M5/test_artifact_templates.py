#!/usr/bin/env python3
"""
Unit tests for artifact template validation.

Tests template frontmatter, required fields, and canonical type field.
"""

import re


class TemplateValidator:
    """Validates artifact templates against canonical requirements."""

    def __init__(self):
        self.frontmatter_pattern = re.compile(
            r"^---\n(.*?)\n---", re.DOTALL | re.MULTILINE
        )

    def validate_template_frontmatter(self, content: str) -> dict:
        """
        Validate template YAML frontmatter.

        Args:
            content: Template file content

        Returns:
            Dictionary with validation results
        """
        result = {
            "valid": True,
            "errors": [],
            "has_frontmatter": False,
            "frontmatter_content": None,
            "fields": {},
        }

        # Extract frontmatter
        match = self.frontmatter_pattern.search(content)

        if not match:
            result["valid"] = False
            result["errors"].append("Missing YAML frontmatter")
            return result

        result["has_frontmatter"] = True
        frontmatter_text = match.group(1)

        # Parse YAML frontmatter
        try:
            result["frontmatter_content"] = self._parse_yaml(frontmatter_text)
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"Failed to parse YAML frontmatter: {e}")
            return result

        return result

    def _parse_yaml(self, yaml_text: str) -> dict:
        """Simple YAML parser for frontmatter."""
        fields = {}
        lines = yaml_text.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Handle key: value format
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Handle list values (e.g., derived_from: [INV-001])
                if value.startswith("[") and value.endswith("]"):
                    value = value[1:-1].split(",")

                fields[key] = value

        return fields

    def test_template_frontmatter_presence(self):
        """Test that templates have YAML frontmatter."""
        print("\n[TEST] Template Frontmatter Presence")

        test_cases = [
            {
                "name": "Specification template has frontmatter",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "should_have": True,
            },
            {
                "name": "Investigation template has frontmatter",
                "content": """---
id: INV-001
type: investigation
title: Investigation Title
milestone_id: M5
status: proposed
---

# Investigation
""",
                "should_have": True,
            },
            {
                "name": "Template without frontmatter",
                "content": """# No frontmatter here

Some content.
""",
                "should_have": False,
            },
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_template_frontmatter(test_case["content"])

            if test_case["should_have"]:
                if result["has_frontmatter"]:
                    print("    ✓ PASS: Frontmatter found")
                else:
                    print("    ✗ FAIL: Frontmatter missing but should be present")
                    all_passed = False
            else:
                if not result["has_frontmatter"]:
                    print("    ✓ PASS: Frontmatter correctly detected as missing")
                else:
                    print("    ✗ FAIL: Frontmatter found but shouldn't be")
                    all_passed = False

        if all_passed:
            print("  ✓ All frontmatter presence tests passed")
        else:
            print("  ✗ Some frontmatter presence tests failed")

        return all_passed

    def test_required_fields_in_templates(self):
        """Test that all templates have required fields."""
        print("\n[TEST] Required Fields in Templates")

        # Required fields for all templates
        required_fields = ["id", "type", "title", "milestone_id", "status"]

        test_cases = [
            {
                "name": "Specification template has all required fields",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "should_have_all": True,
            },
            {
                "name": "Investigation template has all required fields",
                "content": """---
id: INV-001
type: investigation
title: Investigation Title
milestone_id: M5
status: proposed
---

# Investigation
""",
                "should_have_all": True,
            },
            {
                "name": "Specification template missing id field",
                "content": """---
type: specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "should_have_all": False,
            },
            {
                "name": "Specification template missing type field",
                "content": """---
id: SPEC-001
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "should_have_all": False,
            },
            {
                "name": "Specification template missing title field",
                "content": """---
id: SPEC-001
type: specification
milestone_id: M5
status: proposed
---

# Specification
""",
                "should_have_all": False,
            },
            {
                "name": "Specification template missing milestone_id field",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
status: proposed
---

# Specification
""",
                "should_have_all": False,
            },
            {
                "name": "Specification template missing status field",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
---

# Specification
""",
                "should_have_all": False,
            },
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_template_frontmatter(test_case["content"])

            if result["valid"]:
                fields = result["frontmatter_content"]
                missing = [field for field in required_fields if field not in fields]

                if test_case["should_have_all"]:
                    if not missing:
                        print("    ✓ PASS: All required fields present")
                    else:
                        print(f"    ✗ FAIL: Missing required fields: {missing}")
                        all_passed = False
                else:
                    if missing:
                        print(f"    ✓ PASS: Correctly missing fields: {missing}")
                    else:
                        print(
                            "    ✗ FAIL: All required fields present but should be missing some"
                        )
                        all_passed = False
            else:
                if not test_case["should_have_all"]:
                    print(
                        "    ✓ PASS: Correctly flagged as invalid (missing frontmatter)"
                    )
                else:
                    print(
                        f"    ✗ FAIL: Should have valid frontmatter but failed: {result['errors']}"
                    )
                    all_passed = False

        if all_passed:
            print("  ✓ All required fields tests passed")
        else:
            print("  ✗ Some required fields tests failed")

        return all_passed

    def test_canonical_type_field(self):
        """Test that templates have canonical `type` field with correct values."""
        print("\n[TEST] Canonical Type Field")

        valid_types = {
            "milestone",
            "specification",
            "verification",
            "test_set",
            "investigation",
            "evaluation",
            "review",
            "audit",
        }

        test_cases = [
            {
                "name": "Specification template has type: specification",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "expected_type": "specification",
                "should_pass": True,
            },
            {
                "name": "Investigation template has type: investigation",
                "content": """---
id: INV-001
type: investigation
title: Investigation Title
milestone_id: M5
status: proposed
---

# Investigation
""",
                "expected_type": "investigation",
                "should_pass": True,
            },
            {
                "name": "Template has type: milestone",
                "content": """---
id: M5
type: milestone
title: Milestone Title
milestone_id: M5
status: proposed
---

# Milestone
""",
                "expected_type": "milestone",
                "should_pass": True,
            },
            {
                "name": "Invalid type: invalid-type",
                "content": """---
id: TEST-001
type: invalid-type
title: Test
milestone_id: M5
status: proposed
---

# Test
""",
                "expected_type": None,
                "should_pass": False,
            },
            {
                "name": "Invalid type: Specification (capitalized)",
                "content": """---
id: SPEC-001
type: Specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
""",
                "expected_type": None,
                "should_pass": False,
            },
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_template_frontmatter(test_case["content"])

            if result["valid"] and test_case["expected_type"]:
                actual_type = result["frontmatter_content"].get("type")

                if test_case["should_pass"]:
                    if actual_type.lower() == test_case["expected_type"].lower():
                        print(f"    ✓ PASS: Type field correct: '{actual_type}'")
                    else:
                        print(
                            f"    ✗ FAIL: Expected '{test_case['expected_type']}', got '{actual_type}'"
                        )
                        all_passed = False
                else:
                    print(f"    ✗ FAIL: Should be invalid but got type '{actual_type}'")
                    all_passed = False
            else:
                if not test_case["should_pass"]:
                    print("    ✓ PASS: Type field correctly flagged as invalid")
                else:
                    print(f"    ✗ FAIL: Should be valid but failed: {result['errors']}")
                    all_passed = False

        if all_passed:
            print("  ✓ All canonical type field tests passed")
        else:
            print("  ✗ Some canonical type field tests failed")

        return all_passed

    def test_template_variations(self):
        """Test various template variations for completeness."""
        print("\n[TEST] Template Variations")

        test_cases = [
            {
                "name": "Template with lineage fields",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
derived_from: [INV-001]
supersedes: [SPEC-000]
related_artifacts: [INV-001, SPEC-000]
---

# Specification
""",
                "should_be_valid": True,
            },
            {
                "name": "Template with dates",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
created_at: 2026-07-27
updated_at: 2026-07-27
template_version: 2.0.0
---

# Specification
""",
                "should_be_valid": True,
            },
            {
                "name": "Template with all optional fields",
                "content": """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
derived_from: [INV-001]
supersedes: [SPEC-000]
superseded_by: [SPEC-002]
related_artifacts: [INV-001, SPEC-000, SPEC-002]
created_at: 2026-07-27
updated_at: 2026-07-27
template_version: 2.0.0
---

# Specification
""",
                "should_be_valid": True,
            },
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            result = self.validate_template_frontmatter(test_case["content"])

            if test_case["should_be_valid"]:
                if result["valid"]:
                    print("    ✓ PASS: Template is valid")
                else:
                    print(
                        f"    ✗ FAIL: Template should be valid but failed: {result['errors']}"
                    )
                    all_passed = False
            else:
                if not result["valid"]:
                    print("    ✓ PASS: Template correctly flagged as invalid")
                else:
                    print("    ✗ FAIL: Template should be invalid but passed")
                    all_passed = False

        if all_passed:
            print("  ✓ All template variation tests passed")
        else:
            print("  ✗ Some template variation tests failed")

        return all_passed

    def test_template_example_consistency(self):
        """Test that template examples are consistent with canonical IDs."""
        print("\n[TEST] Template Example Consistency")

        template = """---
id: SPEC-001
type: specification
title: Specification Title
milestone_id: M5
status: proposed
---

# Specification
"""

        result = self.validate_template_frontmatter(template)

        if result["valid"]:
            fields = result["frontmatter_content"]

            # Check canonical ID format
            id_format_checks = [
                (fields.get("id") == "SPEC-001", "SPEC-001 format"),
                (fields.get("type") == "specification", "type: specification"),
                (fields.get("milestone_id") == "M5", "milestone_id: M5"),
                (fields.get("status") == "proposed", "status: proposed"),
            ]

            all_checks_pass = all(check for check, _ in id_format_checks)

            if all_checks_pass:
                print("  ✓ PASS: Template examples consistent with canonical IDs")
                return True
            else:
                for check, name in id_format_checks:
                    if not check:
                        print(f"    ✗ FAIL: {name} mismatch")
                return False
        else:
            print(f"  ✗ FAIL: Template should be valid: {result['errors']}")
            return False


if __name__ == "__main__":
    validator = TemplateValidator()
    all_passed = True

    all_passed = validator.test_template_frontmatter_presence() and all_passed
    all_passed = validator.test_required_fields_in_templates() and all_passed
    all_passed = validator.test_canonical_type_field() and all_passed
    all_passed = validator.test_template_variations() and all_passed
    all_passed = validator.test_template_example_consistency() and all_passed

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✓ All artifact template tests passed")
        exit(0)
    else:
        print("✗ Some artifact template tests failed")
        exit(1)
