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
from typing import List, Dict, Any, Optional


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


class RequiredFieldsValidator(Validator):
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


class VersionValidator(Validator):
    """Validates version information and -stable suffix"""

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


class NameValidator(Validator):
    """Validates skill name extraction"""

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
    """Orchestrates validation using multiple validators"""

    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
            VersionValidator(),
            NameValidator(),
        ]
    
    def validate(self, content: str) -> Dict[str, Any]:
        """Runs all validators and combines results."""
        results = [validator.validate(content) for validator in self.validators]
        
        # Aggregate results
        all_errors = []
        all_warnings = []
        scores = []
        
        for result in results:
            all_errors.extend(result.get("errors", []))
            all_warnings.extend(result.get("warnings", []))
            scores.append(result.get("score", 0.0))
        
        # Calculate overall score (average of validator scores)
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        # Determine overall validation status
        is_valid = len(all_errors) == 0
        
        # Extract additional info from results
        extra_info = {}
        for result in results:
            extra_info.update({k: v for k, v in result.items() if k not in ["is_valid", "errors", "warnings", "score"]})
        
        return {
            "is_valid": is_valid,
            "errors": all_errors,
            "warnings": all_warnings,
            "score": overall_score,
            **extra_info,
        }


class SkillValidator:
    """Main skill validator that orchestrates all validation rules"""
    
    def __init__(self):
        self.orchestrator = ValidationOrchestrator()
    
    def validate(self, content: str) -> Dict[str, Any]:
        """Validates skill content using the validation orchestrator.
        
        Args:
            content: SKILL.md file content
            
        Returns:
            Dict containing validation results with keys:
            - is_valid: bool indicating if validation passed
            - errors: List[str] of error messages
            - warnings: List[str] of warning messages
            - score: float validation score (0.0-100.0)
            - name: str skill name (if found)
            - version: str skill version (if found)
            - has_stable_suffix: bool indicating if version has stable suffix
        """
        return self.orchestrator.validate(content)


def validate_skill_file(skill_path: Path) -> dict:
    """
    Validates a skill file by reading its content and running validation.
    
    Args:
        skill_path: Path to skill directory containing SKILL.md
        
    Returns:
        Dict containing validation results
    """
    try:
        skill_md_path = skill_path / "SKILL.md"
        if not skill_md_path.exists():
            return {
                "is_valid": False,
                "errors": ["SKILL.md file not found"],
                "warnings": [],
                "score": 0.0,
            }
        
        content = skill_md_path.read_text()
        validator = SkillValidator()
        return validator.validate(content)
        
    except Exception as e:
        return {
            "is_valid": False,
            "errors": [f"Error reading skill file: {str(e)}"],
            "warnings": [],
            "score": 0.0,
        }