#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-REGISTRY_INIT-001}
# {Requirement IDs: FR-REGISTRY_INIT}
# Test Type: IMPLEMENTATION_CHECK

import sys
import os

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.registry import get_registry

def test_registry_initialization():
    registry = get_registry()

    expected_methods = [
        'register_type',
        'get_type',
        'get_schema',
        'get_storage_rule',
        'list_types',
    ]
    for method in expected_methods:
        if not hasattr(registry, method):
            print(f"FAIL: ArtifactRegistry missing method: {method}")
            return 1

    types = registry.list_types()
    if not types:
        print("FAIL: Registry returned no types")
        return 1

    for expected_type in types:
        if registry.get_type(expected_type) is None:
            print(f"FAIL: Registry missing type: {expected_type}")
            return 1

        schema = registry.get_schema(expected_type)
        if not isinstance(schema, dict) or not schema:
            print(f"FAIL: get_schema('{expected_type}') returned invalid schema")
            return 1

        storage_rule = registry.get_storage_rule(expected_type)
        if not isinstance(storage_rule, dict) or not storage_rule:
            print(f"FAIL: get_storage_rule('{expected_type}') returned invalid storage rule")
            return 1

    print("PASS: Registry initialized with types, schemas, and storage rules")
    return 0

if __name__ == '__main__':
    sys.exit(test_registry_initialization())
