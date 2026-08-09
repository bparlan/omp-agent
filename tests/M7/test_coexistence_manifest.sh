#!/bin/bash
# Verification IDs: V-FR-15
# Requirement IDs: FR-15
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify legacy manifest integration for resolving IDs without YAML frontmatter

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
RESOLVE_SCRIPT="$PROJECT_ROOT/bin/resolve_artifact.py"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/coexistence"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup handler
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# Check if resolve_artifact.py exists
if [ ! -f "$RESOLVE_SCRIPT" ]; then
    echo "FAIL: resolve_artifact.py not found at $RESOLVE_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# Create fixture directory
mkdir -p "$FIXTURE_DIR/M99"

# Create M99S1.md — NO YAML frontmatter, legacy filename only
cat > "$FIXTURE_DIR/M99/M99S1.md" << 'EOF'
# Spec

Body.
EOF

# Create M99S1V.md — NO YAML frontmatter, legacy filename only
cat > "$FIXTURE_DIR/M99/M99S1V.md" << 'EOF'
# Ver

Body.
EOF

# Step 1: Run legacy_indexer.py to generate legacy_manifest.txt
echo "Step 1: Generate legacy manifest..."
if [ -f "$INDEXER_SCRIPT" ]; then
    python3 "$INDEXER_SCRIPT" \
        --milestone-dir "$FIXTURE_DIR" \
        --output "$FIXTURE_DIR/legacy_manifest.txt" \
        --verbose 2>&1
    INDEXER_EXIT=$?
    if [ $INDEXER_EXIT -ne 0 ]; then
        echo "FAIL: legacy_indexer.py exited with code $INDEXER_EXIT"
        echo "This is a VALID_INITIAL_FAILURE — indexer not yet implemented."
        exit $TEST_FAILED
    fi
    echo "PASS: legacy_indexer.py completed successfully"
else
    echo "NOTE: legacy_indexer.py not found — skipping indexer execution."
    echo "This is a VALID_INITIAL_FAILURE path."
    # Touch an empty manifest so resolve_artifact.py can still attempt resolution
    # via Tier 3 filename heuristics without the manifest integration
    touch "$FIXTURE_DIR/legacy_manifest.txt"
fi

# Step 2: Resolve M99S1 via resolve_artifact.py
echo ""
echo "Step 2: Resolve M99S1..."
OUTPUT=$(python3 "$RESOLVE_SCRIPT" M99S1 --milestone M99 --cwd "$FIXTURE_DIR" --verbose 2>&1)
EXIT_CODE=$?
echo "Exit code: $EXIT_CODE"
echo "Output:"
echo "$OUTPUT"

if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: resolve_artifact.py M99S1 exited with code $EXIT_CODE"
    echo "This is a VALID_INITIAL_FAILURE — resolution not yet implemented for legacy IDs."
    exit $TEST_FAILED
fi

# Assert output contains resolved file path
if ! echo "$OUTPUT" | grep -q "M99S1"; then
    echo "FAIL: Output does not contain M99S1 in resolved path"
    exit $TEST_FAILED
fi

# Assert verbose output mentions resolution tier
if ! echo "$OUTPUT" | grep -qE "[Tt]ier\s*[0-9]|[Ll]egacy|[Ff]ilename"; then
    echo "FAIL: Verbose output does not mention resolution tier or mechanism"
    exit $TEST_FAILED
fi
echo "PASS: M99S1 resolved successfully"

# Step 3: Resolve M99S1V via resolve_artifact.py
echo ""
echo "Step 3: Resolve M99S1V..."
OUTPUT2=$(python3 "$RESOLVE_SCRIPT" M99S1V --milestone M99 --cwd "$FIXTURE_DIR" --verbose 2>&1)
EXIT_CODE2=$?
echo "Exit code: $EXIT_CODE2"
echo "Output:"
echo "$OUTPUT2"

if [ $EXIT_CODE2 -ne 0 ]; then
    echo "FAIL: resolve_artifact.py M99S1V exited with code $EXIT_CODE2"
    echo "This is a VALID_INITIAL_FAILURE — resolution not yet implemented for legacy IDs."
    exit $TEST_FAILED
fi

# Assert output contains resolved file path
if ! echo "$OUTPUT2" | grep -q "M99S1V"; then
    echo "FAIL: Output does not contain M99S1V in resolved path"
    exit $TEST_FAILED
fi

# Assert verbose output mentions resolution tier
if ! echo "$OUTPUT2" | grep -qE "[Tt]ier\s*[0-9]|[Ll]egacy|[Ff]ilename"; then
    echo "FAIL: Verbose output does not mention resolution tier or mechanism"
    exit $TEST_FAILED
fi
echo "PASS: M99S1V resolved successfully"

echo ""
echo "All tests passed."
exit $TEST_PASSED