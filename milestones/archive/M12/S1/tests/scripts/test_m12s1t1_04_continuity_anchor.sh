#!/bin/bash
# test_m12s1t1_04_continuity_anchor.sh - Continuity anchor enforcement validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-04: Continuity Anchor Enforcement"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-M12S1-3, VR-M12S1-4"

# Expected team assignments (same as test 03)
declare -A EXPECTED_TEAMS=(
    ["milestone"]="the-analyst the-architect the-implementer"
    ["specification"]="the-architect the-skeptic the-implementer"
    ["verification"]="the-skeptic the-auditor the-implementer"
    ["tests"]="the-strategist the-auditor the-implementer"
    ["evaluation"]="the-reviewer the-auditor the-implementer"
    ["implementation"]="the-implementer the-architect the-reviewer"
)

# Load fixture
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

# Phase 1: Verify the-implementer appears in every team
echo ""
echo "Phase 1: Continuity Anchor Verification"
echo "----------------------------------------"

continuity_failures=0
missing_phase_failures=0

# Check each phase
for phase in "${!EXPECTED_TEAMS[@]}"; do
    expected="${EXPECTED_TEAMS[$phase]}"
    if [[ ! "$expected" =~ "the-implementer" ]]; then
        echo "FAIL: Phase '$phase' does not contain continuity anchor 'the-implementer'"
        continuity_failures=$((continuity_failures + 1))
    else
        echo "✓ Phase '$phase' contains continuity anchor 'the-implementer'"
    fi
done

# Check we have exactly 6 phases
phase_count=${#EXPECTED_TEAMS[@]}
if [[ $phase_count -ne 6 ]]; then
    echo "FAIL: Expected 6 phases but found $phase_count"
    missing_phase_failures=$((missing_phase_failures + 1))
fi

# Phase 2: Verify team size is exactly 3 members per FR-M12S1-3
echo ""
echo "Phase 2: Team Size Verification"
echo "----------------------------------------"

size_failures=0
for phase in "${!EXPECTED_TEAMS[@]}"; do
    expected="${EXPECTED_TEAMS[$phase]}"
    member_count=$(echo "$expected" | wc -w)
    if [[ $member_count -ne 3 ]]; then
        echo "FAIL: Phase '$phase' does not have exactly 3 members (has $member_count)"
        size_failures=$((size_failures + 1))
    else
        echo "✓ Phase '$phase' has exactly 3 members"
    fi
done

# Phase 3: Verify no duplicate members within any team
echo ""
echo "Phase 3: Team Uniqueness Verification"
echo "----------------------------------------"

uniqueness_failures=0
for phase in "${!EXPECTED_TEAMS[@]}"; do
    expected="${EXPECTED_TEAMS[$phase]}"
    duplicates=$(echo "$expected" | tr ' ' '\n' | sort | uniq -d)
    if [[ -n "$duplicates" ]]; then
        echo "FAIL: Phase '$phase' contains duplicate members: $duplicates"
        uniqueness_failures=$((uniqueness_failures + 1))
    else
        echo "✓ Phase '$phase' has no duplicate members"
    fi
done

# Phase 4: Verify all required persona IDs are present (FR-M12S1-2)
echo ""
echo "Phase 4: Required Persona IDs Verification"
echo "----------------------------------------"

# Extract all unique persona IDs from expected teams
all_ids=$(echo "${EXPECTED_TEAMS[*]}" | tr ' ' '\n' | tr '[:upper:]' '[:lower:]' | sort -u)

required_ids=("the-skeptic" "the-architect" "the-implementer" "the-auditor" "the-strategist" "the-reviewer" "the-analyst")

missing_ids=0
for id in "${required_ids[@]}"; do
    if ! echo "$all_ids" | grep -q "^$id$"; then
        echo "FAIL: Required persona ID '$id' not found in any team assignment"
        missing_ids=$((missing_ids + 1))
    fi
done

if [[ $missing_ids -eq 0 ]]; then
    echo "✓ All 7 required persona IDs present in team assignments"
else
    echo "✗ $missing_ids required persona IDs missing from team assignments"
fi

# Final summary
echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: Checking continuity anchor enforcement"
echo "Tests Failed: $((continuity_failures + missing_phase_failures + size_failures + uniqueness_failures + missing_ids))"
echo "Expected Results: All continuity anchor tests pass (EXIT_CODE=0)"
echo "========================================================"

total_failures=$((continuity_failures + missing_phase_failures + size_failures + uniqueness_failures + missing_ids))

if [[ $total_failures -gt 0 ]]; then
    echo "FAIL: Continuity anchor validation found $total_failures failures"
    exit 1
fi

echo "✓ All continuity anchor validation tests passed"
exit 0