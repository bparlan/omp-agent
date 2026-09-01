---
id: VER-M13S2V
type: verification
status: draft
milestone_id: M13
derived_from:
  - M13
  - SPEC-M13S2
template_version: 1.1.0
---

## Success Criteria

This verification protocol ensures the M13S2 Artifact Naming & Frontmatter Compliance specification requirements are met:

## Followup Reuse

_(Include for followup specifications)_

### Reusable Items from Prior Verifications

- Regression items: All verification items from prior M13 specifications
- Automated test patterns: Core validation and metadata extraction patterns
- Edge cases: Artifact naming boundary conditions, frontmatter field validation
- Failure scenarios: Invalid filename patterns, malformed frontmatter

### New Verification Required

- Items specific to this followup scope: Artifact naming validation, frontmatter schema validation, metadata version compliance

---

## Functional Validation

### VER-M13S2V-001
- **Verification ID**: VER-M13S2V-001
- **Source Requirement ID**: FR-ARTIFACT_NAMING_VALIDATION
- **Verification Method**: SCRIPT_EXECUTION
- **Target**: `bin/validate-metadata` script with filename pattern validation
- **Preconditions**: 
  - `core/validation.py` is importable and functional
  - `bin/validate-metadata` script exists with validate_metadata() integration
  - Test fixture directory with both valid and invalid filenames exists
- **Input or fixture**: 
  - Test filenames: `["M13S1.md", "VER-M13S2V1.md", "TEST-M13S3T1.md", "EVA-M13S4.md", "REV-M13S5.md", "CLOSE-M13-7.md", "invalid-name.md", "VER-Invalid-Name.md"]`
- **Expected Evidence**: 
  - Valid filenames: exit code 0 with {"valid": true, "errors": []}
  - Invalid filenames: exit code 0 with {"valid": false, "errors": ["<pattern-violation>"]}
- **Failure Condition**: Any filename validation result does not match expected pattern compliance or exit codes differ
- **Initial Failure Expectation**: Command will fail with exit code 127 (Command Not Found) if `bin/validate-metadata` doesn't exist
- **Post-Implementation Success Expectation**: All filename validations return correct pattern compliance with specific error messages for invalid patterns

### VER-M13S2V-002
- **Verification ID**: VER-M13S2V-002
- **Source Requirement ID**: FR-FRONTMATTER_SCHEMA_VALIDATION
- **Verification Method**: INTEGRITY_TEST
- **Target**: Frontmatter validation integrity for specification artifacts
- **Preconditions**: 
  - `core/artifacts/metadata.py` is importable with `extract_frontmatter()` function
  - `core/validation.py` is importable with `validate_metadata()` function
  - Test fixture specifications with valid and invalid frontmatter exist
- **Input or fixture**: 
  - Valid frontmatter: `{id: "M13S1.md", type: "specification", milestone_id: "M13", status: "draft", derived_from: [], template_version: "1.3.0", metadata: {created_at: "2026-08-31", updated_at: "2026-08-31", artifact_identity: "test", artifact_type: "specification"}}`
  - Invalid frontmatter: Missing required fields, incorrect types, malformed data
- **Expected Evidence**: 
  - Valid frontmatter: {"valid": true, "errors": [], "missing_fields": []}
  - Invalid frontmatter: {"valid": false, "errors": ["<specific-errors>"], "missing_fields": ["<missing-fields>"]}
- **Failure Condition**: Frontmatter validation results do not match expected compliance or error reporting does not include specific missing/invalid fields
- **Initial Failure Expectation**: Script will fail with exit code 127 if validation dependencies are missing
- **Post-Implementation Success Expectation**: All frontmatter validations return correct validation status with specific error details for invalid fields

### VER-M13S2V-003
- **Verification ID**: VER-M13S2V-003
- **Source Requirement ID**: FR-METADATA_VERSION_COMPLIANCE
- **Verification Method**: UNIT_TEST
- **Target**: Metadata version parsing and validation via core registry
- **Preconditions**: 
  - `core/artifacts/registry.py` is importable with `get_registry()` function
  - Test versions: `["1.3.0", "2.0.0", "0.9.0", "invalid-version", "1.3.0.0", "1.3"]`
- **Input or fixture**: 
  - Version validation test cases with both valid and invalid semantic versions
- **Expected Evidence**: 
  - Valid versions: {"valid": true, "errors": []}
  - Invalid versions: {"valid": false, "errors": ["<version-validation-errors>"]}
- **Failure Condition**: Version validation does not correctly identify valid/invalid semantic versions or error reporting is incomplete
- **Initial Failure Expectation**: Test will fail with ImportError if registry module is not available
- **Post-Implementation Success Expectation**: All version validations correctly identify semantic version compliance and report specific validation errors for invalid versions

### VER-M13S2V-004
- **Verification ID**: VER-M13S2V-004
- **Source Requirement ID**: FR-FRONTMATTER_SCHEMA_VALIDATION
- **Verification Method**: INTEGRITY_TEST
- **Target**: Complete artifact validation workflow integration
- **Preconditions**: 
  - Full artifact validation stack is functional (core/validation.py + core/artifacts/metadata.py + core/artifacts/registry.py)
  - Test artifact files with complete frontmatter exist
- **Input or fixture**: 
  - Complete artifact specification files following M13 naming conventions and frontmatter format
- **Expected Evidence**: 
  - All validations: {"valid": true, "errors": [], "missing_fields": []}
  - Complete audit trail in PIPELINE-STATE.md with validation timestamps
- **Failure Condition**: End-to-end validation fails or PIPELINE-STATE.md logging is incomplete
- **Initial Failure Expectation**: Integration test will fail if validation components are missing
- **Post-Implementation Success Expectation**: Complete validation workflow processes all artifacts correctly with comprehensive logging in PIPELINE-STATE.md

---

## Edge Cases

- **VER-M13S2V-EC-001**: Filenames at pattern boundaries (minimum and maximum valid characters)
- **VER-M13S2V-EC-002**: Frontmatter with empty vs. missing vs. null values for required fields
- **VER-M13S2V-EC-003**: Version edge cases (major version 0, very large version numbers)
- **VER-M13S2V-EC-004**: Combined validation failures across multiple frontmatter fields
- **VER-M13S2V-EC-005**: Unicode characters in filenames and frontmatter values

---

## Failure Scenarios

- **VER-M13S2V-FS-001**: Malformed frontmatter YAML syntax
- **VER-M13S2V-FS-002**: Filename with valid pattern but invalid artifact type
- **VER-M13S2V-FS-003**: Template version with correct format but invalid baseline (e.g., "0.1.0")
- **VER-M13S2V-FS-004**: Missing entire frontmatter delimiters (---)
- **VER-M13S2V-FS-005**: Cross-reference validation failures in derived_from field

---

## Regression Checklist

- **VER-M13S2V-RC-001**: All prior verification items from M13S1 still pass
- **VER-M13S2V-RC-002**: Existing artifact validation contracts unchanged
- **VER-M13S2V-RC-003**: Core AEF integration with validation and metadata modules maintained
- **VER-M13S2V-RC-004**: No unintended side effects on other milestone artifacts
- **VER-M13S2V-RC-005**: Backward compatibility with existing specification formats

---

## Manual Validation

1. Review generated verification protocol for complete requirement coverage
2. Validate that all VER-M13S2V-XXX IDs are unique and sequential
3. Confirm each verification item references correct source FR ID
4. Check that verification methods match target types (SCRIPT_EXECUTION, UNIT_TEST, INTEGRITY_TEST)
5. Verify initial failure expectations are appropriate for each verification type
6. Ensure system awareness checks for AEF core components are documented
7. Validate traceability lineage from verification items back to source requirements
8. Confirm gap detection addresses specification interface completeness

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

_This mechanical check must be executed by `evaluate-implementation` before tests are considered passed._

- **Command:** `git diff --name-only milestones/M13/VER-M13S2V.md`
- **Assertion:** The output of this command MUST strictly match the "Allowlist" defined in the Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

* Existing tests
* New tests
* Commands

---

## Expected Outcomes

This verification protocol ensures that:

1. **Filename Pattern Validation**: All M13 artifact filenames strictly conform to specified regex patterns with appropriate error reporting
2. **Frontmatter Schema Validation**: All mandatory frontmatter fields are present and correctly typed with specific error details for violations
3. **Metadata Version Compliance**: Template versions follow semantic versioning with baseline 1.3.0 validation
4. **System Integration**: Verification uses actual AEF core components (core/validation.py, core/artifacts/metadata.py, core/artifacts/registry.py)
5. **Traceability**: Every verification item maps back to source functional requirement with stable FR IDs
6. **Testability**: All requirements define observable boundaries with executable verification contracts

The verification protocol is machine-readable and directly consumable by the `/generate-tests` stage to create executable test suites that validate the M13S2 specification requirements.
