---
id: SPEC-M9S1
type: specification
title: "AEF Core Artifact Infrastructure - Registry, Resolver, Validator, Types, Legacy Compatibility, Traceability"
milestone_id: M9
status: draft
derived_from:
  - M9
template_version: 1.3.0
---

# AEF Core Artifact Infrastructure - Registry, Resolver, Validator, Types, Legacy Compatibility, Traceability

#### Objective

Define the core artifact infrastructure that enables canonical artifact management across the AEF development platform. This specification establishes the registry for artifact types, the resolver for locating artifacts, the validator for metadata compliance, and the foundational types and legacy compatibility mechanisms that ensure consistent artifact handling across all AEF skills.

#### Followup Context

No prior specifications exist for M9. This is the first specification for this milestone and establishes the core artifact infrastructure foundation that subsequent specifications (M9S2-M9S4) will build upon.

#### Functional Requirements

##### FR-REGISTRY_INIT

* **Type**: Structured Schema Contract
* **Interface Contract**: `core/artifacts/registry.py` with `ArtifactRegistry` class containing:
  - `register_type(type_name: str, schema: Dict[str, Any], storage_rule: Dict[str, Any]) -> None`
  - `get_type(type_name: str) -> Optional[ArtifactTypeDefinition]`
  - `get_schema(type_name: str) -> Optional[Dict[str, Any]]`
  - `get_storage_rule(type_name: str) -> Optional[Dict[str, Any]]`
  - `list_types() -> List[str]`
* **Expected Behavior**: Registry initializes with built-in artifact types (specification, verification, test, milestone, skill). Each type includes metadata schema and storage rules. Registry provides singleton access via `get_registry()`.
* **Observable Boundary**: File `core/artifacts/registry.py` must exist and contain the `ArtifactRegistry` class with all defined methods implementing type registration and retrieval.

##### FR-VALIDATOR_INIT

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/validation.py` exposing `validate_metadata(artifact_path, schema?) -> Dict[str, Any]` and `validate_artifact(metadata) -> Dict[str, Any]`, with `bin/omp-verify-metadata` as the CLI entrypoint that calls the validation API directly.
* **Expected Behavior**: Validates YAML frontmatter structure, required fields (`id`, `type`, `milestone_id`), and type-specific requirements. Returns structured result with `valid`, `errors`, and `missing_fields`.
* **Observable Boundary**: Running `python bin/omp-verify-metadata milestones/M9/M9.md` must return exit code 0 for valid milestone files, exit code 1 for invalid files.

##### FR-RESOLVER_INIT

* **Observable Boundary**: Running `python -m core.artifacts.resolve --identity "SPEC-M9S1" --type "specification"` must return JSON with resolved artifact details or ambiguity error.

##### FR-TYPE_DEFS

* **Type**: Structured Schema Contract
* **Interface Contract**: `core/artifacts/types.py` with artifact type definitions.
* **Expected Behavior**: Defines canonical artifact types with their metadata schemas and storage rules. Includes serialization methods for type definitions.
* **Observable Boundary**: File `core/artifacts/types.py` must exist and define `CanonicalArtifactType` dataclass and `_ARTIFACT_TYPE_DEFINITIONS` with schemas for at least: specification, verification, test, milestone, skill.

##### FR-LEGACY_COMPAT

* **Type**: Filesystem State Contract
* **Interface Contract**: Legacy artifact resolution through `ARTIFACTS_BASE_DIR = "milestones"` and `LEGACY_ARTIFACT_MAPPINGS` in `core/artifacts/resolution.py`.
* **Expected Behavior**: Existing legacy artifacts remain readable through canonical resolver. New artifacts use canonical rules. Legacy artifacts can coexist with canonical artifacts.
* **Observable Boundary**: File `core/artifacts/resolution.py` must contain `LEGACY_ARTIFACT_MAPPINGS` dictionary and `_is_canonical_artifact()` function that detects canonical artifacts by frontmatter.

##### FR-TRACEABILITY

* **Type**: Structured Schema Contract
* **Interface Contract**: `core/artifacts/registry.py` relationship tracking.
* **Expected Behavior**: Tracks relationships between artifacts (specification → verification → test → implementation). Supports relationship types: derived_from, verifies, tests, implements, evaluates, reviews.
* **Observable Boundary**: Registry must support relationship storage and retrieval. Artifact resolution must include relationship context.

#### Non-Functional Requirements

##### NFR-STORAGE_MODEL

* **Constraint**: All artifacts stored in `milestones/` directory following pattern `{milestone_id}/{type}/{artifact_identity}.md`
* **Verification**: Directory structure must match expected storage model when artifacts are created via canonical creation protocol

##### NFR-SCHEMA_CONSTRAINTS

* **Constraint**: All metadata must be valid YAML with required keys: `id`, `type`, `milestone_id`. Specification types require `requirements` section. Verification types require `verification_items` section.
* **Verification**: `validate_metadata()` in `core/validation.py` must enforce schema constraints and return structured validation errors

##### NFR-RESOLUTION_PRIORITY

* **Constraint**: Artifact resolution prioritizes canonical artifacts over legacy artifacts. Ambiguous resolution surfaces error with available options.
* **Verification**: `resolve_artifact()` must return structured ambiguity error with matching artifact IDs and user instructions

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**
*   [ ] `core/artifacts/registry.py` — Core artifact type registry implementation
*   [ ] `core/artifacts/resolution.py` — Artifact resolution logic and legacy compatibility
*   [ ] `core/artifacts/resolve.py` — CLI wrapper for resolver
*   [ ] `core/artifacts/types.py` — Canonical artifact type definitions and schemas
*   [ ] `core/artifacts/metadata.py` — Metadata extraction and validation utilities
*   [ ] `core/validation.py` — Validation API and CLI behavior
*   [ ] `bin/omp-verify-metadata` — CLI entrypoint for metadata validation

**Denylist (Do NOT Touch):**
*   [ ] All `*.md` files in root and `milestones/` except new artifact creation
*   [ ] All `*.py` files in existing skills (bootstrap-project, generate-spec, etc.)
*   [ ] All `*.sh` test files in `tests/` directories
*   [ ] Configuration files outside `.omp/config.yml` scope

##### Affected Modules

* `core/artifacts/` - Core artifact system components: registry, resolver, types, metadata, errors, resolve CLI
* `core/validation.py` - Canonical validation API used by artifact system and CLI wrappers
* `bin/omp-verify-metadata` - CLI entrypoint invoking canonical validator
* `skills/` - Skills that produce/consume artifacts (bootstrap-project, generate-spec, etc.)

##### New Modules

N/A - Core modules already exist at `core/artifacts/` and `core/validation.py`

##### Removed Modules

N/A - No modules to be removed in this specification

##### Public Interfaces

* `ArtifactRegistry.register_type(type_name: str, schema: Dict[str, Any], storage_rule: Dict[str, Any]) -> None`
* `ArtifactRegistry.get_type(type_name: str) -> Optional[ArtifactTypeDefinition]`
* `ArtifactRegistry.get_schema(type_name: str) -> Optional[Dict[str, Any]]`
* `ArtifactRegistry.get_storage_rule(type_name: str) -> Optional[Dict[str, Any]]`
* `ArtifactRegistry.list_types() -> List[str]`
* `ArtifactRegistry.store_relationship(source_id: str, target_id: str, relationship_type: str, metadata: dict = None) -> bool`
* `ArtifactRegistry.get_relationships(source_id: str = None) -> list`
* `get_registry() -> ArtifactRegistry`
* `resolve_artifact(identity: Optional[str] = None, type: Optional[str] = None, metadata_filter: Optional[Dict[str, Any]] = None, strict: bool = False) -> Dict[str, Any]`
* `construct_canonical_path(milestone_id: str, artifact_type: str, artifact_id: str, extension: str = '.md') -> str`
* `validate_metadata(artifact_path: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`
* `validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]`

#### Interface Boundaries

##### Module Thresholds
* `bin/omp-verify-metadata` reads `.yml`/`.md` artifact files and validates against canonical schema via `core.validation.validate_metadata`
* `core/artifacts/registry.py` accepts type definitions and provides query methods for skill consumption
* `core/artifacts/resolution.py` provides artifact resolution API for skill integration
* `core/validation.py` provides canonical validation API consumed by resolver and CLI wrappers

##### Schema Contracts
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "milestone_id", "frontmatter"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^SPEC-M[0-9]+S[0-9]+$|^VER-M[0-9]+S[0-9]+V$|^TEST-M[0-9]+S[0-9]+T[0-9]+$|^M[0-9]+$|^SKILL-[a-zA-Z0-9_-]+$"
    },
    "type": {
      "type": "string",
      "enum": ["specification", "verification", "test", "milestone", "skill"]
    },
    "milestone_id": {
      "type": "string",
      "pattern": "^M[0-9]+$"
    },
    "frontmatter": {
      "type": "object",
      "required": ["type", "identity"],
      "properties": {
        "type": {"type": "string"},
        "identity": {"type": "string"}
      }
    }
  }
}
```

#### Implementation Tasks

1. Verify `core/artifacts/errors.py` implements custom error classes (`AmbiguousResolutionError`, `ValidationError`, `ArtifactNotFoundError`) `[FR-ERROR_TYPES]`
2. Verify `core/artifacts/types.py` defines canonical artifact types and schemas `[FR-TYPE_DEFS]`
3. Verify `core/artifacts/registry.py` implements `ArtifactRegistry` class with type registration and retrieval `[FR-REGISTRY_INIT]`
4. Verify `core/artifacts/resolution.py` implements `resolve_artifact()` function with legacy compatibility `[FR-RESOLVER_INIT]`
5. Verify `core/artifacts/metadata.py` with metadata extraction and validation utilities `[FR-METADATA_EXTRACT]`
6. Verify `core/validation.py` exposes `validate_metadata()` and `validate_artifact()` `[FR-VALIDATOR_INIT]`
7. Verify `bin/omp-verify-metadata` invokes canonical validator correctly `[FR-VALIDATOR_INIT]`
8. Implement integration tests in `tests/M9/S1/` for artifact registry, resolver, and validator functionality `[FR-TEST_INTEGRATION]`

##### FR-FIXTURE_VALIDATION

* **Type**: Fixture State Contract
* **Interface Contract**: Validation test fixtures in `tests/fixtures/synthetic_metadata_valid/` and `tests/fixtures/synthetic_metadata_invalid/` must conform to canonical artifact metadata schema.
* **Expected Behavior**: Valid fixture artifacts must contain all required metadata fields: `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`, and `metadata`. The `metadata` sub-object must contain `created_at`, `updated_at`, `artifact_identity`, and `artifact_type`. Invalid fixtures must be missing at least one required field or have malformed frontmatter.
* **Observable Boundary**: Running `python bin/omp-verify-metadata tests/fixtures/synthetic_metadata_valid/valid_artifact.md` must return exit code 0. Running `python bin/omp-verify-metadata tests/fixtures/synthetic_metadata_invalid/no_frontmatter.md` must return exit code 1.

#### Constraints

* This specification establishes core infrastructure only - it does not define project configuration rules (M9S2), skill behavioral contracts (M9S3), or pipeline integration (M9S4)
* The implementation must maintain backward compatibility with existing legacy artifacts while establishing canonical rules for new artifacts
* No skill-specific canonical path resolution implementations are permitted - all resolution must go through the canonical resolver
* The system must not automatically migrate existing legacy artifacts - legacy compatibility must be read-only
* Project isolation must be enforced through workspace boundaries, not filesystem permissions
* Validation test fixtures must conform to canonical artifact metadata schema with all required fields present

#### Assumptions

* The `milestones/` directory serves as the primary artifact storage location
* YAML frontmatter is the canonical format for artifact metadata
* Artifacts are primarily Markdown files (.md extension) with embedded YAML frontmatter
* The artifact registry can be initialized with standard Python dictionaries and dataclasses
* Legacy artifacts follow predictable filename patterns that can be mapped to artifact identities

#### Acceptance Criteria

* [ ] Artifact registry initializes with all canonical artifact types (specification, verification, test, milestone, skill) each with defined schemas and storage rules `[FR-REGISTRY_INIT]`
* [ ] Validation API correctly validates canonical artifact frontmatter against schema, rejecting invalid artifacts with structured error messages `[FR-VALIDATOR_INIT]`
* [ ] Resolver correctly resolves artifacts by identity, type, or metadata filters using canonical storage model `[FR-RESOLVER_INIT]`
* [ ] Legacy artifacts remain readable through canonical resolver using legacy mappings `[FR-LEGACY_COMPAT]`
* [ ] Artifact system tracks and provides relationships between related artifacts (specification → verification → test → implementation) `[FR-TRACEABILITY]`
* [ ] All core artifact infrastructure components are implemented as modules with clear public interfaces for skill consumption `[FR-TYPE_DEFS]`

#### Next Steps

Run `/generate-verification` to create the verification protocol for this core artifact infrastructure specification. This will establish the observable behaviors and validation criteria required to verify the implementation meets the specification's functional and non-functional requirements.

#### Followup Context

This specification builds on the milestone M9's objective to integrate the canonical artifact architecture into the AEF development infrastructure. It focuses on the core infrastructure components (registry, resolver, validator, types, legacy compatibility, and traceability) that will enable consistent artifact management across all AEF skills. This specification must be completed before proceeding with M9S2 (project configuration), M9S3 (skill integration), and M9S4 (pipeline integration).

This updated specification corrects implementation path references from `src/core/artifacts/...` and `src/omp_cli/...` to the actual canonical locations: `core/artifacts/...`, `core/validation.py`, and `bin/omp-verify-metadata`.

#### User Approval

- [x] Approved for implementation by user