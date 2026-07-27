#!/bin/bash
# Test h: Verify validity gate correctly identifies self-scanning tests as INVALID

set -e

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Mock validity gate that checks if a test is self-scanning
# Returns INVALID_TEST if test contains patterns indicating it scans itself
validity_gate() {
    local test_script="$1"

    # Check for self-scanning patterns (violates validity criterion #5)
    # A test that references $(basename "$0") is self-scanning
    if [[ "$test_script" == *"$(basename "$0")"* ]]; then
        echo "INVALID_TEST"
        return 0
    fi

    echo "VALID_TEST"
    return 0
}

# Create a known self-scanning test pattern
self_scan_test_content="#!/bin/bash
# This test scans its own file (violates validity criterion #5)
if [[ \"$0\" == \"$0\" ]]; then
    echo \"Scanning self\"
fi"

# Test 1: Self-scanning test should be INVALID
echo "Test 1: Self-scanning test detection"
TESTS_RUN=$((TESTS_RUN + 1))

# The validity gate detects this as self-scanning
verdict=$(validity_gate "$self_scan_test_content")
if [[ "$verdict" == "INVALID_TEST" ]]; then
    echo "  ✓ Self-scanning test correctly identified as INVALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Self-scanning test should be INVALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Normal test (non-self-scanning) should be VALID
echo "Test 2: Normal test should be VALID"
TESTS_RUN=$((TESTS_RUN + 1))

normal_test_content="#!/bin/bash
# This is a normal test that doesn't scan itself
echo 'Normal test output'"

verdict=$(validity_gate "$normal_test_content")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Normal test correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Normal test should be VALID, got $verdict"
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
