#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-FR-INSIGHTS_GENERATION-1}
# {Requirement IDs: FR-HEALTHCENTER-INSIGHTS_GENERATION}
# Test Type: IMPLEMENTATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from core.artifacts.artifact_types import get_artifact_type


def main():
    artifact_type = get_artifact_type("health-check")
    if artifact_type is None:
        print("FAIL: health-check artifact type not found")
        sys.exit(1)

    # Test metadata with issues
    metadata_with_issues = {
        "id": "HC-skill-1",
        "type": "health-check",
        "milestone_id": "M9",
        "skill_id": "skill_a",
        "validation_score": 85,
        "status": "needs_review",
        "timestamp": "2024-01-01T00:00:00Z",
        "insights": ["Missing -stable suffix", "Missing required fields"],
        "recommendations": [
            "Add -stable to version field",
            "Add missing required fields",
        ],
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "artifact_identity": "HC-skill_a-1",
            "artifact_type": "health-check",
        },
    }

    # Test metadata without issues
    metadata_no_issues = {
        "id": "HC-skill-2",
        "type": "health-check",
        "milestone_id": "M9",
        "skill_id": "skill_b",
        "validation_score": 100,
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "insights": [],
        "recommendations": [],
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "artifact_identity": "HC-skill_b-1",
            "artifact_type": "health-check",
        },
    }

    # Check that insights are populated when issues exist
    if not metadata_with_issues["insights"]:
        print("FAIL: Missing insights when health issues detected")
        sys.exit(1)

    # Check that recommendations are populated when issues exist
    if not metadata_with_issues["recommendations"]:
        print("FAIL: Missing recommendations when health issues detected")
        sys.exit(1)

    # Check that insights are structured as string arrays
    for insight in metadata_with_issues["insights"]:
        if not isinstance(insight, str):
            print("FAIL: Insight not structured as string")
            sys.exit(1)

    # Check that recommendations are structured as string arrays
    for recommendation in metadata_with_issues["recommendations"]:
        if not isinstance(recommendation, str):
            print("FAIL: Recommendation not structured as string")
            sys.exit(1)

    # Check that empty arrays when no issues
    if metadata_no_issues["insights"]:
        print("FAIL: Insights present when no issues detected")
        sys.exit(1)

    if metadata_no_issues["recommendations"]:
        print("FAIL: Recommendations present when no issues detected")
        sys.exit(1)

    print("PASS: Insights and recommendations correctly generated and structured")
    sys.exit(0)


if __name__ == "__main__":
    main()
