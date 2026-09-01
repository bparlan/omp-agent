#!/bin/bash
# Verification IDs: V-FR-12b
# Requirement IDs: FR-12 (T2)
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 2 classification (directory structure) for files without frontmatter

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/classify_tier2"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup: remove fixture dir on exit
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# Self-validity check
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "FAIL: legacy_indexer.py not found at $INDEXER_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# Setup fixture: create M1 with subdirectories and files (no YAML frontmatter)
mkdir -p "$FIXTURE_DIR/M1/specifications"
mkdir -p "$FIXTURE_DIR/M1/verifications"
mkdir -p "$FIXTURE_DIR/M1/tests"

cat > "$FIXTURE_DIR/M1/specifications/spec.md" << 'EOF'
# Some Document

Body.
EOF

cat > "$FIXTURE_DIR/M1/verifications/ver.md" << 'EOF'
# Some Document

Body.
EOF

cat > "$FIXTURE_DIR/M1/tests/test.md" << 'EOF'
# Some Document

Body.
EOF

MANIFEST_OUTPUT="$FIXTURE_DIR/legacy_manifest.txt"

# Run the indexer with verbose output
echo "Test 1: V-FR-12b — Tier 2 directory structure classification..."
OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_DIR" \
    --output "$MANIFEST_OUTPUT" \
    --verbose 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: legacy_indexer.py exited with code $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi

# Check verbose output mentions Tier 2 or directory-based classification
if ! echo "$OUTPUT" | grep -qi "tier 2\|tier.*2\|directory.*classif\|classif.*directory\|infer.*director\|director.*infer"; then
    echo "FAIL: Verbose output does not indicate Tier 2 (directory structure) classification"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose output references Tier 2 classification"

# Check that all 3 files appear in the manifest
if [ ! -f "$MANIFEST_OUTPUT" ]; then
    echo "FAIL: Manifest file not created at $MANIFEST_OUTPUT"
    exit $TEST_FAILED
fi

MANIFEST_LINES=$(wc -l < "$MANIFEST_OUTPUT")
if [ "$MANIFEST_LINES" -ne 3 ]; then
    echo "FAIL: Manifest contains $MANIFEST_LINES lines, expected 3"
    echo "Manifest content:"
    cat "$MANIFEST_OUTPUT"
    exit $TEST_FAILED
fi

# Verify each file is in the manifest
for relpath in "M1/specifications/spec.md" "M1/verifications/ver.md" "M1/tests/test.md"; do
    if ! grep -q "$relpath" "$MANIFEST_OUTPUT"; then
        echo "FAIL: Manifest missing entry for $relpath"
        echo "Manifest content:"
        cat "$MANIFEST_OUTPUT"
        exit $TEST_FAILED
    fi
done
echo "PASS: All 3 files present in manifest"

# Verify each line matches SHA-256 <relative-path> format
INVALID_LINES=$(grep -c -v '^[0-9a-f]\{64\} ' "$MANIFEST_OUTPUT" || true)
if [ "$INVALID_LINES" -ne 0 ]; then
    echo "FAIL: Manifest contains $INVALID_LINES lines not matching SHA-256 <relative-path> format"
    echo "Manifest content:"
    cat "$MANIFEST_OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: All manifest entries match SHA-256 checksum format"

echo "All tests passed."
exit $TEST_PASSED
