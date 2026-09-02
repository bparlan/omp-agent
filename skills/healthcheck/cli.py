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

# Import SkillValidator from core validation module (for root CLI compatibility)
from skills.healthcheck.core.validation import SkillValidator

# Import other healthcheck modules
from .core.validation import validate_skill_file
from .discovery import discover_skills
from .reporting import generate_badges, generate_health_report


def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments.
    
    Returns:
        argparse.Namespace with skill_name, all_flag, help_flag attributes.
    """
    parser = argparse.ArgumentParser(
        description="Skill Health Checker - Validates skills for AEF-OMP compliance"
    )
    
    parser.add_argument(
        "skill_name", 
        nargs="?", 
        help="Name of skill to validate (optional, shows all skills if not specified)"
    )
    
    parser.add_argument(
        "--all", 
        "-a", 
        action="store_true", 
        help="Check all skills"
    )
    
    parser.add_argument(
        "--help", 
        "-h", 
        action="store_true", 
        help="Show help information"
    )
    
    return parser.parse_args()


def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """
    Validates a single skill.
    
    Args:
        skill_name: Name of skill to validate
        
    Returns:
        Dict containing validation results, or None if skill not found
    """
    skills_dir = Path("skills")
    skill_path = skills_dir / skill_name
    
    if not skill_path.exists() or not skill_path.is_dir():
        return None
    
    try:
        # Use the skill validator to validate the skill file
        result = validate_skill_file(skill_path)
        return result
    except Exception as e:
        return {
            "skill_name": skill_name,
            "is_valid": False,
            "errors": [f"Validation error: {str(e)}"],
            "warnings": [],
            "score": 0.0,
        }


def process_all_skills() -> List[Dict[str, Any]]:
    """
    Processes all skills and returns validation results for each.
    
    Returns:
        List of dictionaries containing validation results for each skill
    """
    skills_dir = Path("skills")
    results = []
    
    # Discover skills using the discovery module
    skills = discover_skills()
    
    for skill_path in skills:
        try:
            # Use the skill validator to validate each skill
            result = validate_skill_file(skill_path)
            if result:  # Only add valid results
                results.append(result)
        except Exception as e:
            # Add error result if validation fails
            results.append({
                "skill_name": skill_path.name,
                "is_valid": False,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": [],
                "score": 0.0,
            })
    
    return results


def run_health_check(
    skill_name: Optional[str] = None, all_flag: bool = False
) -> List[Dict[str, Any]]:
    """
    Runs health check based on arguments.
    
    Args:
        skill_name: Name of specific skill to check (optional)
        all_flag: Whether to check all skills (optional)
        
    Returns:
        List of dictionaries containing validation results for checked skills
    """
    if all_flag:
        return process_all_skills()
    
    if skill_name:
        result = validate_single_skill(skill_name)
        return [result] if result else []
    
    return process_all_skills()


def print_help() -> None:
    """
    Prints help information.
    """
    help_text = """
=== Skill Health Checker Help ===

Usage:
    python healthcheck.py [skill_name] [--all] [--help]

Arguments:
    skill_name          Name of skill to validate (optional)
    --all, -a           Check all skills
    --help, -h          Show this help message

Description:
    Validates skills for AEF-OMP compliance, focusing on:
    - Milestone and specification agnosticism
    - Code quality and structure
    - Adherence to architectural patterns
    - Required skill metadata (SKILL.md)
    - Version stability (-stable or -test suffix)

Examples:
    python healthcheck.py                    # Check all skills
    python healthcheck.py --all                # Check all skills
    python healthcheck.py my-skill             # Check specific skill
    python healthcheck.py --help               # Show help

Output:
    The tool generates reports in:
    - health_badges.md     : Visual status badges for each skill
    - health_check_report.json : Detailed JSON validation report
    
    Reports include validation scores, issues, and compliance status.
    
The healthcheck skill validates that skills:
1. Are milestone-agnostic (no hardcoded M1, M2, M3 references)
2. Are specification-agnostic (no hardcoded SPEC-M1S1 references)
3. Have proper SKILL.md metadata files
4. Follow AEF architectural patterns
5. Use proper versioning (-stable or -test suffix)
"""
    print(help_text)


def generate_all_reports(results: List[Dict[str, Any]]) -> None:
    """
    Generates all reports from health check results.
    
    Args:
        results: List of validation results for skills
    """
    if not results:
        print("No results to report")
        return
    
    print("\n=== Generating Health Check Reports ===\n")
    
    # Generate health_badges.md
    print("Generating health_badges.md...")
    with open("health_badges.md", "w") as f:
        f.write("# Skill Health Badges\n\n")
        for result in results:
            skill_name = result.get("skill_name", "Unknown")
            is_valid = result.get("is_valid", False)
            score = result.get("score", 0.0)
            issues = result.get("errors", [])
            
            status = "✅ HEALTHY" if is_valid and score >= 90 else "⚠️ NEEDS REVIEW" if is_valid else "❌ ERROR"
            
            f.write(f"## {skill_name}\n")
            f.write(f"- **Status**: {status}\n")
            f.write(f"- **Validation Score**: {score:.1f}/100.0\n")
            if issues:
                f.write(f"- **Issues**: {', '.join(issues[:3])}\n")
            f.write("\n")
    
    # Generate health_check_report.json
    print("Generating health_check_report.json...")
    import json
    from datetime import datetime
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_skills": len(results),
        "results": results,
        "summary": {
            "healthy": len([r for r in results if r.get("is_valid", False) and r.get("score", 0.0) >= 90]),
            "needs_review": len([r for r in results if r.get("is_valid", False) and 70 <= r.get("score", 0.0) < 90]),
            "errors": len([r for r in results if not r.get("is_valid", True)]),
        }
    }
    
    with open("health_check_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    # Print summary to console
    print("\n=== Health Check Summary ===")
    print(f"Total skills checked: {len(results)}")
    print(f"Healthy skills: {len([r for r in results if r.get('is_valid', False) and r.get('score', 0.0) >= 90])}")
    print(f"Skills needing review: {len([r for r in results if r.get('is_valid', False) and 70 <= r.get('score', 0.0) < 90])}")
    print(f"Skills with errors: {len([r for r in results if not r.get('is_valid', True)])}")
    
    # Show problematic skills
    print("\n=== Problematic Skills ===")
    for result in results:
        if not result.get("is_valid", True) or result.get("score", 0.0) < 70:
            skill_name = result.get("skill_name", "Unknown")
            score = result.get("score", 0.0)
            issues = result.get("errors", [])
            
            print(f"- {skill_name}: {score:.1f}/100.0")
            for issue in issues:
                print(f"  ❌ {issue}")


# Re-export at module level for test mocking (cli.discover_skills, cli.get_skills_directory)
discover_skills = discover_skills

__all__ = (
    "parse_arguments",
    "validate_single_skill",
    "process_all_skills",
    "run_health_check",
    "print_help",
    "generate_all_reports",
)