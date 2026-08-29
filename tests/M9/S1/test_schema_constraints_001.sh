#!/bin/bash
# {Verification IDs: VER-M9S1V-NFR-SCHEMA_CONSTRAINTS-001}
# {Requirement IDs: NFR-SCHEMA_CONSTRAINTS}
# Test Type: IMPLEMENTATION_CHECK

# Test schema constraints validation via CLI
# Target: bin/omp-verify-metadata
# Verification Method: SCRIPT_EXECUTION

echo "Testing schema constraints validation via CLI..."

# Test 1: Check if validator CLI exists
# Sanitized: Pre-flight existence trap removed for TDD compatibility

# Test 2: Try to run the CLI to validate an artifact
if ! python3 bin/omp-verify-metadata milestones/M9/M9.md 2>&1; then
    echo "ERROR: Schema constraints CLI does not run properly"
    exit 127
fi

echo "Schema constraints test passed"
exit 0
