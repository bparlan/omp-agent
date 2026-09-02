from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from core.artifacts.artifact_types import _ARTIFACT_TYPE_DEFINITIONS


@dataclass
class ArtifactTypeDefinition:
    """Artifact type registration record."""

    name: str
    schema: Dict[str, Any]
    storage_rule: Dict[str, Any]


class ArtifactRegistry:
    """Canonical registry for artifact types, metadata schemas, and storage rules."""

    def __init__(self) -> None:
        self._types: Dict[str, ArtifactTypeDefinition] = {}
        self._relationships: Dict[str, List[Dict[str, Any]]] = {}

    def register_type(
        self, type_name: str, schema: Dict[str, Any], storage_rule: Dict[str, Any]
    ) -> None:
        """Registers an artifact type definition."""
        self._types[type_name] = ArtifactTypeDefinition(
            name=type_name,
            schema=schema,
            storage_rule=storage_rule,
        )

    def get_type(self, type_name: str) -> Optional[ArtifactTypeDefinition]:
        """Returns registered type definition or None."""
        return self._types.get(type_name)

    def get_schema(self, type_name: str) -> Optional[Dict[str, Any]]:
        """Returns metadata schema for type or None."""
        record = self._types.get(type_name)
        return record.schema if record else None

    def get_storage_rule(self, type_name: str) -> Optional[Dict[str, Any]]:
        """Returns storage rule for type or None."""
        record = self._types.get(type_name)
        return record.storage_rule if record else None

    def list_types(self) -> List[str]:
        """Returns all registered type names."""
        return list(self._types.keys())

    def store_relationship(
        self, source_id: str, relationship_type: str, target_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """Store a relationship between artifacts.
        
        Returns:
            bool: True if relationship stored successfully
        """
        if source_id not in self._relationships:
            self._relationships[source_id] = []
        
        self._relationships[source_id].append({
            "type": relationship_type,
            "target_id": target_id,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat(),
        })
        
        return True

    def get_relationships(self, source_id: str = None) -> list:
        """Get relationships from artifacts.
        
        Args:
            source_id: Optional source artifact ID
            
        Returns:
            list: List of relationships
        """
        if source_id:
            return self._relationships.get(source_id, [])
        else:
            all_relationships = []
            for relationships in self._relationships.values():
                all_relationships.extend(relationships)
            return all_relationships


_registry = ArtifactRegistry()


def _ensure_registered_types() -> None:
    """Registers canonical artifact types from type definitions."""
    import core.artifacts.artifact_types as artifact_types

    # Register all canonical artifact types
    for type_name, type_definition in _ARTIFACT_TYPE_DEFINITIONS.items():
        schema = {
            "type": type_definition.get("type"),
            "description": type_definition.get("description", ""),
            "fields": type_definition.get("fields", []),
        }
        
        storage_rule = {
            "path_template": type_definition.get("path_template"),
            "filename": type_definition.get("filename"),
            "storage_location": type_definition.get("storage_location", "milestones"),
        }
        
        _registry.register_type(type_name, schema, storage_rule)


_registry.register_type(
    "specification",
    {
        "type": "specification",
        "description": "Specification artifacts",
        "fields": ["name", "title", "milestone_id", "status"],
    },
    {
        "path_template": "milestones/{milestone_id}/SPEC-{spec_id}.md",
        "filename": "SPEC-{spec_id}.md",
        "storage_location": "milestones",
    },
)

_registry.register_type(
    "verification",
    {
        "type": "verification",
        "description": "Verification artifacts",
        "fields": ["spec_id", "milestone_id", "status"],
    },
    {
        "path_template": "milestones/{milestone_id}/VER-{spec_id}V{m}.md",
        "filename": "VER-{spec_id}V{m}.md",
        "storage_location": "milestones",
    },
)

_registry.register_type(
    "test_set",
    {
        "type": "test_set",
        "description": "Test set artifacts",
        "fields": ["milestone_id", "spec_id", "status"],
    },
    {
        "path_template": "milestones/{milestone_id}/TEST-{spec_id}T{p}.md",
        "filename": "TEST-{spec_id}T{p}.md",
        "storage_location": "milestones",
    },
)

_registry.register_type(
    "evaluation",
    {
        "type": "evaluation",
        "description": "Evaluation artifacts",
        "fields": ["milestone_id", "spec_id"],
    },
    {
        "path_template": "milestones/{milestone_id}/EVA-{spec_id}.md",
        "filename": "EVA-{spec_id}.md",
        "storage_location": "milestones",
    },
)

_registry.register_type(
    "review",
    {
        "type": "review",
        "description": "Review artifacts",
        "fields": ["milestone_id", "spec_id"],
    },
    {
        "path_template": "milestones/{milestone_id}/REV-{spec_id}.md",
        "filename": "REV-{spec_id}.md",
        "storage_location": "milestones",
    },
)

_registry.register_type(
    "closure",
    {
        "type": "closure",
        "description": "Closure artifacts",
        "fields": ["milestone_id"],
    },
    {
        "path_template": "CLOSE-{milestone_id}-*.md",
        "filename": "CLOSE-{milestone_id}-*.md",
        "storage_location": "milestones",
    },
)

_import_modules()


def _import_modules():
    """Import module dependencies."""
    try:
        import datetime
    except ImportError:
        import datetime


_registry = ArtifactRegistry()


def _ensure_registered_types() -> None:
    """Registers canonical artifact types from type definitions."""
    import core.artifacts.artifact_types as artifact_types

    # Register all canonical artifact types
    for type_name, type_definition in _ARTIFACT_TYPE_DEFINITIONS.items():
        schema = {
            "type": type_definition.get("type"),
            "description": type_definition.get("description", ""),
            "fields": type_definition.get("fields", []),
        }
        
        storage_rule = {
            "path_template": type_definition.get("path_template"),
            "filename": type_definition.get("filename"),
            "storage_location": type_definition.get("storage_location", "milestones"),
        }
        
        _registry.register_type(type_name, schema, storage_rule)


# Import modules for datetime
import datetime

# Register canonical types
_ensure_registered_types()


def get_registry() -> ArtifactRegistry:
    """Returns the global artifact registry instance."""
    return _registry


def get_artifact_type(identifier: str) -> Optional["CanonicalArtifactType"]:
    """Returns registered artifact type definition or None.
    
    Args:
        identifier: Artifact type identifier
        
    Returns:
        Optional[CanonicalArtifactType]: Artifact type definition or None
    """
    registry = get_registry()
    type_def = registry.get_type(identifier)
    
    if type_def is None:
        return None
    
    # Convert ArtifactTypeDefinition to CanonicalArtifactType
    from core.artifacts.types import CanonicalArtifactType
    
    return CanonicalArtifactType(
        name=type_def.name,
        schema=type_def.schema,
        storage_rule=type_def.storage_rule,
    )


def get_all_artifact_types() -> List["CanonicalArtifactType"]:
    """Returns all registered artifact types.
    
    Returns:
        List[CanonicalArtifactType]: All artifact types
    """
    registry = get_registry()
    type_names = registry.list_types()
    
    from core.artifacts.types import CanonicalArtifactType
    
    artifact_types = []
    for type_name in type_names:
        type_def = registry.get_type(type_name)
        if type_def:
            artifact_types.append(
                CanonicalArtifactType(
                    name=type_def.name,
                    schema=type_def.schema,
                    storage_rule=type_def.storage_rule,
                )
            )
    
    return artifact_types


def get_type_definition(name: str) -> Optional[Dict[str, Any]]:
    """Returns type definition for given name.
    
    Args:
        name: Type name
        
    Returns:
        Optional[Dict[str, Any]]: Type definition or None
    """
    artifact_type = get_artifact_type(name)
    
    if artifact_type is None:
        return None
    
    return {
        "name": artifact_type.name,
        "schema": artifact_type.schema,
        "storage_rule": artifact_type.storage_rule,
    }


def get_all_type_definitions() -> Dict[str, Dict[str, Any]]:
    """Returns all type definitions.
    
    Returns:
        Dict[str, Dict[str, Any]]: All type definitions keyed by name
    """
    from core.artifacts.types import CanonicalArtifactType
    
    artifact_types = get_all_artifact_types()
    
    type_definitions = {}
    for artifact_type in artifact_types:
        type_definitions[artifact_type.name] = {
            "name": artifact_type.name,
            "schema": artifact_type.schema,
            "storage_rule": artifact_type.storage_rule,
        }
    
    return type_definitions


def store_relationship(source_id: str, relationship_type: str, target_id: str, metadata: Dict[str, Any]) -> bool:
    """Store a relationship between artifacts.
    
    Args:
        source_id: Source artifact ID
        relationship_type: Type of relationship
        target_id: Target artifact ID
        metadata: Relationship metadata
        
    Returns:
        bool: True if relationship stored successfully
    """
    return get_registry().store_relationship(source_id, relationship_type, target_id, metadata)


def get_relationships(source_id: str = None) -> list:
    """Get relationships from artifacts.
    
    Args:
        source_id: Optional source artifact ID
        
    Returns:
        list: List of relationships
    """
    return get_registry().get_relationships(source_id)