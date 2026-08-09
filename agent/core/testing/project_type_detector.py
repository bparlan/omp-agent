#!/usr/bin/env python3

import sys
from pathlib import Path

# --- Configuration ---
# Define indicators for different project types.
# These are basic heuristics and can be expanded.
PROJECT_INDICATORS = {
    "markdown": [".md"],  # Look for .md files, potentially in docs/ or similar.
    "htmlcss": ["index.html", "style.css", "*.html", "*.css"], # Look for core web files.
    "python": ["requirements.txt", "setup.py", "*.py"], # Look for Python project markers.
    "aef_task": ["SKILL.md", "templates/"], # Look for OMP-specific agent structure.
}

def detect_project_type(project_path: Path) -> str | None:
    """Detects the project type based on file presence and heuristics."""
    
    # Check for specific files first (e.g., setup.py, SKILL.md)
    for project_type, indicators in PROJECT_INDICATORS.items():
        for indicator in indicators:
            if indicator.endswith("/") and (project_path / indicator).is_dir():
                return project_type
            if (project_path / indicator).is_file():
                return project_type
            if "*" in indicator:
                # Basic glob check for files
                if any((project_path / indicator).glob(indicator)):
                    return project_type
    
    # Fallback or more complex checks can be added here
    # For example, checking for specific directory structures or file contents.
    
    # If no clear indicators are found, return None
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_project_type.py <project_path>", file=sys.stderr)
        sys.exit(1)
    
    project_path_str = sys.argv[1]
    project_path = Path(project_path_str)
    
    if not project_path.is_dir():
        print(f"Error: Project path '{project_path_str}' is not a directory.", file=sys.stderr)
        sys.exit(1)
        
    project_type = detect_project_type(project_path)
    
    if project_type:
        print(project_type)
    else:
        # If no specific type is detected, we could default or indicate unknown.
        # For now, let's exit with an error if unknown.
        print("Error: Unknown project type.", file=sys.stderr)
        sys.exit(1)
