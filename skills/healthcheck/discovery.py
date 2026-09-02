#!/usr/bin/env python3
"""
Skill discovery module for AEF-OMP HealthCheck Skill.

Provides project-agnostic skill directory discovery functionality.
This module is separated from I/O operations for better testability and maintainability.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional


def discover_skills() -> List[Path]:
    """
    Discovers skills in the AEF-OMP project structure.
    
    Returns:
        List of Paths to skill directories containing SKILL.md files.
        The function uses project-agnostic discovery to locate skills.
    """
    skills_dir = Path("skills")
    if not skills_dir.exists():
        return []
    
    discovered_skills = []
    
    # Recursively find all directories containing SKILL.md
    for skill_path in skills_dir.rglob("SKILL.md"):
        skill_dir = skill_path.parent
        discovered_skills.append(skill_dir)
    
    return discovered_skills


def get_skills_directory() -> Path:
    """
    Gets the skills directory path.
    
    Returns:
        Path to the skills directory.
    """
    return Path("skills")


def discover_skill_by_name(skill_name: str) -> Optional[Path]:
    """
    Discovers a specific skill by name.
    
    Args:
        skill_name: Name of skill to find
        
    Returns:
        Path to skill directory if found, None otherwise.
    """
    skills = discover_skills()
    
    for skill_path in skills:
        if skill_path.name == skill_name:
            return skill_path
    
    return None


def get_skills_summary() -> Dict[str, Any]:
    """
    Gets a summary of all discovered skills.
    
    Returns:
        Dictionary containing summary information about skills.
    """
    skills = discover_skills()
    
    summary = {
        "total_skills": len(skills),
        "skill_names": [skill.name for skill in skills],
        "skill_paths": [str(skill) for skill in skills],
    }
    
    return summary


def get_skills_summary_dict() -> Dict[str, Any]:
    """
    Gets skills summary as a dictionary (alternative implementation).
    
    Returns:
        Dictionary containing skills summary.
    """
    return get_skills_summary()


def is_milestone_agnostic(skill_path: Path) -> bool:
    """
    Checks if a skill is milestone agnostic.
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        True if skill is milestone agnostic, False otherwise.
    """
    skill_md_path = skill_path / "SKILL.md"
    if not skill_md_path.exists():
        return False
    
    content = skill_md_path.read_text()
    
    # Check for hardcoded milestone IDs
    milestone_patterns = [
        r'\bM\d+',           # M1, M2, M3, etc.
        r'milestone_id:\s*["\']?M\d+',  # milestone_id: M1
        r'M\d+\.',          # M1. or M1.S1
        r'milestones/M\d+/',  # directories with milestone numbers
    ]
    
    for pattern in milestone_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False
    
    return True


def is_spec_agnostic(skill_path: Path) -> bool:
    """
    Checks if a skill is specification agnostic.
    
    Args:
        skill_path: Path to skill directory
        
    Returns:
        True if skill is specification agnostic, False otherwise.
    """
    skill_md_path = skill_path / "SKILL.md"
    if not skill_md_path.exists():
        return False
    
    content = skill_md_path.read_text()
    
    # Check for hardcoded specification IDs
    spec_patterns = [
        r'SPEC-M\d+[A-Z]\d',  # SPEC-M1S1, SPEC-M1S2
        r'SPEC-\d+[A-Z]\d',   # SPEC-1S1, SPEC-1S2
        r'spec_id:\s*["\']?SPEC-[A-Z]\d*\d',  # spec_id: SPEC-M1S1
    ]
    
    for pattern in spec_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False
    
    return True