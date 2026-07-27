# CHANGELOG_ENTRIES

**Milestone**: M8S1
**Session**: M8S1SA1
**Date**: 2026-07-27

## Valid Evidence Lifecycle Concept (M8S1)

### Added
- **AGENTS.md**: Added "Valid Evidence" section defining VALID_TEST, INVALID_TEST, VALIDITY CHECK terminology and six validity criteria (lines 56-76)
- **skills/evaluate-implementation/SKILL.md**: Inserted Step 4 "Validate Test Results" before Step 5; added VALID_TESTS/INVALID_TESTS counters; documented exit code 2 for validity failures (v1.0.2 → v1.0.3)
- **skills/generate-tests/SKILL.md**: Added Step 3 "Add Self-Validity Assertions"; defined core principle verbatim; extended to 8 steps from original 4 (v1.1.0 → v2.0.0)
- **skills/review-implementation/SKILL.md**: Added Step 5 "Test Validity analysis"; added "Test Valid?" column to compliance matrix; added invalidation report recommendation logic (v1.0.1 → v1.0.2)
- **templates/evaluation_template.md**: Added "Validity Gate Results" section (lines 16-25); added VALID_TESTS/INVALID_TESTS counters; added invalidation reports table
- **templates/review_template.md**: Added "Test Validity" section (lines 47-59); added "Test Valid?" checkboxes; added findings categories (test wrong vs implementation wrong)
- **templates/test_template.md**: Added "Validity Metadata" section (lines 12-17); added subject, acceptance criteria, expected failures, prerequisites fields

### Created
- **tests/M8/test_h_validity_gate_self_scan.sh**: 2/2 tests passed — validates criterion #5 (test does not scan itself)
- **tests/M8/test_i_validity_gate_wrong_path.sh**: 3/3 tests passed — validates criterion #1 (correct subject path)
- **tests/M8/test_j_validity_gate_valid_test.sh**: 3/3 tests passed — negative test for valid tests
- **tests/M8/test_k_validity_gate_dirty_tree.sh**: 3/3 tests passed — validates criterion #4 (clean working tree)
- **tests/M8/test_l_self_validity_exit_code_2.sh**: 3/3 tests passed — verifies exit code 2 for validity failures
- **M8S1E.md**: Evaluation report (14/14 tests passed, 2.13 seconds)
- **M8S1R.md**: Review report (18,639 bytes, ACCEPTABLE status)

### Fixed
- None — no bugs found requiring fixes

### Deprecated
- None

### Removed
- None

### Updated
- **M8S1.md**: Completed milestone definition with Valid Evidence concept
- **M8S1C.md**: Completion report documenting all 11 functional requirements implemented
- **M8S1V.md**: Verification protocol defining 9 edge cases and test coverage

---

**Total Changes**: 18 files modified, 5 new test scripts created, 3 milestone artifacts generated
