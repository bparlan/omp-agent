#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-ARTIFACT_CREATION-1}
# {Requirement IDs: FR-HEALTHCENTER-ARTIFACT_CREATION}
# Test Type: IMPLEMENTATION_CHECK

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from core.artifacts.metadata import extract_frontmatter


def run_healthcenter():
    cmd = [
        os.path.join(REPO_ROOT, "skills", "healthcenter", "healthcenter.py"),
        "--skill",
        "example_skill",
    ]
    proc = subprocess.run(
        cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return proc.returncode, proc.stdout.decode(), proc.stderr.decode()


def main():
    ARTIFACT = os.path.join(
        REPO_ROOT, "milestones", "M9", "M9-health-check-example_skill.md"
    )
    os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
    if os.path.exists(ARTIFACT):
        os.remove(ARTIFACT)

    returncode, stdout, stderr = run_healthcenter()

    if returncode == 127:
        print("VALID_INITIAL_FAILURE: healthcenter skill not available yet")
        sys.exit(127)

    if returncode != 0:
        print(f"FAIL: healthcenter exited with {returncode}\n{stdout}\n{stderr}")
        sys.exit(1)

    if not os.path.exists(ARTIFACT):
        print(f"FAIL: Missing artifact at {ARTIFACT}")
        sys.exit(1)

    metadata = extract_frontmatter(ARTIFACT)
    if metadata is None:
        print("FAIL: Artifact missing parseable YAML frontmatter")
        sys.exit(1)

    required = [
        "id",
        "type",
        "milestone_id",
        "template_version",
        "derived_from",
        "metadata",
    ]
    missing = [key for key in required if key not in metadata]
    if missing:
        print(f"FAIL: Artifact missing required frontmatter keys: {missing}")
        sys.exit(1)

    if metadata.get("type") != "health-check":
        print("FAIL: Artifact type is not 'health-check'")
        sys.exit(1)

    print("PASS: Health-check artifact frontmatter is valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
