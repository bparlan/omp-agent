#!/bin/bash
# Test k: Verify validity gate correctly identifies dirty working tree as INVALID

set -e

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Mock validity gate that checks git status (validity criterion #4)
validity_gate_git() {
    local git_dir="$1"

    # Check if git repository exists
    if [[ ! -d "$git_dir/.git" ]]; then
        echo "UNCERTAIN"
        return 0
    fi

    # Check git status for uncommitted changes
    cd "$git_dir" || exit 1
    if git diff --quiet && git diff --cached --quiet; then
        echo "VALID_TEST"
        return 0
    else
        echo "INVALID_TEST"
        return 0
    fi
}

# Test 1: Clean tree should be VALID
echo "Test 1: Clean working tree should be VALID"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a temporary git repository
temp_git_dir=$(mktemp -d)
cd "$temp_git_dir" || exit 1

# Initialize git repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

# Create an initial file
echo "initial content" > test.txt
git add test.txt
git commit -m "Initial commit"

# Test with clean repository
verdict=$(validity_gate_git "$temp_git_dir")
if [[ "$verdict" == "VALID_TEST" ]]; then
    echo "  ✓ Clean tree correctly identified as VALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Clean tree should be VALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Dirty tree (uncommitted changes) should be INVALID
echo "Test 2: Dirty working tree should be INVALID"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a new uncommitted file
echo "uncommitted content" >> test.txt

# Test with dirty repository
verdict=$(validity_gate_git "$temp_git_dir")
if [[ "$verdict" == "INVALID_TEST" ]]; then
    echo "  ✓ Dirty tree correctly identified as INVALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Dirty tree should be INVALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Dirty tree (staged changes) should be INVALID
echo "Test 3: Staged changes should be INVALID"
TESTS_RUN=$((TESTS_RUN + 1))

# Create a new file and stage it
echo "staged content" > staged.txt
git add staged.txt

# Test with staged changes
verdict=$(validity_gate_git "$temp_git_dir")
if [[ "$verdict" == "INVALID_TEST" ]]; then
    echo "  ✓ Staged changes correctly identified as INVALID"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo "  ✗ FAILED: Staged changes should be INVALID, got $verdict"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Summary
echo "TESTS_RUN=$TESTS_RUN"
echo "TESTS_PASSED=$TESTS_PASSED"
echo "TESTS_FAILED=$TESTS_FAILED"

# Cleanup
cd - > /dev/null || true
rm -rf "$temp_git_dir" 2>/dev/null || true

if [[ $TESTS_FAILED -eq 0 ]]; then
    exit 0
else
    exit 1
fi
