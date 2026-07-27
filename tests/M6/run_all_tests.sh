#!/bin/bash
# M6S1T1: Test Runner for Canonical Artifact Model
# This script runs all M6 tests with color-coded output and coverage reporting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   M6S1T1: Test Suite for Canonical Artifact Model       ║${NC}"
echo -e "${BLUE}║   Running All Test Files                                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Count test files
TEST_FILES=$(find "$SCRIPT_DIR" -name "test_*.py" -type f | wc -l)
echo -e "${YELLOW}Found $TEST_FILES test files${NC}"
echo ""

# Run all tests
echo -e "${BLUE}Running all tests...${NC}"
echo ""

# Run pytest with color output
python -m pytest "$SCRIPT_DIR" -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ALL TESTS PASSED                                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
else
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   TESTS FAILED                                          ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
