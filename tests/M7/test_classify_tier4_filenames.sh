#!/bin/bash
# Verification IDs: V-FR-12d
# Requirement IDs: FR-12 (T4)
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 4 filename classification — all 8 non-YAML, non-directory-context files
#              are classified by filename heuristic; random.md falls through as unclassified.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$SCRIPT_DIR/fixtures/classify_tier4"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup handler — runs on exit regardless of signal
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# --- Create fixture ---
MILESTONE_DIR="$FIXTURE_DIR/M1"
mkdir -p "$MILESTONE_DIR"

# 8 files, all NO YAML, NO directory context, NO heading match
for fname in M1S1.md M1S1V.md M1S1T1.md M1S1C.md M1S1E.md M1S1R.md M1S1I1.md random.md; do
    printf '# Random\n\nBody.\n' > "$MILESTONE_DIR/$fname"
done

# --- Self-validity check ---
if [ ! -d "$MILESTONE_DIR" ]; then
    echo "FAIL: Fixture directory not found: $MILESTONE_DIR"
    exit $TEST_FAILED
fi

# --- Check if legacy_indexer.py exists ---
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "FAIL: legacy_indexer.py not found at $INDEXER_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# --- Test 1: Exit code 0 ---
echo "Test 1: Exit code 0..."
OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_DIR" \
    --output "$FIXTURE_DIR/legacy_manifest.txt" \
    --verbose 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Exit code 0"

# --- Test 2: Verbose output mentions 'Tier 4' or 'filename' ---
echo "Test 2: Verbose output mentions Tier 4 or filename..."
if ! echo "$OUTPUT" | grep -qi "tier 4\|tier.*4\|filename"; then
    echo "FAIL: Verbose output does not mention 'Tier 4' or 'filename'"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose output mentions Tier 4 or filename"

# --- Test 3: All 8 files appear in the manifest ---
echo "Test 3: All 8 files in manifest..."
if [ ! -f "$FIXTURE_DIR/legacy_manifest.txt" ]; then
    echo "FAIL: Manifest file not created at $FIXTURE_DIR/legacy_manifest.txt"
    exit $TEST_FAILED
fi

MANIFEST=$(cat "$FIXTURE_DIR/legacy_manifest.txt")
for fname in M1S1.md M1S1V.md M1S1T1.md M1S1C.md M1S1E.md M1S1R.md M1S1I1.md random.md; do
    if ! echo "$MANIFEST" | grep -q "$fname"; then
        echo "FAIL: Manifest does not contain $fname"
        echo "Manifest:"
        echo "$MANIFEST"
        exit $TEST_FAILED
    fi
done
echo "PASS: All 8 files present in manifest"

# --- Test 4: random.md falls through (not classified as a known type) ---
echo "Test 4: random.md falls through (unclassified)..."
# The manifest entry for random.md should either:
#   - be absent entirely (if the indexer only dumps classified files), or
#   - carry an explicit "unclassified" / "unknown" / "fallthrough" marker
if ! echo "$MANIFEST" | grep -qi "random.*unclassified\|random.*unknown\|random.*fallthrough\|random.*fall.?thru"; then
    # Alternative: check if random.md is listed without a known type classification
    # A known type classification would be one of the standard suffix types
    echo "WARNING: random.md fallthrough not explicitly marked; checking secondary indicators..."
    # If the indexer omits unclassified files entirely, random.md should not be in the manifest
    if echo "$MANIFEST" | grep -q "random.md"; then
        # It IS in the manifest — check the line doesn't claim a known type
        LINE=$(echo "$MANIFEST" | grep "random.md")
        if echo "$LINE" | grep -qi "specification\|verification\|test\|implementation\|evaluation\|review\|audit\|investigation\|investigation"; then
            echo "FAIL: random.md classified as a known type"
            echo "Line: $LINE"
            exit $TEST_FAILED
        fi
        echo "PASS: random.md listed but not classified as a known type"
    else
        echo "PASS: random.md excluded from manifest (unclassified)"
    fi
fi
echo "PASS: random.md falls through correctly"

echo "All tests passed."
exit $TEST_PASSED
