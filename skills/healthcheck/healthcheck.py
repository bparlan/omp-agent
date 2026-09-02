#!/usr/bin/env python3
"""
Healthcheck skill CLI wrapper.

Entry point for the HealthCheck Skill modular architecture.
This wrapper maintains backward compatibility while delegating to the new modular CLI.
"""

import sys
from pathlib import Path
import argparse

# Add the script's directory to Python path to import modules from root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import CLI functions directly at module level
# from cli import (
# parse_arguments,
# run_health_check,
#)

# Import from the modular components
from skills.healthcheck.cli import (
    parse_arguments,
    run_health_check,
    print_help,
    generate_all_reports,
)

def main():
    """Entry point that delegates to the CLI module."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Check for help flag
        if getattr(args, "help_flag", False) or getattr(args, "help", False):
            print_help()
            return 0

        # Run health check based on arguments
        results = run_health_check(
            skill_name=args.skill_name if args.skill_name else None,
            all_flag=args.all_flag,
        )

        # Generate all reports from the results
        generate_all_reports(results)

        return 0
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())
