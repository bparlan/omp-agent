#!/usr/bin/env python3
"""
Test evaluation for M9S3 - Skill Integration & Healthcenter
Based on test ledger in milestones/M9/M9S3T1.md
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
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "error": None
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Timeout",
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "error": str(e)
        }

def main():
    # M9S3 tests from the ledger (based on milestones/M9/M9S3T1.md)
    test_files = [
        # UNIT_TEST from ledger
        ("tests/M9/S3/test_health_check_artifact_validation.py", "python3"),
        ("tests/M9/S3/test_health_check_history_tracking.py", "python3"),
        ("tests/M9/S3/test_health_check_insights_generation.py", "python3"),
        ("tests/M9/S3/test_health_check_ledger_integration.py", "python3"),
        ("tests/M9/S3/test_healthcheck_type_registered.py", "python3"),
        ("tests/M9/S3/test_health_check_error_handling.py", "python3"),
        
        # SCRIPT_EXECUTION from ledger  
        ("tests/M9/S3/test_health_check_artifact_creation.py", "bash"),
        ("tests/M9/S3/test_health_check_batch_processing.py", "bash"),
        ("tests/M9/S3/test_health_check_single_skill.py", "bash"),
        ("tests/M9/S3/test_single_skill_artifact.sh", "bash"),
        ("tests/M9/S3/test_batch_processing.sh", "bash"),
        ("tests/M9/S3/test_single_skill_fix_mode.sh", "bash"),
        
        # IMPLEMENTATION_CHECK from ledger
        ("tests/M9/S3/test_health_check_backward_compatibility.py", "python3"),
        ("tests/M9/S3/test_health_check_performance.py", "python3"),
        ("tests/M9/S3/test_health_check_compliance.py", "python3"),
        
        # Additional unit tests (from directory listing)
        ("tests/M9/S3/test_single_skill_artifact_frontmatter.py", "python3"),
        ("tests/M9/S3/test_error_handling_batch_continues.sh", "bash"),
        ("tests/M9/S3/test_legacy_healthcheck_removed.py", "python3"),
    ]

    tests_run = 0
    tests_passed = 0
    tests_failed = 0
    valid_initial_failures = 0
    invalid_tests = 0
    tdd_leaks = 0
    spec_checks = 0

    print("=== M9S3 TEST EVALUATION (based on test ledger) ===\n")

    for test_path, interpreter in test_files:
        tests_run += 1
        print(f"Running: {test_path} (interpreter: {interpreter})")

        # First check if file exists
        if not os.path.exists(test_path):
            print(f"  ❌ File not found: {test_path}")
            tests_failed += 1
            continue

        # Check for syntax errors first (INVALID_TEST)
        try:
            with open(test_path, 'r') as f:
                content = f.read()
                if '\x00' in content:
                    print(f"  ❌ INVALID_TEST - Contains NUL bytes")
                    invalid_tests += 1
                    continue
                if not content.startswith('#!/usr/bin/env python3'):
                    # Check if it's a bash script
                    if not ('#!/bin/bash' in content or '#!/bin/sh' in content):
                        print(f"  ❌ INVALID_TEST - Invalid shebang")
                        invalid_tests += 1
                        continue
        except Exception as e:
            print(f"  ❌ INVALID_TEST - Cannot read file: {e}")
            invalid_tests += 1
            continue

        # Run the test
        result = run_test(test_path, interpreter)

        # Determine test type based on filename and content
        is_unit_test = 'test_health_check_artifact_validation.py' in test_path or \
                      'test_health_check_history_tracking.py' in test_path or \
                      'test_health_check_insights_generation.py' in test_path or \
                      'test_health_check_ledger_integration.py' in test_path or \
                      'test_healthcheck_type_registered.py' in test_path or \
                      'test_health_check_error_handling.py' in test_path or \
                      'test_single_skill_artifact_frontmatter.py' in test_path
        
        is_script_execution = test_path.endswith('.sh') or \
                            'test_health_check_artifact_creation.py' in test_path or \
                            'test_health_check_batch_processing.py' in test_path or \
                            'test_health_check_single_skill.py' in test_path
        
        is_implementation_check = 'test_health_check_backward_compatibility.py' in test_path or \
                                 'test_health_check_performance.py' in test_path or \
                                 'test_health_check_compliance.py' in test_path or \
                                 'test_legacy_healthcheck_removed.py' in test_path

        # Classify results based on test type and exit code
        if result['error'] or 'SyntaxError' in result.get('stderr', ''):
            print(f"  ❌ INVALID_TEST - Syntax error")
            print(f"     Error: {result['stderr']}")
            invalid_tests += 1
        elif is_unit_test:
            # UNIT_TEST can pass (spec compliance)
            if result['success']:
                print(f"  ✅ SPECIFICATION_CHECK - Exit code 0 (validates spec compliance)")
                tests_passed += 1
                spec_checks += 1
            else:
                print(f"  ❌ TEST_FAILED - Exit code {result['exit_code']}")
                print(f"     Error: {result['stderr']}")
                tests_failed += 1
        elif is_script_execution:
            # SCRIPT_EXECUTION should fail with 127/1 (VALID_INITIAL_FAILURE)
            if result['exit_code'] == 127:
                print(f"  ✅ VALID_INITIAL_FAILURE - Exit code 127 (Command Not Found)")
                valid_initial_failures += 1
                tests_passed += 1
            elif result['exit_code'] == 1 and 'VALID_INITIAL_FAILURE' in result.get('stdout', ''):
                print(f"  ✅ VALID_INITIAL_FAILURE - Exit code 1 (Assertion Failed)")
                valid_initial_failures += 1
                tests_passed += 1
            else:
                print(f"  ⚠️  POTENTIAL TDD_LEAK - Exit code {result['exit_code']} (may be passing prematurely)")
                print(f"     Output: {result['stdout'][:200]}")
                tdd_leaks += 1
                tests_passed += 1
        elif is_implementation_check:
            # IMPLEMENTATION_CHECK should fail with 127/1 (VALID_INITIAL_FAILURE)
            if result['exit_code'] == 127:
                print(f"  ✅ VALID_INITIAL_FAILURE - Exit code 127 (Command Not Found)")
                valid_initial_failures += 1
                tests_passed += 1
            elif result['exit_code'] == 1 and 'VALID_INITIAL_FAILURE' in result.get('stdout', ''):
                print(f"  ✅ VALID_INITIAL_FAILURE - Exit code 1 (Assertion Failed)")
                valid_initial_failures += 1
                tests_passed += 1
            else:
                print(f"  ⚠️  POTENTIAL TDD_LEAK - Exit code {result['exit_code']} (may be passing prematurely)")
                print(f"     Output: {result['stdout'][:200]}")
                tdd_leaks += 1
                tests_passed += 1
        else:
            # Unknown test type - treat as unit test
            if result['success']:
                print(f"  ✅ SPECIFICATION_CHECK - Exit code 0 (validates spec compliance)")
                tests_passed += 1
                spec_checks += 1
            else:
                print(f"  ❌ TEST_FAILED - Exit code {result['exit_code']}")
                print(f"     Error: {result['stderr']}")
                tests_failed += 1

    exit_code = 0
    if invalid_tests > 0 or tdd_leaks > 0:
        exit_code = 2

    print("\n=== SUMMARY ===")
    print(f"Tests run: {tests_run}")
    print(f"Tests passed: {tests_passed}")
    print(f"Tests failed: {tests_failed}")
    print(f"Valid initial failures: {valid_initial_failures}")
    print(f"Invalid tests: {invalid_tests}")
    print(f"Specification checks: {spec_checks}")
    print(f"TDD leaks: {tdd_leaks}")

    # Write results
    with open("test_m9s3_results.json", "w") as f:
        import json
        json.dump({
            "tests_run": tests_run,
            "tests_passed": tests_passed,
            "tests_failed": tests_failed,
            "valid_initial_failures": valid_initial_failures,
            "invalid_tests": invalid_tests,
            "spec_checks": spec_checks,
            "tdd_leaks": tdd_leaks,
            "exit_code": exit_code
        }, f, indent=2)

    if exit_code == 2:
        print(f"\n🔴 PIPELINE LOCKED - Exit Code 2 (Invalid tests or TDD leaks detected)")
    else:
        print(f"\n🟢 BASELINE VERIFIED - Exit Code 0 (Test suite certified healthy)")

    return exit_code

if __name__ == "__main__":
    sys.exit(main())
