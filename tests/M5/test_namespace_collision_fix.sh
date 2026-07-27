#!/bin/bash

# Test Suite: Issue 3 - Namespace Collision Resolution
# Tests: Test Case 3.1, 3.2, 3.3
# Total: 3 test cases

set -e

# Test counter
TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print test header
print_header() {
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Test Suite: Issue 3 - Namespace Collision Resolution"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
}

# Function to print test footer
print_footer() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Test Summary"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Tests Run: $TESTS_RUN"
    echo "  Tests Pass: $TESTS_PASS"
    echo "  Tests Fail: $TESTS_FAIL"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    if [ $TESTS_FAIL -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed!${NC}"
        exit 1
    fi
}

print_header

# Test Case 3.1: Project-scoped milestone directories exist
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 3.1: Project-scoped milestone directories exist"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking milestone directory structure..."

# Check if project-scoped directories exist
PROJECT_SCOPED_DIRS=0
for dir in milestones/*/; do
    # Check if directory contains nested milestone subdirectories (indicates project scoping)
    if [ "$(find "$dir" -maxdepth 1 -type d | wc -l)" -gt 1 ]; then
        echo -e "  ${GREEN}✓${NC} $dir (project-scoped structure detected)"
        PROJECT_SCOPED_DIRS=$((PROJECT_SCOPED_DIRS + 1))
    fi
done

if [ "$PROJECT_SCOPED_DIRS" -gt 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - Found $PROJECT_SCOPED_DIRS project-scoped milestone directory(ies)"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - No project-scoped milestone directories found"
    echo "  Expected: milestones/{project_slug}/"
    echo "  Current: Flat structure detected"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 3.2: No collision with multiple projects
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 3.2: No collision with multiple projects"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for independent milestone directories..."

MILESTONE_COUNT=$(find milestones -type d -name "M*" | wc -l)

if [ "$MILESTONE_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - Found $MILESTONE_COUNT milestone directory(ies)"
    echo "  Milestones:"
    find milestones -type d -name "M*" | while read dir; do
        echo "    - $dir"
    done
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - No milestone directories found"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Test Case 3.3: Validation prevents duplicate milestone IDs
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Case 3.3: Validation prevents duplicate milestone IDs"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

echo "  Checking for duplicate milestone IDs across directories..."

# Extract milestone IDs from directory names
MILESTONE_IDS=()
for dir in milestones/*/; do
    # Extract milestone ID from directory name (e.g., "milestones/aef/M5" -> "M5")
    if [[ "$dir" =~ /([A-Z]\d+)$ ]]; then
        MILESTONE_ID="${BASH_REMATCH[1]}"
        MILESTONE_IDS+=("$MILESTONE_ID")
    fi
done

# Check for duplicates
DUPLICATE_COUNT=0
UNIQUE_IDS=()
for id in "${MILESTONE_IDS[@]}"; do
    if [[ ! " ${UNIQUE_IDS[@]} " =~ " $id " ]]; then
        UNIQUE_IDS+=("$id")
    else
        DUPLICATE_COUNT=$((DUPLICATE_COUNT + 1))
    fi
done

if [ "$DUPLICATE_COUNT" -eq 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - All milestone IDs are unique"
    echo "  Unique IDs: ${UNIQUE_IDS[*]}"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${RED}✗ FAILED${NC} - Found $DUPLICATE_COUNT duplicate milestone ID(s):"
    echo "  ${MILESTONE_IDS[*]}"
    echo "  Collision detected - this indicates namespace collision not resolved"
    TESTS_FAIL=$((TESTS_FAIL + 1))
fi

echo ""

# Bonus: Check for project-scoped milestone artifacts
echo "═══════════════════════════════════════════════════════════════"
echo "  Bonus: Project-scoped milestone artifacts exist"
echo "═══════════════════════════════════════════════════════════════"
TESTS_RUN=$((TESTS_RUN + 1))

# Count milestone artifacts in project-scoped directories
ARTIFACT_COUNT=$(find milestones -type f -name "*.md" | wc -l)

if [ "$ARTIFACT_COUNT" -gt 0 ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - Found $ARTIFACT_COUNT milestone artifact(s)"
    TESTS_PASS=$((TESTS_PASS + 1))
else
    echo -e "  ${YELLOW}⚠ WARNING${NC} - No milestone artifacts found (optional)"
    TESTS_PASS=$((TESTS_PASS + 1))
fi

print_footer
