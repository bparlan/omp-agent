# OMP Framework Architecture

## Architectural Patterns

The OhMyPi (OMP) Framework is built upon core engineering principles to ensure robustness and predictability in agentic workflows. Key architectural patterns include:

### Spec-Driven Development

A strict, five-stage sequential workflow (`milestone` → `generate-spec` → `generate-verification` → `implement-specification` → `review-implementation`) governs development. Each stage must complete before the next can begin, ensuring artifacts are stable and well-defined at each step.

### Agent-Tool Separation

A fundamental boundary exists between Agents (responsible for strategy, interpretation, and decision-making) and Tools (responsible for deterministic execution and API interaction). This separation prevents complexity creep within agents and ensures tools remain predictable.

### Hierarchical Control System

The system is structured in three layers:

1.  **Project Manager Layer**: Oversees intent from high-level goals to detailed milestones (e.g., `M1.md`).
2.  **Tactical Lifecycle Engine**: Manages the spec-driven assembly line, executing skills and transforming artifacts.
3.  **Meta-Learning & Canonical Docs**: Accumulates knowledge from execution to feed back into system evolution.

### Artifact Persistence

All decisions, specifications, and rationales are serialized into human-readable Markdown files, forming a complete and persistent engineering history. This creates a "Single Source of Truth" that agents can refer to, preventing context loss and ensuring consistency.

## Module Organization

The codebase is organized around the OMP framework's structure:

-   **Skills**: Core functionalities (e.g., `bootstrap-project`, `milestone`, `lsp`, `grep`) that agents use for specific tasks. These are typically located in `~/.omp/agent/skills/`.
-   **Agents/Prompts**: Definitions for different agent roles (e.g., `implementer.md`, `planner.md`, `reviewer.md`) that dictate their responsibilities and behavior. These are located in prompt directories.
-   **Workflows**: Python scripts (e.g., `implement_workflow.py`) that orchestrate agent actions for specific tasks.
-   **Documentation**: Canonical documentation resides in `docs/` and includes `engineering.md`, `FRAMEWORK.md`, `SPEC.md`, etc.
-   **Configuration**: System configuration and agent prompts are managed in dedicated directories.
