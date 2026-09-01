#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-NFR-STORAGE_MODEL-001}
# {Requirement IDs: NFR-STORAGE_MODEL}
# Test Type: IMPLEMENTATION_CHECK

import os
import sys
import re

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.registry import get_registry


def test_storage_model():
    registry = get_registry()
    types = registry.list_types()
    pattern = re.compile(r"^<M_ID>/.+<.+>.md$")

    for artifact_type in types:
        storage_rule = registry.get_storage_rule(artifact_type)
        if not storage_rule or not isinstance(storage_rule, dict):
            continue
        canonical_location = storage_rule.get("canonical_storage_location")
        if not canonical_location:
            continue
        if not pattern.match(canonical_location):
            print(
                f"FAIL: Storage rule for '{artifact_type}' does not match canonical path pattern: {canonical_location}"
            )
            return 1

    print("PASS: Registry storage rules follow canonical path pattern")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(test_storage_model())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
