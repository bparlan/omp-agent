#!/bin/bash
# Verification IDs: V-FR-13
# Requirement IDs: FR-13
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify legacy_indexer.py is read-only — no files modified/created/deleted in M1/
# On missing implementation, the command will fail naturally (exit code 127/1) = VALID_INITIAL_FAILURE

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/zero_touch"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
TEST_PASSED=0
TEST_FAILED=1

# Setup: create fixture directory and files
mkdir -p "$FIXTURE_DIR/M1"

# Create fixture files with distinct content
echo "spec content M1S1" > "$FIXTURE_DIR/M1/M1S1.md"
echo "verification content M1S1V" > "$FIXTURE_DIR/M1/M1S1V.md"
echo "test content M1S1T1" > "$FIXTURE_DIR/M1/M1S1T1.md"

# Register cleanup — remove fixture dir on exit
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# --- Phase 1: Record pre-execution baseline ---

# Count files in M1/ before execution
FILE_COUNT_BEFORE=$(find "$FIXTURE_DIR/M1" -type f | wc -l | tr -d ' ')

# Record checksums of all 3 fixture files
CHKSUM1_BEFORE=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1.md" | awk '{print $1}')
CHKSUM2_BEFORE=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1V.md" | awk '{print $1}')
CHKSUM3_BEFORE=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1T1.md" | awk '{print $1}')

# --- Phase 2: Execute legacy_indexer.py ---

python3 "$INDEXER_SCRIPT" --milestone-dir "$FIXTURE_DIR" --output "$FIXTURE_DIR/legacy_manifest.txt"
EXIT_CODE=$?

# --- Phase 3: Validate ---

# Assert 1: Exit code 0
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    exit $TEST_FAILED
fi

# Assert 2: All checksums unchanged
CHKSUM1_AFTER=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1.md" | awk '{print $1}')
CHKSUM2_AFTER=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1V.md" | awk '{print $1}')
CHKSUM3_AFTER=$(shasum -a 256 "$FIXTURE_DIR/M1/M1S1T1.md" | awk '{print $1}')

if [ "$CHKSUM1_BEFORE" != "$CHKSUM1_AFTER" ]; then
    echo "FAIL: M1S1.md checksum changed"
    echo "  Before: $CHKSUM1_BEFORE"
    echo "  After:  $CHKSUM1_AFTER"
    exit $TEST_FAILED
fi

if [ "$CHKSUM2_BEFORE" != "$CHKSUM2_AFTER" ]; then
    echo "FAIL: M1S1V.md checksum changed"
    echo "  Before: $CHKSUM2_BEFORE"
    echo "  After:  $CHKSUM2_AFTER"
    exit $TEST_FAILED
fi

if [ "$CHKSUM3_BEFORE" != "$CHKSUM3_AFTER" ]; then
    echo "FAIL: M1S1T1.md checksum changed"
    echo "  Before: $CHKSUM3_BEFORE"
    echo "  After:  $CHKSUM3_AFTER"
    exit $TEST_FAILED
fi

# Assert 3: No files added/removed inside M1/
FILE_COUNT_AFTER=$(find "$FIXTURE_DIR/M1" -type f | wc -l | tr -d ' ')

if [ "$FILE_COUNT_BEFORE" -ne "$FILE_COUNT_AFTER" ]; then
    echo "FAIL: File count in M1/ changed (before: $FILE_COUNT_BEFORE, after: $FILE_COUNT_AFTER)"
    exit $TEST_FAILED
fi

echo "PASS: All checksums unchanged, file count unchanged, exit code 0"
exit $TEST_PASSED