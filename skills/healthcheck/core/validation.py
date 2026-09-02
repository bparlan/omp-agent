#!/usr/bin/env python3
"""
Core validation logic for AEF-OMP HealthCheck Skill.

Pure validation functionality with Validator base classes and validation orchestrators.
Separated from I/O operations for better testability and maintainability.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ValidationResult:
    """Model for skill validation results"""

    name: str
    status: str  # "healthy", "needs_review", "error"
    validation_score: float  # 0.0-1.0, percentage of passed checks
    has_stable_suffix: bool  # True if version contains "-stable"
    issues: List[str]  # List of validation issues found
    last_modified: str  # ISO timestamp of last file modification
    last_checked: str  # ISO timestamp of validation check


class ValidatorBase:
    """Abstract base class for skill validation rules"""

    def validate(self, content: str) -> Dict[str, Any]:
        """Validates content based on specific rules.

        Args:
            content: String content to validate

        Returns:
            Dict containing validation results with keys:
            - is_valid: bool indicating if validation passed
            - errors: List[str] of error messages
            - warnings: List[str] of warning messages
            - score: float validation score (0.0-100.0)
        """
        raise NotImplementedError


class RequiredFieldsValidator(ValidatorBase):
    """Validates required fields in SKILL.md file"""

    def validate(self, content: str) -> Dict[str, Any]:
        required_fields = ["name", "description", "version", "userInvocable"]
        errors = []
        warnings = []

        # Check each required field
        for field in required_fields:
            # Check for different field formats
            field_pattern = rf"^\s*{field}:\s*(.+?)$"
            if not re.search(field_pattern, content, re.MULTILINE | re.IGNORECASE):
                errors.append(f"Missing required field: {field}")

        score = max(0.0, 100.0 - len(errors) * 25.0)

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "score": score,
        }


class StableSuffixValidator(ValidatorBase):
    """Validates -stable suffix in version field"""

    def validate(self, content: str) -> Dict[str, Any]:
        version_pattern = r"^\s*version:\s*(.+?)$"
        version_match = re.search(version_pattern, content, re.MULTILINE | re.IGNORECASE)

        if not version_match:
            return {
                "is_valid": False,
                "errors": ["Version field not found"],
                "warnings": [],
                "score": 0.0,
            }

        version = version_match.group(1).strip('"\' ')
        has_stable_suffix = version.endswith('-stable') or version.endswith('-test')

        errors = []
        if not has_stable_suffix:
            errors.append(f"Version '{version}' does not have -stable or -test suffix")

        score = 100.0 if has_stable_suffix else 50.0

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": [],
            "score": score,
            "has_stable_suffix": has_stable_suffix,
            "version": version,
        }


class SkillNameValidator(ValidatorBase):
    """Extracts and validates skill name from frontmatter"""

    def validate(self, content: str) -> Dict[str, Any]:
        name_pattern = r"^\s*name:\s*(.+?)$"
        name_match = re.search(name_pattern, content, re.MULTILINE | re.IGNORECASE)

        if not name_match:
            return {
                "is_valid": False,
                "errors": ["Name field not found"],
                "warnings": [],
                "score": 0.0,
            }

        name = name_match.group(1).strip('"\' ')

        # Basic name validation
        if len(name) < 2:
            return {
                "is_valid": False,
                "errors": ["Name is too short"],
                "warnings": [],
                "score": 0.0,
            }

        return {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "score": 100.0,
            "name": name,
        }


class ValidationOrchestrator:
    """Orchestrates multiple validators to produce final validation results"""

    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
            StableSuffixValidator(),
            SkillNameValidator()
        ]

    def validate_skill_file(self, skill_path: Path) -> ValidationResult:
        """MAIN VALIDATION INTERFACE - PURE FUNCTION"""
        """Orchestrates validation of a single skill file"""
        try:
            skill_file = skill_path / "SKILL.md"
            if not skill_file.exists():
                return ValidationResult(
                    name="Unknown",
                    status="error",
                    validation_score=0.0,
                    has_stable_suffix=False,
                    issues=["SKILL.md not found"],
                    last_modified=datetime.now().isoformat(),
                    last_checked=datetime.now().isoformat(),
                )

            content = skill_file.read_text()

            # Extract skill name
            name_pattern = r"^\s*name:\s*(.+?)$"
            name_match = re.search(name_pattern, content, re.MULTILINE | re.IGNORECASE)
            name = name_match.group(1).strip('"\' ') if name_match else "Unknown"

            # Extract version
            version_pattern = r"^\s*version:\s*(.+?)$"
            version_match = re.search(version_pattern, content, re.MULTILINE | re.IGNORECASE)
            version = version_match.group(1).strip('"\' ') if version_match else ""

            has_stable_suffix = version.endswith('-stable') or version.endswith('-test')

            # Run validators
            field_result = RequiredFieldsValidator().validate(content)
            version_result = StableSuffixValidator().validate(content)
            name_result = SkillNameValidator().validate(content)

            # Combine results
            all_errors = field_result["errors"] + version_result["errors"] + name_result["errors"]
            all_warnings = field_result["warnings"] + version_result["warnings"] + name_result["warnings"]
            total_score = (field_result["score"] + version_result["score"] + name_result["score"]) / 3.0

            # Determine status
            if len(all_errors) > 0:
                status = "error"
            elif total_score >= 100.0:
                status = "healthy"
            else:
                status = "needs_review"

            return ValidationResult(
                name=name,
                status=status,
                validation_score=total_score,
                has_stable_suffix=has_stable_suffix,
                issues=all_errors + all_warnings,
                last_modified=datetime.fromtimestamp(skill_file.stat().st_mtime).isoformat(),
                last_checked=datetime.now().isoformat(),
            )

        except Exception as e:
            return ValidationResult(
                name="Unknown",
                status="error",
                validation_score=0.0,
                has_stable_suffix=False,
                issues=[f"Error validating skill: {str(e)}"],
                last_modified=datetime.now().isoformat(),
                last_checked=datetime.now().isoformat(),
            )

    def combine_validators_for_testing(self) -> List[ValidatorBase]:
        """Returns validators list for testing - PUBLIC API"""
        return self.validators


class SkillValidator:
    """Main skill validator that orchestrates all validation rules"""

    def __init__(self):
        self.orchestrator = ValidationOrchestrator()

    def validate(self, content: str) -> Dict[str, Any]:
        """Validates skill content using the validation orchestrator."""
        # Run individual validators
        field_result = RequiredFieldsValidator().validate(content)
        version_result = StableSuffixValidator().validate(content)
        name_result = SkillNameValidator().validate(content)

        # Combine results
        all_errors = field_result["errors"] + version_result["errors"] + name_result["errors"]
        all_warnings = field_result["warnings"] + version_result["warnings"] + name_result["warnings"]
        total_score = (field_result["score"] + version_result["score"] + name_result["score"]) / 3.0

        # Determine status
        if len(all_errors) > 0:
            status = "error"
        elif total_score >= 100.0:
            status = "healthy"
        else:
            status = "needs_review"

        # Extract values
        name = name_result.get("name", "Unknown")
        version = version_result.get("version", "")
        has_stable_suffix = version_result.get("has_stable_suffix", False)

        return {
            "is_valid": len(all_errors) == 0,
            "errors": all_errors,
            "warnings": all_warnings,
            "score": total_score,
            "status": status,
            "name": name,
            "has_stable_suffix": has_stable_suffix,
            "last_modified": datetime.now().isoformat(),
            "last_checked": datetime.now().isoformat(),
        }


def validate_skill_file(skill_path: Path) -> dict:
    """
    Validates a skill file by reading its content and running validation.

    Args:
        skill_path: Path to skill directory containing SKILL.md

    Returns:
        Dict containing validation results
    """
    try:
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            return {
                "is_valid": False,
                "errors": ["SKILL.md not found"],
                "warnings": [],
                "score": 0.0,
                "status": "error",
                "name": "Unknown",
            }

        content = skill_file.read_text()

        # Extract basic info from content
        name_match = re.search(r"^\s*name:\s*(.+?)$", content, re.MULTILINE | re.IGNORECASE)
        version_match = re.search(r"^\s*version:\s*(.+?)$", content, re.MULTILINE | re.IGNORECASE)

        # Use SkillValidator to validate
        validator = SkillValidator()
        result = validator.validate(content)

        # Add timestamp information
        result["last_modified"] = datetime.fromtimestamp(skill_file.stat().st_mtime).isoformat()
        result["last_checked"] = datetime.now().isoformat()

        return result

    except Exception as e:
        return {
            "is_valid": False,
            "errors": [f"Error validating skill: {str(e)}"],
            "warnings": [],
            "score": 0.0,
            "status": "error",
            "name": "Unknown",
        }