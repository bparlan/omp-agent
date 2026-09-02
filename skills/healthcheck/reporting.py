#!/usr/bin/env python3
"""
Reporting module for AEF-OMP HealthCheck Skill.

Provides report generation functionality for skill health checks.
This module is separated from I/O operations for better testability and maintainability.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


# Import validation functions from discovery module
from .discovery import is_milestone_agnostic, is_spec_agnostic


def generate_badges(results: List[Dict[str, Any]]) -> None:
    """
    Generates health_badges.md file from validation results.
    
    Args:
        results: List of validation results for skills
    """
    badges_content = "# Skill Health Badges\n\n"
    
    for result in results:
        skill_name = result.get("skill_name", "Unknown")
        is_valid = result.get("is_valid", False)
        score = result.get("score", 0.0)
        issues = result.get("errors", [])
        
        status = "✅ HEALTHY" if is_valid and score >= 90 else "⚠️ NEEDS REVIEW" if is_valid else "❌ ERROR"
        
        badges_content += f"## {skill_name}\n"
        badges_content += f"- **Status**: {status}\n"
        badges_content += f"- **Validation Score**: {score:.1f}/100.0\n"
        if issues:
            badges_content += f"- **Issues**: {', '.join(issues[:3])}\n"
        badges_content += "\n"
    
    # Write badges to file
    with open("health_badges.md", "w") as f:
        f.write(badges_content)


def generate_health_report(results: List[Dict[str, Any]]) -> None:
    """
    Generates health_check_report.json file from validation results.
    
    Args:
        results: List of validation results for skills
    """
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
    
    # Write report to file
    with open("health_check_report.json", "w") as f:
        json.dump(report_data, f, indent=2)


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
        if not result.get("is_valid", True) or result.get("score", 0.0) < 70:
            skill_name = result.get("skill_name", "Unknown")
            score = result.get("score", 0.0)
            issues = result.get("errors", [])
            
            print(f"- {skill_name}: {score:.1f}/100.0")
            for issue in issues:
                print(f"  ❌ {issue}")


def generate_reports(results: List[Dict[str, Any]]) -> None:
    """
    Generates all reports from health check results.
    
    Args:
        results: List of validation results for skills
    """
    if not results:
        print("No results to report")
        return
    
    print("\n=== Generating Health Check Reports ===\n")
    
    # Generate badges report
    generate_badges(results)
    print("Generated health_badges.md")
    
    # Generate JSON report
    generate_health_report(results)
    print("Generated health_check_report.json")
    
    # Generate console summary
    generate_console_summary(results)


def validate_skill_files(skill_paths: List[Path]) -> List[Dict[str, Any]]:
    """
    Validates multiple skill files.
    
    Args:
        skill_paths: List of paths to skill directories
        
    Returns:
        List of validation results
    """
    results = []
    
    for skill_path in skill_paths:
        try:
            # Read SKILL.md file
            skill_md_path = skill_path / "SKILL.md"
            if not skill_md_path.exists():
                results.append({
                    "skill_name": skill_path.name,
                    "is_valid": False,
                    "errors": ["SKILL.md file not found"],
                    "warnings": [],
                    "score": 0.0,
                })
                continue
            
            content = skill_md_path.read_text()
            
            # Basic validation using imported functions
            is_milestone_agnostic = is_milestone_agnostic(skill_path)
            is_spec_agnostic = is_spec_agnostic(skill_path)
            
            # Calculate score
            score = 100.0
            issues = []
            
            if not is_milestone_agnostic:
                score -= 30.0
                issues.append("Not milestone agnostic")
            
            if not is_spec_agnostic:
                score -= 30.0
                issues.append("Not specification agnostic")
            
            # Check for version field
            version_match = re.search(r"^\s*version:\s*(.+?)$", content, re.MULTILINE | re.IGNORECASE)
            if version_match:
                version = version_match.group(1).strip('"\' ')
                if version.endswith('-stable') or version.endswith('-test'):
                    # Good, no penalty
                    pass
                else:
                    score -= 20.0
                    issues.append(f"Version '{version}' does not have -stable or -test suffix")
            else:
                score -= 20.0
                issues.append("No version field found")
            
            # Update last modified
            stat_result = skill_md_path.stat()
            last_modified = datetime.fromtimestamp(stat_result.st_mtime).isoformat()
            
            results.append({
                "skill_name": skill_path.name,
                "is_valid": len(issues) == 0,
                "errors": issues,
                "warnings": [],
                "score": max(0.0, score),
                "last_modified": last_modified,
                "last_checked": datetime.now().isoformat(),
                "milestone_agnostic": is_milestone_agnostic,
                "spec_agnostic": is_spec_agnostic,
            })
            
        except Exception as e:
            results.append({
                "skill_name": skill_path.name,
                "is_valid": False,
                "errors": [f"Error validating skill: {str(e)}"],
                "warnings": [],
                "score": 0.0,
            })
    
    return results