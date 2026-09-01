#!/usr/bin/env bash
# {Verification IDs: VER-M9S3-FR-ARTIFACT_CREATION-1}
# {Requirement IDs: FR-HEALTHCENTER-ARTIFACT_CREATION}
# Test Type: SCRIPT_EXECUTION

import sys
from pathlib import Path
import subprocess
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


def main():
    ARTIFACT_DIR = REPO_ROOT / "milestones" / "M9"

    # Clean up any previous artifacts for deterministic test execution
    import shutil

    for existing_artifact in ARTIFACT_DIR.glob("M9-health-check-*.md"):
        existing_artifact.unlink(missing_ok=True)

    # Create test skill
    example_skill_path = REPO_ROOT / "skills" / "example_skill"
    example_skill_path.mkdir(exist_ok=True)

    # Write example skill SKILL.md
    example_skill_path.joinpath("SKILL.md").write_text("""---
id: SKILL-example_skill
type: skill
milestone_id: M9
template_version: 1.3.0
---
# Example Skill

An example skill for artifact creation testing.
""")

    # Run healthcenter to create health-check artifact
    healthcenter_path = REPO_ROOT / "skills" / "healthcenter" / "healthcenter.py"
    if not healthcenter_path.exists():
        print("ERROR: healthcenter.py not found at ", healthcenter_path)
        sys.exit(1)

    # Run the healthcenter command
    result = subprocess.run(
        [str(healthcenter_path), "--skill", "example_skill"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 127:
        print("VALID_INITIAL_FAILURE: healthcenter skill not available yet")
        sys.exit(127)

    if result.returncode != 0:
        print(
            f"INFO: healthcenter --skill example_skill exited with {result.returncode}"
        )
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        # Continue to check if artifact was created anyway

    # Verify artifact was created
    artifact_path = ARTIFACT_DIR / "M9-health-check-example_skill.md"
    if not artifact_path.exists():
        print(f"FAIL: Missing health-check artifact at {artifact_path}")
        sys.exit(1)

    # Verify artifact contains required YAML frontmatter
    artifact_content = artifact_path.read_text()
    if "^---$" not in artifact_content:
        print("FAIL: Artifact missing YAML frontmatter delimiter")
        sys.exit(1)

    # Extract and validate frontmatter
    lines = artifact_content.split("\n")
    frontmatter_lines = []
    in_frontmatter = False

    for line in lines:
        if line.strip() == "---" and not in_frontmatter:
            in_frontmatter = True
            continue
        elif line.strip() == "---" and in_frontmatter:
            in_frontmatter = False
            break
        if in_frontmatter:
            frontmatter_lines.append(line)

    if not frontmatter_lines:
        print("FAIL: No YAML frontmatter found")
        sys.exit(1)

    frontmatter_text = "\n".join(frontmatter_lines)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except Exception as e:
        print(f"FAIL: Invalid YAML frontmatter: {e}")
        sys.exit(1)

    # Check required fields
    required_fields = [
        "id",
        "type",
        "milestone_id",
        "template_version",
        "derived_from",
        "metadata",
    ]
    missing = [field for field in required_fields if field not in frontmatter]
    if missing:
        print(f"FAIL: Missing required frontmatter fields: {missing}")
        sys.exit(1)

    # Check specific field values
    if frontmatter.get("type") != "health-check":
        print(f"FAIL: Artifact type is not 'health-check': {frontmatter.get('type')}")
        sys.exit(1)

    if frontmatter.get("milestone_id") != "M9":
        print(f"FAIL: Milestone ID is not 'M9': {frontmatter.get('milestone_id')}")
        sys.exit(1)

    # Clean up
    shutil.rmtree(example_skill_path, ignore_errors=True)

    print("PASS: Artifact creation test completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
