#!/usr/bin/env python3
"""Artifact validation module - FR-ARTIFACT_VALIDATION

Validates artifact metadata against canonical contract.
Implements contract: validate_metadata(artifact_path, schema?)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import yaml
from pathlib import Path
import re
from core.artifacts.metadata import extract_frontmatter
from core.artifacts.artifact_types import get_all_type_definitions


@dataclass
class ValidationResult:
    """M9S1 canonical artifact validation result."""

    valid: bool = True
    errors: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)



class Validator:
    """Abstract base class for skill validation rules (M8S1 FR-VALIDATOR_BASE_CLASS)."""

    def validate(self, content: str) -> Dict[str, Any]:
        raise NotImplementedError




def _required_artifact_keys() -> List[str]:
    """Return required artifact metadata keys per canonical contract."""
    return [
        "id",
        "type",
        "title",
        "milestone_id",
        "status",
        "derived_from",
        "template_version",
        "metadata",
    ]


def _required_metadata_keys() -> List[str]:
    """Return required metadata sub-keys."""
    return ["created_at", "updated_at", "artifact_identity", "artifact_type"]


class RequiredFieldsValidator(Validator):
    """Validates required fields in SKILL.md file"""

    def validate(self, content: str) -> Dict[str, Any]:
        """Validate required fields presence"""
        result: Dict[str, Any] = {
            "score": 0.0,
            "status": "unknown",
            "fields_checked": [],
            "field_results": {},
            "errors": [],
            "stable_suffix_detected": False,
        }

        try:
            # Parse YAML frontmatter
            parsed = self._parse_frontmatter(content)
            if parsed is None:
                result["errors"].append("Invalid or missing YAML frontmatter")
                return result

            # Validate required fields
            result["fields_checked"], field_results = self._validate_fields(parsed)
            result["field_results"] = field_results

            # Calculate score
            result["score"] = self._calculate_score(field_results)

            # Determine status
            result["status"] = self._determine_status(result["score"], result["errors"])

            # Check for stable suffix
            result["stable_suffix_detected"] = self._check_stable_suffix(content)

        except Exception as e:
            result["errors"].append(f"Validation error: {str(e)}")

        return result

    def _parse_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse YAML frontmatter from skill content."""
        # Simple frontmatter detection: YAML block between --- delimiters
        if not content or not isinstance(content, str):
            return None

        lines = content.split("\n")
        if len(lines) < 2 or lines[0].strip() != "---":
            return None

        try:
            end_idx = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    end_idx = i
                    break

            if end_idx is None:
                return None

            frontmatter_text = "\n".join(lines[1:end_idx])
            return yaml.safe_load(frontmatter_text) or {}

        except Exception:
            return None

    def _validate_fields(
        self, frontmatter: Dict[str, Any]
    ) -> tuple[List[str], Dict[str, Any]]:
        """Validate skill frontmatter fields and return results."""
        fields_checked = []
        field_results = {}

        # Check required fields for skill artifacts
        required_fields = ["id", "title", "type", "status"]

        for field in required_fields:
            fields_checked.append(field)
            if field in frontmatter:
                value = frontmatter[field]
                is_valid = self._validate_field_value(field, value)
                field_results[field] = {
                    "valid": is_valid,
                    "value": value,
                    "error": None if is_valid else f"Invalid {field} value",
                }
            else:
                field_results[field] = {
                    "valid": False,
                    "value": None,
                    "error": f"Missing required field: {field}",
                }

        return fields_checked, field_results

    def _validate_field_value(self, field: str, value: Any) -> bool:
        """Validate a single field value."""
        if value is None:
            return False

        if field == "id":
            return isinstance(value, str) and bool(value.strip())
        elif field == "title":
            return isinstance(value, str) and bool(value.strip())
        elif field == "type":
            return isinstance(value, str) and bool(value.strip())
        elif field == "status":
            return isinstance(value, str) and bool(value.strip())

        return False

    def _calculate_score(self, field_results: Dict[str, Any]) -> float:
        """Calculate validation score based on field results."""
        if not field_results:
            return 0.0

        valid_count = 0
        for field_result in field_results.values():
            if field_result.get("valid", False):
                valid_count += 1

        return valid_count / len(field_results)

    def _determine_status(self, score: float, errors: List[str]) -> str:
        """Determine validation status based on score and errors."""
        if errors:
            return "invalid"
        elif score >= 1.0:
            return "healthy"
        elif score >= 0.5:
            return "warning"
        else:
            return "invalid"

    def _check_stable_suffix(self, content: str) -> bool:
        """Check if content has stable suffix detection (e.g., `-stable` in path)."""
        if not content:
            return False

        # Check if there's a stable suffix in the content

        # Look for patterns like `-stable` in frontmatter or other indicators
        stable_indicators = [r"-stable\b", r"--stable\b", r"stable[-_]?\d*$"]

        for indicator in stable_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                return True

        return False


class ValidationOrchestrator:
    """Orchestrates validation using multiple validators"""

    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
        ]

    def validate_skill(self, content: str, skill_path: Path) -> ValidationResult:
        """Run all validators and combine results"""
        # Base result with skill info
        result = ValidationResult(valid=True, errors=[], missing_fields=[])

        # Run all validators
        for validator in self.validators:
            try:
                validation_result = validator.validate(content)

                # Merge results
                if hasattr(validation_result, "valid"):
                    result.valid = validation_result.valid
                    result.errors = validation_result.errors
                    result.missing_fields = validation_result.missing_fields
                    break

            except Exception as e:
                # If any validator fails, mark as error
                result.valid = False
                result.errors.append(f"Validation error: {str(e)}")
                break

        return result


class SkillValidator:
    """Concrete validator for skill content (M8S1 FR-SKILL_VALIDATOR)."""

    def validate(self, content: str) -> Dict[str, Any]:
        """Validate skill content (M8S1 FR-SKILL_VALIDATOR_VALIDATE).

        Args:
            content: Raw SKILL.md content string to validate

        Returns:
            Dict with keys: score, status, fields_checked, field_results, errors, stable_suffix_detected
        """
        result: Dict[str, Any] = {
            "score": 0.0,
            "status": "unknown",
            "fields_checked": [],
            "field_results": {},
            "errors": [],
            "stable_suffix_detected": False,
        }

        try:
            # Parse YAML frontmatter
            parsed = self._parse_frontmatter(content)
            if parsed is None:
                result["errors"].append("Invalid or missing YAML frontmatter")
                return result

            # Validate required fields
            result["fields_checked"], field_results = self._validate_fields(parsed)
            result["field_results"] = field_results

            # Calculate score
            result["score"] = self._calculate_score(field_results)

            # Determine status
            result["status"] = self._determine_status(result["score"], result["errors"])

            # Check for stable suffix
            result["stable_suffix_detected"] = self._check_stable_suffix(content)

        except Exception as e:
            result["errors"].append(f"Validation error: {str(e)}")

        return result

    def _parse_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Parse YAML frontmatter from skill content."""
        # Simple frontmatter detection: YAML block between --- delimiters
        if not content or not isinstance(content, str):
            return None

        lines = content.split("\n")
        if len(lines) < 2 or lines[0].strip() != "---":
            return None

        try:
            end_idx = None
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    end_idx = i
                    break

            if end_idx is None:
                return None

            frontmatter_text = "\n".join(lines[1:end_idx])
            return yaml.safe_load(frontmatter_text) or {}

        except Exception:
            return None

    def _validate_fields(
        self, frontmatter: Dict[str, Any]
    ) -> tuple[List[str], Dict[str, Any]]:
        """Validate skill frontmatter fields and return results."""
        fields_checked = []
        field_results = {}

        # Check required fields for skill artifacts
        required_fields = ["id", "title", "type", "status"]

        for field in required_fields:
            fields_checked.append(field)
            if field in frontmatter:
                value = frontmatter[field]
                is_valid = self._validate_field_value(field, value)
                field_results[field] = {
                    "valid": is_valid,
                    "value": value,
                    "error": None if is_valid else f"Invalid {field} value",
                }
            else:
                field_results[field] = {
                    "valid": False,
                    "value": None,
                    "error": f"Missing required field: {field}",
                }

        return fields_checked, field_results

    def _validate_field_value(self, field: str, value: Any) -> bool:
        """Validate a single field value."""
        if value is None:
            return False

        if field == "id":
            return isinstance(value, str) and bool(value.strip())
        elif field == "title":
            return isinstance(value, str) and bool(value.strip())
        elif field == "type":
            return isinstance(value, str) and bool(value.strip())
        elif field == "status":
            return isinstance(value, str) and bool(value.strip())

        return False

    def _calculate_score(self, field_results: Dict[str, Any]) -> float:
        """Calculate validation score based on field results."""
        if not field_results:
            return 0.0

        valid_count = 0
        for field_result in field_results.values():
            if field_result.get("valid", False):
                valid_count += 1

        return valid_count / len(field_results)

    def _determine_status(self, score: float, errors: List[str]) -> str:
        """Determine validation status based on score and errors."""
        if errors:
            return "invalid"
        elif score >= 1.0:
            return "healthy"
        elif score >= 0.5:
            return "warning"
        else:
            return "invalid"

    def _check_stable_suffix(self, content: str) -> bool:
        """Check if content has stable suffix detection (e.g., `-stable` in path)."""
        if not content:
            return False

        # Check if there's a stable suffix in the content

        # Look for patterns like `-stable` in frontmatter or other indicators
        stable_indicators = [r"-stable\b", r"--stable\b", r"stable[-_]?\d*$"]

        for indicator in stable_indicators:
            if re.search(indicator, content, re.IGNORECASE):
                return True

        return False

    def validate_skill_file(self, skill_path: Path) -> dict:
        """Legacy validation method for backward compatibility

        This method is provided to maintain backward compatibility with
        existing healthcheck code that expects the SkillValidator to have
        this method. The new modular validation system uses the validate
        method instead, which is consistent with AEF validation requirements.

        Args:
            skill_path: Path to the skill file (e.g., SKILL.md)

        Returns:
            dict: Validation result with legacy format for backward compatibility
        """
        orchestrator = ValidationOrchestrator()

        try:
            content = skill_path.read_text()

            # Use the existing validate method for actual validation
            result = self.validate(content)

            # Convert to legacy format for backward compatibility
            return {
                "name": skill_path.parent.name,
                "status": result.get("status", "unknown"),
                "validation_score": result.get("score", 0.0),
                "has_stable_suffix": result.get("stable_suffix_detected", False),
                "issues": result.get("errors", []),
                "last_modified": datetime.now().isoformat(),
                "last_checked": datetime.now().isoformat(),
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


def validate_metadata(
    artifact_path: str, schema: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Validates artifact frontmatter and metadata against the Artifact Registry schema."""

    try:
        metadata = extract_frontmatter(artifact_path)
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Could not read file: {e}"],
            "missing_fields": _required_artifact_keys(),
        }

    if metadata is None:
        return {
            "valid": False,
            "errors": ["No valid YAML frontmatter found"],
            "missing_fields": _required_artifact_keys(),
        }

    required = _required_artifact_keys()
    missing = [field for field in required if field not in metadata]

    errors: List[str] = []

    if "metadata" in metadata:
        metadata_obj = metadata["metadata"]
        if not isinstance(metadata_obj, dict):
            errors.append("Field 'metadata' must be an object")
        else:
            for field in _required_metadata_keys():
                if field not in metadata_obj:
                    errors.append(f"metadata.{field} is required")

    if "type" in metadata:
        artifact_type = metadata["type"]
        if not isinstance(artifact_type, str) or not artifact_type.strip():
            errors.append("Field 'type' must be a non-empty string")

    if "milestone_id" in metadata:
        milestone_id = metadata["milestone_id"]
        if not isinstance(milestone_id, str) or not milestone_id.strip():
            errors.append("Field 'milestone_id' must be a non-empty string")

    valid = not missing and not errors
    return {"valid": valid, "errors": errors, "missing_fields": missing}




def _validate_field_type(value: Any, constraints: Dict[str, Any]) -> List[str]:
    """Validate a single field against its type constraints."""
    errors = []

    if "type" in constraints:
        if not _check_type(value, constraints["type"]):
            errors.append(f"Value must be of type {constraints['type']}")

    if "pattern" in constraints and isinstance(value, str):
        if not _check_pattern(value, constraints["pattern"]):
            errors.append(f"Value must match pattern {constraints['pattern']}")

    return errors


def _check_type(value: Any, expected_type: str) -> bool:
    """Check if value matches expected type."""
    type_checkers = {
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: isinstance(v, int),
        "boolean": lambda v: isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)),
        "array": lambda v: isinstance(v, list),
        "object": lambda v: isinstance(v, dict),
    }

    if expected_type in type_checkers:
        return type_checkers[expected_type](value)
    return True


def _check_pattern(value: str, pattern: str) -> bool:
    """Check if value matches regex pattern."""

    return bool(re.match(pattern, value))


def validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates complete artifact against metadata schema.

    Returns a structured result with:
      - valid: boolean
      - errors: string[]
      - missing_fields: string[]
    """
    required = _required_artifact_keys()
    missing_fields = [field for field in required if field not in metadata]

    errors: List[str] = []

    # Validate artifact type against canonical types
    if "type" in metadata:
        artifact_type = metadata["type"]
        if not isinstance(artifact_type, str) or not artifact_type.strip():
            errors.append("Field 'type' must be a non-empty string")
        else:
            # Check if type is in canonical artifact types
            valid_types = get_all_type_definitions().keys()
            if artifact_type not in valid_types:
                errors.append(
                    f"Field 'type' must be one of: {', '.join(sorted(valid_types))}"
                )

    # Validate validation_score range (0-100)
    if "validation_score" in metadata:
        validation_score = metadata["validation_score"]
        if not isinstance(validation_score, (int, float)):
            errors.append("Field 'validation_score' must be a number")
        elif not (0 <= validation_score <= 100):
            errors.append(
                f"Field 'validation_score' must be between 0 and 100 (got {validation_score})"
            )

    if "metadata" in metadata:
        metadata_obj = metadata["metadata"]
        if not isinstance(metadata_obj, dict):
            errors.append("Field 'metadata' must be an object")
        else:
            for field in _required_metadata_keys():
                if field not in metadata_obj:
                    errors.append(f"metadata.{field} is required")

    if "milestone_id" in metadata:
        milestone_id = metadata["milestone_id"]
        if not isinstance(milestone_id, str) or not milestone_id.strip():
            errors.append("Field 'milestone_id' must be a non-empty string")

    valid = not missing_fields and not errors
    return {"valid": valid, "errors": errors, "missing_fields": missing_fields}


# Project Configuration Validation Functions
def validate_project_config(project_root: str) -> Dict[str, Any]:
    """Validate project configuration at the project root."""

    config_file = Path(project_root) / "config.yaml"

    try:
        with open(config_file, "r") as f:
            yaml_content = yaml.safe_load(f)
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Could not read config file: {e}"],
            "missing_fields": [],
        }

    if yaml_content is None:
        return {
            "valid": False,
            "errors": ["No valid YAML in config file"],
            "missing_fields": [],
        }

    errors: List[str] = []
    missing: List[str] = []

    # Check for required fields
    config_schema = {
        "name": {"type": "string", "required": True},
        "version": {"type": "string", "required": True},
        "description": {"type": "string", "required": False},
        "skills": {"type": "array", "required": False},
    }

    for field, field_config in config_schema.items():
        if field_config["required"] and field not in yaml_content:
            missing.append(field)

    # Validate field types and patterns
    for field, value in yaml_content.items():
        if field in config_schema:
            field_errors = _validate_field_type(value, config_schema[field])
            errors.extend([f"{field}: {error}" for error in field_errors])

    # Add human-readable error context for project config validation
    if not missing and not errors:
        return {"valid": True, "errors": [], "missing_fields": []}
    else:
        enhanced_errors = []
        for error in errors:
            enhanced_errors.append(f"Configuration error: {error}")
        for missing_field in missing:
            enhanced_errors.append(f"Missing required field: {missing_field}")
        return {"valid": False, "errors": enhanced_errors, "missing_fields": missing}
