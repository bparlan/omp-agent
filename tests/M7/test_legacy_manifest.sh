#!/bin/bash

# #{Verification IDs: V-FR-11}
# #{Requirement IDs: FR-11}

# Test Type: IMPLEMENTATION_CHECK
# Tests that legacy_indexer.py produces a manifest of 64-char hex + relative path for each file.

set -euo pipefail

# --- Test Configuration ---
SCRIPT="bin/legacy_indexer.py"
FIXTURE_BASE="tests/M7/fixtures/legacy_indexer"
MILESTONE_DIR="${FIXTURE_BASE}/M1"
MANIFEST_OUT="${FIXTURE_BASE}/legacy_manifest.txt"

# --- Cleanup Handler ---
cleanup() {
    rm -rf "${FIXTURE_BASE}"
}
trap cleanup EXIT

# --- Create Fixture ---
mkdir -p "${MILESTONE_DIR}"

# Create three milestone files with distinct content
echo "spec content" > "${MILESTONE_DIR}/M1S1.md"
echo "verification content" > "${MILESTONE_DIR}/M1S1V.md"
echo "test content" > "${MILESTONE_DIR}/M1S1T1.md"

# Verify fixture files were created
for f in M1S1.md M1S1V.md M1S1T1.md; do
    if [[ ! -f "${MILESTONE_DIR}/${f}" ]]; then
        echo "FAIL: Failed to create fixture file ${MILESTONE_DIR}/${f}"
        exit 1
    fi
done

# --- Run legacy_indexer ---
# On missing implementation, the command will fail naturally (exit code 127/1) = VALID_INITIAL_FAILURE
python3 "$SCRIPT" --milestone-dir "${MILESTONE_DIR}" --output "${MANIFEST_OUT}" || {
    rc=$?
    echo "IMPLEMENTATION FAILURE: ${SCRIPT} exited with code ${rc} (VALID_INITIAL_FAILURE — expected when script is not yet implemented)"
    echo "FAIL"
    exit 1
}

# --- Verify exit code ---
# If we reach here, the script exited 0 (set -e would have caught non-zero)
echo "PASS: ${SCRIPT} exited with code 0"

# --- Verify manifest file exists ---
if [[ ! -f "${MANIFEST_OUT}" ]]; then
    echo "FAIL: Manifest file '${MANIFEST_OUT}' was not created"
    exit 1
fi
echo "PASS: Manifest file exists at ${MANIFEST_OUT}"

# --- Verify manifest has exactly 3 non-empty lines ---
# Count non-empty lines
NON_EMPTY_LINES=$(grep -c '.' "${MANIFEST_OUT}" 2>/dev/null || echo 0)
if [[ "${NON_EMPTY_LINES}" -ne 3 ]]; then
    echo "FAIL: Expected 3 non-empty lines in manifest, got ${NON_EMPTY_LINES}"
    exit 1
fi
echo "PASS: Manifest has exactly 3 non-empty lines"

# --- Verify each line matches 64-char hex + space + relative path ---
LINE_NUM=0
while IFS= read -r line; do
    LINE_NUM=$((LINE_NUM + 1))
    # Skip empty lines (already validated count above, but be safe)
    [[ -z "$line" ]] && continue

    # Format: 64 hex chars, space, relative path (no leading ./)
    if [[ ! "$line" =~ ^[0-9a-f]{64}\ [^\ ]+$ ]]; then
        echo "FAIL: Line ${LINE_NUM} does not match format '64-char-hex <space> relative-path'"
        echo "  Got: '${line}'"
        exit 1
    fi

    # Extract the path part and verify it's relative to milestone dir
    hex_part="${line:0:64}"
    path_part="${line:66}"

    # Verify hex part is truly 64 characters
    if [[ "${#hex_part}" -ne 64 ]]; then
        echo "FAIL: Line ${LINE_NUM}: hex part is ${#hex_part} chars, expected 64"
        exit 1
    fi

    # Verify the path references a file inside the fixture
    full_path="${MILESTONE_DIR}/${path_part}"
    if [[ ! -f "${full_path}" ]]; then
        echo "FAIL: Line ${LINE_NUM}: referenced file '${path_part}' does not exist at '${full_path}'"
        exit 1
    fi
done < "${MANIFEST_OUT}"

echo "PASS: All 3 manifest lines match expected format"
echo "PASS"
exit 0
