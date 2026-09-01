#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-2}
# {Requirement IDs: FR-OPS_HANDOFF_POINTS_IN_MANAGE_DEVELOPMENT}
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


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def pass_(msg):
    print(f"PASS: {msg}")


def main():
    if not DEV_SKILL.exists():
        fail(f"{DEV_SKILL}: file does not exist")

    content = DEV_SKILL.read_text()

    # Check for explicit ops handoff points section markers
    ops_handoff_indicators = [
        "ops handoff points",
        "trigger conditions",
        "manage-docs",
        "sync-documentation",
        "artifact format references",
        "handoff boundary",
        "trigger condition",
    ]

    found = False
    for indicator in ops_handoff_indicators:
        if indicator.lower() in content.lower():
            found = True
            break

    if not found:
        fail(f"{DEV_SKILL}: no ops handoff points found")

    pass_("Ops handoff points documented in manage-development skill")


if __name__ == "__main__":
    main()
