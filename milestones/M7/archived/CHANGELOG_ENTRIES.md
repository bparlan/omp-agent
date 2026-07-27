# Changelog Entries — M7

| Property | Value |
|----------|-------|
| Session | SA1 |
| Milestone | M7 |
| Date | 2026-07-27 |

## Added

- **generate-tests skill v2.0.0**: Added file classification guardrails (5-category system: TEST_ARTIFACT, TEST_FIXTURE, TEST_HELPER, PRODUCTION_IMPLEMENTATION, DOCUMENTATION)
- **generate-tests skill v2.0.0**: Added test-first enforcement — generated tests are executed before completion, exit codes captured, failure expected
- **generate-tests skill v2.0.0**: Added language-specific executable test requirements with cross-language prohibition
- **generate-tests skill v2.0.0**: Added Guardrail Breach Protocol — exact halt-and-report procedure for production path violations
- **generate-tests skill v2.0.0**: Added machine-readable output contract (TESTS_RUN, TESTS_PASSED, TESTS_FAILED, EXIT_CODE)
- **Investigation**: `milestones/M7/M7INVESTIGATION.md` — 7-question root cause analysis of test/implementation boundary contamination
- **Lifecycle postmortem**: `milestones/M7/M7SA1.md` — 10 architectural findings preserved as canonical lifecycle rules

## Changed

- **generate-tests skill v1.1.0 → v2.0.0**: Process expanded from 3 steps to 8 steps with mandatory classification, syntax validation, test execution, and machine-readable output
- **generate-tests skill v1.1.0 → v2.0.0**: "Out of Scope" section strengthened with denylist paths and explicit prohibition of `implement-specification` invocation
- **M7S1 specification**: User Approval stamp appended

## Fixed

- **Test C** (`test_c_no_production_files.sh`): Replaced working-tree git diff with isolated temporary repository baseline
- **Test D** (`test_d_no_pseudo_code.sh`): Replaced self-scanning with isolated fixture directory; harness excluded from scan
- **Test E** (`test_e_no_implementation_snippets.sh`): Replaced self-scanning with isolated fixtures and external patterns file
- **Test G** (`test_g_no_implementation_on_failure.sh`): Fixed false-positive grep on negative instructions ("Do NOT invoke" incorrectly matched as affirmative invocation)
