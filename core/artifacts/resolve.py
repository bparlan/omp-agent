#!/usr/bin/env python3
"""
Artifact Resolution CLI - FR-RESOLVER_IMPLEMENTATION

Command-line interface for the canonical artifact resolution system.
Implements the contract: python3 -m core.artifacts.resolve --identity <artifact_id> --type <artifact_type> --metadata-filter <json_filter> --strict <boolean>
"""

import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)
import json
import argparse
from typing import Dict, Any

# Import the core resolution function
from .resolution import resolve_artifact


def json_parser(json_str: str) -> Dict[str, Any]:
    """Parse JSON string argument."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"Invalid JSON: {e}")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Resolve artifacts by identity, type, or metadata filter"
    )

    parser.add_argument(
        "--identity", help="Artifact identity to resolve (e.g., M9S1I1 or SPEC-001)"
    )

    parser.add_argument(
        "--type", dest="artifact_type", help="Artifact type to filter by"
    )

    parser.add_argument(
        "--metadata-filter",
        dest="metadata_filter",
        type=json_parser,
        help="JSON object for metadata filtering",
    )

    parser.add_argument(
        "--strict",
        type=lambda x: x.lower() in ("true", "1", "yes", "on"),
        default=True,
        help="Strict resolution mode (default: True)",
    )

    args = parser.parse_args()

    try:
        result = resolve_artifact(
            identity=args.identity,
            type=args.artifact_type,
            metadata_filter=args.metadata_filter,
            strict=args.strict,
        )

        # Output JSON result
        print(json.dumps(result, indent=2))

        # Exit with appropriate code
        if result.get("resolved", False):
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        # Output error in required format
        error_result = {
            "resolved": False,
            "error": {"type": type(e).__name__, "message": str(e)},
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
