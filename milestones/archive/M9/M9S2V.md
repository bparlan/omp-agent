---
id: VER-M9S2V
type: verification
milestone_id: M9
status: draft
derived_from:
  - M9
  - SPEC-M9S2
template_version: 1.3.0
---

# Verification Protocol for M9S2 - Project Configuration

## Verification Items

### VER-M9S2V-FR-PROJECT_CONFIG_SCHEMA-001
- **Verification ID**: VER-M9S2V-FR-PROJECT_CONFIG_SCHEMA-001
- **Source Requirement ID**: FR-PROJECT_CONFIG_SCHEMA
- **Verification Method**: UNIT_TEST
- **Target**: `tests/M9/S2/schema_validation.py`
- **Preconditions**:
  - `core/validation.py` exists and is importable
  - `validate_project_config()` function is accessible via the validation API
  - Standard Python environment with schema validation capabilities
- **Input or fixture**:
  - Test that validates schema validation against `.omp/config.yml` files
  - Test that validates schema enforcement against invalid configurations
- **Expected Evidence**:
  - Schema validation correctly accepts valid `.omp/config.yml` files
  - Schema validation correctly rejects invalid `.omp/config.yml` files
  - Schema validation enforces required fields (project_id, project_slug, version)
  - Schema validation enforces field patterns and constraints
- **Failure Condition**:
  - Valid configurations incorrectly rejected
  - Invalid configurations incorrectly accepted
  - Missing or incorrect error messages
- **Initial Failure Expectation**:
  - Exit code 127 (Command Not Found) - validation implementation not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - schema validation works correctly

### VER-M9S2V-FR-PROJECT_CONFIG_VALIDATION-002
- **Verification ID**: VER-M9S2V-FR-PROJECT_CONFIG_VALIDATION-002
- **Source Requirement ID**: FR-PROJECT_CONFIG_VALIDATION
- **Verification Method**: UNIT_TEST
- **Target**: `tests/M9/S2/function_api.py`
- **Preconditions**:
  - `validate_project_config()` function is accessible via the validation API
  - `core/validation.py` exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test that validates the `validate_project_config(project_root: str)` function
  - Test that validates the function return dictionary structure
- **Expected Evidence**:
  - `validate_project_config()` returns correct dictionary structure with `valid`, `errors`, `missing_fields` keys
  - `validate_project_config()` correctly validates valid configuration files
  - `validate_project_config()` correctly reports invalid configuration files
  - `validate_project_config()` correctly handles missing configuration files
- **Failure Condition**:
  - Function returns incorrect or missing data
  - Function does not correctly handle valid or invalid configurations
  - Function does not correctly handle missing files
- **Initial Failure Expectation**:
  - Exit code 127 (Command Not Found) - validation function not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - validation function works correctly

### VER-M9S2V-FR-PROJECT_CONFIG_REGISTRATION-003
- **Verification ID**: VER-M9S2V-FR-PROJECT_CONFIG_REGISTRATION-003
- **Source Requirement ID**: FR-PROJECT_CONFIG_REGISTRATION
- **Verification Method**: UNIT_TEST
- **Target**: `tests/M9/S2/artifact_integration.py`
- **Preconditions**:
  - Artifact type registry exists and is importable
  - `get_artifact_type()` function is accessible via the artifact registry API
  - `core/artifacts/artifact_types.py` exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test that validates `get_artifact_type("project-config")` returns correct type definition
  - Test that validates `project-config` type registration in the artifact registry
- **Expected Evidence**:
  - `get_artifact_type("project-config")` returns non-None type definition
  - Type definition has correct `canonical_storage_location` (".omp/config.yml")
  - Type definition has correct `machine_identifier` ("project-config")
  - Artifact type is properly registered during registry initialization
- **Failure Condition**:
  - `get_artifact_type("project-config")` returns None
  - Type definition has incorrect storage location or identifier
  - Artifact type not registered in the registry
- **Initial Failure Expectation**:
  - Exit code 127 (Command Not Found) - artifact registry not found
- **Post-Implementation Success Expectation**:
  - Exit code 0 - artifact registry registration works correctly

### VER-M9S2V-NFR-MINIMALISM-004
- **Verification ID**: VER-M9S2V-NFR-MINIMALISM-004
- **Source Requirement ID**: NFR-MINIMALISM
- **Verification Method**: UNIT_TEST
- **Target**: `tests/M9/S2/schema_validation.py`
- **Preconditions**:
  - Schema validation is working via `validate_project_config()`
  - `core/validation.py` exists and is importable
  - Standard Python environment
- **Input or fixture**:
  - Test that validates schema enforcement against unauthorized fields
  - Test that validates schema minimalism (no extra fields allowed)
- **Expected Evidence**:
  - Schema validation correctly rejects `mode` field addition
  - Schema validation correctly rejects technology stack declarations
  - Schema validation strictly enforces only three required fields
  - Schema validation provides clear error messages for unauthorized fields
- **Failure Condition**:
  - Schema validation accepts unauthorized fields
  - Schema validation does not provide clear error messages
  - Schema validation is not strict enough
- **Initial Failure Expectation**:
  - Exit code 127 (Command Not Found) - schema validation not implemented
- **Post-Implementation Success Expectation**:
  - Exit code 0 - schema minimalism enforced correctly

## Testability Assessment Summary

### Requirements Status

| FR ID | Requirement Category | Current Status | Testability Assessment |
|:------|:-------------------|:----------------|:----------------------|
| FR-PROJECT_CONFIG_SCHEMA | Implementation | Partially Implemented | ✅ High - Schema validation tests cover requirements |
| FR-PROJECT_CONFIG_VALIDATION | Implementation | Partially Implemented | ✅ High - API function tests cover requirements |
| FR-PROJECT_CONFIG_REGISTRATION | Implementation | Partially Implemented | ✅ High - Artifact registry tests cover requirements |
| NFR-MINIMALISM | Non-Functional | Partially Implemented | ✅ High - Schema validation tests cover requirements |

### Testability Summary

**High Testability (4/4 requirements)**: All requirements have observable contracts (CLI, Schema, or Filesystem) with clear validation criteria.

**Overall Testability Score**: 100% - All 4 requirements are fully testable with clear contracts and expectations.

### Test Structure Recommendations

**Unit Tests Required**:
- `schema_validation.py` - Schema validation and minimalism tests
- `function_api.py` - API function validation tests  
- `artifact_integration.py` - Artifact registry integration tests

**Integration Tests Required**:
- Test that validates integration between validation and artifact registry

## Next Steps

Run `/evaluate-tests` to verify your TDD pre-implementation baseline against the newly generated tests. The generated tests will validate the canonical artifact infrastructure implementation against the specification requirements.