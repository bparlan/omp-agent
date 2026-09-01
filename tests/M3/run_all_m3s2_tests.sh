#!/bin/bash
# M3S2 — Test Suite Runner
# Runs all 6 FR test scripts and reports summary.
# Usage: ./tests/M3/run_all_m3s2_tests.sh

set -euo pipefail

TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PASSED=0
FAILED=0
TOTAL=0
FAILED_TESTS=""

echo "=============================================="
echo "  M3S2 — The Mechanism: Test Suite Runner"
echo "=============================================="
echo ""

run_test() {
    local script="$1"
    local name="$2"
    TOTAL=$((TOTAL + 1))

    echo ""
    echo "----------------------------------------------"
    echo "  Running: $name"
    echo "  Script: $script"
    echo "----------------------------------------------"

    if [ ! -f "$script" ]; then
        echo "  SKIP: $script not found"
        return
    fi

    if "$script"; then
        PASSED=$((PASSED + 1))
        echo ""
        echo "  >>> $name: PASS <<<"
    else
        FAILED=$((FAILED + 1))
        FAILED_TESTS="$FAILED_TESTS $name"
        echo ""
        echo "  >>> $name: FAIL <<<"
    fi
}

cd "$TESTS_DIR/../.."

run_test "$TESTS_DIR/test_uncertainty_marker.sh" "FR-1: Uncertainty Marker"
run_test "$TESTS_DIR/test_zero_trust_review.sh" "FR-2: Zero-Trust Review"
run_test "$TESTS_DIR/test_evidence_debugging.sh" "FR-3: Evidence-Based Debugging"
run_test "$TESTS_DIR/test_raw_evidence_mandate.sh" "FR-4: Raw Evidence Mandate"
run_test "$TESTS_DIR/test_ground_truth_helper.sh" "FR-5: Ground-Truth Helper"
run_test "$TESTS_DIR/test_tooling_stack.sh" "FR-6: Mechanical Tooling Stack"

echo ""
echo "=============================================="
echo "  M3S2 Test Summary"
echo "=============================================="
echo "  Total:  $TOTAL"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
if [ -n "$FAILED_TESTS" ]; then
    echo "  Failed tests:$FAILED_TESTS"
fi
echo "=============================================="

exit "$FAILED"
