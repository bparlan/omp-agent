#!/bin/bash
# Verification IDs: V-NFR-2
# Requirement IDs: NFR-2
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify resolve_artifact.py does not modify any files during resolution

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

# Record checksums before resolution
echo "Recording checksums before resolution..."
BEFORE_CHECKSUMS=$(find "$FIXTURE_DIR" -type f -exec sha256sum {} \; | sort)
echo "$BEFORE_CHECKSUMS" > /tmp/checksums_before.txt

# Run resolution
echo "Running resolution..."
python3 "$RESOLVE_SCRIPT" SPEC-001 --milestone M99 --cwd "$FIXTURE_DIR" > /dev/null 2>&1
RESOLVE_EXIT=$?
python3 "$RESOLVE_SCRIPT" VER-001 --milestone M99 --cwd "$FIXTURE_DIR" > /dev/null 2>&1
python3 "$RESOLVE_SCRIPT" M7S1 --milestone M99 --cwd "$FIXTURE_DIR" > /dev/null 2>&1

# Record checksums after resolution
echo "Recording checksums after resolution..."
AFTER_CHECKSUMS=$(find "$FIXTURE_DIR" -type f -exec sha256sum {} \; | sort)
echo "$AFTER_CHECKSUMS" > /tmp/checksums_after.txt

# Compare
if ! diff /tmp/checksums_before.txt /tmp/checksums_after.txt > /dev/null 2>&1; then
    echo "FAIL: File checksums changed after resolution!"
    echo "Differences:"
    diff /tmp/checksums_before.txt /tmp/checksums_after.txt
    exit $TEST_FAILED
fi

echo "PASS: No files modified during resolution (checksums identical)"
echo "All tests passed."
exit $TEST_PASSED