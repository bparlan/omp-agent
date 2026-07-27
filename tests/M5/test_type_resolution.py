#!/usr/bin/env python3
"""
Unit tests for artifact type resolution.

Tests deterministic type resolution, performance (<100ms),
conflict detection, and fail-closed behavior.
"""

import re
import time
from pathlib import Path
from typing import Optional


class ArtifactTypeResolver:
    """Deterministic artifact type resolution with fail-closed conflicts."""

    # Canonical artifact types and their directory patterns
    ARTIFACT_TYPES = {
        "milestone": ["milestone.md"],
        "specification": ["specs/"],
        "verification": ["verifications/"],
        "test_set": ["tests/"],
        "investigation": ["investigations/"],
        "evaluation": ["evaluations/"],
        "review": ["reviews/"],
        "audit": ["audits/"],
    }

    def __init__(self, current_milestone: str = "M5"):
        self.current_milestone = current_milestone
        self.type_pattern = re.compile(r'^type:\s*([a-z-]+)$', re.MULTILINE)

    def resolve_artifact_type(self, path: str) -> str:
        """
        Resolve artifact type using priority:
        1. Explicit `type` field in metadata
        2. Canonical artifact directory
        3. Filename as final fallback

        Args:
            path: Path to artifact file

        Returns:
            Resolved artifact type

        Raises:
            ValueError: If type resolution conflicts
        """
        path_obj = Path(path)

        # Try to extract type from YAML frontmatter
        metadata_type = self._extract_type_from_metadata(path)

        # Determine directory-based type
        directory_type = self._extract_type_from_directory(path_obj)

        # Resolve based on priority
        if metadata_type:
            if directory_type and metadata_type != directory_type:
                # CONFLICT: metadata type differs from directory type
                raise ValueError(
                    f"Artifact type conflict: metadata declares type '{metadata_type}' "
                    f"but artifact is in directory '{directory_type}' directory"
                )
            return metadata_type

        if directory_type:
            return directory_type

        # Fallback to filename
        return self._extract_type_from_filename(path_obj)

    def _extract_type_from_metadata(self, path: str) -> Optional[str]:
        """Extract type from YAML frontmatter."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = self.type_pattern.search(content)
                if match:
                    return match.group(1).lower()
        except FileNotFoundError:
            return None
        except (IOError, OSError) as e:
            print(f"Warning: Could not read {path}: {e}")
            return None

    def _extract_type_from_directory(self, path_obj: Path) -> Optional[str]:
        """Extract type from directory structure."""
        parts = path_obj.parts

        # Find which milestone directory we're in
        milestone_idx = None
        for i, part in enumerate(parts):
            if re.match(r'^M\d+$', part):
                milestone_idx = i
                break

        if milestone_idx is None:
            return None

        # Check subdirectories for canonical type directories
        if milestone_idx + 1 < len(parts):
            subdir = parts[milestone_idx + 1]
            for type_name, directories in self.ARTIFACT_TYPES.items():
                # Handle directories with trailing slashes
                directory_patterns = [d.rstrip('/') for d in directories]
                if subdir in directory_patterns:
                    return type_name
    def _extract_type_from_filename(self, path_obj: Path) -> str:
        """Extract type from filename using canonical pattern."""
        filename = path_obj.stem.lower()

        # Check for canonical filename patterns
        for type_name, directories in self.ARTIFACT_TYPES.items():
            for pattern in directories:
                # Handle directory-based patterns (e.g., specs/)
                if pattern.endswith('/'):
                    expected_prefix = f"{type_name}-"
                    if filename.startswith(expected_prefix):
                        return type_name

        return "unknown"

    def test_resolution_priority(self):
        """Test type resolution prioritizes metadata over directory over filename."""
        print("\n[TEST] Type Resolution Priority")

        # Test 1: Metadata priority
        test_cases = [
            {
                "name": "Metadata takes priority over directory",
                "path": "milestones/M5/specs/INV-001.md",
                "content": "type: investigation\n---",
                "expected": "investigation",
                "priority": "metadata"
            },
            {
                "name": "Directory used when no metadata",
                "path": "milestones/M5/specs/SPEC-001.md",
                "content": "# Specification",
                "expected": "specification",
                "priority": "directory"
            },
            {
                "name": "Filename used as final fallback",
                "path": "milestones/M5/investigations/INVESTIGATIONS.md",
                "content": "# Investigation",
                "expected": "investigation",
                "priority": "filename"
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']} (priority: {test_case['priority']})")
            self._create_test_file(test_case['path'], test_case['content'])
            resolver = ArtifactTypeResolver()

            try:
                result = resolver.resolve_artifact_type(test_case['path'])
                if result == test_case['expected']:
                    print(f"    ✓ PASS: Got '{result}'")
                else:
                    print(f"    ✗ FAIL: Expected '{test_case['expected']}', got '{result}'")
                    all_passed = False
            except Exception as e:
                print(f"    ✗ FAIL: Unexpected exception: {e}")
                all_passed = False

            self._cleanup_test_file(test_case['path'])

        if all_passed:
            print("  ✓ All resolution priority tests passed")
        else:
            print("  ✗ Some resolution priority tests failed")

        return all_passed

    def test_determinism(self):
        """Test that resolution is deterministic and reproducible."""
        print("\n[TEST] Determinism")

        path = "milestones/M5/specs/SPEC-001.md"
        self._create_test_file(path, "type: specification\n---")

        resolver = ArtifactTypeResolver()
        results = []

        # Run resolution multiple times
        for i in range(5):
            result = resolver.resolve_artifact_type(path)
            results.append(result)

        # All results should be identical
        unique_results = set(results)

        self._cleanup_test_file(path)

        if len(unique_results) == 1 and results[0] == "specification":
            print(f"  ✓ PASS: Resolution is deterministic (all returned '{results[0]}')")
            return True
        else:
            print(f"  ✗ FAIL: Non-deterministic resolution: {results}")
            return False

    def test_resolution_performance(self):
        """Test that resolution completes in < 100ms."""
        print("\n[TEST] Performance (target: < 100ms)")

        path = "milestones/M5/specs/SPEC-001.md"
        self._create_test_file(path, "type: specification\n---")

        resolver = ArtifactTypeResolver()

        # Measure execution time for 1000 resolutions
        num_tests = 1000
        start_time = time.time()

        for _ in range(num_tests):
            resolver.resolve_artifact_type(path)

        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to ms

        self._cleanup_test_file(path)

        avg_time = elapsed / num_tests

        if avg_time < 100:
            print(f"  ✓ PASS: Average resolution time: {avg_time:.2f}ms (< 100ms)")
            return True
        else:
            print(f"  ✗ FAIL: Average resolution time: {avg_time:.2f}ms (>= 100ms)")
            return False

    def test_conflict_detection(self):
        """Test that conflicts are detected and fail closed."""
        print("\n[TEST] Conflict Detection")

        test_cases = [
            {
                "name": "Metadata investigation in specs directory",
                "path": "milestones/M5/specs/INV-001.md",
                "content": "type: investigation\n---",
                "should_fail": True
            },
            {
                "name": "Metadata specification in investigations directory",
                "path": "milestones/M5/investigations/SPEC-001.md",
                "content": "type: specification\n---",
                "should_fail": True
            },
            {
                "name": "Ambiguous metadata, specs directory, investigation filename",
                "path": "milestones/M5/specs/INVESTIGATIONS.md",
                "content": "# No type field\n---",
                "should_fail": True
            },
            {
                "name": "Valid case: metadata and directory match",
                "path": "milestones/M5/specs/SPEC-001.md",
                "content": "type: specification\n---",
                "should_fail": False
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            self._create_test_file(test_case['path'], test_case['content'])
            resolver = ArtifactTypeResolver()

            try:
                result = resolver.resolve_artifact_type(test_case['path'])

                if test_case['should_fail']:
                    print(f"    ✗ FAIL: Should have raised conflict error, got '{result}'")
                    all_passed = False
                else:
                    print(f"    ✓ PASS: No conflict, returned '{result}'")
            except ValueError as e:
                if test_case['should_fail']:
                    print(f"    ✓ PASS: Conflict detected: {str(e)[:50]}...")
                else:
                    print(f"    ✗ FAIL: Unexpected conflict error: {e}")
                    all_passed = False
            except Exception as e:
                print(f"    ✗ FAIL: Unexpected exception: {e}")
                all_passed = False

            self._cleanup_test_file(test_case['path'])

        if all_passed:
            print("  ✓ All conflict detection tests passed")
        else:
            print("  ✗ Some conflict detection tests failed")

        return all_passed

    def test_fail_closed_no_silent_reinterpretation(self):
        """Test that resolution does not silently reinterpret artifacts on conflict."""
        print("\n[TEST] Fail Closed on Conflicts")

        test_cases = [
            {
                "name": "Metadata investigation in specs directory",
                "path": "milestones/M5/specs/INV-001.md",
                "content": "type: investigation\n---",
                "expected_error": "conflict"
            },
            {
                "name": "Metadata specification in investigations directory",
                "path": "milestones/M5/investigations/SPEC-001.md",
                "content": "type: specification\n---",
                "expected_error": "conflict"
            }
        ]

        all_passed = True
        for test_case in test_cases:
            print(f"  - {test_case['name']}")
            self._create_test_file(test_case['path'], test_case['content'])
            resolver = ArtifactTypeResolver()

            try:
                result = resolver.resolve_artifact_type(test_case['path'])

                if result in ["investigation", "specification"]:
                    print(f"    ✗ FAIL: Silent reinterpretation to '{result}'")
                    all_passed = False
                else:
                    print(f"    ✗ FAIL: Silent reinterpretation to '{result}'")
                    all_passed = False
            except ValueError as e:
                if "conflict" in str(e).lower():
                    print(f"    ✓ PASS: Did not reinterpret, raised error")
                else:
                    print(f"    ✗ FAIL: Raised error but not about conflict: {e}")
                    all_passed = False
            except Exception as e:
                print(f"    ✗ FAIL: Unexpected exception: {e}")
                all_passed = False

            self._cleanup_test_file(test_case['path'])

        if all_passed:
            print("  ✓ All fail-closed tests passed")
        else:
            print("  ✗ Some fail-closed tests failed")

        return all_passed

    def test_error_message_clarity(self):
        """Test that conflict error messages are explicit and helpful."""
        print("\n[TEST] Error Message Clarity")

        path = "milestones/M5/specs/INV-001.md"
        self._create_test_file(path, "type: investigation\n---")
        resolver = ArtifactTypeResolver()

        try:
            resolver.resolve_artifact_type(path)
            print(f"  ✗ FAIL: No error raised")
            return False
        except ValueError as e:
            error_msg = str(e)

            # Check for required components
            has_type_in_metadata = "investigation" in error_msg
            has_directory = "specs" in error_msg or "directory" in error_msg
            has_explicit_conflict = "conflict" in error_msg.lower()

            self._cleanup_test_file(path)

            if has_type_in_metadata and has_directory and has_explicit_conflict:
                print(f"  ✓ PASS: Error message includes all required components")
                return True
            else:
                print(f"  ✗ FAIL: Error message missing components: metadata={has_type_in_metadata}, directory={has_directory}, conflict={has_explicit_conflict}")
                print(f"    Message: {error_msg}")
                return False
        except Exception as e:
            self._cleanup_test_file(path)
            print(f"  ✗ FAIL: Unexpected exception: {e}")
            return False

    # Utility methods for testing

    def _create_test_file(self, path: str, content: str):
        """Create a test file in the milestones directory."""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        path_obj.write_text(content, encoding='utf-8')

    def _cleanup_test_file(self, path: str):
        """Remove a test file."""
        try:
            path_obj = Path(path)
            if path_obj.exists():
                path_obj.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    resolver = ArtifactTypeResolver()
    all_passed = True

    all_passed = resolver.test_resolution_priority() and all_passed
    all_passed = resolver.test_determinism() and all_passed
    all_passed = resolver.test_resolution_performance() and all_passed
    all_passed = resolver.test_conflict_detection() and all_passed
    all_passed = resolver.test_fail_closed_no_silent_reinterpretation() and all_passed
    all_passed = resolver.test_error_message_clarity() and all_passed

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✓ All type resolution tests passed")
        exit(0)
    else:
        print("✗ Some type resolution tests failed")
        exit(1)
