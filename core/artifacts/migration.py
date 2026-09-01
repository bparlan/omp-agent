#!/usr/bin/env python3
"""
Legacy artifact migration workflow.

Implements FR-MIGRATION_SAFETY:
- Migration is an explicit separate process from normal artifact creation.
- Preserves original content and provenance.
- Establishes lineage through canonical relationships.
- Validates migrated artifacts before reporting success.
- Reports results explicitly.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import yaml
from core.artifacts.errors import ArtifactNotFoundError
from core.artifacts.artifact_types import get_type_definition
from core.validation import validate_metadata


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class MigrationResult:
    """Explicit migration result report."""

    def __init__(
        self,
        success: bool,
        original_path: str,
        migrated_path: Optional[str],
        validation_result: Dict[str, Any],
        provenance: Dict[str, Any],
        errors: List[str],
    ) -> None:
        self.success = success
        self.original_path = original_path
        self.migrated_path = migrated_path
        self.validation_result = validation_result
        self.provenance = provenance
        self.errors = errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "original_path": self.original_path,
            "migrated_path": self.migrated_path,
            "validation_result": self.validation_result,
            "provenance": self.provenance,
            "errors": self.errors,
        }


def _read_legacy_artifact(path: str) -> Dict[str, Any]:
    """Read legacy artifact content and metadata."""
    if not os.path.exists(path):
        raise ArtifactNotFoundError(
            identity=None,
            attempted_path=path,
            failure_reason="Legacy artifact file does not exist",
        )

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---\n", 2)
    metadata: Dict[str, Any] = {}
    body = content
    if len(parts) >= 3:
        metadata = yaml.safe_load(parts[1]) or {}
        body = parts[2]

    return {"metadata": metadata, "body": body, "content": content}


def _build_migration_frontmatter(
    legacy_metadata: Dict[str, Any],
    artifact_type: str,
    canonical_identity: str,
    migrated_at: str,
) -> Dict[str, Any]:
    """Build canonical frontmatter for migrated artifact."""
    frontmatter: Dict[str, Any] = {
        "id": canonical_identity,
        "type": artifact_type,
        "title": legacy_metadata.get("title", "Migrated artifact"),
        "milestone_id": legacy_metadata.get("milestone_id", ""),
        "status": legacy_metadata.get("status", "archived"),
        "derived_from": legacy_metadata.get("derived_from", []),
        "template_version": legacy_metadata.get("template_version", "1.0.0"),
        "metadata": {
            "created_at": legacy_metadata.get("created_at", migrated_at),
            "updated_at": migrated_at,
            "artifact_identity": canonical_identity,
            "artifact_type": artifact_type,
        },
        "relationships": {
            "derived_from": [
                f"legacy:{os.path.basename(legacy_metadata.get('_legacy_path', ''))}"
            ],
        },
    }

    return frontmatter


def migrate_legacy_artifact(
    legacy_path: str,
    artifact_type: str,
    canonical_identity: str,
    destination_root: Optional[str] = None,
) -> MigrationResult:
    """Migrate a legacy artifact to canonical form.

    This is an explicit opt-in process. It does not alter the original artifact.
    """
    errors: List[str] = []
    original_path = os.path.abspath(legacy_path)

    try:
        legacy = _read_legacy_artifact(original_path)
    except Exception as exc:
        return MigrationResult(
            success=False,
            original_path=original_path,
            migrated_path=None,
            validation_result={
                "valid": False,
                "errors": [str(exc)],
                "missing_fields": [],
            },
            provenance={},
            errors=[str(exc)],
        )

    type_def = get_type_definition(artifact_type)
    storage_template = type_def.get("canonical_storage_location") if type_def else None
    if not type_def:
        errors.append(f"Unregistered artifact type: {artifact_type}")

    if not canonical_identity:
        errors.append("Missing canonical identity for migrated artifact")

    if errors:
        return MigrationResult(
            success=False,
            original_path=original_path,
            migrated_path=None,
            validation_result={"valid": False, "errors": errors, "missing_fields": []},
            provenance={},
            errors=errors,
        )

    migrated_at = _now_iso()
    legacy_metadata = dict(legacy["metadata"])
    legacy_metadata["_legacy_path"] = original_path

    frontmatter = _build_migration_frontmatter(
        legacy_metadata=legacy_metadata,
        artifact_type=artifact_type,
        canonical_identity=canonical_identity,
        migrated_at=migrated_at,
    )

    frontmatter_block = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\n"
    migrated_content = frontmatter_block + legacy["body"]

    if storage_template:
        migrated_path = storage_template.replace(
            "<M_ID>", frontmatter.get("milestone_id", "")
        ).replace("<SPEC_ID>", canonical_identity)
    else:
        type_dir = artifact_type + "s"
        milestone_id = frontmatter.get("milestone_id", "")
        migrated_path = os.path.join(
            destination_root or "milestones",
            milestone_id,
            type_dir,
            f"{canonical_identity}.md",
        )

    migrated_dir = os.path.dirname(migrated_path)
    if migrated_dir:
        os.makedirs(migrated_dir, exist_ok=True)

    try:
        with open(migrated_path, "w", encoding="utf-8") as f:
            f.write(migrated_content)
    except Exception as exc:
        return MigrationResult(
            success=False,
            original_path=original_path,
            migrated_path=migrated_path,
            validation_result={
                "valid": False,
                "errors": [f"Failed to write migrated artifact: {exc}"],
                "missing_fields": [],
            },
            provenance={},
            errors=[f"Failed to write migrated artifact: {exc}"],
        )

    validation_result = validate_metadata(migrated_path)

    provenance = {
        "original_path": original_path,
        "migrated_at": migrated_at,
        "canonical_identity": canonical_identity,
        "artifact_type": artifact_type,
        "original_preserved": os.path.exists(original_path),
    }

    success = (
        bool(validation_result.get("valid", False))
        and os.path.exists(migrated_path)
        and os.path.exists(original_path)
    )

    return MigrationResult(
        success=success,
        original_path=original_path,
        migrated_path=migrated_path,
        validation_result=validation_result,
        provenance=provenance,
        errors=validation_result.get("errors", []) if not success else [],
    )
