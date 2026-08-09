#!/bin/bash

# Verification IDs: V-FR-14
# Requirement IDs: FR-14

# Test Type: IMPLEMENTATION_CHECK
# Description: Verify that files unclassifiable through tiers 1-5 resolve to
#              AMBIGUOUS_LEGACY_ARTIFACT and are flagged for manual review.
#              On missing implementation, the command will fail naturally
#              (exit code 127/1) = VALID_INITIAL_FAILURE.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/safe_fallback"
FIXTURE_M1="$FIXTURE_DIR/M1"
MANIFEST_FILE="$FIXTURE_DIR/legacy_manifest.txt"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup handler
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# Create fixture
mkdir -p "$FIXTURE_M1"

cat > "$FIXTURE_M1/unknown_1.xyz" << 'EOF'
# Unknown

Body.
EOF

cat > "$FIXTURE_M1/data.bin" << 'EOF'
# Unknown

Body.
EOF

echo "Test 1: FR-14 — Safe fallback for unclassifiable files..."

# Run the indexer once, capturing stdout and stderr separately.
# If script doesn't exist, this fails naturally (VALID_INITIAL_FAILURE).
# Use a temp file for stderr so we can capture it alongside the exit code.
STDERR_FILE=$(mktemp)
STDOUT_FILE=$(mktemp)
python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_DIR" \
    --output "$MANIFEST_FILE" \
    --verbose > "$STDOUT_FILE" 2> "$STDERR_FILE"
EXIT_CODE=$?
STDERR_OUTPUT=$(cat "$STDERR_FILE")
rm -f "$STDERR_FILE" "$STDOUT_FILE"

if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Indexer exited with code $EXIT_CODE (expected 0)."
    echo "This is a VALID_INITIAL_FAILURE — bin/legacy_indexer.py not yet implemented."
    exit $TEST_FAILED
fi

# Check that manifest was created
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "FAIL: Manifest file not created at $MANIFEST_FILE"
    exit $TEST_FAILED
fi

# Check that manifest contains AMBIGUOUS_LEGACY_ARTIFACT for both files
AMBIGUOUS_COUNT=$(grep -c "AMBIGUOUS_LEGACY_ARTIFACT" "$MANIFEST_FILE" || true)
if [ "$AMBIGUOUS_COUNT" -lt 2 ]; then
    echo "FAIL: Expected 2 manifest entries with 'AMBIGUOUS_LEGACY_ARTIFACT', found $AMBIGUOUS_COUNT."
    echo "Manifest contents:"
    cat "$MANIFEST_FILE"
    exit $TEST_FAILED
fi

# Verify no guessed type like 'specification' or 'investigation' appears
if grep -qi "specification\|investigation\|test\|verification\|implementation\|evaluation\|review\|audit" "$MANIFEST_FILE"; then
    echo "FAIL: Manifest contains guessed type labels instead of AMBIGUOUS_LEGACY_ARTIFACT."
    grep -i "specification\|investigation\|test\|verification\|implementation\|evaluation\|review\|audit" "$MANIFEST_FILE"
    exit $TEST_FAILED
fi

# Check that stderr flags both files for manual review
for file in unknown_1.xyz data.bin; do
    if ! echo "$STDERR_OUTPUT" | grep -q "$file"; then
        echo "FAIL: Stderr does not flag $file for manual review."
        echo "Stderr output: $STDERR_OUTPUT"
        exit $TEST_FAILED
    fi
done

# Verify stderr contains manual-review language
if ! echo "$STDERR_OUTPUT" | grep -qi "review\|manual\|ambiguous\|unclassified"; then
    echo "FAIL: Stderr does not contain manual review flag language."
    echo "Stderr output: $STDERR_OUTPUT"
    exit $TEST_FAILED
fi

echo "PASS: FR-14 — Both unclassifiable files produce AMBIGUOUS_LEGACY_ARTIFACT with manual review flag."
exit $TEST_PASSED