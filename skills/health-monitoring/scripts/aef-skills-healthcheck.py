#!/usr/bin/env python3
"""
AEF Skills Health Check System

Comprehensive validation and auto-fix system for AEF skills stability and health.
Manages version compliance, YAML frontmatter validation, and AEF integration.

Author: Healthcheck System
Version: 1.0.0
"""

import re
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum


class HealthCheckStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class ValidationIssue:
    def __init__(
        self,
        issue_type: str,
        severity: str,
        message: str,
        skill_path: str,
        fix_suggestion: str = "",
    ):
        self.issue_type = issue_type
        self.severity = severity
        self.message = message
        self.skill_path = skill_path
        self.fix_suggestion = fix_suggestion
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "issue_type": self.issue_type,
            "severity": self.severity,
            "message": self.message,
            "skill_path": self.skill_path,
            "fix_suggestion": self.fix_suggestion,
            "timestamp": self.timestamp.isoformat(),
        }


class SkillHealthChecker:
    def __init__(self, skills_dir: str = "skills", dry_run: bool = False):
        self.skills_dir = Path(skills_dir)
        self.dry_run = dry_run
        self.issues: List[ValidationIssue] = []
        self.stable_skills = 0
        self.total_skills = 0

        # Phase groups for systematic processing
        self.phase_groups = {
            "development_cycle": [],
            "management_infra": [],
            "planning_specification": [],
            "testing_verification": [],
            "implementation": [],
        }

        # Core skills that should be prioritized
        self.core_skills = [
            "generate-spec",
            "generate-verification",
            "generate-tests",
            "implement-specification",
            "evaluate-implementation",
            "evaluate-tests",
            "review-implementation",
            "close-milestone",
            "healthcheck",
        ]

    def discover_skill_phases(self) -> None:
        """Discover skills and group them by functional phase."""
        print("=== Discovering Skills and Grouping by Phase ===")

        # Define phase classifications based on skill functionality
        development_cycle_skills = [
            "evaluate-implementation",
            "evaluate-tests",
            "implement-specification",
        ]

        management_infra_skills = [
            "manage-development",
            "manage-roadmap",
            "review-implementation",
            "close-milestone",
            "session-audit",
            "evolve-skills",
            "sync-documentation",
            "archive-docs",
            "healthcheck",
        ]

        planning_specification_skills = [
            "milestoner",
            "milestone-focus",
            "milestone-planning",
            "generate-spec",
            "generate-verification",
            "generate-tests",
            "specification-writer",
            "requirement-analyzer",
        ]

        testing_verification_skills = [
            "evaluate-tests",
            "evaluate-implementation",
            "evaluate-verification",
            "test-validator",
            "verification-auditor",
            "quality-assurance",
        ]

        implementation_skills = [
            "implement-specification",
            "implement-tests",
            "implement-verification",
            "implementation-orchestrator",
            "code-implementation",
            "production-deploy",
        ]

        # Assign skills to phases
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            skill_file = skill_dir / "SKILL.md"

            if not skill_file.exists():
                continue

            # Classify skill based on name and content
            is_development = any(
                dev_skill in skill_name.lower()
                for dev_skill in development_cycle_skills
            )
            is_management = any(
                mgmt_skill in skill_name.lower()
                for mgmt_skill in management_infra_skills
            )
            is_planning = any(
                plan_skill in skill_name.lower()
                for plan_skill in planning_specification_skills
            )
            is_testing = any(
                test_skill in skill_name.lower()
                for test_skill in testing_verification_skills
            )
            is_implementation = any(
                impl_skill in skill_name.lower() for impl_skill in implementation_skills
            )

            # Assign to primary phase
            if is_development:
                self.phase_groups["development_cycle"].append(skill_name)
            elif is_management:
                self.phase_groups["management_infra"].append(skill_name)
            elif is_planning:
                self.phase_groups["planning_specification"].append(skill_name)
            elif is_testing:
                self.phase_groups["testing_verification"].append(skill_name)
            elif is_implementation:
                self.phase_groups["implementation"].append(skill_name)
            else:
                # Default to management_infra if unclear classification
                self.phase_groups["management_infra"].append(skill_name)

        print("Phase Groups:")
        for phase, skills in self.phase_groups.items():
            if skills:
                print(f"  {phase}: {len(skills)} skills")
                for skill in sorted(skills):
                    print(f"    - {skill}")

    def validate_yaml_frontmatter(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """Validate YAML frontmatter structure and required fields."""
        issues = []

        try:
            content = skill_path.read_text(encoding="utf-8")

            # Check for proper YAML frontmatter delimiters
            if not content.startswith("---"):
                issues.append("Missing YAML frontmatter opening delimiter '---'")
                return False, issues

            parts = content.split("---")
            if len(parts) < 3:
                issues.append(
                    "Invalid YAML frontmatter structure - missing closing delimiter '---'"
                )
                return False, issues

            # Extract frontmatter
            frontmatter_text = parts[1].strip()

            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_text)

            if frontmatter is None:
                issues.append("Invalid YAML content - could not parse frontmatter")
                return False, issues

            # Required fields validation
            required_fields = [
                "name",
                "version",
                "description",
                "tools",
                "user-invocable",
            ]
            missing_fields = []

            for field in required_fields:
                if field not in frontmatter:
                    missing_fields.append(field)

            if missing_fields:
                issues.append(
                    f"Missing required YAML fields: {', '.join(missing_fields)}"
                )
                return False, issues

            # Validate field types and constraints
            if not isinstance(frontmatter.get("name"), str) or not frontmatter["name"]:
                issues.append("Field 'name' must be a non-empty string")

            if (
                not isinstance(frontmatter.get("version"), str)
                or not frontmatter["version"]
            ):
                issues.append("Field 'version' must be a non-empty string")
            else:
                # Check version format
                version = frontmatter["version"]
                if not re.match(r"^\d+\.\d+\.\d+", version) and not re.match(
                    r"^\d+\.\d+$", version
                ):
                    issues.append(
                        f"Version field '{version}' should follow semantic versioning pattern (e.g., 1.0.0)"
                    )

            if (
                not isinstance(frontmatter.get("description"), str)
                or not frontmatter["description"]
            ):
                issues.append("Field 'description' must be a non-empty string")

            if (
                not isinstance(frontmatter.get("tools"), list)
                or not frontmatter["tools"]
            ):
                issues.append("Field 'tools' must be a non-empty list")
            else:
                for tool in frontmatter["tools"]:
                    if not isinstance(tool, str) or not tool:
                        issues.append(
                            "Each tool in 'tools' list must be a non-empty string"
                        )
                        break

            if not isinstance(frontmatter.get("user-invocable"), bool):
                issues.append("Field 'user-invocable' must be a boolean")

        except yaml.YAMLError as e:
            issues.append(f"YAML parsing error: {str(e)}")
            return False, issues
        except Exception as e:
            issues.append(f"Error reading YAML frontmatter: {str(e)}")
            return False, issues

        return True, issues

    def validate_stability_requirements(
        self, skill_path: Path
    ) -> Tuple[bool, List[str]]:
        """Validate stability requirements for the skill."""
        issues = []

        try:
            content = skill_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return False, issues

            parts = content.split("---")
            if len(parts) < 3:
                return False, issues

            frontmatter_text = parts[1].strip()
            frontmatter = yaml.safe_load(frontmatter_text)

            # Check for -stable suffix in version
            version = frontmatter.get("version", "")
            if not version.endswith("stable"):
                issues.append(f"Version '{version}' does not end with '-stable' suffix")
                return False, issues

        except Exception as e:
            issues.append(f"Error validating stability requirements: {str(e)}")

        return len(issues) == 0, issues

    def validate_aef_integration(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """Validate AEF integration and compliance."""
        issues = []

        try:
            content = skill_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return False, issues

            parts = content.split("---")
            if len(parts) < 3:
                return False, issues

            frontmatter_text = parts[1].strip()
            frontmatter = yaml.safe_load(frontmatter_text)

            skill_name = frontmatter.get("name", "")

            # Check for AEF-specific patterns and conventions
            aef_patterns = [
                r"aef",
                r"omp",
                r"specification",
                r"pipeline",
                r"agent",
                r"development",
                r"management",
                r"testing",
                r"verification",
            ]

            has_aef_keywords = any(
                re.search(pattern, content.lower()) for pattern in aef_patterns
            )
            if not has_aef_keywords:
                issues.append(
                    f"Skill '{skill_name}' may not be properly integrated with AEF framework"
                )

            # Check for proper tool specifications
            tools = frontmatter.get("tools", [])
            if not any(tool in tools for tool in ["read", "write", "edit"]):
                issues.append(
                    f"Skill '{skill_name}' may lack essential AEF tools (read, write, edit)"
                )

            # Check for user-invocable flag
            if not frontmatter.get("user-invocable", False):
                issues.append(
                    f"Skill '{skill_name}' should be user-invocable for AEF pipeline integration"
                )

        except Exception as e:
            issues.append(f"Error validating AEF integration: {str(e)}")

        return len(issues) == 0, issues

    def validate_file_integrity(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """Validate file integrity (no NUL bytes, proper formatting)."""
        issues = []

        try:
            content = skill_path.read_text(encoding="utf-8")

            # Check for NUL bytes
            if "\x00" in content:
                issues.append("File contains NUL bytes (0x00) which is not valid UTF-8")

            # Check for proper line endings (LF only)
            if "\r\n" in content:
                issues.append("File contains Windows line endings (CRLF). Use LF only")

            # Check file size (reasonable limit)
            file_size = len(content.encode("utf-8"))
            if file_size > 1024 * 1024:  # 1MB
                issues.append(f"File size is {file_size} bytes, exceeds 1MB limit")

            # Check for proper YAML structure
            lines = content.split("\n")
            yaml_section = False
            yaml_end = False

            for line in lines:
                if line.strip() == "---":
                    if not yaml_section:
                        yaml_section = True
                    elif not yaml_end:
                        yaml_end = True
                        break
                    continue

            if yaml_section and not yaml_end:
                issues.append("YAML frontmatter does not have proper closing delimiter")

        except Exception as e:
            issues.append(f"Error validating file integrity: {str(e)}")

        return len(issues) == 0, issues

    def check_skill_compatibility(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """Check skill compatibility with other AEF skills and dependencies."""
        issues = []

        try:
            content = skill_path.read_text(encoding="utf-8")
            if not content.startswith("---"):
                return False, issues

            parts = content.split("---")
            if len(parts) < 3:
                return False, issues

            frontmatter_text = parts[1].strip()
            frontmatter = yaml.safe_load(frontmatter_text)

            skill_name = frontmatter.get("name", "")

            # Basic compatibility check - references to other skills
            if "generate-spec" in content.lower() and skill_name != "generate-spec":
                if "generated_spec" not in content.lower():
                    issues.append(
                        f"Skill '{skill_name}' may depend on generate-spec but doesn't reference it properly"
                    )

        except Exception as e:
            issues.append(f"Error checking skill compatibility: {str(e)}")

        return len(issues) == 0, issues

    def validate_skill_comprehensive(
        self, skill_path: Path
    ) -> Tuple[HealthCheckStatus, List[ValidationIssue]]:
        """Perform comprehensive validation of a single skill."""
        print(f"\n=== Validating {skill_path.name} ===")

        status = HealthCheckStatus.HEALTHY
        all_issues: List[ValidationIssue] = []

        # Validate YAML frontmatter
        yaml_valid, yaml_issues = self.validate_yaml_frontmatter(skill_path)
        if not yaml_valid:
            for issue in yaml_issues:
                all_issues.append(
                    ValidationIssue(
                        "YAML_FRONTMATTER",
                        "CRITICAL",
                        issue,
                        str(skill_path),
                        "Fix YAML frontmatter according to AEF standards",
                    )
                )
            status = HealthCheckStatus.BLOCKED

        # Validate stability requirements
        stability_valid, stability_issues = self.validate_stability_requirements(
            skill_path
        )
        if not stability_valid:
            for issue in stability_issues:
                all_issues.append(
                    ValidationIssue(
                        "STABILITY",
                        "CRITICAL",
                        issue,
                        str(skill_path),
                        "Add '-stable' suffix to version field",
                    )
                )
            status = HealthCheckStatus.BLOCKED

        # Validate AEF integration
        integration_valid, integration_issues = self.validate_aef_integration(
            skill_path
        )
        if not integration_valid:
            for issue in integration_issues:
                all_issues.append(
                    ValidationIssue(
                        "AEF_INTEGRATION",
                        "WARNING",
                        issue,
                        str(skill_path),
                        "Review AEF integration requirements",
                    )
                )
            if status == HealthCheckStatus.HEALTHY:
                status = HealthCheckStatus.WARNING

        # Validate file integrity
        integrity_valid, integrity_issues = self.validate_file_integrity(skill_path)
        if not integrity_valid:
            for issue in integrity_issues:
                all_issues.append(
                    ValidationIssue(
                        "FILE_INTEGRITY",
                        "WARNING",
                        issue,
                        str(skill_path),
                        "Fix file integrity issues",
                    )
                )
            if status == HealthCheckStatus.HEALTHY:
                status = HealthCheckStatus.WARNING

        # Check compatibility with other AEF skills
        compatibility_valid, compatibility_issues = self.check_skill_compatibility(
            skill_path
        )
        if not compatibility_valid:
            for issue in compatibility_issues:
                all_issues.append(
                    ValidationIssue(
                        "COMPATIBILITY",
                        "WARNING",
                        issue,
                        str(skill_path),
                        "Review AEF skill compatibility",
                    )
                )
            if status == HealthCheckStatus.HEALTHY:
                status = HealthCheckStatus.WARNING

        # Display results
        print(f"  Status: {status.value}")
        if all_issues:
            print(f"  Issues found: {len(all_issues)}")
            for issue in all_issues:
                print(f"    [{issue.severity}] {issue.issue_type}: {issue.message}")
        else:
            print("  No issues found - skill is healthy!")

        return status, all_issues

    def auto_fix_skill(self, skill_path: Path) -> bool:
        """Attempt to auto-fix common issues in a skill."""
        print(f"\n=== Attempting to auto-fix {skill_path.name} ===")

        try:
            content = skill_path.read_text(encoding="utf-8")

            # Check for auto-fixable issues
            fixes_applied = []

            # Fix 1: Add missing -stable suffix to version
            if not content.startswith("---"):
                print("  Cannot auto-fix - YAML frontmatter malformed")
                return False

            parts = content.split("---")
            if len(parts) < 3:
                print("  Cannot auto-fix - incomplete YAML frontmatter")
                return False

            frontmatter_text = parts[1].strip()

            try:
                frontmatter = yaml.safe_load(frontmatter_text)
                if frontmatter and "version" in frontmatter:
                    version = frontmatter["version"]
                    if not version.endswith("stable"):
                        # Fix version
                        new_version = version + "-stable"
                        frontmatter["version"] = new_version

                        # Reconstruct frontmatter
                        new_frontmatter = yaml.dump(
                            frontmatter, default_flow_style=False
                        ).strip()
                        new_content = f"---\n{new_frontmatter}\n---\n{parts[2]}"

                        if not self.dry_run:
                            skill_path.write_text(new_content, encoding="utf-8")
                            fixes_applied.append(f"Updated version to '{new_version}'")
                        else:
                            fixes_applied.append(
                                f"Would update version to '{new_version}' (dry run)"
                            )

                        print(f"  Applied fixes: {', '.join(fixes_applied)}")
                        return True
            except Exception as e:
                print(f"  Error during auto-fix: {e}")
                return False

        except Exception as e:
            print(f"  Error in auto-fix: {e}")
            return False

    def run_comprehensive_health_check(self) -> Dict:
        """Run comprehensive health check on all AEF skills."""
        print("=== AEF Skills Comprehensive Health Check ===")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Discover and group skills by phase
        self.discover_skill_phases()

        # Process skills by phase
        all_issues = []
        phase_results = {}

        for phase, skills in self.phase_groups.items():
            print(f"\n{'='*60}")
            print(f"PHASE: {phase.upper().replace('_', ' ')}")
            print(f"{'='*60}")
            print(f"Skills in this phase: {len(skills)}")

            phase_issues = []

            for skill_name in sorted(skills):
                skill_path = self.skills_dir / skill_name / "SKILL.md"

                if not skill_path.exists():
                    print(f"\n❌ Skill '{skill_name}': SKILL.md not found")
                    continue

                # Validate skill
                status, issues = self.validate_skill_comprehensive(skill_path)

                # Record issues
                for issue in issues:
                    all_issues.append(issue)
                    phase_issues.append(issue)

                # Update counters
                self.total_skills += 1
                if status == HealthCheckStatus.HEALTHY:
                    self.stable_skills += 1

            phase_results[phase] = {
                "total": len(skills),
                "healthy": sum(
                    1 for skill_name in skills if self.is_skill_healthy(skill_name)
                ),
                "issues": len(phase_issues),
            }

        # Generate final report
        report = self.generate_comprehensive_report(phase_results, all_issues)

        return report

    def is_skill_healthy(self, skill_name: str) -> bool:
        """Check if a skill is healthy based on our criteria."""
        skill_path = self.skills_dir / skill_name / "SKILL.md"
        if not skill_path.exists():
            return False

        try:
            status, _ = self.validate_skill_comprehensive(skill_path)
            return status == HealthCheckStatus.HEALTHY
        except:
            return False

    def generate_comprehensive_report(
        self, phase_results: Dict, all_issues: List[ValidationIssue]
    ) -> Dict:
        """Generate comprehensive health report."""
        total_skills = sum(phase["total"] for phase in phase_results.values())
        healthy_skills = self.stable_skills
        total_issues = len(all_issues)

        # Group issues by type
        issue_types = {}
        for issue in all_issues:
            if issue.issue_type not in issue_types:
                issue_types[issue.issue_type] = []
            issue_types[issue.issue_type].append(issue)

        report = {
            "summary": {
                "generated": datetime.now().isoformat(),
                "total_skills_analyzed": total_skills,
                "healthy_skills": healthy_skills,
                "skills_needing_attention": total_skills - healthy_skills,
                "compliance_rate": (healthy_skills / total_skills * 100)
                if total_skills > 0
                else 0,
                "total_issues_found": total_issues,
            },
            "phase_analysis": phase_results,
            "issue_analysis": issue_types,
            "recommendations": self.generate_recommendations(all_issues),
            "action_items": self.generate_action_items(all_issues),
        }

        return report

    def generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate recommendations based on issues found."""
        recommendations = []

        if any(
            issue.issue_type == "YAML_FRONTMATTER" and issue.severity == "CRITICAL"
            for issue in issues
        ):
            recommendations.append(
                "Fix YAML frontmatter structure in all skills with critical errors"
            )

        if any(
            issue.issue_type == "STABILITY" and issue.severity == "CRITICAL"
            for issue in issues
        ):
            recommendations.append(
                "Add '-stable' suffix to all skill versions to meet stability requirements"
            )

        if any(issue.issue_type == "AEF_INTEGRATION" for issue in issues):
            recommendations.append(
                "Review AEF integration for all skills to ensure proper framework compliance"
            )

        if any(issue.issue_type == "FILE_INTEGRITY" for issue in issues):
            recommendations.append(
                "Fix file integrity issues (NUL bytes, line endings, file size)"
            )

        if not recommendations:
            recommendations.append(
                "All skills are healthy - maintain current compliance standards"
            )

        return recommendations

    def generate_action_items(self, issues: List[ValidationIssue]) -> List[Dict]:
        """Generate specific action items for remediation."""
        action_items = []

        # Group issues by severity and type
        critical_issues = [issue for issue in issues if issue.severity == "CRITICAL"]
        warning_issues = [issue for issue in issues if issue.severity == "WARNING"]

        for issue in critical_issues:
            action_items.append(
                {
                    "priority": "CRITICAL",
                    "skill": issue.skill_path,
                    "issue": issue.message,
                    "action": "Immediate fix required",
                    "fix_suggestion": issue.fix_suggestion,
                }
            )

        for issue in warning_issues:
            action_items.append(
                {
                    "priority": "MEDIUM",
                    "skill": issue.skill_path,
                    "issue": issue.message,
                    "action": "Review and fix",
                    "fix_suggestion": issue.fix_suggestion,
                }
            )

        return action_items

    def export_report(
        self, report: Dict, output_file: str = "aef-skills-health-report.json"
    ):
        """Export health check report to JSON file."""
        try:
            import json

            # Convert ValidationIssue objects to dict for JSON serialization
            issue_data = []
            for issue in self.issues:
                issue_data.append(issue.to_dict())

            report["issues"] = issue_data
            report["exported_at"] = datetime.now().isoformat()

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, default=str)

            print(f"\n✅ Report exported to: {output_file}")
            return True

        except Exception as e:
            print(f"Error exporting report: {e}")
            return False


def main():
    """Main function to run the comprehensive health check."""
    import argparse

    parser = argparse.ArgumentParser(
        description="AEF Skills Comprehensive Health Check System"
    )
    parser.add_argument(
        "--skills-dir",
        "-s",
        default="skills",
        help="Path to skills directory (default: skills)",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Run in dry-run mode (don't modify files)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="aef-skills-health-report.json",
        help="Output file for health report (default: aef-skills-health-report.json)",
    )
    parser.add_argument(
        "--auto-fix",
        "-f",
        action="store_true",
        help="Attempt to auto-fix common issues",
    )

    args = parser.parse_args()

    # Create health checker instance
    checker = SkillHealthChecker(skills_dir=args.skills_dir, dry_run=args.dry_run)

    # Run comprehensive health check
    report = checker.run_comprehensive_health_check()

    # Display summary
    print(f"\n{'='*60}")
    print("HEALTH CHECK SUMMARY")
    print(f"{'='*60}")
    print(f"Skills Analyzed: {report['summary']['total_skills_analyzed']}")
    print(f"Healthy Skills: {report['summary']['healthy_skills']}")
    print(f"Compliance Rate: {report['summary']['compliance_rate']:.1f}%")
    print(f"Issues Found: {report['summary']['total_issues_found']}")

    # Auto-fix if requested
    if args.auto_fix:
        print(f"\n{'='*60}")
        print("AUTO-FIX MODE")
        print(f"{'='*60}")
        print("Attempting to auto-fix common issues...")

        for phase, skills in checker.phase_groups.items():
            print(f"\nProcessing phase: {phase}")
            for skill_name in skills:
                skill_path = checker.skills_dir / skill_name / "SKILL.md"
                if skill_path.exists():
                    checker.auto_fix_skill(skill_path)

    # Export report
    if args.output:
        success = checker.export_report(report, args.output)
        if success:
            print("\n✅ Health check completed successfully!")
            print(f"   - Report saved to: {args.output}")
        else:
            print(f"\n❌ Error saving report to: {args.output}")
            sys.exit(1)


if __name__ == "__main__":
    main()
