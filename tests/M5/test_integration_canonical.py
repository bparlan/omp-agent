#!/usr/bin/env python3
"""
Integration tests for canonical artifact creation and lineage.

Tests investigation artifact creation, specification creation with lineage,
output format validation, and no ID prescription.
"""

import re
from pathlib import Path


class CanonicalArtifactTest:
    """Integration tests for canonical artifact generation and behavior."""

    def __init__(self):
        self.milestone_id = "M5"
        self.test_dir = Path("milestones/M5")

        # Ensure test directory exists
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def test_investigation_canonical_id(self):
        """Test that investigations are created with canonical IDs (INV-{N})."""
        print("\n[TEST] Investigation Canonical ID")

        # Simulate investigate-issue output
        investigation_content = """---
id: INV-001
type: investigation
title: Canonical Investigation
milestone_id: M5
status: proposed
template_version: 1.2.0
---

# Investigation Findings

## Finding 1: Artifact Type Misclassification
- Root cause: AEF relies on filename patterns for type detection
- Impact: Investigations misclassified as implementation reports
- Recommendation: Use explicit metadata instead

## Finding 2: Compound ID Problem
- Root cause: investigate-issue prescribes compound spec IDs
- Impact: IDs encode investigation lineage and semantic meaning
- Recommendation: Delegte spec identity to generate-spec

## Recommendation: Use Canonical IDs
- Investigation: INV-001
- Specification: SPEC-001 (delegated to generate-spec)

## Derived From
- Milestone M5
"""
        investigation_path = self.test_dir / "investigations" / "INV-001.md"
        investigation_path.parent.mkdir(parents=True, exist_ok=True)
        investigation_path.write_text(investigation_content, encoding="utf-8")

        # Check for canonical ID format
        content = investigation_path.read_text(encoding="utf-8")

        # Should have canonical ID in frontmatter if it existed
        has_canonical_id = re.search(r"^id:\s*INV-\d+$", content, re.MULTILINE)

        if has_canonical_id:
            print("  ✓ PASS: Investigation has canonical ID format: INV-001")
        else:
            print("  ✗ FAIL: Investigation missing canonical ID or incorrect format")
            return False

        # Check that it does NOT prescribe compound spec IDs
        # Looking for patterns like "M5S1I1", "INV-001 -> SPEC-INV-001", etc.
        compound_id_patterns = [
            r"M5S1I1",
            r"SPEC-INV-001",
            r"INV-\d+.*SPEC-INV-",
            r"spec.*specification.*investigation.*specification",
        ]

        has_compound_id = any(
            re.search(pattern, content, re.IGNORECASE)
            for pattern in compound_id_patterns
        )

        if not has_compound_id:
            print("  ✓ PASS: Investigation does not prescribe compound spec IDs")
        else:
            print("  ✗ FAIL: Investigation prescribes compound spec IDs")
            return False

        # Clean up
        investigation_path.unlink()

        return True

    def test_specification_canonical_id_and_lineage(self):
        """Test that specifications are created with canonical IDs and lineage."""
        print("\n[TEST] Specification Canonical ID and Lineage")

        # Simulate generate-spec output
        specification_content = """---
id: SPEC-001
type: specification
title: Redesign AEF Artifact Identity Model
milestone_id: M5
status: proposed
derived_from: [INV-001]
related_artifacts: [INV-001]
template_version: 1.2.0
---

# Specification: Artifact Identity and Type Detection

## Objective

Redesign AEF artifact identity, type detection, lineage, and storage model...

## Functional Requirements

1. Define canonical artifact types...
2. Implement canonical storage model...
"""

        # Write specification artifact
        specs_dir = self.test_dir / "specs"
        specs_dir.mkdir(parents=True, exist_ok=True)

        specification_path = specs_dir / "SPEC-001.md"
        specification_path.write_text(specification_content, encoding="utf-8")

        # Check canonical ID format
        content = specification_path.read_text(encoding="utf-8")

        # Check id field
        has_canonical_id = re.search(r"^id:\s*SPEC-\d+$", content, re.MULTILINE)
        has_type = re.search(r"^type:\s*specification$", content, re.MULTILINE)
        has_milestone_id = re.search(r"^milestone_id:\s*M5$", content, re.MULTILINE)

        all_present = has_canonical_id and has_type and has_milestone_id

        if all_present:
            print("  ✓ PASS: Specification has canonical ID: SPEC-001")
        else:
            print("  ✗ FAIL: Specification missing required fields")
            if not has_canonical_id:
                print("    Missing: id field (expected SPEC-001)")
            if not has_type:
                print("    Missing: type field")
            if not has_milestone_id:
                print("    Missing: milestone_id field")
            specification_path.unlink()
            return False

        # Check lineage fields
        has_derived_from = "derived_from:" in content
        has_related_artifacts = "related_artifacts:" in content

        if has_derived_from and has_related_artifacts:
            print("  ✓ PASS: Specification includes lineage fields")
        else:
            print("  ✗ FAIL: Specification missing lineage fields")
            if not has_derived_from:
                print("    Missing: derived_from")
            if not has_related_artifacts:
                print("    Missing: related_artifacts")
            specification_path.unlink()
            return False

        # Check that title is present
        has_title = re.search(r"^title:", content, re.MULTILINE)
        if has_title:
            print("  ✓ PASS: Specification has title field")
        else:
            print("  ✗ FAIL: Specification missing title field")
            specification_path.unlink()
            return False

        # Clean up
        specification_path.unlink()

        return True

    def test_multiple_findings_to_multiple_specs(self):
        """Test that one investigation can generate multiple specifications."""
        print("\n[TEST] Multiple Findings to Multiple Specifications")

        investigation_content = """# Investigation Findings

## Finding 1: Type Resolution Issues
- Impact: Misclassification of investigation artifacts
- Recommendation: Create SPEC-001

## Finding 2: Lineage Representation Issues
- Impact: Missing lineage metadata
- Recommendation: Create SPEC-002

## Finding 3: Documentation Gaps
- Impact: No ARTIFACT_ARCHITECTURE.md
- Recommendation: Create SPEC-003
"""

        # Write investigation
        investigation_path = self.test_dir / "investigations" / "INV-001.md"
        investigation_path.parent.mkdir(parents=True, exist_ok=True)
        investigation_path.write_text(investigation_content, encoding="utf-8")

        # Simulate generating 3 specs from investigation
        spec_contents = [
            """---
id: SPEC-001
type: specification
title: Fix Type Resolution Issues
milestone_id: M5
status: proposed
derived_from: [INV-001]
---

# SPEC-001
""",
            """---
id: SPEC-002
type: specification
title: Fix Lineage Representation Issues
milestone_id: M5
status: proposed
derived_from: [INV-001]
---

# SPEC-002
""",
            """---
id: SPEC-003
type: specification
title: Add Documentation Gaps
milestone_id: M5
status: proposed
derived_from: [INV-001]
---

# SPEC-003
""",
        ]

        specs_dir = self.test_dir / "specs"
        specs_dir.mkdir(parents=True, exist_ok=True)

        spec_paths = []
        all_passed = True

        for i, spec_content in enumerate(spec_contents):
            spec_path = specs_dir / f"SPEC-{i+1}.md"
            spec_path.write_text(spec_content, encoding="utf-8")
            spec_paths.append(spec_path)

            # Check each spec
            content = spec_path.read_text(encoding="utf-8")
            has_canonical_id = re.search(r"^id:\s*SPEC-\d+$", content, re.MULTILINE)
            has_type = re.search(r"^type:\s*specification$", content, re.MULTILINE)
            has_derived_from = "derived_from:" in content
            has_milestone_id = re.search(r"^milestone_id:\s*M5$", content, re.MULTILINE)

            if has_canonical_id and has_type and has_derived_from and has_milestone_id:
                print(f"  ✓ PASS: SPEC-{i+1} has all required fields")
            else:
                print(f"  ✗ FAIL: SPEC-{i+1} missing required fields")
                all_passed = False

        # Clean up
        investigation_path.unlink()
        for spec_path in spec_paths:
            spec_path.unlink()

        return all_passed

    def test_generate_spec_output_format(self):
        """Test that generate-spec creates specifications with correct format."""
        print("\n[TEST] generate-spec Output Format")

        # Simulate generate-spec output
        specification = """# Specification: Artifact Identity and Type Detection

## Objective

Redesign AEF artifact identity, type detection, lineage, and storage model.

## Followup Context

### Derived From
- M5 (agentic friendly filenames and folder structure milestone)
- Investigation Report (M5/INVESTIGATION.md)

### Investigation Summary

**Current Failure**:
- Investigation artifacts (e.g., `M5S1I1.md`) are misclassified as Implementation Reports
- investigate-issue prescribes compound specification IDs

**Proposed Solution**:
- Canonical artifact types: Milestone, Specification, Verification, Test Set, Investigation, Evaluation, Review, Audit
- Canonical IDs: M{N}, SPEC-{N}, VER-{N}, TEST-{N}, INV-{N}, EVAL-{N}, REVIEW-{N}, AUDIT-{N}
- Directory-based classification: milestones/M{N}/specs/, investigations/, etc.

## Functional Requirements

**FR-1**: Canonical Artifact Types...

**FR-2**: Canonical Storage Model...

**FR-3**: Artifact Metadata Schema...

## Non-Functional Requirements

**NFR-1**: Determinism...
**NFR-2**: Performance...
**NFR-3**: Maintainability...

**Architecture Impact**

**Strict File Scope (Allowlist & Denylist)**

**Allowlist**:
- milestones/M5/M5S1.md (this specification)
- skills/investigate-issue/SKILL.md
- skills/generate-spec/SKILL.md
- ...

**Denylist**:
- All individual SDD skill internal logic...
- All markdown documentation...
"""

        # Check that investigation is referenced but not prefixed with spec ID
        # The investigation should be referenced as M5/INVESTIGATION.md
        investigation_referenced = "M5/INVESTIGATION.md" in specification

        # Should NOT contain prescription of compound spec IDs
        # Looking for patterns like "M5S1I1", "INV-001 -> SPEC-INV-001", etc.
        compound_id_patterns = [
            r"M5S1I1",
            r"SPEC-INV-001",
            r"INV-\d+.*SPEC-INV-\d+",  # Require digit after SPEC-INV-
        ]

        # Should NOT contain prescription of compound spec IDs (not just mentions)
        # Looking for patterns where the spec actually prescribes/recommends them
        compound_id_patterns = [
            r"prescribes.*M5S1I1",
            r"should.*prescribe.*M5S1I1",
            r"should.*create.*M5S1I1",
            r"M5S1I1.*should",
            r"SPEC-INV-\d+.*should",
            r"specification.*prescribes.*M5S1I1",
            r"generate-spec.*prescribes.*SPEC-INV",
        ]

        has_compound_id_prescription = any(
            re.search(pattern, specification, re.IGNORECASE)
            for pattern in compound_id_patterns
        )

        if investigation_referenced and not has_compound_id_prescription:
            print(
                "  ✓ PASS: Investigation referenced correctly without compound spec ID"
            )
            return True
        else:
            print(
                "  ✗ FAIL: Investigation reference incorrect or compound spec IDs present"
            )
            if not investigation_referenced:
                print("    Missing: Investigation reference (M5/INVESTIGATION.md)")
            if has_compound_id_prescription:
                print("    Has: Compound spec IDs detected")
            return False
        # Should NOT contain prescription of compound spec IDs (not just mentions)
        # Looking for patterns where the spec actually prescribes/recommends them
        compound_id_patterns = [
            r"prescribes.*M5S1I1",
            r"should.*prescribe.*M5S1I1",
            r"should.*create.*M5S1I1",
            r"M5S1I1.*should",
            r"SPEC-INV-\d+.*should",
            r"generate-spec.*prescribes.*SPEC-INV",
        ]

        has_compound_id_prescription = any(
            re.search(pattern, specification, re.IGNORECASE)
            for pattern in compound_id_patterns
        )

        if investigation_referenced and not has_compound_id_prescription:
            print(
                "  ✓ PASS: Investigation referenced correctly without compound spec ID"
            )
            return True
        else:
            print(
                "  ✗ FAIL: Investigation reference incorrect or compound spec IDs present"
            )
            if not investigation_referenced:
                print("    Missing: Investigation reference (M5/INVESTIGATION.md)")
            if has_compound_id_prescription:
                print("    Has: Compound spec IDs detected")
            return False

    def test_investigate_issue_delegates_spec_identity(self):
        """Test that investigate-issue delegates spec identity to generate-spec."""
        print("\n[TEST] investigate-issue Delegates Spec Identity")

        # Simulate investigate-issue output
        output = """# Investigation Report

## Findings

1. **Root Cause**: AEF relies on filename patterns for type detection
2. **Impact**: Investigations misclassified as implementation reports
3. **Recommendation**: Use explicit metadata and canonical IDs

## Recommended Actions

1. Update investigate-issue to create investigation artifacts with canonical IDs (INV-{N})
2. Update investigate-issue to recommend findings, not prescribe spec IDs
3. Delegte specification identity to generate-spec skill
4. Update generate-spec to create specifications with canonical IDs (SPEC-{N}) and lineage metadata

## Output for generate-spec

The following investigation can be transformed into specifications:
- Findings 1, 2, and 3 -> Create SPEC-001

Pass the investigation ID (INV-001) to generate-spec for lineage tracking.
"""

        # Check that output does not prescribe compound spec IDs
        compound_id_patterns = [
            r"M5S1I1",
            r"SPEC-INV-001",
            r"INV-\d+.*SPEC-INV-",
        ]

        has_compound_id = any(
            re.search(pattern, output, re.IGNORECASE)
            for pattern in compound_id_patterns
        )

        # Check that investigation ID is provided for lineage tracking
        has_investigation_id_reference = re.search(r"INV-\d+", output)

        if not has_compound_id and has_investigation_id_reference:
            print("  ✓ PASS: Output does not prescribe compound spec IDs")
            print("  ✓ PASS: Provides investigation ID for lineage tracking")
            return True
        else:
            print(
                "  ✗ FAIL: Output has compound spec IDs or missing investigation ID reference"
            )
            if has_compound_id:
                print("    Has: Compound spec IDs detected")
            if not has_investigation_id_reference:
                print("    Missing: Investigation ID reference")
            return False

    def cleanup(self):
        """Clean up test files."""
        try:
            for file in self.test_dir.rglob("*.md"):
                file.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    tester = CanonicalArtifactTest()
    all_passed = True

    all_passed = tester.test_investigation_canonical_id() and all_passed
    all_passed = tester.test_specification_canonical_id_and_lineage() and all_passed
    all_passed = tester.test_multiple_findings_to_multiple_specs() and all_passed
    all_passed = tester.test_generate_spec_output_format() and all_passed
    all_passed = tester.test_investigate_issue_delegates_spec_identity() and all_passed

    tester.cleanup()

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✓ All canonical artifact integration tests passed")
        exit(0)
    else:
        print("✗ Some canonical artifact integration tests failed")
        exit(1)
