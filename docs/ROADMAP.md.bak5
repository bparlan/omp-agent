# OMP Framework Roadmap

## Existing Capabilities

### Core Framework & Spec-Driven Development

-   **Spec-Driven Workflow**: Fully implemented 5-stage lifecycle (`milestone` → `generate-spec` → `generate-verification` → `implement-specification` → `review-implementation`).
-   **Agent-Tool Separation**: Strict architectural boundary enforced.
-   **Artifact Persistence**: Serialization of all knowledge and decisions into Markdown.
-   **Hierarchical Control**: Three-layer architecture (Project Manager, Tactical Lifecycle, Meta-Learning).
-   **Repository Bootstrapping**: `bootstrap-project` skill for initial setup and documentation generation.
-   **Infrastructure Skills**: Core infrastructure skills (`code-search`, `session-audit`) providing reusable capabilities across the framework.
-   **Health Monitoring System**: Automated skills-auditor for monitoring evolve-skills dependencies with YAML health reports and console dashboard, ensuring quality standards across the framework.
-   **Session Audit System**: Complete session-based workflow improvements with TEMP milestone support, multiple SA document handling, and evolve-skills integration.

### Agent Orchestration & Management

-   **Task Delegation**: `task` tool for parallelized subagent execution.
-   **Agent Communication**: `irc` for inter-agent messaging and `job` for background task management.
-   **Tooling**: Comprehensive set of specialized tools for code analysis, editing, execution, and debugging.

### Recently Completed

-   **M2: Session Audit Infrastructure** (75% Complete)
-    -   Session-audit skill with 5 output formats (M{X}SA{Y}.md, SESSION_CHANGES.md, CHANGELOG_ENTRIES.md, MILESTONE_UPDATES.md, INGEST_ENTRIES.md)
-    -   Code-search infrastructure with comprehensive README.md documentation
-    -   Multiple SA document support with cumulative context and last SA becoming primary
-    -   TEMP milestone automatic detection and handling
-    -   /docs/ingest/ workflow integration with manage-roadmap
-    -   Skills-auditor health monitoring system with 13 health reports and console dashboard
-
-   **M3: The Mechanism Upgrade** (75% Complete)
-    -   Uncertainty Marker (`#NEEDS-CLARIFICATION`) codified in FRAMEWORK.md, AGENTS.md, and implement-specification SKILL.md
-    -   Zero-Trust Review pass with live-state verification in review-implementation and review_template.md
-    -   Evidence-Based Debugging mandate in investigate-issue and evaluate-implementation SKILL.md files
-    -   Raw Evidence Mandate (exact command + raw output) in completion and evaluation templates
-    -   Ground-Truth Helper Utility (`bin/ground-truth-check.sh`) — read-only POSIX shell utility
-    -   Mechanical Tooling Stack mandate in bootstrap-project SKILL.md and AGENTS.md
-
-   **M7: Restore Determinism** (Completed 2026-07-27)
-    -   generate-tests v2.0.0: file classification guardrails, test-first enforcement, language-specific rules, Guardrail Breach Protocol, machine-readable output
-    -   Meta-tests A–G in tests/M7/ validating generate-tests behavior
-    -   Lifecycle postmortem: 10 architectural findings on test validity, isolated baselines, platform assumptions, meta-test vs project test distinction, and lifecycle precondition gates
-    -   Version bumps: generate-tests 2.0.0, implement-specification 1.0.2, evaluate-implementation 1.0.3

---

## Known Gaps & Future Items

### Testing & Documentation

-   **Testing with Real Sessions**: Execute and validate session-audit workflow with real development sessions.
-   **Documentation Updates**: Complete documentation updates for all core skills.
-   **Production Deployment**: Prepare and execute production deployment of the framework.

### Enhanced Verification & Testing

-   **Automated Test Generation**: Developing capabilities to automatically generate comprehensive test suites based on specifications, going beyond the current `generate-verification` and `review-implementation` stages.
-   **End-to-End (E2E) Testing Integration**: Integrating with E2E testing frameworks to validate complex agentic workflows.

### Advanced Meta-Learning & System Evolution

-   **Self-Improving Framework**: Developing mechanisms for the Meta-Learning layer to proactively suggest architectural improvements or new skills based on observed workflow patterns and failure modes.
-   **Dynamic Skill Generation**: Investigating the feasibility of agents generating new skills or adapting existing ones based on evolving requirements.

### Lifecycle Integrity

- **Lifecycle Precondition Gates**: Formalize test-validity, artifact-integrity, and platform-compatibility checks before each lifecycle phase transition. M7 demonstrated that test-validity preconditions prevent implementation against invalid tests. Extend this pattern to all SDD phase boundaries (spec→verification, verification→tests, tests→implementation, implementation→evaluation).

### Scalability and Performance

-   **Optimized Artifact Storage and Retrieval**: Exploring more efficient methods for storing and querying the growing body of Markdown artifacts.
- **Distributed Execution**: Investigating options for scaling agent execution across distributed systems.

---

## Demonstration Use Cases

This roadmap demonstrates OMP AEF across three independent repositories with distinct objectives and bootstrap stages:

### 1. BariaDAO (Brownfield + Issue Resolution)

**Objective**: Revamp existing landing page with issues by selectively preserving healthy elements (specific buttons, content blocks, design patterns, functional aims) and rebuilding an agentic-friendly version.

**Requirements**:
- Identify and extract agentic-friendly patterns from broken UI (navigation, interaction states, content structure)
- Preserve functional intent and user goals while improving maintainability
- Leverage existing bootstrap infrastructure
- Convert static elements into agent-manageable components

**Key Challenge**: Selective extraction from degraded codebase without context loss

---

### 2. BParlan.com (Brownfield + Design Preservation)

**Objective**: Maintain existing design identity while converting entire one-pager site to agent-manageable format.

**Requirements**:
- Preserve visual design, layout, and user experience exactly
- Convert HTML/CSS/JS into agent-processable structure
- Enable iterative content and functional updates via agent workflow
- Second brownfield bootstrap test

**Key Challenge**: Design preservation + structural conversion without deviation

---

### 3. Autonomedia (Greenfield + Minimal Scope)

**Objective**: Generate landing page from README content explaining project concept and aims.

**Requirements**:
- No existing site to analyze
- Generate single-page marketing site from documentation
- Minimal scope to validate greenfield bootstrap process
- Final verification of framework applicability

**Key Challenge**: Zero-context content generation from documentation source

---

### Use Case Progression

Each repository represents a distinct phase of OMP AEF adoption:

1. **Brownfield with Issues** (BariaDAO) → Selective preservation and agentic upgrade
2. **Brownfield Design Preservation** (BParlan.com) → Structural conversion without redesign
3. **Greenfield Minimal Scope** (Autonomedia) → Complete generation from documentation

**Goal**: Validate OMP AEF flexibility across bootstrap stages, project types, and update frequencies (continuous agent-driven, user-ordered updates).