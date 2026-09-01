#!/usr/bin/env bash
# {Verification IDs: VI-M12S3-5}
# {Requirement IDs: FR-END_TO_END_CIRCULATION_VALIDATION}
# Purpose: Validate DevOps cycle handoff boundaries across manage-roadmap → manage-development → manage-docs → sync-documentation → close-milestone

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATION_REPORT="$REPO_ROOT/docs/queue/circulation-validation-report.md"

mkdir -p "$(dirname "$VALIDATION_REPORT")"

echo "Starting end-to-end circulation validation..."

PASS_COUNT=0
FAIL_COUNT=0
BOUNDARIES=()

validate_boundary() {
    local boundary_name="$1"
    local check_command="$2"

    echo "Checking boundary: $boundary_name"
    if eval "$check_command"; then
        echo "  PASS: $boundary_name"
        PASS_COUNT=$((PASS_COUNT + 1))
        BOUNDARIES+=("- [x] $boundary_name: PASS")
    else
        echo "  FAIL: $boundary_name"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        BOUNDARIES+=("- [ ] $boundary_name: FAIL")
    fi
}

validate_boundary \
    "manage-roadmap → manage-development" \
    "test -f '$REPO_ROOT/milestones/M12/M12.md' && test -s '$REPO_ROOT/milestones/M12/M12.md'"

validate_boundary \
    "manage-development → manage-docs" \
    "grep -q '#### User Approval' '$REPO_ROOT/milestones/M12/M12S3.md'"

validate_boundary \
    "manage-docs → sync-documentation" \
    "grep -q 'operations-consolidation' '$REPO_ROOT/core/artifacts/artifact_types.py'"

validate_boundary \
    "sync-documentation → close-milestone" \
    "test -f '$REPO_ROOT/../.omp/plugins/node_modules/omp-aef/skills/manage-development/SKILL.md' && test -f '$REPO_ROOT/../.omp/plugins/node_modules/omp-aef/skills/manage-docs/SKILL.md'"

validate_boundary \
    "close-milestone → manage-roadmap" \
    "test -f '$REPO_ROOT/milestones/M12/M12S3CLOSE-1.md' || test -f '$REPO_ROOT/milestones/M12/M12S3C1.md'"

cat > "$VALIDATION_REPORT" <<EOF
# Circulation Validation Report

**Date:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Validation ID:** CIRC-VAL-M12S3-1
**Milestone:** M12
**Specification:** M12S3

## Summary

- **Boundaries Checked:** $((PASS_COUNT + FAIL_COUNT))
- **Passed:** $PASS_COUNT
- **Failed:** $FAIL_COUNT
- **Overall Status:** $([ $FAIL_COUNT -eq 0 ] && echo "PASS" || echo "FAIL")

## Boundary Checks

$(printf '%s\n' "${BOUNDARIES[@]}")

EOF

echo "Circulation validation complete."
echo "Report written to: $VALIDATION_REPORT"
echo "Passed: $PASS_COUNT, Failed: $FAIL_COUNT"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "FAIL: Some boundaries failed validation."
    exit 1
else
    echo "PASS: All boundaries passed."
    exit 0
fi
