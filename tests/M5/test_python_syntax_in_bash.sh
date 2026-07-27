#!/bin/bash

# Test Suite: Issue 1 - M5 Test Hallucination - Python Syntax in Bash Files
# Tests: Test Case 1.1, 1.2, 1.3
# Total: 3 test cases

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
    echo "  Test Suite: Issue 1 - M5 Test Hallucination - Python Syntax"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
}

# Function to print test footer
print_footer() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Test Summary"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Tests Run: $TESTS_RUN"
    echo "  Tests Pass: $TESTS_PASS"
    echo "  Tests Fail: $TESTS_FAIL"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    if [ $TESTS_FAIL -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed!${NC}"
        exit 1
    fi
}

print_header

# Test Case 1.1: Python syntax not embedded in bash files
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 1.1: Python syntax not embedded in bash files"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for Python class definitions in bash files..."

# Count Python class definitions in bash files
PYTHON_CLASSES=$(grep -l "^class " tests/M5/*.sh 2>/dev/null | wc -l)

if [ "$PYTHON_CLASSES" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - No Python class definitions found"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - Found $PYTHON_CLASSES bash file(s) with Python class definitions:"
    grep -l "^class " tests/M5/*.sh 2>/dev/null
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 1.2: Bash scripts execute without syntax errors
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 1.2: Bash scripts execute without syntax errors"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Running bash -n syntax checks on all test scripts..."

BASH_SYNTAX_ERRORS=0
for script in tests/M5/*.sh; do
    if bash -n "$script" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $script"
    else
        echo -e "  ${RED}✗${NC} $script (syntax error)"
        BASH_SYNTAX_ERRORS=$((BASH_SYNTAX_ERRORS + 1))
    fi
done

if [ "$BASH_SYNTAX_ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - All bash scripts have valid syntax"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - $BASH_SYNTAX_ERRORS bash script(s) have syntax errors"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 1.3: Test counters accurate
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 1.3: Test counters accurate"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking test counter definitions in bash files..."

COUNTER_ERRORS=0
for script in tests/M5/*.sh; do
    # Check for TESTS_RUN, TESTS_PASS, TESTS_FAIL definitions
    if grep -q "^TESTS_RUN=0$" "$script" && \
       grep -q "^TESTS_PASS=0$" "$script" && \
       grep -q "^TESTS_FAIL=0$" "$script"; then
        echo -e "  ${GREEN}✓${NC} $script"
    else
        echo -e "  ${RED}✗${NC} $script (incomplete counter definitions)"
        COUNTER_ERRORS=$((COUNTER_ERRORS + 1))
    fi
done

if [ "$COUNTER_ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - All test scripts have accurate counter definitions"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - $COUNTER_ERRORS test script(s) have incomplete counter definitions"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

print_footer
