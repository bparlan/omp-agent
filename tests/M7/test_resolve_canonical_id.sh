#!/bin/bash
# Verification IDs: V-FR-7a, V-FR-9
# Requirement IDs: FR-7, FR-9
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify canonical ID resolution via YAML metadata (Tier 1) and directory context (Tier 2)

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

# Test 1: Resolve SPEC-001 via YAML metadata (Tier 1)
echo "Test 1: Resolve SPEC-001 via YAML metadata..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" SPEC-001 --milestone M99 --cwd "$FIXTURE_DIR" 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -q "SPEC-001.md"; then
    echo "FAIL: Output does not contain SPEC-001.md"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: SPEC-001 resolved successfully"

# Test 2: Resolve VER-001 via directory context (Tier 2)
echo "Test 2: Resolve VER-001 via directory context..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" VER-001 --milestone M99 --cwd "$FIXTURE_DIR" 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -q "VER-001.md"; then
    echo "FAIL: Output does not contain VER-001.md"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: VER-001 resolved successfully"

# Test 3: Verbose mode shows resolution tier (V-FR-9)
echo "Test 3: Verbose mode tier reporting..."
VERBOSE_FIXTURE="$PROJECT_ROOT/tests/M7/fixtures/resolve_verbose"
OUTPUT=$(python3 "$RESOLVE_SCRIPT" SPEC-005 --milestone M99 --cwd "$VERBOSE_FIXTURE" --verbose 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -qi "tier 1\|tier.*1\|yaml.*metadata"; then
    echo "FAIL: Verbose output does not report resolution tier"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose mode reports resolution tier"

echo "All tests passed."
exit $TEST_PASSED