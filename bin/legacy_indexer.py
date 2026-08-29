#!/usr/bin/env python3
"""
legacy_indexer.py — OMP AEF Legacy Artifact Indexer (FR-11, FR-12, FR-13, FR-14)

Scans pre-M10 milestone directories (M1-M9), computes SHA-256 checksums,
and classifies artifacts via a strict 6-tier fallback system.

Tiers:
  1. YAML frontmatter metadata
  2. Directory structure inference
  3. Top-level Markdown headers
  4. Legacy filename naming conventions
  5. Custom filename pattern mapping
  6. Human review — AMBIGUOUS_LEGACY_ARTIFACT

Output (legacy manifest): one line per scanned file.
  Classified:   <SHA-256> <relative-path>
  Unclassified: <SHA-256> <relative-path> unclassified:AMBIGUOUS_LEGACY_ARTIFACT

Usage:
  python3 bin/legacy_indexer.py [--milestone-dir <path>] [--output <path>]
                                [--verbose] [--pattern-map <path>]
"""

import sys
import os
import re
import hashlib
import argparse

from core.artifacts.metadata import extract_frontmatter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Directory name → artifact type mapping (mirrors resolve_artifact.py)
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

# Markdown heading text → artifact type (Tier 3)
HEADING_TO_TYPE = {
    "specification": "specification",
    "specifications": "specification",
    "verification": "verification",
    "test plan": "test_set",
    "tests": "test_set",
    "investigation": "investigation",
    "completion report": "completion",
    "completion": "completion",
    "evaluation report": "evaluation",
    "evaluation": "evaluation",
    "review report": "review",
    "review": "review",
    "audit": "audit",
    "audits": "audit",
    "architecture": "architecture",
}

# Legacy filename suffix → artifact type (Tier 4)
# Format: M{X}S{Y}[SUFFIX][N].md
LEGACY_FILENAME_TYPE = {
    "": "specification",   # M1S1.md
    "V": "verification",
    "T": "test_set",
    "C": "completion",
    "E": "evaluation",
    "R": "review",
    "I": "investigation",
    "H": "hotfix",
}

# Legacy filename pattern: M{X}S{Y}[SUFFIX][{Z}].md
LEGACY_FILENAME_PATTERN = re.compile(
    r"^M(\d+)S(\d+)([A-Z]*?)(\d+)?\.md$"
)

# Valid single-letter suffixes for legacy filenames
VALID_LEGACY_SUFFIXES = frozenset({"V", "T", "C", "E", "R", "I", "H"})




# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------

def classify_tier1(filepath, verbose):
    """Tier 1: Classify via YAML frontmatter metadata.

    Returns (artifact_type, classification_source) or (None, None).
    """
    try:
        metadata = extract_frontmatter(filepath)
    except (UnicodeDecodeError, ValueError):
        return None, None
    if metadata is not None:
        # Check explicit 'type' field
        if "type" in metadata and isinstance(metadata["type"], str):
            if verbose:
                print(f"  Tier 1: '{os.path.basename(filepath)}' type={metadata['type']}",
                      file=sys.stderr)
            return metadata["type"], "frontmatter.type"
        # Fall back to inferring from 'id' field (e.g., SPEC-001 → specification)
        if "id" in metadata and isinstance(metadata["id"], str):
            id_str = str(metadata["id"])
            prefix_match = re.match(r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT|HOT)-\d+$", id_str)
            if prefix_match:
                prefix = prefix_match.group(1)
                TYPE_PREFIX_TO_DIR = {
                    "SPEC": "specifications",
                    "VER": "verifications",
                    "TEST": "tests",
                    "INV": "investigations",
                    "COMP": "implementations",
                    "EVAL": "evaluations",
                    "REVIEW": "reviews",
                    "AUDIT": "audits",
                    "HOT": "hotfixes",
                }
                dir_name = TYPE_PREFIX_TO_DIR.get(prefix)
                if dir_name and dir_name in DIR_TO_TYPE:
                    if verbose:
                        print(f"  Tier 1: '{os.path.basename(filepath)}' id={id_str} → {DIR_TO_TYPE[dir_name]}",
                              file=sys.stderr)
                    return DIR_TO_TYPE[dir_name], "frontmatter.id"
    return None, None


def classify_tier2(filepath, verbose):
    """Tier 2: Classify via directory structure.

    Infers artifact type from the parent directory name.
    Returns (artifact_type, classification_source) or (None, None).
    """
    parent = os.path.basename(os.path.dirname(filepath))
    if parent in DIR_TO_TYPE:
        if verbose:
            print(f"  Tier 2: '{os.path.basename(filepath)}' dir={parent} → {DIR_TO_TYPE[parent]}",
                  file=sys.stderr)
        return DIR_TO_TYPE[parent], "directory"
    return None, None


def classify_tier3(filepath, verbose):
    """Tier 3: Classify via top-level Markdown headers.

    Reads the first line and checks for '# <heading>' patterns.
    Returns (artifact_type, classification_source) or (None, None).
    """
    try:
        with open(filepath, "r") as f:
            first_line = f.readline().strip()
    except (IOError, OSError, UnicodeDecodeError):
        return None, None

    if first_line.startswith("##"):
        # Skip subheadings — only top-level
        return None, None

    if first_line.startswith("# "):
        heading = first_line[2:].strip().lower()
        if heading in HEADING_TO_TYPE:
            if verbose:
                print(f"  Tier 3: '{os.path.basename(filepath)}' heading='{heading}' → {HEADING_TO_TYPE[heading]}",
                      file=sys.stderr)
            return HEADING_TO_TYPE[heading], "heading"
    return None, None


def classify_tier4(filepath, verbose):
    """Tier 4: Classify via legacy filename naming conventions.

    Matches M{X}S{Y}[SUFFIX][N].md patterns.
    Returns (artifact_type, classification_source) or (None, None).
    """
    fname = os.path.basename(filepath)
    match = LEGACY_FILENAME_PATTERN.match(fname)
    if match:
        suffix = match.group(3) if match.group(3) else ""
        # Validate suffix — must be a known single or compound letter
        if suffix == "":
            # M1S1.md → specification
            if verbose:
                print(f"  Tier 4: '{fname}' stem match → specification", file=sys.stderr)
            return "specification", "filename"
        elif suffix in VALID_LEGACY_SUFFIXES:
            if suffix in LEGACY_FILENAME_TYPE:
                if verbose:
                    print(f"  Tier 4: '{fname}' suffix={suffix} → {LEGACY_FILENAME_TYPE[suffix]}",
                          file=sys.stderr)
                return LEGACY_FILENAME_TYPE[suffix], "filename"
    return None, None


def classify_tier5(filepath, pattern_map, verbose):
    """Tier 5: Classify via custom filename pattern mapping.

    pattern_map: dict of {filename: artifact_type}
    Returns (artifact_type, classification_source) or (None, None).
    """
    if pattern_map is None:
        return None, None
    fname = os.path.basename(filepath)
    if fname in pattern_map:
        atype = pattern_map[fname]
        if verbose:
            print(f"  Tier 5: '{fname}' custom pattern → {atype}", file=sys.stderr)
        return atype, "custom_pattern"
    return None, None


def load_pattern_map(pattern_map_path):
    """Load custom filename→type mapping from a text file.

    Format: one line per entry, <filename>:<artifact_type>
    Returns dict of {filename: artifact_type}.
    """
    mapping = {}
    if not pattern_map_path or not os.path.isfile(pattern_map_path):
        return mapping
    with open(pattern_map_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                fname, atype = line.split(":", 1)
                mapping[fname.strip()] = atype.strip()
    return mapping


# ---------------------------------------------------------------------------
# Core indexing
# ---------------------------------------------------------------------------

def is_pre_m10(dirname):
    """Check if a directory name matches M1-M9 pattern."""
    return re.match(r"^M([1-9])$", dirname) is not None


def sha256_file(filepath):
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def index_milestones(milestone_dir, output_path, verbose, pattern_map_path):
    """Scan M1-M9 directories, classify files, and write manifest.

    Returns 0 on success, 1 on error.
    """
    # Resolve the milestone base directory
    base_dir = os.path.abspath(milestone_dir)

    if not os.path.isdir(base_dir):
        print(f"Error: Milestone directory not found: {base_dir}", file=sys.stderr)
        return 1

    if verbose:
        print(f"Legacy Indexer: Scanning {base_dir}", file=sys.stderr)
        print(f"Legacy Indexer: Output → {os.path.abspath(output_path)}", file=sys.stderr)

    # Load custom pattern map (Tier 5)
    pattern_map = load_pattern_map(pattern_map_path)

    # Collect all pre-M10 files
    entries = []  # list of (sha256, rel_path, artifact_type)

    # Walk milestone directories for M1-M9
    for entry in sorted(os.listdir(base_dir)):
        entry_path = os.path.join(base_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        if not is_pre_m10(entry):
            if verbose:
                print(f"  Skipping non-M1-M9 directory: {entry}", file=sys.stderr)
            continue

        # Walk files in this milestone directory
        for root, _, files in os.walk(entry_path):
            for fname in sorted(files):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, base_dir)
                _classify_file(fpath, rel_path, base_dir, entries, pattern_map, verbose)

    # If no entries found and base_dir itself is an M1-M9 directory, scan it directly
    if not entries and is_pre_m10(os.path.basename(base_dir)):
        if verbose:
            print(f"  Scanning base directory as M1-M9: {base_dir}", file=sys.stderr)
        for root, _, files in os.walk(base_dir):
            for fname in sorted(files):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, base_dir)
                if verbose:
                    print(f"\nProcessing: {rel_path}", file=sys.stderr)
                _classify_file(fpath, rel_path, base_dir, entries, pattern_map, verbose)

    # Write manifest
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        for sha, rel_path, atype in entries:
            if atype == "AMBIGUOUS_LEGACY_ARTIFACT":
                f.write(f"{sha} {rel_path} unclassified:AMBIGUOUS_LEGACY_ARTIFACT\n")
            else:
                f.write(f"{sha} {rel_path}\n")

    if verbose:
        print(f"\nLegacy Indexer: Wrote {len(entries)} entries to {os.path.abspath(output_path)}",
              file=sys.stderr)

    return 0



def _classify_file(fpath, rel_path, base_dir, entries, pattern_map, verbose):
    """Run 6-tier classification on a single file and add it to entries."""
    fname = os.path.basename(fpath)
    if verbose:
        print(f"\nProcessing: {rel_path}", file=sys.stderr)

    atype = None

    # Tier 1: YAML frontmatter
    atype, source = classify_tier1(fpath, verbose)
    if atype:
        if verbose:
            print(f"  → {atype} (Tier 1: {source})", file=sys.stderr)
        _add_entry(entries, fpath, rel_path, atype, verbose)
        return

    # Tier 2: Directory structure
    atype, source = classify_tier2(fpath, verbose)
    if atype:
        if verbose:
            print(f"  → {atype} (Tier 2: {source})", file=sys.stderr)
        _add_entry(entries, fpath, rel_path, atype, verbose)
        return

    # Tier 3: Top-level Markdown headers
    atype, source = classify_tier3(fpath, verbose)
    if atype:
        if verbose:
            print(f"  → {atype} (Tier 3: {source})", file=sys.stderr)
        _add_entry(entries, fpath, rel_path, atype, verbose)
        return

    # Tier 4: Legacy filename naming
    atype, source = classify_tier4(fpath, verbose)
    if atype:
        if verbose:
            print(f"  → {atype} (Tier 4: {source})", file=sys.stderr)
        _add_entry(entries, fpath, rel_path, atype, verbose)
        return

    # Tier 5: Custom pattern mapping
    atype, source = classify_tier5(fpath, pattern_map, verbose)
    if atype:
        if verbose:
            print(f"  → {atype} (Tier 5: {source})", file=sys.stderr)
        _add_entry(entries, fpath, rel_path, atype, verbose)
        return

    # Tier 6: Human review / AMBIGUOUS_LEGACY_ARTIFACT
    if verbose:
        print(f"  Tier 6: '{fname}' → AMBIGUOUS_LEGACY_ARTIFACT (requires manual review)",
              file=sys.stderr)
        print(f"AMBIGUOUS_LEGACY_ARTIFACT: {rel_path} — requires manual review",
              file=sys.stderr)
    _add_entry(entries, fpath, rel_path, "AMBIGUOUS_LEGACY_ARTIFACT", verbose)
def _add_entry(entries, fpath, rel_path, atype, verbose):
    """Compute SHA-256 and add entry to the entries list."""
    try:
        sha = sha256_file(fpath)
        entries.append((sha, rel_path, atype))
    except (IOError, OSError) as e:
        if verbose:
            print(f"  Error reading {fpath}: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OMP AEF Legacy Artifact Indexer — maps M1-M9 files to SHA-256 checksums "
                    "with 6-tier classification fallback.",
        epilog="Exit codes: 0=success, 1=failure",
    )
    parser.add_argument(
        "--milestone-dir",
        default="milestones",
        help="Base path for M1-M9 directories (default: milestones/)",
    )
    parser.add_argument(
        "--output",
        default="milestones/M7/legacy_manifest.txt",
        help="Output path for legacy manifest (default: milestones/M7/legacy_manifest.txt)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print classification trace per file to stderr",
    )
    parser.add_argument(
        "--pattern-map",
        help="Path to custom filename pattern mapping file for Tier 5",
    )
    args = parser.parse_args()

    exit_code = index_milestones(
        milestone_dir=args.milestone_dir,
        output_path=args.output,
        verbose=args.verbose,
        pattern_map_path=args.pattern_map,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
