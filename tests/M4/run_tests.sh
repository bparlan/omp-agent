#!/bin/bash
# Test runner script for M4S1 pre-implementation orchestration tests

set -e

echo "=== Running M4S1 Pre-Implementation Orchestration Tests ==="
echo ""

# Navigate to test directory
cd ~/devcode/aef/agent

# Run all M4S1 tests
echo "Running all M4S1 tests..."
pytest tests/M4/ -v --tb=short

echo ""
echo "=== Test Execution Complete ==="
