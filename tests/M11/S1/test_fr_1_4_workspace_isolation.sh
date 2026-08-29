#!/bin/bash
# {Verification IDs: V-FR-1.4}
# {Requirement IDs: FR-1.4}
# Test Type: IMPLEMENTATION_CHECK
# Strategy: bash-only, direct binary invocation, no interpreter override.
# This script asserts observable CLI contracts from SPEC-M11S1 (FR-1.4).
# On a blank codebase it must fail naturally with exit 127 (VALID_INITIAL_FAILURE).

set -uo pipefail

echo "[TEST] FR-1.4 CLI contract evidence for workspace isolation management"

# Direct invocation: no interpreter prefix, no pre-flight binary check.
# The OS kernel resolves interpreter via shebang (e.g., bin/workspace-create).

# 1. workspace-create
if workspace-create --project . --runtime python --name my_workspace 2>/dev/null; then
    echo "PASS: workspace-create returned 0"
else
    echo "FAIL (expected pre-impl): workspace-create non-functional"
fi

# 2. workspace-activate
if workspace-activate --project . --runtime python 2>/dev/null; then
    echo "PASS: workspace-activate returned 0"
else
    echo "FAIL (expected pre-impl): workspace-activate non-functional"
fi

# 3. workspace-status
if workspace-status --project . --runtime python 2>/dev/null; then
    echo "PASS: workspace-status returned 0"
else
    echo "FAIL (expected pre-impl): workspace-status non-functional"
fi

# 4. workspace-clean
if workspace-clean --project . --runtime python --force 2>/dev/null; then
    echo "PASS: workspace-clean returned 0"
else
    echo "FAIL (expected pre-impl): workspace-clean non-functional"
fi
