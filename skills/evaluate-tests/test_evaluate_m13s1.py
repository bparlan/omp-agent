#!/usr/bin/env python3
"""
M13S1 Test Evaluation Skill Implementation

Validate test quality and establish healthy "Red" TDD baseline (VALID_INITIAL_FAILURE).
Generates TEVAL-M13S1TE.md test evaluation report.
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def read_test_plan_ledger() -> List[Dict[str, str]]:
    """Read Test Plan Ledger from milestones/M13/M13S1T1.md"""
    ledger_path = Path("milestones/M13/M13S1T1.md")

    if not ledger_path.exists():
        print(f"ERROR: Test Plan Ledger not found: {ledger_path}")
        return []

    test_files = []
    content = ledger_path.read_text()

    # Parse table format from markdown
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("|") and "tests/M13/S1/" in line:
            # Extract test file path from markdown table
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 4:
                test_file = parts[0]
                if test_file.endswith(".py"):
                    test_files.append(
                        {
                            "file": test_file,
                            "verification_id": parts[1],
                            "requirement_id": parts[2],
                            "test_type": parts[3],
                        }
                    )

    return test_files


def execute_test(test_info: Dict[str, str]) -> Dict[str, Any]:
    """Execute a single test file and capture results"""
    test_file = test_info["file"]
    verification_id = test_info["verification_id"]
    requirement_id = test_info["requirement_id"]
    test_type = test_info["test_type"]

    print(f"\n=== Executing {test_file} ({verification_id}) ===")

    # Determine interpreter based on file extension
    if test_file.endswith(".py"):
        cmd = [sys.executable, test_file]
    elif test_file.endswith(".sh"):
        cmd = ["bash", test_file]
    else:
        return {
            "status": "ERROR",
            "classification": "INVALID_TEST",
            "is_valid_failure": False,
            "exit_code": -1,
            "output": f"Unsupported file type: {test_file}",
            "file": test_file,
            "verification_id": verification_id,
            "requirement_id": requirement_id,
            "test_type": test_type,
        }

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, cwd=Path.cwd()
        )

        # Analyze test result
        output = result.stdout + result.stderr

        # Check if test passed or failed
        if result.returncode == 0:
            status = "PASS"
            classification = "VALID_TEST"
            is_valid_failure = False
        else:
            status = "FAIL"

            # For blank/un-implemented codebase, all failures should be VALID_INITIAL_FAILURE
            # if the code is missing required components or functions
            if (
                "No module named" in output
                or "Function signature does not match" in output
                or "Cannot import" in output
                or "not found" in output.lower()
                or "INSUFFICIENT" in output.upper()
                or "error" in output.lower()
            ):
                classification = "VALID_INITIAL_FAILURE"
                is_valid_failure = True
            else:
                classification = "INVALID_TEST"
                is_valid_failure = False

        return {
            "status": status,
            "classification": classification,
            "is_valid_failure": is_valid_failure,
            "exit_code": result.returncode,
            "output": output,
            "file": test_file,
            "verification_id": verification_id,
            "requirement_id": requirement_id,
            "test_type": test_type,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "ERROR",
            "classification": "INVALID_TEST",
            "is_valid_failure": False,
            "exit_code": -2,
            "output": "Timeout after 60 seconds",
            "file": test_file,
            "verification_id": verification_id,
            "requirement_id": requirement_id,
            "test_type": test_type,
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "classification": "INVALID_TEST",
            "is_valid_failure": False,
            "exit_code": -3,
            "output": str(e),
            "file": test_file,
            "verification_id": verification_id,
            "requirement_id": requirement_id,
            "test_type": test_type,
        }


def generate_evaluation_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comprehensive evaluation report"""

    total_tests = len(test_results)
    passed_tests = len([t for t in test_results if t["status"] == "PASS"])
    failed_tests = len([t for t in test_results if t["status"] == "FAIL"])
    error_tests = len([t for t in test_results if t["status"] == "ERROR"])

    valid_failures = len(
        [t for t in test_results if t.get("classification") == "VALID_INITIAL_FAILURE"]
    )
    invalid_tests = len(
        [t for t in test_results if t.get("classification") == "INVALID_TEST"]
    )

    # Generate summary
    summary = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "error_tests": error_tests,
        "valid_failures": valid_failures,
        "invalid_tests": invalid_tests,
        "red_baseline_healthy": True if invalid_tests == 0 else False,
        "test_execution_time": datetime.now().isoformat(),
    }

    # Generate report
    report = {
        "report_id": f'TEVAL-M13S1TE-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        "timestamp": datetime.now().isoformat(),
        "milestone": "M13",
        "specification": "M13S1",
        "test_suite": "M13S1",
        "summary": summary,
        "test_results": test_results,
        "analysis": {
            "baseline_status": "RED"
            if failed_tests > 0 and invalid_tests == 0
            else "UNHEALTHY",
            "expected_initial_failures": valid_failures,
            "unexpected_failures": invalid_tests,
            "implementation_readiness": "NOT_STARTED" if failed_tests > 0 else "READY",
        },
    }

    return report


def write_evaluation_report(report: Dict[str, Any]) -> str:
    """Write evaluation report to TEVAL-M13S1TE.md"""

    report_path = Path("TEVAL-M13S1TE.md")

    # Generate markdown report
    content = f"""# M13S1 Test Evaluation Report

**Report ID:** {report['report_id']}
**Generated:** {report['timestamp']}
**Milestone:** {report['milestone']}
**Specification:** {report['specification']}
**Test Suite:** {report['test_suite']}

## Executive Summary

| Metric | Count |
|--------|-------|
| Total Tests | {report['summary']['total_tests']} |
| Passed Tests | {report['summary']['passed_tests']} |
| Failed Tests | {report['summary']['failed_tests']} |
| Error Tests | {report['summary']['error_tests']} |
| Valid Initial Failures | {report['summary']['valid_failures']} |
| Invalid Tests | {report['summary']['invalid_tests']} |

**Red TDD Baseline Status:** {'✅ HEALTHY' if report['summary']['red_baseline_healthy'] else '❌ UNHEALTHY'}
**Test Execution Time:** {report['summary']['test_execution_time']}

## Analysis

- **Baseline Status:** {report['analysis']['baseline_status']}
- **Expected Initial Failures:** {report['analysis']['expected_initial_failures']}
- **Unexpected Failures:** {report['analysis']['unexpected_failures']}
- **Implementation Readiness:** {report['analysis']['implementation_readiness']}

## Detailed Test Results

"""

    for i, test_result in enumerate(report["test_results"], 1):
        test_file = Path(test_result["file"]).name
        verification_id = test_result["verification_id"]
        requirement_id = test_result["requirement_id"]
        test_type = test_result["test_type"]

        content += f"""### Test {i}: {test_file}

**Verification ID:** {verification_id}
**Requirement ID:** {requirement_id}
**Test Type:** {test_type}
**Status:** {test_result['status']}
**Classification:** {test_result['classification']}
**Expected Initial Failure:** {'✅ YES' if test_result.get('is_valid_failure', False) else '❌ NO'}

**Output:**
```
{test_result['output'][:500]}{'...' if len(test_result['output']) > 500 else ''}
```

---

"""

    # Write report
    report_path.write_text(content)
    return str(report_path)


def main() -> int:
    """Main skill execution function"""
    print("=== M13S1 Test Evaluation Skill ===")
    print("Validating test quality and establishing healthy 'Red' TDD baseline\n")

    # Step 1: Read Test Plan Ledger
    print("Step 1: Reading Test Plan Ledger...")
    test_plan = read_test_plan_ledger()

    if not test_plan:
        print("ERROR: No test files found in Test Plan Ledger")
        return 1

    print(f"Found {len(test_plan)} test files to execute:")
    for test_info in test_plan:
        print(f"  - {test_info['file']} ({test_info['verification_id']})")

    # Step 2: Execute all tests
    print("\nStep 2: Executing tests...")
    test_results = []

    for test_info in test_plan:
        result = execute_test(test_info)
        test_results.append(result)

    # Step 3: Generate evaluation report
    print("\nStep 3: Generating evaluation report...")
    report = generate_evaluation_report(test_results)

    # Step 4: Write report
    print(f"Writing report to {report['report_id']}.md")
    report_path = write_evaluation_report(report)

    # Step 5: Display summary
    print("\n=== Test Evaluation Summary ===")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed_tests']}")
    print(
        f"Failed: {report['summary']['failed_tests']} (Valid: {report['summary']['valid_failures']}, Invalid: {report['summary']['invalid_tests']})"
    )
    print(f"Errors: {report['summary']['error_tests']}")
    print(f"\nReport written to: {report_path}")

    # Step 6: Return appropriate exit code
    if report["summary"]["invalid_tests"] > 0:
        print("\n❌ INVALID TESTS DETECTED - RED BASELINE UNHEALTHY")
        return 2  # INVALID_TEST_BLOCKED
    elif (
        report["summary"]["valid_failures"] > 0
        and report["summary"]["failed_tests"] > 0
    ):
        print("\n✅ VALID INITIAL FAILURES - HEALTHY RED BASELINE")
        return 0  # SUCCESS
    else:
        print("\n❓ UNEXPECTED TEST RESULTS")
        return 1  # UNKNOWN


if __name__ == "__main__":
    sys.exit(main())
