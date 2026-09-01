#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-BATCH_PROCESSING-1}
# {Requirement IDs: FR-HEALTHCENTER-BATCH_PROCESSING}
# Test Type: SCRIPT_EXECUTION

import sys
from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


def main():
    ARTIFACT_DIR = REPO_ROOT / "milestones" / "M9"

    # Clean up any previous artifacts for deterministic test execution
    for existing_artifact in ARTIFACT_DIR.glob("M9-health-check-*.md"):
        existing_artifact.unlink(missing_ok=True)

    # Run healthcenter to create health-check artifacts
    healthcenter_path = REPO_ROOT / "skills" / "healthcenter" / "healthcenter.py"
    if not healthcenter_path.exists():
        print("ERROR: healthcenter.py not found at ", healthcenter_path)
        sys.exit(1)

    # Run the healthcenter batch processing
    result = subprocess.run(
        [str(healthcenter_path), "--all"], capture_output=True, text=True
    )

    if result.returncode == 127:
        print("VALID_INITIAL_FAILURE: healthcenter skill not available yet")
        sys.exit(127)

    if result.returncode != 0:
        print(f"INFO: healthcenter --all exited with {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        # Continue to check if artifacts were created anyway

    # Verify artifacts were created for all skills
    expected_skills = [
        "health_badges",
        "health_check_report",
        "processed_skills",
        "skills-ledger",
    ]
    for skill in expected_skills:
        artifact_path = ARTIFACT_DIR / f"M9-health-check-{skill}.md"
        if not artifact_path.exists():
            print(f"FAIL: Missing batch artifact for {skill} at {artifact_path}")
            sys.exit(1)

    print("PASS: Batch processing created health-check artifacts for all skills")
    sys.exit(0)


if __name__ == "__main__":
    main()
