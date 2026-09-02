"""
Skill discovery mechanisms for healthcheck.
Handles project-agnostic skill directory detection and skill discovery.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

# Global skills directory discovery
skills_dir: Optional[Path] = None
def discover_skills_directory() -> Path:
    """Find skills directory using multiple strategies"""
    script_dir = Path(__file__).parent.absolute()

    # Strategy 1: Look for skills directory in parent of script
    possible_paths = [
        script_dir.parent,  # /Users/bparlan/devcode/aef/agent/skills
    ]

    # Strategy 2: Check environment variable
    omp_project_root = os.environ.get("OMP_PROJECT_ROOT")
    if omp_project_root:
        possible_paths.append(Path(omp_project_root))

    # Strategy 3: Look for skills-ledger.json upward
    for parent in script_dir.parents:
        ledger_path = parent / "skills-ledger.json"
        if ledger_path.exists():
            return parent

    # Fallback to current working directory
    cwd = Path.cwd()
    if (cwd / "skills-ledger.json").exists():
        return cwd

    # Absolute fallback - check if skills directory exists with skills-ledger.json
    for path in possible_paths:
        if (path / "skills-ledger.json").exists():
            return path

    # Default fallback
    return script_dir
def get_skills_directory() -> Path:
    """Get the global skills directory, discovering if not already set"""
    global skills_dir
    if skills_dir is None:
        skills_dir = discover_skills_directory()
        print(f"Skills directory: {skills_dir}", file=sys.stderr)
    return skills_dir
def discover_skills() -> List[Path]:
    """Discover all skill directories"""
    skills = []
    skills_dir = get_skills_directory()

    if not skills_dir.exists():
        print(f"Skills directory does not exist: {skills_dir}", file=sys.stderr)
        return skills

    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append(skill_file)
    return skills
def discover_skill_by_name(skill_name: str) -> Optional[Path]:
    """Discover a specific skill by name"""
    skills = discover_skills()
    for skill_file in skills:
        if skill_file.parent.name == skill_name:
            return skill_file
    return None
def get_skills_summary() -> dict:
    """Get summary information about discovered skills"""
    skills = discover_skills()
    return {
        "total_skills": len(skills),
        "skills_directory": str(get_skills_directory()),
        "skills_list": [s.parent.name for s in skills]
    }