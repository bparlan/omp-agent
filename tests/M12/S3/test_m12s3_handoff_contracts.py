#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-1}
# {Requirement IDs: FR-HANDOFF_ROADMAP_TO_DEVELOPMENT, FR-HANDOFF_DEVELOPMENT_TO_DOCS}
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
DEV_SKILL = REPO_ROOT / "skills" / "manage-development" / "SKILL.md"
DOCS_SKILL = REPO_ROOT / "skills" / "manage-docs" / "SKILL.md"


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def main():
    # Check dev skill contains handoff contracts
    if not DEV_SKILL.exists():
        fail(f"{DEV_SKILL}: file does not exist")
    dev_text = DEV_SKILL.read_text()

    # Check for required section markers or recipient skill names
    handoff_indicators = [
        "handoff",
        "manage-docs",
        "sync-documentation",
        "trigger condition",
        "recipient skill",
        "artifact format",
    ]

    found = False
    for indicator in handoff_indicators:
        if indicator.lower() in dev_text.lower():
            found = True
            break

    if not found:
        fail(f"{DEV_SKILL}: no handoff contract indicators found")

    # Check docs skill contains handoff contracts
    if not DOCS_SKILL.exists():
        fail(f"{DOCS_SKILL}: file does not exist")
    docs_text = DOCS_SKILL.read_text()

    docs_indicators = ["handoff", "cross-skill", "circulation", "trigger"]

    docs_found = False
    for indicator in docs_indicators:
        if indicator.lower() in docs_text.lower():
            docs_found = True
            break

    if not docs_found:
        fail(f"{DOCS_SKILL}: no handoff contract indicators found")

    pass_("Handoff contracts documented in both skill files")


if __name__ == "__main__":
    main()
