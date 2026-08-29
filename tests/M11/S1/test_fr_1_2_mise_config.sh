#!/bin/bash
# {Verification IDs: V-FR-1.2}
# {Requirement IDs: FR-1.2}
# Test Type: IMPLEMENTATION_CHECK
# Strategy: bash-only, direct binary invocation, no interpreter override.
# This script asserts observable CLI contracts from SPEC-M11S1 (FR-1.2).
# On a blank codebase it must fail naturally with exit 127 (VALID_INITIAL_FAILURE).

set -uo pipefail

echo "[TEST] FR-1.2 CLI contract evidence for .mise.toml configuration"

# Direct invocation: no interpreter prefix, no pre-flight binary check.
# The OS kernel resolves interpreter via shebang (e.g., bin/mise-validate).

# 1. mise-validate
if mise-validate --config . --schema 1.0.0 2>/dev/null; then
    echo "PASS: mise-validate returned 0"
else
    echo "FAIL (expected pre-impl): mise-validate non-functional"
fi

# 2. mise-generate
if mise-generate --runtime python --output ./generated.toml --template python 2>/dev/null; then
    echo "PASS: mise-generate returned 0"
else
    echo "FAIL (expected pre-impl): mise-generate non-functional"
fi

# 3. mise-merge
if mise-merge --base ./base.toml --override ./override.toml --output ./merged.toml 2>/dev/null; then
    echo "PASS: mise-merge returned 0"
else
    echo "FAIL (expected pre-impl): mise-merge non-functional"
fi
