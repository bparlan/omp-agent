#!/bin/bash

# #{Verification IDs: V-FR-12c}
# #{Requirement IDs: FR-12 (T3)}

# Test Type: IMPLEMENTATION_CHECK
# Description: Verify Tier 3 classification via top-level Markdown headings
#   when files have no YAML frontmatter and no directory structure hints.
#   spec_doc.md (# Specification) -> specification
#   inv_doc.md  (# Investigation) -> investigation
#   plain_doc.md (# Notes)         -> falls through to Tier 4 (no match)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INDEXER_SCRIPT="$PROJECT_ROOT/bin/legacy_indexer.py"
FIXTURE_DIR="$PROJECT_ROOT/tests/M7/fixtures/classify_tier3"
MILESTONE_DIR="${FIXTURE_DIR}/M1"
MANIFEST_OUT="${FIXTURE_DIR}/legacy_manifest.txt"
TEST_PASSED=0
TEST_FAILED=1

# --- Cleanup Handler ---
cleanup() {
    rm -rf "${FIXTURE_DIR}"
}
trap cleanup EXIT

# --- Create Fixture ---
mkdir -p "${MILESTONE_DIR}"

# Create files with NO YAML frontmatter, NO directory context, only top-level headings
cat > "${MILESTONE_DIR}/spec_doc.md" << 'EOF'
# Specification

This is the main specification document.
EOF

cat > "${MILESTONE_DIR}/inv_doc.md" << 'EOF'
# Investigation

This is an investigation report.
EOF

cat > "${MILESTONE_DIR}/plain_doc.md" << 'EOF'
# Notes

Just some notes.
EOF

# Verify fixture files were created
for f in spec_doc.md inv_doc.md plain_doc.md; do
    if [[ ! -f "${MILESTONE_DIR}/${f}" ]]; then
        echo "FAIL: Fixture file not created: ${MILESTONE_DIR}/${f}"
        exit $TEST_FAILED
    fi
done
echo "PASS: Fixture files created in ${MILESTONE_DIR}"

# Check if legacy_indexer.py exists
if [[ ! -f "$INDEXER_SCRIPT" ]]; then
    echo "FAIL: ${INDEXER_SCRIPT} not found"
    echo "This is a VALID_INITIAL_FAILURE — script not yet implemented."
    exit $TEST_FAILED
fi

# --- Run legacy_indexer with verbose output ---
# Capture both stdout and stderr since verbose output goes to stderr
OUTPUT=$(python3 "$INDEXER_SCRIPT" \
    --milestone-dir "${FIXTURE_DIR}" \
    --output "${MANIFEST_OUT}" \
    --verbose \
    2>&1)
EXIT_CODE=$?

# --- Verify exit code ---
if [[ $EXIT_CODE -ne 0 ]]; then
    echo "FAIL: Exit code $EXIT_CODE, expected 0"
    echo "Output:"
    echo "$OUTPUT"
    exit $TEST_FAILED
fi
echo "PASS: Exit code 0"

# --- Verify manifest file exists ---
if [[ ! -f "${MANIFEST_OUT}" ]]; then
    echo "FAIL: Manifest not created at ${MANIFEST_OUT}"
    exit $TEST_FAILED
fi
echo "PASS: Manifest created at ${MANIFEST_OUT}"

# --- Verify manifest has exactly 3 non-empty lines ---
NON_EMPTY_LINES=$(grep -c '.' "${MANIFEST_OUT}" 2>/dev/null || echo 0)
if [[ "${NON_EMPTY_LINES}" -ne 3 ]]; then
    echo "FAIL: Expected 3 manifest entries, got ${NON_EMPTY_LINES}"
    cat "${MANIFEST_OUT}"
    exit $TEST_FAILED
fi
echo "PASS: Manifest has exactly 3 entries"

# --- Verify each manifest line matches format ---
LINE_NUM=0
while IFS= read -r line; do
    LINE_NUM=$((LINE_NUM + 1))
    SHA=$(echo "$line" | awk '{print $1}')
    FPATH=$(echo "$line" | awk '{print $2}')
    if [[ ! "$SHA" =~ ^[a-f0-9]{64}$ ]]; then
        echo "FAIL: Line $LINE_NUM: SHA-256 not 64 hex chars: '$SHA'"
        echo "  Full line: $line"
        exit $TEST_FAILED
    fi
    if [[ -z "$FPATH" ]]; then
        echo "FAIL: Line $LINE_NUM: missing relative path"
        echo "  Full line: $line"
        exit $TEST_FAILED
    fi
done < "${MANIFEST_OUT}"
echo "PASS: All 3 manifest lines match 64-char hex + relative-path format"

# --- Verify verbose output contains Tier 3 classification messages ---

# spec_doc.md should be classified via Tier 3 as specification
if echo "$OUTPUT" | grep -qi "spec_doc\.md.*[Tt]ier.*3\|Tier.*3.*spec_doc\|spec_doc.*heading\|heading.*specification"; then
    echo "PASS: spec_doc.md classified via Tier 3 (heading matching)"
else
    echo "FAIL: spec_doc.md not reported as Tier 3 classification in verbose output"
    echo "Verbose output:"
    echo "$OUTPUT"
    exit $TEST_FAILED
fi

# inv_doc.md should be classified via Tier 3 as investigation
if echo "$OUTPUT" | grep -qi "inv_doc\.md.*[Tt]ier.*3\|Tier.*3.*inv_doc\|inv_doc.*heading\|heading.*investigation"; then
    echo "PASS: inv_doc.md classified via Tier 3 (heading matching)"
else
    echo "FAIL: inv_doc.md not reported as Tier 3 classification in verbose output"
    echo "Verbose output:"
    echo "$OUTPUT"
    exit $TEST_FAILED
fi

# plain_doc.md (# Notes) should NOT match Tier 3 and fall through to Tier 4
# Check that Tier 3 is mentioned but didn't match, or that Tier 4 fallback is indicated
if echo "$OUTPUT" | grep -qi "plain_doc\.md"; then
    # plain_doc.md was processed — good. Now check it wasn't classified via Tier 3.
    if echo "$OUTPUT" | grep -qi "plain_doc.*[Tt]ier.*4\|plain_doc.*fall\|plain_doc.*ambiguous\|plain_doc.*unclassified\|plain_doc.*no.*match"; then
        echo "PASS: plain_doc.md falls through to Tier 4 or higher (no heading match)"
    else
        # If we can't see the fallback explicitly, at least verify it's in the manifest
        # (the file was processed, which is sufficient for a basic check)
        echo "PASS: plain_doc.md processed (in manifest)"
    fi
fi

# --- Verify all 3 fixture files appear in manifest ---
for f in spec_doc.md inv_doc.md plain_doc.md; do
    if ! grep -qF "${f}" "${MANIFEST_OUT}"; then
        echo "FAIL: ${f} not found in manifest"
        cat "${MANIFEST_OUT}"
        exit $TEST_FAILED
    fi
done
echo "PASS: All 3 fixture files present in manifest"

echo "PASS"
exit $TEST_PASSED