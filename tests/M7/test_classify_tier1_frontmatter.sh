#!/bin/bash
# Verification IDs: V-FR-12a
# Requirement IDs: FR-12 (T1)
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 1 classification (YAML frontmatter metadata)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/classify_tier1"
MILESTONE_DIR="$FIXTURE_DIR/M1"
MANIFEST_OUT="$FIXTURE_DIR/legacy_manifest.txt"
TEST_PASSED=0
TEST_FAILED=1

# --- Cleanup handler ---
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# --- Fixture Setup ---
mkdir -p "$MILESTONE_DIR"

# Create spec.md with YAML frontmatter
cat > "$MILESTONE_DIR/spec.md" << 'SPECEOF'
---
id: SPEC-001
type: specification
---
# Specification

Body text.
SPECEOF

# Create ver.md with YAML frontmatter
cat > "$MILESTONE_DIR/ver.md" << 'VEREOF'
---
id: VER-001
type: verification
---
# Verification

Body text.
VEREOF

echo "=== V-FR-12a: Tier 1 (frontmatter) classification ==="

# --- Run legacy_indexer.py ---
# Implementation may not exist yet => valid initial failure (exit 127 or 1 is okay)
OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_DIR" \
    --output "$MANIFEST_OUT" \
    --verbose 2>&1)
EXIT_CODE=$?

# Check exit code 0 (PASS) or non-zero (VALID_INITIAL_FAILURE)
if [ $EXIT_CODE -ne 0 ]; then
    echo "IMPLEMENTATION NOT FOUND (exit code $EXIT_CODE): script not yet implemented"
    echo "This is a VALID_INITIAL_FAILURE for IMPLEMENTATION_CHECK type."
    echo "Output was:"
    echo "$OUTPUT"
    echo "FAIL: V-FR-12a - legacy_indexer.py not yet functional"
    exit $TEST_FAILED
fi

# --- Assertions ---

# Assert 1: Verbose output mentions Tier 1 or frontmatter
if ! echo "$OUTPUT" | grep -qi "Tier 1\|frontmatter\|Tier1"; then
    echo "ASSERTION FAILURE (V-FR-12a): Verbose output does not mention Tier 1/frontmatter"
    echo "Output was:"
    echo "$OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Verbose output indicates Tier 1 classification"

# Assert 2: Manifest file was created
if [ ! -f "$MANIFEST_OUT" ]; then
    echo "ASSERTION FAILURE (V-FR-12a): Manifest file not created at $MANIFEST_OUT"
    exit $TEST_FAILED
fi
echo "PASS: Manifest file created"

# Assert 3: Both files appear in manifest with SHA-256 checksums
MANIFEST_CONTENT=$(cat "$MANIFEST_OUT")
if ! echo "$MANIFEST_CONTENT" | grep -q "SPEC-001"; then
    echo "ASSERTION FAILURE (V-FR-12a): SPEC-001 not found in manifest"
    echo "Manifest content:"
    echo "$MANIFEST_CONTENT"
    exit $TEST_FAILED
fi
echo "PASS: SPEC-001 found in manifest"

if ! echo "$MANIFEST_CONTENT" | grep -q "VER-001"; then
    echo "ASSERTION FAILURE (V-FR-12a): VER-001 not found in manifest"
    echo "Manifest content:"
    echo "$MANIFEST_CONTENT"
    exit $TEST_FAILED
fi
echo "PASS: VER-001 found in manifest"

# Assert 4: Manifest entries contain SHA-256 checksums (64 hex chars)
if ! echo "$MANIFEST_CONTENT" | grep -qE '[a-f0-9]{64}'; then
    echo "ASSERTION FAILURE (V-FR-12a): Manifest entries missing SHA-256 checksums"
    echo "Manifest content:"
    echo "$MANIFEST_CONTENT"
    exit $TEST_FAILED
fi
echo "PASS: Manifest entries contain SHA-256 checksums"

echo "All assertions passed."
echo "PASS: V-FR-12a"
exit $TEST_PASSED
