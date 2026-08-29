import subprocess
import os

# Path to the script being tested
SCRIPT_PATH = "bin/omp-verify-precondition"

def run_script(ledger_path, test_dir):
    """Runs the omp-verify-precondition script and returns its exit code."""
    command = [SCRIPT_PATH, "--ledger", ledger_path, "--test-dir", test_dir]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        print(f"--- STDOUT ---\n{result.stdout}\n--- STDERR ---\n{result.stderr}\n--- EXIT CODE ---\n{result.returncode}")
        return result.returncode
    except FileNotFoundError:
        # Should not happen if SCRIPT_PATH is correct and script is executable
        print(f"Error: {SCRIPT_PATH} not found.")

def test_valid_fixtures():
    """Tests the tool with valid fixtures where some scripts fail as expected."""
    ledger = "tests/fixtures/synthetic_precondition_valid/ledger.csv"
    test_dir = "tests/fixtures/synthetic_precondition_valid/"

    # Expected outcome:
    # script_that_doesnt_exist.sh -> expected 127 (VALID_INITIAL_FAILURE), simulated by exit code -1
    # script_that_fails.sh -> expected 1 (FAIL)
    # The tool should report PASS if all expected outcomes match.
    # The script's internal logic maps:
    # - actual -1 with expected 127 to PASS (simulated VALID_INITIAL_FAILURE).
    # - actual 1 with expected 1
    # Thus, overall PASS (exit code 0) is expected.

    print(f"\nRunning test_valid_fixtures with ledger: {ledger}, test_dir: {test_dir}")
    exit_code = run_script(ledger, test_dir)

    # Expecting overall PASS (exit code 0)
    assert exit_code == 0, f"Expected exit code 0 (PASS) for valid fixtures, but got {exit_code}"
    print("test_valid_fixtures passed.")

def test_invalid_fixtures():
    """Tests the tool with invalid fixtures, expecting specific failures and validity errors."""
    ledger = "tests/fixtures/synthetic_precondition_invalid/ledger.csv"
    test_dir = "tests/fixtures/synthetic_precondition_invalid/"

    # Expected outcome:
    # script_that_passes_prematurely.sh -> expected 1 (FAIL), but it exits 0. This leads to FAIL.
    # script_with_syntax_error.sh -> expected 2 (VALIDITY_FAILURE), and it exits with a syntax error (likely 2 or other non-zero).
    # Overall, this should result in FAIL (exit code 1) because of the premature passing, and potentially VALIDITY_FAILURE depending on exact error handling.
    # The determine_overall_exit_code logic prioritizes VALIDITY_FAILURE (2) if any script returns 2.
    # If script_with_syntax_error.sh exits with 2, then VALIDITY_FAILURE is expected.
    # If script_that_passes_prematurely.sh causes a general FAIL (1), and syntax error causes VALIDITY_FAILURE (2), then 2 should be returned.

    print(f"\nRunning test_invalid_fixtures with ledger: {ledger}, test_dir: {test_dir}")
    exit_code = run_script(ledger, test_dir)

    # Expecting VALIDITY_FAILURE (exit code 2) due to syntax error script.
    # If script_with_syntax_error.sh exits with 2, then 2 is the overall exit code.
    # If script_that_passes_prematurely.sh causes a general FAIL (1), and syntax error causes VALIDITY_FAILURE (2), then 2 should be returned.
    assert exit_code == 2, f"Expected exit code 2 (VALIDITY_FAILURE) for invalid fixtures, but got {exit_code}"
    print("test_invalid_fixtures passed.")

def test_missing_ledger():
    """Tests the tool when the ledger file is missing."""
    ledger = "tests/non_existent_ledger.csv"
    test_dir = "tests/fixtures/synthetic_precondition_valid/" # A valid test dir is still needed

    print(f"\nRunning test_missing_ledger with ledger: {ledger}")
    exit_code = run_script(ledger, test_dir)

    # Missing ledger should result in VALIDITY_FAILURE (exit code 2) as per implementation logic for parse_ledger errors.
    assert exit_code == 2, f"Expected exit code 2 (VALIDITY_FAILURE) for missing ledger, but got {exit_code}"
    print("test_missing_ledger passed.")

def test_missing_test_dir():
    """Tests the tool when the test directory is missing."""
    ledger = "tests/fixtures/synthetic_precondition_valid/ledger.csv"
    test_dir = "tests/non_existent_test_dir/"

    print(f"\nRunning test_missing_test_dir with ledger: {ledger}, test_dir: {test_dir}")
    exit_code = run_script(ledger, test_dir)

    # Missing test dir should lead to scripts not being found, and likely overall FAIL (1).
    # The execute_script returns -1 for FileNotFoundError. The determine_overall_exit_code maps
    # actual -1 with expected != 127 to FAIL (1).
    assert exit_code == 1, f"Expected exit code 1 (FAIL) for missing test directory, but got {exit_code}"
    print("test_missing_test_dir passed.")

# The following tests are commented out because the current script does not directly support
# testing for missing scripts that are *not* in the ledger. It only checks scripts present in the ledger.
# If a script is not in the ledger, it's simply ignored.
# If we wanted to test cases where the ledger references a script that exists in the dir but not in the ledger,
# we would need to modify the script to handle that.
# def test_script_in_dir_but_not_in_ledger():
#     """Tests scenario where a script exists in test_dir but not in ledger."""
#     # This requires creating a new fixture where a script exists in the dir
#     # but is not listed in ledger.csv
#     pass

# Example of how to run these tests if this were a standard Python test file:
# if __name__ == "__main__":
#     test_valid_fixtures()
#     test_invalid_fixtures()
#     test_missing_ledger()
#     test_missing_test_dir()
#     print("\nAll implemented tests completed.")

if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main([__file__]))