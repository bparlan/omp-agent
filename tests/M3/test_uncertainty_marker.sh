#!/bin/bash
# M3S2 — FR-1: Uncertainty Marker (#NEEDS-CLARIFICATION)
# Verifies that the literal grep-able marker is codified in:
#   docs/FRAMEWORK.md  AGENTS.md  skills/implement-specification/SKILL.md
# Usage: ./tests/M3/test_uncertainty_marker.sh

set -euo pipefail
FAILED=0

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

echo "=== FR-1: Uncertainty Marker (#NEEDS-CLARIFICATION) ==="

# --- Test 1: grep for marker in each target file ---
for f in docs/FRAMEWORK.md AGENTS.md skills/implement-specification/SKILL.md; do
    if [ ! -f "$f" ]; then
        echo "  SKIP: $f not found (not yet implemented)"
        continue
    fi
    if grep -qF '#NEEDS-CLARIFICATION' "$f"; then
        report_pass "$f contains #NEEDS-CLARIFICATION"
    else
        report_fail "$f does NOT contain #NEEDS-CLARIFICATION"
    fi
done

# --- Test 2: FRAMEWORK.md has "The Uncertainty Marker" section ---
if [ -f docs/FRAMEWORK.md ]; then
    if grep -qE '\- ### The Uncertainty Marker|## The Uncertainty Marker' docs/FRAMEWORK.md; then
        report_pass "FRAMEWORK.md has 'The Uncertainty Marker' section"
    else
        report_fail "FRAMEWORK.md missing 'The Uncertainty Marker' section heading"
    fi

    # Check that the section is between Spec-Driven Development and Agent-Tool Separation
    sdd_line=$(grep -n 'Spec-Driven Development' docs/FRAMEWORK.md | head -1 | cut -d: -f1)
    marker_line=$(grep -n 'The Uncertainty Marker' docs/FRAMEWORK.md | head -1 | cut -d: -f1)
    ats_line=$(grep -n 'Agent-Tool Separation' docs/FRAMEWORK.md | head -1 | cut -d: -f1)

    if [ -n "$sdd_line" ] && [ -n "$marker_line" ] && [ -n "$ats_line" ]; then
        if [ "$sdd_line" -lt "$marker_line" ] && [ "$marker_line" -lt "$ats_line" ]; then
            report_pass "Uncertainty Marker section positioned correctly (SDD < Marker < ATS)"
        else
            report_fail "Uncertainty Marker section NOT between SDD and Agent-Tool Separation (SDD=$sdd_line Marker=$marker_line ATS=$ats_line)"
        fi
    else
        report_fail "Could not locate all three section markers"
    fi
fi

# --- Test 3: AGENTS.md has the Uncertainty Marker rule ---
if [ -f AGENTS.md ]; then
    if grep -q 'HALT\|halt\|must.*stop\|MUST.*stop' <(grep -A5 -B2 '#NEEDS-CLARIFICATION' AGENTS.md 2>/dev/null); then
        report_pass "AGENTS.md has HALT/stop rule associated with the marker"
    else
        # Check broader presence
        ag_ctx=$(grep -cF '#NEEDS-CLARIFICATION' AGENTS.md || true)
        if [ "$ag_ctx" -gt 0 ]; then
            report_fail "AGENTS.md has #NEEDS-CLARIFICATION but no HALT/stop rule found nearby"
        else
            report_fail "AGENTS.md has no #NEEDS-CLARIFICATION marker at all"
            fi
    fi
fi

# --- Test 4: implement-specification SKILL.md has marker in "When uncertain" ---
if [ -f skills/implement-specification/SKILL.md ]; then
    if grep -q '#NEEDS-CLARIFICATION' skills/implement-specification/SKILL.md; then
        report_pass "implement-specification/SKILL.md references #NEEDS-CLARIFICATION"
    else
        report_fail "implement-specification/SKILL.md missing #NEEDS-CLARIFICATION reference"
    fi
fi

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-1 PASSED"
else
    echo "RESULT: FR-1 FAILED"
fi
exit "$FAILED"