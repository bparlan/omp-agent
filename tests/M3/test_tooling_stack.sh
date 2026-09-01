#!/bin/bash
# M3S2 — FR-6: Mechanical Tooling Stack Mandate
# Verifies that bootstrap-project/SKILL.md and AGENTS.md contain the
# four-category tooling mandate with no hardcoded brand names.
# Usage: ./tests/M3/test_tooling_stack.sh

set -euo pipefail
FAILED=0

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

echo "=== FR-6: Mechanical Tooling Stack Mandate ==="

# --- Target files ---
bp_file="skills/bootstrap-project/SKILL.md"
ag_file="AGENTS.md"

# --- Category presence in bootstrap-project ---
echo "--- bootstrap-project/SKILL.md ---"
if [ -f "$bp_file" ]; then
    for cat in "Environment Manager" "Fast Linter/Formatter" "Pre-commit Framework" "Type Checker"; do
        if grep -qiE "$cat" "$bp_file"; then
            report_pass "bootstrap-project references '$cat' category"
        else
            report_fail "bootstrap-project missing '$cat' category"
        fi
    done

    # Check positioning: step between "Create missing documents" (step 7) and "Create root-level entry points" (step 8)
    step7_line=$(grep -n 'Create missing documents' "$bp_file" | head -1 | cut -d: -f1 || true)
    step8_line=$(grep -n 'Create root-level entry points\|root-level entry' "$bp_file" | head -1 | cut -d: -f1 || true)
    tooling_lines=$(grep -n 'Mechanical Tooling\|tooling stack\|Environment Manager' "$bp_file" | head -5 | cut -d: -f1 || true)

    if [ -n "$step7_line" ] && [ -n "$step8_line" ] && [ -n "$tooling_lines" ]; then
        # Check that at least one tooling reference falls between steps 7 and 8
        between=0
        while IFS= read -r tl; do
            if [ "$tl" -gt "$step7_line" ] && [ "$tl" -lt "$step8_line" ]; then
                between=1
                break
            fi
        done <<< "$tooling_lines"

        if [ "$between" -eq 1 ]; then
            report_pass "Tooling stack step positioned between steps 7 and 8"
        else
            report_fail "Tooling stack step NOT positioned between steps 7 and 8 (7=$step7_line 8=$step8_line tooling=$tooling_lines)"
        fi
    else
        if [ -z "$step7_line" ]; then report_fail "Could not locate step 7 (Create missing documents)"; fi
        if [ -z "$step8_line" ]; then report_fail "Could not locate step 8 (Create root-level entry points)"; fi
        if [ -z "$tooling_lines" ]; then report_fail "No Mechanical Tooling Stack reference found in bootstrap-project"; fi
    fi
else
    report_fail "$bp_file not found"
fi

echo "--- AGENTS.md ---"
if [ -f "$ag_file" ]; then
    for cat in "Environment Manager" "Fast Linter/Formatter" "Pre-commit Framework" "Type Checker"; do
        if grep -qiE "$cat" "$ag_file"; then
            report_pass "AGENTS.md references '$cat' category"
        else
            report_fail "AGENTS.md missing '$cat' category"
        fi
    done

    # Check for Mechanical Tooling Stack section under Core Concepts
    if grep -q "Mechanical Tooling Stack" "$ag_file"; then
        report_pass "AGENTS.md has 'Mechanical Tooling Stack' section"
    else
        report_fail "AGENTS.md missing 'Mechanical Tooling Stack' section"
    fi

    # Check for "every bootstrapped project" language
    if grep -qiE "every.*project.*document|each.*project.*define|bootstrapped.*stack" "$ag_file"; then
        report_pass "AGENTS.md mandates documentation per bootstrapped project"
    else
        report_fail "AGENTS.md missing mandate for per-project tooling stack documentation"
    fi
else
    report_fail "$ag_file not found"
fi

# --- Brand name audit (NFR-4) ---
echo "--- Brand Name Audit (NFR-4) ---"
brands_found=""
for brand in mise ruff poetry black isort flake8 pylint eslint prettier biome mypy pipenv venv "golangci-lint" clippy; do
    for f in "$bp_file" "$ag_file"; do
        if [ -f "$f" ] && grep -iqs "$brand" "$f"; then
            # Exclude if the brand is in a negative example or "do not hardcode" context
            context=$(grep -i "$brand" "$f" 2>/dev/null || true)
            if ! echo "$context" | grep -qiE "do not.*hard.*code\|must not.*use\|example.*only\|e\.g\."; then
                brands_found="$brands_found $brand($f)"
            fi
        fi
    done
done

if [ -z "$brands_found" ]; then
    report_pass "No hardcoded tooling brand names found in target files (NFR-4)"
else
    report_fail "Hardcoded brand names found:$brands_found"
fi

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-6 PASSED"
else
    echo "RESULT: FR-6 FAILED"
fi
exit "$FAILED"
