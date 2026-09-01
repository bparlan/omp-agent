---
id: SPEC-M9S3C
type: spec
title: "M9S3 Implementation Specification - Healthcenter Skill"
milestone_id: M9
status: draft
derived_from:
  - MILESTONE-M9
template_version: 1.0.0
---

# M9S3 Implementation Specification

## Overview
This document defines the implementation specification for M9S3: Healthcenter Skill - Canonical Artifact Adoption. It translates the specification into detailed implementation requirements with clear, observable interface contracts.

## Implementation Interface Contracts

### 1. Healthcenter CLI Interface (`skills/healthcenter/healthcenter.py`)

**Public CLI API:**
```bash
# Process all skills in skills/ directory
skills/healthcenter/healthcenter.py --all

# Process single skill by name  
skills/healthcenter/healthcenter.py --skill skill_name

# Fix compliance issues in single skill
skills/healthcenter/healthcenter.py --skill skill_name --fix

# Show help
skills/healthcenter/healthcenter.py --help
```

**Function Signatures:**
- `process_skill_batch(skills_list: List[Tuple[str, str]]) -> List[Dict]`
- `create_health_artifact(skill_name: str, skill_path: str) -> Optional[str]`
- `fix_skill_compliance(skill_path: str) -> Dict[str, Any]`

**Return Contract:**
- Success: `{"status": "success", "artifact_id": "HC-<skill_name>"}`
- Failure: `{"status": "failed", "artifact_id": null}`

### 2. Artifact Creation (`core/artifacts/creation.py`)

**Public Functions:**
- `create_canonical_artifact(source_path: str, artifact_type: str, metadata: Dict) -> str`
- `create_health_check_artifact(skill_metadata: Dict, skill_path: str) -> str`

**Function Contract:**
```python
def create_canonical_artifact(
    source_path: str, 
    artifact_type: str, 
    metadata: Dict[str, Any]
) -> str:
    """Creates a canonical artifact with validation and registry integration.
    
    Returns: Artifact ID (format: M9-<type>-<skill_name>)
    Raises: ValueError if metadata validation fails
    """
```

### 3. Artifact Registry (`core/artifacts/registry.py`)

**Public Interface:**
```python
def store_relationship(
    source_id: str, 
    target_id: str, 
    type: str, 
    metadata: Dict[str, Any]
) -> bool

def get_relationships() -> List[Dict[str, Any]]
```

**Method Contracts:**
- `store_relationship()`: Returns True on successful storage
- `get_relationships()`: Returns all stored relationships with timestamp metadata

### 4. Artifact Types Registry (`core/artifacts/types.py`)

**Public Functions:**
- `get_artifact_type(artifact_type: str) -> Optional[CanonicalArtifactType]`
- `register_artifact_type(type_definition: Dict[str, Any]) -> bool`

**Function Contract:**
```python
def get_artifact_type(artifact_type: str) -> Optional[CanonicalArtifactType]:
    """Retrieves the canonical type definition for a given type identifier.
    
    Args:
        artifact_type: Must match one of the canonical types ("specification", "verification", "test", "implementation", "milestone", "review", "evaluation", "documentation", "team-consolidation", "operations-consolidation", "health-check", "project-config")
    
    Returns:
        CanonicalArtifactType object or None if type not registered
    """
```

### 5. Validation (`core/validation.py`)

**Public Functions:**
- `validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]`
- `validate_metadata(artifact_path: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`

**Return Contract:**
```python
def validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Validates artifact metadata against canonical contracts.
    
    Returns: {"valid": bool, "errors": List[str], "missing_fields": List[str]}
    
    Validation Rules:
    - Required fields: ["id", "type", "title", "milestone_id", "status", "derived_from", "template_version", "metadata"]
    - Field "type" must be in canonical types
    - Field "validation_score" must be number between 0-100
    - Field "metadata" must be dict with keys ["created_at", "updated_at", "artifact_identity", "artifact_type"]
    """
```

### 6. Healthcenter Module (`skills/healthcenter/healthcenter.py`)

**Public Functions:**
- `process_skill_batch(skills_list: list) -> list`
- `create_health_artifact(skill_name: str, skill_path: str) -> str`
- `fix_skill_compliance(skill_path: str) -> dict`

**Function Contract:**
```python
def create_health_artifact(skill_name: str, skill_path: str) -> str:
    """Creates a health-check artifact for a skill.
    
    Args:
        skill_name: Name of the skill directory
        skill_path: Full path to skill directory containing SKILL.md
    
    Returns:
        Artifact ID string if successful, None otherwise
    
    Precondition:
        SKILL.md file must exist in skill_path directory
        SKILL.md must have valid YAML frontmatter with "id" field
    
    Postcondition:
        Creates artifact with id format "HC-<skill_name>"
        Stores artifact in milestones/M9/ directory
        Registers artifact in registry with "derived_from" relationship
    """
```

## Interface Dependencies

### Required Integration Points
1. **Core Artifact System**: All artifact creation must use `core/artifacts/creation.py`
2. **Validation Layer**: Validation must use `core/validation.py` 
3. **Registry System**: Relationships must use `core/artifacts/registry.py`
4. **Type System**: Artifact types must use `core/artifacts/types.py`

### External Interfaces
- **Filesystem**: Reads SKILL.md files from skills/<skill_name>/ directory
- **Standard I/O**: Prints status messages to stdout, errors to stderr
- **Exit Codes**: Returns 0 for success, 1 for failures

## Implementation Contracts

### CLI Contract (`healthcenter.py`)
```bash
skills/healthcenter/healthcenter.py --all
# Output: Success/failure summary with counts
# Exit: 0 if any skills processed, 1 otherwise

skills/healthcenter/healthcenter.py --skill skill_name
# Output: "SUCCESS: Artifact HC-skill_name created for skill skill_name"
# Exit: 0 on success, 1 on failure

skills/healthcenter/healthcenter.py --skill skill_name --fix
# Output: Fix results with counts of fixed items, errors, recommendations
# Exit: 0 on successful fix processing
```

### Function Contract (`create_health_artifact`)
```python
# Input: skill_name="example_skill", skill_path="/path/to/skills/example_skill"
# Output: artifact_id="HC-example_skill"
# Side effects:
# - Creates file: /path/to/milestones/M9/M9-health-check-example_skill.md
# - Registers relationship in artifact registry
```

## Implementation Rules

### Coding Standards
- Type hints required for all public functions
- Comprehensive docstrings with Args/Returns/Examples
- Error handling with meaningful error messages
- Logging of key operations for debugging

### Testing Requirements
- Unit tests for all public functions with deterministic outputs
- CLI integration tests for all command-line interfaces
- Mock-based tests for external dependencies (filesystem, registry)
- Performance tests for batch processing operations

### Quality Gates
- All tests must pass (exit code 0)
- 100% code coverage for public interfaces
- No hardcoded paths in module interfaces
- Comprehensive error documentation
