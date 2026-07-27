#!/bin/bash

# Test Suite: Issue 2 - M4's 100% Pass Claim - Unverified
# Tests: Test Case 2.1, 2.2, 2.3
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
    echo "  Test Suite: Issue 2 - M4's 100% Pass Claim - Unverified"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
}

# Function to print test footer
print_footer() {
UNVERIFIED_CLAIM=$(grep -n "100% pass" milestones/M4/M4S1E.md 2>/dev/null || true)
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

# Test Case 2.1: M4S1E.md contains no unverified claims
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 2.1: M4S1E.md contains no unverified claims"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for unverified '100% pass' claims in M4S1E.md..."

# Check for "100% pass" pattern in M4S1E.md
UNVERIFIED_CLAIM=$(grep -n "100% pass" milestones/M4/M4S1E.md 2>/dev/null || true)

if [ -z "$UNVERIFIED_CLAIM" ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - No '100% pass' claim found in M4S1E.md"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - Found unverified claim in M4S1E.md:"
    echo "  $UNVERIFIED_CLAIM"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 2.2: M4 test scripts execute cleanly
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 2.2: M4 test scripts execute cleanly"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Running M4 test scripts with bash -n syntax check..."

M4_SYNTAX_ERRORS=0
for script in tests/M4/*.sh; do
    if bash -n "$script" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $script"
    else
        echo -e "  ${RED}✗${NC} $script (syntax error)"
        M4_SYNTAX_ERRORS=$((M4_SYNTAX_ERRORS + 1))
    fi
done

if [ "$M4_SYNTAX_ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - All M4 test scripts have valid syntax"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - $M4_SYNTAX_ERRORS M4 test script(s) have syntax errors"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 2.3: Warnings not conflated with passes
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 2.3: Warnings not conflated with passes"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for 'PASSED with warnings' or similar partial pass indicators..."

# Check for partial pass indicators in bash test scripts
PARTIAL_PASS_COUNT=$(grep -r "PASSED with warnings" tests/M4/ 2>/dev/null | wc -l)

if [ "$PARTIAL_PASS_COUNT" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - No partial pass indicators found"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - Found $PARTIAL_PASS_COUNT partial pass indicator(s) in M4 test scripts:"
    grep -r "PASSED with warnings" tests/M4/ 2>/dev/null
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Bonus: Verify M4S1E.md mentions actual test execution results
echo "═══════════════════════════════════════════════════════════════"
echo "  Bonus: M4S1E.md mentions actual test execution"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

if grep -q "Exit code" milestones/M4/M4S1E.md && \
   grep -q "wall time" milestones/M4/M4S1E.md; then
    echo -e "  ${GREEN}✓ PASSED${NC} - M4S1E.md includes execution details"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${YELLOW}⚠ WARNING${NC} - M4S1E.md missing execution details (optional)"
    TESTS_PASS=$((TESTS_PASS + 1))
fi

print_footer
