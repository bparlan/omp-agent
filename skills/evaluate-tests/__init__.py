#!/usr/bin/env python3
"""
Evaluate Tests Skill Implementation

Evaluate generated test suites and produce validation artifacts.
Implements milestone-agnostic test evaluation with proper AEF compliance.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def main() -> int:
    """Main skill execution function"""
    print("=== Evaluate Tests Skill ===")
    print("Version: 3.7.0-stable")
    print()

    # Show skill info
    skill_info = {
        "name": "evaluate-tests",
        "version": "3.7.0-stable",
        "description": "Evaluate generated test suites and produce validation artifacts",
    }

    print(f"Skill Info: {skill_info}")
    print()

    # Scan ALL milestone directories for test files
    # Not limited to M13, should be milestone-agnostic
    milestone_dirs = [Path(d) for d in os.listdir('.') if os.path.isdir(d) and d.startswith('milestones/')]
    
    # Find ALL test plan files
    test_plan_files = []
    for milestone_dir in milestone_dirs:
        test_plan_files.extend(milestone_dir.glob("TEST-*.md"))
    
    if not test_plan_files:
        print("No test plan files found")
        return 1

    print(f"Found {len(test_plan_files)} test plan files")
    print()

    # Process each test plan
    evaluation_reports = []

    for test_plan_file in test_plan_files:
        spec_id = test_plan_file.stem
        milestone_id = test_plan_file.parent.name
        print(f"--- Processing {spec_id} from {milestone_id} ---")

        # Read test plan content
        content = test_plan_file.read_text()

        # Parse test plan to get test files
        test_files = _parse_test_plan(content, milestone_id)
        
        # Run tests and generate evaluation report
        evaluation_report = _run_tests(test_files, spec_id, milestone_id)
        
        if evaluation_report:
            evaluation_reports.append(evaluation_report)

    # Create evaluation reports
    results = _create_evaluation_reports(evaluation_reports)

    print("\n=== Evaluation Complete ===")
    print(f"Evaluation reports generated: {len(results)}")

    for report_path in results:
        print(f"  - {report_path}")

    return 0


def _parse_test_plan(content: str, milestone_id: str) -> List[Dict[str, str]]:
    """Parse test plan markdown content to extract test files."""
    test_files = []
    
    # Extract test files from traceability table
    lines = content.split('\n')
    in_table = False
    
    for line in lines:
        line = line.strip()
        
        # Look for table header
        if line.startswith("| Test File |"):
            in_table = True
            continue
        
        # Look for table row
        if in_table and line.startswith("|") and not line.startswith("|---"):
            # Parse table row: | tests/M13/S5/test_generation.py | V-FR-TEST-GENERATION-CONTRACT | FR-TEST-GENERATION-CONTRACT | IMPLEMENTATION_CHECK |
            columns = [col.strip() for col in line.split('|') if col.strip()]
            
            if len(columns) >= 4:
                test_file_path = columns[0]
                verification_id = columns[1]
                requirement_id = columns[2]
                test_type = columns[3]
                
                # Extract milestone and spec IDs from path
                test_file_path = test_file_path.strip('`')
                
                test_files.append({
                    "path": test_file_path,
                    "verification_id": verification_id,
                    "requirement_id": requirement_id,
                    "test_type": test_type,
                    "milestone_id": milestone_id,
                })
        
        # Stop when we reach next section
        if in_table and line.startswith("##") and "Test Objectives" in line:
            break
    
    return test_files


def _run_tests(test_files: List[Dict[str, str]], spec_id: str, milestone_id: str) -> Optional[Dict[str, Any]]:
    """Run tests and generate evaluation results."""
    print(f"Running tests for {spec_id}...")
    
    test_results = []
    passed_tests = 0
    total_tests = len(test_files)
    
    for test_file_info in test_files:
        test_file_path = test_file_info["path"]
        test_name = os.path.basename(test_file_path)
        
        print(f"  Testing: {test_name}")
        
        # Try to run the test file
        result = _execute_test_file(test_file_path, test_name)
        
        if result:
            test_results.append(result)
            if result.get("passed", False):
                passed_tests += 1
        else:
            # Test file execution failed
            test_results.append({
                "test_name": test_name,
                "status": "ERROR",
                "passed": False,
                "error_details": "Failed to execute test file",
                "execution_time": 0.0,
                "artifact_validation": {},
                "contract_compliance": {},
            })
    
    # Determine overall status
    status = "passed" if passed_tests == total_tests else "failed"
    
    # Generate evaluation report
    evaluation_report = {
        "spec_id": spec_id,
        "timestamp": datetime.now().isoformat(),
        "milestone_id": milestone_id,
        "test_files": [tf["path"] for tf in test_files],
        "summary": {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0.0,
        },
        "test_results": test_results,
        "issues": _generate_issues(test_results),
        "blocking_issues": _generate_blocking_issues(test_results),
        "status": status,
        "template_version": "1.3.0",
    }
    
    return evaluation_report


def _execute_test_file(test_file_path: str, test_name: str) -> Optional[Dict[str, Any]]:
    """Execute a test file and return results."""
    try:
        # Check if test file exists
        if not os.path.exists(test_file_path):
            return {
                "test_name": test_name,
                "status": "ERROR",
                "passed": False,
                "error_details": f"Test file not found: {test_file_path}",
                "execution_time": 0.0,
                "artifact_validation": {},
                "contract_compliance": {},
            }
        
        # Execute the test file using python
        start_time = datetime.now()
        
        # Run the test file as a Python script
        import subprocess
        result = subprocess.run(
            [sys.executable, test_file_path],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Determine test result based on exit code and output
        passed = result.returncode == 0
        
        # Parse output for additional information
        output_lines = result.stdout.split('\n') if result.stdout else []
        error_lines = result.stderr.split('\n') if result.stderr else []
        
        # Extract validation and compliance information from output
        artifact_validation = _extract_artifact_validation(output_lines)
        contract_compliance = _extract_contract_compliance(output_lines)
        
        # Analyze output for issues
        issues = []
        if result.returncode != 0:
            issues.extend(error_lines)
        
        return {
            "test_name": test_name,
            "status": "PASSED" if passed else "FAILED",
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr if not passed else None,
            "execution_time": execution_time,
            "artifact_validation": artifact_validation,
            "contract_compliance": contract_compliance,
            "issues": issues,
        }
        
    except subprocess.TimeoutExpired:
        return {
            "test_name": test_name,
            "status": "TIMEOUT",
            "passed": False,
            "error_details": "Test execution timed out after 60 seconds",
            "execution_time": 60.0,
            "artifact_validation": {},
            "contract_compliance": {},
        }
    except Exception as e:
        return {
            "test_name": test_name,
            "status": "ERROR",
            "passed": False,
            "error_details": f"Exception during test execution: {str(e)}",
            "execution_time": 0.0,
            "artifact_validation": {},
            "contract_compliance": {},
        }


def _extract_artifact_validation(output_lines: List[str]) -> Dict[str, Any]:
    """Extract artifact validation information from test output."""
    artifact_validation = {}
    
    for line in output_lines:
        if "artifact_validation" in line.lower() or "validate_metadata" in line.lower():
            # Extract validation information
            if "valid:" in line.lower():
                is_valid = "valid:" in line.lower() and "true" in line.lower()
                artifact_validation["valid"] = is_valid
                artifact_validation["message"] = line.strip()
    
    return artifact_validation


def _extract_contract_compliance(output_lines: List[str]) -> Dict[str, Any]:
    """Extract contract compliance information from test output."""
    contract_compliance = {}
    
    for line in output_lines:
        if "contract" in line.lower():
            # Extract compliance information
            contract_compliance["has_contracts"] = True
            contract_compliance["contracts_valid"] = "valid" in line.lower()
    
    return contract_compliance


def _generate_issues(test_results: List[Dict[str, Any]]) -> List[str]:
    """Generate list of issues from test results."""
    issues = []
    
    for result in test_results:
        if not result.get("passed", False):
            issues.append(f"{result['test_name']}: {result.get('error_details', 'Test failed')}")
    
    return issues


def _generate_blocking_issues(test_results: List[Dict[str, Any]]) -> List[str]:
    """Generate list of blocking issues from test results."""
    blocking_issues = []
    
    for result in test_results:
        if result.get("status") == "ERROR" or "TIMEOUT" in result.get("status", ""):
            blocking_issues.append(f"{result['test_name']}: Critical error - {result.get('error_details', 'Unknown error')}")
    
    return blocking_issues


def _create_evaluation_reports(evaluation_reports: List[Dict[str, Any]]) -> List[str]:
    """Create evaluation report files."""
    reports = []
    
    for report_data in evaluation_reports:
        # Create evaluation report content
        report_content = _format_evaluation_report(report_data)
        
        # Create report file path
        milestone_id = report_data["milestone_id"]
        spec_id = report_data["spec_id"]
        report_filename = f"EVA-{spec_id}.md"
        report_path = Path("milestones") / milestone_id / report_filename
        
        # Write report to file
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_content)
        
        reports.append(str(report_path))
        
        print(f"  Generated evaluation report: {report_path}")
    
    return reports


def _format_evaluation_report(report_data: Dict[str, Any]) -> str:
    """Format evaluation report as markdown."""
    milestone_id = report_data["milestone_id"]
    spec_id = report_data["spec_id"]
    
    report_content = f"""---
id: EVA-{spec_id}
type: evaluation
title: "Evaluation Report for {spec_id}"
milestone_id: {milestone_id}
derived_from: ["TEST-{spec_id}"]
status: completed
template_version: 1.3.0
---

# Evaluation Report {spec_id}

## Executive Summary

**Protocol ID:** EVA-{spec_id}
**Specification:** {spec_id}
**Milestone:** {milestone_id}
**Generated:** {report_data["timestamp"]}
**Testable:** true
**Test Framework:** pytest

## Test Execution Summary

**Total Tests:** {report_data["summary"]["total_tests"]}
**Tests Passed:** {report_data["summary"]["passed_tests"]}
**Tests Failed:** {report_data["summary"]["failed_tests"]}
**Success Rate:** {report_data["summary"]["success_rate"]:.1f}%
**Status:** {report_data["status"].upper()}

## Test Results

| Test File | Status | Execution Time | Artifact Validation | Contract Compliance |
|-----------|--------|----------------|---------------------|----------------------|
"""
    
    for result in report_data["test_results"]:
        status = result.get("status", "ERROR")
        execution_time = result.get("execution_time", 0.0)
        artifact_validation = "✅ Valid" if result.get("artifact_validation", {}).get("valid", False) else "❌ Invalid"
        contract_compliance = "✅ Compliant" if result.get("contract_compliance", {}).get("has_contracts", False) else "❌ Non-compliant"
        
        report_content += f"| {result['test_name']} | {status} | {execution_time:.2f}s | {artifact_validation} | {contract_compliance} |\n"
    
    report_content += f"""

## Issues and Blockers

### Issues
{chr(10).join(f"- {issue}" for issue in report_data["issues"])}

### Blocking Issues
{chr(10).join(f"- {issue}" for issue in report_data["blocking_issues"])}

## Next Steps

{"✅ All tests passed. Ready to proceed to next phase." if report_data["status"] == "passed" else "❌ Tests failed. Review issues and fix problems before proceeding."}

---
*Evaluation report generated by evaluate-tests skill*
"""
    
    return report_content


if __name__ == "__main__":
    sys.exit(main())