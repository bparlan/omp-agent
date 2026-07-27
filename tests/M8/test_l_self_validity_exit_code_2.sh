#!/bin/bash
# Test l: Verify that self-validity assertion failures exit with code 2

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Script with failing self-validity assertion should exit with code 2
echo "Test 1: Self-validity assertion failure exit code"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary script with a failing self-validity assertion
temp_script=$(mktemp)
trap "rm -f $temp_script" EXIT

cat > "$temp_script" <<'EOFSCRIPT'
#!/bin/bash
# Self-validity assertion failure
if [[ false ]]; then
    echo "VALIDITY FAILURE: test did not exercise intended subject"
    echo "Subject: $0"
    echo "Reason: assertion failed"
    exit 2
fi

# Test logic (should not reach here)
echo "test passed"
exit 0
EOFSCRIPT

# Make it executable
chmod +x "$temp_script"

# Run the script, capture output separately, and capture exit code
output=$("$temp_script")
exit_code=$?

if [[ $exit_code -eq 2 ]]; then
    echo "  ✓ Self-validity assertion failure correctly exits with code 2"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Expected exit code 2, got $exit_code"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Script with valid self-validity assertion should exit with code 0
echo "Test 2: Valid self-validity assertion exit code"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary script with a passing self-validity assertion
temp_script2=$(mktemp)
trap "rm -f $temp_script2" EXIT

cat > "$temp_script2" <<'EOFSCRIPT'
#!/bin/bash
# Self-validity assertion success
if [[ true ]]; then
    echo "validity check passed"
    echo "subject exercised successfully"
fi

# Test logic (should reach here)
echo "test passed"
exit 0
EOFSCRIPT

# Make it executable
chmod +x "$temp_script2"

# Run the script, capture output separately, and capture exit code
output=$("$temp_script2")
exit_code=$?

if [[ $exit_code -eq 0 ]]; then
    echo "  ✓ Valid self-validity assertion correctly exits with code 0"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Expected exit code 0, got $exit_code"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Script with failing test logic (exit 1) should NOT be confused with exit 2
echo "Test 3: Test failure exit code is distinct from validity failure"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary script with failing test logic
temp_script3=$(mktemp)
trap "rm -f $temp_script3" EXIT

cat > "$temp_script3" <<'EOFSCRIPT'
#!/bin/bash
# Self-validity assertion success
if [[ true ]]; then
    echo "validity check passed"
fi

# Test logic failure (exit 1, NOT exit 2)
echo "test failed"
exit 1
EOFSCRIPT

# Make it executable
chmod +x "$temp_script3"

# Run the script, capture output separately, and capture exit code
output=$("$temp_script3")
exit_code=$?

if [[ $exit_code -eq 1 ]]; then
    echo "  ✓ Test failure (exit 1) correctly distinguished from validity failure (exit 2)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Expected exit code 1 for test failure, got $exit_code"
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
