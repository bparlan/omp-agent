import yaml
from typing import Dict, Any, Optional, List
from core.artifacts.types import CanonicalArtifactType

METADATA_SERIALIZATION_FORMAT = 'yaml'

def parse_metadata(content: str) -> Dict[str, Any]:
    """Parses metadata from content, assuming YAML frontmatter."""
    try:
        # YAML frontmatter is typically delimited by '---'
        parts = content.split('---\n', 2)
        if len(parts) < 2:
            # No frontmatter found or malformed
            return {}
        metadata_str = parts[1]
        metadata = yaml.safe_load(metadata_str)
        return metadata if isinstance(metadata, dict) else {}
    except yaml.YAMLError:
        # Handle potential YAML parsing errors
        print("Warning: Failed to parse YAML metadata.")
        return {}

def validate_metadata(metadata: Dict[str, Any], artifact_type: Optional[CanonicalArtifactType] = None) -> bool:
    """Validates metadata against a schema and required fields."""
    if not metadata:
        print("Warning: Metadata is empty.")
        # Depending on requirements, empty metadata might be valid or not.
        # For now, we'll allow it but warn.
        return True

    # Check for required fields based on artifact type (if provided)
    if artifact_type:
        for required_field in artifact_type.required_metadata:
            if required_field not in metadata or metadata[required_field] is None:
                print(f"Error: Missing required metadata field '{required_field}' for artifact type '{artifact_type.machine_identifier}'.")
                return False

    # Basic type checks for common fields (can be expanded)
    if 'id' in metadata and not isinstance(metadata['id'], str):
        print("Error: Metadata field 'id' must be a string.")
        return False
    if 'type' in metadata and not isinstance(metadata['type'], str):
        print("Error: Metadata field 'type' must be a string.")
        return False
    if 'milestone_id' in metadata and not isinstance(metadata['milestone_id'], str):
        print("Error: Metadata field 'milestone_id' must be a string.")
        return False
    if 'status' in metadata and not isinstance(metadata['status'], str):
        print("Error: Metadata field 'status' must be a string.")
        return False

    return True

def get_metadata_from_file(file_path: str) -> Dict[str, Any]:
    """Reads a file and extracts metadata from its YAML frontmatter."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return parse_metadata(content)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
        return {}
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return {}

# Example usage (conceptual):
# if __name__ == "__main__":
#     sample_content_with_metadata = """
# ---
# id: SPEC-001
# type: specification
# title: Define Canonical Artifact Model
# milestone_id: M9
# status: proposed
# derived_from:
#   - INV-001
# template_version: \"1.1.0\"
# producer_skill: generate-spec
# ---
# # Actual artifact content starts here...
# This is the content of the specification.
# """
#     metadata = parse_metadata(sample_content_with_metadata)
#     print(f"Parsed Metadata: {metadata}")
# 
#     # Conceptual: In a real scenario, we'd fetch the artifact type definition
#     # For now, we'll check some common fields without strict type validation.
#     is_valid = validate_metadata(metadata)
#     print(f"Metadata valid: {is_valid}")
