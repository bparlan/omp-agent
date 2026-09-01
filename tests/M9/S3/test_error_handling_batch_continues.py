#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-NFR-ERROR_HANDLING-1}
# {Requirement IDs: NFR-HEALTHCENTER-ERROR_HANDLING}
# Test Type: IMPLEMENTATION_CHECK

import sys
from pathlib import Path
import subprocess
import shutil

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

def main():
    ARTIFACT_DIR = REPO_ROOT / "milestones" / "M9"
    
    # Clean up any previous artifacts for deterministic test execution
    for existing_artifact in ARTIFACT_DIR.glob("M9-health-check-*.md"):
        existing_artifact.unlink(missing_ok=True)
    
    # Run healthcenter to create health-check artifact
    healthcenter_path = REPO_ROOT / "skills" / "healthcenter" / "healthcenter.py"
    if not healthcenter_path.exists():
        print("ERROR: healthcenter.py not found at ", healthcenter_path)
        sys.exit(1)
    
    # Run the healthcenter command
    result = subprocess.run([str(healthcenter_path), "--all"], 
                           capture_output=True, text=True)
    
    if result.returncode == 127:
        print("VALID_INITIAL_FAILURE: healthcenter skill not available yet")
        sys.exit(127)
    
    if result.returncode != 0:
        print(f"INFO: healthcenter --all exited with {result.returncode}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        # Continue to check if artifact was created anyway
    
    # Verify artifact was created
    artifact_path = ARTIFACT_DIR / "M9-health-check-health_badges.md"
    if not artifact_path.exists():
        print(f"FAIL: Missing expected artifact for health_badges at {artifact_path}")
        sys.exit(1)
    
    # Verify artifact contains YAML frontmatter
    artifact_content = artifact_path.read_text()
    if "^---$" not in artifact_content:
        print("FAIL: Artifact missing YAML frontmatter delimiter")
        sys.exit(1)
    
    print("PASS: Batch processing continued and created artifact despite errors")
    sys.exit(0)

if __name__ == "__main__":
    main()
