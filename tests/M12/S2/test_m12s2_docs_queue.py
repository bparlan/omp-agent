#!/usr/bin/env python3
# Verification IDs: VI-M12S2-2
# Requirement IDs: FR-M12S2-DOCS_QUEUE_CREATION
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
DOCS_DIR = REPO_ROOT / "docs"
QUEUE_DIR = DOCS_DIR / "queue"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def main():
    if not DOCS_DIR.exists() or not DOCS_DIR.is_dir():
        fail(f"{DOCS_DIR}: docs directory does not exist")

    if not QUEUE_DIR.exists() or not QUEUE_DIR.is_dir():
        fail(f"{QUEUE_DIR}: intake buffer directory does not exist")

    pass_("Docs queue directory structure validation passed")


if __name__ == "__main__":
    main()
