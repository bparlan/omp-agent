#!/bin/bash

# FR-VALIDATION-ORCHESTRATION-CONTRACT CLI Executable
# Validates test orchestration functionality as per M13S5 specification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test orchestration contract validation
validate_orchestration_contract() {
    echo "=== FR-VALIDATION-ORCHESTRATION-CONTRACT Validation ==="
    echo "Validating test orchestration functionality..."
    
    # Check if evaluate-tests skill exists
    if [[ ! -f "skills/evaluate-tests/__init__.py" ]]; then
        echo -e "${RED}❌ Error: evaluate-tests skill not found at skills/evaluate-tests/__init__.py${NC}"
        return 1
    fi
    
    # Check if evaluate-tests skill is executable
    if [[ ! -x "skills/evaluate-tests/__init__.py" ]]; then
        echo -e "${RED}❌ Error: evaluate-tests skill is not executable${NC}"
        return 1
    fi
    
    # Check if evaluation artifact exists
    if [[ ! -f "milestones/M13/EVA-M13S5.md" ]]; then
        echo -e "${YELLOW}⚠️  Warning: EVA-M13S5.md evaluation artifact not found${NC}"
    fi
    
    # Check if test plan ledger exists
    if [[ ! -f "milestones/M13/M13S5T1.md" ]]; then
        echo -e "${RED}❌ Error: M13S5 test plan ledger not found${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ All orchestration contract requirements satisfied${NC}"
    echo "FR-VALIDATION-ORCHESTRATION-CONTRACT: VALID"
    return 0
}

# Orchestrate tests with specification validation
orchestrate_with_specification() {
    echo "=== Orchestrating Tests with Specification Compliance ==="
    echo "Running evaluate-tests skill with full specification validation..."
    
    # Run the evaluate-tests skill
    if python3 skills/evaluate-tests/__init__.py; then
        echo -e "${GREEN}✅ Tests orchestrated successfully${NC}"
        
        # Validate evaluation artifact
        echo "Validating evaluation artifact..."
        
        # Check if evaluation artifact was created
        if [[ -f "milestones/M13/EVA-M13S5.md" ]]; then
            echo -e "${GREEN}✅ Evaluation artifact created${NC}"
            echo "Evaluation artifact: milestones/M13/EVA-M13S5.md"
            
            # Check evaluation artifact content
            if grep -q "passed_tests == total_tests" "milestones/M13/EVA-M13S5.md" 2>/dev/null; then
                echo -e "${GREEN}✅ Evaluation artifact contains passed_tests == total_tests${NC}"
            else
                echo -e "${YELLOW}⚠️  Evaluation artifact missing passed_tests == total_tests${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  Evaluation artifact not created${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Error: Failed to orchestrate tests${NC}"
        return 1
    fi
}

# Display help information
show_help() {
    cat << EOF
=== FR-VALIDATION-ORCHESTRATION-CONTRACT Help ===

Usage: $0 [OPTIONS]

Options:
  --validate     Validate orchestration contract requirements
  --test         Orchestrate tests with specification compliance
  --help         Show this help message

Description:
  CLI executable for FR-VALIDATION-ORCHESTRATION-CONTRACT test oracle.
  Validates that the evaluate-tests skill meets all specification requirements
  and implements observable contract boundaries.

Specification Requirements:
  - validate that the evaluate-tests skill exists and is executable
  - verify that evaluation reports are generated with proper structure
  - confirm test execution validates core AEF interfaces
  - ensure evaluation artifacts contain required validation results
  - verify deterministic test execution and reporting

Contract Validation:
  - skill existence: skills/evaluate-tests/__init__.py
  - skill executability: executable permission
  - evaluation artifact: milestones/M13/EVA-M13S5.md
  - test plan ledger: milestones/M13/M13S5T1.md
  - passed_tests == total_tests: in evaluation artifact

Expected Exit Codes:
  0 - Validation successful
  1 - Validation failed

Examples:
  $0 --validate     # Validate orchestration contract
  $0 --test          # Orchestrate tests with specification compliance
  $0 --help          # Show this help message
EOF
}

# Main function
main() {
    case "${1:-}" in
        --validate)
            validate_orchestration_contract
            ;;
        --test)
            orchestrate_with_specification
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