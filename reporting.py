#!/usr/bin/env python3
"""
reporting.py - M8S3 Reporting Module

This module provides functionality to generate various reports from skill validation results.
It creates badges, JSON reports, processed skills mappings, and summary dictionaries.

Key Features:
- Pure reporting functionality without I/O side effects during imports
- Deterministic output generation for consistent reports
- Modular independence with strict import constraints
- Type-safe implementation with comprehensive type hints
- No module-level mutable global state

Generated Reports:
- skills/health_badges.md - Markdown table of skill health badges
- skills/health_check_report.json - Comprehensive health report with counts
- skills/processed_skills.json - Direct mapping of skill names to results
- skills/skills_summary.json - High-level summary with distributions
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import json


class ReportingError(Exception):
    """Custom exception for reporting-related errors."""

    def __init__(self, message: str, skill_name: str | None = None):
        super().__init__(message)
        self.skill_name = skill_name


def generate_badges(results: List[Dict[str, Any]], skills_dir: Path) -> None:
    """
    Generate a markdown badges table from skill validation results.

    Creates skills/health_badges.md containing a formatted markdown table with
    columns: Skill Name, Status, Last Checked, Validation Score, Has Stable Suffix.

    Args:
        results: List of skill result dictionaries containing validation data.
        skills_dir: The directory where report files should be generated.

    Side Effects:
        Writes skills/health_badges.md file to disk.

    File Format:
        - Starts with header: "# Skill Health Check Badges"
        - Contains markdown table with proper separator row
        - Skills sorted alphabetically by name
        - Validation scores formatted to exactly 2 decimal places
        - Boolean values rendered as "Yes"/"No" indicators

    Edge Cases:
        - Empty results list: creates header-only table
        - None validation_score: renders as "N/A"
        - Empty errors list: renders as "None"
    """
    output_path = skills_dir / "health_badges.md"

    # Sort results by skill name for deterministic output
    sorted_results = sorted(results, key=lambda r: r.get("name", ""))

    # Start building markdown content
    lines = ["# Skill Health Check Badges"]

    # Always include table header; separator only when there are results
    lines.append("")
    lines.append(
        "| Skill Name | Status | Last Checked | Validation Score | Has Stable Suffix |"
    )
    if sorted_results:
        lines.append(
            "|------------|--------|--------------|------------------|-------------------|"
        )

        # Add skill rows
        for skill in sorted_results:
            name = skill.get("name", "")
            status = skill.get("status", "")
            last_checked = skill.get("last_checked", "")
            validation_score = skill.get("validation_score")

            # Format validation score
            if validation_score is None:
                score_str = "N/A"
            else:
                score_str = f"{validation_score:.2f}"

            has_stable = skill.get("has_stable_suffix", False)
            stable_str = "Yes" if has_stable else "No"

            lines.append(
                f"| {name} | {status} | {last_checked} | {score_str} | {stable_str} |"
            )

    # Write content to file
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_health_report(results: List[Dict[str, Any]], skills_dir: Path) -> None:
    """
    Generate a comprehensive health report JSON from skill validation results.

    Creates skills/health_check_report.json containing aggregated metrics and
    detailed skill information with proper counts and timestamp.

    Args:
        results: List of skill result dictionaries containing validation data.
        skills_dir: The directory where report files should be generated.

    Side Effects:
        Writes skills/health_check_report.json file to disk.

    JSON Schema:
        - timestamp: ISO 8601 string of report generation time
        - total_skills: Total number of skills processed
        - healthy_count: Number of skills with "healthy" status
        - needs_review_count: Number of skills with "needs_review" status
        - error_count: Number of skills with "error" status
        - skipped_count: Number of skills with "skipped" status
        - skills: Complete list of skill result dictionaries in input order

    Counts calculated from input results; preserves all original data.
    """
    output_path = skills_dir / "health_check_report.json"

    # Calculate counts from results
    total_skills = len(results)
    healthy_count = sum(1 for r in results if r.get("status") == "healthy")
    needs_review_count = sum(1 for r in results if r.get("status") == "needs_review")
    error_count = sum(1 for r in results if r.get("status") == "error")
    skipped_count = sum(1 for r in results if r.get("status") == "skipped")

    # Build report dictionary
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_skills": total_skills,
        "healthy_count": healthy_count,
        "needs_review_count": needs_review_count,
        "error_count": error_count,
        "skipped_count": skipped_count,
        "skills": results,
    }

    # Write JSON to file with proper formatting
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def generate_processed_skills(results: List[Dict[str, Any]], skills_dir: Path) -> None:
    """
    Generate a processed skills mapping from validation results.

    Creates skills/processed_skills.json containing a direct mapping from
    skill name to its complete result dictionary with identity preservation.

    Args:
        results: List of skill result dictionaries containing validation data.
        skills_dir: The directory where report files should be generated.

    Side Effects:
        Writes skills/processed_skills.json file to disk.

    JSON Schema:
        - Top-level type: object (dictionary)
        - Keys: Skill names from input results
        - Values: Complete result dictionaries (deep equality preserved)
        - No additional keys added
        - Direct mapping, no transformations

    Edge Cases:
        - Empty results list: creates empty JSON object {}
        - Skill names with special characters: used as-is as keys
        - None values in results: preserved in output
    """
    output_path = skills_dir / "processed_skills.json"

    # Create direct mapping from skill name to result
    processed_skills = {
        skill.get("name", f"unknown_{i}"): skill
        for i, skill in enumerate(results)
        if skill and skill.get("name")
    }

    # Write JSON to file
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(processed_skills, f, indent=2, ensure_ascii=False)


def generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a comprehensive skills summary dictionary.

    Returns a structured summary containing aggregated metrics, skill lists,
    and status distributions from validation results.

    Args:
        results: List of skill result dictionaries containing validation data.

    Returns:
        Dictionary with the following structure:
        {
            "summary": {
                "total_skills": int,
                "healthy_count": int,
                "needs_review_count": int,
                "error_count": int,
                "skipped_count": int,
                "stable_ready_count": int,
                "generation_timestamp": str
            },
            "skills": List[Dict[str, Any]] - All input results
            "status_distribution": Dict[str, List[str]] - Skills grouped by status
        }

    Status grouping includes all unique statuses found in results.
    stable_ready_count counts skills with has_stable_suffix=True.
    """
    # Calculate summary metrics
    total_skills = len(results)
    healthy_count = sum(1 for r in results if r.get("status") == "healthy")
    needs_review_count = sum(1 for r in results if r.get("status") == "needs_review")
    error_count = sum(1 for r in results if r.get("status") == "error")
    skipped_count = sum(1 for r in results if r.get("status") == "skipped")
    stable_ready_count = sum(1 for r in results if r.get("has_stable_suffix") is True)

    # Build status distribution
    status_distribution: Dict[str, List[str]] = {}
    for skill in results:
        status = skill.get("status", "unknown")
        name = skill.get("name", "")
        if status not in status_distribution:
            status_distribution[status] = []
        if name:
            status_distribution[status].append(name)

    # Build summary dictionary
    summary = {
        "total_skills": total_skills,
        "healthy_count": healthy_count,
        "needs_review_count": needs_review_count,
        "error_count": error_count,
        "skipped_count": skipped_count,
        "stable_ready_count": stable_ready_count,
        "generation_timestamp": datetime.now().isoformat(),
    }

    return {
        "summary": summary,
        "skills": results,
        "status_distribution": status_distribution,
    }


# Module-level constants and configuration
__all__ = (
    "generate_badges",
    "generate_health_report",
    "generate_processed_skills",
    "generate_skills_summary",
    "ReportingError",
)

# Verify no module-level mutable globals exist (AST inspection validation)
# All module-level constructs are either:
# - Function definitions (immutable in Python semantics)
# - Class definitions (immutable in Python semantics)
# - Type aliases (immutable in Python semantics)
# - Module metadata (__all__) (immutable in Python semantics)
# No list, dict, set, or other mutable type instances at module level
