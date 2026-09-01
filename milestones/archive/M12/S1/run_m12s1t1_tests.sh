#!/bin/bash
# run_m12s1t1_tests.sh - M12S1T1 Test Runner
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Configuration
TEMPLATE_VERSION="1.0.0"
TEST_SUITE="M12S1T1 - Verification Tests for M12S1"
EXPECTED_EXIT_CODE=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test Scripts - matches active ledger M12S1T1.md
test_scripts=(
    "test_m12s1t1_01_schema_validation.sh"
    "test_m12s1t1_02_uniqueness.sh"
    "test_m12s1t1_03_phase_team_assignments.sh"
    "test_m12s1t1_04_continuity_anchor.sh"
    "test_m12s1t1_05_consolidation_report_format.sh"
    "test_m12s1t1_06_pipeline_logic_invariance.sh"
    "test_m12s1t1_07_skills_ledger.sh"
    "test_m12s1t1_08_fixture_integrity.sh"
    "test_m12s1t1_09_field_length_validation.sh"
    "test_m12s1t1_10_phase_affinity.sh"
)

echo "========================================================"
echo "Test Suite: $TEST_SUITE"
echo "Template Version: $TEMPLATE_VERSION"
echo "Expected Exit Code: $EXPECTED_EXIT_CODE (SUCCESS)"
echo "========================================================"
echo ""

# Run each test script
total_tests=0
total_passed=0
total_failed=0

for test_script in "${test_scripts[@]}"; do
    test_file="$test_script"
    total_tests=$((total_tests + 1))

    echo "----------------------------------------"
    echo "Running: $test_file"
    echo "----------------------------------------"

    if [[ ! -f "$test_file" ]]; then
        echo "✗ Test script not found: $test_file"
        total_failed=$((total_failed + 1))
        continue
    fi

    if [[ ! -x "$test_file" ]] && ! bash -n "$test_file" 2>/dev/null; then
        echo "✗ Test script syntax error: $test_file"
        total_failed=$((total_failed + 1))
        continue
    fi

    # Execute test - capture exit code
    set +e
    bash "$test_file" 2>&1
    exit_code=$?
    set -e

    if [[ $exit_code -eq $EXPECTED_EXIT_CODE ]]; then
        echo -e "${GREEN}✓ $test_file exited with expected code: $exit_code${NC}"
        total_passed=$((total_passed + 1))
    else
        echo -e "${RED}✗ $test_file unexpected exit code: $exit_code (expected $EXPECTED_EXIT_CODE)"${NC}
        total_failed=$((total_failed + 1))
    fi
    echo ""
done

echo "========================================================"
echo "Test Execution Summary"
echo "Template Version: $TEMPLATE_VERSION"
echo "Total Test Scripts: $total_tests"
echo "Tests Passed: $total_passed"
echo "Tests Failed: $total_failed"
echo "Expected Results: All tests pass (EXIT_CODE=$EXPECTED_EXIT_CODE)"
echo "========================================================"

if [[ $total_failed -gt 0 ]]; then
    exit 1
else
    exit 0
fi
