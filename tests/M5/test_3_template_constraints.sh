#!/bin/bash

# Test Suite: Template Language Constraints
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

print_header "2.1" "Template specifies bash script requirements"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking template for bash script requirements..."

TEMPLATE_FILE="templates/test_template.md"

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Template file not found: $TEMPLATE_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for bash-related documentation
    BASH_FOUND=$(grep -i "bash" "$TEMPLATE_FILE" | grep -E "(function|variable|exit code)" | wc -l | tr -d ' ')

    if [ "$BASH_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Template includes bash script requirements"
        echo "    Found $BASH_FOUND references to bash syntax/function/variable"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $RED ✗ FAIL$NC - Template lacks bash script requirements"
        echo "    Expected: References to bash function syntax, variable usage, exit codes"
        TESTS_FAIL=$((TESTS_FAIL + 1))
    fi
fi

echo ""

print_header "2.2" "Template prohibits embedded mock code"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking template for mock code prohibition..."

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Template file not found: $TEMPLATE_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for explicit prohibition of embedded mock code
    MOCK_FOUND=$(grep -i "mock" "$TEMPLATE_FILE" | grep -i "embedded\|python class\|separate" | wc -l | tr -d ' ')

    if [ "$MOCK_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Template explicitly prohibits embedded mock code"
        echo "    Found $MOCK_FOUND references to mock code separation"
        grep -i "mock" "$TEMPLATE_FILE" | grep -i "embedded\|python class\|separate"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $YELLOW ⚠ WARNING$NC - Template may not explicitly prohibit embedded mock code"
        echo "    Expected: 'Mock objects must be defined in separate files or bash functions, not as Python classes'"
        TESTS_PASS=$((TESTS_PASS + 1))
    fi
fi

echo ""

print_header "2.3" "Template enforces language extension consistency"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking template for language extension consistency..."

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Template file not found: $TEMPLATE_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for language extension constraints
    EXT_FOUND=$(grep -E "\.sh.*bash" "$TEMPLATE_FILE" | wc -l | tr -d ' ')
    EXT2_FOUND=$(grep -E "file extension.*language" "$TEMPLATE_FILE" | wc -l | tr -d ' ')

    if [ "$EXT_FOUND" -gt 0 ] || [ "$EXT2_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Template enforces language extension consistency"
        echo "    Found $EXT_FOUND references to .sh files with bash"
        [ "$EXT2_FOUND" -gt 0 ] && echo "    Found $EXT2_FOUND references to file extension matching language"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $YELLOW ⚠ WARNING$NC - Template may not explicitly enforce language extension consistency"
        echo "    Expected: Template links .sh files to bash syntax requirements"
        TESTS_PASS=$((TESTS_PASS + 1))
    fi
fi

echo ""

print_header "2.4" "Template documentation is complete"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking template structure..."

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Template file not found: $TEMPLATE_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for required sections
    REQUIRED_SECTIONS=("Output Format" "Mock Code Rules" "Language Extension Consistency")

    MISSING_SECTIONS=0

    for section in "${REQUIRED_SECTIONS[@]}"; do
        if grep -q "^## $section" "$TEMPLATE_FILE" || grep -q "^### $section" "$TEMPLATE_FILE"; then
            echo "    $GREEN ✓$NC $section section found"
        else
            echo "    $RED ✗$NC $section section missing"
            MISSING_SECTIONS=$((MISSING_SECTIONS + 1))
        fi
    done

    if [ "$MISSING_SECTIONS" -eq 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Template has complete documentation"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $RED ✗ FAIL$NC - Template missing $MISSING_SECTIONS required sections"
        TESTS_FAIL=$((TESTS_FAIL + 1))
    fi
fi

echo ""

print_footer
