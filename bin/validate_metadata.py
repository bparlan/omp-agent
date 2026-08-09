#!/usr/bin/env python3
# {Verification IDs: V-FR-1.5, V-FR-3.3}
# {Requirement IDs: FR-2, FR-3.1, FR-3.2, FR-3.3, FR-3.4, FR-5}

import sys
import yaml
import re
import os
from pathlib import Path

def get_active_milestone_id() -> str:
    """Dynamically determine the active milestone ID by scanning milestones/ directory."""
    active_id = "M10"  # Default fallback
    try:
        milestones_dir = Path("milestones")
        if milestones_dir.exists() and milestones_dir.is_dir():
            milestone_nums = []
            for path in milestones_dir.iterdir():
                if path.is_dir() and re.match(r"^M\d+$", path.name):
                    milestone_nums.append(int(path.name[1:]))
            if milestone_nums:
                active_id = f"M{max(milestone_nums)}"
    except Exception:
        pass
    return active_id

def validate_file(filepath: str) -> bool:
    try:
        normalized_path = filepath.replace("\\", "/").lower()
        
        # Step 1: Detect and gracefully skip Skill files and general non-lifecycle docs
        if "skills/" in normalized_path or normalized_path.endswith("skill.md") or "agent/skills/" in normalized_path:
            print(f"Metadata SKIP: {filepath} is a Skill definition (validated by skills-auditor).")
            return True

        if not os.path.exists(filepath):
            print(f"Error: File not found at '{filepath}'.")
            return False

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Strip UTF-8 BOM if present (BOM handling from EXPERIENCES.md)
        if content.startswith('\ufeff'):
            content = content.lstrip('\ufeff')
            
        # Normalize line endings to Unix style (\n) to prevent carriage return issues
        content = content.replace('\r\n', '\n')
        
        # Strip leading whitespace/newlines to ensure we start directly at the frontmatter block
        content = content.lstrip()
        
        # Manual Line-Splitting Frontmatter Extractor (100% regex-free & double-escaping immune)
        lines = content.split('\n')
        if not lines or lines[0].strip() != '---':
            # Option 2 Boundary Check: Differentiate legacy milestones from canonical active ones
            if "milestones/" in normalized_path:
                active_ms = get_active_milestone_id().lower()
                # If the file resides in an older, legacy milestone directory (M1-M9), skip it gracefully
                if f"milestones/{active_ms}/" not in normalized_path:
                    print(f"Metadata SKIP (Legacy compatibility): {filepath} is a legacy milestone document.")
                    return True
                else:
                    # Newly generated canonical artifacts under active development MUST have valid frontmatter
                    print(f"Error: No valid YAML frontmatter found in active milestone file {filepath}. Must be enclosed in '---'.")
                    return False
            else:
                # Non-milestone general documentation files are skipped gracefully
                print(f"Metadata SKIP: {filepath} is a general document.")
                return True
                
        # Find closing '---' delimiter
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break
                
        if end_idx == -1:
            print(f"Error: No valid YAML frontmatter found in active milestone file {filepath}. Must be enclosed in '---'.")
            return False
            
        frontmatter_text = '\n'.join(lines[1:end_idx])
        
        try:
            # Parse YAML frontmatter safely
            data = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as ye:
            print(f"Error parsing YAML in {filepath}: {ye}")
            return False
            
        if not data:
            print(f"Error: Frontmatter in {filepath} is empty.")
            return False
            
        # Step 2: Gracefully skip Skill configurations or custom templates that aren't lifecycle artifacts
        if 'name' in data and 'id' not in data:
            print(f"Metadata SKIP: {filepath} contains a Skill signature (name: '{data.get('name')}').")
            return True
        if data.get('type') == 'skill':
            print(f"Metadata SKIP: {filepath} is classified as type: skill.")
            return True
            
        # Required Canonical Fields validation for standard lifecycle artifacts
        required_fields = ['id', 'type', 'milestone_id']
        for field in required_fields:
            if field not in data:
                print(f"Error: Missing required field '{field}' in {filepath} frontmatter.")
                return False
                
        # Validate Identity Structure
        id_val = data['id']
        if not isinstance(id_val, str) or not id_val.strip():
            print(f"Error: 'id' must be a non-empty string in {filepath}.")
            return False
            
        # Validate ID Format: Supports legacy (SPEC-001) and canonical M10 alphanumeric (SPEC-M10S4)
        if not re.match(r'^[A-Z]+-[A-Z0-9]+$', id_val):
            print(f"Error: Invalid ID format '{id_val}' in {filepath}. Expected e.g. SPEC-001 or SPEC-M10S4.")
            return False
            
        # Reject semantic qualifiers in IDs (M10S2 and review rules)
        if any(qual in id_val.upper() for qual in ['-CORRECTED', '-FINAL', '-V2', '-V3', '-FIXED', '-REVISED']):
            print(f"Error: 'id' '{id_val}' contains prohibited semantic qualifiers or version tags.")
            return False
            
        # Validate Semantic Types
        valid_types = ['specification', 'verification', 'test_set', 'completion', 'evaluation', 'review', 'milestone']
        if data['type'] not in valid_types:
            print(f"Error: 'type' '{data['type']}' is invalid in {filepath}. Must be one of {valid_types}.")
            return False
            
        if not isinstance(data['milestone_id'], str) or not data['milestone_id'].strip():
            print(f"Error: 'milestone_id' must be a non-empty string in {filepath}.")
            return False
            
        # derived_from is optional but must be a list if present
        if 'derived_from' in data:
            if not isinstance(data['derived_from'], list):
                print(f"Error: 'derived_from' must be a list in {filepath}.")
                return False
                
        print(f"Metadata OK: {filepath} ({data['id']} - {data['type']})")
        return True
        
    except Exception as e:
        print(f"Exception validating {{filepath}}: {{e}}")
        return False

def main():
    import os
    print(f"Current working directory for validate_metadata.py: {os.getcwd()}")
    print(f"Absolute path of validate_metadata.py: {os.path.abspath(__file__)}")

    raw_args = sys.argv[1:]
    
    # Filter out common CLI flags starting with '--' (e.g. --spec, --verification)
    # to support both positional arguments and flag-based validation sweeps.
    filepaths = [arg for arg in raw_args if not arg.startswith('--')]
    
    if not filepaths:
        print("Usage: python3 validate_metadata.py [--spec] <file1> [--verification] [file2 ...]")
        sys.exit(1)
        
    success = True
    for filepath in filepaths:
        if not validate_file(filepath):
            success = False
            
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()