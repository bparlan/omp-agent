"""
CLI interface for healthcheck skill.
Handles command-line argument parsing and user interaction orchestration.
"""

from dataclasses import asdict
from skills.healthcheck.core.validation import SkillValidator, ValidationOrchestrator
import argparse
import sys
from typing import List, Optional, Dict, Any
from dataclasses import asdict

from .discovery import get_skills_directory, discover_skills, discover_skill_by_name
from .reporting import (
    generate_badges,
    generate_health_report,
    generate_processed_skills,
    generate_skills_summary
)
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="AEF-OMP Skill Health Checker",
        usage="""healthcheck.py [skill_name] [--all] [--help]

EXAMPLES:
  healthcheck.py                    # Check all skills (default mode)
  healthcheck.py my_skill           # Check specific skill
  healthcheck.py --all              # Process all skills in 3 batches
        """
    )

    parser.add_argument(
        'skill_name',
        nargs='?',
        help='Specific skill name to check (optional)'
    )

    parser.add_argument(
        '--all',
        dest='all_flag',
        action='store_true',
        help='Process all skills in 3 batches'
    )

    return parser.parse_args()
def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """Validate a single skill by name"""
    orchestrator = ValidationOrchestrator()

    # Discover the skill file
    skill_file_path = discover_skill_by_name(skill_name)

    if not skill_file_path:
        print(f"Skill '{skill_name}' not found", file=sys.stderr)
        return None

    print(f"Checking {skill_name}...", end=" ")
    result = orchestrator.validate_skill_file(skill_file_path)
    print(f"{result.status} (score: {result.validation_score:.2f})")

    return asdict(result)

def process_all_skills() -> List[Dict[str, Any]]:
    """Process all skills in 3 batches"""
    print("Processing all skills in 3 batches...")

    skills = discover_skills()

    # Batch 1: Core skills (first 3)
    print("\n=== BATCH 1: CORE SKILLS ===")
    batch1_results = []
    orchestrator = ValidationOrchestrator()

    for skill_file in skills[:3]:
        print(f"Checking {skill_file.parent.name}...", end=" ")
        result = orchestrator.validate_skill_file(skill_file)
        print(f"{result.status} (score: {result.validation_score:.2f})")
        batch1_results.append(asdict(result))

    # Batch 2: Extension skills (next 3)
    print("\n=== BATCH 2: EXTENSION SKILLS ===")
    batch2_results = []
    for skill_file in skills[3:6]:
        print(f"Checking {skill_file.parent.name}...", end=" ")
        result = orchestrator.validate_skill_file(skill_file)
        print(f"{result.status} (score: {result.validation_score:.2f})")
        batch2_results.append(asdict(result))

    # Batch 3: Edge cases (remaining)
    print("\n=== BATCH 3: EDGE CASES ===")
    batch3_results = []
    for skill_file in skills[6:]:
        print(f"Checking {skill_file.parent.name}...", end=" ")
        result = orchestrator.validate_skill_file(skill_file)
        print(f"{result.status} (score: {result.validation_score:.2f})")
        batch3_results.append(asdict(result))

    all_results = batch1_results + batch2_results + batch3_results

    print(f"\n=== BATCH SUMMARY ===")
    print(f"Batch 1 (Core): {len(batch1_results)} skills processed")
    print(f"Batch 2 (Extensions): {len(batch2_results)} skills processed")
    print(f"Batch 3 (Edge Cases): {len(batch3_results)} skills processed")
    print(f"Total: {len(all_results)} skills processed")

    return all_results
def run_health_check(skill_name: Optional[str] = None, all_flag: bool = False) -> List[Dict[str, Any]]:
    """Run health check with modular architecture"""
    print("=== AEF-OMP Skill Health Checker ===\n")

    if skill_name:
        # Single skill mode
        result = validate_single_skill(skill_name)
        return [result] if result else []

    elif all_flag:
        # Batch processing mode
        return process_all_skills()

    else:
        # Default: process all skills
        skills = discover_skills()
        print(f"Found {len(skills)} skills to check\n")

        results = []
        validator = SkillValidator()

        for skill_file in skills:
            print(f"Checking {skill_file.parent.name}...", end=" ")
            result = validator.validate_skill_file(skill_file)
            print(f"{result['status']} (score: {result['validation_score']:.2f})")
            results.append(result)

        return results
def print_help() -> None:
    """Print help information"""
    help_text = """
AEF-OMP Skill Health Checker Help
================================

Usage:
  healthcheck.py [skill_name]           # Check specific skill
  healthcheck.py --all                 # Process all skills in 3 batches

Validates SKILL.md files for:
  - Required fields: name, version, description, tools, userInvocable
  - -stable suffix in version fields
  - Proper frontmatter formatting

Output Reports:
  - health_badges.md: Status badges
  - health_check_report.json: Detailed JSON report
  - processed_skills.json: Name-to-result mapping

Modular Architecture:
  - core/validation.py: Pure validation logic
  - discovery.py: Skill discovery mechanisms
  - reporting.py: Report generation
  - cli.py: CLI interface and orchestration
  - main.py: Entry point and workflow coordination
    """
    print(help_text)
def generate_all_reports(results: List[Dict[str, Any]]) -> None:
    """Generate all reports from validation results"""
    print("\n=== Health Check Reports ===")

    # Generate badges
    generate_badges(results)
    generate_health_report(results)
    generate_processed_skills(results)
    
    summary = generate_skills_summary(results)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total skills checked: {summary['summary']['total_skills']}")
    print(f"Healthy skills: {summary['summary']['healthy_count']}")
    print(f"Skills needing review: {summary['summary']['needs_review_count']}")
    print(f"Skills with errors: {summary['summary']['error_count']}")
    
    if summary['summary']['stable_ready_count'] > 0:
        print(f"\n=== SKILLS WITH STABLE SUFFIX ===")
        stable_skills = [r for r in results if r['status'] == 'healthy' and r['has_stable_suffix']]
        for skill in sorted([s['name'] for s in stable_skills]):
            print(f"  - {skill}")
            
    if summary['summary']['error_count'] > 0:
        print("\n=== SKILLS WITH ERRORS ===")
        for skill in summary['status_distribution']['error']:
            print(f"  - {skill['name']}")
            for issue in skill.get('issues', []):
                print(f"    [FAIL] {issue}")

    return None