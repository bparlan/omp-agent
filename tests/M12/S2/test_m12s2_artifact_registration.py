#!/usr/bin/env python3
# Verification IDs: VI-M12S2-3
# Requirement IDs: FR-M12S2-OPERATIONS_CONSOLIDATION_REGISTRATION
# Test Type: SPECIFICATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "AGENTS.md").exists() or (p / ".git").exists()
    ),
    Path(__file__).resolve().parents[4],
)
ARTIFACT_TYPES_PATH = REPO_ROOT / "core" / "artifacts" / "artifact_types.py"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def main():
    if not ARTIFACT_TYPES_PATH.exists():
        fail(f"{ARTIFACT_TYPES_PATH}: artifact types module does not exist")

    content = ARTIFACT_TYPES_PATH.read_text()
    if "operations-consolidation" not in content:
        fail("operations-consolidation artifact type not registered")

    pass_("Operations-consolidation registration validation passed")


if __name__ == "__main__":
    main()
