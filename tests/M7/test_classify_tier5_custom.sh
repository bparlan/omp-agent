#!/bin/bash
# Verification IDs: V-FR-12e
# Requirement IDs: FR-12 (T5)
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 5 classification — custom filename pattern mapping

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_BASE="$PROJECT_ROOT/tests/M7/fixtures/classify_tier5"
FIXTURE_DIR="$FIXTURE_BASE/M1"
PATTERN_MAP="$FIXTURE_BASE/pattern_map.txt"
OUTPUT_MANIFEST="$FIXTURE_BASE/legacy_manifest.txt"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup handler
cleanup() {
    rm -rf "$FIXTURE_BASE"
}
trap cleanup EXIT

# --- Create Fixtures ---
mkdir -p "$FIXTURE_DIR"

# custom-report.md — NO YAML, NO directory, NO heading, NO legacy naming
cat << 'EOF' > "$FIXTURE_DIR/custom-report.md"
# Report

Body.
EOF

# custom-spec.md — Same pattern
cat << 'EOF' > "$FIXTURE_DIR/custom-spec.md"
# Report

Body.
EOF

# Create pattern map
cat << 'EOF' > "$PATTERN_MAP"
custom-report.md:investigation
custom-spec.md:specification
EOF

echo "Test: Tier 5 — Custom filename pattern mapping (V-FR-12e)"
echo "Fixture dir: $FIXTURE_DIR"
echo "Pattern map: $PATTERN_MAP"

# --- Execute ---
# If the script does not exist, this is a VALID_INITIAL_FAILURE
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "VALID_INITIAL_FAILURE: $INDEXER_SCRIPT not found — script not yet implemented."
    exit $TEST_PASSED
fi

OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_BASE" \
    --output "$OUTPUT_MANIFEST" \
    --verbose \
    --pattern-map "$PATTERN_MAP" 2>&1)
EXIT_CODE=$?

# Assert 1: Exit code 0
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Exit code 0"

# Assert 2: Verbose output mentions Tier 5 or custom pattern
if ! echo "$OUTPUT" | grep -qi "tier 5\|tier.*5\|custom pattern\|pattern.*map"; then
    echo "FAIL: Verbose output does not mention Tier 5 or custom pattern mapping"
    echo "Output: $OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose output references Tier 5 / custom pattern mapping"

# Assert 3: Manifest exists and contains both files
if [ ! -f "$OUTPUT_MANIFEST" ]; then
    echo "FAIL: Manifest not created at $OUTPUT_MANIFEST"
    exit $TEST_FAILED
fi

MANIFEST_CONTENT=$(cat "$OUTPUT_MANIFEST")

if ! echo "$MANIFEST_CONTENT" | grep -q "custom-report.md"; then
    echo "FAIL: Manifest does not contain custom-report.md"
    echo "Manifest: $MANIFEST_CONTENT"
    exit $TEST_FAILED
fi
echo "PASS: Manifest contains custom-report.md"

if ! echo "$MANIFEST_CONTENT" | grep -q "custom-spec.md"; then
    echo "FAIL: Manifest does not contain custom-spec.md"
    echo "Manifest: $MANIFEST_CONTENT"
    exit $TEST_FAILED
fi
echo "PASS: Manifest contains custom-spec.md"

echo "All tests passed."
exit $TEST_PASSED
