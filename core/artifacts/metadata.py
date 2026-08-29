import re

import yaml
from typing import Dict, Any, Optional, List


def parse_metadata(content: str) -> Dict[str, Any]:
    """Parses metadata from content, assuming YAML frontmatter."""
    try:
        parts = content.split('---\n', 2)
        if len(parts) < 2:
            return {}
        metadata_str = parts[1]
        metadata = yaml.safe_load(metadata_str)
        return metadata if isinstance(metadata, dict) else {}
    except yaml.YAMLError:
        return {}


def get_metadata_from_file(file_path: str) -> Dict[str, Any]:
    """Reads a file and extracts metadata from its YAML frontmatter."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return parse_metadata(content)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def extract_frontmatter(filepath: str) -> Optional[Dict[str, Any]]:
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
        with open(filepath, "r", encoding="utf-8") as fh:
            content = fh.read()
    except (IOError, OSError):
        return None

    # Strip UTF-8 BOM if present
    if content.startswith('\ufeff'):
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
