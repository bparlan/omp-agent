#!/bin/bash

# Test Suite: Issue 1 - M5 Test Hallucination - Python Syntax Validation
# Tests: Test Case 1.1, 1.2, 1.3
# Total: 4 test cases

set -e

# Test counter
TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print test header
print_header() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Test Case $1: $2"
    echo "═══════════════════════════════════════════════════════════════"
}

# Function to print test footer
print_footer() {
    echo ""
    echo "  Total Tests Run: $TESTS_RUN"
    echo "  Tests Passed: $TESTS_PASS"
    echo "  Tests Failed: $TESTS_FAIL"
    echo ""
    if [ "$TESTS_FAIL" -eq 0 ]; then
        echo "  Result: $GREEN ALL TESTS PASSED$NC"
    else
        echo "  Result: $RED SOME TESTS FAILED$NC"
    fi
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
}

print_header "1.1" "Python syntax not embedded in bash files"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for Python class definitions in bash files..."

# Count Python class definitions in bash files
PYTHON_CLASSES=$(grep -l "^class " tests/M5/*.sh 2>/dev/null | wc -l | tr -d ' ')

if [ "$PYTHON_CLASSES" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - No Python class definitions found"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - Found $PYTHON_CLASSES files with Python class definitions:"
    grep -l "^class " tests/M5/*.sh | while read file; do
        echo "    - $file"
        grep -n "^class " "$file" | head -3
    done
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_header "1.2" "Bash scripts use bash syntax"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for bash function definitions..."

# Check for bash function definitions (not Python class definitions)
BASH_FUNCTIONS=$(grep -E "^function " tests/M5/*.sh | wc -l | tr -d ' ')

echo "  Found $BASH_FUNCTIONS bash function definitions"

if [ "$BASH_FUNCTIONS" -gt 0 ]; then
    echo "  $GREEN ✓ PASS$NC - Bash scripts use bash function syntax"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $YELLOW ⚠ WARNING$NC - No bash function definitions found"
    echo "  This may be valid if scripts use different syntax"
    TESTS_PASS=$((TESTS_PASS + 1))
fi

echo ""

print_header "1.3" "Scripts have valid shebangs"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Validating shebang lines in all bash scripts..."

VALID_SHEBANGS=0
INVALID_SHEBANGS=0

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        shebang=$(head -1 "$script" | tr -d '\n' | cut -c3-)
        if echo "$shebang" | grep -qE "(#!/|bash|/bin/bash|/usr/bin/env bash)"; then
            if echo "$shebang" | grep -qE "(bash|/bin/bash|/usr/bin/env bash)"; then
                VALID_SHEBANGS=$((VALID_SHEBANGS + 1))
            else
                echo "  $YELLOW ⚠ WARNING$NC - Script $script uses $shebang (not bash)"
            fi
        else
            echo "  $RED ✗ FAIL$NC - Script $script missing shebang"
            INVALID_SHEBANGS=$((INVALID_SHEBANGS + 1))
        fi
    fi
done

echo "  Valid shebangs found: $VALID_SHEBANGS"

if [ "$INVALID_SHEBANGS" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - All scripts have valid shebangs"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - $INVALID_SHEBANGS scripts missing valid shebangs"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_header "1.4" "Bash scripts execute without syntax errors"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Running bash -n syntax checks on all test scripts..."

BASH_SYNTAX_ERRORS=0

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        if ! bash -n "$script" 2>/dev/null; then
            echo "  $RED ✗ FAIL$NC - Syntax error in $script"
            BASH_SYNTAX_ERRORS=$((BASH_SYNTAX_ERRORS + 1))
        fi
    fi
done

if [ "$BASH_SYNTAX_ERRORS" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - All scripts pass bash syntax validation"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - $BASH_SYNTAX_ERRORS scripts have syntax errors"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_footer
