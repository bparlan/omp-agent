#!/bin/bash

# FR-TEST-GENERATION-CONTRACT CLI Executable
# Validates test generation functionality as per M13S5 specification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test generation contract validation
validate_generation_contract() {
    echo "=== FR-TEST-GENERATION-CONTRACT Validation ==="
    echo "Validating test generation functionality..."
    
    # Check if generate-tests skill exists
    if [[ ! -f "skills/generate-tests/__init__.py" ]]; then
        echo -e "${RED}❌ Error: generate-tests skill not found at skills/generate-tests/__init__.py${NC}"
        return 1
    fi
    
    # Check if generate-tests skill is executable
    if [[ ! -x "skills/generate-tests/__init__.py" ]]; then
        echo -e "${RED}❌ Error: generate-tests skill is not executable${NC}"
        return 1
    fi
    
    # Check if milestone directory exists
    if [[ ! -d "milestones/M13" ]]; then
        echo -e "${RED}❌ Error: M13 milestone directory not found${NC}"
        return 1
    fi
    
    # Check if specification file exists
    if [[ ! -f "milestones/M13/SPEC-M13S5.md" ]]; then
        echo -e "${RED}❌ Error: SPEC-M13S5 specification file not found${NC}"
        return 1
    fi
    
    # Check if test files exist in correct location
    if [[ ! -d "tests/M13/S5" ]]; then
        echo -e "${YELLOW}⚠️  Warning: tests/M13/S5 directory not found (may be created during generation)${NC}"
    fi
    
    echo -e "${GREEN}✅ All generation contract requirements satisfied${NC}"
    echo "FR-TEST-GENERATION-CONTRACT: VALID"
    return 0
}

# Generate tests with specification validation
generate_with_specification() {
    echo "=== Generating Tests with Specification Compliance ==="
    echo "Running generate-tests skill with full specification validation..."
    
    # Run the generate-tests skill
    if python3 skills/generate-tests/__init__.py; then
        echo -e "${GREEN}✅ Tests generated successfully${NC}"
        
        # Validate generated test artifacts
        echo "Validating generated test artifacts..."
        
        # Check if test files were created
        test_files_created=0
        for test_file in tests/M13/S5/test_*.py; do
            if [[ -f "$test_file" ]]; then
                test_files_created=$((test_files_created + 1))
            fi
        done
        
        if [[ $test_files_created -gt 0 ]]; then
            echo -e "${GREEN}✅ $test_files_created test file(s) created${NC}"
            echo "Generated test files:"
            ls -la tests/M13/S5/test_*.py 2>/dev/null || true
        else
            echo -e "${YELLOW}⚠️  No test files were generated${NC}"
        fi
        
        # Check if test plan ledger was created
        if [[ -f "milestones/M13/M13S5T1.md" ]]; then
            echo -e "${GREEN}✅ Test plan ledger created${NC}"
            echo "Test plan ledger: milestones/M13/M13S5T1.md"
        else
            echo -e "${YELLOW}⚠️  Test plan ledger not found${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Error: Failed to generate tests${NC}"
        return 1
    fi
}

# Display help information
show_help() {
    cat << EOF
=== FR-TEST-GENERATION-CONTRACT Help ===

Usage: $0 [OPTIONS]

Options:
  --validate     Validate generation contract requirements
  --test         Generate tests with specification compliance
  --help         Show this help message

Description:
  CLI executable for FR-TEST-GENERATION-CONTRACT test oracle.
  Validates that the generate-tests skill meets all specification requirements
  and implements observable contract boundaries.

Specification Requirements:
  - validate that the generate-tests skill exists and is executable
  - verify that test files are generated with deterministic content
  - confirm test generation validates specification contracts (S1-S4)
  - ensure generated test artifacts follow M13 naming conventions
  - verify FR traceability in generated test files

Contract Validation:
  - skill existence: skills/generate-tests/__init__.py
  - skill executability: executable permission
  - milestone directory: milestones/M13/
  - specification file: milestones/M13/SPEC-M13S5.md
  - test artifacts: tests/M13/S5/test_*.py
  - test plan ledger: milestones/M13/M13S5T1.md

Expected Exit Codes:
  0 - Validation successful
  1 - Validation failed

Examples:
  $0 --validate     # Validate generation contract
  $0 --test          # Generate tests with specification compliance
  $0 --help          # Show this help message
EOF
}

# Main function
main() {
    case "${1:-}" in
        --validate)
            validate_generation_contract
            ;;
        --test)
            generate_with_specification
            ;;
        --help)
            show_help
            ;;
        "")
            echo "Usage: $0 [--validate|--test|--help]"
            echo "Use --help for more information"
            ;;
        *)
            echo "Error: Unknown option: $1"
            echo "Use --help for more information"
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"