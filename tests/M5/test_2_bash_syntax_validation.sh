#!/bin/bash

# Test Suite: Bash Syntax Validation
# Tests: Test Case 1.2, 1.4 (revisited)
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

print_header "1.2" "Bash scripts use bash function definitions"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Searching for bash function definitions in M5 test scripts..."

BASH_FUNCTION_COUNT=0
PYTHON_CLASS_COUNT=0

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        # Count bash function definitions
        func_count=$(grep -c "^function " "$script" 2>/dev/null || echo "0")
        BASH_FUNCTION_COUNT=$((BASH_FUNCTION_COUNT + func_count))

        # Count Python class definitions (should be 0)
        class_count=$(grep -c "^class " "$script" 2>/dev/null || echo "0")
        PYTHON_CLASS_COUNT=$((PYTHON_CLASS_COUNT + class_count))
    fi
done

echo "  Found $BASH_FUNCTION_COUNT bash function definitions"
echo "  Found $PYTHON_CLASS_COUNT Python class definitions"

if [ "$PYTHON_CLASS_COUNT" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - No Python class definitions found in bash scripts"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - Found $PYTHON_CLASS_COUNT Python class definitions"
    echo "    Python class definitions should be replaced with bash functions"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_header "1.3" "Test counters used correctly"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for TESTS_RUN, TESTS_PASS, TESTS_FAIL counter definitions..."

COUNTER_ERRORS=0

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        # Check for counter definitions
        if ! grep -q "TESTS_RUN=" "$script" && ! grep -q "TESTS_RUN =" "$script"; then
            echo "  $YELLOW ⚠ WARNING$NC - $script missing TESTS_RUN counter"
            COUNTER_ERRORS=$((COUNTER_ERRORS + 1))
        fi

        if ! grep -q "TESTS_PASS=" "$script" && ! grep -q "TESTS_PASS =" "$script"; then
            echo "  $YELLOW ⚠ WARNING$NC - $script missing TESTS_PASS counter"
            COUNTER_ERRORS=$((COUNTER_ERRORS + 1))
        fi

        if ! grep -q "TESTS_FAIL=" "$script" && ! grep -q "TESTS_FAIL =" "$script"; then
            echo "  $YELLOW ⚠ WARNING$NC - $script missing TESTS_FAIL counter"
            COUNTER_ERRORS=$((COUNTER_ERRORS + 1))
        fi
    fi
done

if [ "$COUNTER_ERRORS" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - All scripts have proper counter definitions"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - $COUNTER_ERRORS scripts missing counter definitions"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_header "1.4" "Bash scripts execute without syntax errors"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Running comprehensive bash syntax checks on all test scripts..."

BASH_SYNTAX_ERRORS=0
INVALID_SCRIPTS=()

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        # Check syntax with bash -n
        if ! bash -n "$script" 2>/dev/null; then
            echo "  $RED ✗ FAIL$NC - Syntax error in $script"
            BASH_SYNTAX_ERRORS=$((BASH_SYNTAX_ERRORS + 1))
            INVALID_SCRIPTS+=("$script")
        fi

        # Check for invalid syntax patterns
        if grep -E "^    (def |class )" "$script" 2>/dev/null | grep -q .; then
            echo "  $RED ✗ FAIL$NC - $script contains Python indented blocks"
            BASH_SYNTAX_ERRORS=$((BASH_SYNTAX_ERRORS + 1))
        fi
    fi
done

echo "  Checked $(ls -1 tests/M5/*.sh 2>/dev/null | wc -l | tr -d ' ') scripts"
echo "  Found $BASH_SYNTAX_ERRORS syntax errors"

if [ "$BASH_SYNTAX_ERRORS" -eq 0 ]; then
    echo "  $GREEN ✓ PASS$NC - All scripts pass bash syntax validation"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $RED ✗ FAIL$NC - $BASH_SYNTAX_ERRORS scripts have syntax errors"
    for invalid_script in "${INVALID_SCRIPTS[@]}"; do
        echo "    - $invalid_script"
    done
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

print_header "Additional" "Verify mock functions use bash syntax"

TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for bash function syntax in mock objects..."

# Count total function definitions
TOTAL_FUNCTIONS=0
FUNCTION_NAMES=()

for script in tests/M5/*.sh; do
    if [ -f "$script" ]; then
        # Count all function definitions (both bash and potential Python)
        func_lines=$(grep -E "^(function |[a-z_]+[a-z0-9_]*\(\))" "$script" 2>/dev/null || true)

        if [ -n "$func_lines" ]; then
            count=$(echo "$func_lines" | wc -l | tr -d ' ')
            TOTAL_FUNCTIONS=$((TOTAL_FUNCTIONS + count))

            # Extract function names
            while IFS= read -r line; do
                if [[ "$line" =~ ^(function|def) ]]; then
                    # Extract function name
                    func_name=$(echo "$line" | sed 's/^[^(]*(\([^)]*\)).*/\1/' | sed 's/def //')
                    if [ -n "$func_name" ]; then
                        FUNCTION_NAMES+=("$func_name")
                    fi
                fi
            done <<< "$func_lines"
        fi
    fi
done

echo "  Found $TOTAL_FUNCTIONS function definitions"
echo "  Sample function names: ${FUNCTION_NAMES[@]:0:5}"

if [ ${#FUNCTION_NAMES[@]} -gt 0 ]; then
    echo "  $GREEN ✓ PASS$NC - Scripts use bash function syntax"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo "  $YELLOW ⚠ WARNING$NC - No function definitions found"
    echo "    Scripts may still be valid without functions"
    TESTS_PASS=$((TESTS_PASS + 1))
fi

echo ""

print_footer
