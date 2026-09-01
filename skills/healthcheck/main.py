#!/usr/bin/env python3
"""
Main orchestrator for AEF-OMP Skill Health Checker.
Coordinates all modular components and maintains backward compatibility.
"""

import sys
import importlib.util

# Import modular components - ALL FROM PROJECT ROOT as per M8S4 requirements
from core.validation import SkillValidator
from discovery import get_skills_directory, discover_skills, discover_skill_by_name
from reporting import generate_badges, generate_health_report, generate_skills_summary

# Import cli from project root (not local directory) - updated for M8S4
from cli import parse_arguments, run_health_check, print_help


def run_single_skill_execution(skill_name: str) -> dict:
    """Execute a single skill using dynamic import"""
    try:
        # Discover the skill file
        skill_file = discover_skill_by_name(skill_name)
        if not skill_file:
            print(f"Skill '{skill_name}' not found")
            return {"status": "error", "message": f"Skill '{skill_name}' not found"}

        # Use importlib to execute the skill
        spec = importlib.util.spec_from_file_location(skill_name, skill_file)
        if spec is None or spec.loader is None:
            return {
                "status": "error",
                "message": f"Cannot load skill module: {skill_name}",
            }

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call main() if available
        if hasattr(module, "main"):
            print(f"Executing {skill_name}...")
            exit_code = module.main()
            return {
                "status": "success" if exit_code == 0 else "error",
                "exit_code": exit_code,
                "message": f"Skill executed with exit code: {exit_code}",
            }
        else:
            return {
                "status": "error",
                "message": f"Skill {skill_name} has no main() function",
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error executing skill '{skill_name}': {e}",
        }


def run_single_skill_validation(skill_name: str) -> dict:
    """Validate a single skill using the modular validation system."""
    skill_file = discover_skill_by_name(skill_name)
    if not skill_file:
        print(f"Skill '{skill_name}' not found")
        return {"status": "error", "message": f"Skill '{skill_name}' not found"}

    validator = SkillValidator()
    result = validator.validate_skill_file(skill_file)
    return result


def run_batch_validation() -> list:
    """Run batch validation in 3 systematic batches."""
    try:
        all_results = []

        # Process skills in 3 batches for deterministic ordering
        skills_dir = get_skills_directory()
        all_skills = discover_skills(skills_dir)

        if not all_skills:
            return []

        # Split into 3 batches (deterministic)
        batch_size = (len(all_skills) + 2) // 3
        batch1 = all_skills[:batch_size]
        batch2 = all_skills[batch_size : 2 * batch_size]
        batch3 = all_skills[2 * batch_size :]

        # Process each batch
        for batch in [batch1, batch2, batch3]:
            for skill_name in batch:
                result = run_single_skill_validation(skill_name)
                if result:
                    result["batch"] = f"Batch {(len(all_results) // batch_size) + 1}"
                    all_results.append(result)

        return all_results

    except Exception as e:
        print(f"Error in batch validation: {e}", file=sys.stderr)
        return []


def run_all_skills_validation() -> list:
    """Run health check on all discovered skills."""
    try:
        all_results = []

        # Discover all skills
        skills_dir = get_skills_directory()
        all_skills = discover_skills(skills_dir)

        for skill_name in all_skills:
            result = run_single_skill_validation(skill_name)
            if result:
                all_results.append(result)

        return all_results

    except Exception as e:
        print(f"Error in all skills validation: {e}", file=sys.stderr)
        return []


def legacy_healthcheck_main():
    """Legacy main function for backward compatibility."""
    try:
        args = parse_arguments()

        if args.help_flag:
            print_help()
            return 0

        results = run_health_check(
            skill_name=args.skill_name if args.skill_name else None,
            all_flag=args.all_flag,
        )

        if results:
            print("\n=== Health Check Results ===")
            for result in results:
                print(
                    f"  - {result.get('name', 'Unknown')}: {result.get('status', 'unknown')}"
                )
        else:
            print("No skills found or validation failed.")

        generate_all_reports(results)

        return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user.", file=sys.stderr)
        return 1
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def generate_all_reports(results: list) -> None:
    """Generate all reports from validation results"""
    try:
        # Generate health report
        health_report = generate_health_report(results)
        print(health_report)

        # Generate badges
        badges = generate_badges(results)
        print(badges)

        # Generate skills summary
        skills_summary = generate_skills_summary(results)
        print(skills_summary)

    except Exception as e:
        print(f"Error generating reports: {e}", file=sys.stderr)


def main():
    """Main entry point - supports both legacy and modular execution."""
    return legacy_healthcheck_main()


if __name__ == "__main__":
    exit(main())
