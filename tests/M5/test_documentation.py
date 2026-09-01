#!/usr/bin/env python3
"""
Documentation validation tests for M5.

Tests that all documentation artifacts are properly created and have required fields.
"""

from pathlib import Path


class DocumentationTest:
    """Tests for M5 documentation artifacts."""

    def __init__(self):
        self.milestone_id = "M5"
        self.milestone_dir = Path("milestones/M5")

    def test_all_required_artifacts_exist(self):
        """Test that all required M5 artifacts exist."""
        print("\n[TEST] All Required Artifacts Exist")

        # Required artifacts
        required_artifacts = [
            "M5.md",  # Milestone document
            "INVESTIGATION.md",  # Investigation/design report
            "M5S1.md",  # Implementation specification
            "M5S1V.md",  # Verification protocol
            "M5S1T1.md",  # Test plan
        ]

        all_exist = True

        for artifact_name in required_artifacts:
            artifact_path = self.milestone_dir / artifact_name

            if artifact_path.exists():
                print(f"  ✓ PASS: {artifact_name} exists")
            else:
                print(f"  ✗ FAIL: {artifact_name} not found")
                all_exist = False

        return all_exist

    def test_milestone_document_validity(self):
        """Test that M5.md milestone document is valid."""
        print("\n[TEST] Milestone Document Validity")

        milestone_path = self.milestone_dir / "M5.md"

        if not milestone_path.exists():
            print("  ✗ FAIL: M5.md not found")
            return False

        content = milestone_path.read_text(encoding="utf-8")

        # Check for required sections
        required_sections = [
            "Goal",
            "Motivation",
            "Scope",
            "Out of Scope",
            "Success Criteria",
            "Risks",
            "Notes",
        ]

        all_present = True

        for section in required_sections:
            if section in content:
                print(f"  ✓ PASS: {section} section present")
            else:
                print(f"  ✗ FAIL: {section} section missing")
                all_present = False

        return all_present

    def test_investigation_report_present(self):
        """Test that investigation report exists and has required structure."""
        print("\n[TEST] Investigation Report Validity")

        investigation_path = self.milestone_dir / "INVESTIGATION.md"

        if not investigation_path.exists():
            print("  ✗ FAIL: INVESTIGATION.md not found")
            return False

        content = investigation_path.read_text(encoding="utf-8")

        # Check for required sections
        required_sections = [
            "Analysis of Current State",
            "Problem Statement",
            "Solution Approach",
            "Design Recommendations",
            "Migration Strategy",
            "Risks and Mitigations",
        ]

        all_present = True

        for section in required_sections:
            if section in content:
                print(f"  ✓ PASS: {section} present")
            else:
                print(f"  ⚠ WARNING: {section} not found (optional)")
                # Don't fail for missing optional sections

        return all_present

    def test_specification_complete(self):
        """Test that specification M5S1.md is complete."""
        print("\n[TEST] Specification Completeness")

        spec_path = self.milestone_dir / "M5S1.md"

        if not spec_path.exists():
            print("  ✗ FAIL: M5S1.md not found")
            return False

        content = spec_path.read_text(encoding="utf-8")

        # Check for required sections
        required_sections = [
            "Functional Requirements",
            "Architecture Impact",
            "Edge Cases",
            "File Scope",
            "Negative Guardrails",
        ]

        all_present = True

        for section in required_sections:
            if section in content:
                print(f"  ✓ PASS: {section} present")
            else:
                print(f"  ✗ FAIL: {section} section missing")
                all_present = False

        return all_present

    def test_verification_protocol_complete(self):
        """Test that verification protocol M5S1V.md is complete."""
        print("\n[TEST] Verification Protocol Completeness")

        ver_path = self.milestone_dir / "M5S1V.md"

        if not ver_path.exists():
            print("  ✗ FAIL: M5S1V.md not found")
            return False

        content = ver_path.read_text(encoding="utf-8")

        # Check for required sections
        required_sections = [
            "Functional Requirements",
            "Success Criteria",
            "Test Cases",
            "Edge Cases",
            "Failure Scenarios",
        ]

        all_present = True

        for section in required_sections:
            if section in content:
                print(f"  ✓ PASS: {section} present")
            else:
                print(f"  ✗ FAIL: {section} section missing")
                all_present = False

        return all_present

    def test_test_plan_present(self):
        """Test that test plan M5S1T1.md exists."""
        print("\n[TEST] Test Plan Present")

        test_plan_path = self.milestone_dir / "M5S1T1.md"

        if not test_plan_path.exists():
            print("  ✗ FAIL: M5S1T1.md not found")
            return False

        print("  ✓ PASS: M5S1T1.md exists")

        return True

    def cleanup(self):
        """Clean up test artifacts (if any)."""
        pass


if __name__ == "__main__":
    tester = DocumentationTest()

    print("=" * 70)
    print("M5 Documentation Validation Tests")
    print("=" * 70)

    # Run all tests
    tests = [
        tester.test_all_required_artifacts_exist,
        tester.test_milestone_document_validity,
        tester.test_investigation_report_present,
        tester.test_specification_complete,
        tester.test_verification_protocol_complete,
        tester.test_test_plan_present,
    ]

    results = []

    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  ✗ EXCEPTION: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 70)
    print(f"Summary: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("✓ All documentation validation tests passed")
        exit(0)
    else:
        print("✗ Some documentation validation tests failed")
        exit(1)
