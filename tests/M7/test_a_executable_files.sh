#!/bin/bash
# Test A: Verify generate-tests produces executable test files
# Purpose: Validate that generate-tests generates executable test files
#          with correct extension, correct interpreter, and valid syntax
# Source: M7S1, FR-7.1
# Source Verification: M7S1V, Test A

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

function test_a_executable_files() {
    local test_dir="tests/M7"
    local fail_count=0
    local total=0

    # Check each test file exists
    for test_file in "$test_dir"/test_*.sh; do
        total=$((total + 1))
        if [ ! -f "$test_file" ]; then
            echo "FAIL: Missing test file: $test_file"
            fail_count=$((fail_count + 1))
            continue
        fi

        # Check file is executable
        if [ ! -x "$test_file" ]; then
            echo "FAIL: Not executable: $test_file"
            fail_count=$((fail_count + 1))
            continue
        fi

        # Check shebang is valid
        shebang=$(head -1 "$test_file")
        if [ "$shebang" != "#!/bin/bash" ] && [ "$shebang" != "#!/usr/bin/env bash" ]; then
            echo "FAIL: Invalid shebang in $test_file: $shebang"
            fail_count=$((fail_count + 1))
            continue
        fi

        # Check bash syntax is valid
        if ! bash -n "$test_file" 2>/dev/null; then
            echo "FAIL: Syntax error in $test_file"
            fail_count=$((fail_count + 1))
            continue
        fi

        echo "PASS: $test_file — executable, valid shebang, valid syntax"
    done

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count / $total test files have issues"
        return 1
    fi

    echo "PASS: All $total test files are valid"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_a_executable_files; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_A_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_A_RESULT=FAIL"
    exit 1
fi
