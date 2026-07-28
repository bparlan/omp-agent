#!/usr/bin/env python3
"""
validate_metadata.py — OMP AEF Artifact Metadata Validator (FR-5)

Parses YAML frontmatter from a file and validates:
  - FR-3: Required fields (id, type, title, milestone_id, status, derived_from)
  - FR-4: ID format (uppercase letters, hyphen, sequential digits; no semantic qualifiers)
"""

import sys
import os
import re
import yaml


REQUIRED_FIELDS = ["id", "type", "title", "milestone_id", "status", "derived_from"]
ALLOWED_TYPES = ["specification", "verification", "test_set", "investigation", "completion", "evaluation", "review", "hotfix"]
ALLOWED_STATUSES = ["draft", "active", "completed", "superseded"]
CANONICAL_ID_PATTERN = re.compile(r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|HOT)-\d+$")


def validate_file(filepath: str) -> bool:
    """Validate a single file. Returns True on success, False on failure."""
    if not os.path.isfile(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return False

    with open(filepath, "r") as fh:
        content = fh.read()

    # Extract YAML frontmatter delimited by --- ... ---
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print(f"Error: No YAML frontmatter found in {filepath}", file=sys.stderr)
        return False

    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        print(f"Error: Invalid YAML in {filepath}: {exc}", file=sys.stderr)
        return False

    if not isinstance(metadata, dict):
        print(f"Error: Frontmatter is not a mapping in {filepath}", file=sys.stderr)
        return False

    # FR-3: check required fields
    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] is None:
            print(f"Error: Missing required field '{field}' in {filepath}", file=sys.stderr)
            return False

    # FR-4: validate ID format — strictly sequential numerical, no semantic qualifiers
    artifact_id = str(metadata["id"])
    if not CANONICAL_ID_PATTERN.match(artifact_id):
        print(f"Error: Invalid ID format '{artifact_id}' in {filepath}. "
              f"Expected e.g. SPEC-001 (type prefix, hyphen, digits).", file=sys.stderr)
        return False

    # Validate type enum
    if metadata["type"] not in ALLOWED_TYPES:
        print(f"Error: Invalid type '{metadata['type']}' in {filepath}. "
              f"Allowed: {ALLOWED_TYPES}", file=sys.stderr)
        return False

    # Validate status enum
    if metadata["status"] not in ALLOWED_STATUSES:
        print(f"Error: Invalid status '{metadata['status']}' in {filepath}. "
              f"Allowed: {ALLOWED_STATUSES}", file=sys.stderr)
        return False

    # derived_from must be a list
    if not isinstance(metadata["derived_from"], list):
        print(f"Error: Field 'derived_from' must be a list in {filepath}", file=sys.stderr)
        return False

    print(f"OK: {filepath} — metadata valid")
    return True


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file> [<file> ...]", file=sys.stderr)
        sys.exit(1)

    all_ok = True
    for path in sys.argv[1:]:
        if not validate_file(path):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
