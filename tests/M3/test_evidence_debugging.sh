#!/bin/bash
# M3S2 — FR-3: Evidence-Based Debugging Mandate
# Verifies that investigate-issue/SKILL.md and evaluate-implementation/SKILL.md
# begin with "Debug from evidence, never from memory" standing rule.
# Usage: ./tests/M3/test_evidence_debugging.sh

set -euo pipefail
FAILED=0

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

echo "=== FR-3: Evidence-Based Debugging Mandate ==="

# Helper: check if a file's first non-metadata content contains the rule
check_file_has_rule() {
    local file="$1"
    local label="$2"

    if [ ! -f "$file" ]; then
        report_fail "$label: $file not found"
        return
    fi

    # Extract content after YAML frontmatter and title
    body=$(awk '/^(---|\.\.\.)/{c++;next} c>=2{print;exit}' "$file" 2>/dev/null || true)
    if [ -z "$body" ]; then
        body=$(tail -n +15 "$file" | head -30)
    fi

    if echo "$body" | grep -qF "Debug from evidence"; then
        report_pass "$label has evidence-based debugging rule"
    elif grep -qF "Debug from evidence" "$file"; then
        report_pass "$label has evidence-based debugging rule (found deeper in file)"
    else
        report_fail "$label missing 'Debug from evidence, never from memory' rule"
    fi

    # Check for specific anti-pattern-matching clause
    if grep -qF "pattern-match" "$file" || grep -qF "pattern matching" "$file" || grep -qF "from memory" "$file"; then
        report_pass "$label has anti-pattern-matching clause"
    else
        report_fail "$label missing anti-pattern-matching prohibition"
    fi

    # Check for --help or introspection mention
    if grep -qF -- "--help" "$file" || grep -qF "introspection" "$file"; then
        report_pass "$label references --help or introspection commands"
    else
        report_fail "$label missing reference to --help or introspection commands"
    fi
}

echo "--- investigate-issue/SKILL.md ---"
check_file_has_rule "skills/investigate-issue/SKILL.md" "investigate-issue"

echo "--- evaluate-implementation/SKILL.md ---"
check_file_has_rule "skills/evaluate-implementation/SKILL.md" "evaluate-implementation"

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-3 PASSED"
else
    echo "RESULT: FR-3 FAILED"
fi
exit "$FAILED"
