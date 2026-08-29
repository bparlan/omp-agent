---
id: SPEC-M9S2
type: specification
title: "Project Configuration — .omp/config.yml Schema, Validation, and Canonical Artifact Registration"
milestone_id: M9
status: draft
derived_from:
  - M9
template_version: 1.3.0
---

# Project Configuration — `.omp/config.yml` Schema, Validation, and Canonical Artifact Registration

#### Objective

Define the project-scoped configuration contract for AEF. This specification establishes the `.omp/config.yml` schema, validation rules, canonical artifact registration, and the required interfaces for reading, writing, and validating project configuration. It ensures `bootstrap-project` and other skills consume a single canonical config model rather than inventing competing schemas.

#### Followup Context

M9S1 established the canonical artifact infrastructure: registry, resolver, validator, types, legacy compatibility, and traceability. M9S2 builds directly on that foundation by registering `.omp/config.yml` as a canonical artifact and requiring that its schema and validation go through the canonical metadata validator, not through ad hoc skill logic.

---

#### Functional Requirements

##### FR-PROJECT_CONFIG_SCHEMA

* **Type**: Structured Schema Contract
* **Interface Contract**: `.omp/config.yml` must conform to a canonical schema registered in the artifact registry under the `project-configuration` artifact type.
* **Expected Behavior**: The schema requires `project_id`, `project_slug`, and `mode`. Supported `mode` values are `framework` and `application`. Additional modes are not permitted unless explicitly added by a downstream specification.
* **Observable Boundary**: A valid `.omp/config.yml` file at project root must validate successfully through `core/config.py` and the canonical metadata validator. An invalid file must return structured validation errors with missing or malformed fields.

##### FR-PROJECT_CONFIG_LOAD

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/config.py` exposes `load_project_config(config_path=None) -> Dict[str, Any]`.
* **Expected Behavior**: Locate the project root by discovering `.omp/config.yml` or `.git`. Load and return the parsed YAML config. If the file is missing, raise `FileNotFoundError` with a clear message.
* **Observable Boundary**: Calling `load_project_config()` from within a project root returns a dict containing at least `project_id`, `project_slug`, and `mode`. Calling it outside any project root raises `FileNotFoundError`.

##### FR-PROJECT_CONFIG_VALIDATE

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/config.py` exposes `validate_config(config: Dict[str, Any]) -> bool`.
* **Expected Behavior**: Validate the config dict against the canonical schema. Return `True` if valid; return `False` and emit structured validation errors if invalid.
* **Observable Boundary**: `validate_config()` returns `False` for missing `project_id`, missing `mode`, or unsupported `mode` values such as `test`. It returns `True` for valid minimal configs.

##### FR-PROJECT_CONFIG_SAVE

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/config.py` exposes `save_project_config(config: Dict[str, Any], config_path=None) -> None`.
* **Expected Behavior**: Write the config dict to `.omp/config.yml` as YAML with block-style formatting and stable key order. Create the `.omp` directory if it does not exist.
* **Observable Boundary**: After `save_project_config()`, the written file exists, is valid YAML, and passes `load_project_config()` and `validate_config()` round-trip.

##### FR-PROJECT_CONFIG_DEFAULT

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/config.py` exposes `create_default_config(project_id: str, project_slug: str, mode: str) -> Dict[str, Any]`.
* **Expected Behavior**: Return a canonical default config dict with the provided values and no extraneous keys.
* **Observable Boundary**: The returned dict contains exactly `project_id`, `project_slug`, and `mode`, and passes `validate_config()`.

##### FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION

* **Type**: Structured Schema Contract
* **Interface Contract**: `core/artifacts/registry.py` must include a registered artifact type for `.omp/config.yml` under the canonical type identity `project-configuration`.
* **Expected Behavior**: The registry exposes the config artifact type with its schema and storage rule. `get_type('project-configuration')` returns a definition whose schema matches `CONFIG_SCHEMA`.
* **Observable Boundary**: Reading the registry type definition for `project-configuration` returns a schema object whose `required` list includes `project_id`, `project_slug`, and `mode`, and whose `properties.mode.enum` contains exactly `framework` and `application`.

##### FR-PROJECT_CONFIG_CANONICAL_VALIDATION

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/validation.py` `validate_metadata(artifact_path, schema?)` and `validate_artifact(metadata)` must accept `.omp/config.yml` artifacts.
* **Expected Behavior**: The canonical validator treats `.omp/config.yml` as a canonical artifact when its metadata includes `type: project-configuration`. It validates both frontmatter metadata and embedded config content against the registered schema.
* **Observable Boundary**: Running `python bin/omp-verify-metadata .omp/config.yml` on a valid config returns exit code 0. Running it on an invalid config returns exit code 1 with structured errors.

##### FR-PROJECT_CONFIG_RESOLUTION

* **Type**: Direct Integration Contract
* **Interface Contract**: `core/artifacts/resolution.py` `resolve_artifact(identity=None, type=None, metadata_filter=None, strict=False)` must resolve `.omp/config.yml` by identity `CONFIG-{project_slug}` or type `project-configuration`.
* **Expected Behavior**: Resolution locates `.omp/config.yml` in the discovered project root and returns its canonical identity, path, and metadata.
* **Observable Boundary**: `resolve_artifact(type='project-configuration')` from within a project root returns a resolution result with `path` ending in `.omp/config.yml`.

##### FR-PROJECT_CONFIG_MODE_ENFORCEMENT

* **Type**: Filesystem State Contract
* **Interface Contract**: `bootstrap-project` must read `.omp/config.yml` before generating project files. `mode: application` suppresses AEF-internal architectural documents. `mode: framework` allows them.
* **Expected Behavior**: Bootstrap behavior is determined by the config file, not by assumptions. The observable outcome is the set of files created or omitted.
* **Observable Boundary**: Running `bootstrap-project` in application mode does not create `FRAMEWORK.md`, `PLAYBOOK.md`, or `DATA.md` unless the spec or config explicitly requires them.

#### Non-Functional Requirements

##### NFR-CONFIG_FILE_LOCATION

* **Constraint**: The canonical project config path is `.omp/config.yml` at the project root.
* **Verification**: `load_project_config()` discovers this path automatically. Skills must not hardcode alternative config paths.

##### NFR-CONFIG_SCHEMA_STABILITY

* **Constraint**: The config schema is backward-compatible within a mode. New optional fields may be added; required fields and enum values must not change without a spec update.
* **Verification**: Valid configs from prior minor versions must continue to validate.

##### NFR-CONFIG_ARTIFACT_REGISTRATION

* **Constraint**: `.omp/config.yml` is a canonical artifact. It must be created, validated, and resolved through the canonical artifact system.
* **Verification**: Artifact registry contains `project-configuration` type. Resolver can locate the config artifact. Validator can validate it.

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**
* `core/config.py` — Project configuration loading, validation, and persistence
* `core/artifacts/registry.py` — Register `project-configuration` artifact type
* `core/artifacts/resolution.py` — Resolution for `.omp/config.yml`
* `core/artifacts/types.py` — Add `project-configuration` type definition
* `core/validation.py` — Ensure validator accepts config artifacts
* `bin/omp-verify-metadata` — CLI entrypoint for metadata validation
* `bin/bootstrap-project` — Mode-aware bootstrapping behavior
* `skills/bootstrap-project/SKILL.md` — Behavioral contract updates

**Denylist (Do NOT Touch):**
* All `*.md` files in root and `milestones/` except new artifact creation
* All `*.py` files in unrelated skills
* All `*.sh` test files in `tests/` directories
* Configuration files outside `.omp/config.yml` scope

##### Affected Modules

* `core/config.py` - Canonical project configuration API
* `core/artifacts/registry.py` - Artifact type registration for `project-configuration`
* `core/artifacts/resolution.py` - Config artifact resolution
* `core/artifacts/types.py` - Config artifact type definition
* `core/validation.py` - Canonical validation API for config artifacts
* `bin/omp-verify-metadata` - CLI validation entrypoint
* `bin/bootstrap-project` - Mode-aware bootstrap behavior
* `skills/bootstrap-project/SKILL.md` - Skill behavioral contract

##### New Modules

N/A - Core modules already exist at `core/config.py` and related artifact infrastructure.

##### Removed Modules

N/A - No modules to be removed in this specification.

##### Public Interfaces

* `load_project_config(config_path: Optional[str] = None) -> Dict[str, Any]`
* `validate_config(config: Dict[str, Any]) -> bool`
* `save_project_config(config: Dict[str, Any], config_path: Optional[str] = None) -> None`
* `create_default_config(project_id: str, project_slug: str, mode: str) -> Dict[str, Any]`
* `ArtifactRegistry.register_type('project-configuration', schema, storage_rule)`
* `ArtifactRegistry.get_type('project-configuration') -> ArtifactTypeDefinition`
* `resolve_artifact(type='project-configuration') -> Dict[str, Any]`
* `validate_metadata('.omp/config.yml') -> Dict[str, Any]`

#### Interface Boundaries

##### Module Thresholds
* `core/config.py` is the single source of truth for `.omp/config.yml` schema and validation.
* `core/artifacts/registry.py` registers `project-configuration` as a canonical artifact type.
* `core/artifacts/resolution.py` resolves `.omp/config.yml` through canonical artifact identity.
* `core/validation.py` validates config artifacts via canonical metadata contract.
* `bin/bootstrap-project` reads `.omp/config.yml` to determine mode; it does not invent schema rules.

##### Schema Contracts

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["project_id", "project_slug", "mode"],
  "properties": {
    "project_id": {
      "type": "string",
      "minLength": 1
    },
    "project_slug": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9-]*[a-z0-9]$"
    },
    "mode": {
      "type": "string",
      "enum": ["framework", "application"]
    }
  }
}
```

#### Implementation Tasks

1. Verify `core/config.py` implements `load_project_config()`, `validate_config()`, `save_project_config()`, and `create_default_config()` with the canonical schema `[FR-PROJECT_CONFIG_SCHEMA, FR-PROJECT_CONFIG_LOAD, FR-PROJECT_CONFIG_VALIDATE, FR-PROJECT_CONFIG_SAVE, FR-PROJECT_CONFIG_DEFAULT]`
2. Verify `core/artifacts/types.py` defines `project-configuration` artifact type with schema and storage rules `[FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION]`
3. Verify `core/artifacts/registry.py` registers `project-configuration` type and exposes it via `get_type()` `[FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION]`
4. Verify `core/validation.py` validates `.omp/config.yml` artifacts through canonical metadata contract `[FR-PROJECT_CONFIG_CANONICAL_VALIDATION]`
5. Verify `core/artifacts/resolution.py` resolves `.omp/config.yml` by identity or type `[FR-PROJECT_CONFIG_RESOLUTION]`
6. Verify `bin/bootstrap-project` reads `.omp/config.yml` and applies mode-aware behavior without inventing schema rules `[FR-PROJECT_CONFIG_MODE_ENFORCEMENT]`
7. Implement integration tests in `tests/M9/S2/` for config schema validation, loading, saving, artifact registration, and resolution `[FR-TEST_INTEGRATION]`

##### FR-FIXTURE_VALIDATION

* **Type**: Fixture State Contract
* **Interface Contract**: Validation test fixtures in `tests/fixtures/synthetic_config_valid/` and `tests/fixtures/synthetic_config_invalid/` must conform to the canonical `.omp/config.yml` schema.
* **Expected Behavior**: Valid fixture configs contain all required fields with supported enum values. Invalid fixtures are missing required fields or contain unsupported `mode` values.
* **Observable Boundary**: `python bin/omp-verify-metadata tests/fixtures/synthetic_config_valid/config.yml` returns exit code 0. `python bin/omp-verify-metadata tests/fixtures/synthetic_config_invalid/bad_mode.yml` returns exit code 1.

#### Constraints

* `.omp/config.yml` is a canonical artifact. Its schema is validated by the canonical metadata validator, not by `bootstrap-project` itself.
* No skill may invent additional required config fields or enum values without a specification update.
* `bootstrap-project` must not generate AEF-internal architectural documents in application mode unless explicitly required by config or specification.
* The config file location is fixed at `.omp/config.yml` at the project root. Alternative paths are not permitted.
* Supported modes are exactly `framework` and `application` for this specification.

#### Assumptions

* The `milestones/` directory serves as the primary artifact storage location.
* YAML frontmatter is the canonical format for artifact metadata.
* `.omp/config.yml` is primarily a YAML file with embedded YAML frontmatter when treated as a canonical artifact.
* The artifact registry can be initialized with standard Python dictionaries and dataclasses.
* Existing `core/config.py` implements the required config API and schema.

#### Acceptance Criteria

* [ ] `.omp/config.yml` schema requires `project_id`, `project_slug`, and `mode`, with `mode` limited to `framework` and `application` `[FR-PROJECT_CONFIG_SCHEMA]`
* [ ] `load_project_config()` discovers `.omp/config.yml` at project root and returns a parsed dict `[FR-PROJECT_CONFIG_LOAD]`
* [ ] `validate_config()` returns `False` for invalid configs and structured errors for missing/invalid fields `[FR-PROJECT_CONFIG_VALIDATE]`
* [ ] `save_project_config()` writes valid YAML to `.omp/config.yml` and round-trips through load/validate `[FR-PROJECT_CONFIG_SAVE]`
* [ ] `create_default_config()` returns a valid default config dict `[FR-PROJECT_CONFIG_DEFAULT]`
* [ ] Artifact registry registers `project-configuration` type with schema and storage rules `[FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION]`
* [ ] Canonical validator accepts `.omp/config.yml` artifacts and returns exit code 0 for valid, 1 for invalid `[FR-PROJECT_CONFIG_CANONICAL_VALIDATION]`
* [ ] Resolver locates `.omp/config.yml` by type or canonical identity `[FR-PROJECT_CONFIG_RESOLUTION]`
* [ ] `bootstrap-project` applies mode-aware behavior based on `.omp/config.yml` without inventing schema rules `[FR-PROJECT_CONFIG_MODE_ENFORCEMENT]`

#### Next Steps

Run `/generate-verification` to create the verification protocol for this project configuration specification. This will establish the observable behaviors and validation criteria required to verify the implementation meets the specification's functional and non-functional requirements.

#### Followup Context

This specification builds on M9S1's canonical artifact infrastructure to register `.omp/config.yml` as a canonical artifact. It ensures project configuration is validated through the canonical metadata validator and consumed by skills through the canonical resolver, not through ad hoc filesystem assumptions. M9S3 and M9S4 will depend on this config contract for skill integration and pipeline behavior.
