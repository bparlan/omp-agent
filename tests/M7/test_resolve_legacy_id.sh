#!/bin/bash
# Verification IDs: V-FR-7b, V-FR-9
# Requirement IDs: FR-7, FR-9
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify legacy ID resolution via filename heuristics (Tier 3)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESOLVE_SCRIPT="$PROJECT_ROOT/bin/resolve_artifact.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/resolve"
TEST_PASSED=0
TEST_FAILED=1

# Self-validity check
if [ ! -d "$FIXTURE_DIR" ]; then
    echo "FAIL: Fixture directory not found: $FIXTURE_DIR"
    exit $TEST_FAILED
fi

# Check if resolve_artifact.py exists
if [ ! -f "$RESOLVE_SCRIPT" ]; then
    echo "FAIL: resolve_artifact.py not found at $RESOLVE_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# Test 1: Resolve M7S1 legacy ID via filename heuristics (Tier 3)
echo "Test 1: Resolve M7S1 legacy ID..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" M7S1 --milestone M99 --cwd "$FIXTURE_DIR" 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -q "M7S1.md"; then
    echo "FAIL: Output does not contain M7S1.md"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: M7S1 resolved via legacy filename heuristic"

# Test 2: Verbose mode reports Tier 3 for legacy ID
echo "Test 2: Verbose mode tier reporting for legacy ID..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" M7S1 --milestone M99 --cwd "$FIXTURE_DIR" --verbose 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -qi "tier 3\|tier.*3\|legacy\|filename.*heuristic\|filename.*pattern"; then
    echo "FAIL: Verbose output does not report Tier 3 (legacy) resolution"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose mode reports Tier 3 for legacy ID"

echo "All tests passed."
exit $TEST_PASSED