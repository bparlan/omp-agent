"""
_frontmatter.py — OMP AEF shared YAML frontmatter extraction utility.

Extracts and parses YAML frontmatter (delimited by --- ... ---) from
Markdown files. Used by both validate_metadata.py and resolve_artifact.py
to ensure structural consistency in frontmatter parsing.

Usage:
    from _frontmatter import extract_frontmatter
    metadata = extract_frontmatter(filepath)
    if metadata is not None:
        ...
"""

import re
import yaml


def extract_frontmatter(filepath: str):
    """Extract and parse YAML frontmatter from a file.

    Opens the file, reads its content, and extracts the YAML frontmatter
    block delimited by --- ... --- at the start of the file.

    Args:
        filepath: Path to the file to parse.

    Returns:
        A dict of parsed YAML metadata, or None if no valid frontmatter
        is found (missing delimiters, unparseable YAML, or non-dict content).
    """
    try:
        with open(filepath, "r") as fh:
            content = fh.read()
    except (IOError, OSError):
        return None

    # Strip UTF-8 BOM if present (\ufeff = \xef\xbb\xbf)
    if content.startswith("\ufeff"):
        content = content[1:]

    # Extract YAML frontmatter delimited by --- ... ---
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

    if not isinstance(metadata, dict):
        return None

    return metadata
