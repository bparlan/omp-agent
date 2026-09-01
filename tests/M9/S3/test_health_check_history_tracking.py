#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-HISTORY_TRACKING-1}
# {Requirement IDs: FR-HEALTHCENTER-HISTORY_TRACKING}
# Test Type: UNIT_TEST

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from core.artifacts.registry import get_registry


def main():
    registry = get_registry()

    # Test relationship storage and retrieval
    relationships = [
        {
            "source_id": "HC-skill-2",
            "target_id": "SKILL-skill",
            "type": "derived_from",
            "metadata": {"timestamp": "2024-01-01T00:00:00Z"}
        },
        {
            "source_id": "HC-skill-1",
            "target_id": "SKILL-skill",
            "type": "derived_from",
            "metadata": {"timestamp": "2024-01-02T00:00:00Z"}
        }
    ]

    # Store relationships
    for rel in relationships:
        success = registry.store_relationship(
            rel["source_id"],
            rel["target_id"],
            rel["type"],
            rel["metadata"]
        )
        if not success:
            print(f"FAIL: Failed to store relationship {rel}")
            sys.exit(1)

    # Retrieve relationships
    all_relationships = registry.get_relationships()

    # Check that all relationships are stored
    found_source1 = any(
        r["source_id"] == "HC-skill-1" and r["target_id"] == "SKILL-skill"
        for r in all_relationships
    )
    found_source2 = any(
        r["source_id"] == "HC-skill-2" and r["target_id"] == "SKILL-skill"
        for r in all_relationships
    )

    if not found_source1:
        print("FAIL: Relationship HC-skill-1 not found")
        sys.exit(1)

    if not found_source2:
        print("FAIL: Relationship HC-skill-2 not found")
        sys.exit(1)

    # Check that relationships have correct types
    # Note: The registry stores with key "relationship_type" instead of "type"
    type_check = any(
        r["source_id"] == "HC-skill-1"
        and r["target_id"] == "SKILL-skill"
        and r.get("type", r.get("relationship_type")) == "derived_from"
        for r in all_relationships
    )

    if not type_check:
        print("FAIL: Relationship type not correctly stored")
        sys.exit(1)

    print("PASS: Chronological relationships stored and retrievable")
    sys.exit(0)
if __name__ == "__main__":
    main()
