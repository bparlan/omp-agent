#!/usr/bin/env python3
"""
Artifact creation module for AEF-OMP.

Implements the 7-step canonical creation protocol for artifacts.
Separated from validation for better modularity.
"""

from __future__ import annotations

import os
import yaml
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from core.artifacts.registry import get_registry, ArtifactRegistry
from core.artifacts.artifact_types import CanonicalArtifactType
from core.artifacts.resolution import construct_canonical_path
from core.validation import validate_metadata


def _now_iso() -> str:
    """Returns current UTC timestamp in ISO 8601 format without microseconds."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_artifact_type(artifact_type: str | CanonicalArtifactType) -> str:
    """Normalizes artifact type to string value."""
    if isinstance(artifact_type, CanonicalArtifactType):
        return artifact_type.name
    return artifact_type


def _validate_artifact_type(artifact_type: str) -> None:
    """Validates that artifact type is registered."""
    registry = get_registry()
    if registry.get_type(artifact_type) is None:
        raise ValueError(f"Unregistered artifact type: {artifact_type}")


def _assign_identity(
    registry: ArtifactRegistry, artifact_type: str, title: str, milestone_id: str, identity: Optional[str] = None
) -> str:
    """Assigns canonical artifact identity."""
    # Generate artifact identity using the resolution module
    from core.artifacts.resolution import _artifact_identity as artifact_identity_func
    
    # Create a minimal artifact dict for identity generation
    artifact_data = {
        "id": identity,
        "artifact_identity": identity,
        "title": title,
        "type": artifact_type,
        "milestone_id": milestone_id,
    }
    
    return artifact_identity_func(artifact_data)


def _build_frontmatter(metadata: Dict[str, Any]) -> str:
    """Builds YAML frontmatter for an artifact."""
    frontmatter = {
        "title": metadata.get("title", ""),
        "artifact_type": metadata.get("artifact_type", ""),
        "milestone_id": metadata.get("milestone_id", ""),
        "identity": metadata.get("identity", ""),
        "status": metadata.get("status", "draft"),
        "derived_from": metadata.get("derived_from", []),
        "template_version": metadata.get("template_version", "1.0.0"),
        "created_at": metadata.get("created_at", _now_iso()),
        "updated_at": metadata.get("updated_at", _now_iso()),
    }
    
    return f"---\n{yaml.dump(frontmatter, default_flow_style=False)}\n---\n"


def _build_metadata(
    artifact_type: str,
    title: str,
    content: str,
    milestone_id: str,
    identity: Optional[str] = None,
    status: str = "draft",
    derived_from: Optional[List[str]] = None,
    template_version: str = "1.0.0",
    extension: str = ".md",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Builds metadata dictionary for an artifact."""
    if metadata is None:
        metadata = {}
    
    # Build artifact identity
    registry = get_registry()
    artifact_identity = _assign_identity(registry, artifact_type, title, milestone_id, identity)
    
    # Build frontmatter
    frontmatter_metadata = {
        "title": title,
        "artifact_type": artifact_type,
        "milestone_id": milestone_id,
        "identity": artifact_identity,
        "status": status,
        "derived_from": derived_from or [],
        "template_version": template_version,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    
    # Build storage path
    storage_path = construct_canonical_path(
        artifact_type, title, milestone_id, artifact_identity, extension
    )
    
    return {
        "artifact_identity": artifact_identity,
        "storage_path": storage_path,
        "frontmatter": frontmatter_metadata,
        "content": content,
        "metadata": metadata,
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
    
    Args:
        artifact_type: Type of artifact to create
        title: Title of the artifact
        content: Content of the artifact
        milestone_id: Milestone ID where artifact should be created
        identity: Optional artifact identity
        status: Artifact status (default: "draft")
        derived_from: List of artifact identities this artifact is derived from
        template_version: Template version for the artifact (default: "1.0.0")
        extension: File extension for the artifact (default: ".md")
        registry: Registry instance to use (default: global registry)
        metadata: Additional metadata for the artifact
        
    Returns:
        Dict[str, Any]: Creation result with keys:
            - created: bool indicating success
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
            "validation_result": {
                "is_valid": False,
                "errors": [str(e)],
                "warnings": [],
                "score": 0.0,
            },
            "error": str(e),
        }
    
    # Step 2: build metadata
    artifact_metadata = _build_metadata(
        artifact_type, title, content, milestone_id, identity, status, derived_from,
        template_version, extension, metadata,
    )
    
    # Step 3: construct storage path
    storage_path = artifact_metadata["storage_path"]
    
    # Step 4: validate metadata
    validation_result = validate_metadata(storage_path)
    
    if not validation_result.get("is_valid", False):
        return {
            "created": False,
            "success": False,
            "artifact_identity": artifact_metadata["artifact_identity"],
            "path": None,
            "validation_result": validation_result,
            "error": "Metadata validation failed",
        }
    
    # Step 5: write artifact to filesystem
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        # Write artifact content
        with open(storage_path, "w") as f:
            # Write frontmatter
            f.write(_build_frontmatter(artifact_metadata["frontmatter"]))
            
            # Write content
            f.write(content)
        
        # Store artifact in registry
        registry.store_relationship(
            artifact_metadata["artifact_identity"], "created", "system", {}
        )
        
        return {
            "created": True,
            "success": True,
            "artifact_identity": artifact_metadata["artifact_identity"],
            "path": storage_path,
            "validation_result": validation_result,
            "error": None,
        }
        
    except Exception as e:
        return {
            "created": False,
            "success": False,
            "artifact_identity": artifact_metadata["artifact_identity"],
            "path": None,
            "validation_result": validation_result,
            "error": f"Failed to write artifact: {str(e)}",
        }