from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from core.artifacts.artifact_types import CanonicalArtifactType, _ARTIFACT_TYPE_DEFINITIONS

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

    def register_type(self, type_name: str, schema: Dict[str, Any], storage_rule: Dict[str, Any]) -> None:
        """Registers an artifact type definition."""
        self._types[type_name] = ArtifactTypeDefinition(
            name=type_name,
            schema=schema,
            storage_rule=storage_rule
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

    def store_relationship(self, source_id: str, target_id: str, relationship_type: str, metadata: dict = None) -> bool:
        """Store a relationship between artifacts.

        Args:
            source_id: The identifier of the source artifact
            target_id: The identifier of the target artifact
            relationship_type: The type of relationship (e.g., "tests", "verifies", "implements")
            metadata: Optional metadata for the relationship

        Returns:
            bool: True if relationship was stored successfully
        """
        relationship = {
            "source_id": source_id,
            "target_id": target_id,
            "relationship_type": relationship_type,
            "metadata": metadata or {}
        }

        if source_id not in self._relationships:
            self._relationships[source_id] = []

        self._relationships[source_id].append(relationship)
        return True

    def get_relationships(self, source_id: str = None) -> list:
        """Get relationships from artifacts.

        Args:
            source_id: Optional artifact identifier to filter relationships

        Returns:
            list: List of relationship dictionaries
        """
        if source_id:
            return self._relationships.get(source_id, [])

        # Return all relationships
        all_relationships = []
        for relationships in self._relationships.values():
            all_relationships.extend(relationships)
        return all_relationships


_registry = ArtifactRegistry()


def _ensure_registered_types() -> None:
    """Registers canonical artifact types from type definitions."""
    for type_name, definition in _ARTIFACT_TYPE_DEFINITIONS.items():
        registry_schema = {
            "type": "object",
            "required": _required_artifact_keys(),
            "properties": {
                "id": {"type": "string", "pattern": "^[A-Z0-9_-]+$"},
                "type": {"type": "string"},
                "title": {"type": "string"},
                "milestone_id": {"type": "string", "pattern": "^M[0-9]+$"},
                "status": {"type": "string", "enum": ["draft", "approved", "implemented", "reviewed", "archived"]},
                "derived_from": {"type": "array", "items": {"type": "string"}},
                "template_version": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
                "metadata": {
                    "type": "object",
                    "required": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
                    "properties": {
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "artifact_identity": {"type": "string"},
                        "artifact_type": {"type": "string"}
                    }
                }
            }
        }

        registry_storage_rule = {
            "pattern": definition.canonical_storage_location,
            "extensions": ["md"],
            "naming_conventions": {
                "milestone_id_prefix": "M",
                "skill_id_prefix": "",
                "health_check_suffix": "-HC",
                "numbering_scheme": "{N}"
            }
        }

        _registry.register_type(type_name, registry_schema, registry_storage_rule)


def _required_artifact_keys() -> List[str]:
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


_ensure_registered_types()


def get_registry() -> ArtifactRegistry:
    """Returns the global artifact registry instance."""
    return _registry
