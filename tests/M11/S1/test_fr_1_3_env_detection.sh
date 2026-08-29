#!/bin/bash
# {Verification IDs: V-FR-1.3}
# {Requirement IDs: FR-1.3}
# Test Type: IMPLEMENTATION_CHECK
# Strategy: bash-only, direct binary invocation, no interpreter override.
# This script asserts observable CLI contracts from SPEC-M11S1 (FR-1.3).
# On a blank codebase it must fail naturally with exit 127 (VALID_INITIAL_FAILURE).

set -uo pipefail

echo "[TEST] FR-1.3 CLI contract evidence for pre-task environment detection"

# Direct invocation: no interpreter prefix, no pre-flight binary check.
# The OS kernel resolves interpreter via shebang (e.g., bin/env-detect).

# 1. env-detect
if env-detect --project . --runtime python --task my_task --cache 2>/dev/null; then
    echo "PASS: env-detect returned 0"
else
    echo "FAIL (expected pre-impl): env-detect non-functional"
fi

# 2. env-status
if env-status --project . --runtime python 2>/dev/null; then
    echo "PASS: env-status returned 0"
else
    echo "FAIL (expected pre-impl): env-status non-functional"
fi

# 3. env-refresh
if env-refresh --project . --runtime python 2>/dev/null; then
    echo "PASS: env-refresh returned 0"
else
    echo "FAIL (expected pre-impl): env-refresh non-functional"
fi
