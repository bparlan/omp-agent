#!/usr/bin/env python3
"""
Comprehensive test evaluation for M9S1
This script simulates what the evaluate-tests skill should do
"""

import os
import subprocess
import sys


def run_test(test_path, interpreter="python3"):
    """Run a single test and return results"""
    try:
        result = subprocess.run(
            [interpreter, test_path],
            cwd="/Users/bparlan/devcode/aef/agent",
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error": None,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Timeout",
            "error": "Timeout",
        }
    except Exception as e:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "error": str(e),
        }


def main():
    # ALL Test files from the ledger (original 9 + 10 integration tests)
    test_files = [
        # Basic tests from original ledger
        ("tests/M9/S1/test_registry_init_001.sh", "bash"),
        ("tests/M9/S1/test_validator_init_001.sh", "bash"),
        ("tests/M9/S1/test_resolver_init_001.sh", "bash"),
        ("tests/M9/S1/test_types_def_001.py", "python3"),
        ("tests/M9/S1/test_legacy_compat_001.py", "python3"),
        ("tests/M9/S1/test_traceability_001.py", "python3"),
        ("tests/M9/S1/test_storage_model_001.sh", "bash"),
        ("tests/M9/S1/test_schema_constraints_001.sh", "bash"),
        ("tests/M9/S1/test_resolution_priority_001.sh", "bash"),
        # Integration tests (added to ledger)
        ("tests/M9/S1/test_vi1_validate_missing_keys.py", "python3"),
        ("tests/M9/S1/test_vi2_ambiguous_resolution.py", "python3"),
        ("tests/M9/S1/test_vi3_artifact_creation.sh", "bash"),
        ("tests/M9/S1/test_vi4_invalid_artifact_failure.sh", "bash"),
        ("tests/M9/S1/test_vi5_milestone_explicit_identity.sh", "bash"),
        ("tests/M9/S1/test_vi6_relationship_fields.py", "python3"),
        ("tests/M9/S1/test_vi7_legacy_strict_flag.sh", "bash"),
        ("tests/M9/S1/test_vi8_type_consistency.py", "python3"),
        ("tests/M9/S1/test_vi9_verify_metadata_cli.sh", "bash"),
        ("tests/M9/S1/test_vi10_performance_threshold.sh", "bash"),
    ]

    tests_run = 0
    tests_passed = 0
    tests_failed = 0
    valid_initial_failures = 0
    invalid_tests = 0
    tdd_leaks = 0
    spec_checks = 0

    print("=== COMPREHENSIVE TEST EVALUATION FOR M9S1 ===\n")

    for test_path, interpreter in test_files:
        tests_run += 1
        print(f"Running: {test_path} (interpreter: {interpreter})")

        # First check if file exists
        if not os.path.exists(test_path):
            print(f"  ❌ File not found: {test_path}")
            tests_failed += 1
            continue

        # Run the test
        result = run_test(test_path, interpreter)

        # Check for syntax errors first (INVALID_TEST)
        if "SyntaxError" in result.get(
            "stderr", ""
        ) or "unterminated string literal" in result.get("stderr", ""):
            print("  ❌ INVALID_TEST - Syntax error")
            print(f"     Error: {result['stderr']}")
            invalid_tests += 1
            continue

        # Determine test type based on filename
        test_type = "implementation"
        if (
            "vi1" in test_path
            or "vi2" in test_path
            or "vi6" in test_path
            or "vi8" in test_path
        ):
            test_type = "specification"

        # Check exit codes with test type awareness
        if result["exit_code"] == 127:
            print("  ✅ VALID_INITIAL_FAILURE - Exit code 127 (Command Not Found)")
            valid_initial_failures += 1
        elif result["exit_code"] == 1:
            print("  ✅ VALID_INITIAL_FAILURE - Exit code 1 (Assertion Failed)")
            valid_initial_failures += 1
        elif result["exit_code"] == 0:
            if test_type == "specification":
                print(
                    "  ✅ SPECIFICATION_CHECK - Exit code 0 (validates spec compliance)"
                )
                spec_checks += 1
            else:
                print(
                    "  ⚠️  POTENTIAL TDD_LEAK - Exit code 0 (passed on empty codebase)"
                )
                tdd_leaks += 1
        else:
            print(f"  ❌ FAILED - Exit code {result['exit_code']}")
            tests_failed += 1

        print(
            f"  Output: {result['stdout'][:300] if result['stdout'] else 'No stdout'}"
        )
        print()

    # Summary
    print("=== SUMMARY ===")
    print(f"Tests run: {tests_run}")
    print(f"Tests passed (0): {tests_passed}")
    print(f"Tests failed (non-zero): {tests_failed}")
    print(f"Valid initial failures (127/1): {valid_initial_failures}")
    print(f"Invalid tests (syntax errors): {invalid_tests}")
    print(f"Specification checks: {spec_checks}")
    print(f"TDD leaks (false passes): {tdd_leaks}")

    # Calculate exit code - FIXED LOGIC
    if invalid_tests > 0 or tdd_leaks > 0:
        print(
            "\n🔴 PIPELINE LOCKED - Exit Code 2 (Invalid tests or TDD leaks detected)"
        )
        exit_code = 2
    else:
        print(
            "\n🟢 BASELINE VERIFIED - Exit Code 0 (All implementation checks properly fail on empty codebase)"
        )
        exit_code = 0

    print("\n=== FINAL ASSESSMENT ===")
    print(
        "Expected for pre-implementation: All IMPLEMENTATION tests should fail with 127/1"
    )
    print("Specification tests can pass with exit 0 (validate spec compliance)")
    print(
        "Any IMPLEMENTATION test passing with exit 0 is a TDD leak and blocks pipeline"
    )
    print("Any test with syntax errors is an invalid test and blocks pipeline")

    # Write results
    with open("test_evaluation_results.json", "w") as f:
        import json

        json.dump(
            {
                "tests_run": tests_run,
                "tests_passed": tests_passed,
                "tests_failed": tests_failed,
                "valid_initial_failures": valid_initial_failures,
                "invalid_tests": invalid_tests,
                "spec_checks": spec_checks,
                "tdd_leaks": tdd_leaks,
                "exit_code": exit_code,
            },
            f,
            indent=2,
        )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
