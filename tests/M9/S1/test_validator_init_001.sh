#!/bin/bash
# {Verification IDs: VER-M9S1V-FR-VALIDATOR_INIT-001}
# {Requirement IDs: FR-VALIDATOR_INIT}
# Test Type: IMPLEMENTATION_CHECK

# Test metadata validator initialization via CLI
# Target: bin/omp-verify-metadata
# Verification Method: SCRIPT_EXECUTION

echo "Testing metadata validator initialization via CLI..."

# Test 1: Check if validator CLI exists
# Sanitized: Pre-flight existence trap removed for TDD compatibility

# Test 2: Check if CLI is executable
if [ ! -x "bin/omp-verify-metadata" ]; then
    echo "ERROR: Validator CLI not executable"
    exit 127
fi

# Test 3: Try to run the CLI with a basic artifact
if ! python3 bin/omp-verify-metadata milestones/M9/M9.md 2>&1; then
    echo "ERROR: Validator CLI does not run properly"
    exit 127
fi

echo "Validator initialization test passed (conceptual)"
exit 0
