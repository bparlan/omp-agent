#!/usr/bin/env python3
# Verification IDs: VI-M12S2-4
# Requirement IDs: FR-M12S2-FOLDER_GOVERNANCE_RULES
# Test Type: DOCUMENT_CHECK

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
SKILL_PATH = REPO_ROOT / "skills" / "manage-docs" / "SKILL.md"
EXPECTED_FOLDERS = ["docs/hotfixes/", "docs/diagrams/", "docs/solutions/", "docs/"]


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def main():
    if not SKILL_PATH.exists():
        fail(f"{SKILL_PATH}: skill file does not exist")

    text = SKILL_PATH.read_text().lower()
    found = [f for f in EXPECTED_FOLDERS if f.lower() in text]
    if len(found) != len(EXPECTED_FOLDERS):
        missing = sorted(set(EXPECTED_FOLDERS) - set(found))
        fail(f"Missing governance rules for: {missing}")

    pass_("Folder governance rules validation passed")


if __name__ == "__main__":
    main()
