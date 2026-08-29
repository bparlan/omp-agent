#!/bin/bash
# {Verification IDs: VER-M9S1V-FR-LEGACY_COMPAT-001}
# {Requirement IDs: FR-LEGACY_COMPAT}
# Test Type: IMPLEMENTATION_CHECK

# Test legacy compatibility
# Target: core/artifacts/resolution.py

# Test 1: Check if resolution module exists
if [ ! -f "core/artifacts/resolution.py" ]; then
    echo "ERROR: Resolution module not found at core/artifacts/resolution.py"
    exit 127
fi

# Test 2: Check if LEGACY_ARTIFACT_MAPPINGS exists
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.resolution import LEGACY_ARTIFACT_MAPPINGS
print('LEGACY_ARTIFACT_MAPPINGS found')
print('MAPPINGS:', LEGACY_ARTIFACT_MAPPINGS)
" 2>/dev/null; then
    echo "ERROR: LEGACY_ARTIFACT_MAPPINGS not found"
    exit 127
fi

# Test 3: Check if _is_canonical_artifact function exists
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.resolution import _is_canonical_artifact
print('_is_canonical_artifact function found')
" 2>/dev/null; then
    echo "ERROR: _is_canonical_artifact function not found"
    exit 127
fi

echo "Legacy compatibility test passed"
exit 0
