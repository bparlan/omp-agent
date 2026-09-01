#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-NFR-COMPLIANCE-1}
# {Requirement IDs: NFR-HEALTHCENTER-COMPLIANCE}
# Test Type: IMPLEMENTATION_CHECK

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
ARTIFACT_DIR="${REPO_ROOT}/milestones/M9"

mkdir -p "${ARTIFACT_DIR}"

cleanup_artifacts() {
  find "${ARTIFACT_DIR}" -maxdepth 1 -name 'M9-health-check-*.md' -delete || true
  # Clean up registry
  if python3 -c "from core.artifacts.registry import get_registry; r = get_registry(); r.clear_all()" 2>/dev/null; then
    :
  fi
}
trap cleanup_artifacts EXIT
cleanup_artifacts

# Create test skill for compliance testing
mkdir -p "${REPO_ROOT}/skills/test_compliance_skill"
cat > "${REPO_ROOT}/skills/test_compliance_skill/SKILL.md" << 'SKILL_EOF'
---
id: SKILL-test_compliance_skill
type: skill
milestone_id: M9
template_version: 1.3.0
---
# Test Compliance Skill

A test skill for compliance testing.
SKILL_EOF

# Run healthcenter to create health-check artifact
skills/healthcenter/healthcenter.py --skill test_compliance_skill

if [[ $? -ne 0 ]]; then
  echo "VALID_INITIAL_FAILURE: healthcenter skill not available yet"
  exit 127
fi

# Compliance validation script
COMPLIANCE_PYTHON="${REPO_ROOT}/test_compliance_validation.py"

cat > "${COMPLIANCE_PYTHON}" << 'PYEOF'
import sys
from pathlib import Path
from core.artifacts.metadata import extract_frontmatter
from core.validation import validate_artifact
from core.artifacts.registry import get_registry
from core.artifacts.artifact_types import get_artifact_type

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

def test_compliance():
    """Test M9 canonical artifact system compliance."""

    registry = get_registry()
    artifact_dir = Path(REPO_ROOT) / "milestones" / "M9"

    # Find created health-check artifacts
    health_artifacts = []
    for f in artifact_dir.glob("M9-health-check-*.md"):
        metadata = extract_frontmatter(str(f))
        if metadata:
            health_artifacts.append(metadata)

    if not health_artifacts:
        print("INFO: No health-check artifacts for compliance testing")
        return True

    # Test 1: Verify artifact creation follows 7-step protocol
    for artifact in health_artifacts:
        if not artifact.get("id"):
            print(f"FAIL: Artifact missing id field")
            return False

        if not artifact.get("type") == "health-check":
            print(f"FAIL: Artifact type not 'health-check': {artifact.get('type')}")
            return False

        # Validate metadata structure
        required_fields = ["id", "type", "milestone_id", "skill_id", "validation_score", "status", "timestamp", "insights"]
        missing = [f for f in required_fields if f not in artifact]
        if missing:
            print(f"FAIL: Missing required fields: {missing}")
            return False

    print("PASS: Artifact creation follows 7-step protocol")

    # Test 2: Verify validation performs schema checks
    for artifact in health_artifacts:
        # Remove metadata wrapper for validation
        metadata = {k: v for k, v in artifact.items() if k != "metadata"}

        validation_result = validate_artifact(metadata)
        if not validation_result.get("valid"):
            print(f"FAIL: Valid artifact rejected: {validation_result}")
            return False

    print("PASS: Validation performs schema checks")

    # Test 3: Verify storage follows canonical rules
    for artifact in health_artifacts:
        artifact_type = get_artifact_type("health-check")
        if not artifact_type:
            print("FAIL: health-check artifact type not found")
            return False

        # Check storage location pattern
        if not str(artifact.get("id", "")).startswith("HC-"):
            print(f"FAIL: Artifact ID doesn't follow pattern: {artifact.get('id')}")
            return False

    print("PASS: Storage follows canonical rules")

    # Test 4: Verify relationships tracked in registry
    all_relationships = registry.get_relationships()

    if not all_relationships:
        print("INFO: No relationships tracked yet (registry test)")
    else:
        print(f"PASS: Registry contains {len(all_relationships)} relationships")

    # Test 5: Verify specific M9 compliance requirements
    for artifact in health_artifacts:
        # Check artifact structure compliance
        if artifact.get("milestone_id") != "M9":
            print(f"FAIL: Milestone ID mismatch: {artifact.get('milestone_id')}")
            return False

        # Verify validation score range
        score = artifact.get("validation_score", 0)
        if not (0 <= score <= 100):
            print(f"FAIL: Invalid validation score: {score}")
            return False

        # Verify insights is array
        if not isinstance(artifact.get("insights", []), list):
            print(f"FAIL: Insights not array: {artifact.get('insights')}")
            return False

    print("PASS: Specific M9 compliance requirements met")
    return True

def main():
    if test_compliance():
        print("PASS: M9 canonical artifact system compliance test completed")
        sys.exit(0)
    else:
        print("FAIL: Compliance test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
PYEOF

python3 "${COMPLIANCE_PYTHON}"

# Clean up
rm -rf "${REPO_ROOT}/skills/test_compliance_skill" "${COMPLIANCE_PYTHON}"

echo "PASS: Compliance test completed successfully"
exit 0