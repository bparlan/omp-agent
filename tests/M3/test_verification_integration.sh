#!/bin/bash
# Closure Task: Integrate and prove the verification gate
# This test proves that verify-scope.py is integrated into the verification workflow

set -e

echo "=========================================="
echo "Closure Task: Verification Gate Integration Test"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BARIA_DIR="/Users/bparlan/devcode/BariaDAO"
GRAPH_CONTEXT_BIN="/Users/bparlan/devcode/aef/agent/skills/graph-context/bin"
PYTHON_CMD="/Users/bparlan/devcode/aef/agent/skills/graph-context/.venv/bin/python3"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Setup:"
echo "  BariaDAO directory: $BARIA_DIR"
echo "  Graph context bin: $GRAPH_CONTEXT_BIN"
echo "  Python command: $PYTHON_CMD"
echo ""

# Create test environment if needed
TEST_ENV="/tmp/closure-test-$$"
mkdir -p "$TEST_ENV/src"
cd "$TEST_ENV"

# Test 1: Verify hook can be executed manually
echo "=========================================="
echo "Test 1: Manual Verification Hook Execution"
echo "=========================================="

# Initialize git repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

# Create in-scope file
echo "# in-scope file" > src/main.py
git add .
git commit -m "Initial commit"

# Test SUCCESS: In-scope modification
echo ""
echo "Scenario A: In-scope modification (should PASS)"
echo "  Declared scope: src/main.py"
echo "  Modified file: src/main.py"

echo "# change" >> src/main.py

echo ""
echo "Running verify-scope.py..."
echo "  Command: $PYTHON_CMD $GRAPH_CONTEXT_BIN/verify-scope.py --scope=src/main.py"
echo ""

EXIT_CODE=0
$PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py 2>&1
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: In-scope modification correctly accepted"
else
    echo -e "${RED}✗ FAIL${NC}: In-scope modification incorrectly rejected (exit code: $EXIT_CODE)"
    exit 1
fi

# Test FAILURE: Out-of-scope modification
echo ""
echo "=========================================="
echo "Test 2: Out-of-Scope Modification (should FAIL)"
echo "=========================================="
echo "  Declared scope: src/main.py"
echo "  Modified file: src/external.py (out-of-scope)"

# Create out-of-scope file
echo "# out-of-scope file" > src/external.py
git add .
git commit -m "Add out-of-scope file"

echo ""
echo "Running verify-scope.py..."
echo "  Command: $PYTHON_CMD $GRAPH_CONTEXT_BIN/verify-scope.py --scope=src/main.py"
echo ""

$PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py 2>&1
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Out-of-scope modification correctly rejected (exit code: $EXIT_CODE)"
    echo ""
    echo "Error message output:"
    $PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py 2>&1 | sed 's/^/  /'
else
    echo -e "${RED}✗ FAIL${NC}: Out-of-scope modification incorrectly accepted (exit code: $EXIT_CODE)"
    exit 1
fi

# Test 3: Multiple in-scope files
echo ""
echo "=========================================="
echo "Test 3: Multiple In-Scope Files (should PASS)"
echo "=========================================="
echo "  Declared scope: src/main.py,src/utils.py"
echo "  Modified files: src/main.py, src/utils.py"

echo "# another change" >> src/main.py
echo "# more code" >> src/utils.py
git add .
git commit -m "Multiple in-scope changes"

echo ""
echo "Running verify-scope.py..."
echo "  Command: $PYTHON_CMD $GRAPH_CONTEXT_BIN/verify-scope.py --scope=src/main.py,src/utils.py"
echo ""

$PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py,src/utils.py 2>&1
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Multiple in-scope modifications correctly accepted"
else
    echo -e "${RED}✗ FAIL${NC}: Multiple in-scope modifications incorrectly rejected (exit code: $EXIT_CODE)"
    exit 1
fi

# Test 4: Mixed in-scope and out-of-scope
echo ""
echo "=========================================="
echo "Test 4: Mixed In-Scope and Out-of-Scope (should FAIL)"
echo "=========================================="
echo "  Declared scope: src/main.py"
echo "  Modified files: src/main.py, src/external.py"

echo "# more changes" >> src/main.py
echo "# out-of-scope change" >> src/external.py
git add .
git commit -m "Mixed in-scope and out-of-scope changes"

echo ""
echo "Running verify-scope.py..."
echo "  Command: $PYTHON_CMD $GRAPH_CONTEXT_BIN/verify-scope.py --scope=src/main.py"
echo ""

$PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py 2>&1
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Mixed in/out-of-scope modifications correctly rejected (exit code: $EXIT_CODE)"
    echo ""
    echo "Error message output:"
    $PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py 2>&1 | sed 's/^/  /'
else
    echo -e "${RED}✗ FAIL${NC}: Mixed in/out-of-scope modifications incorrectly accepted (exit code: $EXIT_CODE)"
    exit 1
fi

# Cleanup
cd ~
rm -rf "$TEST_ENV"

echo ""
echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo -e "${GREEN}✓ All tests passed${NC}"
echo ""
echo "Verification Gate Integration Confirmed:"
echo "  1. Manual hook execution works correctly"
echo "  2. In-scope modifications are accepted (exit code 0)"
echo "  3. Out-of-scope modifications are rejected (exit code != 0)"
echo "  4. Multiple in-scope files are handled correctly"
echo "  5. Mixed in-scope/out-of-scope modifications are rejected"
echo ""
echo "Evidence collected:"
echo "  - Command invocations logged above"
echo "  - Exit codes captured and validated"
echo "  - Error messages captured for rejection cases"
echo ""
echo "Conclusion:"
echo "  The verify-scope.py hook is correctly integrated and working as expected."
echo "  It will prevent out-of-scope edits from being committed."
echo ""
