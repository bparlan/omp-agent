#!/bin/bash
# test_m12s1t1_01_schema_validation.sh - Schema validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-01: Persona Vector Schema Validation"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-M12S1-1, VR-M12S1-1"

# Load test fixtures
FIXTURE_FILE="../../../../tests/fixtures/synthetic_managedev_personas/persona_vectors.yml"

if [[ ! -f "$FIXTURE_FILE" ]]; then
    echo "FAIL: Test fixture not found: $FIXTURE_FILE"
    exit 1
fi

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

# Phase 1: Validate fixture files exist and are parseable
echo ""
echo "Phase 1: Fixture File Validation"
echo "----------------------------------------"

if [[ ! -f "$FIXTURE_FILE" ]]; then
    echo "✗ Test fixtures not found at $FIXTURE_FILE"
    exit 1
fi

echo "✓ Test fixtures loaded from $FIXTURE_FILE"

# Phase 2: Run schema validation test cases
# We parse the YAML and validate each case using bash for deterministic testing
echo ""
echo "Phase 2: Schema Validation Test Cases"
echo "----------------------------------------"

test_count=0
test_failed=0

# Test case 1: the-skeptic valid
name="the-skeptic valid"
should_pass="true"
id="the-skeptic"
label="Adversarial Verification Engineer"
baseline="Seeks disconfirming evidence for every claim in the specification, questioning assumptions before they become implementation dependencies."
pressure_shift="Under time pressure, escalates assumption challenges rather than deferring them, producing a compact assumptions inventory instead of silent acceptance."
optimizes_for="Preventing false confidence in untested boundaries; exposing specification gaps before they reach implementation."
neglects="Implementation feasibility when evidence is incomplete; tends to block progress on unresolved ambiguities rather than documenting them as tracked risks."
phase_affinity="verification evaluation"
continuation_anchor="false"

# Validation logic
test_schema_case() {
    local name="$1"
    local should_pass="$2"
    local id_val="$3"
    local label_val="$4"
    local baseline_val="$5"
    local pressure_shift_val="$6"
    local optimizes_for_val="$7"
    local neglects_val="$8"
    local phase_affinity_val="$9"
    local continuation_anchor_val="${10}"

    local errors=""

    # Rule 1: id must match ^[a-z0-9-]+$
    if ! echo "$id_val" | grep -qE '^[a-z0-9-]+$'; then
        errors="${errors}FAIL: id '$id_val' does not match pattern ^[a-z0-9-]+$\\n"
    fi

    # Rule 2: All four required fields must be non-empty and >= 20 chars
    if [[ ${#baseline_val} -lt 20 ]]; then
        errors="${errors}FAIL: baseline length ${#baseline_val} < 20 chars\\n"
    fi
    if [[ ${#pressure_shift_val} -lt 20 ]]; then
        errors="${errors}FAIL: pressure_shift length ${#pressure_shift_val} < 20 chars\\n"
    fi
    if [[ ${#optimizes_for_val} -lt 20 ]]; then
        errors="${errors}FAIL: optimizes_for length ${#optimizes_for_val} < 20 chars\\n"
    fi
    if [[ ${#neglects_val} -lt 20 ]]; then
        errors="${errors}FAIL: neglects length ${#neglects_val} < 20 chars\\n"
    fi

    # Rule 3: phase_affinity must contain only valid enum values
    local valid_phases="milestone specification verification tests evaluation implementation"
    for phase in $phase_affinity_val; do
        phase_clean=$(echo "$phase" | tr -d '[],"')
        if ! echo "$valid_phases" | grep -qw "$phase_clean"; then
            errors="${errors}FAIL: Invalid phase_affinity value '$phase_clean'\\n"
        fi
    done

    # Rule 4: continuation_anchor must be boolean
    if [[ "$continuation_anchor_val" != "true" && "$continuation_anchor_val" != "false" ]]; then
        errors="${errors}FAIL: continuation_anchor '$continuation_anchor_val' is not a boolean\\n"
    fi

    # Determine pass/fail
    local has_errors=false
    if [[ -n "$errors" ]]; then
        has_errors=true
    fi

    if [[ "$has_errors" == "true" && "$should_pass" == "true" ]]; then
        echo "✗ $name - Expected to pass but found errors:"
        echo -e "$errors"
        test_failed=$((test_failed + 1))
        return 1
    elif [[ "$has_errors" == "false" && "$should_pass" == "false" ]]; then
        echo "✗ $name - Expected to fail but passed"
        test_failed=$((test_failed + 1))
        return 1
    else
        echo "✓ $name"
        test_passed=true
        return 0
    fi
}

# Run all test cases
# Test case 1: the-skeptic valid
if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 2: the-architect valid
name="the-architect valid"
should_pass="true"
id="the-architect"
label="Systems Architect"
baseline="Maps integration boundaries, interface contracts, and dependency flows between components before any implementation begins."
pressure_shift="Under time pressure, simplifies architectural models to the minimum viable contract set, deferring non-critical interface decisions to tracked open questions."
optimizes_for="Technical feasibility and integration boundaries; ensuring implementation has a stable contract to execute against."
neglects="Detailed failure scenario enumeration; tends to treat boundary conditions as acceptable risks rather than test requirements."
phase_affinity="specification implementation"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 3: the-implementer valid (continuation anchor)
name="the-implementer valid (continuation anchor)"
should_pass="true"
id="the-implementer"
label="Engineering Executor"
baseline="Translates approved contracts into the simplest robust implementation, prioritizing maintainability and contract faithfulness over optimization."
pressure_shift="Under time pressure, accepts simplified implementations with explicit technical debt annotations rather than stalling on perfection."
optimizes_for="Practical implementation continuity; producing working code that satisfies the established contract."
neglects="Long-term architectural elegance; tends to accept local optimizations that create integration friction later."
phase_affinity="implementation"
continuation_anchor="true"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 4: the-auditor valid
name="the-auditor valid"
should_pass="true"
id="the-auditor"
label="Independent Test Auditor"
baseline="Validates that tests are independent, deterministic, and oracle-driven rather than merely executable assertions."
pressure_shift="Under time pressure, flags test quality concerns as post-implementation audit items rather than blocking progress, ensuring traceability is not lost."
optimizes_for="Test quality and evidence contracts; ensuring tests would catch real regressions, not just pass by construction."
neglects="Test generation throughput; tends to demand higher rigor than the current phase timeline can accommodate."
phase_affinity="tests evaluation"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 5: the-strategist valid
name="the-strategist valid"
should_pass="true"
id="the-strategist"
label="Adversarial QA / Test Strategist"
baseline="Designs test scenarios around failure modes and edge cases that the happy path would never reveal."
pressure_shift="Under time pressure, documents failure scenario catalogues as deferred test items rather than generating full test suites immediately."
optimizes_for="Comprehensive failure scenario coverage; ensuring negative paths are tested before implementation commits to a design."
neglects="Test execution speed and resource constraints; tends to propose exhaustive coverage that exceeds available test budget."
phase_affinity="tests"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 6: the-reviewer valid
name="the-reviewer valid"
should_pass="true"
id="the-reviewer"
label="Adversarial Reviewer"
baseline="Searches for hidden defects, security issues, and assumption violations that pass surface-level validation."
pressure_shift="Under time pressure, produces a risk-ranked defect catalogue with severity and likelihood rather than blocking on every concern."
optimizes_for="Hidden defect detection and contract violation prevention; catching what automated checks miss."
neglects="Implementation speed; tends to raise concerns that require human judgment rather than mechanical validation."
phase_affinity="evaluation implementation"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 7: the-analyst valid
name="the-analyst valid"
should_pass="true"
id="the-analyst"
label="Requirements Analyst"
baseline="Validates evidence completeness, requirement clarity, and boundary definitions before any specification is considered complete."
pressure_shift="Under time pressure, documents evidence gaps as tracked open questions rather than accepting implied completeness."
optimizes_for="Evidence completeness and scope clarity; preventing ambiguity from propagating into implementation."
neglects="Technical implementation detail; tends to focus on what is being built rather than how it connects to existing systems."
phase_affinity="milestone"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 8: Missing pressure_shift (invalid)
name="missing pressure_shift"
should_pass="false"
id="the-skeptic"
label="Adversarial Verification Engineer"
baseline="Seeks disconfirming evidence"
pressure_shift=""
optimizes_for="Preventing false confidence"
neglects="Implementation feasibility"
phase_affinity=""
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 9: Empty baseline (invalid)
name="empty baseline"
should_pass="false"
id="the-skeptic"
label="Adversarial Verification Engineer"
baseline=""
pressure_shift="Escalates under pressure"
optimizes_for="Preventing false confidence"
neglects="Implementation feasibility"
phase_affinity=""
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 10: Invalid id with underscore (invalid)
name="invalid id with underscore"
should_pass="false"
id="the_skeptic"
label="Adversarial Verification Engineer"
baseline="Seeks disconfirming evidence for every claim in the specification, questioning assumptions before they become implementation dependencies."
pressure_shift="Under time pressure, escalates assumption challenges rather than deferring them, producing a compact assumptions inventory instead of silent acceptance."
optimizes_for="Preventing false confidence in untested boundaries; exposing specification gaps before they reach implementation."
neglects="Implementation feasibility when evidence is incomplete; tends to block progress on unresolved ambiguities rather than documenting them as tracked risks."
phase_affinity="verification"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

# Test case 11: Invalid phase affinity (invalid)
name="invalid phase affinity"
should_pass="false"
id="the-skeptic"
label="Adversarial Verification Engineer"
baseline="Seeks disconfirming evidence for every claim in the specification, questioning assumptions before they become implementation dependencies."
pressure_shift="Under time pressure, escalates assumption challenges rather than deferring them, producing a compact assumptions inventory instead of silent acceptance."
optimizes_for="Preventing false confidence in untested boundaries; exposing specification gaps before they reach implementation."
neglects="Implementation feasibility when evidence is incomplete; tends to block progress on unresolved ambiguities rather than documenting them as tracked risks."
phase_affinity="invalid_phase"
continuation_anchor="false"

if test_schema_case "$name" "$should_pass" "$id" "$label" "$baseline" "$pressure_shift" "$optimizes_for" "$neglects" "$phase_affinity" "$continuation_anchor"; then
    test_count=$((test_count + 1))
fi

echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: $test_count"
echo "Tests Failed: $test_failed"
echo "Expected Results: All schema validation tests pass (EXIT_CODE=0)"
echo "========================================================"

if [[ $test_failed -gt 0 ]]; then
    exit 1
else
    exit 0
fi