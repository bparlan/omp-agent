from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class CanonicalArtifactType:
    machine_identifier: str
    human_readable_name: str
    purpose: str
    producer_skills: List[str]
    consumer_skills: List[str]
    canonical_storage_location: str
    required_metadata: List[str]
    optional_metadata: List[str]
    lifecycle_states: List[str]
    allowed_relationships: List[str]

_RAW_ARTIFACT_TYPE_DEFINITIONS = {
    "specification": {
        "machine_identifier": "specification",
        "human_readable_name": "Specification",
        "purpose": "Defines canonical requirements and contracts",
        "producer_skills": ["generate-spec", "generate-verification"],
        "consumer_skills": ["implement-specification", "evaluate-implementation"],
        "canonical_storage_location": "<M_ID>/specifications/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version", "producer_skill"],
        "lifecycle_states": ["draft", "proposed", "implemented", "reviewed", "archived"],
        "allowed_relationships": ["derived_from", "verifies", "implements", "evaluates"]
    },
    "verification": {
        "machine_identifier": "verification",
        "human_readable_name": "Verification Protocol",
        "purpose": "Defines testing and validation requirements",
        "producer_skills": ["generate-verification"],
        "consumer_skills": ["evaluate-implementation", "review-implementation"],
        "canonical_storage_location": "<M_ID>/verifications/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "proposed", "implemented", "reviewed", "archived"],
        "allowed_relationships": ["derived_from", "tests", "evaluates", "implements"]
    },
    "test": {
        "machine_identifier": "test",
        "human_readable_name": "Test Plan",
        "purpose": "Defines executable test cases",
        "producer_skills": [],
        "consumer_skills": ["evaluate-implementation"],
        "canonical_storage_location": "<M_ID>/tests/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "proposed", "implemented", "reviewed", "archived"],
        "allowed_relationships": ["derived_from", "tests", "implements", "evaluates"]
    },
    "implementation": {
        "machine_identifier": "implementation",
        "human_readable_name": "Implementation",
        "purpose": "Actual code implementation",
        "producer_skills": ["implement-specification"],
        "consumer_skills": ["evaluate-implementation"],
        "canonical_storage_location": "<M_ID>/implementations/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version", "commit_hash"],
        "lifecycle_states": ["draft", "proposed", "implemented", "reviewed", "archived"],
        "allowed_relationships": ["derived_from", "implements", "evaluates", "verifies"]
    },
    "milestone": {
        "machine_identifier": "milestone",
        "human_readable_name": "Milestone",
        "purpose": "Aggregates artifacts for a major release",
        "producer_skills": [],
        "consumer_skills": ["manage-roadmap"],
        "canonical_storage_location": "<M_ID>/<M_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "approved", "implemented", "reviewed", "archived"],
        "allowed_relationships": ["derived_from", "verifies", "evaluates", "reviews", "implements", "tests"]
    },
    "review": {
        "machine_identifier": "review",
        "human_readable_name": "Review",
        "purpose": "Peer review of artifacts",
        "producer_skills": [],
        "consumer_skills": [],
        "canonical_storage_location": "<M_ID>/reviews/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "proposed", "completed", "archived"],
        "allowed_relationships": ["derived_from", "reviews", "evaluates"]
    },
    "evaluation": {
        "machine_identifier": "evaluation",
        "human_readable_name": "Evaluation",
        "purpose": "Assessment of implementation quality",
        "producer_skills": ["evaluate-implementation"],
        "consumer_skills": [],
        "canonical_storage_location": "<M_ID>/evaluations/<SPEC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "proposed", "completed", "archived"],
        "allowed_relationships": ["derived_from", "evaluates"]
    },
    "documentation": {
        "machine_identifier": "documentation",
        "human_readable_name": "Documentation",
        "purpose": "User and developer documentation",
        "producer_skills": [],
        "consumer_skills": [],
        "canonical_storage_location": "<M_ID>/documentation/<DOC_ID>.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type"],
        "optional_metadata": ["version"],
        "lifecycle_states": ["draft", "reviewed", "published", "archived"],
        "allowed_relationships": ["derived_from"]
    },
    "team-consolidation": {
        "machine_identifier": "team-consolidation",
        "human_readable_name": "Team Consolidation Report",
        "purpose": "Captures phase-boundary team commentary, dual recommendations, and consensus for SDD pipeline decisions",
        "producer_skills": ["manage-development"],
        "consumer_skills": ["manage-development", "review-implementation", "close-spec"],
        "canonical_storage_location": "<M_ID>/team_consolidations/<SPEC_ID>TC-{N}.md",
        "required_metadata": ["created_at", "updated_at", "artifact_identity", "artifact_type", "phase", "team_members"],
        "optional_metadata": ["primary_recommendation", "second_best_option", "consensus_count", "derived_from"],
        "lifecycle_states": ["draft", "proposed", "completed", "archived"],
        "allowed_relationships": ["derived_from", "reviews", "evaluates"]
    },
}

# Canonical type definitions for AEF artifact system
_ARTIFACT_TYPE_DEFINITIONS: Dict[str, CanonicalArtifactType] = {}
for key, value in _RAW_ARTIFACT_TYPE_DEFINITIONS.items():
    _ARTIFACT_TYPE_DEFINITIONS[key] = CanonicalArtifactType(**value)


def get_artifact_type(identifier: str) -> Optional[CanonicalArtifactType]:
    """Retrieves a canonical artifact type by its machine identifier."""
    for artifact_type in _ARTIFACT_TYPE_DEFINITIONS.values():
        if artifact_type.machine_identifier == identifier:
            return artifact_type
    return None


def get_all_artifact_types() -> List[CanonicalArtifactType]:
    """Returns a list of all defined canonical artifact types."""
    return list(_ARTIFACT_TYPE_DEFINITIONS.values())


def register_artifact_types(types: List[CanonicalArtifactType]):
    """Registers a list of artifact types. (Placeholder for future implementation)"""
    pass


def get_type_definition(name: str) -> Optional[Dict[str, Any]]:
    """Returns definition for an artifact type or None."""
    return _ARTIFACT_TYPE_DEFINITIONS.get(name)


def get_all_type_definitions() -> Dict[str, Dict[str, Any]]:
    """Returns all artifact type definitions."""
    return dict(_ARTIFACT_TYPE_DEFINITIONS)


__all__ = [
    "CanonicalArtifactType",
    "get_artifact_type",
    "get_all_artifact_types",
    "register_artifact_types",
    "get_type_definition",
    "get_all_type_definitions",
]
