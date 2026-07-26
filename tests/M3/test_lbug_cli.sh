#!/bin/bash
# FR-1: lbug CLI Installation & PATH Verification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="/tmp/test-lbug-cli-$$"
VERBOSE=false

# Parse arguments
if [[ "$1" == "--verbose" ]]; then
    VERBOSE=true
fi

echo "Testing lbug CLI installation..."

# Test 1: Check if lbug command exists
echo "  [Test 1] Checking if 'lbug' command is available..."
if ! command -v lbug &> /dev/null; then
    echo "  ✗ FAILED: 'lbug' command not found"
    exit 1
else
    echo "  ✓ lbug command found in PATH"
fi

# Test 2: Get version information
echo "  [Test 2] Retrieving lbug version..."
VERSION_OUTPUT=$(lbug --version 2>&1)
if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: 'lbug --version' failed"
    echo "    Output: $VERSION_OUTPUT"
    exit 1
fi

echo "  ✓ lbug --version succeeded"
echo "    Version: $VERSION_OUTPUT"

# Test 3: Confirm PATH includes installation directory
echo "  [Test 3] Verifying PATH includes lbug installation..."
PATH_DIR=$(which lbug)
echo "    lbug location: $PATH_DIR"

if [ -z "$PATH_DIR" ]; then
    echo "  ✗ FAILED: lbug location not found in PATH"
    exit 1
fi

# Test 4: Test from fresh shell environment
echo "  [Test 4] Testing from fresh shell (simulating agent session)..."

# Create a fresh subshell
SHELL_OUTPUT=$(bash -c "lbug --version 2>&1" 2>&1)
if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: lbug not accessible from fresh shell"
    echo "    Output: $SHELL_OUTPUT"
    exit 1
fi

echo "  ✓ lbug accessible from fresh shell"
echo "    Fresh shell version: $SHELL_OUTPUT"

# Test 5: Test lbug --help
echo "  [Test 5] Testing lbug --help..."
HELP_OUTPUT=$(lbug --help 2>&1)
if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: 'lbug --help' failed"
    echo "    Output: $HELP_OUTPUT"
    exit 1
fi

echo "  ✓ lbug --help succeeded"
echo "    Help output (first 5 lines):"
echo "$HELP_OUTPUT" | head -5

echo ""
echo "  ✓ All FR-1 tests PASSED"
echo ""
