#!/bin/bash
# Verification IDs: V-FR-6, V-FR-10
# Requirement IDs: FR-6, FR-10
# Test Type: SPECIFICATION_CHECK
# Description: Verify docs/ARTIFACT_ARCHITECTURE.md contains formalized contract

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ARCH_DOC="$PROJECT_ROOT/docs/ARTIFACT_ARCHITECTURE.md"
TEST_PASSED=0
TEST_FAILED=1

# Self-validity check
if [ ! -f "$ARCH_DOC" ]; then
    echo "FAIL: ARTIFACT_ARCHITECTURE.md not found at $ARCH_DOC"
    echo "This is a VALID_INITIAL_FAILURE — document not yet updated."
    exit $TEST_FAILED
fi

# Read the document
CONTENT=$(cat "$ARCH_DOC")

# Test 1: FR-6 — Canonical directory structure contract
echo "Test 1: FR-6 — Canonical directory structure..."

# Check for definitive language (not "Proposed" or "Future")
if echo "$CONTENT" | grep -qi "proposed\|future\|idea\|draft"; then
    echo "WARNING: Document contains provisional language ('Proposed', 'Future', 'Idea')"
    echo "This may indicate the contract is not yet formalized."
fi

# Check for base path pattern
if ! echo "$CONTENT" | grep -qi "milestones.*{M_ID}\|milestones.*M{X}"; then
    echo "FAIL: Document does not define milestone directory structure"
    exit $TEST_FAILED
fi

# Check for type subdirectory names
TYPE_DIRS_FOUND=0
for dir in specifications verifications tests investigations implementations evaluations reviews audits; do
    if echo "$CONTENT" | grep -q "$dir"; then
        TYPE_DIRS_FOUND=$((TYPE_DIRS_FOUND + 1))
    fi
done
if [ $TYPE_DIRS_FOUND -lt 4 ]; then
    echo "FAIL: Document defines fewer than 4 type subdirectories (found: $TYPE_DIRS_FOUND)"
    exit $TEST_FAILED
fi
echo "PASS: Canonical directory structure defined ($TYPE_DIRS_FOUND/8 type subdirectories)"

# Test 2: FR-10 — Resolution priority references
echo "Test 2: FR-10 — Resolution priority references..."
if ! echo "$CONTENT" | grep -qi "3-tier\|three.*tier\|resolution.*priority\|priority.*resolution\|tier.*1\|tier.*2\|tier.*3"; then
    echo "FAIL: Document does not reference 3-tier resolution priority"
    exit $TEST_FAILED
fi
echo "PASS: Resolution priority referenced"

# Test 3: FR-10 — Conflict detection reference
echo "Test 3: FR-10 — Conflict detection reference..."
if ! echo "$CONTENT" | grep -qi "conflict.*detect\|disagreement\|type.*mismatch\|directory.*disagree"; then
    echo "FAIL: Document does not reference conflict detection"
    exit $TEST_FAILED
fi
echo "PASS: Conflict detection referenced"

# Test 4: FR-10 — Dual query support reference
echo "Test 4: FR-10 — Dual query support reference..."
if ! echo "$CONTENT" | grep -qi "canonical.*id\|legacy.*id\|dual.*query\|both.*canonical.*legacy"; then
    echo "FAIL: Document does not reference dual query support (canonical + legacy IDs)"
    exit $TEST_FAILED
fi
echo "PASS: Dual query support referenced"

echo "All tests passed."
exit $TEST_PASSED