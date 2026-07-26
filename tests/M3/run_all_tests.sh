#!/usr/bin/env bash

# Run All M3 Tests
# Ensures no regressions after M3S1I1 stability fixes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AEF_ROOT="$SCRIPT_DIR/.."

echo "========================================"
echo "Running All M3 Tests"
echo "========================================"
echo ""

# Change to AEF root
cd "$AEF_ROOT"

# Run graph-based scope verification tests
echo "Running M3S1I1 Integration Tests..."
if [ -f "$SCRIPT_DIR/test_graph_scope_verification.sh" ]; then
    "$SCRIPT_DIR/test_graph_scope_verification.sh"
else
    echo "ERROR: test_graph_scope_verification.sh not found"
    exit 1
fi
echo ""

# Run pre-merge diff scope test
echo "Running Pre-Merge Diff Scope Test..."
if [ -f "$SCRIPT_DIR/test_diff_scope_premerge.sh" ]; then
    "$SCRIPT_DIR/test_diff_scope_premerge.sh"
else
    echo "WARNING: test_diff_scope_premerge.sh not found, skipping"
fi
echo ""

# Run BariaDAO pilot test
echo "Running BariaDAO Pilot Test..."
if [ -f "$SCRIPT_DIR/test_baria_pilot.sh" ]; then
    "$SCRIPT_DIR/test_baria_pilot.sh"
else
    echo "WARNING: test_baria_pilot.sh not found, skipping"
fi
echo ""

echo "========================================"
echo "All M3 Tests Completed"
echo "========================================"
