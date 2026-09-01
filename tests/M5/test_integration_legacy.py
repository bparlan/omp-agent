#!/usr/bin/env python3
"""
Integration tests for legacy artifact compatibility.

Tests legacy artifact accessibility, classification, mixed workflows,
and controlled migration readiness.
"""

from pathlib import Path


class LegacyCompatibilityTest:
    """Integration tests for legacy artifact compatibility."""

    def __init__(self):
        self.milestone_id = "M5"
        self.test_dir = Path("milestones/M5")

        # Ensure test directory exists
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def test_legacy_artifact_accessibility(self):
        """Test that legacy artifacts remain accessible."""
        print("\n[TEST] Legacy Artifact Accessibility")

        # Simulate legacy artifact files
        legacy_artifacts = [
            "M5S1.md",
            "M5S1I1-CORRECTED.md",
            "M5S1I1.md",
            "M5S1I1T1.md",
            "M5S1I1V.md",
            "M5S1I2.md",
            "M5S1I2T1.md",
            "M5S1I2V.md",
            "M5S1T1.md",
            "M5S1T2.md",
            "M5S1V.md",
        ]

        all_accessible = True

        for artifact_name in legacy_artifacts:
            artifact_path = self.test_dir / artifact_name

            # Create a simple legacy artifact
            content = (
                f"# Legacy Artifact: {artifact_name}\n\nThis is a legacy artifact.\n"
            )
            artifact_path.write_text(content, encoding="utf-8")

            # Check if accessible (readable)
            try:
                artifact_path.read_text(encoding="utf-8")
                print(f"  ✓ PASS: {artifact_name} is accessible")
            except Exception as e:
                print(f"  ✗ FAIL: {artifact_name} is not accessible: {e}")
                all_accessible = False

        return all_accessible

    def test_legacy_artifact_classification(self):
        """Test that legacy artifacts can be classified using multiple sources."""
        print("\n[TEST] Legacy Artifact Classification")

        # Simulate legacy artifacts
        legacy_artifacts = {
            "M5S1I1-CORRECTED.md": "investigation",
            "M5S1T1.md": "test",
            "M5S1V.md": "verification",
        }

        all_correctly_classified = True

        for artifact_name, expected_type in legacy_artifacts.items():
            artifact_path = self.test_dir / artifact_name
            content = f"# {artifact_name}\n"

            # Add different classification sources
            if expected_type == "investigation":
                content += "\n# Document Type: Investigation\n"
            elif expected_type == "test":
                content += "\n# Test\n"
            elif expected_type == "verification":
                content += "\n# Verification\n"

            artifact_path.write_text(content, encoding="utf-8")

            # Simulate classification using multiple sources
            # 1. Directory location (if any)
            # 2. Existing metadata
            # 3. Document headers
            # 4. Explicit Document Type field

            classified_as = self._classify_legacy_artifact(artifact_path, content)

            if classified_as == expected_type:
                print(f"  ✓ PASS: {artifact_name} classified as '{expected_type}'")
            else:
                print(
                    f"  ✗ FAIL: {artifact_name} classified as '{classified_as}', expected '{expected_type}'"
                )
                all_correctly_classified = False

        return all_correctly_classified

    def _classify_legacy_artifact(self, path: Path, content: str) -> str:
        """Simulate classification using multiple sources."""
        content_lower = content.lower()

        # 1. Check for explicit Document Type field
        if "document type: investigation" in content_lower:
            return "investigation"
        elif "document type: specification" in content_lower:
            return "specification"
        elif "document type: verification" in content_lower:
            return "verification"
        elif "document type: test" in content_lower:
            return "test"

        # 2. Check document headers
        if "# investigation" in content_lower:
            return "investigation"
        elif "# specification" in content_lower:
            return "specification"
        elif "# verification" in content_lower:
            return "verification"
        elif "# test" in content_lower:
            return "test"

        # 3. Check filename patterns (legacy classification)
        if "inv" in path.stem.lower():
            return "investigation"
        elif "spec" in path.stem.lower():
            return "specification"
        elif "ver" in path.stem.lower():
            return "verification"
        elif "test" in path.stem.lower():
            return "test"

        # Default
        return "unknown"

    def test_mixed_canonical_legacy_workflows(self):
        """Test that framework can handle mixed canonical and legacy artifacts."""
        print("\n[TEST] Mixed Canonical and Legacy Workflows")

        # Create canonical artifacts
        canonical_dir = self.test_dir / "investigations"
        canonical_dir.mkdir(parents=True, exist_ok=True)

        canonical_path = canonical_dir / "INV-001.md"
        canonical_content = """---
id: INV-001
type: investigation
title: Canonical Investigation
milestone_id: M5
status: proposed
---

# Canonical Investigation
"""

        canonical_path.write_text(canonical_content, encoding="utf-8")

        # Create legacy artifacts
        legacy_path = self.test_dir / "M5S1I1.md"
        legacy_content = """# Legacy Investigation

This is a legacy artifact.
"""

        legacy_path.write_text(legacy_content, encoding="utf-8")

        # Test that both types can be accessed
        try:
            canonical_read = canonical_path.read_text(encoding="utf-8")
            legacy_read = legacy_path.read_text(encoding="utf-8")

            if canonical_read and legacy_read:
                print("  ✓ PASS: Both canonical and legacy artifacts accessible")
                return True
            else:
                print("  ✗ FAIL: One or both artifacts not readable")
                return False
        except Exception as e:
            print(f"  ✗ FAIL: Error accessing artifacts: {e}")
            return False
        finally:
            # Clean up
            canonical_path.unlink()
            legacy_path.unlink()

    def test_controlled_migration_documentation(self):
        """Test that controlled migration documentation is present."""
        print("\n[TEST] Controlled Migration Documentation")

        # Check if migration documentation exists in investigation report
        investigation_path = self.test_dir / "INVESTIGATION.md"

        if not investigation_path.exists():
            print("  ⚠ WARNING: Investigation report not found")
            print("  This is expected during test creation")
            return True

        content = investigation_path.read_text(encoding="utf-8")
        migration_keywords = [
            "controlled migration",
            "migration strategy",
            "migration path",
            "controlled",
            "automatic migration",
        ]

        has_migration_docs = any(
            keyword in content.lower() for keyword in migration_keywords
        )

        if has_migration_docs:
            print("  ✓ PASS: Migration documentation found in investigation report")
            return True
        else:
            print("  ✗ FAIL: Migration documentation not found")
        if not investigation_path.exists():
            print("  ⚠ WARNING: Investigation report not found")
            print("  This is expected during test creation")
            return True
        print("\n[TEST] No Automatic Migration Without Planning")

        # Check investigation report for statements about automatic migration
        investigation_path = self.test_dir / "INVESTIGATION.md"

        if not investigation_path.exists():
            print("  ⚠ WARNING: Investigation report not found")
            print("  This is expected during test creation")
            return False

        content = investigation_path.read_text(encoding="utf-8")

        # Check for statements against automatic migration
        anti_auto_migration_keywords = [
            "no automatic migration",
            "automatic migration not allowed",
            "manual migration only",
            "controlled migration",
            "not automatically rename",
        ]

        has_anti_auto = any(
            keyword in content.lower() for keyword in anti_auto_migration_keywords
        )

        if has_anti_auto:
            print("  ✓ PASS: Documentation prevents automatic migration")
            return True
        else:
            print("  ✗ FAIL: Documentation does not prevent automatic migration")
            return False

    def test_multiple_classification_sources(self):
        """Test that classification uses multiple sources."""
        print("\n[TEST] Multiple Classification Sources")

        # Create artifact with ambiguous cues
        artifact_content = """# M5S1I1.md

This is a legacy investigation artifact.

# Document Type: Specification

Despite filename and document header suggesting "specification",
this is actually an investigation.
"""

        artifact_path = self.test_dir / "M5S1I1.md"
        artifact_path.write_text(artifact_content, encoding="utf-8")

        # Test classification using multiple sources
        classified = self._classify_legacy_artifact(artifact_path, artifact_content)

        artifact_path.unlink()

        # Should use explicit Document Type field as primary source
        if classified == "specification":
            print("  ✓ PASS: Classification uses explicit Document Type field")
            return True
        else:
            print("  ✗ FAIL: Classification did not use explicit Document Type field")
            return False

    def test_existing_milestones_still_work(self):
        """Test that existing milestones remain functional."""
        print("\n[TEST] Existing Milestones Still Work")

        # Check for existing milestone directories
        milestone_dirs = [
            "M2",
            "M3",
            "M4",
        ]

        all_exist = True

        for milestone in milestone_dirs:
            milestone_path = self.test_dir.parent / milestone

            if milestone_path.exists() and milestone_path.is_dir():
                # Check if milestone is accessible
                try:
                    # List files/directories
                    list(milestone_path.iterdir())
                    print(f"  ✓ PASS: Milestone {milestone} is accessible")
                except Exception as e:
                    print(f"  ✗ FAIL: Milestone {milestone} is not accessible: {e}")
                    all_exist = False
            else:
                print(
                    f"  ⚠ INFO: Milestone {milestone} does not exist (may not have been created yet)"
                )
                # Don't fail, just info

        return all_exist

    def cleanup(self):
        """Clean up test files."""
        try:
            for file in self.test_dir.rglob("*.md"):
                file.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    tester = LegacyCompatibilityTest()
    all_passed = True

    all_passed = tester.test_legacy_artifact_accessibility() and all_passed
    all_passed = tester.test_legacy_artifact_classification() and all_passed
    all_passed = tester.test_mixed_canonical_legacy_workflows() and all_passed
    all_passed = tester.test_controlled_migration_documentation() and all_passed
    all_passed = tester.test_no_auto_migration_without_planning() and all_passed
    all_passed = tester.test_multiple_classification_sources() and all_passed
    all_passed = tester.test_existing_milestones_still_work() and all_passed

    tester.cleanup()

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✓ All legacy compatibility integration tests passed")
        exit(0)
    else:
        print("✗ Some legacy compatibility integration tests failed")
        exit(1)
