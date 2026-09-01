---
id: VER-M9S2
milestone_id: M9
status: draft
type: verification
derived_from:
  - M9
  - SPEC-M9S2
template_version: 1.3.0
---

# Verification Protocol for Project Configuration — .omp/config.yml Schema, Validation, and Canonical Artifact Registration

## Verification Items

### VER-M9S2-FR-PROJECT_CONFIG_SCHEMA-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_SCHEMA-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_SCHEMA
- **Verification Method**: UNIT_TEST
- **Target**: `core/artifacts/types.py`
- **Preconditions**:
  - Artifact type definitions module exists and is importable
  - Standard Python environment with all dependencies installed
- **Input or fixture**:
  - Test that imports from `core.artifacts.types` and checks `project-configuration` type definition
- **Expected Evidence**:
  - `CanonicalArtifactType` definition for `project-configuration` exists in `_RAW_ARTIFACT_TYPE_DEFINITIONS`
  - Schema matches `CONFIG_SCHEMA` from `core/config.py` with required fields: `project_id`, `project_slug`, `mode`
  - `mode` enum contains exactly `framework` and `application`
  - Storage rule defined for `project-configuration` type
- **Failure Condition**:
  - Missing `project-configuration` type definition
  - Schema does not match `CONFIG_SCHEMA` from spec
  - `mode` enum contains unsupported values
  - Storage rule not defined or incorrect pattern
- **Initial Failure Expectation**:
  - Exit code 127 - `project-configuration` type not found in artifact types
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `project-configuration` type properly defined with correct schema and storage rule

### VER-M9S2-FR-PROJECT_CONFIG_LOAD-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_LOAD-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_LOAD
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment with PyYAML and jsonschema installed
- **Input or fixture**:
  - Valid `.omp/config.yml` file in test project root
- **Expected Evidence**:
  - `load_project_config()` returns dict with keys: `project_id`, `project_slug`, `mode`
  - Values match those in `.omp/config.yml` file
  - Correctly discovers project root via `.omp/config.yml` or `.git` directory
- **Failure Condition**:
  - `load_project_config()` fails to locate `.omp/config.yml`
  - Returns incorrect or malformed configuration
  - Missing required fields in returned dict
  - Validation errors during load
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `load_project_config()` correctly loads and validates config

### VER-M9S2-FR-PROJECT_CONFIG_VALIDATE-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_VALIDATE-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_VALIDATE
- **Verification Method**: UNIT_TEST
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment with jsonschema installed
- **Input or fixture**:
  - Valid config dict with all required fields
  - Invalid config dict (missing `project_id`)
  - Invalid config dict (missing `mode`)
  - Invalid config dict (unsupported `mode` value)
- **Expected Evidence**:
  - `validate_config()` returns `True` for valid configs
  - `validate_config()` returns `False` for invalid configs
  - Structured validation errors emitted for invalid configs
  - Missing field detection for required fields
  - Enum validation for `mode` field
- **Failure Condition**:
  - Valid config returns `False`
  - Invalid config returns `True`
  - Missing structured error messages for invalid configs
  - No validation for `mode` enum values
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `validate_config()` correctly validates all config types

### VER-M9S2-FR-PROJECT_CONFIG_SAVE-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_SAVE-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_SAVE
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment with PyYAML installed
- **Input or fixture**:
  - Valid config dict
- **Expected Evidence**:
  - `save_project_config()` creates `.omp/config.yml` file
  - File contains valid YAML with correct formatting
  - Keys maintain stable order
  - File passes `load_project_config()` round-trip validation
  - File passes `validate_config()` validation
- **Failure Condition**:
  - File not created or incorrect path
  - Invalid YAML content
  - Keys order not preserved
  - Round-trip validation fails
  - Validation fails after save
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `save_project_config()` writes valid YAML file that passes all validations

### VER-M9S2-FR-PROJECT_CONFIG_DEFAULT-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_DEFAULT-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_DEFAULT
- **Verification Method**: UNIT_TEST
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test parameters: `project_id="test-project", project_slug="test-project", mode="framework"`
  - Test parameters: `project_id="another-project", project_slug="another-project", mode="application"`
- **Expected Evidence**:
  - `create_default_config()` returns dict with exactly `project_id`, `project_slug`, `mode` keys
  - Values match input parameters
  - No extraneous keys in returned dict
  - Returns `True` for `validate_config()` round-trip
- **Failure Condition**:
  - Missing required keys in returned dict
  - Contains extraneous keys
  - Values do not match input parameters
  - Round-trip validation fails
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `create_default_config()` returns valid default config

### VER-M9S2-FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION
- **Verification Method**: UNIT_TEST
- **Target**: `core/artifacts/registry.py`
- **Preconditions**:
  - Artifact registry module exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test that imports `get_registry()` and checks for `project-configuration` type
- **Expected Evidence**:
  - `project-configuration` type registered in artifact registry
  - `get_type('project-configuration')` returns non-None `ArtifactTypeDefinition`
  - Schema matches `CONFIG_SCHEMA` from `core/config.py`
  - `required` list includes `project_id`, `project_slug`, `mode`
  - `properties.mode.enum` contains exactly `framework` and `application`
  - Storage rule exists for type
- **Failure Condition**:
  - `project-configuration` type not registered
  - Schema does not match `CONFIG_SCHEMA`
  - Missing required fields in schema
  - Unsupported enum values in schema
  - Missing or incorrect storage rule
- **Initial Failure Expectation**:
  - Exit code 127 - Artifact registry module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - `project-configuration` type registered with correct schema and storage rule

### VER-M9S2-FR-PROJECT_CONFIG_CANONICAL_VALIDATION-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_CANONICAL_VALIDATION-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_CANONICAL_VALIDATION
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `bin/omp-verify-metadata`
- **Preconditions**:
  - CLI tool `omp-verify-metadata` accessible via `python bin/omp-verify-metadata`
  - Valid `.omp/config.yml` file exists
  - Invalid `.omp/config.yml` file exists
  - Standard Python environment with PyYAML installed
- **Input or fixture**:
  - Valid `.omp/config.yml` file (all required fields, supported `mode`)
  - Invalid `.omp/config.yml` file (missing `project_id`)
  - Invalid `.omp/config.yml` file (unsupported `mode` value)
- **Expected Evidence**:
  - `python bin/omp-verify-metadata valid_config.yml` returns exit code 0
  - `python bin/omp-verify-metadata invalid_config.yml` returns exit code 1
  - Structured error messages for invalid configs
  - Missing field detection for invalid configs
  - Enum validation for `mode` field
- **Failure Condition**:
  - Valid config returns exit code 1
  - Invalid config returns exit code 0
  - Missing structured error messages
  - No validation for required fields or enum
- **Initial Failure Expectation**:
  - Exit code 127 - CLI tool not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - CLI tool correctly validates `.omp/config.yml` artifacts

### VER-M9S2-FR-PROJECT_CONFIG_RESOLUTION-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_RESOLUTION-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_RESOLUTION
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `core/artifacts/resolution.py`
- **Preconditions**:
  - Artifact resolution module exists and is importable
  - Standard Python environment
  - `.omp/config.yml` file exists in test project
- **Input or fixture**:
  - Command: `resolve_artifact(type='project-configuration')`
  - Command: `resolve_artifact(identity='CONFIG-test-project')`
- **Expected Evidence**:
  - Resolution returns object with `resolved: true` for `.omp/config.yml`
  - Returned artifact contains identity and metadata
  - Path ends with `.omp/config.yml`
  - Correctly resolves by type `project-configuration`
  - Correctly resolves by identity `CONFIG-{project_slug}`
- **Failure Condition**:
  - Returns `resolved: false` for `.omp/config.yml`
  - Missing required fields in resolution result
  - Incorrect path in resolution result
  - Cannot resolve by type `project-configuration`
  - Cannot resolve by identity
- **Initial Failure Expectation**:
  - Exit code 127 - Resolution module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - Resolution correctly locates and returns `.omp/config.yml` artifact

### VER-M9S2-FR-PROJECT_CONFIG_MODE_ENFORCEMENT-001
- **Verification ID**: VER-M9S2-FR-PROJECT_CONFIG_MODE_ENFORCEMENT-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_MODE_ENFORCEMENT
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `bin/bootstrap-project`
- **Preconditions**:
  - CLI tool `bootstrap-project` accessible via `python bin/bootstrap-project`
  - Standard Python environment
  - Test project directory structure
- **Input or fixture**:
  - `bootstrap-project --mode framework --project-id test --project-slug test`
  - `bootstrap-project --mode application --project-id app --project-slug app`
- **Expected Evidence**:
  - Framework mode creates `.omp/config.yml` with `mode: framework`
  - Framework mode creates AEF-specific documentation (`.omp/docs/`)
  - Application mode creates `.omp/config.yml` with `mode: application`
  - Application mode does NOT create AEF-specific documentation
  - Both modes create `.omp` directory
  - Configuration file validates successfully after creation
- **Failure Condition**:
  - Incorrect `mode` value in `.omp/config.yml`
  - Framework mode creates `.omp/docs/`
  - Application mode creates `.omp/docs/`
  - Missing `.omp` directory in either mode
  - Configuration validation fails after bootstrap
- **Initial Failure Expectation**:
  - Exit code 127 - Bootstrap tool not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - Bootstrap creates correct project structure based on mode

### VER-M9S2-NFR-CONFIG_FILE_LOCATION-001
- **Verification ID**: VER-M9S2-NFR-CONFIG_FILE_LOCATION-001
- **Source Requirement ID**: NFR-CONFIG_FILE_LOCATION
- **Verification Method**: UNIT_TEST
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test project with `.omp/config.yml` at project root
  - Test project with `.git` directory (no `.omp/config.yml`)
- **Expected Evidence**:
  - `load_project_config()` discovers `.omp/config.yml` when present
  - `load_project_config()` falls back to `.git` directory when `.omp/config.yml` absent
  - Fixed path `.omp/config.yml` used (not hardcoded alternatives)
  - Project root correctly identified in both cases
- **Failure Condition**:
  - `load_project_config()` cannot find `.omp/config.yml`
  - `load_project_config()` uses hardcoded alternative path
  - Project root incorrectly identified
  - Does not check for `.git` directory as fallback
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - Config file location correctly handled and discovered

### VER-M9S2-NFR-CONFIG_SCHEMA_STABILITY-001
- **Verification ID**: VER-M9S2-NFR-CONFIG_SCHEMA_STABILITY-001
- **Source Requirement ID**: NFR-CONFIG_SCHEMA_STABILITY
- **Verification Method**: UNIT_TEST
- **Target**: `core/config.py`
- **Preconditions**:
  - `core/config.py` module exists and is importable
  - Standard Python environment with jsonschema
- **Input or fixture**:
  - Valid config from prior version (minimal config with required fields)
  - Valid config with optional fields (if any)
- **Expected Evidence**:
  - Schema validation passes for prior version config
  - Backward compatibility maintained for valid configs
  - Required fields still validated
  - `mode` enum values still enforced
  - New optional fields may be added without breaking validation
- **Failure Condition**:
  - Valid prior config fails validation
  - Schema validation broken for existing configs
  - Required fields no longer validated
  - `mode` enum changed without specification update
- **Initial Failure Expectation**:
  - Exit code 127 - `core/config.py` module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - Schema maintains backward compatibility

### VER-M9S2-NFR-CONFIG_ARTIFACT_REGISTRATION-001
- **Verification ID**: VER-M9S2-NFR-CONFIG_ARTIFACT_REGISTRATION-001
- **Source Requirement ID**: NFR-CONFIG_ARTIFACT_REGISTRATION
- **Verification Method**: UNIT_TEST
- **Target**: `core/artifacts/registry.py`
- **Preconditions**:
  - Artifact registry module exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Check if `project-configuration` type is registered
  - Verify type has correct metadata
- **Expected Evidence**:
  - `project-configuration` type is present in artifact registry
  - Type has valid schema and storage rule
  - Registry contains `get_type()`, `get_schema()`, `get_storage_rule()` methods
  - Type correctly registered with `register_type()`
- **Failure Condition**:
  - `project-configuration` type not registered
  - Registry methods missing or broken
  - Schema or storage rule invalid
  - Registration process fails
- **Initial Failure Expectation**:
  - Exit code 127 - Artifact registry module not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - Config artifact properly registered in canonical artifact system

## Testability Assessment Summary

### Requirements Status

| FR ID | Requirement Category | Current Status | Testability Assessment |
|:------|:-------------------|:----------------|:----------------------|
| FR-PROJECT_CONFIG_SCHEMA | Implementation | Not Implemented | ✅ High - Observable schema contract |
| FR-PROJECT_CONFIG_LOAD | Implementation | Not Implemented | ✅ High - Observable file and API contract |
| FR-PROJECT_CONFIG_VALIDATE | Implementation | Not Implemented | ✅ High - Observable validation contract |
| FR-PROJECT_CONFIG_SAVE | Implementation | Not Implemented | ✅ High - Observable filesystem contract |
| FR-PROJECT_CONFIG_DEFAULT | Implementation | Not Implemented | ✅ High - Observable contract |
| FR-PROJECT_CONFIG_ARTIFACT_REGISTRATION | Implementation | Not Implemented | ✅ High - Observable registry contract |
| FR-PROJECT_CONFIG_CANONICAL_VALIDATION | Implementation | Not Implemented | ✅ High - Observable CLI contract |
| FR-PROJECT_CONFIG_RESOLUTION | Implementation | Not Implemented | ✅ High - Observable resolution contract |
| FR-PROJECT_CONFIG_MODE_ENFORCEMENT | Implementation | Not Implemented | ✅ High - Observable behavior contract |
| NFR-CONFIG_FILE_LOCATION | Non-Functional | Not Implemented | ✅ High - Observable discovery contract |
| NFR-CONFIG_SCHEMA_STABILITY | Non-Functional | Not Implemented | ✅ High - Observable compatibility contract |
| NFR-CONFIG_ARTIFACT_REGISTRATION | Non-Functional | Not Implemented | ✅ High - Observable registry contract |

### Testability Summary

**High Testability (11/11 requirements)**: All requirements have observable contracts (CLI, Schema, or Filesystem) with clear validation criteria.

**Overall Testability Score**: 100% - All 11 requirements are fully testable with clear contracts and expectations.

### Test Structure Recommendations

**Unit Tests Required**:
- `test_config_schema_001.py` - Config schema verification
- `test_config_load_001.py` - Config loading verification
- `test_config_validate_001.py` - Config validation verification
- `test_config_save_001.py` - Config saving verification
- `test_config_default_001.py` - Default config verification
- `test_config_artifact_registration_001.py` - Artifact registration verification

**Integration Tests Required**:
- `test_config_canonical_validation_001.sh` - Canonical validation verification
- `test_config_resolution_001.py` - Config resolution verification
- `test_config_mode_enforcement_001.sh` - Mode enforcement verification
- `test_config_file_location_001.py` - Config file location verification
- `test_config_schema_stability_001.py` - Schema stability verification
- `test_config_artifact_registration_integration_001.py` - Registry integration verification

## Next Steps

Run `/generate-tests` to create executable test suites from this verification protocol. The generated tests will validate the project configuration implementation against the specification requirements.

## Followup Context

This verification protocol builds on M9S1's canonical artifact infrastructure to ensure that `.omp/config.yml` is properly registered as a canonical artifact type. It verifies that project configuration follows the canonical validation and resolution patterns rather than ad hoc skill logic. The protocol ensures backward compatibility and establishes clear observable contracts for all config operations, enabling downstream modules M9S3 and M9S4 to depend on this stable configuration contract.
