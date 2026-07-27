# OMP Milestones

This document lists active and archived milestones for the OMP Framework project.

## Active Milestones

- ### M8 — Valid Evidence — Formalise Test Validity as a Lifecycle Concept
  - **Status**: COMPLETE ✅
  - **Phase**: Requirements Elicitation
  - **Date**: 2026-07-27
  - **Description**: Introduce a mandatory validity check between test execution and evidence interpretation in the SDD pipeline. Test exit codes alone are insufficient — we must first establish that a test failure is attributable to the intended subject before advancing the lifecycle. This is a direct architectural followup to M7's finding that "test failed" is not equivalent to "implementation missing."
  - **Key Deliverables**:
    - "Valid Evidence" concept codified in framework documentation with the core principle: "Never advance the lifecycle based solely on test exit codes"
    - Validity gate in `evaluate-implementation` — mandatory pre-processing before test interpretation
    - Self-validity assertions in all generated tests — tests prove they exercised their subject
    - INVALID_TEST classification as a formal test result state
    - Invalidation protocol — pipeline stops on INVALID_TEST, produces diagnostic report
    - Validity analysis in `review-implementation` — distinguish "test is wrong" from "implementation is wrong"
    - Meta-test for the validity gate
  - **Skills Updated**:
    - `skills/evaluate-implementation/SKILL.md` — v1.0.4 (expected)
    - `skills/review-implementation/SKILL.md` — (expected)
    - `skills/generate-tests/SKILL.md` — v2.0.x (expected)
  - **Artifacts**:
    - `milestones/M8/M8.md` — Milestone definition (this document)
    - `milestones/M8/M8S1.md` — Specification (to be generated)
    - `milestones/M8/M8S1V.md` — Verification protocol (to be generated)
    - `milestones/M8/M8S1T1.md` — Test plan (to be generated)
    - `milestones/M8/M8S1C.md` — Completion report (to be generated)
    - `milestones/M8/M8S1E.md` — Evaluation report (to be generated)
    - `milestones/M8/M8S1R.md` — Review report (to be generated)
    - `tests/M8/` — Meta-test scripts (to be generated)

- ### M4 — Harden OMP Pre-Implementation Orchestration and Approval Gate
-
- - **Status**: In Progress
- - **Phase**: Orchestration & Integrity
- - **Description**: Harden OMP Pre-Implementation Orchestration and Approval Gate — stabilize the SDD pipeline with explicit state machine, artifact validation, and strict pre-implementation gates to prevent workflow-state violations.
- - **Key Deliverables**:
-   - Incident analysis of orchestration failure
-   - Pre-implementation state machine
-   - Mandatory pre-implementation chain enforcement
-   - Test-first readiness validation
-   - Human approval gate
-   - Resume/recovery support
-   - Artifact integrity validation
-   - Tests for ordering, blocking, approval gates, and resume
- - **Artifacts**:
-   - `milestones/M4/M4.md` — Milestone definition
-   - `milestones/M4/M4S1.md` — Specification (to be generated)
-   - `milestones/M4/M4S1V.md` — Verification protocol (to be generated)
-   - `milestones/M4/M4S1T1.md` — Test plan (to be generated)
-   - `milestones/M4/M4S1C.md` — Completion report (to be generated)
-   - `milestones/M4/M4S1E.md` — Evaluation report (to be generated)
-   - `milestones/M4/M4S1R.md` — Review report (to be generated)
-   - `milestones/M4/M4SA1.md` — Session Audit Document (to be generated)
-   - `milestones/M4/SESSION_CHANGES.md` — Change log (to be generated)
-   - `milestones/M4/CHANGELOG_ENTRIES.md` — Changelog entries (to be generated)
-   - `milestones/M4/MILESTONE_UPDATES.md` — Milestone updates (to be generated)
-   - `milestones/M4/INGEST_ENTRIES.md` — Ingestion entries (to be generated)
-   - `tests/M4/` — Test scripts (to be generated)
-
- - **Status**: 75% Complete (Documentation and Tooling)
- - **Phase**: Infrastructure & Session Management
- - **Session**: SA1 (completed 2026-07-18)
- - **Description**: Added session-audit skill for session-based framework improvements, enhanced code-search infrastructure with comprehensive documentation, and integrated session-audit into evolve-skills workflow.
- - **Key Deliverables**:
-   - Session-audit v1.1.0 with 5 output formats
-   - Code-search README.md infrastructure documentation
-   - TEMP milestone automatic detection and handling
-   - /docs/ingest/ workflow integration
- - **Health Audit Layer**: Automated skills-auditor for monitoring evolve-skills dependencies with 13 health reports and console dashboard
- - **Artifacts**:
-   - `milestones/M2/M2SA1.md` — Session Audit Document
-   - `milestones/M2/SESSION_CHANGES.md` — Change log
-   - `milestones/M2/CHANGELOG_ENTRIES.md` — Changelog entries
-   - `milestones/M2/MILESTONE_UPDATES.md` — Milestone updates
- - `milestones/M2/M2SA2.md` — Session Audit Document


### M3 — The Mechanism Upgrade

- **Status**: 75% Complete (M3S2 Accepted; M3S1 pending remediation)
- **Phase**: Implementation & Mechanical Tooling
- **Description**: Embed "The Mechanism" into the OMP AEF canonical architecture to enforce mechanical uncertainty markers, zero-trust reviews, evidence-based debugging, raw evidence mandates, and project-agnostic mechanical tooling gates.
- **Key Deliverables**:
  - Mandatory `#NEEDS-CLARIFICATION` marker codified in FRAMEWORK.md and AGENTS.md
  - Zero-trust review pass with live-state verification in review-implementation
  - Evidence-based debugging mandate in investigate-issue and evaluate-implementation
  - Raw Evidence section in completion and evaluation templates
  - Read-only ground-truth check utility script
  - Mechanical Tooling Stack mandate in bootstrap-project
  - `milestones/M3/M3S2.md` — Specification (Accepted)
  - `milestones/M3/M3S2V.md` — Verification protocol
  - `milestones/M3/M3S2T1.md` — Test plan
  - `milestones/M3/M3S2C.md` — Completion report
  - `milestones/M3/M3S2E.md` — Evaluation report
  - `milestones/M3/M3S2R.md` — Review report (Accepted)
  - `milestones/M3/M3SA1.md` — Session Audit Document
  - `milestones/M3/SESSION_CHANGES.md` — Change log
  - `milestones/M3/CHANGELOG_ENTRIES.md` — Changelog entries
  - `milestones/M3/MILESTONE_UPDATES.md` — Milestone updates
  - `milestones/M3/INGEST_ENTRIES.md` — Ingestion entries

---

## Archived Milestones

- ### M7 — Restore Determinism — Repair `generate-tests` Test-First Integrity
  - **Status**: ✅ Complete
  - **Phase**: Testing & Remediation
  - **Date**: 2026-07-27
  - **Session**: SA1 (completed 2026-07-27)
  - **Description**: Restored test-first integrity to the SDD pipeline by making `generate-tests` deterministic — it now produces executable tests that initially fail, enforces hard boundary guardrails against production code, and generates machine-readable output. Includes investigation report, test contract, test-first enforcement, language-specific executable test rules, guardrail breach protocol, and meta-tests A–G.
  - **Key Deliverables**:
    - Investigation report identifying contamination root cause (7 questions)
    - Hard boundary guardrails with 5-category file classification
    - Test contract defining strict test artifact requirements
    - Test-first enforcement (run tests, capture exit codes, expect failure)
    - Language-specific executable test rules with cross-language prohibition
    - Guardrail Breach Protocol with STOP-and-report
    - Machine-readable output (TESTS_RUN, TESTS_PASSED, TESTS_FAILED, EXIT_CODE)
    - 7 meta-tests (Tests A–G) for the test generator
    - Lifecycle postmortem with 10 architectural findings
  - **Skills Updated**:
    - `skills/generate-tests/SKILL.md` — v1.1.0 → v2.0.0
    - `skills/implement-specification/SKILL.md` — v1.0.1 → v1.0.2
    - `skills/evaluate-implementation/SKILL.md` — v1.0.2 → v1.0.3
  - **Artifacts**:
    - `milestones/M7/M7.md` — Milestone definition
    - `milestones/M7/M7S1.md` — Specification (Approved)
    - `milestones/M7/M7S1V.md` — Verification protocol
    - `milestones/M7/M7S1T1.md` — Test plan
    - `milestones/M7/M7S1C.md` — Completion report
    - `milestones/M7/M7S1E.md` — Evaluation report
    - `milestones/M7/M7S1R.md` — Review report
    - `milestones/M7/M7INVESTIGATION.md` — Investigation report
    - `milestones/M7/M7SA1.md` — Session Audit Document (SA1)
    - `milestones/M7/SESSION_CHANGES.md` — Change log
    - `milestones/M7/CHANGELOG_ENTRIES.md` — Changelog entries
    - `milestones/M7/MILESTONE_UPDATES.md` — Milestone updates
    - `milestones/M7/INGEST_ENTRIES.md` — Ingestion entries
    - `tests/M7/` — 7 meta-test scripts (Tests A–G)
    - `docs/MILESTONES.md` — Archived entry (this section)
  - **Architectural Findings**: 10 lifecycle lessons preserved in M7SA1.md

---

## Infrastructure Skills

The following Infrastructure Skills provide core capabilities used across the OMP Framework:

- **code-search**: Semantic code analysis and pattern matching across the codebase, enabling rapid understanding of code structure and relationships without reading every file.
- **session-audit**: Comprehensive session tracking and documentation generation, creating audit reports (M{X}SA{Y}.md) that track all major changes and generate outputs for all OMP AEF documents.