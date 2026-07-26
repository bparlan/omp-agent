#!/bin/bash
# M3S2 — FR-2: Zero-Trust Review Pass
# Verifies that review-implementation/SKILL.md and review_template.md
# enforce live-state verification with the zero-trust standing rule.
# Usage: ./tests/M3/test_zero_trust_review.sh

set -euo pipefail
FAILED=0

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

echo "=== FR-2: Zero-Trust Review Pass ==="

# --- Test 1: Standing rule at beginning of review-implementation/SKILL.md ---
skill_file="skills/review-implementation/SKILL.md"
if [ -f "$skill_file" ]; then
    # Extract content after YAML frontmatter (everything after the second --- or ...)
    body=$(awk '/^(---|\.\.\.)/{c++;next} c>=2{print;exit}' "$skill_file" 2>/dev/null || true)
    if [ -z "$body" ]; then
        body=$(tail -n +10 "$skill_file" | head -20)
    fi

    if echo "$body" | grep -qF "Assume the prior report is wrong"; then
        report_pass "SKILL.md has the zero-trust standing rule"
    else
        # Check the whole file in case frontmatter detection fails
        if grep -qF "Assume the prior report is wrong" "$skill_file"; then
            report_pass "SKILL.md has the zero-trust standing rule (found deeper in file)"
        else
            report_fail "SKILL.md missing zero-trust standing rule: 'Assume the prior report is wrong'"
        fi
    fi

    # Check for live-state verification mention
    if grep -qF "live state" "$skill_file" || grep -qF "live-state" "$skill_file"; then
        report_pass "SKILL.md references 'live state' verification"
    else
        report_fail "SKILL.md missing 'live state' verification requirement"
    fi
else
    report_fail "$skill_file not found"
fi

# --- Test 2: Live State Verification section in review_template.md ---
tmpl_file="templates/review_template.md"
if [ -f "$tmpl_file" ]; then
    if grep -q "## Live State Verification" "$tmpl_file"; then
        report_pass "review_template.md has 'Live State Verification' section"
    else
        report_fail "review_template.md missing 'Live State Verification' section"
    fi

    # Check that the section has claim/command/observed-state fields
    section=$(sed -n '/## Live State Verification/,/^## /p' "$tmpl_file" 2>/dev/null || true)
    if [ -n "$section" ]; then
        for keyword in claim command observed; do
            if echo "$section" | grep -qi "$keyword"; then
                report_pass "Live State Verification section has '$keyword' field"
            else
                report_fail "Live State Verification section missing '$keyword' field"
            fi
        done
    else
        report_fail "Could not extract Live State Verification section content"
    fi

    # Check positioning (after Compliance/Verification, before Architecture Assessment)
    compliance_line=$(grep -n 'Specification Compliance\|Compliance Matrix' "$tmpl_file" | head -1 | cut -d: -f1)
    live_line=$(grep -n '## Live State Verification' "$tmpl_file" | head -1 | cut -d: -f1)
    arch_line=$(grep -n '## Architecture Assessment' "$tmpl_file" | head -1 | cut -d: -f1)

    if [ -n "$compliance_line" ] && [ -n "$live_line" ] && [ -n "$arch_line" ]; then
        if [ "$compliance_line" -lt "$live_line" ] && [ "$live_line" -lt "$arch_line" ]; then
            report_pass "Live State Verification positioned correctly (Compliance < Live State < Architecture)"
        else
            report_fail "Live State Verification section in wrong position (Compliance=$compliance_line Live=$live_line Arch=$arch_line)"
        fi
    fi
else
    report_fail "$tmpl_file not found"
fi

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-2 PASSED"
else
    echo "RESULT: FR-2 FAILED"
fi
exit "$FAILED"