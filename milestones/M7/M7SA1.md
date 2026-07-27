# Session Audit Report M7SA1

## Session Metadata
- **Date**: 2026-07-27
- **Session ID**: SA1
- **Milestone**: M7 (Restore Determinism — Repair `generate-tests` Test-First Integrity)
- **Session Type**: Full SDD lifecycle execution
- **Duration**: Single session (all phases: spec → verification → tests → implement → evaluate → review)

## Lifecycle Phases Completed

| Phase | Artifact | Status |
|-------|----------|--------|
| Milestone definition | `milestones/M7/M7.md` | ✅ |
| generate-spec | `milestones/M7/M7S1.md` | ✅ Approved |
| generate-verification | `milestones/M7/M7S1V.md` | ✅ |
| generate-tests | `milestones/M7/M7S1T1.md` + `tests/M7/test_*.sh` | ✅ (with test repairs C/D/E) |
| approve-spec | User approval stamped on M7S1.md | ✅ |
| implement-specification | `skills/generate-tests/SKILL.md` v1.1.0 → v2.0.0 | ✅ |
| evaluate-implementation | `milestones/M7/M7S1E.md` | ✅ (7/7 tests pass) |
| review-implementation | `milestones/M7/M7S1R.md` | ✅ |
| M7 lifecycle postmortem | This document (M7SA1) | ✅ |

## Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| `skills/generate-tests/SKILL.md` | MAJOR | v1.1.0 → v2.0.0: Added file classification guardrails, test-first enforcement, language-specific rules, machine-readable output, guardrail breach protocol |
| `tests/M7/test_c_no_production_files.sh` | FIX | Repaired: replaced working-tree git diff with isolated temp repository |
| `tests/M7/test_d_no_pseudo_code.sh` | FIX | Repaired: replaced self-scanning with isolated fixture directory |
| `tests/M7/test_e_no_implementation_snippets.sh` | FIX | Repaired: replaced self-scanning with isolated fixtures + external patterns file |
| `tests/M7/test_g_no_implementation_on_failure.sh` | FIX | Fixed false-positive grep on negative instructions |
| `milestones/M7/M7INVESTIGATION.md` | CREATED | Investigation report — 7-question root cause analysis |
| `milestones/M7/M7S1C.md` | CREATED | Implementation completion report |
| `milestones/M7/M7S1E.md` | CREATED | Evaluation report |
| `milestones/M7/M7S1R.md` | CREATED | Review report |
| `milestones/M7/M7S1.md` | STAMPED | User Approval stamp added |
| `milestones/M7/M7SA1.md` | CREATED | This document |
| `milestones/M7/SESSION_CHANGES.md` | CREATED | Change log |
| `milestones/M7/CHANGELOG_ENTRIES.md` | CREATED | Changelog entries |
| `milestones/M7/MILESTONE_UPDATES.md` | CREATED | Milestone updates |
| `milestones/M7/INGEST_ENTRIES.md` | CREATED | Ingestion entries |

## Classification
- **Major Changes**: 1 — `skills/generate-tests/SKILL.md` full rewrite
- **Minor/Fix Changes**: 4 — Test C, D, E, G repairs
- **Documentation Changes**: 6 — Investigation, completion, evaluation, review reports + this audit + changelog

## Code-Search Analysis

### Framework Changes Detected
- [x] Agent handoff patterns updated in generate-tests SKILL.md
- [x] Template usage verified (test_template.md unchanged)
- [x] Negative guardrails enforced (Guardrail Breach Protocol)
- [x] File classification boundary added to process flow
- [x] Test-first lifecycle enforcement added

### Infrastructure Skills Usage
- [x] generate-tests updated to v2.0.0
- [ ] session-audit invoked (this document)
- [ ] evolve-skills pending (recommended)
- [ ] manage-roadmap pending (ingestion entries produced)

### Milestone Progress
- M7 completion: **100%**
- Current phase: **Complete — awaiting archive**
- Remaining tasks: 0

---

## Lifecycle Postmortem: Architectural Findings

The M7 lifecycle revealed 10 architectural lessons that extend beyond this milestone. These are preserved as **canonical architectural findings** for the OMP AEF framework.

### Finding 1: Test Failure != Valid Evidence

A failing test is not automatically meaningful. The failure may be in:
- The implementation (expected — test found a real bug)
- The test itself (test has a defect → false positive or false negative)
- The environment (platform differences, pre-existing state)
- The specification (mismatch between spec, verification, and test expectations)

**Rule**: Before attributing a test failure to missing implementation, establish that the test is valid. Invalid tests are noise, not evidence.

### Finding 2: Test Validity Must Be Established Before Interpreting Failures

The M7 precondition check (before implement-specification) correctly identified that Tests C, D, E failed for the *wrong* reason. This validation gate prevented:
- Fixing implementation to satisfy an invalid test
- Accepting false evidence as proof of missing functionality
- Wasting time debugging a healthy system against defective tests

**Rule**: A "test-first" requirement is incomplete without a "test-validity" precondition. The lifecycle must distinguish:
1. Test validity check (does the test correctly test what it intends to test?)
2. Test execution (does the implementation pass the valid test?)
3. Evidence interpretation (what does the result mean?)

### Finding 3: Test Harnesses Must Never Scan Themselves

Tests D and E both scanned their own source code, creating self-referencing false positives:
- Test D's forbidden Python patterns existed in its own grep expressions
- Test E's forbidden implementation patterns existed in its own pattern array

**Rule**: Every meta-test must define two paths:
- `SUBJECT_PATH` — what the test validates (isolated fixture or target system)
- `HARNESS_PATH` — the test itself (explicitly excluded from scanning)

The test must assert that `HARNESS_PATH` is never inspected.

### Finding 4: Tests Requiring Repository State Need Isolated Baselines

Test C failed because it examined the user's working tree `git diff`, which included pre-existing unstaged changes from prior sessions. The working tree is not a valid baseline — it is contaminated by the session history.

**Rule**: Any test that validates repository state changes must:
1. Create an isolated temporary repository
2. Establish a known clean baseline commit
3. Execute the operation under test
4. Compare state against the baseline, not the user's working tree

Using `mktemp`, `git init`, `git add -A`, `git commit -m baseline` is the canonical pattern.

### Finding 5: Platform Assumptions Matter

Test C used a grep regex pattern (`\b`) that is valid on GNU grep (Linux) but invalid on BSD grep (macOS). This caused a runtime error on the development machine.

**Rule**: All test scripts must be tested on the target platform. Framework conventions must document platform assumptions. Platform-specific constructs must be avoided or guarded with conditional logic. The standard approach is to test on the development platform (macOS in this case) and avoid GNU-only extensions.

### Finding 6: Meta-Tests and Generated Project Tests Are Different Layers

M7's Tests A–G are *meta-tests* — they test the behavior of the `generate-tests` skill itself, not a feature implemented by the skill. This is different from *project tests* (e.g., M5's `test_*.py` files that test artifact type resolution).

**Rule**: Meta-tests and project tests have different validity criteria:
- **Project test**: Must initially fail (test-first) against unimplemented features
- **Meta-test**: Must produce valid evidence. May pass if the behavior under test is already correct

The "must initially fail" invariant applies to project tests, not meta-tests. For meta-tests, the invariant is "must produce valid evidence."

### Finding 7: The Orchestrator Must Not Infer Artifact Type from Filenames

The M7S1 specification references `tests/M7/test_*.sh` files. The orchestrator (this agent) must determine what these files test by reading them, not by inferring from their existence in the `tests/` directory. A file in `tests/M7/` could be:
- A project test for M7 features
- A meta-test for the `generate-tests` skill
- A test fixture
- A runner script

**Rule**: Artifact type must be determined by explicit metadata or content analysis, not by directory convention alone. This is consistent with the M6 canonical artifact model.

### Finding 8: Existing Artifacts Must Be Treated as Protected State

Throughout M7, a strict immutability boundary was maintained around M3–M6 artifacts. This prevented accidental corruption of existing milestone state during remediation work. The boundary was verified by checksum comparison before and after each phase.

**Rule**: Any lifecycle phase that modifies shared framework components must:
1. Capture baseline state (checksums, file inventory) before modification
2. Verify no changes to protected paths after modification
3. Fail if any protected artifact changed, was deleted, or was renamed

This protects against the "unknowing corruption" failure mode where a change to one milestone silently damages another.

### Finding 9: Implementation Must Never Be Inferred as the Next Step Solely from a Failed Test

The M7 precondition check stopped the pipeline when tests failed for invalid reasons. A naive orchestrator might interpret "tests fail → need implementation" as the universal pattern and proceed to implement against defective tests.

**Rule**: The lifecycle must require test validity confirmation before proceeding to implementation:
1. Tests fail → classify failure reason (valid/invalid)
2. Valid failure → proceed to implementation
3. Invalid failure → stop, fix tests, re-validate
4. Test passes (pre-implementation) → warning, investigation, stop

This prevents the "fixing the tests by implementing" anti-pattern.

### Finding 10: A Lifecycle Transition Needs Validated Preconditions

Each phase transition in the SDD lifecycle must validate its preconditions before starting:
- generate-tests → implement-specification: tests must exist, be executable, and produce valid evidence
- implement-specification → evaluate-implementation: implementation must complete without errors
- evaluate-implementation → review-implementation: evaluation evidence must be complete

**Rule**: Every lifecycle phase must define:
1. Input precondition (what must be true before starting)
2. Output postcondition (what must be true after completing)
3. Validation gate (how to check both)
4. Fallback action (what to do if validation fails)

M7 demonstrated this with the test-validity gate before implementation — a pattern that should be formalized in the lifecycle orchestration.

---

## Recommended evolve-skills Actions

1. **[HIGH] generate-tests** — Update version number to 2.0.0 (already done in SKILL.md header)
2. **[HIGH] implement-specification** — Add test-validity precondition check before proceeding to implementation (Finding 2, Finding 10)
3. **[MEDIUM] evaluate-implementation** — Add logic to distinguish valid failures from invalid test failures (Finding 1)
4. **[MEDIUM] Framework documentation** — Preserve the 10 architectural findings as canonical lifecycle rules in FRAMEWORK.md or a dedicated ARCHITECTURE.md
5. **[LOW] test_template.md** — Consider removing Python-in-bash example code block; replace with text-only description
6. **[LOW] Meta-test conventions** — Codify the isolated-fixture pattern and harness/subject separation as a testing convention

## Dependencies
- M7SA1 (this document)
- None

## Status
- [x] Analysis complete
- [x] M7 lifecycle postmortem documented
- [x] 10 architectural findings preserved
- [x] SA document generated
- [x] Recommended evolve-skills actions provided
- [x] Awaiting evolve-skills processing
