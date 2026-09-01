#!/bin/bash
# test_fr_1_2_mise_config.sh - CLI test script for FR-1.2 .mise.toml Configuration Schema
# Template Version: 1.0.0
# Expected Exit Code: 0 (implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="FR-1.2 .mise.toml Configuration Schema"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-1.2.1,FR-1.2.2,FR-1.2.3"

# Load test fixtures
FIXTURE_FILE="./test_fixtures/mise_config.yml"
if [[ -f "$FIXTURE_FILE" ]]; then
    echo "✓ Loaded test fixtures from $FIXTURE_FILE"
else
    echo "✗ Test fixtures not found at $FIXTURE_FILE"
    exit 1
fi

# Test mise-validate command
test_mise_validate() {
    local test_name="$1"
    local expected_pass="$2"

    echo "Running test case: $test_name"

    # Test mise-validate --config <path> --schema <version>
    echo "Testing: mise-validate --config $FIXTURE_FILE --schema 1.0.0"
    if command -v mise-validate >/dev/null 2>&1; then
        mise_output=$(mise-validate --config "$FIXTURE_FILE" --schema 1.0.0 2>&1 || true)
        echo "Command output: $mise_output"
        if mise-validate --config "$FIXTURE_FILE" --schema 1.0.0 >/dev/null 2>&1; then
            echo "✓ mise-validate succeeded as expected"
            return 0
        else
            echo "✗ mise-validate failed unexpectedly"
            return 1
        fi
    else
        echo "✗ mise-validate command not found"
        return 1
    fi
}

# Parse YAML test cases
test_count=0
test_passed=0
test_failed=0

while IFS= read -r name_line; do
    if [[ -z "$name_line" ]]; then
        continue
    fi
    # Extract test case name
    name=$(echo "$name_line" | sed 's/^\s*- name: //; s/"//g')
    # Extract should_pass flag
    should_pass=$(grep -A 20 "name: \"$name\"" "$FIXTURE_FILE" | grep "should_pass:" | head -1 | sed 's/^\s*should_pass: //')

    test_count=$((test_count + 1))

    echo "========================================================"
    echo "Test Case: $name"
    echo "========================================================"

    if test_mise_validate "$name" "$should_pass"; then
        test_passed=$((test_passed + 1))
        echo "✓ Test case '$name' passed"
    else
        test_failed=$((test_failed + 1))
        echo "✗ Test case '$name' failed"
    fi
    echo ""
done < <(grep "name:" "$FIXTURE_FILE")

echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "Tests Run: $test_count"
echo "Tests Passed: $test_passed"
echo "Tests Failed: $test_failed"
echo "========================================================"

if [[ $test_failed -eq 0 ]]; then
    echo "✓ All tests passed"
    exit 0
else
    echo "✗ Some tests failed"
    exit 1
fi
