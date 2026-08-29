#!/usr/bin/env python3
"""
Core artifact creation - Implements the 7-step canonical artifact creation protocol.

Public API:
- create_artifact(artifact_type, title, content, milestone_id, identity, status, derived_from, template_version, extension, registry)

Returns structured dict with created, artifact_identity, path, validation_result, error
"""

from __future__ import annotations

import os
import yaml
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from core.artifacts.registry import get_registry, ArtifactRegistry
from core.artifacts.artifact_types import CanonicalArtifactType
from core.artifacts.resolution import construct_canonical_path, _artifact_identity
from core.validation import validate_metadata


def _now_iso() -> str:
    """Returns current UTC timestamp in ISO 8601 format without microseconds."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_artifact_type(artifact_type: str | CanonicalArtifactType) -> str:
    """Normalizes artifact type to string value."""
    if isinstance(artifact_type, CanonicalArtifactType):
        return artifact_type.value
    return artifact_type


def _validate_artifact_type(artifact_type: str) -> None:
    """Validates that artifact type is registered."""
    registry = get_registry()
    if registry.get_type(artifact_type) is None:
        raise ValueError(f"Unregistered artifact type: {artifact_type}")


def _assign_identity(
    artifact_type: str,
    milestone_id: str,
    requested_identity: Optional[str],
) -> str:
    """Assigns canonical artifact identity."""
    if requested_identity:
        return requested_identity

    registry = get_registry()
    if artifact_type not in registry.list_types():
        raise ValueError(f"Cannot assign identity for unregistered artifact type: {artifact_type}")

    base = artifact_type[:4].upper()
    candidate = f"{base}-{milestone_id}"
    if _artifact_identity({"id": candidate}) != candidate:
        raise ValueError(f"Generated canonical identity '{candidate}' is not canonical.")
    return candidate


def _build_frontmatter(
    artifact_identity: str,
    artifact_type: str,
    title: str,
    milestone_id: str,
    status: str,
    derived_from: List[str],
    template_version: str,
    metadata: Dict[str, Any],
) -> str:
    """Builds YAML frontmatter for an artifact."""
    frontmatter = {
        "id": artifact_identity,
        "type": artifact_type,
        "title": title,
        "milestone_id": milestone_id,
        "status": status,
        "derived_from": derived_from or [],
        "template_version": template_version,
        "metadata": metadata,
    }
    yaml_block = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False).strip()
    return f"---\n{yaml_block}\n---\n"


def _build_metadata(
    artifact_identity: str,
    artifact_type: str,
    title: str,
    milestone_id: str,
    status: str,
    template_version: str,
    derived_from: List[str],
) -> Dict[str, Any]:
    """Builds metadata dictionary for an artifact."""
    now = _now_iso()
    return {
        "created_at": now,
        "updated_at": now,
        "artifact_identity": artifact_identity,
        "artifact_type": artifact_type,
        "title": title,
        "milestone_id": milestone_id,
        "status": status,
        "template_version": template_version,
        "derived_from": derived_from,
    }


def create_artifact(
    artifact_type: str | CanonicalArtifactType,
    title: str,
    content: str,
    milestone_id: Optional[str] = None,
    identity: Optional[str] = None,
    status: str = "draft",
    derived_from: Optional[List[str]] = None,
    template_version: str = "1.0.0",
    extension: str = ".md",
    registry: Optional[ArtifactRegistry] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Creates a canonical artifact via the 7-step protocol.

    Returns a dict with fields:
      - created: boolean indicating success
      - artifact_identity: canonical identity string or None
      - path: absolute filesystem path or None
      - validation_result: dict with validation details
      - error: error message string or None
    """
    if milestone_id is None:
        milestone_id = "M9"

    if registry is None:
        registry = get_registry()

    # Step 1: determine artifact type
    artifact_type = _normalize_artifact_type(artifact_type)
    try:
        _validate_artifact_type(artifact_type)
    except ValueError as e:
        return {
            "created": False,
            "success": False,
            "artifact_identity": None,
            "path": None,
            "validation_result": {},
            "error": str(e),
        }
    type_def = registry.get_type(artifact_type)
    if type_def is None:
        return {
            "created": False,
            "success": False,
            "artifact_identity": None,
            "path": None,
            "validation_result": {},
            "error": f"Artifact type '{artifact_type}' is not registered in Artifact Registry.",
        }

    # Step 2: assign canonical artifact identity
    try:
        assigned_identity = _assign_identity(artifact_type, milestone_id, identity)
    except ValueError as e:
        return {
            "created": False,
            "success": False,
            "artifact_identity": None,
            "path": None,
            "validation_result": {},
            "error": str(e),
        }

    # Step 2: assign canonical artifact identity
    try:
        assigned_identity = _assign_identity(artifact_type, milestone_id, identity)
    except ValueError as e:
        return {
            "created": False,
            "artifact_identity": None,
            "path": None,
            "validation_result": {},
            "error": str(e),
        }

    # Step 3: generate required metadata
    metadata = _build_metadata(
        assigned_identity,
        artifact_type,
        title,
        milestone_id,
        status,
        template_version,
        derived_from or [],
    )

    # Step 4: write canonical frontmatter
    frontmatter = _build_frontmatter(
        assigned_identity,
        artifact_type,
        title,
        milestone_id,
        status,
        derived_from or [],
        template_version,
        metadata,
    )
    body = f"{frontmatter}{content.strip()}\n"

    # Step 5: resolve canonical storage path
    try:
        relative_path = construct_canonical_path(milestone_id, artifact_type, assigned_identity, extension=extension)
    except ValueError as e:
        return {
            "created": False,
            "artifact_identity": assigned_identity,
            "path": None,
            "validation_result": {},
            "error": f"Canonical storage path resolution failed: {e}",
        }

    resolved_path = os.path.abspath(relative_path)
    os.makedirs(os.path.dirname(resolved_path), exist_ok=True)

    # Step 6: validate resulting artifact
    tmp_path = resolved_path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(body)
        validation_result = validate_metadata(tmp_path, schema=registry.get_schema(artifact_type))
    except Exception as e:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        return {
            "created": False,
            "artifact_identity": assigned_identity,
            "path": None,
            "validation_result": {},
            "error": f"Failed to validate created artifact: {e}",
        }

    if not validation_result.get("valid", False):
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        error_message = (
            f"Artifact validation failed for identity={assigned_identity}: "
            f"missing_fields={validation_result.get('missing_fields', [])} "
            f"errors={validation_result.get('errors', [])}"
        )
        return {
            "created": False,
            "artifact_identity": assigned_identity,
            "path": None,
            "validation_result": validation_result,
            "error": error_message,
        }

    # Step 7: move artifact to final location
    try:
        os.replace(tmp_path, resolved_path)
    except OSError:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        return {
            "created": False,
            "artifact_identity": assigned_identity,
            "path": None,
            "validation_result": validation_result,
            "error": "Failed to move temporary artifact to canonical path.",
        }

    # Step 8: report created artifact
    return {
        "created": True,
        "artifact_identity": assigned_identity,
        "path": resolved_path,
        "validation_result": validation_result,
        "error": None,
    }