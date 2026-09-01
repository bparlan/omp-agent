#!/bin/bash
# Verification IDs: V-NFR-6
# Requirement IDs: NFR-6
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify legacy_indexer.py completes indexing 100 files within 1 second

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/performance"
TEST_PASSED=0
TEST_FAILED=1

# --- Cleanup handler ---
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# --- Create fixture ---
MILESTONE_DIR="$FIXTURE_DIR/M1"
mkdir -p "$MILESTONE_DIR"

for i in $(seq 1 100); do
    echo "# Milestone 1 Section $i" > "$MILESTONE_DIR/M1S${i}.md"
done

echo "Created 100 fixture files in $MILESTONE_DIR"

# --- Check if legacy_indexer.py exists ---
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "FAIL: legacy_indexer.py not found at $INDEXER_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# --- Performance test ---
echo "Test: Performance bound — index 100 files under 1 second..."

OUTPUT_FILE="$FIXTURE_DIR/legacy_manifest.txt"

# Use TIMEFORMAT to get real time in seconds, capture it via stderr redirection
# time writes to stderr of the subshell; we isolate python3's output to fd 3
TIMEFORMAT=%R
ELAPSED=$({ time python3 "$INDEXER_SCRIPT" --milestone-dir "$FIXTURE_DIR" --output "$OUTPUT_FILE" 1>&3 2>&3; } 3>&1)
EXIT_CODE=$?

# Validate exit code
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented or errored."
    exit $TEST_FAILED
fi

# Validate output file exists
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "FAIL: Output manifest not created at $OUTPUT_FILE"
    exit $TEST_FAILED
fi

# Validate timing
ELAPSED_CLEAN=$(echo "$ELAPSED" | tr -d ' \n')
echo "Elapsed time: ${ELAPSED_CLEAN}s"

# Use bc for floating-point comparison if available, otherwise awk
if command -v bc &>/dev/null; then
    WITHIN_BOUND=$(echo "$ELAPSED_CLEAN <= 1.0" | bc)
else
    WITHIN_BOUND=$(awk "BEGIN {print ($ELAPSED_CLEAN <= 1.0) ? 1 : 0}")
fi

if [ "$WITHIN_BOUND" != "1" ]; then
    echo "FAIL: Performance bound exceeded — ${ELAPSED_CLEAN}s > 1.0s"
    exit $TEST_FAILED
fi

echo "PASS: Indexed 100 files in ${ELAPSED_CLEAN}s (<= 1.0s bound)"
exit $TEST_PASSED
