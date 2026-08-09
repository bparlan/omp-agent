#!/bin/bash
# Verification IDs: V-NFR-5
# Requirement IDs: NFR-5
# Test Type: IMPLEMENTATION_CHECK
# Description: Verify post-execution SHA-256 checksum integrity of M1-M9 files against legacy manifest

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/integrity"
TEST_PASSED=0
TEST_FAILED=1

# Cleanup handler — remove fixture dir on exit
cleanup() {
    rm -rf "$FIXTURE_DIR"
}
trap cleanup EXIT

# Create fixture directory structure
mkdir -p "$FIXTURE_DIR/M1"

# Create fixture files with distinct content
cat > "$FIXTURE_DIR/M1/M1S1.md" << 'EOF'
---
id: SPEC-001
type: specification
---
# Specification

This is a pre-M10 specification artifact for integrity verification.
EOF

cat > "$FIXTURE_DIR/M1/M1S1V.md" << 'EOF'
---
id: VER-001
type: verification
---
# Verification

This is a pre-M10 verification artifact for integrity verification.
EOF

# Check if legacy_indexer.py exists
if [ ! -f "$INDEXER_SCRIPT" ]; then
    echo "FAIL: legacy_indexer.py not found at $INDEXER_SCRIPT"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# Step 1: Run legacy_indexer.py to generate legacy_manifest.txt
echo "Test 1: Generate legacy manifest with legacy_indexer.py..."
MANIFEST_OUTPUT="$FIXTURE_DIR/legacy_manifest.txt"
INDEXER_OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "$FIXTURE_DIR" \
    --output "$MANIFEST_OUTPUT" \
    2>&1)
INDEXER_EXIT=$?

if [ $INDEXER_EXIT -ne 0 ]; then
    echo "FAIL: legacy_indexer.py exited with code $INDEXER_EXIT"
    echo "Output: $INDEXER_OUTPUT"
    echo "This is a VALID_INITIAL_FAILURE — manifest generation failed."
    exit $TEST_FAILED
fi

if [ ! -f "$MANIFEST_OUTPUT" ]; then
    echo "FAIL: legacy_manifest.txt was not created at $MANIFEST_OUTPUT"
    exit $TEST_FAILED
fi

echo "PASS: legacy_indexer.py generated manifest successfully"

# Step 2: Verify manifest integrity — recompute SHA-256 for each file and compare
echo "Test 2: Verify checksum integrity against legacy manifest..."
VERIFY_OUTPUT=$(python3 -c "
import hashlib, os
manifest = '$MANIFEST_OUTPUT'
base = '$FIXTURE_DIR'
mismatches = []
with open(manifest) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        expected_hash, rel_path = line.split(' ', 1)
        full_path = os.path.join(base, rel_path)
        if not os.path.isfile(full_path):
            mismatches.append(f'{rel_path}: file not found')
            continue
        actual_hash = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
        if actual_hash != expected_hash:
            mismatches.append(f'{rel_path}: expected {expected_hash}, got {actual_hash}')
if mismatches:
    print('MISMATCHES:', '\n'.join(mismatches))
    exit(1)
else:
    print('ALL MATCH')
    exit(0)
" 2>&1)
VERIFY_EXIT=$?

if [ $VERIFY_EXIT -ne 0 ]; then
    echo "FAIL: Checksum verification failed (exit code $VERIFY_EXIT)"
    echo "Output: $VERIFY_OUTPUT"
    exit $TEST_FAILED
fi

if ! echo "$VERIFY_OUTPUT" | grep -q "ALL MATCH"; then
    echo "FAIL: Verification output did not contain 'ALL MATCH'"
    echo "Output: $VERIFY_OUTPUT"
    exit $TEST_FAILED
fi

echo "PASS: $VERIFY_OUTPUT"

echo "All tests passed."
exit $TEST_PASSED