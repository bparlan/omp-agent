- # Changelog
-
- This document tracks changes to the OhMyPi (OMP) Framework.
-
- All significant changes will be recorded here chronologically.
-
- ### Infrastructure & Session Management
-
- - **Health Monitoring System**: New `skills-auditor` Python script for automated health monitoring of evolve-skills dependencies. Audits 13 skills, generates YAML health reports, and provides console dashboard.
- - **Skills-Auditor**: Automated quality monitoring with priority levels (HIGH/MEDIUM/LOW), status values (CRITICAL/NEEDS_IMPROVEMENT/HEALTHY), and health reports for all 13 evolve-skills dependencies.
- - **Evolve-Skills Health Audit Layer**: New Phase 4 in evolve-skills that adds automated dependency health monitoring, session-audit integration, and "Every Session" workflow.
- - **Skills-Auditor Playbook**: New operational workflows documentation including "Every Session" workflow, single-skill audit instructions, and health report structure documentation.
- - **Framework Documentation Updates**: Added comprehensive documentation to PLAYBOOK.md, FRAMEWORK.md, and skills.md covering session-audit, evolve-skills, and skills-auditor integrations.
- - **Health Dashboard**: Console interface for quick status overview showing CRITICAL/NEEDS_IMPROVEMENT/HEALTHY skills with priority and issue counts.
- - **13 Health Reports**: Generated YAML reports in `evolve-skills/health/{skill-name}.yaml` containing skill metadata, issues, recommendations, and overall status.
-
- ### The Mechanism (M3S2)
-
- - **Uncertainty Marker**: `#NEEDS-CLARIFICATION: <specific missing fact>` marker codified in FRAMEWORK.md, AGENTS.md, and implement-specification SKILL.md with HALT-on-guessing rule.
- - **Zero-Trust Review**: Standing rule "Assume the prior report is wrong" added to review-implementation SKILL.md. Live State Verification section added to review_template.md.
- - **Evidence-Based Debugging**: "Debug from evidence, never from memory" rule added to investigate-issue and evaluate-implementation SKILL.md files.
- - **Raw Evidence Mandate**: "## Raw Evidence" sections with exact command + raw output template appended to completion_template.md and evaluation_template.md.
- - **Ground-Truth Utility**: `bin/ground-truth-check.sh` — new read-only POSIX shell utility for live-state verification (5 commands, zero write operations).
- - **Mechanical Tooling Stack**: bootstrap-project mandates 4 tooling categories (Environment Manager, Linter/Formatter, Pre-commit, Type Checker) during project setup. Codified in AGENTS.md.
- - **Version Bumps**: review-implementation 1.1.0, evaluate-implementation 1.0.2, investigate-issue 1.0.1, implement-specification 1.0.1, bootstrap-project 1.0.2.

### Restore Determinism (M7)

- **generate-tests v2.0.0**: Complete rewrite with hard boundary guardrails, test-first enforcement, language-specific executable test rules, and machine-readable output. Includes 5-category file classification (TEST_ARTIFACT, TEST_FIXTURE, TEST_HELPER, PRODUCTION_IMPLEMENTATION, DOCUMENTATION) with STOP-and-report Guardrail Breach Protocol.
- **Test-validity precondition**: implement-specification v1.0.2 now requires test-validity validation before implementation. Tests are classified as Valid failure, Invalid test, or Pre-implementation pass before implementation begins.
- **Failure classification**: evaluate-implementation v1.0.3 now classifies each failure (Valid, Invalid, Environment, Specification Mismatch) before fixing. Only valid failures trigger implementation fixes.
- **Meta-tests A–G**: New test suite in `tests/M7/` validates generate-tests behavior: executable files, initial failure, production boundary, pseudo-code detection, implementation snippets, artifact preservation, and no-implementation-on-failure.
- **Investigation report**: Root cause analysis in `milestones/M7/M7INVESTIGATION.md` answering 7 questions about test/implementation boundary contamination.
- **Lifecycle postmortem**: 10 architectural findings preserved in M7SA1.md covering test validity, isolated baselines, platform assumptions, meta-test vs project test distinction, and lifecycle precondition gates.
- **Version bumps**: generate-tests 2.0.0, implement-specification 1.0.2, evaluate-implementation 1.0.3.

### Valid Evidence (M8S1)

- **evaluate-implementation v1.0.3**: Validity gate implementation with 5 validity criteria, self-validity assertions, INVALID_TEST classification, and exit code 2 semantics for validity failures.
- **review-implementation v1.0.2**: Validity analysis capability to distinguish "test is wrong" from "implementation is wrong".
- **generate-tests v2.0.0**: Meta-test suite (tests H–L) validating 5 validity criteria: correct subject path, self-validity check, clean working tree, exit code 2 on validity failure, negative test for valid tests.
- **Meta-test suite**: 14/14 tests passed (100%): test_h_validity_gate_self_scan.sh (2 tests), test_i_validity_gate_wrong_path.sh (3 tests), test_j_validity_gate_valid_test.sh (3 tests), test_k_validity_gate_dirty_tree.sh (3 tests), test_l_self_validity_exit_code_2.sh (3 tests).
- **Lifecycle formalization**: VALID_TESTS/INVALID_TESTS counters, exit code 2 as validity failure indicator, test-validity gate as mandatory pre-processing step.
- **M7 compatibility**: Preserved test exit codes (0=PASS, 1=FAIL) and backward compatibility.
- **Session Audit**: M8S1SA1 generated with comprehensive inventory of 17 modified files and 5 created files, plus 7 milestone artifacts and 5 session audit reports.
