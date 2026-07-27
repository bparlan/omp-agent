# INGEST_ENTRIES

**Milestone**: M8S1
**Session**: M8S1SA1
**Date**: 2026-07-27
**Source**: M8S1 completion and review reports

## Ingestion Requirements

This document provides the required entries for canonical documentation ingestion via `/docs/ingest/`.

## Entry 1: Valid Evidence Concept

**Source**: M8S1.md (milestone definition)

**Category**: Concept / Architecture

**Path**: `docs/SPEC.md` (or appropriate architecture document)

**Content**:
```
Valid Evidence Lifecycle Concept (M8S1)

The OMP AEF introduces a mandatory validity gate that evaluates whether test failures are attributable to the intended subject before interpreting exit codes. This prevents false conclusions from tests that don't actually exercise the subject (self-scanning tests, wrong paths, dirty working trees, etc.).

Core Terminology:
- VALID_TEST: A test whose result exercised the intended subject and whose failure/success is attributable to that subject
- INVALID_TEST: A test whose result is not attributable to the intended subject — the pipeline must stop
- VALIDITY CHECK: The mandatory evaluation-time pre-processing step that classifies each test before interpreting its exit code

Six Validity Criteria:
1. The test exercised the intended subject (loaded, imported, or invoked the correct code path)
2. The failure is attributable to the subject (not infrastructure, config, or environment)
3. The test environment is deterministic (same inputs produce same results)
4. The working tree is clean (no uncommitted changes that could affect behavior)
5. The test does not scan itself (test script is not testing its own contents)
6. The failure message is diagnostic (identifies WHAT failed and WHY, not just an exit code)

Core Principle:
"Never advance the lifecycle based solely on test exit codes. First establish that the test itself is valid and that its failure is attributable to the intended subject."

For more details, see milestones/M8/M8S1.md and milestones/M8/M8S1V.md.
```

## Entry 2: Validity Gate Implementation

**Source**: M8S1C.md (completion report)

**Category**: Implementation

**Path**: `docs/IMPLEMENTATION.md` (or appropriate implementation document)

**Content**:
```
Validity Gate Implementation (M8S1)

Skills Modified:
- skills/evaluate-implementation/SKILL.md (v1.0.2 → v1.0.3)
  - Inserted Step 4 "Validate Test Results" before Step 5
  - Added VALID_TESTS/INVALID_TESTS counters
  - Documented exit code 2 for validity failures
  - Added human override mechanism for INVALID_TEST

- skills/generate-tests/SKILL.md (v1.1.0 → v2.0.0)
  - Added Step 3 "Add Self-Validity Assertions"
  - Defined core principle verbatim in skill instructions
  - Documented exit code 2 for validity failures
  - Extended to 8 steps from original 4
  - Provided mechanical check examples (file existence, module import, function existence, output inspection)

- skills/review-implementation/SKILL.md (v1.0.1 → v1.0.2)
  - Added Step 5 "Test Validity analysis"
  - Added "Test Valid?" column to compliance matrix
  - Added invalidation report recommendation logic
  - Documented distinction between "test is wrong" and "implementation is wrong"

Templates Modified:
- templates/evaluation_template.md
  - Added "Validity Gate Results" section (lines 16-25)
  - Added VALID_TESTS/INVALID_TESTS counters
  - Added invalidation reports table

- templates/review_template.md
  - Added "Test Validity" section (lines 47-59)
  - Added "Test Valid?" checkboxes
  - Added findings categories (test wrong vs implementation wrong)

- templates/test_template.md
  - Added "Validity Metadata" section (lines 12-17)
  - Added subject, acceptance criteria, expected failures, prerequisites fields

M7 Compatibility:
- TESTS_RUN/PASSED/FAILED/EXIT_CODE preserved unchanged
- Extended with VALID_TESTS/INVALID_TESTS for M8
- Exit code semantics: 0=PASS, 1=FAIL, 2=VALIDITY_FAILURE

Test Coverage:
- 5 meta-test scripts created in tests/M8/
- 14 test cases total, all passed (14/14)
- Validity criteria #1-#5 validated
- Exit code 2 properly distinguished from exit 1

For details, see milestones/M8/M8S1C.md.
```

## Entry 3: Meta-Test Suite

**Source**: M8S1T1.md (test plan)

**Category**: Testing

**Path**: `docs/TESTING.md` (or appropriate testing document)

**Content**:
```
Validity Gate Meta-Tests (M8S1)

Five meta-test scripts were created to validate the validity gate concept:

1. test_h_validity_gate_self_scan.sh (2 tests)
   - Validates criterion #5: test does not scan itself
   - Tests mock test that tries to scan its own contents
   - Verifies INVALID_TEST classification

2. test_i_validity_gate_wrong_path.sh (3 tests)
   - Validates criterion #1: test exercised intended subject
   - Tests invalid test with wrong subject path
   - Verifies INVALID_TEST classification

3. test_j_validity_gate_valid_test.sh (3 tests)
   - Negative test for valid tests
   - Verifies valid tests are NOT invalidated
   - Tests file existence, module import, function existence checks

4. test_k_validity_gate_dirty_tree.sh (3 tests)
   - Validates criterion #4: working tree is clean
   - Tests git operations on dirty working tree
   - Verifies validity gate fails on uncommitted changes

5. test_l_self_validity_exit_code_2.sh (3 tests)
   - Verifies exit code 2 for validity failures
   - Tests exit code distinctness from test failure (exit 1)
   - Validates error message format

Results: 14/14 tests passed (100%)
Wall time: 2.13 seconds

For details, see tests/M8/ and milestones/M8/M8S1T1.md.
```

## Entry 4: Review Report

**Source**: M8S1R.md (review report)

**Category**: Review

**Path**: `docs/REVIEW.md` (or appropriate review document)

**Content**:
```
M8S1 Review Report

Milestone: M8S1 — Valid Evidence
Review Status: ACCEPTABLE
Date: 2026-07-27
Review Report: milestones/M8/M8S1R.md (18,639 bytes)

Functional Requirements:
- 11/11 functional requirements (FR-1 through FR-7, plus NFRs) fully implemented ✅
- FR-1.1: VALID_TEST, INVALID_TEST, VALIDITY CHECK terminology defined ✅
- FR-1.2: Six validity criteria documented ✅
- FR-1.3: Core principle verbatim in AGENTS.md ✅
- FR-2.1: Mandatory validity check before test interpretation ✅
- FR-2.2: Three verdicts (VALID_TEST, INVALID_TEST, UNCERTAIN) ✅
- FR-2.3: Invalidation report fields defined ✅
- FR-2.4: Validity check before pass/fail interpretation ✅
- FR-3.1: Self-validity assertion requirement added ✅
- FR-3.2: Mechanical check examples provided ✅
- FR-3.4: Validity failure exit message and exit code 2 ✅
- FR-5.1: Validity Metadata section in test plan ✅
- FR-5.2: Validity metadata in executable test headers ✅
- FR-6.1: Test Validity section in review ✅
- FR-6.2: Distinguish test wrong vs implementation wrong ✅
- FR-6.3: Test Valid? column in compliance matrix ✅
- FR-7.1: Core principle verbatim in documentation ✅
- FR-7.2: Core principle is literal text ✅
- FR-7.3: Valid Evidence concept documented ✅
- NFR-1: Determinism preserved ✅
- NFR-3: M7 output format preserved ✅
- NFR-4: Human override mechanism documented ✅
- NFR-5: No test framework changes ✅

Test Coverage:
- 14 meta-test cases, all passed (14/14) ✅
- All validity criteria #1-#5 validated ✅
- Exit code 2 properly distinguished from exit 1 ✅

Test Validity: All 14 meta-tests classified as VALID ✅

No blocking issues found. Implementation is production-ready.

For details, see milestones/M8/M8S1R.md.
```

---

**Total Entries**: 4
**Source Documents**: M8S1.md, M8S1C.md, M8S1T1.md, M8S1R.md
**Status**: Ready for ingestion
