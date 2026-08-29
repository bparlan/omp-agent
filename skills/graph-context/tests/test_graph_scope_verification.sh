#!/usr/bin/env bash
# Integration tests for graph-based scope verification
# Tests verify-scope.py with various scopes and file modifications

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="/Users/bparlan/devcode/BariaDAO"
VERIFY_SCRIPT="$SCRIPT_DIR/../bin/verify-scope.py"
LBUG_GRAPH="$PROJECT_DIR/.omp/graph/baria.lbug"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local scope="$2"
    local files_to_modify="$3"
    local expected_result="$4"  # "pass" or "fail"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${YELLOW}Test $TESTS_RUN: $test_name${NC}"
    echo "Scope: $scope"
    echo "Files: $files_to_modify"
    echo "Expected: $expected_result"

    # Reset git state
    cd "$PROJECT_DIR"
    git reset --hard HEAD 2>/dev/null || true

    # Create test files
    for file in $files_to_modify; do
        if [ -f "$file" ]; then
            echo "# Test content" >> "$file"
            git add "$file"
        else
            echo "# Test content" > "$file"
            git add "$file"
        fi
    done
    # Run verification
    if [ "$expected_result" == "pass" ]; then
        if python3 "$VERIFY_SCRIPT" --scope="$scope" --graph > /dev/null 2>&1; then
            echo -e "${GREEN}✓ PASSED${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}✗ FAILED${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        if python3 "$VERIFY_SCRIPT" --scope="$scope" --graph > /dev/null 2>&1; then
            echo -e "${RED}✗ FAILED (should have failed)${NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        else
            echo -e "${GREEN}✓ PASSED${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        fi
    fi
}

# Main test suite
echo "========================================"
echo "Graph Scope Verification Integration Tests"
echo "========================================"

# Test 1: In-scope modification with directory scope (pass)
run_test \
    "In-scope modification with directory scope" \
    "$PROJECT_DIR/src/" \
    "src/app_routes.py src/data/content_loader.py" \
    "pass"

# Test 2: Out-of-scope modification (fail)
run_test \
    "Out-of-scope modification" \
    "$PROJECT_DIR/src/" \
    "tests/test_example.py" \
    "fail"

# Test 3: Specific file scope (pass)
run_test \
    "Specific file scope - app_routes.py" \
    "$PROJECT_DIR/src/app_routes.py" \
    "src/app_routes.py" \
    "pass"

# Test 4: Multiple file scope (pass)
run_test \
    "Multiple file scope" \
    "$PROJECT_DIR/src/app_routes.py,$PROJECT_DIR/src/data/content_loader.py" \
    "src/data/content_loader.py src/app_routes.py" \
    "pass"

# Test 5: File not reachable from scope (fail)
run_test \
    "File not reachable from scope" \
    "$PROJECT_DIR/src/app_routes.py,$PROJECT_DIR/src/data/" \
    "src/config.py" \
    "fail"

# Test 6: No files modified (pass)
run_test \
    "No files modified" \
    "$PROJECT_DIR/src/" \
    "" \
    "pass"

# Test 7: Directory scope with unreachable file (fail)
run_test \
    "Directory scope with unreachable file" \
    "$PROJECT_DIR/src/" \
    "src/app_routes.py tests/test_example.py" \
    "fail"

# Test 8: File scope only - single file (pass)
run_test \
    "Single file scope" \
    "$PROJECT_DIR/src/app_routes.py" \
    "src/app_routes.py" \
    "pass"

# Summary
echo -e "\n========================================"
echo "Test Summary"
echo "========================================"
echo "Total tests run: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi
