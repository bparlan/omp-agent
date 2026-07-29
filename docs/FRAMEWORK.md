# OMP Framework Architecture

## Architectural Patterns

The OhMyPi (OMP) Framework is built upon core engineering principles to ensure robustness and predictability in agentic workflows. Key architectural patterns include:

### Spec-Driven Development

A strict, five-stage sequential workflow (`milestone` → `generate-spec` → `generate-verification` → `implement-specification` → `review-implementation`) governs development. Each stage must complete before the next can begin, ensuring artifacts are stable and well-defined at each step.

### The Uncertainty Marker

A mandatory literal marker `#NEEDS-CLARIFICATION: <specific missing fact>` establishes an evidence-first culture. If an agent's confidence in a fact is below "I could paste the command that proves this," it MUST either run the command immediately to prove it, or emit `#NEEDS-CLARIFICATION: <specific missing fact>` and HALT. Guessing is strictly forbidden.

### Agent-Tool Separation

A fundamental boundary exists between Agents (responsible for strategy, interpretation, and decision-making) and Tools (responsible for deterministic execution and API interaction). This separation prevents complexity creep within agents and ensures tools remain predictable.

### Hierarchical Control System

The system is structured in three layers:

1.  **Project Manager Layer**: Oversees intent from high-level goals to detailed milestones (e.g., `M1.md`).
2.  **Tactical Lifecycle Engine**: Manages the spec-driven assembly line, executing skills and transforming artifacts.
3.  **Meta-Learning & Canonical Docs**: Accumulates knowledge from execution to feed back into system evolution.

### Artifact Persistence

All decisions, specifications, and rationales are serialized into human-readable Markdown files, forming a complete and persistent engineering history. This creates a "Single Source of Truth" that agents can refer to, preventing context loss and ensuring consistency.

## Infrastructure Skills

The OMP Framework includes core Infrastructure Skills that provide reusable capabilities across the system:

### code-search

- **Purpose**: Semantic code analysis and pattern matching across the entire codebase
- **Capabilities**: Finds code patterns, relationships, and dependencies using AST-based queries without reading file content
- **Integration**: Used by session-audit and other skills for rapid understanding of code structure
- **Documentation**: Comprehensive examples covering all major usage patterns and integration points

### session-audit

- **Purpose**: Comprehensive session tracking and documentation generation
- **Capabilities**: Generates audit reports (`M{X}SA{Y}.md`) for each session, tracks all major changes, and creates outputs for all OMP AEF documents (CHANGELOG.md, MILESTONES.md, ROADMAP.md, FRAMEWORK.md, README.md)
- **Features**:
- Multiple session audits per milestone (SA1, SA2, SA3...) with cumulative context
- TEMP milestone automatic detection for sessions without formal milestones
- Ingestion workflow integration with `/docs/ingest/` folder and manage-roadmap
- Reverse order flow (TEMP > Milestone priority)
- Code-search integration for semantic analysis
- **Outputs**: M{X}SA{Y}.md, SESSION_CHANGES.md, CHANGELOG_ENTRIES.md, MILESTONE_UPDATES.md, INGEST_ENTRIES.md
  **Integration with evolve-skills**:
  session-audit automatically recommends prompt improvements after each session
  evolve-skills analyzes SA documents and updates SKILL.md files
  Changes require per-skill approval via evolve-skills
  Health dashboard used to track skill quality
  **Integration with manage-roadmap**:
  session-audit generates INGEST_ENTRIES.md
  manage-roadmap processes ingestion entries after user permission

### evolve-skills

**Purpose**: Analyze recent project artifacts (`M{X}SA{Y}.md`, Review Reports, Completion Reports) to learn from mistakes, identify workflow inefficiencies, and automatically update/version SKILL.md files
**Capabilities**:
Read SA documents chronologically for each milestone
Identify failure patterns, inefficiencies, and areas for improvement
Draft targeted prompt improvements for each skill
Apply updates to SKILL.md files with incremented version numbers
Document evolution in EVOLUTION.md
Process TEMP milestones before formal milestones

## **Artifacts Modified**:

`skills/*/SKILL.md` files (with incremented version numbers)
`skills/evolve-skills/EVOLUTION.md` ledger

## **Health Dashboard**:

Automated quality monitoring via skills-auditor.py
13 evolve-skills dependencies audited for version consistency, required tools (read, edit), and user-invocable flags
Health status values: HEALTHY, NEEDS_IMPROVEMENT, CRITICAL
Priority levels: HIGH, MEDIUM, LOW
YAML health reports in `evolve-skills/health/{skill-name}.yaml`

## **Dashboard Commands**:

`python3 skills-auditor.py audit` — Full audit of all 13 skills
`python3 skills-auditor.py list` — Color-coded dashboard with status
`python3 skills-auditor.py audit --skill <name>` — Single skill audit

## **Every Session Workflow**:

1. Run `python3 skills-auditor.py audit` to check skill health
2. Run `evolve-skills` to process SA recommendations
3. Review health dashboard for any CRITICAL issues
4. Address critical issues before continuing work

- **Location**: `skills/evolve-skills/SKILL.md`

### session-audit

- `session-audit` recommends `evolve-skills` improvements after each session
- `evolve-skills` processes `session-audit` recommendations and applies fixes
- Creates comprehensive documentation of skill evolution
