import os
import yaml
from typing import Dict, Any, Optional, List

from core.artifacts.artifact_types import get_type_definition
from core.artifacts.metadata import parse_metadata, get_metadata_from_file
from core.artifacts.errors import AmbiguousResolutionError, ValidationError, ArtifactNotFoundError
from core.validation import validate_metadata

# Define the base directory for artifacts, relative to the project root
ARTIFACTS_BASE_DIR = "milestones"
LEGACY_ARTIFACT_MAPPINGS = {
    # Example mapping: "M5S1I1.md": "investigation"
    # This would need to be populated based on known legacy patterns.
}


def _error_to_dict(error):
    """Convert an error object to a dictionary with type field for test expectations."""
    if isinstance(error, AmbiguousResolutionError):
        return {
            "type": "AmbiguousResolutionError",
            "matching_artifacts": error.matching_artifacts,
            "match_criteria": error.match_criteria,
            "user_instruction": error.user_instruction
        }
    elif isinstance(error, ArtifactNotFoundError):
        return {
            "type": "ArtifactNotFoundError",
            "identity": error.identity,
            "attempted_path": error.attempted_path,
            "failure_reason": error.failure_reason
        }
    elif isinstance(error, ValidationError):
        return {
            "type": "ValidationError",
            "artifact_identity": error.artifact_identity,
            "errors": error.errors,
            "missing_fields": error.missing_fields
        }
    else:
        return {
            "type": type(error).__name__,
            "message": str(error)
        }


def _artifact_identity(artifact: Dict[str, Any]) -> str:
    """Extract canonical artifact identity from artifact metadata."""
    return artifact.get('id') or artifact.get('artifact_identity') or ''


def _is_canonical_artifact(artifact_path: str) -> bool:
    """Check if an artifact file has a canonical identity."""
    try:
        metadata = parse_metadata(artifact_path)
        if not metadata:
            return False
        has_legacy_id = 'id' in metadata
        has_canonical_identity = 'artifact_identity' in metadata
        return has_legacy_id or has_canonical_identity
    except Exception:
        return False


def _collect_candidates(identity: Optional[str] = None, artifact_type: Optional[str] = None,
                       metadata_filter: Optional[Dict[str, Any]] = None, strict: bool = False) -> List[str]:
    """Collect candidate artifact paths based on resolution criteria."""
    candidates = []

    for root, dirs, files in os.walk(ARTIFACTS_BASE_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                if strict and not _is_canonical_artifact(file_path):
                    continue

                try:
                    metadata = get_metadata_from_file(file_path)
                    if not metadata:
                        continue

                    if identity and _artifact_identity(metadata) != identity:
                        continue

                    if artifact_type and metadata.get('type') != artifact_type:
                        continue

                    if metadata_filter:
                        match = True
                        for key, value in metadata_filter.items():
                            if key not in metadata or metadata[key] != value:
                                match = False
                                break
                        if not match:
                            continue

                    candidates.append(file_path)
                except Exception:
                    continue

    return candidates


def construct_canonical_path(milestone_id: str, artifact_type: str, artifact_id: str, extension: str = '.md') -> str:
    """Constructs the canonical path for an artifact."""
    artifact_type_def = get_type_definition(artifact_type)
    if not artifact_type_def:
        raise Exception(f"Unknown artifact type: {artifact_type}")

    storage_template = artifact_type_def.get('canonical_storage_location') if isinstance(artifact_type_def, dict) else getattr(artifact_type_def, 'canonical_storage_location', None)
    if not storage_template:
        if artifact_type in ['specification', 'verification', 'investigation', 'implementation', 'evaluation', 'review', 'audit']:
            type_dir = artifact_type + 's'
            return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, type_dir, f"{artifact_id}{extension}")
        elif artifact_type == 'milestone':
            return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, f"{milestone_id}{extension}")
        else:
            return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, artifact_type + 's', f"{artifact_id}{extension}")

    canonical_path = storage_template.replace('<M_ID>', milestone_id).replace('<SPEC_ID>', artifact_id)
    return canonical_path


def resolve_artifact(identity: Optional[str] = None, type: Optional[str] = None,
                    metadata_filter: Optional[Dict[str, Any]] = None, strict: bool = False) -> Dict[str, Any]:
    """Resolves an artifact's type, metadata, and other details.

    Supports resolution by identity, type, or metadata filter.
    Handles ambiguous resolution and legacy compatibility.
    """
    candidates = _collect_candidates(identity, type, metadata_filter, strict)

    if not candidates:
        error = ArtifactNotFoundError(
            identity=identity,
            attempted_path=None,
            failure_reason=f"No artifact found matching criteria: identity={identity}, type={type}, filter={metadata_filter}, strict={strict}"
        )
        return {"resolved": False, "error": _error_to_dict(error)}

    if len(candidates) == 1:
        artifact_path = candidates[0]
        try:
            metadata = parse_metadata(artifact_path)
            if not metadata:
                error = ArtifactNotFoundError(
                    identity=identity,
                    attempted_path=artifact_path,
                    failure_reason="No metadata found in artifact file"
                )
                return {"resolved": False, "error": _error_to_dict(error)}

            artifact_type_def = get_type_definition(metadata.get('type'))
            if not artifact_type_def:
                error = ArtifactNotFoundError(
                    identity=identity,
                    attempted_path=artifact_path,
                    failure_reason=f"Unknown artifact type '{metadata.get('type')}'"
                )
                return {"resolved": False, "error": _error_to_dict(error)}

            validation_result = validate_metadata(artifact_path, artifact_type_def)
            if not validation_result.get('valid'):
                error = ValidationError(
                    artifact_identity=_artifact_identity(metadata),
                    errors=validation_result.get('errors', []),
                    missing_fields=validation_result.get('missing_fields', [])
                )
                return {"resolved": False, "error": _error_to_dict(error)}

            milestone_id = metadata.get('milestone_id')
            if not milestone_id:
                error = ArtifactNotFoundError(
                    identity=identity,
                    attempted_path=artifact_path,
                    failure_reason="Missing milestone_id in metadata"
                )
                return {"resolved": False, "error": _error_to_dict(error)}

            canonical_path = construct_canonical_path(milestone_id, metadata.get('type'), metadata.get('id'))

            return {
                "resolved": True,
                "artifact": {
                    "path": artifact_path,
                    "metadata": metadata,
                    "canonical_path": canonical_path,
                    "source": 'resolution'
                }
            }

        except Exception as e:
            error = ArtifactNotFoundError(
                identity=identity,
                attempted_path=artifact_path,
                failure_reason=str(e)
            )
            return {"resolved": False, "error": _error_to_dict(error)}

    error = AmbiguousResolutionError(
        matching_artifacts=[_artifact_identity(parse_metadata(path)) for path in candidates if parse_metadata(path)],
        match_criteria={
            "identity": identity,
            "type": type,
            "metadata_filter": metadata_filter,
            "strict": strict
        },
        user_instruction="Provide identity or type filter to disambiguate"
    )
    return {"resolved": False, "error": _error_to_dict(error)}