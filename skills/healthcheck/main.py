#!/usr/bin/env python3
"""
Main orchestrator for AEF-OMP Skill Health Checker.
Coordinates all modular components and maintains backward compatibility.
"""

import sys
import traceback
from pathlib import Path
from datetime import datetime

# Import modular components - ALL FROM PROJECT ROOT as per M8S4 requirements
from core.validation import SkillValidator
from discovery import get_skills_directory, discover_skills, discover_skill_by_name
from reporting import (
    generate_badges,
    generate_health_report,
    generate_processed_skills,
    generate_skills_summary
)
# Import cli from project root (not local directory) - updated for M8S4
from cli import (
    parse_arguments,
    run_health_check,
    print_help
)
def run_single_skill_validation(skill_name: str) -> dict:
    """Validate a single skill using the modular validation system."""
    skill_file = discover_skill_by_name(skill_name)
    if not skill_file:
        print(f"Skill '{skill_name}' not found")
        return None

    validator = SkillValidator()
    result = validator.validate_skill_file(skill_file)
    return result
def run_batch_validation() -> list:
    """Run batch validation in 3 systematic batches."""
    skills = discover_skills()
    all_results = []

    # Batch 1: Core skills (first 3)
    print("=== BATCH 1: Core ===")
    batch1_skills = skills[:3]
    for skill_name in batch1_skills:
        result = run_single_skill_validation(skill_name)
        if result:
            all_results.append(result)

    # Batch 2: Extensions skills (next 3)
    print("=== BATCH 2: Extensions ===")
    batch2_skills = skills[3:6]
    for skill_name in batch2_skills:
        result = run_single_skill_validation(skill_name)
        if result:
            all_results.append(result)

    # Batch 3: Edge Cases skills (remaining)
    print("=== BATCH 3: Edge Cases ===")
    batch3_skills = skills[6:]
    for skill_name in batch3_skills:
        result = run_single_skill_validation(skill_name)
        if result:
            all_results.append(result)

    return all_results
def run_all_skills_validation() -> list:
    """Run health check on all discovered skills."""
    skills = discover_skills()
    results = []

    for skill_name in skills:
        result = run_single_skill_validation(skill_name)
        if result:
            results.append(result)

    return results
class HealthCheckOrchestrator:
    """Orchestrates the health check process across all modules."""

    def __init__(self):
        self.validator = SkillValidator()
        self.skills_dir = get_skills_directory()

    def validate_skill(self, skill_name: str) -> dict:
        """Validate a single skill and return result."""
        skill_file = discover_skill_by_name(skill_name)
        if not skill_file:
            print(f"Skill '{skill_name}' not found")
            return None

        result = self.validator.validate_skill_file(skill_file)
        return result

    def process_all(self):
        """Process all skills and generate reports."""
        skills = discover_skills()
        all_results = []

        for skill_name in skills:
            result = self.validate_skill(skill_name)
            if result:
                all_results.append(result)

        return all_results
def legacy_healthcheck_main():
    """Legacy main function for backward compatibility."""

    try:
        # Parse command line arguments
        args = parse_arguments()

        # Check for help flag
        if args.help_flag:
            print_help()
            return 0

        # Run appropriate mode based on arguments
        if args.skill_name:
            # Single skill mode
            results = run_single_skill_validation(args.skill_name)
            if not results:
                return 1

        elif args.all_flag:
            # Batch mode
            results = run_batch_validation()

        else:
            # Default mode
            results = run_all_skills_validation()

        # Generate reports
        generate_all_reports(results)

        return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        return 1
def main():
    """Main entry point - supports both legacy and modular execution."""
    return legacy_healthcheck_main()
if __name__ == "__main__":
    exit(main())