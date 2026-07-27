#!/bin/bash
# Test i: Verify validity gate correctly identifies tests targeting non-existent files as INVALID

set -e

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Mock validity gate that checks file existence
validity_gate() {
    local subject_path="$1"

    # Check if file exists (simulating validity criterion #1)
    if [[ ! -f "$subject_path" ]]; then
        echo "INVALID_TEST"
        return 0
    fi

    echo "VALID_TEST"
    return 0
}

# Test 1: Non-existent file should be INVALID
echo "Test 1: Non-existent file detection"
TESTS_RUN=$((TESTS_RUN + 1))

# Test with a path that doesn't exist
non_existent_path="/tmp/non_existent_file_12345.txt"

verdict=$(validity_gate "$non_existent_path")
if [[ "$verdict" == "INVALID_TEST" ]]; then
    echo "  ✓ Non-existent path correctly identified as INVALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Non-existent path should be INVALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Existing file should be VALID
echo "Test 2: Existing file should be VALID"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary file
temp_file=$(mktemp)
trap "rm -f $temp_file" EXIT

verdict=$(validity_gate "$temp_file")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Existing path correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Existing path should be VALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Directory instead of file (invalid)
echo "Test 3: Directory should be INVALID"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary directory
temp_dir=$(mktemp -d)
trap "rm -rf $temp_dir" EXIT

verdict=$(validity_gate "$temp_dir")
if [[ "$verdict" == "INVALID_TEST" ]]; then
    echo "  ✓ Directory path correctly identified as INVALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Directory path should be INVALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Summary
echo "TESTS_RUN=$TESTS_RUN"
echo "TESTS_PASSED=$TESTS_PASSED"
echo "TESTS_FAILED=$TESTS_FAILED"

if [[ $TESTS_FAILED -eq 0 ]]; then
    exit 0
else
    exit 1
fi
