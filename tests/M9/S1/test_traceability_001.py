#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-TRACEABILITY-001}
# {Requirement IDs: FR-TRACEABILITY}
# Test Type: IMPLEMENTATION_CHECK

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.registry import ArtifactRegistry, get_registry

def test_traceability():
    registry = get_registry()

    source_id = "ART-SRC-TRACE-001"
    target_id = "ART-TGT-TRACE-001"

    stored = registry.store_relationship(source_id, target_id, "derived_from", {"note": "traceability check"})
    assert stored is True, "store_relationship must return True on successful storage"

    relationships = registry.get_relationships(source_id)
    assert isinstance(relationships, list), "get_relationships must return a list"

    match = [r for r in relationships if r.get("target_id") == target_id and r.get("relationship_type") == "derived_from"]
    assert match, "get_relationships did not return stored relationship"

    print("PASS: Registry stores and retrieves relationship tracking data")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(test_traceability())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
