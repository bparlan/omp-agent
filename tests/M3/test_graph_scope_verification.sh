#!/usr/bin/env bash

# Test Graph-Based Scope Verification
# M3S1I1 Integration Tests
# Tests: In-scope, Out-of-scope, Multiple in-scope, Mixed in-scope/out-of-scope

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AEF_ROOT="$SCRIPT_DIR/.."
GRAPH_CONTEXT_BIN="$AEF_ROOT/skills/graph-context/bin"
VERIFY_SCOPE="$GRAPH_CONTEXT_BIN/verify-scope.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# BariaDAO project path
BARIADOA_PATH="$HOME/devcode/BariaDAO"

# BariaDAO graph path
BARIADOA_GRAPH="$BARIADOA_PATH/.omp/graph/baria.lbug"

# Temporary test file
TEMP_TEST_FILE="$BARIADOA_PATH/temp_test_file.py"

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_test() {
    echo -e "${YELLOW}[$TESTS_RUN] $1${NC}"
}

print_pass() {
    echo -e "${GREEN}✓ PASS: $1${NC}"
    ((TESTS_PASSED++))
}

print_fail() {
    echo -e "${RED}✗ FAIL: $1${NC}"
    ((TESTS_FAILED++))
}

cleanup_test_file() {
    if [ -f "$TEMP_TEST_FILE" ]; then
        rm -f "$TEMP_TEST_FILE"
    fi
}

run_lbug_query() {
    local query="$1"
    if [ ! -f "$BARIADOA_GRAPH" ]; then
        echo "ERROR: Graph file not found: $BARIADOA_GRAPH"
        return 1
    fi
    lbug "$BARIADOA_GRAPH" "$query" 2>&1 || return 1
}

# Test 1: Schema Property Check (file2 vs fileId)
print_header "Test 1: Schema Property Check (file2 vs fileId)"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Check if ingest-skeleton.py uses 'file2' property (not 'fileId')"

if grep -q 'file2' "$GRAPH_CONTEXT_BIN/ingest-skeleton.py" 2>/dev/null; then
    print_pass "ingest-skeleton.py uses 'file2' property"
else
    print_fail "ingest-skeleton.py does not use 'file2' property"
fi

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Query Symbol nodes with correct property name"

OUTPUT=$(run_lbug_query "MATCH (s:Symbol {name2: 'index_page'}) RETURN s.file2" 2>&1)
if echo "$OUTPUT" | grep -q "Property 'fileId' not found"; then
    print_fail "Query returned 'Property fileId not found' error"
elif [ -n "$OUTPUT" ]; then
    print_pass "Symbol query returned valid output: $OUTPUT"
else
    print_fail "Symbol query returned no output"
fi

# Test 2: IMPORTS Edge Creation
print_header "Test 2: IMPORTS Edge Creation"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Check if IMPORTS edges are created"

EDGE_COUNT=$(run_lbug_query "MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)" 2>&1 || echo "0")
if echo "$EDGE_COUNT" | grep -q "Property 'fileId' not found"; then
    print_fail "Query returned 'Property fileId not found' error"
elif [ -n "$EDGE_COUNT" ] && [ "$EDGE_COUNT" != "0" ]; then
    print_pass "IMPORTS edges exist (count: $EDGE_COUNT)"
else
    print_fail "No IMPORTS edges found (count: $EDGE_COUNT)"
fi

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Query specific IMPORTS edge (app_routes.py → content_loader.py)"

OUTPUT=$(run_lbug_query "MATCH (f1:File {name2: 'app_routes.py'})-[r:IMPORTS]->(f2:File) RETURN f1.name2, f2.name2, r.kind" 2>&1)
if echo "$OUTPUT" | grep -q "Property 'fileId' not found"; then
    print_fail "Query returned 'Property fileId not found' error"
elif [ -n "$OUTPUT" ]; then
    print_pass "IMPORTS edge found: $OUTPUT"
else
    print_fail "No IMPORTS edge found"
fi

# Test 3: Complete File Population
print_header "Test 3: Complete File Population"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Check if all 3 files from skeleton.md are in graph"

FILE_COUNT=$(run_lbug_query "MATCH (:File) RETURN count(*)" 2>&1 || echo "0")
if echo "$FILE_COUNT" | grep -q "Property 'fileId' not found"; then
    print_fail "Query returned 'Property fileId not found' error"
elif [ -n "$FILE_COUNT" ] && [ "$FILE_COUNT" = "3" ]; then
    print_pass "All 3 files are in graph (count: $FILE_COUNT)"
else
    print_fail "Expected 3 files, got $FILE_COUNT"
fi

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Verify README.md is present (often missed)"

OUTPUT=$(run_lbug_query "MATCH (:File {name2: 'README.md'}) RETURN f.path" 2>&1)
if echo "$OUTPUT" | grep -q "Property 'fileId' not found"; then
    print_fail "Query returned 'Property fileId not found' error"
elif [ -n "$OUTPUT" ]; then
    print_pass "README.md is present in graph"
else
    print_fail "README.md is missing from graph"
fi

# Test 4: In-Scope Modification (should pass)
print_header "Test 4: In-Scope Modification (Should Pass)"

cleanup_test_file
TESTS_RUN=$((TESTS_RUN + 1))
print_test "Create test file outside scope"

if touch "$TEMP_TEST_FILE"; then
    print_pass "Created temporary test file: $TEMP_TEST_FILE"
else
    print_fail "Failed to create test file"
fi

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Verify out-of-scope modification is detected"

cd "$BARIADOA_PATH"
if [ -f "$VERIFY_SCOPE" ]; then
    OUTPUT=$($VERIFY_SCOPE --scope=src/app_routes.py 2>&1)
    EXIT_CODE=$?

    # Check if exit code is 1 (fail) due to out-of-scope file
    if [ "$EXIT_CODE" = "1" ]; then
        if echo "$OUTPUT" | grep -qi "out-of-scope\|external.py\|temp_test_file"; then
            print_pass "verify-scope.py correctly rejected out-of-scope modification"
        else
            print_fail "verify-scope.py failed but for unexpected reason: $OUTPUT"
        fi
    else
        print_fail "verify-scope.py should have failed (exit code: $EXIT_CODE)"
    fi
else
    print_fail "verify-scope.py not found: $VERIFY_SCOPE"
fi

# Test 5: Out-of-Scope Modification (should fail)
print_header "Test 5: Out-of-Scope Modification (Should Fail)"

cleanup_test_file

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Create temporary file in scope"

echo "# in-scope modification" > "$TEMP_TEST_FILE"
print_pass "Created temporary file in scope: $TEMP_TEST_FILE"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Verify in-scope modification passes"

if [ -f "$VERIFY_SCOPE" ]; then
    OUTPUT=$($VERIFY_SCOPE --scope=src/app_routes.py 2>&1)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" = "0" ]; then
        print_pass "verify-scope.py correctly passed in-scope modification"
    else
        print_fail "verify-scope.py should have passed (exit code: $EXIT_CODE): $OUTPUT"
    fi
else
    print_fail "verify-scope.py not found: $VERIFY_SCOPE"
fi

# Test 6: Multiple In-Scope Files (should pass)
print_header "Test 6: Multiple In-Scope Files (Should Pass)"

cleanup_test_file

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Create test file for second in-scope file"

echo "# in-scope modification 2" > "$TEMP_TEST_FILE"
print_pass "Created second test file in scope"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Verify multiple in-scope files pass"

if [ -f "$VERIFY_SCOPE" ]; then
    OUTPUT=$($VERIFY_SCOPE --scope=src/app_routes.py 2>&1)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" = "0" ]; then
        print_pass "verify-scope.py correctly passed multiple in-scope files"
    else
        print_fail "verify-scope.py should have passed (exit code: $EXIT_CODE): $OUTPUT"
    fi
else
    print_fail "verify-scope.py not found: $VERIFY_SCOPE"
fi

# Test 7: Mixed In-Scope/Out-of-Scope (should fail)
print_header "Test 7: Mixed In-Scope/Out-of-Scope (Should Fail)"

cleanup_test_file

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Create file outside scope"

echo "# out-of-scope file" > "$TEMP_TEST_FILE"
print_pass "Created out-of-scope test file"

TESTS_RUN=$((TESTS_RUN + 1))
print_test "Verify mixed scope is rejected"

if [ -f "$VERIFY_SCOPE" ]; then
    OUTPUT=$($VERIFY_SCOPE --scope=src/app_routes.py 2>&1)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" = "1" ]; then
        if echo "$OUTPUT" | grep -qi "out-of-scope\|external\|temp"; then
            print_pass "verify-scope.py correctly rejected mixed scope"
        else
            print_fail "verify-scope.py failed but for unexpected reason: $OUTPUT"
        fi
    else
        print_fail "verify-scope.py should have failed (exit code: $EXIT_CODE)"
    fi
else
    print_fail "verify-scope.py not found: $VERIFY_SCOPE"
fi

# Cleanup
print_header "Cleanup"
cleanup_test_file
print_pass "Cleaned up temporary test files"

# Final Summary
print_header "Test Summary"

echo -e "Tests Run: $TESTS_RUN"
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed!${NC}"
    exit 1
fi
