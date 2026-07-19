---
generated-from: AGENTS.md
generated-date: 2026-07-18
original-file: AGENTS.md
ingestion-folder: M2
delegated-to: sync-documentation
context: Standard sync — Add Infrastructure Skills section
action: MODIFIED
file-size: ~7460 bytes
---

# OMP Agentic Engineering Framework Guide

## Core Concepts

### Agent Architecture

The OMP Agentic Engineering Framework is built around specialized subagents, each with a narrow, well-defined scope. This architecture ensures:

- **Clear Boundaries**: Each agent has explicit responsibilities and handoffs
- **No Redundancy**: Agents don't duplicate work; they orchestrate specialized tasks
- **Template-Driven**: All artifacts follow standardized templates
- **Negative Guardrails**: Out of Scope sections prevent unwanted actions

### Spec-Driven Development (SDD)

The framework follows a specification-driven development pipeline:

1. **Milestone** — Interactive requirements elicitation → M{X}.md
2. **Generate Spec** — Approved milestone → M{X}S{Y}.md (Specification)
3. **Implement** — Specification → Working Code
4. **Generate Verification** — Specification → M{X}S{Y}V.md (Verification Protocol)
5. **Generate Tests** — Verification → M{X}S{Y}T{Z}.md (Test Plan) + tests/M{X}/ (Executable Scripts)
6. **Evaluate** — Execute tests, auto-fix bugs, generate M{X}S{Y}E.md
7. **Review** — Compare implementation vs specification, generate M{X}S{Y}R.md

### Agent Handoffs

Agents always handoff to specific next agents, never arbitrary code or external tools:

```
User → milestone → generate-spec → implement-specification → generate-verification → generate-tests → evaluate-implementation → review-implementation
```

Each agent:
- Reads required artifacts from `milestones/M{X}/`
- Writes its artifact to `milestones/M{X}/` or `tests/M{X}/`
- Stops when complete, never continues autonomously
- Reports exactly what was done and what files were created

## Agent Roles

### Strategic Layer Agents

**Purpose**: Define project-level strategies, roadmaps, and governance.

#### manage-roadmap

**Role**: Strategic orchestrator aligning ROADMAP.md with user goals and generating actionable Milestones (M{X}.md).

**Key Responsibilities**:
- Read and interpret ROADMAP.md
- Elicit requirements from users via milestone agent
- Generate M{X}.md with: Problem Statement, Goals, Architecture Impact, Success Criteria
- Align with user's long-term vision and constraints

**Artifacts**:
- `milestones/M{X}/M{X}.md` — Milestone definition document

**Out of Scope**:
- Implementing specifications
- Writing verification protocols
- Creating test plans
- Archiving milestones

**Interaction Flow**:
```
User (via milestone) → manage-roadmap → milestone → generate-spec → ...
```

#### manage-development

**Role**: Tactical Engineering Manager orchestrating the Spec-Driven Development pipeline with cycle reporting and roadmap integration.

**Key Responsibilities**:
- Monitor SDD pipeline progress
- Ensure each phase completes before handoff
- Report cycle status and issues
- Coordinate between milestone planning and execution

**Artifacts**:
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

### Core Development Agents

**Purpose**: Implement the specification-driven development workflow.

#### milestone

**Role**: Transforms rough feature ideas into complete milestone documents through interactive requirements elicitation.

**Key Responsibilities**:
- Elicit requirements from users via question-driven process
- Generate M{X}.md with: Problem Statement, Goals, Architecture Impact, Success Criteria
- Ensure clear, unambiguous requirements
- Validate against user constraints and preferences

**Artifacts**:
- `milestones/M{X}/M{X}.md` — Milestone definition document

**Process**:
1. Ask clarifying questions
2. Gather constraints (time, scope, tech stack)
3. Identify scope boundaries
4. Generate M{X}.md

**Out of Scope**:
- Writing specifications
- Implementing code
- Creating verification protocols
- Archiving milestones

#### generate-spec

**Role**: Transforms approved milestone documents into detailed implementation specifications.

**Key Responsibilities**:
- Read M{X}.md (Milestone)
- Extract Functional Requirements
- Generate Architecture Impact section
- Create detailed specification document
- Ensure verification protocol can be generated from spec

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}.md` — Specification document

**Process**:
1. Read M{X}.md
2. Define Functional Requirements (FR-1, FR-2, ...)
3. Specify Architecture Impact
4. Identify Edge Cases
5. Generate M{X}S{Y}.md

**Out of Scope**:
- Implementing code
- Writing verification protocols
- Creating test plans
- Modifying milestones

#### implement-specification

**Role**: Implements approved specifications using project architecture, conventions, and verification plans.

**Key Responsibilities**:
- Read M{X}S{Y}.md (Specification) and M{X}S{Y}V.md (Verification)
- Analyze existing codebase with LSP
- Create Todo list (one task per Functional Requirement)
- Spawn parallel task subagents for localized changes
- Execute verification commands
- Summarize results

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}C.md` — Completion report

**Process**:
1. Resolve artifacts (spec, verification, AGENTS.md)
2. Read project context and conventions
3. Analyze specification and architecture impact
4. Inspect existing code via LSP
5. Create Todo list (Foundation → Implementation → Verification)
6. Orchestrate parallel implementation
7. Verify with tests
8. Generate completion report

**Implementation Principles**:
- **Before modifying code**: Read context, identify reusable components
- **During implementation**: Preserve boundaries, minimal changes, extend existing
- **When uncertain**: Ask clarification via `ask`

**Out of Scope**:
- Generating specifications or milestones
- Writing verification protocols
- Creating test plans
- Archiving milestones
- Running tests or evaluating results
- Creating README.md, SUMMARY.md, .txt files in project root

#### generate-verification

**Role**: Transforms specifications into verification protocols defining correctness evaluation methods.

**Key Responsibilities**:
- Read M{X}S{Y}.md (Specification)
- Identify Functional Requirements and Architecture Impact
- Define success criteria for each requirement
- Create testable assertions
- Specify expected behavior for edge cases
- Document failure scenarios

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}V.md` — Verification Protocol

**Process**:
1. Read M{X}S{Y}.md
2. Extract Functional Requirements
3. For each requirement:
   - Define success criteria
   - Identify test cases
   - Specify edge case coverage
   - Document failure scenarios
4. Generate M{X}S{Y}V.md

**Out of Scope**:
- Implementing code
- Writing test scripts
- Running tests
- Creating test plans
- Modifying specifications or milestones

#### generate-tests

**Role**: Translates verification protocols into executable use-case scripts and tests.

**Key Responsibilities**:
- Read M{X}S{Y}V.md (Verification Protocol)
- Generate executable test scripts (Python pytest, JS, bash, etc.)
- Save test plan documentation
- Save executable scripts to tests/M{X}/ directory
- Document expected coverage

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}T{Z}.md` — Test Plan documentation
- `tests/M{X}/` — Executable test scripts

**Process**:
1. Read Verification Protocol
2. Read Implementation (from implement-specification phase)
3. Generate executable test scripts
4. Save test plan documentation using test_template.md
5. Save executable scripts to tests/M{X}/ directory
6. Stop (do not execute tests)

**Out of Scope**:
- Running tests
- Modifying implementation code
- Updating specifications
- Creating README.md, SUMMARY.md, .txt files in project root

#### evaluate-implementation

**Role**: Executes tests, autonomously fixes minor bugs, and generates the Evaluation Report.

**Key Responsibilities**:
- Locate test scripts from generate-tests
- Execute tests (offline, dry-run, or real execution)
- Analyze traces and test results
- Autonomously fix minor bugs (logical errors, typos)
- Generate structured Evaluation Report
- Handoff to review-implementation

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}E.md` — Evaluation Report

**Process**:
1. Locate tests from generate-tests output
2. Execute tests using bash
3. Analyze stack traces and errors
4. Auto-fix minor bugs using edit tool
5. Re-run tests to verify fix
6. Generate Evaluation Report

**Autonomy Level**:
- **Minor bugs only**: Logical errors, typos, missing basic connections
- **Not allowed**: Major architectural changes, rewriting entire modules

**Out of Scope**:
- Rewriting entire test scripts (report structural issues)
- Major architectural changes (log as "Remaining Failure")
- Creating README.md, SUMMARY.md, .txt files in project root

#### review-implementation

**Role**: Evaluates completed implementation against approved specifications and verification protocols.

**Key Responsibilities**:
- Read implementation artifacts (spec, verification, completion)
- Compare implementation against specification
- Test verification coverage
- Identify incomplete requirements and issues
- Assess architecture compliance
- Generate review report

**Artifacts**:
- `milestones/M{X}/M{X}S{Y}R.md` — Review Report

**Process**:
1. Read M{X}S{Y}.md, M{X}S{Y}V.md, M{X}S{Y}C.md
2. Read implementation files
3. Run git diff if available
4. Create compliance matrix
5. Generate review report
6. Archive or keep in milestones/M{X}/

## Infrastructure Skills

The OMP AEF framework includes two key infrastructure skills that support framework operations and documentation:

### 1. session-audit (v1.1.0)

**Role**: Analyzes session-based framework improvements and generates comprehensive documentation for evolve-skills.

**Key Responsibilities**:
- Generates 5 output formats for each session (M{X}SA{Y}.md, SESSION_CHANGES.md, CHANGELOG_ENTRIES.md, MILESTONE_UPDATES.md, INGEST_ENTRIES.md)
- Supports multiple session audits per milestone (SA1, SA2, SA3...)
- Handles TEMP milestone structure for sessions without formal milestones
- Provides comprehensive OMP AEF documentation updates
- Generates ingestion entries for /docs/ingest/ workflow

**Artifacts**:
- Session Audit Documents
- Change Logs
- Changelog Entries
- Milestone Updates
- Ingestion Entries

**Integration**:
- Uses code-search for semantic analysis
- Generates INGEST_ENTRIES.md for manage-roadmap processing
- Recommends evolve-skills actions

**Usage**:
- Run at the end of every session
- Generates automatic documentation
- Maintains complete audit trail

### 2. code-search (v1.0.0)

**Role**: Provides semantic repository understanding for all framework operations.

**Key Responsibilities**:
- Enables semantic search across the codebase
- Generates skeleton structure for codebase understanding
- Provides tree-sitter-based AST analysis
- Reduces token usage for large codebase navigation

**Artifacts**:
- Skeletons (docs/skeletons/OMP-AEF_skeleton.md)
- Vector Database (code_index_OMP-AEF.db)
- Search Results

**Integration**:
- Used by session-audit for semantic analysis
- Used by evolve-skills for pattern matching
- Used by all agents for codebase understanding

**Usage**:
- Use before reading full files
- Prefer semantic search over exhaustive file reading
- Use for pattern finding and codebase navigation

**For detailed usage, patterns, and integration with framework skills, see:**
- **[code-search/README.md](./skills/code-search/README.md)** — Complete infrastructure documentation
