#!/usr/bin/env python3
# {Verification IDs: V-FR-1.5, V-FR-3.3}
# {Requirement IDs: FR-2, FR-3.1, FR-3.2, FR-3.3, FR-3.4, FR-5}

import sys
import re
import os
from pathlib import Path
from _frontmatter import extract_frontmatter

# Default legacy milestone boundaries (pre-canonical milestones without frontmatter)
LEGACY_BOUNDARIES_DEFAULTS = ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9"]


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


def is_legacy_milestone(normalized_path: str) -> bool:
    """Check if a milestone path falls under default legacy boundaries."""
    m = re.search(r"/milestones/(m\d+)/", normalized_path)
    if not m:
        return False
    milestone_dir = m.group(1)
    return milestone_dir in LEGACY_BOUNDARIES_DEFAULTS


def check_template_version_compatibility(data: dict, filepath: str) -> list:
    """Check template_version compatibility for milestone lifecycle artifacts.

    Returns list of warning messages.
    Compatible versions: same major.minor, patch may differ.
    """
    warnings = []
    artifact_type = data.get('type', '')
    artifact_ver = str(data.get('template_version', ''))

    if not artifact_ver:
        return warnings

    if artifact_type == 'milestone':
        try:
            major = int(artifact_ver.split('.')[0])
            if major < 2:
                warnings.append(f"COMPATIBILITY: {filepath} uses template_version {artifact_ver} (pre-contract, consider upgrading to 2.0.0)")
        except (ValueError, IndexError):
            pass

    elif artifact_type == 'specification':
        try:
            parts = artifact_ver.split('.')
            major, minor = int(parts[0]), int(parts[1])
            if major != 1 or minor != 2:
                warnings.append(f"COMPATIBILITY: {filepath} template_version {artifact_ver} differs from specification_template.md (1.2.x)")
        except (ValueError, IndexError):
            pass

    elif artifact_type == 'verification':
        try:
            parts = artifact_ver.split('.')
            major, minor = int(parts[0]), int(parts[1])
            if major != 1 or minor != 1:
                warnings.append(f"COMPATIBILITY: {filepath} template_version {artifact_ver} differs from verification_template.md (1.1.x)")
        except (ValueError, IndexError):
            pass

    return warnings


def validate_file(filepath: str) -> bool:
    try:
        normalized_path = filepath.replace("\\", "/").lower()

        # Detect and gracefully skip Skill files and general non-lifecycle docs
        if "skills/" in normalized_path or normalized_path.endswith("skill.md") or "agent/skills/" in normalized_path:
            print(f"Metadata SKIP: {filepath} is a Skill definition (validated by skills-auditor).")
            return True

        if not os.path.exists(filepath):
            print(f"Error: File not found at '{filepath}'.")
            return False

        data = extract_frontmatter(filepath)

        if data is None:
            # No valid frontmatter found — check legacy vs active milestone
            if "milestones/" in normalized_path:
                if is_legacy_milestone(normalized_path):
                    print(f"Metadata SKIP (Legacy compatibility): {filepath} is a legacy milestone document.")
                    return True
                active_ms = get_active_milestone_id().lower()
                if f"milestones/{active_ms}/" not in normalized_path:
                    print(f"Metadata SKIP (Legacy compatibility): {filepath} is a legacy milestone document.")
                    return True
                else:
                    print(f"Error: No valid YAML frontmatter found in active milestone file {filepath}. Must be enclosed in '---'.")
                    return False
            else:
                print(f"Metadata SKIP: {filepath} is a general document.")
                return True

        # Gracefully skip Skill configurations or custom templates that aren't lifecycle artifacts
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

        # Reject semantic qualifiers in IDs
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

        # Check template version compatibility
        compat_warnings = check_template_version_compatibility(data, filepath)
        for w in compat_warnings:
            print(w)

        print(f"Metadata OK: {filepath} ({data['id']} - {data['type']})")
        return True

    except Exception as e:
        print(f"Exception validating {filepath}: {e}")
        return False


def main():
    import os
    print(f"Current working directory for validate_metadata.py: {os.getcwd()}")
    print(f"Absolute path of validate_metadata.py: {os.path.abspath(__file__)}")

    raw_args = sys.argv[1:]

    # Filter out common CLI flags starting with '--'
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