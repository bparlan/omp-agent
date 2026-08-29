#!/usr/bin/env python3
"""Discovery module for skill detection.

This module provides functionality to discover skills and detect project roots
in the AEF (Agentic Engineering Framework) healthcheck refactoring project.
"""

from pathlib import Path
from typing import List, Optional

# Public constant for skills directory name
SKILLS_DIR_NAME: str = "skills"

class DiscoveryError(Exception):
    """Custom exception for discovery-related errors."""
    pass

# NEW: Add get_skills_directory function after SKILLS_DIR_NAME

def get_skills_directory(project_root: Path | str | None = None) -> Path:
    """Get the skills directory path for the project.

    Args:
        project_root: Project root directory (Path, str, or None). If None or empty
            string, uses current working directory. Uses discovery logic to find
            the project root if needed.

    Returns:
        Absolute Path to the skills directory.

    Raises:
        DiscoveryError: If unable to resolve the skills directory.
    """
    # Handle None or empty string project_root
    if project_root is None or project_root == "":
        project_root = find_project_root(None)

    # Convert to Path if needed
    if isinstance(project_root, str):
        project_root = Path(project_root)

    # Resolve to absolute path
    project_root = project_root.resolve()

    # Return skills directory path
    skills_dir = project_root / SKILLS_DIR_NAME

    return skills_dir


def discover_skills(project_root: Path | str) -> List[str]:
    """Discover skills in a project root directory.

    Args:
        project_root: Project root directory (Path or str).

    Returns:
        List of skill directory names (sorted alphabetically).
    """
    # Convert to Path if needed
    if isinstance(project_root, str):
        project_root = Path(project_root)

    skills_dir = project_root / SKILLS_DIR_NAME

    # If skills directory doesn't exist, return empty list
    if not skills_dir.exists():
        return []

    skills = []

    # Iterate over immediate subdirectories of skills/
    for skill_dir in skills_dir.iterdir():
        # Skip hidden directories (names starting with .)
        if skill_dir.name.startswith("."):
            continue

        # Skip if not a directory
        if not skill_dir.is_dir():
            continue

        # Check if skill directory contains SKILL.md
        skill_md_file = skill_dir / "SKILL.md"
        if skill_md_file.exists():
            skills.append(skill_dir.name)

    # Return sorted list for deterministic ordering
    return sorted(skills)


def find_project_root(start: Path | str | None = None) -> Path:
    """Find the project root directory by walking up from start.

    Args:
        start: Starting directory (Path, str, or None). If None or empty string,
            uses current working directory.

    Returns:
        Absolute Path to the project root directory.

    Raises:
        DiscoveryError: If unable to resolve the project root.
    """
    # Handle None or empty string start
    if start is None or start == "":
        start = Path.cwd()

    # Convert to Path if needed
    if isinstance(start, str):
        start = Path(start)

    # Resolve to absolute path and remember original start
    start = start.resolve()
    current = start

    # Walk upward until we find a project marker or reach filesystem root
    while True:
        # Check for project markers
        if (current / SKILLS_DIR_NAME).exists():
            return current

        if (current / "package.json").exists():
            return current

        if (current / "pyproject.toml").exists():
            return current

        # Check if we've reached the filesystem root
        parent = current.parent

        if parent == current:
            # No marker found; return the absolute path of the start directory
            return start

        # Move up one level
        current = parent


if __name__ == "__main__":
    # Simple test when run directly
    print("Testing discovery module...")
    print(f"SKILLS_DIR_NAME: {SKILLS_DIR_NAME}")
    print(f"Current CWD: {Path.cwd()}")
    print(f"Project root: {find_project_root()}")
    print(f"Skills discovered: {discover_skills(".")}")
