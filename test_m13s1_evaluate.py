#!/usr/bin/env python3
"""
M13S1 Test Evaluation Script

Evaluates the M13S1 test suite according to the Test Plan Ledger (M13S1T1.md).
This script implements the evaluate-tests skill functionality for M13S1.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
def read_test_plan_ledger(milestone_id: str, spec_id: str) -> List[Dict[str, Any]]:
    """
    Read the Test Plan Ledger (M{num}S{n}T{n}.md) to get the list of test files to execute.

    Args:
        milestone_id: Milestone identifier (e.g., "M13")
        spec_id: Specification ID (e.g., "M13S1")

    Returns:
        List of test file information dictionaries with keys:
        - "test_file": Path to the test file
        - "verification_id": Verification ID from the ledger
        - "requirement_id": Requirement ID from the ledger
        - "test_type": Test type from the ledger
    """
    test_set_file = Path(f"milestones/{milestone_id}/{spec_id}T1.md")

    if not test_set_file.exists():
        print(f"ERROR: Test Plan Ledger not found: {test_set_file}")
        return []

    print(f"Reading Test Plan Ledger: {test_set_file}")

    # Parse the test plan ledger (M13S1T1.md)
    test_files = []

    with open(test_set_file, 'r') as f:
        content = f.read()

    # Look for the table in the content
    lines = content.split('\n')
    in_table = False
    table_lines = []

    for line in lines:
        if '| Test File | Verification ID | Requirement ID | Test Type |' in line:
            in_table = True
            continue
        if in_table and line.strip().startswith('|'):
            table_lines.append(line)
        elif in_table and line.strip().startswith('---'):
            continue
        elif in_table and not line.strip().startswith('|'):
            break

    # Parse table rows
    for line in table_lines:
        # Remove pipe characters and split
        columns = [col.strip() for col in line.split('|') if col.strip()]

        if len(columns) >= 4:
            test_file_path = columns[0].strip()
            verification_id = columns[1].strip()
            requirement_id = columns[2].strip()
            test_type = columns[3].strip()

            # Resolve the test file path
            resolved_test_file = Path(test_file_path)
            if not resolved_test_file.exists():
                print(f"WARNING: Test file not found: {test_file_path}")
                continue

            test_files.append({
                "test_file": str(resolved_test_file),
                "verification_id": verification_id,
                "requirement_id": requirement_id,
                "test_type": test_type
            })

    print(f"Found {len(test_files)} test files in Test Plan Ledger:")
    for test_file in test_files:
        print(f"  - {test_file['test_file']} ({test_file['test_type']})")

    return test_files
def execute_test_file(test_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a single test file and return results.

    Args:
        test_info: Test file information dictionary

    Returns:
        Dict containing test execution results with keys:
        - "test_file": Path to the test file
        - "status": "PASSED", "FAILED", or "ERROR"
        - "exit_code": Exit code from test execution
        - "output": Output from test execution
        - "error": Error message if applicable
        - "test_type": Test type
        - "verification_id": Verification ID
        - "requirement_id": Requirement ID
    """
    test_file_path = Path(test_info["test_file"])
    test_type = test_info["test_type"]
    verification_id = test_info.get("verification_id", "")
    requirement_id = test_info.get("requirement_id", "")

    print(f"\nExecuting test: {test_file_path.name}")
    print(f"  Type: {test_type}")
    print(f"  Verification ID: {verification_id}")
    print(f"  Requirement ID: {requirement_id}")

    try:
        # Execute test based on file type and test type
        if test_file_path.suffix == '.py':
            # Python test files
            if test_type == "IMPLEMENTATION_CHECK":
                # Implementation checks should fail (VALID_INITIAL_FAILURE)
                print("  Running as IMPLEMENTATION_CHECK (should fail)...")
                result = os.system(f"python3 {test_file_path} 2>&1")
                exit_code = os.waitstatus_to_returncode(result)
            else:
                # Other tests should also fail initially
                print("  Running Python test (should fail initially)...")
                result = os.system(f"python3 {test_file_path} 2>&1")
                exit_code = os.waitstatus_to_returncode(result)

        elif test_file_path.suffix == '.sh':
            # Shell test files
            print("  Running shell test...")
            result = os.system(f"bash {test_file_path} 2>&1")
            exit_code = os.waitstatus_to_returncode(result)

        else:
            return {
                "test_file": str(test_file_path),
                "status": "ERROR",
                "exit_code": 1,
                "output": f"Unsupported file type: {test_file_path.suffix}",
                "error": f"Unsupported file type: {test_file_path.suffix}",
                "test_type": test_type,
                "verification_id": verification_id,
                "requirement_id": requirement_id
            }

        # Determine test status based on exit code
        if exit_code == 0:
            status = "PASSED"
        elif exit_code == 1:
            # Exit code 1 could be expected failure (VALID_INITIAL_FAILURE) or actual error
            # For M13S1 tests, we expect failures initially
            if test_type in ["IMPLEMENTATION_CHECK", "INTEGRITY_CHECK", "UNIT_TEST"]:
                status = "FAILED"
            else:
                status = "ERROR"
        else:
            status = "ERROR"

        # Get test output (simplified - in practice we'd capture actual output)
        output = f"Test execution completed with exit code: {exit_code}"

        return {
            "test_file": str(test_file_path),
            "status": status,
            "exit_code": exit_code,
            "output": output,
            "error": None if status != "ERROR" else f"Test failed with exit code: {exit_code}",
            "test_type": test_type,
            "verification_id": verification_id,
            "requirement_id": requirement_id
        }

    except Exception as e:
        return {
            "test_file": str(test_file_path),
            "status": "ERROR",
            "exit_code": 1,
            "output": "",
            "error": str(e),
            "test_type": test_type,
            "verification_id": verification_id,
            "requirement_id": requirement_id
        }
def evaluate_test_suite(milestone_id: str, spec_id: str) -> Dict[str, Any]:
    """
    Evaluate the complete test suite for a specification.

    Args:
        milestone_id: Milestone identifier (e.g., "M13")
        spec_id: Specification ID (e.g., "M13S1")

    Returns:
        Dict containing evaluation results with keys:
        - "spec_id": Specification ID
        - "milestone_id": Milestone ID
        - "generated_at": Timestamp when evaluation was performed
        - "test_files": List of test file information
        - "test_results": List of test execution results
        - "summary": Summary statistics
        - "exit_code": Overall exit code (0 for success, 2 for blocked)
        - "blocking_issues": List of blocking issues
        - "recommendations": List of recommendations
    """
    print(f"=== M13S1 Test Evaluation Suite ===")
    print(f"Specification: {spec_id}")
    print(f"Milestone: {milestone_id}")
    print(f"Generated: {datetime.now().isoformat()}")
    print()

    # Read test plan ledger
    test_files = read_test_plan_ledger(milestone_id, spec_id)

    if not test_files:
        print("ERROR: No test files found in Test Plan Ledger")
        return {
            "spec_id": spec_id,
            "milestone_id": milestone_id,
            "generated_at": datetime.now().isoformat(),
            "test_files": [],
            "test_results": [],
            "summary": {
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "error_tests": 0,
                "red_tests": 0,
                "valid_tests": 0
            },
            "exit_code": 2,  # BLOCKED
            "blocking_issues": ["No test files found in Test Plan Ledger"],
            "recommendations": ["Verify Test Plan Ledger (M13S1T1.md) exists and contains test file entries"]
        }

    # Execute all test files
    test_results = []
    red_tests = 0
    valid_tests = 0

    for test_info in test_files:
        result = execute_test_file(test_info)
        test_results.append(result)

        # Classify test result
        if result["status"] == "PASSED":
            valid_tests += 1
            print(f"✓ {test_info['test_file'].split('/')[-1]}: PASSED")
        elif result["status"] == "FAILED":
            red_tests += 1
            print(f"✓ {test_info['test_file'].split('/')[-1]}: FAILED (VALID_INITIAL_FAILURE)")
        else:
            print(f"✗ {test_info['test_file'].split('/')[-1]}: ERROR")

    # Calculate summary statistics
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "PASSED"])
    failed_tests = len([r for r in test_results if r["status"] == "FAILED"])
    error_tests = len([r for r in test_results if r["status"] == "ERROR"])

    # Determine if this is a healthy Red TDD baseline
    has_red_tests = failed_tests > 0
    has_valid_tests = passed_tests > 0

    if has_red_tests and has_valid_tests:
        exit_code = 0  # SUCCESS (healthy Red TDD baseline)
    else:
        exit_code = 2  # BLOCKED (incomplete test suite)

    # Identify blocking issues
    blocking_issues = []
    recommendations = []

    if error_tests > 0:
        blocking_issues.append(f"Found {error_tests} error tests")
        recommendations.append("Fix error tests")

    if not has_red_tests:
        blocking_issues.append("No Red TDD baseline tests found")
        recommendations.append("Create Red TDD baseline tests (tests that fail initially)")

    if not has_valid_tests:
        blocking_issues.append("No valid tests found")
        recommendations.append("Add more comprehensive test coverage")

    # Generate evaluation report
    evaluation_report = {
        "spec_id": spec_id,
        "milestone_id": milestone_id,
        "generated_at": datetime.now().isoformat(),
        "test_files": test_files,
        "test_results": test_results,
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "red_tests": red_tests,
            "valid_tests": valid_tests
        },
        "exit_code": exit_code,
        "blocking_issues": blocking_issues,
        "recommendations": recommendations
    }

    # Print summary
    print(f"\n=== Test Evaluation Complete ===")
    print(f"Total tests: {total_tests}")
    print(f"  - Passed: {passed_tests}")
    print(f"  - Failed (Red TDD baseline): {failed_tests}")
    print(f"  - Error: {error_tests}")

    if exit_code == 0:
        print(f"✓ Evaluation successful - healthy Red TDD baseline established")
    else:
        print(f"✗ Evaluation blocked - {len(blocking_issues)} blocking issues found")

    return evaluation_report
def write_evaluation_report(evaluation_report: Dict[str, Any]) -> str:
    """
    Write evaluation report to file.

    Args:
        evaluation_report: Evaluation report dictionary

    Returns:
        Path to the written evaluation report file
    """
    spec_id = evaluation_report["spec_id"]
    milestone_id = evaluation_report["milestone_id"]

    # Create output directory
    output_dir = Path(f"milestones/{milestone_id}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate report file path
    report_id = f"{spec_id}TE"
    report_file = output_dir / f"{report_id}.md"

    # Generate report content
    content = f"""---
id: {report_id}
type: test_evaluation
title: "{spec_id} Test Evaluation Report"
milestone_id: {milestone_id}
status: completed
template_version: 1.0.0
---

# Test Evaluation Report {report_id}

## Overview

**Specification:** {spec_id}
**Milestone:** {milestone_id}
**Generated:** {evaluation_report['generated_at']}
**Overall Status:** {"SUCCESS" if evaluation_report['exit_code'] == 0 else "BLOCKED"}

## Summary

- **Total Tests:** {evaluation_report['summary']['total_tests']}
- **Passed Tests:** {evaluation_report['summary']['passed_tests']}
- **Red TDD Baseline Tests:** {evaluation_report['summary']['red_tests']}
- **Valid Tests:** {evaluation_report['summary']['valid_tests']}
- **Error Tests:** {evaluation_report['summary']['error_tests']}
- **Exit Code:** {evaluation_report['exit_code']}

## Detailed Test Results

"""

    for test_result in evaluation_report['test_results']:
        content += f"### {Path(test_result['test_file']).name}\n\n"
        content += f"- **Status:** {test_result['status']}\n"
        content += f"- **Exit Code:** {test_result['exit_code']}\n"
        content += f"- **Test Type:** {test_result['test_type']}\n"
        content += f"- **Verification ID:** {test_result.get('verification_id', 'N/A')}\n"
        content += f"- **Requirement ID:** {test_result.get('requirement_id', 'N/A')}\n"
        if test_result['error']:
            content += f"- **Error:** {test_result['error']}\n"
        content += "\n"

    if evaluation_report['blocking_issues']:
        content += "## Blocking Issues\n\n"
        for issue in evaluation_report['blocking_issues']:
            content += f"- {issue}\n"
        content += "\n"

    if evaluation_report['recommendations']:
        content += "## Recommendations\n\n"
        for rec in evaluation_report['recommendations']:
            content += f"- {rec}\n"
        content += "\n"

    content += f"**Report Status:** EXIT_CODE={evaluation_report['exit_code']}\n"
    content += f"\n---\n\n*This test evaluation report was auto-generated by the evaluate-tests skill for M13S1*\n"

    # Write report to file
    report_file.write_text(content)

    print(f"✓ Evaluation report written: {report_file}")

    return str(report_file)
def main():
    """Main evaluation function"""
    # Configuration for M13S1
    milestone_id = "M13"
    spec_id = "M13S1"

    print(f"Starting M13S1 Test Evaluation")
    print(f"=" * 60)

    # Evaluate test suite
    evaluation_report = evaluate_test_suite(milestone_id, spec_id)

    # Write evaluation report
    report_file = write_evaluation_report(evaluation_report)

    # Return appropriate exit code
    return evaluation_report["exit_code"]
if __name__ == "__main__":
    sys.exit(main())
