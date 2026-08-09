# validators.py

# Imports from original scripts
import argparse
import sys
import os
import re
import subprocess

# Path to the git integrity check script, assumed to be in the same directory
# This needs to be relative to the *execution environment* of the script. 
# If bin/ is at the root, and validators are in src/omp_cli, the path might need adjustment.
# For now, assuming bin/ is still at root.
GIT_INTEGRITY_SCRIPT = "./bin/omp-verify-git-integrity"

def check_approval_stamp(spec_path: str) -> bool:
    try:
        with open(spec_path, 'r') as f:
            content = f.read()
        # Looking for the exact pattern specified
        approval_marker = "#### User Approval\n* [x] Approved for implementation by user"
        return approval_marker in content
    except FileNotFoundError:
        print(f"Error: Specification file not found at {spec_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error reading specification file {spec_path}: {e}", file=sys.stderr)
        return False

def check_test_readiness(test_dir: str) -> bool:
    # This function checks if the test directory exists and is not empty,
    # and that no files within it contain NUL bytes (\x00).
    if not os.path.isdir(test_dir):
        print(f"BLOCKED: Test directory not found at {test_dir}", file=sys.stderr)
        return False # Indicate failure (leads to exit 1)
    
    try:
        files_in_dir = os.listdir(test_dir)
        if not files_in_dir:
            print(f"BLOCKED: Test directory '{test_dir}' is empty. No tests found.", file=sys.stderr)
            return False # Indicate failure (leads to exit 1)
        
        for filename in files_in_dir:
            filepath = os.path.join(test_dir, filename)
            # Basic check for NUL bytes in files
            with open(filepath, 'rb') as f:
                if b'\x00' in f.read():
                    print(f"BLOCKED: File '{filename}' in '{test_dir}' contains NUL byte.", file=sys.stderr)
                    return False # Indicate failure (leads to exit 1)
        
        return True # Directory exists, is not empty, and contains no NUL bytes.
    except Exception as e:
        print(f"Error checking test directory {test_dir}: {e}", file=sys.stderr)
        return False

def run_git_integrity_check(ledger_path: str) -> int:
    """Runs the git integrity check script and returns its exit code."""
    try:
        # Ensure the script is executable (though we made it executable earlier, this is a safeguard)
        if not os.access(GIT_INTEGRITY_SCRIPT, os.X_OK):
            print(f"Error: Git integrity script is not executable: {GIT_INTEGRITY_SCRIPT}", file=sys.stderr)
            return 2 # VALIDITY_FAILURE

        # Execute the git integrity check, passing the ledger path.
        result = subprocess.run([
            GIT_INTEGRITY_SCRIPT,
            "--ledger", ledger_path
        ], capture_output=True, text=True, check=False)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
        return result.returncode

    except FileNotFoundError:
        print(f"Error: Git integrity script not found: {GIT_INTEGRITY_SCRIPT}", file=sys.stderr)
        return 2 # VALIDITY_FAILURE
    except Exception as e:
        print(f"An unexpected error occurred while running git integrity check: {e}", file=sys.stderr)
        return 2 # VALIDITY_FAILURE


# Note: The main function with argparse from original scripts is omitted here, 
# as these are now intended to be library functions within the 'omp_cli' package.
# If these functions were intended to be directly executable commands,
# they would need to be exposed via __init__.py or a dedicated CLI entry point.

# Example of how these functions might be used externally:
# from omp_cli.validators import check_approval_stamp, check_test_readiness, run_git_integrity_check

# if __name__ == "__main__":
#     # Example usage if this file were run directly (which it shouldn't be after refactoring)
#     # This part would need to be adapted based on how these validators are intended to be invoked.
