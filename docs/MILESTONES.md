# OMP Milestones

This document lists active and archived milestones for the OMP Framework project.

## Active Milestones

### M2 — Framework Improvement Strategy

- **Status**: 75% Complete (Documentation and Tooling)
- **Phase**: Infrastructure & Session Management
- **Session**: SA1 (completed 2026-07-18)
- **Description**: Added session-audit skill for session-based framework improvements, enhanced code-search infrastructure with comprehensive documentation, and integrated session-audit into evolve-skills workflow.
- **Key Deliverables**:
  - Session-audit v1.1.0 with 5 output formats
  - Code-search README.md infrastructure documentation
  - TEMP milestone automatic detection and handling
  - /docs/ingest/ workflow integration
- **Health Audit Layer**: Automated skills-auditor for monitoring evolve-skills dependencies with 13 health reports and console dashboard
- **Artifacts**:
  - `milestones/M2/M2SA1.md` — Session Audit Document
  - `milestones/M2/SESSION_CHANGES.md` — Change log
  - `milestones/M2/CHANGELOG_ENTRIES.md` — Changelog entries
  - `milestones/M2/MILESTONE_UPDATES.md` — Milestone updates
- `milestones/M2/M2SA2.md` — Session Audit Document

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
  - `tests/M3/` — Test scripts (7 files, 70 assertions, 6/6 passing)

---

## Archived Milestones

*(No milestones archived yet)*

---

## Infrastructure Skills

The following Infrastructure Skills provide core capabilities used across the OMP Framework:

- **code-search**: Semantic code analysis and pattern matching across the codebase, enabling rapid understanding of code structure and relationships without reading every file.
- **session-audit**: Comprehensive session tracking and documentation generation, creating audit reports (M{X}SA{Y}.md) that track all major changes and generate outputs for all OMP AEF documents.