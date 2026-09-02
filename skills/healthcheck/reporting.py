"""
Reporting functionality for healthcheck.
Handles generation of all report formats: badges, JSON reports, and processed skills.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from discovery import get_skills_directory
def generate_badges(results: List[Dict[str, Any]]) -> None:
    """Generate health badges markdown file"""
    skills_dir = get_skills_directory()
    badges_file = skills_dir / "health_badges.md"

    content = f"""# Skill Health Check Badges

This file provides a quick overview of skill health status.
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Skill Health Summary

| Skill Name | Status | Last Checked | Validation Score | Has Stable Suffix |
|------------|--------|---------------|------------------|-------------------|
"""

    for result in sorted(results, key=lambda x: x['name']):
        status_emoji = {
            "healthy": "✅",
            "needs_review": "⚠️",
            "blocked": "❌",
            "error": "🔴",
            "skipped": "⏭️"
        }.get(result['status'], "❓")

        content += f"| {result['name']} | {status_emoji} {result['status']} | {result['last_checked']} | {result['validation_score']:.2f} | {'✅' if result['has_stable_suffix'] else '❌'} |\n"

    badges_file.write_text(content)
    print(f"Generated: {badges_file.name}")
    print(f"  Lines: {len(content.splitlines())}")
def generate_health_report(results: List[Dict[str, Any]]) -> None:
    """Generate health report JSON file"""
    health_report = {
        "timestamp": datetime.now().isoformat(),
        "total_skills": len(results),
        "healthy_count": len([r for r in results if r['status'] == 'healthy']),
        "needs_review_count": len([r for r in results if r['status'] == 'needs_review']),
        "error_count": len([r for r in results if r['status'] == 'error']),
        "skipped_count": len([r for r in results if r['status'] == 'skipped']),
        "skills": results,
    }

    skills_dir = get_skills_directory()
    health_report_file = skills_dir / "health_check_report.json"
    with open(health_report_file, 'w') as f:
        json.dump(health_report, f, indent=2)

    print(f"Generated: {health_report_file.name}")
    print(f"  Skills: {health_report['healthy_count']} healthy, {health_report['needs_review_count']} needs review, {health_report['error_count']} errors")
def generate_processed_skills(results: List[Dict[str, Any]]) -> None:
    """Generate processed skills JSON file"""
    processed_skills = {result['name']: result for result in results}

    skills_dir = get_skills_directory()
    processed_file = skills_dir / "processed_skills.json"
    with open(processed_file, 'w') as f:
        json.dump(processed_skills, f, indent=2)

    print(f"Generated: {processed_file.name}")
    print(f"  Skills: {len(processed_skills)}")
def generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate comprehensive skills summary"""
    return {
        "summary": {
            "total_skills": len(results),
            "healthy_count": len([r for r in results if r['status'] == 'healthy']),
            "needs_review_count": len([r for r in results if r['status'] == 'needs_review']),
            "error_count": len([r for r in results if r['status'] == 'error']),
            "skipped_count": len([r for r in results if r['status'] == 'skipped']),
            "stable_ready_count": len([r for r in results if r['status'] == 'healthy' and r['has_stable_suffix']]),
            "generation_timestamp": datetime.now().isoformat(),
        },
        "skills": results,
        "status_distribution": {
            "healthy": [r for r in results if r['status'] == 'healthy'],
            "needs_review": [r for r in results if r['status'] == 'needs_review'],
            "error": [r for r in results if r['status'] == 'error'],
            "skipped": [r for r in results if r['status'] == 'skipped']
        }
    }