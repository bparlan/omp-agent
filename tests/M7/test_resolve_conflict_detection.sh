#!/bin/bash
# Verification IDs: V-FR-8
# Requirement IDs: FR-8
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify conflict detection when YAML type disagrees with directory location

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESOLVE_SCRIPT="$PROJECT_ROOT/bin/resolve_artifact.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/resolve_conflict"
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

# Test: Resolve VER-001 from specifications/ directory (conflict expected)
echo "Test: Conflict detection when YAML type disagrees with directory..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" VER-001 --milestone M99 --cwd "$FIXTURE_DIR" 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 2 ]; then
    echo "FAIL: Expected exit code 2 (conflict), got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi

# Check that the conflict report includes required fields
if ! echo "$OUTPUT" | grep -qi "conflict\|mismatch\|disagreement"; then
    echo "FAIL: Conflict report does not indicate a conflict"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -q "VER-001"; then
    echo "FAIL: Conflict report does not include queried identifier VER-001"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -qi "specification\|expected.*type\|actual.*type"; then
    echo "FAIL: Conflict report does not include expected vs actual type"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi

echo "PASS: Conflict detected correctly with exit code 2"
echo "All tests passed."
exit $TEST_PASSED