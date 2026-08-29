#!/usr/bin/env python3
"""
Skill Health Checker CLI Wrapper

Entry point for the HealthCheck Skill modular architecture.
This wrapper maintains backward compatibility while delegating to the new modular architecture.
"""

import sys
from pathlib import Path

# Add the script's directory to Python path to import modules from root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    """Entry point that delegates to the root-level cli module."""
    try:
        from cli import parse_arguments, run_health_check, print_help, generate_all_reports

        # Parse command line arguments
        args = parse_arguments()

        # Check for help flag
        if args.help_flag:
            print_help()
            return 0

        # Run health check based on arguments
        results = run_health_check(
            skill_name=args.skill_name if args.skill_name else None,
            all_flag=args.all_flag
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