#!/usr/bin/env python3
"""
resolve_artifact.py — OMP AEF Artifact Resolution Utility (FR-7, FR-8, FR-9, FR-15)

Resolves an artifact identifier (canonical or legacy) to a file path using
a strict priority with legacy manifest fallback:
  1. Explicit YAML metadata — Scan YAML frontmatter for canonical IDs
  2. Canonical Directory Context — Infer type from identifier prefix, search subdirectory
  3. Legacy filename heuristics — Match against pre-M10 naming patterns
  4. Legacy manifest lookup — Consult legacy_indexer's manifest as fallback

Conflict detection: When a file's YAML `type` field disagrees with its directory
location, the script flags it as a conflict and exits with code 2.

Usage:
  python3 bin/resolve_artifact.py <identifier> --milestone <M_ID> [--verbose] [--cwd <path>]
"""

import sys
import os
import re
import argparse

from _frontmatter import extract_frontmatter

# Canonical type prefix to directory name mapping
TYPE_DIR_MAP = {
    "SPEC": "specifications",
    "VER": "verifications",
    "TEST": "tests",
    "INV": "investigations",
    "COMP": "implementations",
    "EVAL": "evaluations",
    "REVIEW": "reviews",
    "AUDIT": "audits",
}

DIR_TO_TYPE = {
    "specifications": "specification",
    "verifications": "verification",
    "tests": "test_set",
    "investigations": "investigation",
    "implementations": "completion",
    "evaluations": "evaluation",
    "reviews": "review",
    "audits": "audit",
}

# Canonical ID pattern: TYPE-NNN
CANONICAL_ID_PATTERN = re.compile(r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT)-\d+$")

# Legacy ID pattern: M{X}S{Y}[SUFFIX][{Z}]
LEGACY_ID_PATTERN = re.compile(r"^M(\d+)S(\d+)([A-Z]+)?(\d+)?$")

# Legacy filename patterns for matching files
LEGACY_FILENAME_PATTERN = re.compile(r"^M(\d+)S(\d+)([A-Z]+?)(\d+)?\.md$")

def resolve_yaml_frontmatter(filepath):
    """Extract YAML frontmatter from a file.
    
    Wraps _frontmatter.extract_frontmatter() to preserve the existing
    (metadata, None) / (None, error_msg) return convention.
    """
    try:
        metadata = extract_frontmatter(filepath)
    except IOError as e:
        return None, str(e)
    return metadata, None

def get_expected_type_from_directory(fpath):
    """Infer the expected artifact type from the file's parent directory name."""
    parent = os.path.basename(os.path.dirname(fpath))
    return DIR_TO_TYPE.get(parent)


def resolve_tier1(identifier, milestone_dir, verbose):
    """Tier 1: Scan all .md files for YAML frontmatter matching the identifier.
    
    Only matches canonical IDs (TYPE-NNN format). Returns (filepath, metadata).
    """
    # Tier 1 only applies to canonical IDs
    if not CANONICAL_ID_PATTERN.match(identifier):
        if verbose:
            print(f"Tier 1: Skipped — identifier '{identifier}' is not a canonical ID",
                  file=sys.stderr)
        return None, None

    if verbose:
        print("Tier 1: Scanning YAML frontmatter...", file=sys.stderr)

    for root, dirs, files in os.walk(milestone_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            metadata, err = resolve_yaml_frontmatter(fpath)
            if err:
                if verbose:
                    print(f"Tier 1: Error reading {fpath}: {err}", file=sys.stderr)
                continue
            if metadata and str(metadata.get("id", "")) == identifier:
                if verbose:
                    print(f"Tier 1: YAML metadata match — {fpath}", file=sys.stderr)
                return fpath, metadata

    if verbose:
        print("Tier 1: No YAML metadata match found", file=sys.stderr)
    return None, None


def resolve_tier2(identifier, milestone_dir, verbose):
    """Tier 2: Infer artifact type from identifier prefix, search canonical subdirectory.
    
    For canonical IDs (e.g., SPEC-001 → specifications/), search for the file
    in the corresponding type subdirectory. Returns (filepath, metadata, type_dir_name).
    """
    prefix_match = CANONICAL_ID_PATTERN.match(identifier)
    if not prefix_match:
        if verbose:
            print(f"Tier 2: Skipped — identifier '{identifier}' is not a canonical ID",
                  file=sys.stderr)
        return None, None, None

    prefix = prefix_match.group(1)
    type_dir = TYPE_DIR_MAP.get(prefix)
    if not type_dir:
        if verbose:
            print(f"Tier 2: No directory mapping for prefix '{prefix}'", file=sys.stderr)
        return None, None, None

    search_dir = os.path.join(milestone_dir, type_dir)
    if not os.path.isdir(search_dir):
        if verbose:
            print(f"Tier 2: Directory '{type_dir}/' not found in milestone", file=sys.stderr)
        return None, None, type_dir

    if verbose:
        print(f"Tier 2: Searching '{type_dir}/' directory...", file=sys.stderr)

    for fname in os.listdir(search_dir):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(search_dir, fname)
        # Match by filename containing the identifier
        if identifier in fname:
            metadata, _ = resolve_yaml_frontmatter(fpath)
            if verbose:
                print(f"Tier 2: Directory context match — {fpath}", file=sys.stderr)
            return fpath, metadata, type_dir

    if verbose:
        print(f"Tier 2: No match found in '{type_dir}/' directory", file=sys.stderr)
    return None, None, type_dir


def resolve_tier3(identifier, milestone_dir, verbose):
    """Tier 3: Legacy filename heuristics for pre-M10 artifacts.
    
    Matches against legacy naming patterns with strict boundary checking:
    - M{X}S{Y}.md                   (exact stem match)
    - M{X}S{Y}{SUFFIX}.md           (suffix: V, T, C, E, R, I, H)
    - M{X}S{Y}{SUFFIX}{N}.md        (suffix + index number)
    
    Strict boundary: the character immediately following the matched
    identifier prefix MUST be '.' or a valid lifecycle suffix letter
    (V, T, C, E, R, I, H) optionally followed by an index number.
    E.g. "M7S1" matches "M7S1.md" and "M7S1V.md" but NOT "M7S10.md".
    """
    if not LEGACY_ID_PATTERN.match(identifier):
        if verbose:
            print(f"Tier 3: Skipped — identifier '{identifier}' does not match legacy pattern",
                  file=sys.stderr)
        return None, None
    
    VALID_LEGACY_SUFFIXES = frozenset({"V", "T", "C", "E", "R", "I", "H"})
    
    if verbose:
        print("Tier 3: Applying legacy filename heuristics...", file=sys.stderr)
    
    for root, dirs, files in os.walk(milestone_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            
            stem = os.path.splitext(fname)[0]
            
            # Exact stem match: "M7S1.md"  →  identifier "M7S1"
            if stem == identifier:
                fpath = os.path.join(root, fname)
                metadata, _ = resolve_yaml_frontmatter(fpath)
                if verbose:
                    print(f"Tier 3: Legacy filename exact match — {fpath}",
                          file=sys.stderr)
                return fpath, metadata
            
            # Suffix match with strict boundary.
            # "M7S1V.md"   → stem="M7S1V",  suffix after "M7S1" = "V"      → valid
            # "M7S1T1.md"  → stem="M7S1T1", suffix after "M7S1" = "T1"     → valid
            # "M7S10.md"   → stem="M7S10",  suffix after "M7S1" = "0"      → INVALID
            # "M7S1A.md"   → stem="M7S1A",  suffix after "M7S1" = "A"      → INVALID
            if stem.startswith(identifier):
                suffix = stem[len(identifier):]
                if (
                    len(suffix) >= 1
                    and suffix[0] in VALID_LEGACY_SUFFIXES
                    and (len(suffix) == 1 or suffix[1].isdigit())
                ):
                    fpath = os.path.join(root, fname)
                    metadata, _ = resolve_yaml_frontmatter(fpath)
                    if verbose:
                        print(f"Tier 3: Legacy filename heuristic match — {fpath}",
                              file=sys.stderr)
                    return fpath, metadata
    
    if verbose:
        print("Tier 3: No legacy filename match found", file=sys.stderr)

def resolve_legacy_manifest(identifier, base_dir, milestone_dir, verbose):
    """Tier 4: Legacy manifest lookup.
    
    Consults the legacy manifest (produced by legacy_indexer.py) as a fallback
    when Tier 3 filename heuristics produce no match.
    
    Searches for the manifest at:
      1. {base_dir}/legacy_manifest.txt
      2. {base_dir}/milestones/{milestone_id}/legacy_manifest.txt
      3. {milestone_dir}/legacy_manifest.txt
    
    Returns (filepath, None) if a match is found, or (None, None).
    """
    if not LEGACY_ID_PATTERN.match(identifier):
        if verbose:
            print(f"Tier 4 (Legacy Manifest): Skipped — identifier '{identifier}' "
                  f"does not match legacy pattern", file=sys.stderr)
        return None, None
    
    # Find the legacy manifest
    manifest_path = None
    candidates = [
        os.path.join(base_dir, "legacy_manifest.txt"),
        os.path.join(base_dir, "milestones", os.path.basename(milestone_dir), "legacy_manifest.txt"),
        os.path.join(milestone_dir, "legacy_manifest.txt"),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            manifest_path = candidate
            if verbose:
                print(f"Tier 4 (Legacy Manifest): Found manifest at {candidate}",
                      file=sys.stderr)
            break
    
    if not manifest_path:
        if verbose:
            print("Tier 4 (Legacy Manifest): No legacy manifest found", file=sys.stderr)
        return None, None
    
    if verbose:
        print("Tier 4 (Legacy Manifest): Consulting legacy manifest...", file=sys.stderr)
    
    try:
        with open(manifest_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Skip lines with AMBIGUOUS_LEGACY_ARTIFACT — not a valid resolution
                if "AMBIGUOUS_LEGACY_ARTIFACT" in line:
                    continue
                # Parse: <SHA-256> <relative-path>
                parts = line.split(" ", 1)
                if len(parts) != 2:
                    continue
                rel_path = parts[1]
                fname = os.path.basename(rel_path)
                stem = os.path.splitext(fname)[0]
                
                # Check if the stem matches the identifier exactly
                if stem == identifier:
                    full_path = os.path.join(base_dir, rel_path)
                    if os.path.isfile(full_path):
                        if verbose:
                            print(f"Tier 4 (Legacy Manifest): Match — {full_path}",
                                  file=sys.stderr)
                        return full_path, None
    except (IOError, OSError) as e:
        if verbose:
            print(f"Tier 4 (Legacy Manifest): Error reading manifest: {e}",
                  file=sys.stderr)
        return None, None
    
    if verbose:
        print("Tier 4 (Legacy Manifest): No match found", file=sys.stderr)
    return None, None


def detect_conflict(fpath, metadata, identifier, verbose):
    """Check if the file's YAML 'type' disagrees with its directory location.
    
    Returns a conflict dict with file_path, expected_type, actual_type, and identifier,
    or None if no conflict is detected.
    """
    if not metadata or not metadata.get("type"):
        if verbose:
            print(f"Conflict check: No metadata or type field for {fpath}", file=sys.stderr)
        return None

    actual_type = metadata["type"]
    expected_type = get_expected_type_from_directory(fpath)

    if not expected_type:
        if verbose:
            print(f"Conflict check: No type mapping for directory '{os.path.basename(os.path.dirname(fpath))}'",
                  file=sys.stderr)
        return None

    if actual_type != expected_type:
        conflict = {
            "file_path": fpath,
            "expected_type": expected_type,
            "actual_type": actual_type,
            "identifier": identifier,
        }
        if verbose:
            print(f"CONFLICT: {conflict}", file=sys.stderr)
        return conflict

    if verbose:
        print(f"Conflict check: No conflict — type '{actual_type}' matches directory",
              file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="OMP AEF Artifact Resolution Utility",
        epilog="Exit codes: 0=resolved, 1=not found, 2=conflict detected",
    )
    parser.add_argument("identifier", help="Canonical ID (SPEC-001) or legacy ID (M7S1)")
    parser.add_argument(
        "--milestone", "-m", required=True,
        help="Milestone ID (e.g., M7)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Print resolution trace to stderr",
    )
    parser.add_argument(
        "--cwd",
        help="Base directory containing milestone subdirectory (for testing with fixtures)",
    )
    args = parser.parse_args()

    # Determine milestone directory
    if args.cwd:
        base_dir = os.path.abspath(args.cwd)
    else:
        # Resolve project root relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(script_dir, ".."))

    milestone_dir = os.path.join(base_dir, args.milestone)

    if not os.path.isdir(milestone_dir):
        print(f"Error: Milestone directory not found: {milestone_dir}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Milestone directory: {milestone_dir}", file=sys.stderr)
        print(f"Queried identifier: {args.identifier}", file=sys.stderr)

    # === Tier 1: YAML metadata scan ===
    fpath, metadata = resolve_tier1(args.identifier, milestone_dir, args.verbose)
    if fpath:
        conflict = detect_conflict(fpath, metadata, args.identifier, args.verbose)
        if conflict:
            print(
                f"Conflict: File {conflict['file_path']} has type "
                f"'{conflict['actual_type']}' in directory "
                f"'{os.path.basename(os.path.dirname(conflict['file_path']))}' "
                f"(expected '{conflict['expected_type']}')",
            )
            sys.exit(2)
        print(os.path.abspath(fpath))
        sys.exit(0)

    # === Tier 2: Canonical directory context ===
    fpath, metadata, type_dir = resolve_tier2(args.identifier, milestone_dir, args.verbose)
    if fpath:
        conflict = detect_conflict(fpath, metadata, args.identifier, args.verbose)
        if conflict:
            print(
                f"Conflict: File {conflict['file_path']} has type "
                f"'{conflict['actual_type']}' in directory "
                f"'{os.path.basename(os.path.dirname(conflict['file_path']))}' "
                f"(expected '{conflict['expected_type']}')",
            )
            sys.exit(2)
        print(os.path.abspath(fpath))
        sys.exit(0)

    # === Tier 3: Legacy filename heuristics ===
    fpath, metadata = resolve_tier3(args.identifier, milestone_dir, args.verbose)
    if fpath:
        # Check for conflict in the legacy path too
        conflict = detect_conflict(fpath, metadata, args.identifier, args.verbose)
        if conflict:
            print(
                f"Conflict: File {conflict['file_path']} has type "
                f"'{conflict['actual_type']}' in directory "
                f"'{os.path.basename(os.path.dirname(conflict['file_path']))}' "
                f"(expected '{conflict['expected_type']}')",
            )
            sys.exit(2)
        print(os.path.abspath(fpath))
        sys.exit(0)

    # === Tier 4: Legacy manifest lookup ===
    fpath, _ = resolve_legacy_manifest(args.identifier, base_dir, milestone_dir, args.verbose)
    if fpath:
        print(os.path.abspath(fpath))
        sys.exit(0)

    # === Not found ===
    print(f"Error: Artifact not found: {args.identifier}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()