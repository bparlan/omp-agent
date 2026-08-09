\
import argparse
import sys
import os
import yaml
import re
from pathlib import Path

def get_active_milestone_id() -> str:
    """Dynamically determine the active milestone ID by scanning milestones/ directory."""
    active_id = "M10"  # Default fallback
    try:
        milestones_dir = Path("milestones")
        if milestones_dir.is_dir():
            milestone_dirs = sorted([d for d in milestones_dir.iterdir() if d.is_dir() and d.name.startswith('M')],
                                     key=lambda x: int(x.name[1:]))
            if milestone_dirs:
                active_id = milestone_dirs[-1].name
        print(f"FAIL: Could not determine active milestone ID: {e}")
        pass # Ignore errors and use default
    return active_id

def validate_file(filepath: str) -> bool:
    """Validates a single file's metadata structure."""
    try:
        # Check for NUL bytes early in the path itself, if path is malformed.
        # The content check is inside the 'with open' block.
        if b'\\x00' in filepath.encode('utf-8', errors='ignore'):
             print(f"FAIL: File path contains NUL byte: {filepath}")
             return False

        if not os.path.exists(filepath):
            print(f"FAIL: File not found: {filepath}")
            return False

        with open(filepath, 'rb') as f: # Read as binary to check for NUL bytes in content
            if b'\\x00' in f.read():
                print(f"FAIL: File content contains NUL byte: {filepath}")
                return False

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match content between first `---` and second `---`
        match = re.match(r'^---\\s*\\n(.*?)\\n---', content, re.DOTALL)
        if not match:
            print(f"FAIL: No valid YAML frontmatter found in {filepath} (must be delimited by `---`)")
            return False

        frontmatter_text = match.group(1)
        data = yaml.safe_load(frontmatter_text)

        if not isinstance(data, dict):
            print(f"FAIL: Frontmatter is not a valid YAML dictionary in {filepath}")
            return False

        # Validate required keys
        required_keys = ('id', 'type', 'milestone_id')
        for key in required_keys:
            if key not in data:
                print(f"FAIL: Frontmatter in {filepath} missing required key: '{key}'")
                return False
        
        # Specific checks based on type (example)
        if data.get('type') == 'specification':
            if 'requirements' not in data and 'Functional Requirements' not in data: # Check for common keys
                 print(f"WARNING: Specification type file {filepath} might be missing 'requirements' or 'Functional Requirements' section.")
        elif data.get('type') == 'verification':
            if 'verification_items' not in data and 'Verification Items' not in data: # Check for common keys
                print(f"WARNING: Verification type file {filepath} might be missing 'verification_items' or 'Verification Items' section.")
        
        # Ensure milestone_id is present and not empty
        if not data.get('milestone_id'):
             print(f"FAIL: Milestone ID is missing or empty in {filepath}")
             return False

        return True

    except FileNotFoundError:
        print(f"FAIL: File not found: {filepath}")
        return False
    except yaml.YAMLError as e:
        print(f"FAIL: Error parsing YAML frontmatter in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"FAIL: An unexpected error occurred validating {filepath}: {e}")
        return False

def validate_metadata_files(*filepaths: str) -> bool:
    """Validates a list of files, returning True if all are valid."""
    if not filepaths:
        print("No file paths provided for validation.")
        return False
    
    all_valid = True
    for fp in filepaths:
        if not validate_file(fp):
            all_valid = False
    return all_valid

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Validates metadata in files, checking for YAML frontmatter, required keys, and basic integrity."
    )
    parser.add_argument(
        '--spec', 
        action='append', 
        help="Path to a specification file to validate. Can be specified multiple times."
    )
    parser.add_argument(
        '--verification', 
        action='append', 
        help="Path to a verification file to validate. Can be specified multiple times."
    )
    
    args = parser.parse_args()
    
    files_to_validate = []
    if args.spec:
        files_to_validate.extend(args.spec)
    if args.verification:
        files_to_validate.extend(args.verification)
        
    if not files_to_validate:
        print("No files specified for validation. Use --spec or --verification.")
        sys.exit(1)
        
    if validate_metadata_files(*files_to_validate):
        sys.exit(0)
    else:
        sys.exit(1)
