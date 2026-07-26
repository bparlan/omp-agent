#!/bin/bash
# FR-2: Python Client Installation

set -e

echo "Testing Python client installation..."

# Test 1: Check if ladybug is importable
echo "  [Test 1] Checking if 'ladybug' can be imported..."
timeout 5 python -c "import ladybug; print(ladybug.__version__)" 2>&1 || {
    echo "  ✗ FAILED: ImportError raised when importing ladybug"
    echo "    Error: $PYTHON_OUTPUT"
    exit 1
}

echo "  ✓ ladybug module imported successfully"
echo "    Version: $PYTHON_OUTPUT"

# Test 2: Check if ladybug is in uv packages
echo "  [Test 2] Checking if ladybug is in uv package list..."
UV_LIST=$(cd ~/devcode/aef/agent && uv list 2>&1 | grep -i ladybug || true)
if [ -z "$UV_LIST" ]; then
    echo "  ⚠ WARNING: ladybug not found in 'uv list' output"
    echo "    This may indicate ladybug is not properly installed via uv"
    # Don't fail here, as ladybug might be installed via pip directly
else
    echo "  ✓ ladybug found in uv packages:"
    echo "$UV_LIST"
fi

# Test 3: Test basic functionality
echo "  [Test 3] Testing basic ladybug functionality..."
timeout 5 python -c "
import ladybug
from ladybug import Graph
print('ladybug Graph class imported successfully')
print(f'ladybug version: {ladybug.__version__}')
" 2>&1 || {
    echo "  ✗ FAILED: Basic functionality test failed"
    echo "    Error: $PYTHON_TEST"
    exit 1
}

echo "  ✓ Basic functionality test passed"
echo "    Output:"
echo "$PYTHON_TEST" | sed 's/^/    /'

echo ""
echo "  ✓ All FR-2 tests PASSED"
echo ""
