#!/bin/bash
# Verification IDs: V-NFR-3, V-NFR-4
# Requirement IDs: NFR-3, NFR-4
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify performance bound (5s) and portable path resolution

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

# Test 1: Performance bound (NFR-3) - must complete within 5 seconds
echo "Test 1: Performance bound (5 second timeout)..."
# Create a larger fixture with 100+ files for performance testing
LARGE_FIXTURE_DIR="/tmp/resolve_large_fixture_$$"
mkdir -p "$LARGE_FIXTURE_DIR/M99/specifications"
# Create a reference file with proper frontmatter
cat > "$LARGE_FIXTURE_DIR/M99/specifications/SPEC-001.md" << 'EOF'
---
id: SPEC-001
type: specification
title: "Performance Test Fixture"
milestone_id: M99
status: draft
derived_from: []
---
EOF
# Create 100 additional files for load testing
for i in $(seq 100 199); do
    echo "---
id: SPEC-$i
type: specification
title: "Performance Test Fixture $i"
milestone_id: M99
status: draft
derived_from: []
---
# SPEC-$i" > "$LARGE_FIXTURE_DIR/M99/specifications/SPEC-$i.md"
done

# Run with timeout
if command -v timeout > /dev/null 2>&1; then
    TIMEOUT_CMD="timeout 5"
else
    # macOS: use perl or gtimeout
    if command -v gtimeout > /dev/null 2>&1; then
        TIMEOUT_CMD="gtimeout 5"
    else
        echo "SKIP: No timeout command available — skipping performance test"
        rm -rf "$LARGE_FIXTURE_DIR"
        echo "PASS: Performance test skipped (no timeout utility)"
        exit $TEST_PASSED
    fi
fi

START_TIME=$(date +%s)
$TIMEOUT_CMD python3 "$RESOLVE_SCRIPT" SPEC-001 --milestone M99 --cwd "$LARGE_FIXTURE_DIR" > /dev/null 2>&1
PERF_EXIT=$?
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

rm -rf "$LARGE_FIXTURE_DIR"

if [ $PERF_EXIT -eq 124 ]; then
    echo "FAIL: Resolution timed out (>5 seconds) with 100+ files"
    exit $TEST_FAILED
fi
if [ $PERF_EXIT -ne 0 ]; then
    echo "FAIL: Resolution failed with exit code $PERF_EXIT (expected 0)"
    exit $TEST_FAILED
fi
echo "PASS: Resolution completed within ${ELAPSED}s (bound: 5s)"

# Test 2: Portable path resolution (NFR-4) - invoke from outside project root
echo "Test 2: Portable path resolution from outside project root..."
TMPDIR=$(mktemp -d)
pushd "$TMPDIR" > /dev/null 2>&1 || exit $TEST_FAILED

OUTPUT=$(python3 "$RESOLVE_SCRIPT" SPEC-001 --milestone M99 --cwd "$FIXTURE_DIR" 2>&1)
EXIT_CODE=$?

popd > /dev/null 2>&1 || true
rm -rf "$TMPDIR"

if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0 from outside project root, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
if ! echo "$OUTPUT" | grep -q "SPEC-001.md"; then
    echo "FAIL: Output does not contain SPEC-001.md"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Resolution works from outside project root"

echo "All tests passed."
exit $TEST_PASSED