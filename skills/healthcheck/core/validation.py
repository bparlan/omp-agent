#!/usr/bin/env python3
"""
Core validation logic for AEF-OMP Skill Health Checker.
Pure validation functionality with Validator base classes and validation orchestrators.
Separated from I/O operations for better testability and maintainability.
"""

import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any
@dataclass
class ValidationResult:
    """Model for validation results"""
    name: str
    status: str  # "healthy", "needs_review", "error"
    validation_score: float
    has_stable_suffix: bool
    issues: List[str]
    last_modified: str
    last_checked: str
class Validator:
    """Base validator class for skill validation rules"""

    def validate(self, content: str, skill_path: Path) -> ValidationResult:
        """Validate skill content - to be implemented by subclasses"""
        raise NotImplementedError
class RequiredFieldsValidator(Validator):
    """Validates required fields in SKILL.md file"""

    def __init__(self):
        self.required_fields = [
            ("name:", "name field"),
            ("version:", "version field"),
            ("description:", "description field"),
            ("tools:", "tools field"),
            ("userInvocable:", "userInvocable field"),
        ]

    def validate(self, content: str, skill_path: Path) -> ValidationResult:
        """Validate required fields presence"""
        issues = []
        validation_score = 0.0
        total_checks = len(self.required_fields)

        content_lower = content.lower()

        for field, field_name in self.required_fields:
            field_lower = field.lower()
            if field_lower in content_lower:
                validation_score += 1.0
            else:
                issues.append(f"Missing {field_name}")

        validation_score = validation_score / total_checks if total_checks > 0 else 0.0

        return ValidationResult(
            name="",
            status="",
            validation_score=validation_score,
            has_stable_suffix="-stable" in content.lower(),
            issues=issues,
            last_modified="",
            last_checked=""
        )
class VersionValidator(Validator):
    """Validates version information and -stable suffix"""

    def validate(self, content: str, skill_path: Path) -> ValidationResult:
        """Validate version and stable suffix"""
        # Extract version using regex
        version_match = re.search(r'version:\s*([^\n]+)', content, re.IGNORECASE)
        version = version_match.group(1) if version_match else None

        # Check for -stable suffix in version field
        has_stable_suffix = "-stable" in content.lower()

        return ValidationResult(
            name="",
            status="",
            validation_score=0.0,
            has_stable_suffix=has_stable_suffix,
            issues=[],
            last_modified="",
            last_checked=""
        )
class NameValidator(Validator):
    """Validates skill name extraction"""

    def validate(self, content: str, skill_path: Path) -> ValidationResult:
        """Extract and validate skill name"""
        name_match = re.search(r'name:\s*([^\n]+)', content, re.IGNORECASE)
        skill_name = name_match.group(1).strip() if name_match else skill_path.parent.name

        return ValidationResult(
            name=skill_name,
            status="",
            validation_score=0.0,
            has_stable_suffix=False,
            issues=[],
            last_modified="",
            last_checked=""
        )
class ValidationOrchestrator:
    """Orchestrates validation using multiple validators"""

    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
            VersionValidator(),
            NameValidator(),
        ]

    def validate_skill(self, content: str, skill_path: Path) -> ValidationResult:
        """Run all validators and combine results"""
        # Base result with skill info
        result = ValidationResult(
            name="",
            status="",
            validation_score=0.0,
            has_stable_suffix=False,
            issues=[],
            last_modified="",
            last_checked=""
        )

        # Run all validators
        for validator in self.validators:
            try:
                validation_result = validator.validate(content, skill_path)

                # Merge results
                if hasattr(validation_result, 'validation_score'):
                    result.validation_score = validation_result.validation_score
                    result.issues = validation_result.issues
                    result.has_stable_suffix = validation_result.has_stable_suffix
                elif hasattr(validation_result, 'has_stable_suffix'):
                    result.has_stable_suffix = validation_result.has_stable_suffix
                elif hasattr(validation_result, 'skill_name'):
                    result.name = validation_result.skill_name

            except Exception as e:
                # If any validator fails, mark as error
                result.status = "error"
                result.issues.append(f"Validation error: {str(e)}")
                break

        # Determine status based on score
        if result.status != "error":
            result.status = "healthy" if result.validation_score >= 0.8 else "needs_review"

        return result
def validate_skill_file(skill_path: Path) -> dict:
    """
    Legacy function for backward compatibility.
    This function provides the original interface for healthcheck.py
    while internally using the new modular validation system.
    """
    orchestrator = ValidationOrchestrator()

    try:
        content = skill_path.read_text()

        # Use the orchestrator to get validation results
        result = orchestrator.validate_skill(content, skill_path)

        # Format result to match original healthcheck.py output format
        return {
            "name": result.name,
            "status": result.status,
            "validation_score": result.validation_score,
            "has_stable_suffix": result.has_stable_suffix,
            "issues": result.issues,
            "last_modified": result.last_modified,
            "last_checked": result.last_checked,
        }

    except Exception as e:
        return {
            "name": skill_path.parent.name,
            "status": "error",
            "validation_score": 0.0,
            "has_stable_suffix": False,
            "issues": [f"Error reading file: {str(e)}"],
            "last_modified": datetime.now().isoformat(),
            "last_checked": datetime.now().isoformat(),
        }