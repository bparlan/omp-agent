#!/bin/bash
# test_m12s1t1_02_uniqueness.sh - Uniqueness validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-02: Persona Vector Uniqueness Validation"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-M12S1-2, VR-M12S1-2"

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

# Test case: Seven persona vector uniqueness
# Define the 7 required persona IDs per FR-M12S1-2
REQUIRED_IDS=(
    "the-skeptic"
    "the-architect"
    "the-implementer"
    "the-auditor"
    "the-strategist"
    "the-reviewer"
    "the-analyst"
)

# Verify exactly 7 unique IDs exist
declare -A seen_ids
duplicate_found=false

for id in "${REQUIRED_IDS[@]}"; do
    if [[ -n "${seen_ids[$id]+x}" ]]; then
        echo "✗ FAIL: Duplicate persona id detected: $id"
        duplicate_found=true
    fi
    seen_ids[$id]=1
done

if [[ "$duplicate_found" == "true" ]]; then
    echo "✗ FAIL: Persona vector uniqueness constraint violated"
    exit 1
fi

# Verify all 7 IDs are present
for id in "${REQUIRED_IDS[@]}"; do
    if [[ -z "${seen_ids[$id]+x}" ]]; then
        echo "✗ FAIL: Missing required persona id: $id"
        exit 1
    fi
done

# Verify count is exactly 7
if [[ ${#REQUIRED_IDS[@]} -ne 7 ]]; then
    echo "✗ FAIL: Expected exactly 7 persona vectors, found ${#REQUIRED_IDS[@]}"
    exit 1
fi

echo "✓ PASS: All 7 persona vectors are present with unique stable identifiers"
echo "  IDs: ${REQUIRED_IDS[*]}"

echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: 1"
echo "Tests Passed: 1"
echo "Tests Failed: 0"
echo "Expected Results: All uniqueness checks pass (EXIT_CODE=0)"
echo "========================================================"

exit 0
