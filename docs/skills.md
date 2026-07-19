# OMP AEF Skills Catalog

This document provides detailed information about all 35 skills in the OMP Agentic Engineering Framework, organized by layer.

## Table of Contents

- [Strategic Layer Agents](#strategic-layer-agents)
  - [manage-roadmap](#manage-roadmap)
  - [manage-development](#manage-development)
  - [milestone](#milestone)
- [Core Development Agents](#core-development-agents)
  - [generate-spec](#generate-spec)
  - [implement-specification](#implement-specification)
  - [generate-verification](#generate-verification)
  - [generate-tests](#generate-tests)
  - [evaluate-implementation](#evaluate-implementation)
  - [review-implementation](#review-implementation)
- [Support & Infrastructure Agents](#support--infrastructure-agents)
  - [session-audit](#session-audit)
  - [investigate-issue](#investigate-issue)
  - [hotfix-issue](#hotfix-issue)
  - [archive-milestone](#archive-milestone)
  - [evolve-skills](#evolve-skills)
  - [sync-documentation](#sync-documentation)
  - [code-search](#code-search)
  - [bootstrap-project](#bootstrap-project)

---

## Strategic Layer Agents

Strategic agents define project-level strategies, roadmaps, and governance. They oversee the high-level direction and coordinate milestone planning.

### manage-roadmap

**Purpose**: Strategic orchestrator aligning ROADMAP.md with user goals and generating actionable Milestones (M{X}.md).

**Key Responsibilities**:
- Read and interpret ROADMAP.md
- Elicit requirements from users via milestone agent
- Generate M{X}.md with: Problem Statement, Goals, Architecture Impact, Success Criteria
- Align with user's long-term vision and constraints
- Coordinate with manage-development for cycle reporting
- Handle /docs/ingest/ workflow with user permission + context

**Artifacts Generated**:
- None (pure orchestrator, coordinates other agents)

**Out of Scope**:
- Implementing specifications
- Writing verification protocols
- Creating test plans
- Archiving milestones

**Interaction Flow**:
```
User (via milestone) → manage-roadmap → milestone → generate-spec → ...
```

**Location**: `skills/manage-roadmap/SKILL.md`

---

### manage-development

**Purpose**: Tactical Engineering Manager orchestrating the Spec-Driven Development pipeline with cycle reporting and roadmap integration.

**Key Responsibilities**:
- Monitor SDD pipeline progress
- Ensure each phase completes before handoff
- Report cycle status and issues
- Coordinate between milestone planning and execution
- Generate cycle reports
- Integrate with manage-roadmap

**Artifacts Generated**:
- None (pure orchestrator)

**Out of Scope**:
- Writing specifications
- Implementing code
- Running tests
- Reviewing implementations

**Interaction Flow**:
```
manage-roadmap → milestone → generate-spec → implement-specification → generate-verification → generate-tests → evaluate-implementation → review-implementation → manage-development → ...
```

**Location**: `skills/manage-development/SKILL.md`

---

### milestone

**Purpose**: Transform rough feature ideas into complete milestone documents through interactive requirements elicitation.

**Key Responsibilities**:
- Elicit requirements via question-driven process
- Generate M{X}.md with: Problem Statement, Goals, Architecture Impact, Success Criteria
- Support followup specifications for existing milestones
- Verification reuse analysis
- Manage iterative milestone development

**Commands**:
- `create` — Initialize new project milestone, creates M{X}/M{X}.md
- `update <milestone_path>` — Continue building on existing milestone
- `followup <milestone_path>` — Generate new specification for followup work
- `analyze-reuse <milestone_path>` — Check reusable verifications/tests

**Artifacts Generated**:
- `milestones/M{X}/M{X}.md` — Milestone definition document
- `milestones/M{X}/M{X}S{Y}.md` — Followup specifications (if followup command used)

**Out of Scope**:
- Implementing specifications
- Writing verification protocols
- Creating test plans
- Archiving milestones

**Interaction Flow**:
```
User → milestone → generate-spec → implement-specification → ...
```

**Location**: `skills/milestone/SKILL.md`

---

## Core Development Agents

Core development agents implement the specification-driven development workflow. They transform milestones into working code.

### generate-spec

**Purpose**: Transform approved milestone document into detailed implementation specification.

**Key Responsibilities**:
- Read and analyze M{X}.md
- Extract functional requirements from milestone scope
- Derive non-functional requirements from risks and needs
- Identify architecture impact
- Define data flow
- Extract constraints and assumptions
- Define acceptance criteria
- Write M{X}S{Y}.md using template
- Support followup specifications for existing milestones
- Verification reuse analysis

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}.md` — Detailed specification document

**Out of Scope**:
- Implementing code
- Running tests
- Writing verification protocols

**Interaction Flow**:
```
milestone → generate-spec → implement-specification
```

**Location**: `skills/generate-spec/SKILL.md`

---

### implement-specification

**Purpose**: Implements approved specifications using project architecture, conventions, and verification plans.

**Key Responsibilities**:
- Read M{X}S{Y}.md specification
- Read M{X}S{Y}V.md verification protocol
- Create Todo list (one task per Functional Requirement)
- Analyze existing codebase with LSP
- Spawn parallel task subagents for localized changes
- Execute verification commands
- Summarize results

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}C.md` — Completion report

**Out of Scope**:
- Generating specifications or milestones
- Writing verification protocols
- Creating test plans

**Implementation Principles**:
- Before modifying code: Read context, identify reusable components
- During implementation: Preserve boundaries, minimal changes, extend existing
- When uncertain: Ask clarification via `ask`

**Interaction Flow**:
```
generate-spec → implement-specification → generate-verification
```

**Location**: `skills/implement-specification/SKILL.md`

---

### generate-verification

**Purpose**: Transform specifications into verification protocols defining how correctness will be evaluated.

**Key Responsibilities**:
- Read M{X}S{Y}.md specification
- Identify Functional Requirements and Architecture Impact
- Define success criteria for each requirement
- Create testable assertions
- Specify expected behavior for edge cases
- Document failure scenarios
- Create M{X}S{Y}V.md

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}V.md` — Verification Protocol

**Out of Scope**:
- Implementing code
- Writing test scripts
- Running tests

**Interaction Flow**:
```
implement-specification → generate-verification → generate-tests
```

**Location**: `skills/generate-verification/SKILL.md`

---

### generate-tests

**Purpose**: Translates verification protocols into executable use-case scripts and tests.

**Key Responsibilities**:
- Read M{X}S{Y}V.md verification protocol
- Generate executable test scripts (Python pytest, JS, bash, etc.)
- Save test plan documentation
- Save executable scripts to tests/M{X}/ directory
- Document expected coverage

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}T{Z}.md` — Test Plan documentation
- `tests/M{X}/` — Executable test scripts

**Out of Scope**:
- Running tests
- Modifying implementation code
- Updating specifications

**Location**: `skills/generate-tests/SKILL.md`

---

### evaluate-implementation

**Purpose**: Executes tests, autonomously fixes minor bugs, and generates the Evaluation Report.

**Key Responsibilities**:
- Locate test scripts from generate-tests
- Execute tests using bash
- Analyze stack traces and errors
- Autonomously fix minor bugs (logical errors, typos)
- Re-run tests to verify fix
- Generate structured Evaluation Report
- Handoff to review-implementation

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}E.md` — Evaluation Report

**Autonomy Level**:
- **Minor bugs only**: Logical errors, typos, missing basic connections
- **Not allowed**: Major architectural changes, rewriting entire modules

**Out of Scope**:
- Rewriting entire test scripts
- Major architectural changes
- Creating documentation in project root

**Interaction Flow**:
```
generate-tests → evaluate-implementation → review-implementation
```

**Location**: `skills/evaluate-implementation/SKILL.md`

---

### review-implementation

**Purpose**: Evaluates completed implementation against approved specifications and verification protocols.

**Key Responsibilities**:
- Read implementation artifacts (spec, verification, completion)
- Compare implementation against specification
- Test verification coverage
- Identify incomplete requirements and issues
- Assess architecture compliance
- Generate review report

**Artifacts Generated**:
- `milestones/M{X}/M{X}S{Y}R.md` — Review Report

**Analysis Focus**:
- **Execution Summary**: What changed, scope, files modified
- **Reality vs Plan**: Completed / Partial / Missing requirements
- **Verification Coverage**: Actual tests vs verification protocol
- **Issues Found**: Bugs, missing error handling, incorrect assumptions
- **Critical Findings**: Security, performance, breaking changes
- **Architecture Compliance**: Module boundaries, constraints
- **Technical Debt**: Shortcuts, TODOs, maintainability gaps

**Out of Scope**:
- Running tests or evaluating results
- Modifying implementation code

**Interaction Flow**:
```
evaluate-implementation → review-implementation → archive-milestone
```

**Location**: `skills/review-implementation/SKILL.md`

---

## Support & Infrastructure Agents

Support and infrastructure agents assist with specific concerns, maintain infrastructure, and handle post-implementation work.

### session-audit

**Purpose**: Comprehensive session tracking and documentation generation for evolve-skills.

**Key Responsibilities**:
- Detect session changes using git or filesystem timestamps
- Classify changes (framework-critical vs cosmetic)
- Generate multiple session audits (SA1, SA2, SA3...)
- Generate comprehensive documentation for evolve-skills
- Handle TEMP milestone structure for sessions without formal milestones
- Integrate with manage-roadmap for ingestion workflow
- Use code-search for semantic analysis

**Artifacts Generated**:
- `milestones/M{X}/M{X}SA{Y}.md` — Session Audit Document
- `milestones/M{X}/SESSION_CHANGES.md` — Change log
- `milestones/M{X}/CHANGELOG_ENTRIES.md` — Changelog entries
- `milestones/M{X}/MILESTONE_UPDATES.md` — Milestone updates
- `milestones/M{X}/INGEST_ENTRIES.md` — Ingestion entries

**Location**: `milestones/M{X}/` or `milestones/TEMP/` (NOT `/docs/ingest/`)

**Numbering**:
- SA documents numbered sequentially per milestone: SA1, SA2, SA3...
- TEMP milestones use M{N} prefix: M1SA1, M2SA1, M3SA1...

**Integration**:
- **code-search**: Semantic search and skeleton generation
- **evolve-skills**: Receives recommended actions
- **manage-roadmap**: Processes ingestion entries

**Location**: `skills/session-audit/SKILL.md`

---

### investigate-issue

**Purpose**: Investigates implementation issues and produces technical understanding.

**Key Responsibilities**:
- Read implementation artifacts (code, tests, spec)
- Understand the current state
- Identify root causes
- Generate detailed investigation report
- Recommend fix approach

**Artifacts Generated**:
- `milestones/M{X}/M{X}I{Z}.md` — Investigation Report

**Out of Scope**:
- Applying fixes
- Running hotfix workflows
- Archiving issues

**Location**: `skills/investigate-issue/SKILL.md`

---

### hotfix-issue

**Purpose**: Implements small, targeted bug fixes directly from investigation reports.

**Key Responsibilities**:
- Read investigation report from investigate-issue
- Understand the root cause
- Identify minimal fix location
- Apply fix using edit tool
- Verify fix works
- Handoff back to investigate-issue

**Artifacts Generated**:
- Modified code files

**Out of Scope**:
- Investigating new issues
- Major refactoring
- Creating documentation

**Location**: `skills/hotfix-issue/SKILL.md`

---

### archive-milestone

**Purpose**: Archives completed milestone artifacts while preserving complete engineering history.

**Key Responsibilities**:
- Identify completed milestone (review-implementation passed)
- Copy artifacts to archive
- Preserve all docs (M{X}.md, M{X}S{Y}*.md, etc.)
- Move implementation code to archive location
- Update documentation links
- Verify archive completeness

**Artifacts Moved**:
- Milestone documents
- Specifications
- Verification protocols
- Test plans
- Implementations
- Tests

**Out of Scope**:
- Modifying live codebase
- Re-opening closed milestones
- Breaking traceability

**Location**: `skills/archive-milestone/SKILL.md`

---

### evolve-skills

**Purpose**: Analyze recent project artifacts and Session Audit Reports to learn from mistakes, identify workflow inefficiencies, and automatically update/version SKILL.md files.

**Key Responsibilities**:
- Analyze recent artifacts (M{X}SA{Y}.md, Review Reports, Completion Reports)
- Read all SA documents chronologically
- Identify failure patterns and inefficiencies
- Draft targeted prompt improvements
- Apply updates to SKILL.md files
- Bump version numbers
- Document evolution in EVOLUTION.md
- Process TEMP milestones before formal milestones

**Artifacts Modified**:
- `skills/*/SKILL.md` files (with incremented version numbers)
- `skills/evolve-skills/EVOLUTION.md` ledger

**Out of Scope**:
- Creating new features
- Running implementation workflows
- Creating new templates

**Location**: `skills/evolve-skills/SKILL.md`

---

### sync-documentation

**Purpose**: Integrate session artifacts into canonical documentation.

**Key Responsibilities**:
- Read session artifacts from `milestones/`
- Update CHANGELOG.md
- Update MILESTONES.md
- Update FRAMEWORK.md
- Update ROADMAP.md
- Move files to `docs/ingest/`
- Handle user permission for ingestion

**Artifacts Processed**:
- SESSION_CHANGES.md
- CHANGELOG_ENTRIES.md
- MILESTONE_UPDATES.md
- INGEST_ENTRIES.md

**Location**: `skills/sync-documentation/SKILL.md`

---

### code-search

**Purpose**: Semantic repository search and skeleton generation for understanding code structure.

**Key Responsibilities**:
- Provides semantic search across OMP AEF codebase
- Generates tree-sitter skeletons for codebase structure
- Finds code patterns, relationships, and dependencies
- Extracts architectural patterns and conventions

**Artifacts Generated**:
- `docs/skeletons/OMP-AEF_skeleton.md` — Tree-sitter extracted signatures and imports
- `code_index_OMP-AEF.db` — Vector embeddings for semantic search

**Usage Patterns**:
- Used by `evolve-skills` to analyze failure patterns
- Used by `session-audit` for semantic analysis
- Used by SDD agents to understand codebase structure

**Out of Scope**:
- Detailed implementation review (use LSP instead)
- Running tests or executing code
- Modifying codebase structure

**Location**: `skills/code-search/SKILL.md`

---

### bootstrap-project

**Purpose**: Initialize the framework in a new repository.

**Key Responsibilities**:
- Analyze existing repository structure
- Generate core documentation files (AGENTS.md, INDEX.md, README.md, etc.)
- Set up templates
- Configure skills-lock.json and config.yml
- Verify installation

**Artifacts Generated**:
- Core documentation files
- Template directory structure
- Configuration files

**Out of Scope**:
- Running full implementation workflows
- Creating specific features

**Location**: `skills/bootstrap-project/SKILL.md`

---

## Links to Detailed Documentation

- **[INDEX.md](../INDEX.md)** — Quick navigation, agent overview, workflow diagrams
- **[AGENTS.md](../AGENTS.md)** — Lightweight navigation hub (180 lines)
- **[PLAYBOOK.md](../docs/PLAYBOOK.md)** — Detailed workflows and procedures
- **[FRAMEWORK.md](../docs/FRAMEWORK.md)** — Architecture patterns and design
- **[docs/EXPERIENCES.md](../EXPERIENCES.md)** — Lessons learned and corrections

---

**Last Updated**: 2026-07-18
