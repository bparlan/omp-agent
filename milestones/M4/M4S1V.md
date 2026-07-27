# Verification M4S1V

| Property         | Value        |
| ---------------- | ------------ |
| Document Type    | Verification |
| Identifier       | M4S1V        |
| Derived From     | M4S1         |
| template_version | 1.1.0        |

## Success Criteria

From the specification acceptance criteria:

- [ ] Incident analysis completed with root cause identified
- [ ] Pre-implementation state machine defined with 7 states and valid transitions
- [ ] Pre-implementation invariant documented and enforced
- [ ] Mandatory pre-implementation chain implemented in `manage-development`
- [ ] Tests must exist and be valid before `implement-specification` can be called
- [ ] `generate-tests` must execute before `implement-specification`
- [ ] Test readiness validation implemented and passing
- [ ] Readiness validation produces `READY_FOR_APPROVAL` or `NOT_READY_FOR_APPROVAL`
- [ ] Readiness validation stops workflow with exact blockers if `NOT_READY_FOR_APPROVAL`
- [ ] Human approval gate implemented with consolidated report
- [ ] Approval gate only allows entry after readiness validation passes
- [ ] Approval gate clearly states `READY FOR IMPLEMENTATION APPROVAL` or `NOT READY FOR IMPLEMENTATION APPROVAL`
- [ ] Approval gate requires explicit approval (no implicit approval)
- [ ] `approve-spec` preserved and not modified
- [ ] Responsibility separation maintained (orchestrator determines WHEN, `approve-spec` handles HOW)
- [ ] Resume and recovery supported at earliest incomplete valid stage
- [ ] Resume invalidates and rebuilds downstream artifacts when upstream artifacts change
- [ ] Artifact integrity validation distinguishes MISSING, GENERATED, VALIDATED, STALE, APPROVED
- [ ] `manage-roadmap` focused on planning/documentation with explicit handoff to `manage-development`
- [ ] All 14 negative guardrails implemented
- [ ] Test A (Correct ordering) passing
- [ ] Test B (Missing tests) blocking implementation
- [ ] Test C (Missing verification) blocking implementation
- [ ] Test D (Readiness failure) blocking approval
- [ ] Test E (Explicit approval required) blocking implementation
- [ ] Test F (Explicit approval granted) allowing implementation
- [ ] Test G (Resume) passing
- [ ] Definition of Done satisfied (independent verification of integrity guarantees)

---

## Functional Validation

### FR-1: Investigate existing orchestration failure

**Input**: Current implementation of orchestration skills

**Expected Output**: Concise incident analysis containing:
- Expected workflow (intended pre-implementation lifecycle)
- Actual workflow (how violation occurred)
- Point where invariant was violated
- Root cause (orchestration logic, state detection, missing validation, etc.)
- Which layer the fix belongs to

**Verification Method**:
- Manual review of code
- Timeline reconstruction from code comments and git history
- Trace back from violation point to upstream calls

**Pass Criteria**: Analysis identifies exact point and root cause, explicitly states which layer requires changes.

---

### FR-2: Define pre-implementation state machine

**Input**: Specification requirements for 7 states and invariant

**Expected Output**:
1. 7 explicit state definitions:
   - `PLANNING_READY`
   - `SPEC_GENERATED`
   - `VERIFICATION_GENERATED`
   - `TESTS_GENERATED`
   - `PRE_IMPLEMENTATION_READY`
   - `AWAITING_HUMAN_APPROVAL`
   - `APPROVED_FOR_IMPLEMENTATION`

2. Valid state transition diagram

3. Invariant definition for implementation permission

**Verification Method**:
- Manual review of state machine definition in `manage-development`
- Validation that all 7 states are defined and documented
- Validation that valid transitions are clearly documented

**Pass Criteria**: All 7 states defined, valid transitions documented, invariant clearly stated.

---

### FR-3: Define invariant for implementation

**Input**: Specification requirement

**Expected Output**:
```
IMPLEMENTATION_ALLOWED only if:
    SPECIFICATION_VALID
    AND
    VERIFICATION_VALID
    AND
    TESTS_VALID
    AND
    PRE_IMPLEMENTATION_READINESS_PASS
    AND
    EXPLICIT_HUMAN_APPROVAL
```

**Verification Method**:
- Manual review of code implementing the invariant
- Validation that all 5 conditions are checked
- Validation that all conditions must be true (AND logic)

**Pass Criteria**: Invariant implemented exactly as specified with all 5 conditions checked.

---

### FR-4: Enforce mandatory pre-implementation chain

**Input**: Specification requirement

**Expected Output**: State machine enforcing exact sequence:
```
generate-spec
    ↓
generate-verification
    ↓
generate-tests
    ↓
readiness validation
    ↓
approval gate
    ↓
implementation allowed
```

**Verification Method**:
- Manual review of state transitions in `manage-development`
- Validation that each skill call is gated by previous stage completion
- Validation that stages cannot be skipped based on artifact appearance

**Pass Criteria**: Sequence enforced, transitions documented, skip attempts blocked.

---

### FR-5: Enforce test-first readiness

**Input**: Implementation request before tests exist

**Expected Output**: Implementation blocked with clear error message

**Verification Method**:
- Test B scenario (create spec+verification, omit tests, attempt implementation)
- Expected error: "Tests missing or invalid"

**Pass Criteria**: Implementation blocked, clear error message explains what's missing.

---

### FR-6: Implement test readiness validation

**Input**: Completed spec, verification, and tests

**Expected Output**:
1. Validation of specification existence and validity
2. Validation of verification existence and validity
3. Validation of tests existence and validity
4. Consistency check across all three artifacts

**Verification Method**:
- Test scenarios for missing/incomplete/invalid artifacts
- Manual review of validation logic

**Pass Criteria**: All three artifacts validated, consistency checked, clear failure messages.

---

### FR-7: Implement readiness validation check

**Input**: Completed spec, verification, and tests

**Expected Output**: Returns `READY_FOR_APPROVAL` or `NOT_READY_FOR_APPROVAL`

**Verification Method**:
- Test D scenarios (inconsistent artifacts)
- Manual review of return values
- Validation that exact strings used

**Pass Criteria**: Returns one of two exact strings, provides clear blockers when `NOT_READY_FOR_APPROVAL`.

---

### FR-8: Implement human approval gate

**Input**: Ready artifacts

**Expected Output**:
1. Consolidated report with specification summary, verification summary, test summary
2. Clear statement of `READY_FOR_IMPLEMENTATION APPROVAL` or `NOT READY FOR IMPLEMENTATION APPROVAL`

**Verification Method**:
- Manual review of report generation logic
- Validation report contains all three summaries
- Validation message is exactly one of the two stated states

**Pass Criteria**: Report generated with all summaries, approval state clearly stated, transitions only allowed after approval.

---

### FR-9: Preserve `approve-spec`

**Input**: Existing `approve-spec` skill

**Expected Output**: No changes to `approve-spec` implementation or behavior

**Verification Method**:
- Git diff to confirm no modifications
- Functional test to confirm approval flow still works
- Validation that responsibility separation maintained (orchestrator determines WHEN, `approve-spec` handles HOW)

**Pass Criteria**: No code changes to `approve-spec`, approval flow functional, responsibility separation maintained.

---

### FR-10: Support safe resumption

**Input**: Interrupted workflow at any stage

**Expected Output**: Workflow resumes at earliest incomplete valid stage

**Verification Method**:
- Test G scenario: Interrupt at each stage, resume, verify correct stage
- Manual review of resume logic
- Validation that completed stages are not restarted

**Pass Criteria**: Resume works at all 5 stages, correct stage resumed, no stage repetition.

---

### FR-11: Implement artifact integrity validation

**Input**: Artifact file(s)

**Expected Output**: Returns one of 5 states:
- `MISSING`
- `GENERATED`
- `VALIDATED`
- `STALE`
- `APPROVED`

**Verification Method**:
- Manual review of validation functions
- Validation that all 5 states are distinguishable
- Validation that state is based on actual artifact, not filenames or reports

**Pass Criteria**: All 5 states distinguishable, validation based on artifact content/state, correct state returned for each case.

---

### FR-12: Implement resume and recovery with invalidation

**Input**: Changed upstream artifact

**Expected Output**: Downstream artifacts invalidated and rebuild triggers

**Verification Method**:
- Test scenario: Change spec, resume, verify verification/tests regenerated
- Manual review of invalidation logic
- Validation that only downstream artifacts affected

**Pass Criteria**: Invalidation works, rebuild triggers, only dependent artifacts affected, no duplicate generation.

---

### FR-13: Refine `manage-roadmap`

**Input**: Planning workflow

**Expected Output**:
1. Focus on planning/documentation
2. Explicit handoff to `manage-development` with:
   - Milestone ID
   - Task ID
   - Current state
   - Available artifacts
   - Next expected stage

**Verification Method**:
- Manual review of `manage-roadmap` implementation
- Validation that handoff information is explicit and complete
- Validation that implementation is not started from `manage-roadmap`

**Pass Criteria**: Handoff information complete, focus maintained, no implementation initiated from `manage-roadmap`.

---

### FR-14: Implement negative guardrails

**Input**: Attempt to bypass guardrails

**Expected Output**: Each guardrail enforced with clear error message

**Verification Method**:
- Test scenarios for each of 14 guardrails
- Expected errors clearly documented

**Pass Criteria**: All 14 guardrails enforced, clear error messages for each violation.

---

### FR-15: Create validation tests

**Input**: Specification requirements for 7 tests

**Expected Output**: 7 executable tests (A-G)

**Verification Method**:
- Automated test execution
- Manual review of test coverage

**Pass Criteria**: All 7 tests pass, tests cover ordering, missing artifacts, readiness, approval, resume scenarios.

---

## Edge Cases

### Empty or Null Inputs

- Milestone/task context is empty or null when calling `generate-spec`
- Artifact file is empty or null when validating integrity
- User approval input is empty or null

### Maximum/Minimum Bounds

- State machine must handle exactly 7 states (not 6, not 8)
- Pre-implementation chain must have exactly 5 stages (spec → verification → tests → readiness → approval)
- Implementation allowed must require all 5 conditions (not 4, not 6)

### Simultaneous Conflicting Operations

- Two orchestration skills attempting to modify state simultaneously
- Resume and update in progress
- Approval and readiness check overlapping

### Invalid State Transitions

- Attempt to transition directly from `PLANNING_READY` to `APPROVED_FOR_IMPLEMENTATION`
- Attempt to skip stages based on artifact existence (spec exists but verification missing)
- Attempt to transition after approval but before readiness validation

### Artifact State Changes

- Artifact generated but content is invalid (syntax error, empty)
- Artifact becomes stale (specification changed)
- Artifact deleted after being approved

### Race Conditions

- `generate-spec` completes but `generate-verification` is not called before `generate-tests`
- Readiness validation runs while tests are still being generated
- Approval requested while readiness validation is still in progress

---

## Failure Scenarios

### Invalid State Transitions

**Input**: Invalid state transition attempt

**Expected Behavior**: Fail closed, no invalid state reached

**Verification**: State machine rejects invalid transitions, error message indicates valid transitions only

**Pass Criteria**: No invalid state transitions allowed, clear error messages for each rejection.

---

### Missing Prerequisites

**Input**: Implementation requested without tests

**Expected Behavior**: Implementation blocked, clear error explaining missing tests

**Verification**: Test B scenario confirms implementation blocked

**Pass Criteria**: Implementation blocked, error message explains requirement for tests.

---

### Inconsistent Artifacts

**Input**: Specification, verification, and tests exist but inconsistent

**Expected Behavior**: Readiness validation fails, approval blocked

**Verification**: Test D scenario confirms approval blocked

**Pass Criteria**: Approval blocked, clear error messages for inconsistency.

---

### Implicit Approval

**Input**: All prerequisites satisfied but no explicit approval

**Expected Behavior**: Implementation blocked

**Verification**: Test E scenario confirms implementation blocked

**Pass Criteria**: Implementation blocked until explicit approval provided.

---

### Stale Artifacts

**Input**: Specification changed after tests were generated

**Expected Behavior**: Tests invalidated, need regeneration

**Verification**: Manual test with changed specification

**Pass Criteria**: Stale tests invalidated, regeneration triggered.

---

### Resume at Invalid Stage

**Input**: Resume at stage that was never completed

**Expected Behavior**: Resume at next valid stage (e.g., resume from `generate-verification` when verification was never started)

**Verification**: Test G scenarios for each stage

**Pass Criteria**: Resume works correctly, no stage repetition.

---

### Workflow State Corruption

**Input**: Workflow interrupted and state corrupted

**Expected Behavior**: Detect corruption, report error, do not proceed to invalid state

**Verification**: Simulate state corruption, verify error handling

**Pass Criteria**: Corruption detected, clear error message, no invalid state reached.

---

### Non-Deterministic Behavior

**Input**: Same workflow state multiple times

**Expected Output**: Same state and behavior each time

**Verification**: Repeat workflow multiple times, compare states

**Pass Criteria**: Workflow is deterministic, same input always produces same output.

---

## Regression Checklist

### manage-development

- **Must maintain**: Current orchestration workflow (when applicable)
- **Must maintain**: Compatibility with existing milestone structures (M2, M3)
- **Must maintain**: All existing milestone/task artifact paths and conventions
- **Must NOT change**: Direct invocation of SDD skills (keep handoff model)

### manage-roadmap

- **Must maintain**: Current planning/documentation workflow
- **Must maintain**: Existing milestone/task creation logic
- **Must maintain**: Compatibility with existing milestones
- **Must NOT change**: Core planning responsibilities

### generate-spec

- **Must maintain**: All existing specification generation logic
- **Must NOT change**: Domain logic or implementation requirements
- **Must maintain**: Output artifact format (M{X}S{Y}.md)

### generate-verification

- **Must maintain**: All existing verification generation logic
- **Must NOT change**: Domain logic or verification strategy
- **Must maintain**: Output artifact format (M{X}S{Y}V.md)

### generate-tests

- **Must maintain**: All existing test generation logic
- **Must NOT change**: Domain logic or test strategy
- **Must preserve**: Existing change that removed implementation-code-read requirement

### approve-spec

- **Must maintain**: All existing approval handling logic
- **Must NOT change**: Approval presentation or decision flow
- **Must maintain**: Approval artifacts and output format

### implement-specification

- **Must maintain**: Current implementation workflow (when called)
- **Must NOT change**: Implementation logic or artifacts
- **Must maintain**: Completion report format

### Documentation

- **Must maintain**: AGENTS.md framework overview
- **Must maintain**: FRAMEWORK.md architectural patterns
- **Must NOT change**: External-facing documentation not on Allowlist

---

## Manual Validation

### 1. Incident Analysis Review

**Steps**:
1. Read the investigation report from FR-1
2. Review the exact point where the invariant was violated
3. Verify the root cause analysis identifies the correct layer for the fix
4. Confirm the analysis aligns with the specification's investigation requirements

**Expected Result**: Investigation clearly documents how `implement-specification` was reached before `generate-tests` and identifies the specific cause.

---

### 2. State Machine Verification

**Steps**:
1. Locate the state machine definition in `manage-development`
2. Count the 7 defined states
3. Trace valid state transitions
4. Verify the invariant is enforced in code
5. Confirm the pre-implementation chain is enforced
6. Test that invalid transitions are rejected with clear errors

**Expected Result**: State machine correctly defined, enforced, and documented with all 7 states and valid transitions clearly identifiable.

---

### 3. Readiness Validation Verification

**Steps**:
1. Create a scenario where all three artifacts exist and are valid
2. Run readiness validation
3. Confirm `READY_FOR_APPROVAL` is returned
4. Create a scenario with inconsistent artifacts
5. Run readiness validation
6. Confirm `NOT_READY_FOR_APPROVAL` is returned with clear blockers
7. Verify exact strings are used (`READY_FOR_APPROVAL` and `NOT_READY_FOR_APPROVAL`)

**Expected Result**: Readiness validation correctly distinguishes ready from not ready with clear error messages.

---

### 4. Approval Gate Verification

**Steps**:
1. Run the readiness validation to get `READY_FOR_APPROVAL`
2. Generate the consolidated report
3. Verify report contains specification summary, verification summary, and test summary
4. Verify approval gate clearly states the readiness status
5. Confirm implementation is blocked until explicit approval
6. Provide explicit approval and confirm implementation is now allowed

**Expected Result**: Consolidated report generated, approval gate enforces explicit approval, implementation transitions only after approval.

---

### 5. Resume and Recovery Verification

**Steps**:
1. Start a workflow and complete `generate-spec`
2. Interrupt before `generate-verification`
3. Resume from `generate-verification`
4. Complete `generate-verification`
5. Interrupt before `generate-tests`
6. Resume from `generate-tests`
7. Complete all stages through to approval
8. For each interruption, verify the correct stage is resumed and completed stages are not repeated

**Expected Result**: Resume works correctly at each stage without restarting completed stages.

---

### 6. Artifact Integrity Validation Verification

**Steps**:
1. Test with missing artifact → should return `MISSING`
2. Test with empty artifact → should return `GENERATED` (if file exists)
3. Test with valid artifact → should return `VALIDATED`
4. Change specification and test → should return `STALE`
5. Test with approved artifact → should return `APPROVED`
6. Verify validation is based on artifact content/state, not filenames

**Expected Result**: All 5 states correctly distinguished based on actual artifact conditions.

---

### 7. Guardrail Enforcement Verification

**Steps**:
1. Test each of the 14 negative guardrails by attempting to bypass
2. Verify each bypass attempt is blocked with a clear error message
3. Confirm the error message explains what's required

**Expected Result**: All 14 guardrails are enforced with clear error messages for each violation.

---

### 8. Manage-Roadmap Handoff Verification

**Steps**:
1. Run a planning workflow through `manage-roadmap`
2. Verify handoff information to `manage-development` includes:
   - Milestone ID
   - Task ID
   - Current state
   - Available artifacts
3. Confirm `manage-roadmap` does not independently start implementation
4. Verify handoff information is complete and explicit

**Expected Result**: Handoff information is complete and explicit, planning workflow does not initiate implementation.

---

### 9. Specification to Implementation Flow Verification

**Steps**:
1. Start a complete SDD workflow from spec through to implementation
2. Verify the order: `generate-spec` → `generate-verification` → `generate-tests` → readiness → approval → implementation
3. Confirm each stage transitions correctly
4. Verify tests are generated before implementation
5. Confirm implementation is blocked until explicit approval

**Expected Result**: Complete workflow follows correct order, tests generated before implementation, approval required.

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

This mechanical check must be executed by `evaluate-implementation` before tests are considered passed.

- **Command**: `git diff --name-only`
- **Assertion**: The output of this command MUST strictly match the "Allowlist" defined in the Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

* Existing tests: Not applicable (no existing tests for this milestone)
* New tests: Test A, B, C, D, E, F, G to be created in `tests/M4/`
* Commands: N/A

---

### Test A — Correct Ordering

**Command**:
```bash
cd ~/devcode/aef/agent
# Create test scenario
# Attempt to start implementation without completing full pipeline
# Verify implementation is blocked
```

**Expected Result**: Implementation blocked with error message indicating tests not generated.

**Verification**: Automated test in `tests/M4/test_ordering.py`

---

### Test B — Missing Tests Block Implementation

**Command**:
```bash
cd ~/devcode/aef/agent
# Create milestone/task context
# Generate spec and verification
# Skip tests
# Attempt implementation
# Verify blocked
```

**Expected Result**: Implementation blocked with clear error about missing tests.

**Verification**: Automated test in `tests/M4/test_missing_tests.py`

---

### Test C — Missing Verification Blocks Implementation

**Command**:
```bash
cd ~/devcode/aef/agent
# Create milestone/task context
# Generate spec and tests
# Skip verification
# Attempt implementation
# Verify blocked
```

**Expected Result**: Implementation blocked with clear error about missing verification.

**Verification**: Automated test in `tests/M4/test_missing_verification.py`

---

### Test D — Readiness Failure Blocks Approval

**Command**:
```bash
cd ~/devcode/aef/agent
# Generate inconsistent artifacts
# Attempt readiness validation
# Verify `NOT_READY_FOR_APPROVAL`
# Verify approval blocked
```

**Expected Result**: Readiness validation fails with clear blockers, approval blocked.

**Verification**: Automated test in `tests/M4/test_readiness_failure.py`

---

### Test E — Explicit Approval Required

**Command**:
```bash
cd ~/devcode/aef/agent
# Generate all valid artifacts
# Verify readiness passes
# Confirm no approval provided
# Attempt implementation
# Verify blocked
```

**Expected Result**: Implementation blocked until explicit approval.

**Verification**: Automated test in `tests/M4/test_explicit_approval_required.py`

---

### Test F — Explicit Approval Granted

**Command**:
```bash
cd ~/devcode/aef/agent
# Generate all valid artifacts
# Verify readiness passes
# Provide explicit approval
# Attempt implementation
# Verify allowed
```

**Expected Result**: Implementation allowed after explicit approval.

**Verification**: Automated test in `tests/M4/test_explicit_approval_granted.py`

---

### Test G — Resume Functionality

**Command**:
```bash
cd ~/devcode/aef/agent
# Generate spec
# Resume from verification
# Generate verification
# Resume from tests
# Generate tests
# Resume from readiness
# Complete readiness
# Resume from approval
# Provide approval
# Resume from implementation
# Verify implementation allowed
```

**Expected Result**: Each resume resumes at correct stage, no stage repetition.

**Verification**: Automated test in `tests/M4/test_resume.py`

---

### State Machine Tests

**Command**:
```bash
cd ~/devcode/aef/agent
# Test all 7 state transitions
# Test invalid state transitions
# Verify state machine enforces invariant
```

**Expected Result**: State machine correctly tracks and validates state transitions.

**Verification**: Automated test in `tests/M4/test_state_machine.py`

---

### Artifact Integrity Tests

**Command**:
```bash
cd ~/devcode/aef/agent
# Test each of 5 artifact states (MISSING, GENERATED, VALIDATED, STALE, APPROVED)
# Verify correct state returned for each case
```

**Expected Result**: All 5 states correctly distinguished.

**Verification**: Automated test in `tests/M4/test_artifact_integrity.py`

---

### Guardrail Enforcement Tests

**Command**:
```bash
cd ~/devcode/aef/agent
# Test each of 14 negative guardrails
# Verify each bypass attempt blocked
```

**Expected Result**: All 14 guardrails enforced.

**Verification**: Automated test in `tests/M4/test_guardrails.py`

---

## Performance Considerations

### Deterministic Execution Time

- **Baseline**: Measure execution time for each stage from start to finish
- **Threshold**: Execution time should not degrade by more than 10% compared to current implementation (when applicable)
- **Measurement**: Run workflow 10 times, record average and standard deviation

### State Machine Performance

- **Baseline**: Measure state transition overhead
- **Threshold**: State transition should complete in < 100ms
- **Measurement**: 1000 state transitions, measure average time

### Artifact Validation Performance

- **Baseline**: Measure time to validate one artifact
- **Threshold**: Single artifact validation should complete in < 50ms
- **Measurement**: 1000 validations, measure average time

### No Race Conditions

- **Concurrency Test**: Run multiple orchestration operations concurrently and verify correct behavior
- **Expected Result**: No race conditions, deterministic outcomes

---

## Security Considerations

### Input Validation

- Validate all artifact paths to prevent directory traversal
- Validate milestone/task IDs to prevent invalid references
- Validate state machine transitions to prevent invalid state manipulation

### Authorization Boundary Tests

- Test that unauthorized access to approval state is prevented
- Test that invalid state transitions cannot be forced

### Data Exposure Prevention

- Ensure artifact integrity checks do not expose sensitive content
- Ensure error messages do not reveal internal implementation details

### Authorization Boundary

- Verify that `manage-development` is the only orchestrator that can enforce gates
- Verify that manual bypass is not possible (e.g., through direct skill invocation without orchestrator)

---

## Observability

### Required Logs

- State transitions (with source, target, timestamp)
- Stage completions (with artifact references)
- Readiness validation results (with blockers)
- Approval gate transitions (with approval decision)
- Error conditions (with detailed error messages)

### Required Metrics

- State machine state counts
- Stage completion rates
- Readiness validation pass/fail rates
- Guardrail violation counts
- Workflow interruption points

### Debug Output

- When readiness validation fails, include detailed explanation of which artifacts are missing/invalid
- When approval is requested, include summary of all artifacts
- When state transition is rejected, include valid transition options

---

## Expected Outcomes

The verification is successful when:

1. **Incident analysis** clearly identifies how the orchestration failure occurred and root cause.

2. **State machine** is implemented with 7 states, valid transitions documented, and invariant enforced.

3. **Pre-implementation chain** is strictly enforced with no stage skipping.

4. **Test-first readiness** is enforced: implementation blocked until tests exist and are valid.

5. **Readiness validation** produces exact strings (`READY_FOR_APPROVAL`/`NOT_READY_FOR_APPROVAL`) with clear blockers.

6. **Human approval gate** enforces explicit approval with consolidated report.

7. **`approve-spec`** is preserved and not modified.

8. **Resume and recovery** work correctly at all 5 stages without restarting completed stages.

9. **Artifact integrity validation** distinguishes all 5 states based on actual artifact conditions.

10. **`manage-roadmap`** focuses on planning with explicit handoff to `manage-development`.

11. **All 14 negative guardrails** are enforced with clear error messages.

12. **All 7 validation tests** (A-G) pass, demonstrating correct ordering, blocking, and resume behavior.

13. **Definition of Done** is satisfied: independent verification confirms implementation cannot bypass test generation or approval.
