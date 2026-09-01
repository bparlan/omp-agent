#!/usr/bin/env python3
"""Test runner for evaluate-tests baseline verification"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

# Tests to run from ledger
tests = [
    ("PYTHON_TEST", "tests/M9/S3/test_fr1_artifact_creation.py"),
    ("PYTHON_TEST", "tests/M9/S3/test_fr2_ledger_integration.py"),
    ("SCRIPT_EXECUTION", "tests/M9/S3/test_fr3_batch_processing.sh"),
    ("SCRIPT_EXECUTION", "tests/M9/S3/test_fr4_single_skill.sh"),
    ("PYTHON_TEST", "tests/M9/S3/test_fr5_validation_integration.py"),
    ("PYTHON_TEST", "tests/M9/S3/test_fr6_storage_compliance.py"),
    ("PYTHON_TEST", "tests/M9/S3/test_fr7_history_tracking.py"),
    ("PYTHON_TEST", "tests/M9/S3/test_fr8_insights_generation.py"),
]

results = {
    "TESTS_RUN": 0,
    "TESTS_PASSED": 0,
    "TESTS_FAILED": 0,
    "VALID_INITIAL_FAILURES": 0,
    "INVALID_TESTS": 0,
    "TDD_LEAKS": 0,
}

print("Running M9S3 test baseline evaluation...\n")

for test_type, test_path in tests:
    test_full_path = REPO_ROOT / test_path
    print(f"Running: {test_path} ({test_type})")

    try:
        if test_type == "PYTHON_TEST":
            result = subprocess.run(
                ["python3", str(test_full_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        else:  # SCRIPT_EXECUTION
            result = subprocess.run(
                ["bash", str(test_full_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

        exit_code = result.returncode
        print(f"  Exit code: {exit_code}")

        if result.stdout:
            print(f"  stdout: {result.stdout[:200]}")
        if result.stderr:
            print(f"  stderr: {result.stderr[:200]}")

        results["TESTS_RUN"] += 1

        if exit_code == 0:
            if test_type in ["SCRIPT_EXECUTION", "UNIT_TEST", "INTEGRATION_TEST"]:
                results["TDD_LEAKS"] += 1
                print(
                    "  ❌ TDD LEAK: Implementation check passed when it should have failed"
                )
            else:
                results["TESTS_PASSED"] += 1
                print("  ✓ PASS")
        elif exit_code == 127 or exit_code == 1:
            results["VALID_INITIAL_FAILURES"] += 1
            print("  ✓ VALID_INITIAL_FAILURE")
        elif exit_code == 2:
            results["INVALID_TESTS"] += 1
            print("  ❌ INVALID_TEST")
        else:
            results["TESTS_FAILED"] += 1
            print(f"  ❌ FAILED (exit code {exit_code})")

    except subprocess.TimeoutExpired:
        results["INVALID_TESTS"] += 1
        results["TESTS_RUN"] += 1
        print("  ❌ INVALID_TEST: Timeout")
    except Exception as e:
        results["INVALID_TESTS"] += 1
        results["TESTS_RUN"] += 1
        print(f"  ❌ INVALID_TEST: {e}")

    print()

print("=" * 60)
print("EVALUATION RESULTS:")
print(f"  Tests Run: {results['TESTS_RUN']}")
print(f"  Tests Passed: {results['TESTS_PASSED']}")
print(f"  Tests Failed: {results['TESTS_FAILED']}")
print(f"  Valid Initial Failures: {results['VALID_INITIAL_FAILURES']}")
print(f"  Invalid Tests: {results['INVALID_TESTS']}")
print(f"  TDD Leaks: {results['TDD_LEAKS']}")

exit_code = 0
if results["INVALID_TESTS"] > 0 or results["TDD_LEAKS"] > 0:
    exit_code = 2
    print("\n❌ BASELINE VERIFICATION FAILED")
else:
    print("\n✅ BASELINE VERIFICATION PASSED")

sys.exit(exit_code)
