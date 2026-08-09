import os
import yaml
from typing import Dict, Any, Optional, List

# Assuming types.py and metadata.py are in the same package directory
from core.artifacts.types import CanonicalArtifactType, get_artifact_type
from core.artifacts.metadata import parse_metadata, validate_metadata, METADATA_SERIALIZATION_FORMAT

# Define the base directory for artifacts, relative to the project root
ARTIFACTS_BASE_DIR = "milestones"
LEGACY_ARTIFACT_MAPPINGS = {
    # Example mapping: "M5S1I1.md": "investigation"
    # This would need to be populated based on known legacy patterns.
}

class ArtifactResolutionError(Exception):
    """Custom exception for artifact resolution issues."""
    pass

class AmbiguousArtifactError(ArtifactResolutionError):
    """Raised when artifact type cannot be determined unambiguously."""
    pass

class MissingMetadataError(ArtifactResolutionError):
    """Raised when required metadata is missing."""
    pass

class InvalidMetadataError(ArtifactResolutionError):
    """Raised when metadata is invalid or malformed."""
    pass

def construct_canonical_path(milestone_id: str, artifact_type: str, artifact_id: str, extension: str = '.md') -> str:
    """Constructs the canonical path for an artifact."""
    # Fetch artifact type definition to get storage location pattern
    artifact_type_def = get_artifact_type(artifact_type)
    if not artifact_type_def:
        raise ArtifactResolutionError(f"Unknown artifact type: {artifact_type}")

    # Example: milestones/<M_ID>/specifications/<SPEC_ID>.md
    # This needs to be dynamic based on artifact_type_def.canonical_storage_location
    # For simplicity, hardcoding common patterns for now.
    storage_template = artifact_type_def.canonical_storage_location
    
    # Basic template replacement - needs more robust handling for various patterns.
    # If storage_template is like 'milestones/<M_ID>/specifications/<SPEC_ID>.md', 
    # we need to substitute M_ID, SPEC_ID, and potentially others.
    
    # Simplified path construction based on common patterns for now:
    if artifact_type in ['specification', 'verification', 'investigation', 'implementation', 'evaluation', 'review', 'audit']:
        type_dir = artifact_type + 's' # e.g., specifications, verifications
        return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, type_dir, f"{artifact_id}{extension}")
    elif artifact_type == 'milestone':
        return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, f"{milestone_id}{extension}")
    else:
        # Fallback for unknown types or custom locations
        return os.path.join(ARTIFACTS_BASE_DIR, milestone_id, artifact_type + 's', f"{artifact_id}{extension}")


def resolve_artifact_type_from_metadata(artifact_path: str) -> Optional[Dict[str, Any]]:
    """Attempts to resolve artifact type and metadata from file content."""
    try:
        with open(artifact_path, 'r') as f:
            content = f.read()
        
        # Check for YAML frontmatter
        parts = content.split('---\n', 2)
        if len(parts) < 2:
            return None # No frontmatter found
            
        metadata_str = parts[1]
        metadata = yaml.safe_load(metadata_str)
        
        if not isinstance(metadata, dict):
            raise InvalidMetadataError("Metadata is not a valid dictionary.")
            
        # Validate required fields
        artifact_type_identifier = metadata.get('type')
        if not artifact_type_identifier:
            raise MissingMetadataError("Artifact type is missing in metadata.")
            
        # Fetch artifact type definition to get required metadata fields
        # This part needs to be connected to the actual registry in types.py
        # For now, we assume basic validation happens later or is skipped if type is unknown.
        
        return metadata
        
    except FileNotFoundError:
        raise ArtifactResolutionError(f"File not found: {artifact_path}")
    except yaml.YAMLError:
        raise InvalidMetadataError(f"Failed to parse YAML metadata in {artifact_path}.")
    except Exception as e:
        raise ArtifactResolutionError(f"Error resolving metadata from {artifact_path}: {e}")

def resolve_artifact_type_from_directory(artifact_path: str) -> Optional[str]:
    """Attempts to infer artifact type from directory structure."""
    # Example: Check if path is within 'specifications/', 'verifications/', etc. directories
    parts = artifact_path.split(os.sep)
    if len(parts) >= 3 and parts[-3] == ARTIFACTS_BASE_DIR:
        potential_type_dir = parts[-2]
        # Map directory names to canonical type identifiers
        type_mapping = {
            'specifications': 'specification',
            'verifications': 'verification',
            'tests': 'test_set',
            'investigations': 'investigation',
            'implementations': 'implementation',
            'evaluations': 'evaluation',
            'reviews': 'review',
            'audits': 'audit',
            # Milestone is handled separately, usually by direct path to M<ID>.md
        }
        return type_mapping.get(potential_type_dir)
    return None

def resolve_artifact_type_from_legacy_mapping(artifact_path: str) -> Optional[str]:
    """Attempts to infer artifact type from legacy filename mappings."""
    # This requires a defined mapping from legacy filenames to canonical types.
    # Example: if artifact_path ends with 'M5S1I1.md', map to 'investigation'
    filename = os.path.basename(artifact_path)
    return LEGACY_ARTIFACT_MAPPINGS.get(filename)

def resolve_artifact_type_from_heuristic(artifact_path: str) -> Optional[str]:
    """Attempts to infer artifact type using filename heuristics as a last resort."""
    # Very basic heuristic: look for common prefixes/suffixes
    filename = os.path.basename(artifact_path).lower()
    if filename.startswith('spec-') or filename.startswith('m<digit>s<digit>-'): # Example heuristic
        return 'specification'
    # Add more heuristics as needed
    return None


def resolve_artifact(artifact_path: str) -> Dict[str, Any]:
    """Resolves an artifact's type, metadata, and other details."""
    # 1. Resolve from metadata
    try:
        metadata = resolve_artifact_type_from_metadata(artifact_path)
        if metadata:
            artifact_type_id = metadata.get('type')
            if not artifact_type_id:
                raise MissingMetadataError("Artifact type missing in metadata.")
            
            artifact_type_def = get_artifact_type(artifact_type_id)
            if not artifact_type_def:
                raise ArtifactResolutionError(f"Unknown artifact type '{artifact_type_id}' found in metadata.")
            
            if not validate_metadata(metadata, artifact_type_def):
                raise InvalidMetadataError(f"Metadata validation failed for {artifact_path}.")

            # Construct canonical path based on resolved info
            milestone_id = metadata.get('milestone_id')
            if not milestone_id:
                 raise MissingMetadataError(f"Milestone ID missing in metadata for {artifact_path}.")
            canonical_path = construct_canonical_path(milestone_id, artifact_type_id, metadata.get('id'))
            
            return {
                'resolved_type': artifact_type_id,
                'metadata': metadata,
                'canonical_path': canonical_path,
                'source': 'metadata'
            }

    except (ArtifactResolutionError, InvalidMetadataError, MissingMetadataError) as e:
        print(f"Metadata resolution failed for {artifact_path}: {e}")
        # Proceed to next resolution step if metadata resolution failed critically
        pass

    # 2. Resolve from directory
    resolved_type_from_dir = resolve_artifact_type_from_directory(artifact_path)
    if resolved_type_from_dir:
        artifact_type_def = get_artifact_type(resolved_type_from_dir)
        if artifact_type_def:
            # Cannot fully validate without metadata, but can infer type and location
            # In a real system, this would trigger a prompt for metadata or assume default schema
            return {
                'resolved_type': resolved_type_from_dir,
                'metadata': {},
                'canonical_path': construct_canonical_path(os.path.basename(os.path.dirname(os.path.dirname(artifact_path)))), # Simplified milestone_id derivation
                'source': 'directory'
            }
        else:
            print(f"Warning: Directory type '{resolved_type_from_dir}' for {artifact_path} is not recognized.")

    # 3. Resolve from legacy mapping
    resolved_type_from_legacy = resolve_artifact_type_from_legacy_mapping(artifact_path)
    if resolved_type_from_legacy:
        # Legacy mapping implies potential ambiguity or need for further checks
        return {
            'resolved_type': resolved_type_from_legacy,
            'metadata': {},
            'canonical_path': None, # Path might not be canonical yet
            'source': 'legacy_mapping'
        }

    # 4. Resolve from heuristic
    resolved_type_from_heuristic = resolve_artifact_type_from_heuristic(artifact_path)
    if resolved_type_from_heuristic:
        # Heuristics are the least reliable, used as a final fallback
        return {
            'resolved_type': resolved_type_from_heuristic,
            'metadata': {},
            'canonical_path': None, # Path might not be canonical yet
            'source': 'heuristic'
        }

    # If no resolution possible
    raise ArtifactResolutionError(f"Could not resolve artifact type for: {artifact_path}")

# Example of how path utilities might be used within resolution:
# if __name__ == "__main__":
#     # Dummy setup for demonstration
#     # In a real scenario, types would be loaded from types.py
#     from core.artifacts.types import CanonicalArtifactType, register_artifact_types
#     SPEC_TYPE = CanonicalArtifactType(
#         machine_identifier='specification',
#         human_readable_name='Specification',
#         purpose='Details requirements.',
#         producer_skills=['generate-spec'],
#         consumer_skills=['implement-specification'],
#         canonical_storage_location='milestones/<M_ID>/specifications/<SPEC_ID>.md',
#         required_metadata=['id', 'type', 'title', 'milestone_id', 'status'],
#         optional_metadata=[],
#         lifecycle_states=['proposed', 'approved'],
#         allowed_relationships=['derived_from', 'supersedes']
#     )
#     register_artifact_types([SPEC_TYPE])
# 
#     # Simulate a file with valid metadata
#     sample_file_content_valid = """
# ---
# id: SPEC-001
# type: specification
# title: Test Spec
# milestone_id: M9
# status: proposed
# derived_from:
#   - INV-001
# ---
# Content...
# """
#     # Create a dummy file for testing
#     with open("dummy_spec.md", "w") as f:
#         f.write(sample_file_content_valid)
#     
#     try:
#         resolved_info = resolve_artifact("dummy_spec.md")
#         print(f"Successfully resolved: {resolved_info}")
#         
#         # Test canonical path construction
#         canonical_path = construct_canonical_path("M9", "specification", "SPEC-001")
#         print(f"Constructed canonical path: {canonical_path}")
#         
#     except ArtifactResolutionError as e:
#         print(f"Resolution failed: {e}")
#     finally:
#         # Clean up dummy file
#         if os.path.exists("dummy_spec.md"):
#             os.remove("dummy_spec.md")
# 
