#!/bin/bash
# Verification IDs: V-FR-12f
# Requirement IDs: FR-12 (T6)
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 6 fallback — legacy_indexer.py flags ambiguous files with no YAML,
#   no directory classifier, no heading, and no legacy naming pattern as requiring manual review.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/classify_tier6"
TEMP_DIR="${FIXTURE_DIR}_$$"
MILESTONE_DIR="$TEMP_DIR/M1"
OUTPUT_FILE="$TEMP_DIR/legacy_manifest.txt"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup on exit
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Setup fixture
mkdir -p "$MILESTONE_DIR"

# unknown_1.xyz: NO YAML, NO directory, NO heading, NO legacy naming
cat > "$MILESTONE_DIR/unknown_1.xyz" << 'FIXTURE_EOF'
# Unknown

Body.
FIXTURE_EOF

# data.bin: NO YAML, NO directory, NO heading, NO legacy naming
cat > "$MILESTONE_DIR/data.bin" << 'FIXTURE_EOF'
binary data
FIXTURE_EOF

# Self-validity check
if [ ! -d "$MILESTONE_DIR" ]; then
    echo "FAIL: Could not create fixture directory: $MILESTONE_DIR"
    exit $TEST_FAILED
fi

# Check if legacy_indexer.py exists
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "FAIL: legacy_indexer.py not found at $INDEXER_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# Test: Run legacy_indexer.py on the ambiguous fixture directory
echo "Test: Tier 6 fallback — ambiguous files flagged for manual review..."

STDERR_OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$MILESTONE_DIR" \
    --output "$OUTPUT_FILE" \
    --verbose 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Stderr: $STDERR_OUTPUT"
    exit $TEST_FAILED
fi

# Check that both files are flagged as requiring manual review
if ! echo "$STDERR_OUTPUT" | grep -qi "AMBIGUOUS_LEGACY_ARTIFACT"; then
    # Fallback check: look for "manual review" or similar flagging language
    if ! echo "$STDERR_OUTPUT" | grep -qi "manual review"; then
        echo "FAIL: Neither 'AMBIGUOUS_LEGACY_ARTIFACT' nor 'manual review' flag found in output"
        echo "Stderr: $STDERR_OUTPUT"
        exit $TEST_FAILED
    fi
fi

# Check that both files are mentioned in the flagged output
if ! echo "$STDERR_OUTPUT" | grep -qi "unknown_1.xyz"; then
    echo "FAIL: unknown_1.xyz not flagged in output"
    echo "Stderr: $STDERR_OUTPUT"
    exit $TEST_FAILED
fi

if ! echo "$STDERR_OUTPUT" | grep -qi "data.bin"; then
    echo "FAIL: data.bin not flagged in output"
    echo "Stderr: $STDERR_OUTPUT"
    exit $TEST_FAILED
fi

echo "PASS: Both ambiguous files flagged for Tier 6 fallback (manual review)"
echo "All tests passed."
exit $TEST_PASSED
