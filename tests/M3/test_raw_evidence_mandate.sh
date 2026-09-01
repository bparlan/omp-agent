#!/bin/bash
# M3S2 — FR-4: Raw Evidence Mandate
# Verifies that completion_template.md and evaluation_template.md
# contain a mandatory "## Raw Evidence" section with the evidence template.
# Usage: ./tests/M3/test_raw_evidence_mandate.sh

set -euo pipefail
FAILED=0

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

echo "=== FR-4: Raw Evidence Mandate ==="

check_template_has_raw_evidence() {
    local file="$1"
    local label="$2"

    if [ ! -f "$file" ]; then
        report_fail "$label: $file not found"
        return
    fi

    # Check for ## Raw Evidence section
    if grep -q "## Raw Evidence" "$file"; then
        report_pass "$label has '## Raw Evidence' section"
    else
        report_fail "$label missing '## Raw Evidence' section"
        return
    fi

    # Extract the Raw Evidence section content
    section=$(sed -n '/^## Raw Evidence/,/^## /p' "$file" 2>/dev/null || true)

    if [ -z "$section" ]; then
        # Maybe section is at the end of the file (no subsequent ## heading)
        section=$(sed -n '/^## Raw Evidence/,$ p' "$file" 2>/dev/null || true)
    fi

    # Check for exact command and raw output language
    if echo "$section" | grep -qF "exact terminal command"; then
        report_pass "$label has 'exact terminal command' language"
    else
        report_fail "$label missing 'exact terminal command' phrase"
    fi

    if echo "$section" | grep -qF "raw output"; then
        report_pass "$label has 'raw output' language"
    else
        report_fail "$label missing 'raw output' phrase"
    fi

    # Check for the bullet template format
    if echo "$section" | grep -qF '<requirement>' && echo "$section" | grep -qF '<command>' && echo "$section" | grep -qF '<raw output>'; then
        report_pass "$label has structured bullet template"
    else
        report_fail "$label missing structured bullet template (requirement/command/raw-output placeholders)"
    fi
}

echo "--- completion_template.md ---"
check_template_has_raw_evidence "templates/completion_template.md" "completion_template"

echo "--- evaluation_template.md ---"
check_template_has_raw_evidence "templates/evaluation_template.md" "evaluation_template"

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-4 PASSED"
else
    echo "RESULT: FR-4 FAILED"
fi
exit "$FAILED"
