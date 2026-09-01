#!/usr/bin/env python3
"""
main.py - M8S5 Main Entry Point Module

Minimal entry point that orchestrates the core healthcheck modules
(validation, discovery, reporting, cli) and maintains backward
compatibility with existing CLI invocation patterns.
"""

import sys
from typing import Optional, List
from pathlib import Path

# Ensure project root is on sys.path for module imports
sys.path.insert(0, str(Path(__file__).parent))

import cli
from discovery import DiscoveryError
from core.validation import ValidationError


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the healthcheck CLI.

    Args:
        argv: Optional list of command-line arguments.
            Defaults to sys.argv[1:] when None.

    Returns:
        int: Exit status (0 for success, non-zero for failure).
    """
    if argv is not None:
        sys.argv = [sys.argv[0]] + argv

    try:
        args = cli.parse_arguments()

        if args.help_flag:
            cli.print_help()
            return 0

        results = cli.run_health_check(
            skill_name=args.skill_name if args.skill_name else None,
            all_flag=args.all_flag,
        )
        cli.generate_all_reports(results)

        return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user.", file=sys.stderr)
        return 1
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 0
    except DiscoveryError as e:
        print(f"Discovery error: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
