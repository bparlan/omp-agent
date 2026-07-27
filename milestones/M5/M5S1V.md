# Verification M5S1V

| Property         | Value        |
| ---------------- | ------------ |
| Document Type    | Verification |
| Identifier       | M5S1V        |
| Derived From     | M5S1         |
| template_version | 1.1.0        |

## Success Criteria

**Primary Success Criteria**

1. **Post-Approval Automation Complete**
   - After approval, framework automatically executes: implement → evaluate → route → repair/review
   - No manual invocation between these stages (except where required for human escalation)
   - Orchestrator maintains full control over sequencing and routing

2. **Evaluation Routing Implemented**
   - PASS path: evaluate → review → final report
   - MINOR defect path: evaluate → hotfix-issue → evaluate (no approval)
   - COMPLEX issue path: evaluate → investigate → (spec change? → approval) → continue
   - HUMAN escalation path: user receives decision report with clear evidence

3. **Repair Loop Bounded**
   - MAX_AUTO_REPAIR_CYCLES limit (default 2-3) prevents infinite loops
   - Counter resets for new implementation cycles
   - Stop after limit reached and report to user

4. **Approval Gate Protected**
   - No repair path can silently modify requirements
   - Any requirement change returns to approval gate
   - Hotfixes limited to localized scope changes

5. **Test-Driven Completion**
   - Tests pass is required for final success
   - Test failures prevent final success
   - No test weakening or rewriting

6. **Review Automation**
   - review-implementation runs automatically when evaluation passes
   - Final report includes all required information
   - Report returned to user

**Secondary Success Criteria**

7. **manage-development Full Lifecycle Orchestration**
   - Owns sequencing, state, preconditions, postconditions, routing, retry limits, human gates
   - No duplication of individual skill internal logic

8. **manage-roadmap Strategic Focus**
   - Remains focused on strategic responsibilities
   - Does NOT expand into execution lifecycle

9. **Zero Breaking Changes**
   - Existing functionality preserved
   - All changes are additive or refactoring
   - Backward compatible

10. **Test Coverage**
    - All routing paths tested
    - Loop limit tested
    - Approval protection tested
    - Test-Driven Completion enforced

---

## Functional Validation

**FR-1: Post-Approval Automation Chain**

**Verification Method**: Integration test

**Test Case 1.1**: Complete post-approval workflow execution
- **Input**: Approved specification, verification protocol, test plan
- **Expected Output**: Implementation completes, evaluation runs, routing occurs automatically
- **Verification**: Observe workflow progression from approval to routing without manual intervention

**Test Case 1.2**: Implementation artifacts received
- **Input**: Implementation starts after approval
- **Expected Output**: Orchestrator provides approved artifacts (spec, verif, test plan) to implementation
- **Verification**: Verify orchestrator passes correct artifacts to implement-specification skill

**Test Case 1.3**: Success not declared on completion alone
- **Input**: Implementation completes without error
- **Expected Output**: Orchestrator continues to evaluation and routing, does not declare success
- **Verification**: Confirm implementation completion does not end workflow

---

**FR-2: Evaluation Routing**

**Verification Method**: Integration tests for each routing path

**Test Case 2.1**: PASS path
- **Input**: Evaluation result = PASS
- **Expected Output**: Orchestrator automatically invokes review-implementation and returns final report
- **Verification**: Check that review-implementation is called, final report contains required fields

**Test Case 2.2**: MINOR DEFECT path conditions
- **Input**: Evaluation result = MINOR IMPLEMENTATION DEFECT with:
  - Root cause clear
  - Defect localized
  - Specification valid
  - Verification criteria valid
  - Approved scope valid
  - Existing tests can validate fix
- **Expected Output**: Orchestrator invokes hotfix-issue, then re-evaluates (no approval required)
- **Verification**: Confirm hotfix-issue is called, re-evaluation occurs, approval not requested

**Test Case 2.3**: MINOR DEFECT path failure conditions
- **Input**: Evaluation result = MINOR IMPLEMENTATION DEFECT but:
  - Root cause unclear
  - Defect spans components
  - Specification invalid
  - Verification criteria invalid
  - Approved scope invalid
  - No tests can validate fix
- **Expected Output**: Orchestrator routes to COMPLEX ISSUE or HUMAN ESCALATION
- **Verification**: Confirm routing decision reflects conditions

**Test Case 2.4**: COMPLEX ISSUE path
- **Input**: Evaluation result = COMPLEX OR UNCLEAR ISSUE with:
  - Root cause unclear
  - Issue crosses multiple components
  - Architecture questionable
  - Specification incomplete
  - Verification criteria invalid
  - Scope questionable
  - Investigation produces concrete report
- **Expected Output**: Orchestrator invokes investigate-issue
- **Verification**: Confirm investigate-issue is called

**Test Case 2.5**: COMPLEX ISSUE → Requirement Change
- **Input**: COMPLEX ISSUE investigation concludes requirements/architecture/scope must change
- **Expected Output**: Workflow automatically returns to: specification → verification → tests → readiness → human approval → implementation
- **Verification**: Confirm routing to pre-approval stages, approval requested

**Test Case 2.6**: COMPLEX ISSUE → No Change
- **Input**: COMPLEX ISSUE investigation concludes no requirement/architecture/scope change needed
- **Expected Output**: Orchestrator re-evaluates (continues workflow)
- **Verification**: Confirm re-evaluation occurs, no approval requested

**Test Case 2.7**: HUMAN ESCALATION conditions
- **Input**: Evaluation result triggers HUMAN ESCALATION when:
  - Requirements conflict
  - Architectural decisions required
  - Approved scope must change
  - Autonomous repair unsafe
  - Repair cycles exhausted
  - Investigation cannot establish reliable root cause
  - Tests and specification disagree
- **Expected Output**: Orchestrator asks user for intervention, delivers evidence-based report containing:
  - Current state
  - Root cause/uncertainty
  - Attempted actions
  - Failed tests
  - Proposed options
  - Exact decision required
- **Verification**: Confirm user intervention requested, report contains all required fields

**Test Case 2.8**: HUMAN ESCALATION on insufficient data
- **Input**: Investigation cannot establish reliable root cause
- **Expected Output**: Orchestrator routes to HUMAN ESCALATION
- **Verification**: Confirm escalation path triggered

---

**FR-3: Autonomous Repair Loop Limit**

**Verification Method**: Unit test + integration test

**Test Case 3.1**: Repair counter increments
- **Input**: MINOR DEFECT repair attempted
- **Expected Output**: Repair counter increments by 1
- **Verification**: Check counter state after each repair

**Test Case 3.2**: Repair limit enforcement
- **Input**: MAX_AUTO_REPAIR_CYCLES = 2
- **Expected Output**: After 2 repair attempts, orchestrator stops, reports, and asks human
- **Verification**: Confirm STOP, REPORT, and ASK HUMAN occur after 2 repairs

**Test Case 3.3**: Counter resets on new approval
- **Input**: New approval cycle starts
- **Expected Output**: Repair counter resets to 0
- **Verification**: Confirm counter is 0 at start of new cycle

**Test Case 3.4**: Counter tracked per task
- **Input**: Multiple implementation tasks in parallel or sequential
- **Expected Output**: Each task has its own repair counter
- **Verification**: Verify isolation between tasks

**Test Case 3.5**: Default limit value
- **Input**: MAX_AUTO_REPAIR_CYCLES not specified
- **Expected Output**: Default value of 2 or 3 used
- **Verification**: Confirm default limit value in use

---

**FR-4: Approval Gate Protection During Repair**

**Verification Method**: Integration tests for each repair type

**Test Case 4.1**: Hotfix doesn't bypass approval for requirement changes
- **Input**: Hotfix changes requirements or scope
- **Expected Output**: Workflow returns to: specification → verification → tests → readiness → human approval
- **Verification**: Confirm routing, approval requested, implementation blocked until approval

**Test Case 4.2**: Hotfix doesn't bypass approval for architecture changes
- **Input**: Hotfix changes architecture
- **Expected Output**: Workflow returns to approval gate
- **Verification**: Confirm routing, approval requested

**Test Case 4.3**: Hotfix doesn't bypass approval for test expectation changes
- **Input**: Hotfix changes test expectations
- **Expected Output**: Workflow returns to approval gate
- **Verification**: Confirm routing, approval requested

**Test Case 4.4**: Localized scope changes allowed without approval
- **Input**: Hotfix is localized, scope remains unchanged
- **Expected Output**: Hotfix proceeds without approval
- **Verification**: Confirm hotfix executed, no approval requested

**Test Case 4.5**: No route bypasses verification → tests → readiness → approval
- **Input**: Any repair path
- **Expected Output**: All paths require verification → tests → readiness → approval before implementation continues
- **Verification**: Trace all repair paths, confirm preconditions met

---

**FR-5: Test-Driven Completion**

**Verification Method**: Integration test + manual inspection

**Test Case 5.1**: Final success requires all passes
- **Input**: Implementation completed, tests pass, verification passes, evaluation passes, review passes
- **Expected Output**: Workflow completes successfully
- **Verification**: Confirm all conditions met, workflow terminates

**Test Case 5.2**: Test failure prevents final success
- **Input**: Tests fail
- **Expected Output**: Workflow does NOT complete successfully
- **Verification**: Confirm test failure blocks completion

**Test Case 5.3**: Test failures treated as real implementation failures
- **Input**: Tests fail during implementation
- **Expected Output**: Orchestrator treats as implementation failure, routes appropriately
- **Verification**: Confirm routing reflects test failure as real issue

**Test Case 5.4**: No test weakening
- **Input**: Implementation has test failures
- **Expected Output**: Orchestrator does NOT weaken, remove, skip, or rewrite tests
- **Verification**: Inspect implementation, confirm tests unchanged

**Test Case 5.5**: Test integrity issue routing
- **Input**: Test is genuinely incorrect (specification/verification/test integrity issue)
- **Expected Output**: Orchestrator identifies as integrity issue and routes through appropriate change path
- **Verification**: Confirm routing decision reflects test integrity issue

---

**FR-6: Review Automation**

**Verification Method**: Integration test + manual inspection

**Test Case 6.1**: Review automatically invoked after PASS
- **Input**: Evaluation result = PASS
- **Expected Output**: review-implementation is automatically invoked
- **Verification**: Confirm review-implementation skill called

**Test Case 6.2**: Review report includes all required fields
- **Input**: Review completes successfully
- **Expected Output**: Report contains: what was implemented, specification compliance, verification results, test results, review findings, known limitations, any follow-up technical debt
- **Verification**: Inspect report, confirm all fields present

**Test Case 6.3**: Review report returned to user
- **Input**: Review completes successfully
- **Expected Output**: Report is returned to user
- **Verification**: Confirm report delivered to user

**Test Case 6.4**: No automatic milestone start
- **Input**: Review completes successfully
- **Expected Output**: Orchestrator does NOT automatically start new milestone
- **Verification**: Confirm no new milestone initiated

---

**FR-7: manage-development Full Lifecycle Orchestration**

**Verification Method**: Manual inspection + test

**Test Case 7.1**: Pre-approval stages executed
- **Input**: New approval cycle starts
- **Expected Output**: manage-development executes: generate-spec → generate-verification → generate-tests → readiness → approval
- **Verification**: Confirm stage sequence and execution

**Test Case 7.2**: Post-approval stages executed
- **Input**: After approval
- **Expected Output**: manage-development executes: implement → evaluate → repair/investigate/review
- **Verification**: Confirm stage sequence and execution

**Test Case 7.3**: Orchestrator owns sequencing
- **Input**: Any workflow stage
- **Expected Output**: Orchestrator determines and executes sequencing
- **Verification**: Confirm orchestrator controls stage order

**Test Case 7.4**: Orchestrator owns state management
- **Input**: Workflow progresses
- **Expected Output**: Orchestrator maintains and updates state
- **Verification**: Inspect state transitions

**Test Case 7.5**: Orchestrator owns preconditions
- **Input**: Each workflow stage
- **Expected Output**: Orchestrator verifies preconditions before executing
- **Verification**: Confirm precondition checks

**Test Case 7.6**: Orchestrator owns postconditions
- **Input**: Each workflow stage completes
- **Expected Output**: Orchestrator verifies postconditions
- **Verification**: Confirm postcondition checks

**Test Case 7.7**: Orchestrator owns routing
- **Input**: Evaluation result
- **Expected Output**: Orchestrator determines routing
- **Verification**: Confirm routing logic in orchestrator

**Test Case 7.8**: Orchestrator owns retry limits
- **Input**: Repair loops, retries
- **Expected Output**: Orchestrator enforces limits
- **Verification**: Confirm limit enforcement

**Test Case 7.9**: Orchestrator owns human gates
- **Input**: Escalation points
- **Expected Output**: Orchestrator requests human intervention at gates
- **Verification**: Confirm human gates positioned correctly

**Test Case 7.10**: Individual skills own domain work
- **Input**: Any skill invocation
- **Expected Output**: Each skill performs its domain-specific work
- **Verification**: Inspect skill implementations

**Test Case 7.11**: Orchestrator coordinates, doesn't rewrite
- **Input**: Any skill invocation
- **Expected Output**: Orchestrator invokes skills, does not rewrite their internal logic
- **Verification**: Confirm no skill internal logic changes

---

**FR-8: manage-roadmap Strategic Focus**

**Verification Method**: Manual inspection

**Test Case 8.1**: No execution lifecycle expansion
- **Input**: Post-approval workflow executes
- **Expected Output**: manage-roadmap does NOT expand into execution lifecycle
- **Verification**: Confirm manage-roadmap unchanged

**Test Case 8.2**: Strategic responsibilities maintained
- **Input**: Post-approval workflow executes
- **Expected Output**: manage-roadmap handles: roadmap state, milestone planning, milestone creation, decomposition, documentation, readiness for development
- **Verification**: Confirm manage-roadmap executes strategic responsibilities

**Test Case 8.3**: Handoff occurs correctly
- **Input**: Execution ready
- **Expected Output**: manage-roadmap → manage-development handoff
- **Verification**: Confirm handoff documented and executed

---

## Edge Cases

**Edge Case 1**: Empty implementation (no code written)
- **Input**: Implementation produces no changes
- **Expected Behavior**: Evaluation detects no implementation, routes appropriately (MINOR or COMPLEX)
- **Verification**: Test with implementation that produces no changes

**Edge Case 2**: Implementation succeeds but evaluation fails
- **Input**: Implementation completes without error, evaluation fails
- **Expected Behavior**: Orchestrator routes based on evaluation failure (MINOR, COMPLEX, or HUMAN)
- **Verification**: Test with successful implementation but failed evaluation

**Edge Case 3**: Concurrent implementation tasks
- **Input**: Multiple implementation tasks in parallel
- **Expected Behavior**: Each task has its own repair counter and state
- **Verification**: Test with parallel tasks

**Edge Case 4**: MAX_AUTO_REPAIR_CYCLES = 1
- **Input**: Limit set to 1
- **Expected Behavior**: First repair attempt triggers stop after limit reached
- **Verification**: Test with limit = 1

**Edge Case 5**: MAX_AUTO_REPAIR_CYCLES = 0
- **Input**: Limit set to 0
- **Expected Behavior**: Repair never allowed (invalid limit, should handle gracefully)
- **Verification**: Test with limit = 0, ensure proper error handling

**Edge Case 6**: Root cause conditions borderline (clear vs unclear)
- **Input**: MINOR defect with borderline root cause clarity
- **Expected Behavior**: Routing decision reflects borderline (may route to HUMAN if ambiguous)
- **Verification**: Test with borderline cases

**Edge Case 7**: Specification validity borderline (valid vs invalid)
- **Input**: MINOR defect with borderline specification validity
- **Expected Behavior**: Routing reflects borderline (may route to COMPLEX if specification questionable)
- **Verification**: Test with borderline specification validity

**Edge Case 8**: Architecture questionable borderline
- **Input**: COMPLEX issue with borderline architecture question
- **Expected Behavior**: Routing reflects borderline (may route to HUMAN if uncertain)
- **Verification**: Test with borderline architecture question

**Edge Case 9**: Tests validation capability borderline
- **Input**: MINOR defect with borderline test validation capability
- **Expected Behavior**: Routing reflects borderline (may route to COMPLEX if tests can't validate)
- **Verification**: Test with borderline test validation

**Edge Case 10**: Partial failure during evaluation
- **Input**: Evaluation starts but fails partway through
- **Expected Behavior**: Orchestrator handles partial failure gracefully
- **Verification**: Test with evaluation that fails midway

**Edge Case 11**: State corruption during workflow
- **Input**: Tool failure corrupts state
- **Expected Behavior**: State transitions robust against failures (resume/recovery from M4)
- **Verification**: Test with simulated state corruption

**Edge Case 12**: Human intervention timeout
- **Input**: HUMAN ESCALATION report sent, user doesn't respond
- **Expected Behavior**: Orchestrator waits indefinitely or has timeout mechanism
- **Verification**: Test with timeout scenarios

**Edge Case 13**: Requirements conflict detection borderline
- **Input**: MINOR defect with borderline requirements conflict
- **Expected Behavior**: Routing reflects borderline (may route to HUMAN if conflict unclear)
- **Verification**: Test with borderline requirements conflict

**Edge Case 14**: Approved scope must change borderline
- **Input**: Hotfix with borderline scope change
- **Expected Behavior**: Routing reflects borderline (may route to approval if scope questionable)
- **Verification**: Test with borderline scope change

**Edge Case 15**: Autonomous repair unsafe borderline
- **Input**: MINOR defect with borderline safety concerns
- **Expected Behavior**: Routing reflects borderline (may route to HUMAN if unsafe unclear)
- **Verification**: Test with borderline safety concern

**Edge Case 16**: Investigation produces contradictory findings
- **Input**: COMPLEX issue investigation produces contradictory conclusions
- **Expected Behavior**: Routing to HUMAN ESCALATION (uncertainty)
- **Verification**: Test with contradictory investigation results

**Edge Case 17**: Tests and specification disagree borderline
- **Input**: Evaluation shows tests passing but specification requires failure
- **Expected Behavior**: Routing to HUMAN ESCALATION (requires decision)
- **Verification**: Test with borderline test/specification disagreement

**Edge Case 18**: Test expectations change during repair loop
- **Input**: Hotfix changes test expectations
- **Expected Behavior**: Detected, routes to approval gate (FR-4)
- **Verification**: Test with test expectation change during repair

**Edge Case 19**: Implementation artifact missing
- **Input**: Approved artifacts not available to implementation
- **Expected Behavior**: Implementation fails gracefully, report error
- **Verification**: Test with missing artifacts

**Edge Case 20**: State not persisted between manual skill invocations
- **Input**: Workflow reaches manual skill invocation (e.g., human approval)
- **Expected Behavior**: State persists and resumes correctly
- **Verification**: Test with manual intervention, resume workflow

---

## Failure Scenarios

**Failure Scenario 1: Security - Unauthorized access to approval gate bypass**
- **Description**: Attempt to invoke implement-specification without going through verification → tests → readiness → approval
- **Verification**: Confirm no skill invocation path bypasses M4 approval gate
- **Test**: Try to invoke implement-specification directly, should fail

**Failure Scenario 2: Security - Silent requirement change**
- **Description**: Hotfix changes requirements without approval
- **Verification**: Confirm requirement-change detection in hotfix-issue
- **Test**: Modify requirement in hotfix, confirm approval gate triggered

**Failure Scenario 3: Security - Test weakening for green state**
- **Description**: Attempt to rewrite tests to hide implementation failures
- **Verification**: Confirm no test weakening or rewriting allowed
- **Test**: Try to modify tests, confirm blocked

**Failure Scenario 4: Reliability - State loss during partial failure**
- **Description**: Tool failure causes state loss during workflow
- **Verification**: Confirm state persists across failures (resume/recovery)
- **Test**: Simulate tool failure, confirm state restored

**Failure Scenario 5: Reliability - Invalid state transitions**
- **Description**: Attempt to transition to invalid state
- **Verification**: Confirm all state transitions validated
- **Test**: Attempt invalid transition, should fail

**Failure Scenario 6: Reliability - Race condition in parallel tasks**
- **Description**: Concurrent implementation tasks interfere with each other
- **Verification**: Confirm task isolation (separate repair counters, state)
- **Test**: Run parallel tasks, confirm isolation

**Failure Scenario 7: Performance - Evaluation routing too slow**
- **Description**: Routing decision takes > 1 second
- **Verification**: Confirm performance threshold (< 1 second)
- **Test**: Measure routing decision time

**Failure Scenario 8: Performance - Redundant artifact reading**
- **Description**: Orchestration reads same artifacts multiple times
- **Verification**: Confirm no unnecessary file I/O
- **Test**: Monitor artifact reads during workflow

**Failure Scenario 9: Maintainability - Orchestrator logic not modular**
- **Description**: Routing logic tightly coupled with other logic
- **Verification**: Confirm modular, testable design
- **Test**: Inspect code structure, confirm separation of concerns

**Failure Scenario 10: Maintainability - Human gates hidden**
- **Description**: Decision points not obvious to user
- **Verification**: Confirm gates are explicit and documented
- **Test**: Inspect user-facing documentation

**Failure Scenario 11: Usability - Escalation report missing information**
- **Description**: HUMAN ESCALATION report lacks required fields
- **Verification**: Confirm all required fields present
- **Test**: Trigger escalation, inspect report content

**Failure Scenario 12: Usability - User doesn't understand report**
- **Description**: Report too technical or confusing
- **Verification**: Confirm report is concise but evidence-based and understandable
- **Test**: Have user review report, ask for feedback

**Failure Scenario 13: Testability - Routing paths not testable in isolation**
- **Description**: Routing logic depends on global state
- **Verification**: Confirm all paths testable independently
- **Test**: Isolate routing paths, test individually

**Failure Scenario 14: Testability - Loop limit not independently verifiable**
- **Description**: Repair loop tracking embedded in complex logic
- **Verification**: Confirm independent, testable component
- **Test**: Test RepairLoopTracker separately

**Failure Scenario 15: Testability - Approval protection not testable**
- **Description**: Approval gate checks not easily testable
- **Verification**: Confirm independent, testable component
- **Test**: Test approval gate protection separately

**Failure Scenario 16: Extensibility - Hardcoded limits or paths**
- **Description**: MAX_AUTO_REPAIR_CYCLES or skill paths hardcoded
- **Verification**: Confirm configurable, no hardcoding
- **Test**: Test with different limits

**Failure Scenario 17: Extensibility - Skill paths hardcoded**
- **Description**: Skill invocation paths hardcoded
- **Verification**: Confirm configurable skill references
- **Test**: Test with different skill paths

**Failure Scenario 18: Error - MAX_AUTO_REPAIR_CYCLES = 0**
- **Description**: Invalid limit value causes errors
- **Verification**: Confirm graceful error handling
- **Test**: Test with limit = 0

**Failure Scenario 19: Error - Invalid state transition**
- **Description**: Attempting invalid transition causes crash
- **Verification**: Confirm robust error handling
- **Test**: Attempt invalid transition, ensure graceful failure

**Failure Scenario 20: Error - Missing implementation artifacts**
- **Description**: Implementation can't start due to missing artifacts
- **Verification**: Confirm graceful error reporting
- **Test**: Test with missing artifacts

**Failure Scenario 21: Error - Manual intervention timeout**
- **Description**: User doesn't respond to escalation within expected timeframe
- **Verification**: Confirm timeout mechanism or indefinite wait
- **Test**: Test with timeout scenarios

---

## Regression Checklist

**manage-development** (previously pre-implementation orchestrator)

- [x] Pre-implementation pipeline integrity maintained (M4)
- [x] Approval gate from M4 remains non-negotiable
- [x] Pipeline sequence enforcement maintained
- [x] Artifact validation maintained
- [x] Test readiness validation maintained
- [x] Resume/recovery patterns maintained
- [x] Lifecycle state machine maintained (7 states)
- [x] Pre-approval stages execute correctly: generate-spec → generate-verification → generate-tests → readiness → approval
- [x] New post-approval stages execute correctly: implement → evaluate → repair/investigate/review
- [x] Orchestrator sequencing control maintained
- [x] State management integration maintained

**manage-roadmap**

- [x] Handoff contract maintained (M4S1)
- [x] Strategic responsibilities maintained
- [x] No expansion into execution lifecycle

**Individual SDD Skills**

- [x] generate-spec internal logic unchanged
- [x] generate-verification internal logic unchanged
- [x] generate-tests internal logic unchanged
- [x] readiness internal logic unchanged
- [x] approve-spec internal logic unchanged
- [x] implement-specification internal logic unchanged
- [x] evaluate-implementation internal logic unchanged
- [x] review-implementation internal logic unchanged
- [x] hotfix-issue internal logic unchanged
- [x] investigate-issue internal logic unchanged

**Documentation**

- [x] AGENTS.md unchanged (unless requested update)
- [x] FRAMEWORK.md unchanged (unless requested update)
- [x] PLAYBOOK.md unchanged (unless requested update)
- [x] INDEX.md unchanged (unless requested update)
- [x] docs/SKILLS.md unchanged (unless requested update)

---

## Manual Validation

**Manual Validation 1**: Post-approval workflow end-to-end
1. Create new milestone with approved specification
2. Run approval gate (approve-spec skill)
3. Observe automatic execution of implement → evaluate → routing → repair/review
4. Verify no manual invocation between stages (except escalation)
5. Confirm workflow completes successfully or routes appropriately
6. **Expected**: Smooth continuous execution without interruptions

**Manual Validation 2**: Evaluation routing decision visualization
1. Trigger a post-approval workflow with known result types
2. Observe routing decisions for PASS, MINOR, COMPLEX, HUMAN paths
3. Verify each path executes correctly
4. Confirm reports are evidence-based and user-friendly
5. **Expected**: Clear routing, concise evidence-based reports

**Manual Validation 3**: Repair loop limit enforcement
1. Configure MAX_AUTO_REPAIR_CYCLES = 2
2. Create workflow with MINOR defects that fail on each attempt
3. Count repair attempts until limit reached
4. Verify workflow stops, reports, and asks human at limit
5. Reset counter, start new cycle
6. Verify counter resets to 0
7. **Expected**: Loop limit enforced, counter resets correctly

**Manual Validation 4**: Approval gate protection verification
1. Attempt to execute hotfix that changes requirements
2. Verify workflow returns to approval gate
3. Attempt to execute hotfix that changes architecture
4. Verify workflow returns to approval gate
5. Attempt localized scope change hotfix
6. Verify hotfix proceeds without approval
7. **Expected**: No silent requirement changes, approval requested appropriately

**Manual Validation 5**: Test-driven completion enforcement
1. Create workflow with test failures
2. Verify workflow does NOT declare success
3. Confirm test failures treated as real implementation failures
4. Inspect implementation, confirm no test weakening
5. **Expected**: Test failures block completion, no test weakening

**Manual Validation 6**: Review automation verification
1. Trigger workflow that evaluates to PASS
2. Observe automatic invocation of review-implementation
3. Inspect review report for required fields
4. Verify report returned to user
5. Confirm no automatic milestone start
6. **Expected**: Review automatically invoked, complete report, no milestone auto-start

**Manual Validation 7**: HUMAN ESCALATION report quality
1. Trigger scenario requiring human intervention
2. Review escalation report for:
   - Current state
   - Root cause/uncertainty
   - Attempted actions
   - Failed tests
   - Proposed options
   - Exact decision required
3. Assess clarity, conciseness, evidence-based nature
4. **Expected**: Report concise but evidence-based, all required fields present

**Manual Validation 8**: State persistence across manual intervention
1. Reach human intervention point in workflow
2. Wait (simulated by user stepping through)
3. Resume workflow from that point
4. Verify state persisted correctly
5. **Expected**: State preserved across manual intervention

**Manual Validation 9**: Orchestration ownership verification
1. Inspect code for:
   - Sequencing control (who decides stage order)
   - State management (who maintains state)
   - Preconditions (who verifies preconditions)
   - Postconditions (who verifies postconditions)
   - Routing logic (who determines routing)
   - Retry limits (who enforces limits)
   - Human gates (who requests intervention)
2. Confirm orchestration logic exists and is documented
3. Confirm individual skills maintain their internal logic
4. **Expected**: Clear separation of orchestration and skill responsibilities

**Manual Validation 10**: manage-roadmap strategic focus verification
1. Inspect manage-roadmap for any execution lifecycle responsibilities
2. Verify only strategic responsibilities remain
3. Confirm handoff to manage-development documented
4. **Expected**: No execution expansion, only strategic responsibilities

---

## Automated Validation

### Diff-Scope Verification (Pre-Merge Check)

**Command:** `git diff --name-only`

**Assertion:** The output of this command MUST strictly match the "Allowlist" defined in the Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

**Allowlist (Files permitted to change):**
- `skills/manage-development/SKILL.md`
- `skills/manage-development/README.md`

**Current Check:**
```bash
git diff --name-only
```

**Test Command (to be executed by evaluate-implementation):**
```bash
git diff --name-only
# Expected output:
# skills/manage-development/SKILL.md
# skills/manage-development/README.md
```

**Test Command (assertion):**
```bash
git diff --name-only | grep -vE "^skills/manage-development/(SKILL|README)\.md$" && exit 1
```

**Expected Result**: Exit code 1 (no out-of-scope files modified)

---

### Existing Tests

**M4S1 Tests** (should still pass):
- Pre-implementation pipeline integrity tests
- Approval gate validation tests
- Pipeline sequence enforcement tests
- Artifact validation tests
- Test readiness validation tests
- Resume/recovery tests
- Lifecycle state machine tests

**Test Command (run all M4 tests):**
```bash
# Placeholder - actual command from M4S1
bash tests/M4/test_orchestration_validation.sh
```

**Expected Result**: All M4S1 tests pass (23/23)

---

### New Tests Required

**Test Suite 1**: Post-Approval Workflow Orchestration

**File**: `tests/M5/test_post_approval_workflow.sh`

**Test Cases**:
1.1. Complete post-approval workflow execution (FR-1)
1.2. Implementation artifacts received by implementation (FR-1)
1.3. Success not declared on completion alone (FR-1)
1.4. Complete PASS path execution (FR-2)
1.5. Complete MINOR DEFECT path execution (FR-2)
1.6. MINOR DEFECT path with invalid conditions routes to COMPLEX (FR-2)
1.7. Complete COMPLEX ISSUE path execution (FR-2)
1.8. COMPLEX ISSUE with requirement change returns to approval (FR-2)
1.9. COMPLEX ISSUE without change continues workflow (FR-2)
1.10. Complete HUMAN ESCALATION path execution (FR-2)
1.11. HUMAN ESCALATION with all required report fields (FR-2)
1.12. HUMAN ESCALATION with insufficient data (FR-2)
1.13. Repair counter increments correctly (FR-3)
1.14. Repair limit enforced (FR-3)
1.15. Counter resets on new approval (FR-3)
1.16. Counter isolated per task (FR-3)
1.17. Hotfix doesn't bypass approval for requirement changes (FR-4)
1.18. Hotfix doesn't bypass approval for architecture changes (FR-4)
1.19. Hotfix doesn't bypass approval for test expectation changes (FR-4)
1.20. Localized scope changes proceed without approval (FR-4)
1.21. No path bypasses verification → tests → readiness → approval (FR-4)
1.22. Final success requires all passes (FR-5)
1.23. Test failures prevent final success (FR-5)
1.24. Test failures treated as real implementation failures (FR-5)
1.25. No test weakening in implementation (FR-5)
1.26. Test integrity issues routed correctly (FR-5)
1.27. Review automatically invoked after PASS (FR-6)
1.28. Review report includes all required fields (FR-6)
1.29. Review report returned to user (FR-6)
1.30. No automatic milestone start (FR-6)

**Test Command**:
```bash
bash tests/M5/test_post_approval_workflow.sh
```

**Expected Result**: All 30 tests pass

---

**Test Suite 2**: Routing Path Isolation Tests

**File**: `tests/M5/test_routing_paths.sh`

**Purpose**: Verify each routing path can be tested in isolation

**Test Cases**:
2.1. PASS path unit test
2.2. MINOR DEFECT path unit test
2.3. COMPLEX ISSUE path unit test
2.4. HUMAN ESCALATION path unit test
2.5. Routing decision isolation test

**Test Command**:
```bash
bash tests/M5/test_routing_paths.sh
```

**Expected Result**: All routing paths testable and pass

---

**Test Suite 3**: Repair Loop Tracker Unit Tests

**File**: `tests/M5/test_repair_tracker.sh`

**Purpose**: Verify RepairLoopTracker independently testable

**Test Cases**:
3.1. Increment counter
3.2. Get counter value
3.3. Check limit (counter < limit) → true
3.4. Check limit (counter >= limit) → false
3.5. Reset counter to 0
3.6. Max cycles = 2, counter = 0, increment → 1 (limit check passes)
3.7. Max cycles = 2, counter = 1, increment → 2 (limit check passes)
3.8. Max cycles = 2, counter = 2, increment → 3 (limit check fails)
3.9. Isolate counters between tasks

**Test Command**:
```bash
bash tests/M5/test_repair_tracker.sh
```

**Expected Result**: All 9 tests pass

---

**Test Suite 4**: Approval Gate Protection Tests

**File**: `tests/M5/test_approval_protection.sh`

**Purpose**: Verify approval gate protected during repair

**Test Cases**:
4.1. Detect requirement change, route to approval (FR-4)
4.2. Detect architecture change, route to approval (FR-4)
4.3. Detect test expectation change, route to approval (FR-4)
4.4. Allow localized scope change without approval (FR-4)
4.5. No bypass of verification → tests → readiness → approval (FR-4)
4.6. Pre-approval gate validation persists (M4 compliance)

**Test Command**:
```bash
bash tests/M5/test_approval_protection.sh
```

**Expected Result**: All 6 tests pass

---

**Test Suite 5**: Test-Driven Completion Tests

**File**: `tests/M5/test_test_driven_completion.sh`

**Purpose**: Verify test failures block completion

**Test Cases**:
5.1. Implementation + tests pass + verification pass + evaluation pass + review pass → success (FR-5)
5.2. Implementation complete + tests fail → no success (FR-5)
5.3. Tests fail during implementation → treated as real failure (FR-5)
5.4. Inspect implementation, no test weakening (FR-5)
5.5. Test integrity issue routed correctly (FR-5)
5.6. Test pass is necessary but not sufficient (requires evaluation + review)

**Test Command**:
```bash
bash tests/M5/test_test_driven_completion.sh
```

**Expected Result**: All 6 tests pass

---

**Test Suite 6**: Review Automation Tests

**File**: `tests/M5/test_review_automation.sh`

**Purpose**: Verify review-implementation automatically invoked

**Test Cases**:
6.1. Review invoked automatically after PASS (FR-6)
6.2. Review report contains required fields (FR-6)
6.3. Review report returned to user (FR-6)
6.4. No automatic milestone start (FR-6)
6.5. Review execution doesn't trigger additional routing (FR-6)

**Test Command**:
```bash
bash tests/M5/test_review_automation.sh
```

**Expected Result**: All 5 tests pass

---

**Test Suite 7**: Orchestration Ownership Tests

**File**: `tests/M5/test_orchestration_ownership.sh`

**Purpose**: Verify manage-development owns sequencing, state, routing

**Test Cases**:
7.1. Orchestrator determines stage order (FR-7)
7.2. Orchestrator manages state (FR-7)
7.3. Orchestrator verifies preconditions (FR-7)
7.4. Orchestrator verifies postconditions (FR-7)
7.5. Orchestrator determines routing (FR-7)
7.6. Orchestrator enforces retry limits (FR-7)
7.7. Orchestrator positions human gates (FR-7)
7.8. Individual skills maintain internal logic (FR-7)
7.9. Orchestrator coordinates, doesn't rewrite skills (FR-7)
7.10. Pre-approval stages executed correctly (FR-7)
7.11. Post-approval stages executed correctly (FR-7)

**Test Command**:
```bash
bash tests/M5/test_orchestration_ownership.sh
```

**Expected Result**: All 11 tests pass

---

**Test Suite 8**: manage-roadmap Strategic Focus Tests

**File**: `tests/M5/test_manage_roadmap_focus.sh`

**Purpose**: Verify manage-roadmap doesn't expand into execution lifecycle

**Test Cases**:
8.1. No execution lifecycle responsibilities (FR-8)
8.2. Strategic responsibilities maintained (FR-8)
8.3. Handoff to manage-development documented (FR-8)
8.4. Manage-roadmap unchanged (M4S1 compliance)

**Test Command**:
```bash
bash tests/M5/test_manage_roadmap_focus.sh
```

**Expected Result**: All 4 tests pass

---

**Test Suite 9**: Performance Tests

**File**: `tests/M5/test_performance.sh`

**Purpose**: Verify performance requirements

**Test Cases**:
9.1. Evaluation routing decision < 1 second (NFR-3)
9.2. Repair loop enforcement O(1) time (NFR-3)
9.3. No redundant artifact reading (NFR-3)
9.4. Routing decisions scalable to parallel tasks (NFR-3)
9.5. State management scalable to many tasks (NFR-3)

**Test Command**:
```bash
bash tests/M5/test_performance.sh
```

**Expected Result**: All 5 tests pass

---

**Test Suite 10**: Reliability Tests

**File**: `tests/M5/test_reliability.sh`

**Purpose**: Verify reliability requirements

**Test Cases**:
10.1. Handles partial failures gracefully (NFR-4)
10.2. State transitions robust against failures (NFR-4)
10.3. No data loss during state transitions (NFR-4)
10.4. Resume/recovery works after failures (NFR-4)
10.5. Isolated counters for parallel tasks (NFR-4)

**Test Command**:
```bash
bash tests/M5/test_reliability.sh
```

**Expected Result**: All 5 tests pass

---

**Test Suite 11**: Testability Tests

**File**: `tests/M5/test_testability.sh`

**Purpose**: Verify testability requirements

**Test Cases**:
11.1. All routing paths testable in isolation (NFR-6)
11.2. Repair loop limit independently verifiable (NFR-6)
11.3. Approval protection independently testable (NFR-6)
11.4. Test-driven completion independently testable (NFR-6)
11.5. Orchestration logic modular (NFR-2)

**Test Command**:
```bash
bash tests/M5/test_testability.sh
```

**Expected Result**: All 5 tests pass

---

**Test Suite 12**: Extensibility Tests

**File**: `tests/M5/test_extensibility.sh`

**Purpose**: Verify extensibility requirements

**Test Cases**:
12.1. MAX_AUTO_REPAIR_CYCLES configurable (NFR-7)
12.2. Repair loop limit in environment variable or config (NFR-7)
12.3. Routing thresholds configurable (NFR-7)
12.4. No hardcoding of skill paths (NFR-7)
12.5. No hardcoding of MAX_AUTO_REPAIR_CYCLES (NFR-7)

**Test Command**:
```bash
bash tests/M5/test_extensibility.sh
```

**Expected Result**: All 5 tests pass

---

**Test Suite 13**: Edge Case Tests

**File**: `tests/M5/test_edge_cases.sh`

**Purpose**: Verify edge case handling

**Test Cases**:
13.1. Empty implementation (no code)
13.2. Implementation succeeds but evaluation fails
13.3. Concurrent implementation tasks
13.4. MAX_AUTO_REPAIR_CYCLES = 1
13.5. MAX_AUTO_REPAIR_CYCLES = 0
13.6. Root cause borderline (clear vs unclear)
13.7. Specification validity borderline
13.8. Architecture questionable borderline
13.9. Tests validation capability borderline
13.10. Partial failure during evaluation
13.11. State corruption handling
13.12. Human intervention timeout
13.13. Requirements conflict borderline
13.14. Approved scope change borderline
13.15. Autonomous repair unsafe borderline
13.16. Investigation produces contradictory findings
13.17. Tests and specification disagree borderline
13.18. Test expectation change during repair
13.19. Implementation artifact missing
13.20. State persistence across manual intervention

**Test Command**:
```bash
bash tests/M5/test_edge_cases.sh
```

**Expected Result**: All 20 tests pass

---

**Test Suite 14**: Risk Mitigation Tests

**File**: `tests/M5/test_risk_mitigation.sh`

**Purpose**: Verify risk mitigations

**Test Cases**:
14.1. Approval gate not weakened (Risk #1)
14.2. Requirement-change detection works (Risk #2)
14.3. MAX_AUTO_REPAIR_CYCLES enforced (Risk #3)
14.4. Test failures = real failures (Risk #4)
14.5. No internal skill logic changes (Risk #5)
14.6. M4 approval gate verified intact (Risk #1)
14.7. Requirement changes require re-approval (Risk #2)
14.8. Limit is enforced (Risk #3)
14.9. Test failures prevent success (Risk #4)
14.10. Individual skills unchanged (Risk #5)
14.11. Allowlist compliance (Success Criteria #10)
14.12. Denylist compliance (Success Criteria #10)

**Test Command**:
```bash
bash tests/M5/test_risk_mitigation.sh
```

**Expected Result**: All 12 tests pass

---

### Test Execution Command

**Command to run all M5 tests**:
```bash
# Run all test suites
bash tests/M5/test_post_approval_workflow.sh
bash tests/M5/test_routing_paths.sh
bash tests/M5/test_repair_tracker.sh
bash tests/M5/test_approval_protection.sh
bash tests/M5/test_test_driven_completion.sh
bash tests/M5/test_review_automation.sh
bash tests/M5/test_orchestration_ownership.sh
bash tests/M5/test_manage_roadmap_focus.sh
bash tests/M5/test_performance.sh
bash tests/M5/test_reliability.sh
bash tests/M5/test_testability.sh
bash tests/M5/test_extensibility.sh
bash tests/M5/test_edge_cases.sh
bash tests/M5/test_risk_mitigation.sh

# Run M4 tests (regression)
bash tests/M4/test_orchestration_validation.sh

# Run diff-scope check
git diff --name-only
```

**Expected Result**: All 13 test suites pass, diff-scope check passes

---

## Expected Outcomes

**Observable Success**:

1. **Workflow Continuity**
   - Post-approval workflow executes smoothly from approval to completion without manual handoffs
   - Only human intervention at appropriate decision points (escalation)

2. **Automatic Routing**
   - Evaluation results automatically route to correct next step
   - Routing decisions are evidence-based and consistent with specification

3. **Loop Boundedness**
   - Repair loops stop at MAX_AUTO_REPAIR_CYCLES limit
   - Counter resets correctly for new cycles
   - No infinite loops occur

4. **Approval Gate Integrity**
   - No repair path silently bypasses approval gate
   - Requirement changes automatically route to approval
   - Approval gate from M4 remains non-negotiable

5. **Test-Driven Completion**
   - Tests pass is required for final success
   - Test failures block completion
   - No test weakening or rewriting occurs

6. **Review Automation**
   - Review-implementation automatically invoked after PASS
   - Complete evidence-based review report generated
   - Report returned to user
   - No automatic milestone start

7. **Orchestration Clarity**
   - manage-development clearly owns sequencing, state, routing, gates
   - Individual skills maintain their internal logic
   - No duplication or rewriting

8. **Strategic Focus**
   - manage-roadmap remains focused on strategic responsibilities
   - No expansion into execution lifecycle
   - Clear handoff to manage-development

9. **Evidence-Based Reports**
   - HUMAN ESCALATION reports are concise but evidence-based
   - Reports contain: current state, root cause/uncertainty, attempted actions, failed tests, proposed options, exact decision required
   - Users can make informed decisions

10. **Test Coverage**
    - All routing paths tested
    - Repair loop limit enforced and tested
    - Approval gate protection verified and tested
    - Test-driven completion enforced and tested

11. **Zero Breaking Changes**
    - All changes are additive or refactoring
    - Backward compatible with existing functionality
    - M4 pre-implementation integrity maintained

12. **Performance**
    - Evaluation routing decisions < 1 second
    - Repair loop enforcement O(1)
    - No redundant artifact reading
    - Scalable to parallel tasks

13. **Reliability**
    - Handles partial failures gracefully
    - State transitions robust
    - No data loss
    - Resume/recovery works

14. **Maintainability**
    - Orchestrator logic modular and testable
    - Routing decisions evidence-based
    - Human gates positioned clearly

15. **Testability**
    - All routing paths testable in isolation
    - Repair loop limit independently verifiable
    - Approval protection independently testable
    - Test-driven completion independently testable

16. **Extensibility**
    - Configurable limits
    - No hardcoding of paths or skills
    - Future-proof design

**Verification Indicators**:

- All 23 acceptance criteria satisfied
- All 13 test suites pass (100% pass rate)
- All edge cases handled correctly
- All failure scenarios detected appropriately
- All regression checklist items verified
- Manual validation passes
- Performance thresholds met
- Safety boundaries maintained
- Zero breaking changes introduced

---

**Completed work**: Verification protocol M5S1V created
