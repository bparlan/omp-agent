#!/usr/bin/env python3
# {Verification IDs: VER-M9S3V1-FR1}
# {Requirement IDs: FR-HEALTHCENTER-ARTIFACT_CREATION}
# Test Type: DOCUMENT_CHECK

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

def test_specification_documentation():
    """Test specification documentation exists and is valid"""
    
    # Read the verification protocol from correct path
    spec_path = REPO_ROOT / "milestones" / "M9" / "M9S3V1.md"
    
    # Check if specification file exists
    if not spec_path.exists():
        print("ERROR: Verification protocol file not found at", spec_path)
        sys.exit(1)
    
    # Read and validate YAML frontmatter
    content = spec_path.read_text()
    
    # Check for required frontmatter fields
    required_frontmatter = [
        "id:", "type:", "title:", "milestone_id:", 
        "derived_from:", "template_version:", "project_language:"
    ]
    
    for field in required_frontmatter:
        if field not in content:
            print(f"ERROR: Required frontmatter field '{field}' missing")
            sys.exit(1)
    
    # Check for functional validation section
    if "## Functional Validation" not in content:
        print("ERROR: Functional Validation section missing")
        sys.exit(1)
    
    # Check for functional requirement sections
    if "### FR-HEALTHCENTER-ARTIFACT_CREATION" not in content:
        print("ERROR: FR-HEALTHCENTER-ARTIFACT_CREATION requirement missing")
        sys.exit(1)
    
    # Verify project language is python
    if "project_language: python" not in content:
        print("ERROR: Project language should be python")
        sys.exit(1)
    
    print("✓ Specification documentation is valid and complete")
    sys.exit(0)

if __name__ == "__main__":
    test_specification_documentation()
