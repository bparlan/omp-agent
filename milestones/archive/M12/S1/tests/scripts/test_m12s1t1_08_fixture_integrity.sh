#!/bin/bash
# test_m12s1t1_08_fixture_integrity.sh - Synthetic fixture integrity validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-08: Synthetic Fixture Integrity"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="All (fixture completeness)"

# Check all required fixture files
FIXTURE_DIR="../../../tests/fixtures/synthetic_managedev_personas"
REQUIRED_FILES=(
    "persona_vectors.yml"
    "phase_team_assignments.yml"
    "consolidation_report_golden.md"
    "skills_ledger_expected.json"
    "baseline_process_section.md"
)

if [[ ! -d "$FIXTURE_DIR" ]]; then
    echo "FAIL: Fixture directory not found: $FIXTURE_DIR"
    exit 1
fi

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

PASS_COUNT=0
FAIL_COUNT=0

# Check all required fixture files exist
for file in "${REQUIRED_FILES[@]}"; do
    path="$FIXTURE_DIR/$file"
    if [[ -f "$path" ]]; then
        echo "PASS: Fixture file exists: $file"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "FAIL: Fixture file missing: $file"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done

# Verify persona_vectors.yml is parseable YAML (contains expected structure)
if grep -q 'persona_vector_validation' "$FIXTURE_DIR/persona_vectors.yml" && \
   grep -q 'test_cases' "$FIXTURE_DIR/persona_vectors.yml"; then
    echo "PASS: persona_vectors.yml has expected structure"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: persona_vectors.yml missing expected structure"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Verify skills_ledger_expected.json is valid JSON
if python3 -c "import json; json.load(open('$FIXTURE_DIR/skills_ledger_expected.json'))" 2>/dev/null; then
    echo "PASS: skills_ledger_expected.json is valid JSON"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: skills_ledger_expected.json is not valid JSON"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Verify consolidation_report_golden.md contains required sections
if grep -q 'Team Consolidation Report' "$FIXTURE_DIR/consolidation_report_golden.md" && \
   grep -q 'Team Commentary' "$FIXTURE_DIR/consolidation_report_golden.md" && \
   grep -q 'Consensus Recommendation' "$FIXTURE_DIR/consolidation_report_golden.md"; then
    echo "PASS: consolidation_report_golden.md contains required sections"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: consolidation_report_golden.md missing required sections"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# Verify baseline_process_section.md contains process section marker
if grep -q '#### 2. Your Process' "$FIXTURE_DIR/baseline_process_section.md"; then
    echo "PASS: baseline_process_section.md contains process section"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo "FAIL: baseline_process_section.md missing process section"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""
echo "========================================================"
echo "Test Execution Summary for $TEST_NAME"
echo "Tests Run: $((PASS_COUNT + FAIL_COUNT))"
echo "Tests Passed: $PASS_COUNT"
echo "Tests Failed: $FAIL_COUNT"
echo "Expected Results: All fixture integrity checks pass (EXIT_CODE=0)"
echo "========================================================"

if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
else
    exit 0
fi
