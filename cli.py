#!/usr/bin/env python3
"""
cli.py - M8S4 CLI Module

Provides the command-line interface for the HealthCheck Skill modular architecture.
Implements six public functions as specified in M8S4 requirements:
- parse_arguments(): Argument parsing using argparse
- validate_single_skill(skill_name): Single skill validation
- process_all_skills(): Batch processing in 3 batches
- run_health_check(skill_name=None, all_flag=False): Mode dispatch
- print_help(): Help text display
- generate_all_reports(results): Report generation orchestration

Key constraints:
- Module independence: imports only from core.validation, discovery, reporting, stdlib
- No module-level mutable global state
- All functions have type hints
- Backward compatibility with existing healthcheck.py interface
"""

import argparse
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path

# Module-level imports - strictly controlled by NFR-CLI_FILE_SCOPE
import discovery
from skills.healthcheck.core.validation import SkillValidator
import reporting
from discovery import discover_skills as _discover_skills
from discovery import get_skills_directory as _get_skills_directory

# Re-export at module level for test mocking (cli.discover_skills, cli.get_skills_directory)
discover_skills = _discover_skills
get_skills_directory = _get_skills_directory

__all__ = (
    "parse_arguments",
    "validate_single_skill",
    "process_all_skills",
    "run_health_check",
    "print_help",
    "generate_all_reports",
)
def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace with skill_name, all_flag, help_flag attributes.

    Implementation details:
    - Uses argparse.ArgumentParser with positional skill_name (optional)
    - --all flag stores to all_flag (store_true)
    - --help flag stores to help_flag (store_true)
    - Maintains backward compatibility with existing CLI interface
    """
    parser = argparse.ArgumentParser(
        description="HealthCheck Skill CLI",
        add_help=False
    )
    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Specific skill name to check"
    )
    parser.add_argument(
        "--all",
        dest="all_flag",
        action="store_true",
        help="Process all skills in 3 batches"
    )
    parser.add_argument(
        "--help",
        dest="help_flag",
        action="store_true",
        help="Show help text"
    )

    return parser.parse_args()
def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """
    Validates a single skill by name.

    Args:
        skill_name: Name of the skill directory (without .md extension).

    Returns:
        Dict result matching SkillValidator.validate() output schema, or None if skill not found.

    Process:
    1. Uses discovery.get_skills_directory() to find skills directory
    2. Uses discover_skills() to check if skill exists (mockable for tests)
    3. Reads file content and validates via SkillValidator().validate()
    4. Prints status line to stdout
    5. Returns result dict or None with stderr error if not found
    """
    try:
        # Get skills directory path
        skills_dir = get_skills_directory()

        # Check if skill exists using discover_skills (mockable via cli.discover_skills)
        available_skills = discover_skills(skills_dir)
        if skill_name not in available_skills:
            print(f"Skill '{skill_name}' not found", file=sys.stderr)
            return None

        # Construct path to skill file
        skill_file = skills_dir / skill_name / "SKILL.md"

        with open(skill_file) as f:
            content = f.read()

        print(f"Checking {skill_name}...", end=" ")
        result = SkillValidator().validate(content)
        result["name"] = skill_name

        print(f"{result['status']} (score: {result['score']:.2f})")

        return result

    except KeyboardInterrupt:
        print(f"\nValidation interrupted for skill '{skill_name}'.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error validating skill '{skill_name}': {e}", file=sys.stderr)
        return None
def process_all_skills() -> List[Dict[str, Any]]:
    """
    Process all skills in 3 batches.

    Process:
    1. Get skills directory
    2. Split skills into 3 equal batches
    3. Process each batch
    4. Return all results
    """
    try:
        # Get skills directory path
        skills_dir = get_skills_directory()

        # Get all available skills
        all_skills = discover_skills(skills_dir)

        if not all_skills:
            return []

        # Split into 3 batches
        batch_size = (len(all_skills) + 2) // 3  # Ceiling division
        batch1 = all_skills[:batch_size]
        batch2 = all_skills[batch_size : 2 * batch_size]
        batch3 = all_skills[2 * batch_size :]

        # Process each batch
        results = []

        for batch_name, batch_skills in [("Batch 1", batch1), ("Batch 2", batch2), ("Batch 3", batch3)]:
            for skill_name in batch_skills:
                result = validate_single_skill(skill_name)
                if result:
                    result["batch"] = batch_name
                    results.append(result)

        return results

    except Exception as e:
        print(f"Error processing all skills: {e}", file=sys.stderr)
        return []
def run_health_check(skill_name: Optional[str] = None, all_flag: bool = False) -> List[Dict[str, Any]]:
    """
    Mode dispatch for health check operations.

    Args:
        skill_name: Optional skill name for single-skill mode.
        all_flag: Process all skills in 3 batches.

    Returns:
        List of result dicts.

    Process:
    1. skill_name provided: Single-skill mode → validate_single_skill()
    2. all_flag set: Process all skills → process_all_skills()
    3. No skill_name and no all_flag: Process all skills → process_all_skills()
    """
    results = []

    try:
        if skill_name:
            # Single-skill mode
            result = validate_single_skill(skill_name)
            if result:
                results.append(result)
        elif all_flag:
            # Process all skills
            results = process_all_skills()
        else:
            # Default: Process all skills (backward compatibility)
            results = process_all_skills()

        return results

    except Exception as e:
        print(f"Error in run_health_check: {e}", file=sys.stderr)
        return []
def print_help() -> None:
    """
    Show help text.

    Displays comprehensive help information including:
    - Available commands and options
    - Skill validation capabilities
    - Batch processing modes
    - Backward compatibility notes
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
    Report generation orchestration.

    Args:
        results: List of result dicts from health check operations.

    Process:
    1. Generates health report with skill statuses
    2. Generates badges for quick status overview
    3. Generates skills summary with statistics
    4. Prints reports to stdout
    5. Handles errors gracefully
    """
    try:
        # Generate health report
        health_report = reporting.generate_health_report(results)
        print(health_report)

        # Generate badges
        badges = reporting.generate_badges(results)
        print(badges)

        # Generate skills summary
        skills_summary = reporting.generate_skills_summary(results)
        print(skills_summary)

    except Exception as e:
        print(f"Error generating reports: {e}", file=sys.stderr)