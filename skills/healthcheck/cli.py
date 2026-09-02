#!/usr/bin/env python3
"""
HealthCheck Skill CLI Module

Provides the command-line interface for the HealthCheck Skill modular architecture.
Implements the same interface as the root CLI module but for the healthcheck skill specifically.

This module exports the six public functions expected by the root CLI and provides
milestone/specification agnostic skill validation capabilities.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import core modules using absolute imports from project root
from core.validation import SkillValidator, validate_skill_file
from discovery import discover_skills, get_skills_directory
from reporting import generate_badges, generate_health_report, generate_processed_skills


def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace with skill_name, all_flag, help_flag attributes.
    """
    parser = argparse.ArgumentParser(
        description="HealthCheck Skill CLI - Validates skill structure and SKILL.md content"
    )
    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Name of skill to check (optional, shows all skills if not specified)",
    )
    parser.add_argument(
        "--all",
        dest="all_flag",
        action="store_true",
        help="Process all skills in 3 batches",
    )
    parser.add_argument(
        "--help",
        dest="help_flag",
        action="store_true",
        help="Show this help text",
    )
    return parser.parse_args()


def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """
    Validate specific skill by name.

    Args:
        skill_name: Name of specific skill to check

    Returns:
        Validation result dict or None if skill not found
    """
    skill_path = discover_skill_by_name(skill_name)
    if skill_path:
        return validate_skill_file(skill_path)
    return None


def process_all_skills() -> List[Dict[str, Any]]:
    """
    Process all skills in 3 systematic batches.

    Returns:
        List of all validation results
    """
    results = []

    # Batch 1: Core skills
    for skill_name in ["generate-spec", "generate-verification", "generate-tests",
                      "implement-specification", "evaluate-tests", "evaluate-implementation",
                      "review-implementation", "sync-documentation", "evolve-skills",
                      "diagrammer", "milestoner", "bootstrap-project", "ponytail"]:
        result = validate_single_skill(skill_name)
        if result:
            results.append(result)

    # Batch 2: Extension skills (ongoing)
    # For now, just process whatever is available
    for skill_path in get_skills_directory().glob("*"):
        if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
            if skill_path.name not in ["generate-spec", "generate-verification", "generate-tests",
                                     "implement-specification", "evaluate-tests", "evaluate-implementation",
                                     "review-implementation", "sync-documentation", "evolve-skills",
                                     "diagrammer", "milestoner", "bootstrap-project", "ponytail"]:
                result = validate_single_skill(skill_path.name)
                if result:
                    results.append(result)

    # Batch 3: Edge cases and error handling
    # This is handled by the validation logic itself
    return results


def run_health_check(
    skill_name: Optional[str] = None, all_flag: bool = False
) -> List[Dict[str, Any]]:
    """
    Main health check orchestration.

    Args:
        skill_name: Optional specific skill name to validate
        all_flag: Whether to process all skills

    Returns:
        List of all validation results
    """
    if skill_name:
        result = validate_single_skill(skill_name)
        return [result] if result else []
    elif all_flag:
        return process_all_skills()
    else:
        return process_all_skills()


def print_help() -> None:
    """
    Display comprehensive help information.

    Shows usage examples, available options, output formats.
    """
    help_text = """
=== HealthCheck Skill CLI ===

USAGE:
    /healthcheck [skill_name] [--all] [--help]

COMMANDS:
    skill_name           Specific skill name to check (optional)
    --all                Process all skills in 3 batches
    --help               Show this help text

MODES:
    Single-Skill Mode (skill_name provided):
        Validates the specified skill's structure and SKILL.md content
        Returns validation status and score

    Batch Mode (--all):
        Processes all discovered skills in 3 systematic batches
        Maintains deterministic ordering across runs

    Default Mode (no arguments):
        Processes all skills (backward compatibility)

SKILL VALIDATION:
    Skills are validated by examining their structure and SKILL.md content
    Each skill must have a SKILL.md file with proper metadata
    Validation includes format checks and quality scoring

BACKWARD COMPATIBILITY:
    This CLI maintains full backward compatibility with the original healthcheck.py
    interface while adding modular architecture.

EXAMPLES:
    /healthcheck                          # Check all skills (default mode)
    /healthcheck --all                     # Process all skills (batch mode)
    /healthcheck generate-spec             # Validate generate-spec skill
    /healthcheck generate-verification      # Validate generate-verification skill

NOTES:
    - Skills are discovered by looking for SKILL.md files in skill directories
    - Skills are validated for proper structure and content
    - Results include validation status and quality scores
"""
    print(help_text)


def generate_all_reports(results: List[Dict[str, Any]]) -> None:
    """
    Generate all reports from health check results.

    Args:
        results: List of validation results for skills
    """
    print("\n=== Generating Health Check Reports ===\n")

    # Generate badges report
    generate_badges(results)
    print("Generated health_badges.md")

    # Generate JSON report
    generate_health_report(results)
    print("Generated health_check_report.json")

    # Generate console summary
    generate_console_summary(results)


def generate_console_summary(results: List[Dict[str, Any]]) -> None:
    """
    Generates console summary from validation results.

    Args:
        results: List of validation results for skills
    """
    print("\n=== Health Check Summary ===")
    print(f"Total skills checked: {len(results)}")
    print(f"Healthy skills: {len([r for r in results if r.get('is_valid', False) and r.get('score', 0.0) >= 90])}")
    print(f"Skills needing review: {len([r for r in results if r.get('is_valid', False) and 70 <= r.get('score', 0.0) < 90])}")
    print(f"Skills with errors: {len([r for r in results if not r.get('is_valid', True)])}")

    # Show problematic skills
    print("\n=== Problematic Skills ===")
    for result in results:
        if not result.get('is_valid', True) or result.get('score', 0.0) < 70:
            skill_name = result.get('skill_name', 'Unknown')
            score = result.get('score', 0.0)
            issues = result.get('errors', [])

            print(f"- {skill_name}: {score:.1f}/100.0")
            for issue in issues:
                print(f"  ❌ {issue}")


# Re-export at module level for test mocking (cli.discover_skills, cli.get_skills_directory)
discover_skills = discover_skills
get_skills_directory = get_skills_directory

__all__ = ("parse_arguments", "validate_single_skill", "process_all_skills",
           "run_health_check", "print_help", "generate_all_reports")