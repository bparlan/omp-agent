#!/bin/bash
# {Verification IDs: V-VI-7}
# {Requirement IDs: FR-LEGACY_COMPAT}
# Test Type: IMPLEMENTATION_CHECK

# VI-7: Legacy Compatibility with Strict Flag
# Verification ID: VI-7
# Source Requirement ID: FR-LEGACY_COMPAT
# Verification Method: SCRIPT_EXECUTION
# Target: Legacy artifact resolution with strict flag

echo "Testing legacy compatibility with strict flag..."

# Check if resolution module exists
if [ ! -f "core/artifacts/resolution.py" ]; then
    echo "ERROR: Resolution module not found at core/artifacts/resolution.py"
    exit 127
fi

# Check if resolution module is importable
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.resolution import resolve_artifact, LEGACY_ARTIFACT_MAPPINGS
print('Resolution module importable')
" 2>/dev/null; then
    echo "ERROR: Resolution module import failed"
    exit 127
fi

echo "Test requires implementation of legacy compatibility with strict flag."
exit 127
