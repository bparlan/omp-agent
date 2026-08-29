#!/bin/bash
# run_cli_tests.sh - Master test runner for M11S1 Environment Layer CLI contracts
# Template Version: 1.0.0
# Expected Exit Code: 1 (baseline failure until implementation)

set -euo pipefail

# Configuration
TEMPLATE_VERSION="1.0.0"
TEST_SUITE="M11S1 Environment / Reproducibility Layer - CLI Execution Contracts"
EXPECTED_EXIT_CODE=1

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test arrays - matches active ledger M11S1T1.md
CLI_TESTS=(
    "test_fr_1_1_env_management.sh"
    "test_fr_1_2_mise_config.sh"
    "test_fr_1_3_env_detection.sh"
    "test_fr_1_4_workspace_isolation.sh"
    "test_fr_1_5_cross_language_runtime.sh"
)

echo "========================================================"
echo "Test Suite: $TEST_SUITE"
echo "Template Version: $TEMPLATE_VERSION"
echo "Expected Exit Code: $EXPECTED_EXIT_CODE (baseline)"
echo "========================================================"
echo ""

# Run each test script
total_tests=0
total_passed=0
total_failed=0

for test_script in "${CLI_TESTS[@]}"; do
    test_file=$(basename "$test_script")
    total_tests=$((total_tests + 1))

    echo "----------------------------------------"
    echo "Running: $test_file"
    echo "----------------------------------------"

    if [[ ! -f "$test_script" ]]; then
        echo "✗ Test script not found: $test_script"
        total_failed=$((total_failed + 1))
        continue
    fi

    if [[ ! -x "$test_script" ]] && ! bash -n "$test_script" 2>/dev/null; then
        echo "✗ Test script syntax error: $test_script"
        total_failed=$((total_failed + 1))
        continue
    fi

    # Execute test - capture exit code
    set +e
    bash "$test_script" 2>&1
    exit_code=$?
    set -e

    if [[ $exit_code -eq $EXPECTED_EXIT_CODE ]]; then
        echo "✓ $test_file exited with expected code: $exit_code"
        total_failed=$((total_failed + 1))
    else
        echo "✗ $test_file unexpected exit code: $exit_code (expected $EXPECTED_EXIT_CODE)"
        total_failed=$((total_failed + 1))
    fi
    echo ""
done

echo "========================================================"
echo "Test Execution Summary"
echo "Template Version: $TEMPLATE_VERSION"
echo "Total Test Scripts: $total_tests"
echo "Tests with Expected Exit Code: $total_failed"
echo "Expected Results: All tests fail (EXIT_CODE=$EXPECTED_EXIT_CODE) - baseline behavior"
echo "========================================================"
exit 1