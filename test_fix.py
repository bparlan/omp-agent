#!/usr/bin/env python3
import sys
import os

print("Python path:", sys.path)
print("Current directory:", os.getcwd())

# Test types import
try:
    from core.artifacts import types as t
    print("Types imported successfully:", hasattr(t, '_ARTIFACT_TYPE_DEFINITIONS'))
    print("Definitions count:", len(t._ARTIFACT_TYPE_DEFINITIONS))
    print("Expected definition 'specification':", 'specification' in t._ARTIFACT_TYPE_DEFINITIONS)
except Exception as e:
    print("Types import failed:", e)
    import traceback
    traceback.print_exc()

# Test registry import
try:
    from core.artifacts import registry as r
    print("Registry imported successfully:", hasattr(r, 'ArtifactRegistry'))
    print("get_registry function:", hasattr(r, 'get_registry'))

    # Test registry instantiation
    registry = r.get_registry()
    print("Registry instantiated:", registry is not None)

    # Test registry methods
    print("Has register_type:", hasattr(r.ArtifactRegistry, 'register_type'))
    print("Has get_type:", hasattr(r.ArtifactRegistry, 'get_type'))
    print("Has get_schema:", hasattr(r.ArtifactRegistry, 'get_schema'))
    print("Has get_storage_rule:", hasattr(r.ArtifactRegistry, 'get_storage_rule'))
    print("Has list_types:", hasattr(r.ArtifactRegistry, 'list_types'))

except Exception as e:
    print("Registry import failed:", e)
    import traceback
    traceback.print_exc()
