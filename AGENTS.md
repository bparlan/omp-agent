# OMP Agentic Engineering Framework: System & Agent Guide (v2.0.0)

This document is the canonical reference for agent roles, Spec-Driven Development (SDD) boundaries, and the mechanical safeguards that enforce process determinism across AEF projects.

---

## 1. Core Architectural Pillars

The framework applies foundational software engineering principles directly to agent orchestration:

- **One Transform at a Time (Single Responsibility):** Each agent performs exactly one specialized transformation with zero cross-cutting concerns.
- **Deterministic Outputs (Pure Functions):** Agents must parse and read state before writing. Programmatic tool calls replace natural language reasoning where possible.
- **Artifact Persistence (Immutable Event Sourcing):** Every step in the SDD lifecycle is serialized into structured, version-controlled Markdown artifacts in `milestones/M{X}/` rather than overwriting shared historical files.
- **No Simulated Output:** Never produce simulated, hypothetical, or illustrative tool/terminal output — a blocked step is reported as blocked, never filled in.

---

## 2. Breaking the TDD "Catch-22" (The Interface Contract Mandate)

A critical failure mode occurs when a high-level, conceptual Milestone is translated into vague prose specifications. This forces downstream agents to generate tests that grep for English words or assume un-implemented APIs, violating the _Test Oracle Independence_ and _No Textual Specification Drift_ rules.

To break this loop, **Specifications must establish concrete, observable Interface Contracts**:

1.  **Observable Boundaries:** `generate-spec` MUST translate prose milestone goals into explicit mechanical contracts—such as CLI binaries (e.g., `bin/omp-discover`), JSON schemas, config keys, or file path mappings.
2.  **No Prose Grepping:** Requirements must be defined in terms of verifiable logic, exit codes, or data structures. Tests are strictly prohibited from scanning markdown files for prose descriptions.
3.  **Synthetic Fixtures:** Tests must run against static, mock directory structures (e.g., `tests/fixtures/synthetic_python`) rather than the active running environment.
4.  **TDD Post-Implementation Assertion:** Tests must assert the final successful execution of the interface contract. If the implementation is missing, the tool naturally exits with status `1` or `127` (Command Not Found). This natural failure is the verified `VALID_INITIAL_FAILURE` required to unblock the pre-implementation gate.

---

## 3. The Mechanical Safeguards

### A. The Uncertainty Marker (`#NEEDS-CLARIFICATION`)

If an agent's confidence in a fact falls below _"I could paste the command that proves this,"_ it MUST emit the literal, grep-able marker `#NEEDS-CLARIFICATION: <missing fact>` and **HALT**. Guessing or assuming is strictly prohibited.

### B. Zero-Trust Review

The reviewer operates under the rule: _"Assume the prior report is wrong until proven otherwise."_ Every claim in the completion report must be independently verified using bash or read commands, and recorded in the _Live State Verification_ section of `REVIEW-{N}.md`.

### C. Valid Evidence Lifecycle

Never advance the SDD pipeline based solely on exit codes. The evaluator must run a mandatory validity check to classify each test:

- **VALID_TEST:** The test correctly loaded, imported, or executed the intended subject. Only valid failures unblock the implementation phase.
- **INVALID_TEST:** The test is malformed, self-scanning, or corrupted by pre-existing environment state. The pipeline must **STOP** immediately (Exit Code `2`) and generate an Invalidation Report.

### D. Evidence-Based Escalation

Reports claiming defects (tool, framework, environment, execution, runtime, filesystem) must satisfy an escalation contract by providing sufficient, verifiable evidence. This ensures escalation is a final investigative outcome, rather than an initial conclusion.

**Escalation Contract Requirements:**

- **Reproducibility:** Provide a minimal, repeatable example that reliably triggers the defect.
- **Independence:** Demonstrate that the defect is not a side-effect of the current implementation or environment configuration.
- **Elimination of Simpler Explanations:** Rule out obvious or simpler causes before escalating.

**Review & Verification:**

- Review processes MUST verify that all escalations meet these evidence requirements.
- Unsupported escalation attempts WILL fail review.

**Constraints:**

- Language Agnostic: Rules apply universally across all development languages and environments.
- Practicality: Requirements are designed to be feasible for solo developers.

---

## 4. Unified Agent Roles & Handoff Matrix

| Layer         | Agent / Skill             | Primary Mandate                                          | Core Artifact                       | Next Handoff Target       |
| :------------ | :------------------------ | :------------------------------------------------------- | :---------------------------------- | :------------------------ |
| **Strategic** | `manage-roadmap`          | Align roadmap; handle ingestion folders with permission. | `ROADMAP.md`, `M{X}.md`             | `manage-development`      |
| **Strategic** | `milestone`               | Elicit requirements interactively; define scope.         | `milestones/M{X}/M{X}.md`           | `generate-spec`           |
| **Tactical**  | `manage-development`      | Orchestrate SDD pipeline; track state and repair limits. | `milestones/M{X}/M{X}C.md`          | Sequence-dependent        |
| **Core Dev**  | `generate-spec`           | Translate milestones into concrete Interface Contracts.  | `milestones/M{X}/M{X}S{Y}.md`       | `generate-verification`   |
| **Core Dev**  | `generate-verification`   | Translate specifications into testable assertions.       | `milestones/M{X}/M{X}S{Y}V.md`      | `generate-tests`          |
| **Core Dev**  | `generate-tests`          | Generate executable scripts from verification contracts. | `milestones/M{X}/M{X}S{Y}T{Z}.md`   | `implement-specification` |
| **Core Dev**  | `implement-specification` | Implement logic to satisfy the specification contracts.  | `milestones/M{X}/M{X}S{Y}C.md`      | `evaluate-implementation` |
| **Core Dev**  | `evaluate-implementation` | Run tests, auto-fix minor bugs, classify failures.       | `milestones/M{X}/M{X}S{Y}E.md`      | `review-implementation`   |
| **Core Dev**  | `review-implementation`   | Run zero-trust reality audits of the implementation.     | `milestones/M{X}/M{X}S{Y}R.md`      | `sync-documentation`      |
| **Support**   | `session-audit`           | Capture session changes and recommend skill evolution.   | `M{X}SA{Y}.md`, `INGEST_ENTRIES.md` | `sync-documentation`      |
| **Support**   | `sync-documentation`      | Integrate session changes into canonical documents.      | Updated canonical docs              | `evolve-skills`           |
| **Support**   | `evolve-skills`           | Refine agent prompts based on empirical session errors.  | Updated `SKILL.md` files            | Human approval            |
