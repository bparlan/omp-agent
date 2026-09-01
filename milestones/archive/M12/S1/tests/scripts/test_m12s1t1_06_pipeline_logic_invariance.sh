#!/bin/bash
# test_m12s1t1_06_pipeline_logic_invariance.sh - Pipeline logic invariance validation test runner for M12S1
# Template Version: 1.0.0
# Expected Exit Code: 0 (all tests pass when implementation complete)

set -euo pipefail

# Test configuration
TEST_NAME="M12S1T1-06: Pipeline Logic Invariance"
TEMPLATE_VERSION="1.0.0"
REQUIREMENTS_COVER="FR-M12S1-5, VR-M12S1-6"

# Expected: pipeline section should be byte-identical to baseline
# The baseline process section is in tests/fixtures/synthetic_managedev_personas/baseline_process_section.md
BASELINE_FILE="../../../tests/fixtures/synthetic_managedev_personas/baseline_process_section.md"

if [[ ! -f "$BASELINE_FILE" ]]; then
    echo "FAIL: Baseline file not found: $BASELINE_FILE"
    exit 1
fi

echo "========================================================"
echo "Running: $TEST_NAME"
echo "Template Version: $TEMPLATE_VERSION"
echo "Requirements Covered: $REQUIREMENTS_COVER"
echo "========================================================"

# Extract the process section from SKILL.md (lines starting with "#### 2.")
echo ""
echo "Phase 1: Extract Pipeline Process Section"
echo "----------------------------------------"

cat > /tmp/extracted_process_section.md << 'EXT'
$(grep -A 200 "^#### 2\." /Users/bparlan/devcode/aef/agent/skills/manage-development/SKILL.md | head -200)
EXT

# Remove the ">>" prefix from extracted lines
echo "Extracted $(wc -l < /tmp/extracted_process_section.md) lines from SKILL.md process section"

# Phase 2: Compare with baseline
echo ""
echo "Phase 2: Byte-Identity Comparison with Baseline"
echo "----------------------------------------"

# Generate baseline file without the initial indicator
head -n -1 "$BASELINE_FILE" > /tmp/baseline_clean.md

# Add newline to both files for comparison
tail -n +2 /tmp/extracted_process_section.md > /tmp/extracted_clean.md

tail -n +2 "$BASELINE_FILE" > /tmp/baseline_tail.md

# Compare ignoring whitespace
echo "Comparing pipeline process sections..."
if diff -w /tmp/extracted_clean.md /tmp/baseline_tail.md > /tmp/diff_output 2>&1; then
    echo "✓ Pipeline process section is byte-identical to baseline"
    echo "✓ Pipeline logic invariance validation PASSED"
    exit 0
else
    echo "FAIL: Pipeline process section differs from baseline"
    echo "Diff output:"
    cat /tmp/diff_output
    exit 1
fi
