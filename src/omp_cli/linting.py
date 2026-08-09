\
import sys
import os
import re

def lint_verification_contract(verification_filepath: str) -> bool:
    """
    Lints a verification contract file for forbidden prose patterns that are not properly tagged.
    Enforces the 'No Prose Contracts' rule.
    Returns True if linting passes, False otherwise.
    """
    if not os.path.isfile(verification_filepath):
        print(f"FAIL: Verification contract file not found: {verification_filepath}", file=sys.stderr)
        return False

    FORBIDDEN_PATTERNS = ("grep", "text search", "text-match", "text matching")
    ALLOWED_TAG = "<!-- ALLOWED: literal-boilerplate -->"
    
    offending_lines = []
    exit_code = 0

    try:
        with open(verification_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                is_forbidden = False
                for pattern in FORBIDDEN_PATTERNS:
                    # Case-insensitive check for forbidden patterns
                    if re.search(pattern, line, re.IGNORECASE):
                        is_forbidden = True
                        break
                
                if is_forbidden:
                    # Check if the line is NOT tagged
                    if ALLOWED_TAG not in line:
                        offending_lines.append(line.strip())
                        exit_code = 1
        
        if exit_code != 0:
            print(f"FAIL: Found forbidden verification patterns without the required tag in {verification_filepath}. Offending lines:", file=sys.stderr)
            for offending_line in offending_lines:
                print(f"  - {offending_line}", file=sys.stderr)
            return False
        else:
            print(f"PASS: Verification contract linting passed for {verification_filepath}. No forbidden patterns found without the required tag.")
            return True

    except Exception as e:
        print(f"FAIL: Error linting verification contract file {verification_filepath}: {e}", file=sys.stderr)
        return False

