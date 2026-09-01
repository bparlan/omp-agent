#!/usr/bin/env python3
"""
Manage Development Skill Implementation

This skill implements the SDD pipeline orchestration for milestone development.
It should orchestrate the 12-stage development lifecycle and manage spec processing.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Skill metadata
SKILL_NAME = "manage-development"
SKILL_VERSION = "2.2.0-stable"


def read_skill_info(skill_name: str) -> Dict[str, Any]:
    """Read skill information from SKILL.md file"""
    skill_dir = Path(f"skills/{skill_name}")
    skill_md_path = skill_dir / "SKILL.md"

    if not skill_md_path.exists():
        return {"error": f"SKILL.md not found for skill: {skill_name}"}

    try:
        with open(skill_md_path, "r") as f:
            content = f.read()

        # Extract frontmatter (YAML)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                # Parse basic frontmatter fields
                result = {
                    "name": skill_name,
                    "version": SKILL_VERSION,
                    "description": skill_name.replace("-", " ").title(),
                }
                return result

        return {"error": "Invalid SKILL.md format"}

    except Exception as e:
        return {"error": f"Failed to read SKILL.md: {str(e)}"}


def discover_milestones() -> list:
    """Discover available milestones"""
    milestones_dir = Path("milestones")
    milestones = []

    if not milestones_dir.exists():
        return milestones

    for item in milestones_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            milestone_file = item / "M*.md"
            if any(milestone_file.parent.glob("*.md")):
                milestones.append(item.name)

    return sorted(milestones)


def discover_specifications(milestone: str) -> list:
    """Discover specifications for a milestone"""
    milestone_dir = Path(f"milestones/{milestone}")
    specs = []

    if not milestone_dir.exists():
        return specs

    # Find files matching M{num}S{num}.md pattern
    for file_path in milestone_dir.glob("M*_S*.md"):
        # Extract spec ID
        match = file_path.name.replace(".md", "")
        if len(match) >= 4 and match[1] == "1" and match[3] == "S":
            specs.append(match)

    return sorted(specs)


def validate_spec_id(spec_id: str) -> bool:
    """Validate specification ID format (M{X}S{Y})"""
    if len(spec_id) < 4:
        return False
    return spec_id.startswith("M") and "S" in spec_id


def get_state_for_spec(spec_id: str, milestones_path: Path) -> Optional[str]:
    """Get current state for a specification artifact"""
    # Check for various artifact types in order of precedence
    artifact_patterns = [
        f"{spec_id}R.md",  # review artifact (final state)
        f"{spec_id}E.md",  # evaluation artifact
        f"{spec_id}C.md",  # implementation artifact
        f"{spec_id}TE.md",  # test evaluation artifact
        f"{spec_id}T*.md",  # test artifact
    ]

    milestone_dir = milestones_path / spec_id[:2]

    for pattern in artifact_patterns:
        if "*" in pattern:
            files = list(milestone_dir.glob(pattern))
            if files:
                return pattern.replace("*", files[0].stem[len(spec_id) : -1])
        else:
            artifact_file = milestone_dir / pattern
            if artifact_file.exists():
                return pattern

    return None


def validate_artifact_state(spec_id: str, milestones_path: Path, type: str) -> str:
    """Validate artifact state - from the skill documentation"""
    if type == "test_evaluation":
        path = milestones_path / spec_id[:2] / f"{spec_id}TE.md"
        if not path.exists():
            return "MISSING"
        content = path.read_text()
        if "EXIT_CODE=2" in content or "status: blocked" in content:
            return "STALE_OR_BLOCKED"
        if "EXIT_CODE=0" in content:
            return "APPROVED_AND_VERIFIED"
        return "PENDING"

    elif type == "evaluation":
        path = milestones_path / spec_id[:2] / f"{spec_id}E.md"
        if not path.exists():
            return "MISSING"
        content = path.read_text()
        if "EXIT_CODE=2" in content:
            return "INVALID_TEST_BLOCKED"
        if "EXIT_CODE=0" in content:
            return "PASSED"
        if "EXIT_CODE=1" in content:
            return "VALID_FAILURES_REMAIN"
        return "PENDING"

    elif type == "review":
        path = milestones_path / spec_id[:2] / f"{spec_id}R.md"
        if not path.exists():
            return "MISSING"
        content = path.read_text()
        if "EXIT_CODE=2" in content:
            return "INTEGRITY_FAILURE"
        if "EXIT_CODE=0" in content:
            return "PASSED"
        if "EXIT_CODE=1" in content:
            return "ISSUES_FOUND"
        return "PENDING"

    elif type == "closure":
        from glob import glob

        closure_files = sorted(glob(str(milestones_path / spec_id[:2] / "*CLOSE-*.md")))
        if not closure_files:
            return "MISSING"
        path = Path(closure_files[-1])
        content = path.read_text()
        if "status: REFUSED" in content:
            return "REFUSED"
        if "status: CLOSED_WITH_DEFECTS" in content:
            return "CLOSED_WITH_DEFECTS"
        if "status: CLOSED" in content:
            return "CLOSED"
        return "PENDING"

    return "UNKNOWN"


def main():
    """Main skill execution function"""
    print(f"=== {SKILL_NAME} Skill ===")
    print(f"Version: {SKILL_VERSION}")
    print()

    # Show skill info
    skill_info = read_skill_info(SKILL_NAME)
    print(f"Skill Info: {skill_info}")
    print()

    # Discover available milestones
    milestones = discover_milestones()
    print(f"Available Milestones: {milestones}")
    print()

    if not milestones:
        print("No milestones found. Please create a milestone first.")
        return

    # For demonstration, focus on M11
    milestone = "M11"
    if milestone in milestones:
        specs = discover_specifications(milestone)
        print(f"Specifications for {milestone}: {specs}")
        print()

        # Analyze each specification state
        milestones_path = Path("milestones")
        for spec_id in specs:
            print(f"--- Analysis for {spec_id} ---")

            # Check current state
            current_state = get_state_for_spec(spec_id, milestones_path)
            print(f"Current state artifact: {current_state}")

            # Validate different artifact states
            for state_type in ["test_evaluation", "evaluation", "review", "closure"]:
                validation = validate_artifact_state(
                    spec_id, milestones_path, state_type
                )
                print(f"{state_type}: {validation}")

            print()

    print("Skill execution completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
