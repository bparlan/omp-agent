#!/bin/bash
# Test j: Negative test — verify a valid test is NOT classified as INVALID

set -e

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Mock validity gate that checks file existence (validity criterion #1)
validity_gate() {
    local subject_path="$1"

    # Check if file exists
    if [[ ! -f "$subject_path" ]]; then
        echo "INVALID_TEST"
        return 0
    fi

    echo "VALID_TEST"
    return 0
}

# Test 1: Valid test with existing file should be VALID
echo "Test 1: Valid test with existing file"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary file
temp_file=$(mktemp)
echo "# Test subject" > "$temp_file"

# Mock subject execution
mock_subject() {
    echo "subject executed"
}

# Valid test: verifies the subject file exists and can be executed
validity_gate "$temp_file"

# The test should succeed if the validity gate returns VALID_TEST
verdict=$(validity_gate "$temp_file")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Valid test correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Valid test should be VALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Test with module import (Python case)
echo "Test 2: Valid test with module import"
TESTS_RUN=$((TESTS_RUN + 1))

# Mock module import check
validity_gate_import() {
    local module_name="$1"

    # Simulate successful import
    if [[ "$module_name" != "non_existent_module" ]]; then
        echo "VALID_TEST"
        return 0
    fi

    echo "INVALID_TEST"
    return 0
}

verdict=$(validity_gate_import "sys")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Valid module import correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Valid module import should be VALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Test with function existence check
echo "Test 3: Valid test with function existence check"
TESTS_RUN=$((TESTS_RUN + 1))

# Mock function existence check
validity_gate_function() {
    local function_name="$1"

    # Simulate successful function check
    if [[ "$function_name" != "non_existent_function" ]]; then
        echo "VALID_TEST"
        return 0
    fi

    echo "INVALID_TEST"
    return 0
}

verdict=$(validity_gate_function "echo")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Valid function check correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Valid function check should be VALID, got $verdict"
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
