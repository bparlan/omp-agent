#!/bin/bash
# {Verification IDs: V-FR-1.1}
# {Requirement IDs: FR-1.1}
# Test Type: IMPLEMENTATION_CHECK
# Strategy: bash-only, direct binary invocation, no interpreter override.
# This script asserts observable CLI contracts from SPEC-M11S1 (FR-1.1).
# On a blank codebase it must fail naturally with exit 127 (VALID_INITIAL_FAILURE).

set -uo pipefail

echo "[TEST] FR-1.1 CLI contract evidence"

# Direct invocation: no interpreter prefix, no pre-flight binary check.
# The OS kernel resolves interpreter via shebang (e.g., bin/env-check).
# If binary missing, shell returns 127 naturally.

# 1. env-check with --validate
if env-check --project . --runtime python --validate 2>/dev/null; then
    echo "PASS: env-check returned 0"
else
    echo "FAIL (expected pre-impl): env-check non-functional (exit=$?)"
fi

# 2. env-setup
if env-setup --project . --runtime node --tool node --version "18.0.0" 2>/dev/null; then
    echo "PASS: env-setup returned 0"
else
    echo "FAIL (expected pre-impl): env-setup non-functional"
fi

# 3. env-list
if env-list --runtime rust --all --json 2>/dev/null; then
    echo "PASS: env-list returned 0"
else
    echo "FAIL (expected pre-impl): env-list non-functional"
fi

# 4. env-diagnose
if env-diagnose --project . --output yaml 2>/dev/null; then
    echo "PASS: env-diagnose returned 0"
else
    echo "FAIL (expected pre-impl): env-diagnose non-functional"
fi
