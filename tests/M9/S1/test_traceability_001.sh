#!/bin/bash
# {Verification IDs: VER-M9S1V-FR-TRACEABILITY-001}
# {Requirement IDs: FR-TRACEABILITY}
# Test Type: IMPLEMENTATION_CHECK

# Test registry relationship tracking
# Target: core/artifacts/registry.py

# Test 1: Check if registry module exists
if [ ! -f "core/artifacts/registry.py" ]; then
    echo "ERROR: Registry module not found at core/artifacts/registry.py"
    exit 127
fi

# Test 2: Check if ArtifactRegistry class exists
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.registry import ArtifactRegistry
print('ArtifactRegistry class found')
" 2>/dev/null; then
    echo "ERROR: ArtifactRegistry class not found"
    exit 127
fi

# Test 3: Check if registry has relationship tracking methods
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.registry import ArtifactRegistry
if hasattr(ArtifactRegistry, 'store_relationship'):
    print('store_relationship method found')
else:
    print('ERROR: store_relationship method not found')
    exit(127)
" 2>/dev/null; then
    echo "ERROR: store_relationship method check failed"
    exit 127
fi

# Test 4: Check if registry has relationship retrieval methods
if ! python3 -c "
import sys
sys.path.insert(0, '.')
from core.artifacts.registry import ArtifactRegistry
if hasattr(ArtifactRegistry, 'get_relationships'):
    print('get_relationships method found')
else:
    print('ERROR: get_relationships method not found')
    exit(127)
" 2>/dev/null; then
    echo "ERROR: get_relationships method check failed"
    exit 127
fi

echo "Traceability test passed"
exit 0
