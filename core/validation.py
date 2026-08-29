#!/usr/bin/env python3
"""Artifact validation module - FR-ARTIFACT_VALIDATION

Validates artifact metadata against canonical contract.
Implements contract: validate_metadata(artifact_path, schema?)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import yaml
from core.artifacts.metadata import extract_frontmatter


@dataclass
class ValidationResult:
    """M9S1 canonical artifact validation result."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)


@dataclass
class ArtifactValidationResult:
    """M9S1 artifact validation result (legacy compatibility)."""
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)


class Validator:
    """Abstract base class for skill validation rules (M8S1 FR-VALIDATOR_BASE_CLASS)."""
    def validate(self, content: str) -> Dict[str, Any]:
        raise NotImplementedError


def _required_artifact_keys() -> List[str]:
    """Return required artifact metadata keys per canonical contract."""
    return ["id", "type", "title", "milestone_id", "status", "derived_from", "template_version", "metadata"]


def _required_metadata_keys() -> List[str]:
    """Return required metadata sub-keys."""
    return ["created_at", "updated_at", "artifact_identity", "artifact_type"]


def validate_metadata(artifact_path: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Validates artifact frontmatter and metadata against the Artifact Registry schema."""

    try:
        metadata = extract_frontmatter(artifact_path)
    except Exception as e:
        return {"valid": False, "errors": [f"Could not read file: {e}"], "missing_fields": _required_artifact_keys()}

    if metadata is None:
        return {"valid": False, "errors": ["No valid YAML frontmatter found"], "missing_fields": _required_artifact_keys()}

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


def validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates artifact metadata against canonical contract.

    Returns a structured result with:
      - valid: boolean
      - errors: string[]
      - missing_fields: string[]
    """
    required = _required_artifact_keys()
    missing_fields = [field for field in required if field not in metadata]

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

    valid = not missing_fields and not errors
    return {"valid": valid, "errors": errors, "missing_fields": missing_fields}
