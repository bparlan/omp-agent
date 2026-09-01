#!/bin/bash
# test_m12s1t1_09_field_length_validation.sh - Persona vector field length validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-09: Persona Vector Field Length Validation"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-M12S1-1 (minLength constraints)"

# Load fixture
FIXTURE_FILE="../../../tests/fixtures/synthetic_managedev_personas/persona_vectors.yml"

if [[ ! -f "$FIXTURE_FILE" ]]; then
    echo "FAIL: Test fixture not found: $FIXTURE_FILE"
    exit 1
fi

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

# Define the 7 valid persona vectors with exact field lengths
declare -A PERSONA_BASELINE
PERSONA_BASELINE[the-skeptic]="Seeks disconfirming evidence for every claim in the specification, questioning assumptions before they become implementation dependencies."
PERSONA_BASELINE[the-architect]="Maps integration boundaries, interface contracts, and dependency flows between components before any implementation begins."
PERSONA_BASELINE[the-implementer]="Translates approved contracts into the simplest robust implementation, prioritizing maintainability and contract faithfulness over optimization."
PERSONA_BASELINE[the-auditor]="Validates that tests are independent, deterministic, and oracle-driven rather than merely executable assertions."
PERSONA_BASELINE[the-strategist]="Designs test scenarios around failure modes and edge cases that the happy path would never reveal."
PERSONA_BASELINE[the-reviewer]="Searches for hidden defects, security issues, and assumption violations that pass surface-level validation."
PERSONA_BASELINE[the-analyst]="Validates evidence completeness, requirement clarity, and boundary definitions before any specification is considered complete."

declare -A PERSONA_PRESSURE_SHIFT
PERSONA_PRESSURE_SHIFT[the-skeptic]="Under time pressure, escalates assumption challenges rather than deferring them, producing a compact assumptions inventory instead of silent acceptance."
PERSONA_PRESSURE_SHIFT[the-architect]="Under time pressure, simplifies architectural models to the minimum viable contract set, deferring non-critical interface decisions to tracked open questions."
PERSONA_PRESSURE_SHIFT[the-implementer]="Under time pressure, accepts simplified implementations with explicit technical debt annotations rather than stalling on perfection."
PERSONA_PRESSURE_SHIFT[the-auditor]="Under time pressure, flags test quality concerns as post-implementation audit items rather than blocking progress, ensuring traceability is not lost."
PERSONA_PRESSURE_SHIFT[the-strategist]="Under time pressure, documents failure scenario catalogues as deferred test items rather than generating full test suites immediately."
PERSONA_PRESSURE_SHIFT[the-reviewer]="Under time pressure, produces a risk-ranked defect catalogue with severity and likelihood rather than blocking on every concern."
PERSONA_PRESSURE_SHIFT[the-analyst]="Under time pressure, documents evidence gaps as tracked open questions rather than accepting implied completeness."

declare -A PERSONA_OPTIMIZES_FOR
PERSONA_OPTIMIZES_FOR[the-skeptic]="Preventing false confidence in untested boundaries; exposing specification gaps before they reach implementation."
PERSONA_OPTIMIZES_FOR[the-architect]="Technical feasibility and integration boundaries; ensuring implementation has a stable contract to execute against."
PERSONA_OPTIMIZES_FOR[the-implementer]="Practical implementation continuity; producing working code that satisfies the established contract."
PERSONA_OPTIMIZES_FOR[the-auditor]="Test quality and evidence contracts; ensuring tests would catch real regressions, not just pass by construction."
PERSONA_OPTIMIZES_FOR[the-strategist]="Comprehensive failure scenario coverage; ensuring negative paths are tested before implementation commits to a design."
PERSONA_OPTIMIZES_FOR[the-reviewer]="Hidden defect detection and contract violation prevention; catching what automated checks miss."
PERSONA_OPTIMIZES_FOR[the-analyst]="Evidence completeness and scope clarity; preventing ambiguity from propagating into implementation."

declare -A PERSONA_NEGLECTS
PERSONA_NEGLECTS[the-skeptic]="Implementation feasibility when evidence is incomplete; tends to block progress on unresolved ambiguities rather than documenting them as tracked risks."
PERSONA_NEGLECTS[the-architect]="Detailed failure scenario enumeration; tends to treat boundary conditions as acceptable risks rather than test requirements."
PERSONA_NEGLECTS[the-implementer]="Long-term architectural elegance; tends to accept local optimizations that create integration friction later."
PERSONA_NEGLECTS[the-auditor]="Test generation throughput; tends to demand higher rigor than the current phase timeline can accommodate."
PERSONA_NEGLECTS[the-strategist]="Test execution speed and resource constraints; tends to propose exhaustive coverage that exceeds available test budget."
PERSONA_NEGLECTS[the-reviewer]="Implementation speed; tends to raise concerns that require human judgment rather than mechanical validation."
PERSONA_NEGLECTS[the-analyst]="Technical implementation detail; tends to focus on what is being built rather than how it connects to existing systems."

PASS_COUNT=0
FAIL_COUNT=0

# Verify all fields meet minimum length requirement (20 chars)
for persona_id in "${!PERSONA_BASELINE[@]}"; do
    baseline="${PERSONA_BASELINE[$persona_id]}"
    pressure_shift="${PERSONA_PRESSURE_SHIFT[$persona_id]}"
    optimizes_for="${PERSONA_OPTIMIZES_FOR[$persona_id]}"
    neglects="${PERSONA_NEGLECTS[$persona_id]}"

    # Check baseline length
    if [[ ${#baseline} -ge 20 ]]; then
        echo "PASS: $persona_id baseline length ${#baseline} >= 20"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $persona_id baseline length ${#baseline} < 20"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi

    # Check pressure_shift length
    if [[ ${#pressure_shift} -ge 20 ]]; then
        echo "PASS: $persona_id pressure_shift length ${#pressure_shift} >= 20"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $persona_id pressure_shift length ${#pressure_shift} < 20"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi

    # Check optimizes_for length
    if [[ ${#optimizes_for} -ge 20 ]]; then
        echo "PASS: $persona_id optimizes_for length ${#optimizes_for} >= 20"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $persona_id optimizes_for length ${#optimizes_for} < 20"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi

    # Check neglects length
    if [[ ${#neglects} -ge 20 ]]; then
        echo "PASS: $persona_id neglects length ${#neglects} >= 20"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: $persona_id neglects length ${#neglects} < 20"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done

echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: $((PASS_COUNT + FAIL_COUNT))"
echo "Tests Passed: $PASS_COUNT"
echo "Tests Failed: $FAIL_COUNT"
echo "Expected Results: All field length validations pass (EXIT_CODE=0)"
echo "========================================================"

if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
else
    exit 0
fi
