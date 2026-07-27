# M6S1V: Verification Protocol - Canonical Artifact Model

## Overview

This verification protocol defines the test cases, success criteria, edge cases, and failure scenarios for the M6S1 implementation specification. It ensures that the canonical artifact model is correctly implemented and that the framework meets all functional requirements.

## Verification Strategy

The verification will use a combination of:

1. **Manual Code Review**: Review of skill implementations and template updates
2. **Automated Testing**: Unit tests for type resolution, metadata validation, ID generation
3. **Integration Testing**: Test skills with actual artifacts
4. **Legacy Compatibility Testing**: Test with existing M2, M3, M4 artifacts
5. **Documentation Review**: Verify artifact architecture documentation

## Success Criteria

For each functional requirement (FR-1 through FR-13), the following success criteria must be met:

1. **Canonical IDs**: All artifacts use canonical ID patterns (M{N}, SPEC-{N}, VER-{N}, TEST-{N}, INV-{N}, EVAL-{N}, REVIEW-{N}, AUDIT-{N})
2. **Type Resolution**: Artifact type resolution completes in < 100ms and uses correct priority order (metadata → directory → filename)
3. **Metadata Schema**: All artifacts have required fields and valid type field
4. **Lineage Model**: Lineage relationships explicitly represented through metadata
5. **Legacy Compatibility**: Existing artifacts remain accessible and correctly classified
6. **Skill Integration**: All skills updated to use new model
7. **Fail-Closed Behavior**: Type conflicts fail closed with clear error messages
8. **Documentation**: Artifact architecture document complete and accurate

## Test Coverage Goals

- **Unit Tests**: 60+ tests covering type resolution, ID generation, metadata validation
- **Integration Tests**: 20+ tests covering skill behaviors
- **Edge Cases**: 10+ tests covering unusual scenarios
- **Legacy Compatibility**: 10+ tests covering existing artifacts
- **Documentation Tests**: 5+ tests verifying documentation completeness
- **Total Coverage**: >80%

## Test Cases

### Functional Requirements Tests

#### FR-1: Canonical Artifact Types

**Test 1-1: Validate canonical ID generation for milestone**
- **Input**: Milestone ID `M6`
- **Expected Output**: `M6` is valid, `M06` is invalid, `M6a` is invalid
- **Test Method**: Run validation function, check for correct/rejection

**Test 1-2: Validate canonical ID generation for specification**
- **Input**: Specification ID `SPEC-001`
- **Expected Output**: `SPEC-001` is valid, `SPEC-1` is invalid, `SPEC-001A` is invalid
- **Test Method**: Run validation function, check for correct/rejection

**Test 1-3: Validate canonical ID generation for investigation**
- **Input**: Investigation ID `INV-001`
- **Expected Output**: `INV-001` is valid, `INV-1` is invalid, `INV-001A` is invalid
- **Test Method**: Run validation function, check for correct/rejection

**Test 1-4: Validate canonical ID generation for all types**
- **Input**: All eight artifact types with valid/invalid IDs
- **Expected Output**: All types validate correctly
- **Test Method**: Run validation for all types, check coverage

#### FR-2: Canonical Storage Model

**Test 2-1: Create artifact in correct directory**
- **Input**: `generate-spec` called with investigation ID
- **Expected Output**: Specification created in `milestones/M6/specs/SPEC-001.md`
- **Test Method**: Create investigation, call generate-spec, check directory

**Test 2-2: Create verification in correct directory**
- **Input**: `generate-verification` called with specification ID
- **Expected Output**: Verification created in `milestones/M6/verifications/VER-001.md`
- **Test Method**: Create specification, call generate-verification, check directory

**Test 2-3: Create test set in correct directory**
- **Input**: `generate-tests` called with specification ID
- **Expected Output**: Test set created in `milestones/M6/tests/TEST-001.md`
- **Test Method**: Create specification, call generate-tests, check directory

**Test 2-4: Create investigation in correct directory**
- **Input**: `investigate-issue` called
- **Expected Output**: Investigation created in `milestones/M6/investigations/INV-001.md`
- **Test Method**: Call investigate-issue, check directory

**Test 2-5: Verify milestone structure invariant**
- **Input**: Any artifact path
- **Expected Output**: Path follows pattern: milestone → type directory → ID
- **Test Method**: Check path structure for all artifacts

#### FR-3: Minimal Metadata Schema

**Test 3-1: Validate required fields present**
- **Input**: Create artifact without required fields
- **Expected Output**: Validation fails with missing field error
- **Test Method**: Try to create artifact, check for validation errors

**Test 3-2: Validate type field values**
- **Input**: Invalid type "invalid-type"
- **Expected Output**: Validation fails with invalid type error
- **Test Method**: Try to create artifact with invalid type, check for error

**Test 3-3: Validate ID format**
- **Input**: Invalid ID format "SPEC-A"
- **Expected Output**: Validation fails with invalid ID format error
- **Test Method**: Try to create artifact with invalid ID, check for error

**Test 3-4: Validate lineage fields are lists**
- **Input**: `derived_from` as string instead of list
- **Expected Output**: Validation fails with type error
- **Test Method**: Try to create artifact with wrong lineage type, check for error

**Test 3-5: Test all optional fields**
- **Input**: Artifact with all optional fields
- **Expected Output**: All fields accepted, warnings only (no errors)
- **Test Method**: Create artifact with all optional fields, check validation result

#### FR-4: Deterministic Type Resolution

**Test 4-1: Priority 1 - Metadata type takes precedence**
- **Input**: File in `investigations/` with `type: specification`
- **Expected Output**: Type resolved as "specification" from metadata
- **Test Method**: Create file with metadata type, check resolution source

**Test 4-2: Priority 2 - Directory type when no metadata**
- **Input**: File in `investigations/` without metadata
- **Expected Output**: Type resolved as "investigation" from directory
- **Test Method**: Create file without metadata, check resolution source

**Test 4-3: Priority 3 - Filename when no metadata or directory**
- **Input**: File without metadata in legacy directory
- **Expected Output**: Type resolved from filename pattern
- **Test Method**: Create file in legacy directory, check resolution source

**Test 4-4: Performance requirement met (< 100ms)**
- **Input**: Resolve type for 1000 artifacts
- **Expected Output**: Average time < 100ms per resolution
- **Test Method**: Time type resolution for multiple artifacts, check average

**Test 4-5: Conflict detection between metadata and directory**
- **Input**: File in `specs/` with `type: investigation`
- **Expected Output**: Type conflict detected, error raised
- **Test Method**: Create conflicting file, check for error

**Test 4-6: Legacy filename pattern matching**
- **Input**: File named `M6S1I1.md`
- **Expected Output**: Type resolved as "investigation" from filename
- **Test Method**: Create file, check resolution

**Test 4-7: Unknown artifact type**
- **Input**: File in non-canonical directory without metadata
- **Expected Output**: Type resolved as "unknown", not error
- **Test Method**: Create file in unusual directory, check resolution

#### FR-5: Lineage Model

**Test 5-1: Specification with derived_from investigation**
- **Input**: Create specification from investigation ID
- **Expected Output**: Specification has `derived_from: [INV-001]`
- **Test Method**: Call generate-spec with investigation ID, check metadata

**Test 5-2: Verification with derived_from specification**
- **Input**: Create verification from specification ID
- **Expected Output**: Verification has `derived_from: [SPEC-002]`
- **Test Method**: Call generate-verification with spec ID, check metadata

**Test 5-3: Evaluation with derived_from verification**
- **Input**: Create evaluation from verification ID
- **Expected Output**: Evaluation has `derived_from: [VER-001]`
- **Test Method**: Call generate-evaluation with verification ID, check metadata

**Test 5-4: Review with superseded_by**
- **Input**: Create review from evaluation ID
- **Expected Output**: Review has `superseded_by: [EVAL-001]`
- **Test Method**: Call generate-review with evaluation ID, check metadata

**Test 5-5: Multiple derived_from values**
- **Input**: Create specification with multiple investigations
- **Expected Output**: Specification has `derived_from: [INV-001, INV-002]`
- **Test Method**: Provide multiple investigation IDs, check metadata

**Test 5-6: Investigation with no specifications**
- **Input**: Create investigation with no findings
- **Expected Output**: Investigation created without derived_from fields
- **Test Method**: Call investigate-issue with no findings, check artifact

#### FR-6: Correction Semantics

**Test 6-1: No CORRECTED suffix in corrected specification**
- **Input**: Create corrected specification
- **Expected Output**: Specification ID is `SPEC-002`, not `SPEC-002-CORRECTED`
- **Test Method**: Create correction, check ID format

**Test 6-2: Correction uses supersedes field**
- **Input**: Create corrected specification
- **Expected Output**: Specification has `supersedes: [SPEC-001]`
- **Test Method**: Create correction, check supersedes field

**Test 6-3: Correction uses derived_from field**
- **Input**: Create corrected specification
- **Expected Output**: Specification has `derived_from: [INV-001]`
- **Test Method**: Create correction, check derived_from field

**Test 6-4: Correction includes reason field**
- **Input**: Create corrected specification
- **Expected Output**: Specification has `reason: [correction]`
- **Test Method**: Create correction, check reason field

#### FR-7: Legacy Compatibility

**Test 7-1: Legacy M5S1.md accessible**
- **Input**: File `M5S1.md` exists
- **Expected Output**: File accessible and classified correctly
- **Test Method**: Check if file exists, run type resolution

**Test 7-2: Legacy M5S1I1.md classified as investigation**
- **Input**: File `M5S1I1.md` exists
- **Expected Output**: Classified as "investigation"
- **Test Method**: Create file, run type resolution, check type

**Test 7-3: Legacy M5S1I1-CORRECTED.md accessible**
- **Input**: File `M5S1I1-CORRECTED.md` exists
- **Expected Output**: File accessible and classified correctly
- **Test Method**: Check if file exists, run type resolution

**Test 7-4: M5S1T1.md classified as test set**
- **Input**: File `M5S1T1.md` exists
- **Expected Output**: Classified as "test_set"
- **Test Method**: Create file, run type resolution, check type

**Test 7-5: M5S1V.md classified as verification**
- **Input**: File `M5S1V.md` exists
- **Expected Output**: Classified as "verification"
- **Test Method**: Create file, run type resolution, check type

**Test 7-6: Multiple classification sources work**
- **Input**: Legacy artifact with explicit metadata
- **Expected Output**: Classified using metadata, not just filename
- **Test Method**: Create file with metadata, check classification

**Test 7-7: No automatic bulk migration**
- **Input**: Existing legacy artifacts
- **Expected Output**: Artifacts remain in place, not automatically renamed
- **Test Method**: Check file system, verify no bulk migration

#### FR-8: investigate-issue Updates

**Test 8-1: Investigation ID is canonical (INV-{N})**
- **Input**: Call investigate-issue
- **Expected Output**: Investigation created with ID `INV-001`
- **Test Method**: Call skill, check artifact ID

**Test 8-2: No specification IDs in output**
- **Input**: Call investigate-issue with findings
- **Expected Output**: Output recommends specifications but doesn't prescribe IDs
- **Test Method**: Call skill, check output format

**Test 8-3: Lineage recommendations reference findings**
- **Input**: Call investigate-issue with findings
- **Expected Output**: Recommendations map findings to specification creation
- **Test Method**: Call skill, check output format

#### FR-9: generate-spec Updates

**Test 9-1: Specification ID is canonical (SPEC-{N})**
- **Input**: Call generate-spec with investigation ID
- **Expected Output**: Specification created with ID `SPEC-001`
- **Test Method**: Call skill, check artifact ID

**Test 9-2: Type field is specification**
- **Input**: Call generate-spec
- **Expected Output**: Created artifact has `type: specification`
- **Test Method**: Call skill, check metadata

**Test 9-3: Derived_from field populated**
- **Input**: Call generate-spec with investigation ID
- **Expected Output**: Specification has `derived_from: [INV-001]`
- **Test Method**: Call skill, check metadata

**Test 9-4: Artifact created in specs/ directory**
- **Input**: Call generate-spec
- **Expected Output**: Artifact created in `milestones/M6/specs/SPEC-001.md`
- **Test Method**: Call skill, check file location

#### FR-10: generate-verification Updates

**Test 10-1: Verification ID is canonical (VER-{N})**
- **Input**: Call generate-verification with specification ID
- **Expected Output**: Verification created with ID `VER-001`
- **Test Method**: Call skill, check artifact ID

**Test 10-2: Type field is verification**
- **Input**: Call generate-verification
- **Expected Output**: Created artifact has `type: verification`
- **Test Method**: Call skill, check metadata

**Test 10-3: Derived_from field populated**
- **Input**: Call generate-verification with specification ID
- **Expected Output**: Verification has `derived_from: [SPEC-002]`
- **Test Method**: Call skill, check metadata

**Test 10-4: Artifact created in verifications/ directory**
- **Input**: Call generate-verification
- **Expected Output**: Artifact created in `milestones/M6/verifications/VER-001.md`
- **Test Method**: Call skill, check file location

#### FR-11: generate-tests Updates

**Test 11-1: Type resolution before use**
- **Input**: Call generate-tests with investigation artifact
- **Expected Output**: Type resolved before generation
- **Test Method**: Call skill, check resolution order

**Test 11-2: Reject investigation as specification**
- **Input**: Call generate-tests with investigation artifact
- **Expected Output**: Error raised: "Cannot resolve source artifact type. Expected: specification. Found: investigation."
- **Test Method**: Call skill with investigation, check error message

**Test 11-3: Reject non-specification types**
- **Input**: Call generate-tests with verification artifact
- **Expected Output**: Error raised: "Cannot resolve source artifact type. Expected: specification. Found: verification."
- **Test Method**: Call skill with verification, check error message

**Test 11-4: Verify milestone association**
- **Input**: Call generate-tests with specification from M6
- **Expected Output**: Error raised: "Specification does not belong to current milestone."
- **Test Method**: Call skill, check milestone validation

**Test 11-5: Cannot misclassify investigations**
- **Input**: Call generate-tests with legacy investigation artifact
- **Expected Output**: Error raised, not silent fallback
- **Test Method**: Call skill with legacy investigation, check behavior

#### FR-12: Fail-Closed Behavior

**Test 12-1: Detect type conflict**
- **Input**: File in `specs/` with `type: investigation`
- **Expected Output**: Error raised with conflict message
- **Test Method**: Create conflicting file, check for error

**Test 12-2: Clear conflict error message**
- **Input**: File in `specs/` with `type: investigation`
- **Expected Output**: Error includes path, metadata type, directory type, resolution steps
- **Test Method**: Check error message format

**Test 12-3: No silent reclassification**
- **Input**: File in `investigations/` with `type: specification`
- **Expected Output**: Error raised, no silent change
- **Test Method**: Create conflicting file, check for silent change

**Test 12-4: Process exits on conflict**
- **Input**: File in `specs/` with `type: investigation`
- **Expected Output**: Process exits with non-zero exit code
- **Test Method**: Create conflicting file, check exit code

#### FR-13: Artifact Architecture Documentation

**Test 13-1: Document includes all sections**
- **Input**: Review artifact architecture document
- **Expected Output**: All 10 required sections present (types, IDs, directory, metadata, lineage, corrections, legacy, resolution, skill matrix, lifecycle)
- **Test Method**: Check document structure, verify all sections exist

**Test 13-2: Examples provided for all sections**
- **Input**: Review artifact architecture document
- **Expected Output**: Each section includes at least one example
- **Test Method**: Check for examples in each section

**Test 13-3: Skill matrix is complete**
- **Input**: Review artifact architecture document
- **Expected Output**: Matrix includes all 8 skills with creation/consumption columns
- **Test Method**: Check matrix completeness

**Test 13-4: Documentation is accurate**
- **Input**: Review artifact architecture document
- **Expected Output**: All information matches implementation
- **Test Method**: Cross-reference with implementation, fix discrepancies

**Test 13-5: Documentation is clear and readable**
- **Input**: Review artifact architecture document
- **Expected Output**: Document is easy to understand, uses proper formatting
- **Test Method**: Read document, assess clarity and readability

## Edge Case Tests

### EC-1: Investigation with No Findings

**Test EC-1-1**: Create investigation with empty findings list
- **Input**: Call investigate-issue with empty findings
- **Expected Output**: Investigation created successfully without `derived_from` fields
- **Test Method**: Create investigation, check artifact

### EC-2: Specification with Multiple Investigations

**Test EC-2-1**: Create specification with two investigation IDs
- **Input**: Call generate-spec with investigation IDs ["INV-001", "INV-002"]
- **Expected Output**: Specification has `derived_from: ["INV-001", "INV-002"]`
- **Test Method**: Call skill, check metadata

### EC-3: Verification from Multiple Specifications

**Test EC-3-1**: Create verification with two specification IDs
- **Input**: Call generate-verification with specification IDs ["SPEC-001", "SPEC-002"]
- **Expected Output**: Verification has `derived_from: ["SPEC-001", "SPEC-002"]`
- **Test Method**: Call skill, check metadata

### EC-4: Missing Metadata During Migration

**Test EC-4-1**: Legacy artifact without type field
- **Input**: Legacy file in `investigations/` without type field
- **Expected Output**: Classified as "investigation" from directory
- **Test Method**: Create file, run type resolution

### EC-5: Artifact Moved Between Directories

**Test EC-5-1**: Move artifact after creation
- **Input**: Create specification, then move to `investigations/`
- **Expected Output**: Next access detects conflict (metadata "specification" vs directory "investigations")
- **Test Method**: Move artifact, try to use it, check for error

### EC-6: Empty Title

**Test EC-6-1**: Create artifact without title
- **Input**: Create artifact with empty title field
- **Expected Output**: Validation passes with default title
- **Test Method**: Create artifact, check validation

### EC-7: Invalid Status Value

**Test EC-7-1**: Create artifact with invalid status
- **Input**: Create artifact with status "invalid"
- **Expected Output**: Validation fails with invalid status error
- **Test Method**: Create artifact, check validation

### EC-8: Circular Lineage

**Test EC-8-1**: Create circular reference (spec → verification → spec)
- **Input**: Try to create verification with spec ID, then spec with verification ID
- **Expected Output**: Validation fails or cycle detected
- **Test Method**: Try circular creation, check for error

### EC-9: Non-Existent Referenced Artifact

**Test EC-9-1**: Create artifact referencing non-existent ID
- **Input**: Create specification with `derived_from: [INV-999]`
- **Expected Output**: Validation fails or warning about missing artifact
- **Test Method**: Create artifact with invalid reference, check validation

### EC-10: Multiple Specifications in Same Directory

**Test EC-10-1**: Create multiple specifications sequentially
- **Input**: Create SPEC-001, then SPEC-002
- **Expected Output**: Both created in correct order
- **Test Method**: Create specifications, check order

## Failure Scenario Tests

### FS-1: Type Resolution Returns Unknown

**Test FS-1-1**: Resolve type for unrecognized file
- **Input**: File in unusual directory without metadata
- **Expected Output**: Type resolved as "unknown", warning logged, not error
- **Test Method**: Create file, run type resolution, check result

### FS-2: Metadata Conflicts with Directory

**Test FS-2-1**: Metadata type conflicts but no explicit type field
- **Input**: File in non-canonical location with no type field
- **Expected Output**: Type resolved from directory or filename, warning logged
- **Test Method**: Create file, check resolution

### FS-3: Skill Cannot Determine milestone_id

**Test FS-3-1**: Create artifact without milestone_id
- **Input**: Call skill without milestone_id
- **Expected Output**: Skill infers milestone_id from path, or fails closed
- **Test Method**: Call skill, check behavior

### FS-4: ID Generation Collision

**Test FS-4-1**: Create two artifacts with same ID
- **Input**: Try to create SPEC-001 twice
- **Expected Output**: Second creation increments ID or fails with error
- **Test Method**: Attempt duplicate creation, check behavior

### FS-5: Template Not Found

**Test FS-5-1**: Try to use missing template
- **Input**: Call skill with non-existent template
- **Expected Output**: Warning logged, artifact created without template
- **Test Method**: Create template, try to use it, check behavior

### FS-6: File System Permissions

**Test FS-6-1**: Try to create artifact in protected directory
- **Input**: Try to create artifact without write permissions
- **Expected Output**: Clear error message with file path
- **Test Method**: Attempt creation without permissions, check error

## Integration Tests

### Integration Test 1: Complete Specification Generation Workflow

**Setup**:
1. Create investigation `INV-001` using `investigate-issue`
2. Create specification `SPEC-001` using `generate-spec`
3. Create verification `VER-001` using `generate-verification`

**Expected Results**:
- `INV-001` created in `investigations/INV-001.md`
- `SPEC-001` created in `specs/SPEC-001.md` with `type: specification` and `derived_from: [INV-001]`
- `VER-001` created in `verifications/VER-001.md` with `type: verification` and `derived_from: [SPEC-001]`

### Integration Test 2: Legacy Compatibility Workflow

**Setup**:
1. Verify existing M5 artifacts exist
2. Call `generate-tests` with M5S1I1.md (investigation)
3. Verify error is raised (investigation not accepted as specification)

**Expected Results**:
- M5 artifacts accessible
- `generate-tests` raises error on investigation
- Error message indicates type conflict

### Integration Test 3: Correction Workflow

**Setup**:
1. Create specification `SPEC-001` from investigation `INV-001`
2. Create corrected specification `SPEC-002` from same investigation
3. Verify `SPEC-002` has `supersedes: [SPEC-001]`

**Expected Results**:
- `SPEC-002` has `supersedes` field
- `SPEC-002` has `derived_from` field
- No `-CORRECTED` suffix in ID

### Integration Test 4: Type Resolution Priority

**Setup**:
1. Create investigation in `investigations/` directory
2. Add `type: specification` to metadata
3. Verify type resolved from metadata, not directory

**Expected Results**:
- Type resolved as "specification" from metadata
- Source indicated as "metadata"

### Integration Test 5: Fail-Closed on Conflict

**Setup**:
1. Create file in `specs/` directory
2. Add `type: investigation` to metadata
3. Try to access artifact
4. Verify error raised and process exits

**Expected Results**:
- Error raised on conflict
- Error message clear
- Process exits with non-zero code

## Legacy Compatibility Tests

### Legacy Test 1: M2, M3, M4 Accessibility

**Setup**:
1. List all artifacts in M2, M3, M4 directories
2. Try to classify each artifact

**Expected Results**:
- All artifacts accessible
- All artifacts classified correctly (no crashes)
- Legacy filenames recognized (M{N}S{N}T{N}, etc.)

### Legacy Test 2: Controlled Migration

**Setup**:
1. Check that legacy artifacts are not automatically renamed
2. Check that migration requires explicit action

**Expected Results**:
- No bulk migration occurs
- Manual migration required
- Migration documented

### Legacy Test 3: Multi-Source Classification

**Setup**:
1. Create legacy artifact with explicit metadata
2. Classify using metadata and filename

**Expected Results**:
- Classification uses metadata when available
- Multiple sources considered

## Documentation Validation Tests

### Doc Test 1: Required Sections Present

**Setup**:
1. Review artifact architecture document
2. Check for all required sections

**Expected Results**:
- All 10 sections present
- Sections properly labeled and ordered

### Doc Test 2: Examples Provided

**Setup**:
1. Review artifact architecture document
2. Check for examples in each section

**Expected Results**:
- At least one example per section
- Examples are accurate

### Doc Test 3: Skill Matrix Complete

**Setup**:
1. Review skill matrix in documentation
2. Check completeness

**Expected Results**:
- All 8 skills included
- Creation/consumption columns present
- Correct data

### Doc Test 4: Accuracy Check

**Setup**:
1. Compare documentation with implementation
2. Identify discrepancies

**Expected Results**:
- No discrepancies
- All information matches implementation

## Test Execution Plan

### Phase 1: Unit Tests (Weeks 1-2)

1. Create test file `tests/M6/test_canonical_ids.py`
2. Implement tests for FR-1 (canonical IDs)
3. Run tests, fix failures
4. Target: 20 tests, all passing

### Phase 2: Type Resolution Tests (Weeks 2-3)

1. Create test file `tests/M6/test_type_resolution.py`
2. Implement tests for FR-4 (type resolution)
3. Run tests, fix failures
4. Target: 20 tests, all passing

### Phase 3: Metadata Validation Tests (Weeks 3-4)

1. Create test file `tests/M6/test_metadata_validation.py`
2. Implement tests for FR-3 (metadata schema)
3. Run tests, fix failures
4. Target: 15 tests, all passing

### Phase 4: Skill Integration Tests (Weeks 4-6)

1. Create test file `tests/M6/test_skill_integration.py`
2. Implement tests for FR-8 through FR-12 (skill updates)
3. Run tests, fix failures
4. Target: 15 tests, all passing

### Phase 5: Legacy Compatibility Tests (Weeks 6-7)

1. Create test file `tests/M6/test_legacy_compatibility.py`
2. Implement tests for FR-7 (legacy compatibility)
3. Run tests, fix failures
4. Target: 10 tests, all passing

### Phase 6: Edge Case Tests (Weeks 7-8)

1. Create test file `tests/M6/test_edge_cases.py`
2. Implement tests for edge cases (EC-1 through EC-10)
3. Run tests, fix failures
4. Target: 10 tests, all passing

### Phase 7: Failure Scenario Tests (Weeks 8-9)

1. Create test file `tests/M6/test_failure_scenarios.py`
2. Implement tests for failure scenarios (FS-1 through FS-6)
3. Run tests, fix failures
4. Target: 6 tests, all passing

### Phase 8: Integration Tests (Weeks 9-10)

1. Create test file `tests/M6/test_integration.py`
2. Implement integration tests
3. Run tests, fix failures
4. Target: 5 integration tests, all passing

### Phase 9: Documentation Tests (Weeks 10-11)

1. Create test file `tests/M6/test_documentation.py`
2. Implement documentation validation tests
3. Run tests, fix failures
4. Target: 5 tests, all passing

### Phase 10: Comprehensive Test Run (Weeks 11-12)

1. Run all test files together
2. Analyze coverage
3. Fix any remaining failures
4. Target: >80% coverage, all tests passing

## Test Artifacts Required

### For Unit Tests
- Test files for each test category
- Mock objects for skills
- Sample artifacts

### For Integration Tests
- Complete workflow from investigation to review
- Legacy artifacts (M2, M3, M4)
- Sample specifications, verifications, tests

### For Edge Case Tests
- Edge case artifacts (no findings, multiple lineage, etc.)
- Conflict artifacts (metadata vs directory)
- Invalid data artifacts

### For Documentation Tests
- Artifact architecture document
- Migration guide
- AGENTS.md updates

## Test Execution Commands

```bash
# Run all tests
python3 -m pytest tests/M6/ -v

# Run specific test file
python3 tests/M6/test_canonical_ids.py
python3 tests/M6/test_type_resolution.py
python3 tests/M6/test_metadata_validation.py
python3 tests/M6/test_skill_integration.py
python3 tests/M6/test_legacy_compatibility.py
python3 tests/M6/test_edge_cases.py
python3 tests/M6/test_failure_scenarios.py
python3 tests/M6/test_integration.py
python3 tests/M6/test_documentation.py

# Run with coverage
python3 -m pytest tests/M6/ --cov=milestones/M6 --cov-report=html

# Run specific test class
python3 -m pytest tests/M6/test_type_resolution.py::TestTypeResolution -v

# Run specific test method
python3 -m pytest tests/M6/test_type_resolution.py::TestTypeResolution::test_priority_1 -v
```

## Acceptance Criteria

Implementation is accepted when:

1. **All functional requirements satisfied**: All FR-1 through FR-13 tests pass
2. **All edge cases handled**: All EC-1 through EC-10 tests pass
3. **All failure scenarios managed**: All FS-1 through FS-6 tests pass
4. **Integration tests pass**: All integration tests pass
5. **Legacy compatibility verified**: All legacy tests pass
6. **Documentation validated**: All documentation tests pass
7. **Test coverage >80%**: Coverage report shows >80%
8. **No critical bugs**: No crashes or silent failures
9. **Performance requirement met**: Type resolution <100ms average
10. **Documentation complete**: Artifact architecture document complete and accurate
