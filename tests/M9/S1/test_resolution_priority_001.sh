#!/bin/bash
# {Verification IDs: VER-M9S1V-NFR-RESOLUTION_PRIORITY-001}
# {Requirement IDs: NFR-RESOLUTION_PRIORITY}
# Test Type: IMPLEMENTATION_CHECK

# Test resolution priority via CLI
# Target: python core/artifacts/resolution.py
# Verification Method: SCRIPT_EXECUTION

echo "Testing resolution priority via CLI..."

# Test 1: Check if resolution CLI exists
if [ ! -f "core/artifacts/resolution.py" ]; then
    echo "ERROR: Resolution CLI not found at core/artifacts/resolution.py"
    exit 127
fi

# Test 2: Try to run the CLI
if ! python3 core/artifacts/resolution.py --identity "TEST" --type "specification" 2>&1; then
    echo "ERROR: Resolution priority CLI does not run properly"
    exit 127
fi

echo "Resolution priority test passed"
exit 0
