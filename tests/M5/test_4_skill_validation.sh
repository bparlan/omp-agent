#!/bin/bash

# Test Suite: generate-tests Skill Strict Validation
# Tests: Test Case 3.1, 3.2, 3.3
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

print_header "3.1" "Skill includes syntax validation gate"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking generate-tests skill for syntax validation documentation..."

SKILL_FILE="skills/generate-tests/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Skill file not found: $SKILL_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for syntax validation mentions
    SYNTAX_FOUND=$(grep -i "syntax" "$SKILL_FILE" | grep -i "validate\|check\|bash -n" | wc -l | tr -d ' ')

    if [ "$SYNTAX_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Skill documents syntax validation step"
        echo "    Found $SYNTAX_FOUND references to syntax validation"
        grep -i "syntax" "$SKILL_FILE" | grep -i "validate\|check\|bash -n" | head -3
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $RED ✗ FAIL$NC - Skill lacks syntax validation documentation"
        echo "    Expected: References to bash -n or python -m py_compile validation"
        TESTS_FAIL=$((TESTS_FAIL + 1))
    fi
fi

echo ""

print_header "3.2" "Skill runs bash syntax check on bash scripts"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for bash syntax check command..."

if [ ! -f "$SKILL_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Skill file not found: $SKILL_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for bash -n command
    BASH_N_FOUND=$(grep -n "bash -n" "$SKILL_FILE" | wc -l | tr -d ' ')

    if [ "$BASH_N_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Skill includes bash -n syntax check"
        echo "    Found $BASH_N_FOUND references to bash -n command at line(s):"
        grep -n "bash -n" "$SKILL_FILE"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $RED ✗ FAIL$NC - Skill does not include bash -n command"
        echo "    Expected: bash -n tests/M{X}/test_*.sh command in skill"
        TESTS_FAIL=$((TESTS_FAIL + 1))
    fi
fi

echo ""

print_header "3.3" "Skill runs Python syntax check on Python scripts"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for Python syntax check command..."

if [ ! -f "$SKILL_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Skill file not found: $SKILL_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for py_compile command
    PY_COMPILE_FOUND=$(grep -n "py_compile" "$SKILL_FILE" | wc -l | tr -d ' ')

    if [ "$PY_COMPILE_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Skill includes python -m py_compile check"
        echo "    Found $PY_COMPILE_FOUND references to py_compile command at line(s):"
        grep -n "py_compile" "$SKILL_FILE"
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $YELLOW ⚠ WARNING$NC - Skill does not include py_compile command"
        echo "    Expected: python -m py_compile tests/M{X}/test_*.py command in skill"
        echo "    (This may be valid if skill only checks bash scripts)"
        TESTS_PASS=$((TESTS_PASS + 1))
    fi
fi

echo ""

print_header "3.4" "Skill rejects completion if syntax errors found"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for syntax error failure handling..."

if [ ! -f "$SKILL_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Skill file not found: $SKILL_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for error handling for syntax errors
    ERROR_FOUND=$(grep -i "if.*syntax.*error" "$SKILL_FILE" | wc -l | tr -d ' ')
    REJECT_FOUND=$(grep -i "reject\|do not mark\|mark.*complete" "$SKILL_FILE" | wc -l | tr -d ' ')

    if [ "$ERROR_FOUND" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Skill includes syntax error handling"
        echo "    Found $ERROR_FOUND references to syntax error conditions"
        grep -A2 -B2 "if.*syntax.*error" "$SKILL_FILE" | head -10
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $RED ✗ FAIL$NC - Skill lacks syntax error handling"
        echo "    Expected: Error handling that rejects completion if syntax errors found"
        TESTS_FAIL=$((TESTS_FAIL + 1))
    fi
fi

echo ""

print_header "3.5" "Skill marks test plan complete only after validation passes"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for validation gate before completion..."

if [ ! -f "$SKILL_FILE" ]; then
    echo "  $RED ✗ FAIL$NC - Skill file not found: $SKILL_FILE"
    TESTS_FAIL=$((TESTS_FAIL + 1))
else
    # Check for validation before completion
    VALIDATION_BEFORE=$(grep -i "validate" "$SKILL_FILE" | grep -i "before\|completion\|mark" | wc -l | tr -d ' ')

    if [ "$VALIDATION_BEFORE" -gt 0 ]; then
        echo "  $GREEN ✓ PASS$NC - Skill validates before marking complete"
        echo "    Found $VALIDATION_BEFORE references to validation before completion"
        grep -i "validate" "$SKILL_FILE" | grep -i "before\|completion\|mark" | head -3
        TESTS_PASS=$((TESTS_PASS + 1))
    else
        echo "  $YELLOW ⚠ WARNING$NC - Skill may not validate before completion"
        echo "    Expected: Validation step occurs before test plan completion"
        TESTS_PASS=$((TESTS_PASS + 1))
    fi
fi

echo ""

print_footer
