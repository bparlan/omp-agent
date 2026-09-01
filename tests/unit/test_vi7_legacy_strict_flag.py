#!/usr/bin/env python3
# {Verification IDs: V-VI-7}
# {Requirement IDs: FR-LEGACY_COMPATIBILITY}
# Test Type: IMPLEMENTATION_CHECK

"""
VI-7: Legacy Compatibility with Strict Flag
Verification ID: VI-7
Source Requirement ID: FR-LEGACY_COMPATIBILITY
Verification Method: UNIT_TEST
Target: core/artifacts/resolution.py:resolve_artifact(identity?, type?, metadata_filter?, strict?)
"""

import os
import sys
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CORE_PATH = os.path.join(REPO_ROOT, "core")

if CORE_PATH not in sys.path:
    sys.path.insert(0, CORE_PATH)

try:
    from core.artifacts.resolution import resolve_artifact, ARTIFACTS_BASE_DIR
except Exception as exc:
    print(f"VALID_INITIAL_FAILURE: cannot import resolve_artifact: {exc}")
    sys.exit(127)


def test_legacy_strict_flag() -> int:
    """Test that the strict flag controls legacy artifact resolution."""
    original_base = ARTIFACTS_BASE_DIR
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # Monkeypatch the base dir to a temp milestones structure
            import core.artifacts.resolution as resolution_mod

            resolution_mod.ARTIFACTS_BASE_DIR = os.path.join(tmpdir, "milestones")
            os.makedirs(resolution_mod.ARTIFACTS_BASE_DIR)

            # Create a canonical artifact (has identity)
            canonical_dir = os.path.join(resolution_mod.ARTIFACTS_BASE_DIR, "M9")
            os.makedirs(canonical_dir)
            canonical_path = os.path.join(canonical_dir, "canonical_m9.md")

            with open(canonical_path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write("id: canonical_m9\n")
                f.write("type: test\n")
                f.write("---\n")
                f.write("This is a canonical artifact with identity.\n")

            # Create a legacy artifact (no identity)
            legacy_dir = os.path.join(resolution_mod.ARTIFACTS_BASE_DIR, "M9", "legacy")
            os.makedirs(legacy_dir)
            legacy_path = os.path.join(legacy_dir, "legacy_m9.md")

            with open(legacy_path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write("type: test\n")
                f.write("---\n")
                f.write("This is a legacy artifact without identity.\n")

            # Test 1: strict=True should resolve canonical artifact but skip legacy
            print("Testing strict=True with canonical artifact...")
            canonical_strict_result = resolve_artifact(
                identity="canonical_m9", strict=True
            )

            if (
                not isinstance(canonical_strict_result, dict)
                or canonical_strict_result.get("resolved") is not True
            ):
                print(
                    f"FAIL: strict=True should resolve canonical artifact, but got: {canonical_strict_result}"
                )
                return 1

            print("Testing strict=True with legacy artifact (should not resolve)...")
            legacy_strict_result = resolve_artifact(identity="legacy_m9", strict=True)

            if (
                isinstance(legacy_strict_result, dict)
                and legacy_strict_result.get("resolved") is not False
            ):
                print(
                    f"FAIL: strict=True should NOT resolve legacy artifact, but got: {legacy_strict_result}"
                )
                return 1

            # Test 2: strict=False should resolve both canonical and legacy
            print("Testing strict=False with canonical artifact...")
            canonical_lenient_result = resolve_artifact(
                identity="canonical_m9", strict=False
            )

            if (
                not isinstance(canonical_lenient_result, dict)
                or canonical_lenient_result.get("resolved") is not True
            ):
                print(
                    f"FAIL: strict=False should resolve canonical artifact, but got: {canonical_lenient_result}"
                )
                return 1

            print(
                "Testing strict=False with legacy artifact (should resolve by path)..."
            )
            # With strict=False, legacy should be resolved by path (filename)
            legacy_lenient_result = resolve_artifact(identity="legacy_m9", strict=False)

            if (
                not isinstance(legacy_lenient_result, dict)
                or legacy_lenient_result.get("resolved") is not True
            ):
                print(
                    f"FAIL: strict=False should resolve legacy artifact, but got: {legacy_lenient_result}"
                )
                return 1

        finally:
            resolution_mod.ARTIFACTS_BASE_DIR = original_base

    print("PASS: legacy compatibility with strict flag works as expected")
    return 0


if __name__ == "__main__":
    sys.exit(test_legacy_strict_flag())
