# Avoid circular imports by using lazy imports
__all__ = [
    "CanonicalArtifactType",
    "ArtifactTypeDefinition",
    "get_type_definition",
    "get_all_type_definitions",
    "ArtifactRegistry",
    "get_registry",
    "AmbiguousResolutionError",
    "ArtifactNotFoundError",
    "resolve_artifact",
    "construct_canonical_path",
    "parse_metadata",
    "get_metadata_from_file",
    "validate_metadata",
    "validate_artifact",
    "ArtifactSystemError",
    "ConfigurationError",
]

def __getattr__(name):
    if name == "CanonicalArtifactType":
        from core.artifacts.artifact_types import CanonicalArtifactType
        return CanonicalArtifactType
    if name == "ArtifactTypeDefinition":
        from core.artifacts.artifact_types import ArtifactTypeDefinition
        return ArtifactTypeDefinition
    if name == "get_type_definition":
        from core.artifacts.artifact_types import get_type_definition
        return get_type_definition
    if name == "get_all_type_definitions":
        from core.artifacts.artifact_types import get_all_type_definitions
        return get_all_type_definitions
    if name == "ArtifactRegistry":
        from core.artifacts.registry import ArtifactRegistry
        return ArtifactRegistry
    if name == "get_registry":
        from core.artifacts.registry import get_registry
        return get_registry
    if name == "AmbiguousResolutionError":
        from core.artifacts.errors import AmbiguousResolutionError
        return AmbiguousResolutionError
    if name == "ArtifactNotFoundError":
        from core.artifacts.errors import ArtifactNotFoundError
        return ArtifactNotFoundError
    if name == "resolve_artifact":
        from core.artifacts.resolution import resolve_artifact
        return resolve_artifact
    if name == "construct_canonical_path":
        from core.artifacts.resolution import construct_canonical_path
        return construct_canonical_path
    if name == "parse_metadata":
        from core.artifacts.metadata import parse_metadata
        return parse_metadata
    if name == "get_metadata_from_file":
        from core.artifacts.metadata import get_metadata_from_file
        return get_metadata_from_file
    if name == "validate_metadata":
        from core.validation import validate_metadata
        return validate_metadata
    if name == "validate_artifact":
        from core.validation import validate_artifact
        return validate_artifact
    if name == "ArtifactSystemError":
        from core.errors import ArtifactSystemError
        return ArtifactSystemError
    if name == "ConfigurationError":
        from core.errors import ConfigurationError
        return ConfigurationError
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
