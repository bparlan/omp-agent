# OhMyPi (OMP) Agentic Engineering Framework (AEF)

> **Production-Grade Spec-Driven Development for AI Coding Agents**

**Status:** Under Development · 2026–Present

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Design Decisions](#design-decisions)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Examples](#examples)

---

## Overview

The **OhMyPi (OMP) Agentic Engineering Framework (AEF)** is a strict, artifact-based Spec-Driven Development (SDD) system for AI coding agents.

### What It Is

- A lifecycle around **specification, roadmap, implementation, verification, and archival** artifacts rather than conversational agent sessions
- Integration of multiple agentic development experiences, reusable skills, and model providers into a controlled workflow
- Model/agent agnostic — usable with different coding agents and LLM providers
- Completed **~50 development milestones** while continuously testing and refining the methodology against real projects

### What It Is Not

- A general-purpose AI agent framework
- A specific tool for a single language or framework
- A finished, production-ready product (currently under development)

---

## Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────────────┐
│  L1: Strategic Layer                                 │
│  • manage-roadmap (aligns priorities)                │
│  • manage-development (orchestrates SDD pipeline)    │
│  • milestoner (creates milestone artifacts)           │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│  L2: Core Development Layer                          │
│  • generate-spec (specification)                     │
│  • generate-verification (verification protocol)     │
│  • generate-tests (test scripts)                     │
│  • implement-specification (code generation)        │
│  • evaluate-implementation (test execution)          │
│  • review-implementation (implementation review)      │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│  L3: Support & Infrastructure Layer                  │
│  • session-audit (tracks session changes)            │
│  • evolve-skills (improves skills based on practice) │
│  • sync-documentation (maintains canonical docs)      │
│  • code-search (semantic code analysis)              │
│  • bootstrap-project (initializes new repos)         │
│  • diagrammer (generates architecture diagrams)      │
│  • investigate-issue / hotfix-issue (issue handling) │
│  • archive-docs (archives completed work)            │
└─────────────────────────────────────────────────────┘
```

### Artifact Lifecycle

Each artifact has a strict lifecycle:

```
Milestone → Specification → Verification → Tests → Implementation → Evaluation → Review → Archive
```

**Artifact Types** (canonical naming: `TYPE-NNN`):

| Type | Producer Skill | Consumer Skill | Purpose |
|------|----------------|----------------|---------|
| `SPEC` | generate-spec | implement-specification | Detailed implementation specification |
| `VER` | generate-verification | generate-tests | Protocol defining correctness evaluation |
| `TEST` | generate-tests | evaluate-implementation | Executable test scripts and plans |
| `COMP` | implement-specification | review-implementation | Implementation completion report |
| `EVAL` | evaluate-implementation | review-implementation | Test execution results and bug fixes |
| `REVIEW` | review-implementation | manage-development | Implementation vs specification comparison |
| `AUDIT` | session-audit | evolve-skills | Session audit records |

### Core Principles

1. **One Transform at a Time:** Each skill performs exactly one specialized transformation with no cross-cutting concerns
2. **Deterministic Outputs:** Agents parse and read state before writing — pure functions
3. **Artifact Persistence:** Each agent writes to new artifacts rather than modifying existing files
4. **Strict Tool Boundaries:** Tools execute deterministically; agents make high-level decisions
5. **Zero-Touch Dependencies:** Skills skip validation, linting, and tests during implementation

---

## Installation

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** (for some skills and tools)
- **Git**
- **Optional:** FreeLLMAPI or compatible model gateway (for LLM-powered skills)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/bparlan/aef.git
   cd aef
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your project (optional but recommended):**

   Create `.omp/config.yml` in your project directory:

   ```yaml
   project_id: my-project
   mode: application

   model_routing:
     default_provider: openai  # or anthropic, or freellmapi
     providers:
       openai:
         api_base: "https://api.openai.com/v1"
         api_key_env: "OPENAI_API_KEY"
         default_model: "gpt-4"
   ```

5. **Verify installation:**

   ```bash
   python3 bin/resolve_artifact.py --help
   ```

   Should output resolution help text (exit code 0).

---

## Usage

### The SDD Workflow

1. **Milestone Definition** (`milestoner` skill)
   - Elicit requirements interactively
   - Create `milestones/M{X}/M{X}.md`

2. **Specification** (`generate-spec` skill)
   - Transform milestone into detailed implementation specification
   - Create `milestones/M{X}/M{X}S{Y}.md`

3. **Verification** (`generate-verification` skill)
   - Define testable assertions
   - Create `milestones/M{X}/M{X}S{Y}V.md`

4. **Test Generation** (`generate-tests` skill)
   - Generate executable test scripts
   - Create `milestones/M{X}/M{X}S{Y}T{Z}.md`

5. **Implementation** (`implement-specification` skill)
   - Implement logic to satisfy the specification
   - Create `milestones/M{X}/M{X}S{Y}C.md`

6. **Evaluation** (`evaluate-implementation` skill)
   - Run tests, auto-fix minor bugs
   - Create `milestones/M{X}/M{X}S{Y}E.md`

7. **Review** (`review-implementation` skill)
   - Compare implementation to specification
   - Create `milestones/M{X}/M{X}S{Y}R.md`

8. **Sync Docs & Archive** (`sync-documentation` + `archive-docs`)
   - Update canonical documentation
   - Archive completed milestone artifacts

### Using the Skills

Skills are invoked through the OMP harness. Each skill directory contains:

- `SKILL.md` — Skill definition and operational instructions
- `README.md` — Skill overview

**Key skills:**

- `milestoner` — Start a new milestone
- `manage-development` — Orchestrate the SDD pipeline
- `generate-spec` — Create a specification from a milestone
- `implement-specification` — Implement code from a specification
- `evaluate-implementation` — Run tests and auto-fix bugs
- `review-implementation` — Zero-trust review of implementation

### Artifact Resolution

Resolve artifacts by canonical ID:

```bash
python3 bin/resolve_artifact.py SPEC-001 --milestone M7 --verbose
```

Resolution uses a 3-tier priority:

1. **YAML metadata** (`id: SPEC-001`)
2. **Directory context** (`milestones/M7/specifications/`)
3. **Legacy heuristics** (`M7S1.md`)

---

## Design Decisions

### Why Spec-Driven Development?

**Problem:** Standard agentic systems fail systematically with context loss, overwrites, infinite loops, and non-deterministic behavior.

**Solution:** SDD provides:
- **One Transform at a Time** — Prevents context thrashing
- **Deterministic Outputs** — Pure functions, no hidden state
- **Artifact Persistence** — Immutable event sourcing
- **Strict Tool Boundaries** — Agents decide; tools execute

### Why Three Layers?

**Strategic Layer** (`manage-roadmap`, `manage-development`, `milestoner`):
- Sets the "What & Why"
- High-level decision making
- Project-wide orchestration

**Core Development Layer** (7 skills):
- The "How"
- Specialized transformations
- Artifact creation and consumption

**Support & Infrastructure Layer** (11 skills):
- Meta-learning and improvement
- Documentation and archiving
- Tooling and utilities

### Why Artifacts Over Conversations?

Artifacts provide:
- **Traceability:** Every decision has a permanent record
- **Reproducibility:** Can re-run the entire pipeline from artifacts
- **Reviewability:** External reviewers can inspect each stage
- **Testability:** Each artifact can be validated independently

### Why Zero-Touch Dependencies?

Skills skip validation, linting, and tests during implementation to:
- **Prevent blocking:** Build failures don't stall the pipeline
- **Enable parallelization:** Independent skills can run concurrently
- **Focus on transformation:** Each skill has a single, clear purpose

---

## Roadmap

### Completed Work

- **~50 milestones** completed across multiple projects
- **22 active skills** organized in three layers
- **Canonical artifact architecture** with strict lifecycle
- **Template system** for artifacts
- **Session audit and evolution** mechanisms

### Current Development Focus

- **Refining skill boundaries** and reducing overlap
- **Improving test generation** quality and coverage
- **Enhancing auto-repair capabilities** in evaluation
- **Expanding integration options** (FreeLLMAPI, custom providers)

### Future Work

- **Plugin system** for custom skills
- **Multi-project management** (workspace-level milestones)
- **Visualization tools** for artifact relationships
- **Performance optimizations** for large codebases

---

## Contributing

### Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bparlan/aef.git
   cd aef
   ```

2. **Read the skills:** Each skill has a `SKILL.md` with detailed instructions.

3. **Follow the SDD pipeline:** Create a milestone, generate a spec, implement, evaluate, and review.

### Guidelines

- **One transform at a time:** Each skill should have a single, clear purpose
- **Deterministic outputs:** Always read state before writing
- **Artifact persistence:** Create new artifacts rather than modifying existing ones
- **Test your changes:** Run tests before submitting
- **Document your changes:** Update relevant skills and documentation

### Development Workflow

1. **Create a milestone** for your feature/fix
2. **Generate a specification** with `generate-spec`
3. **Generate tests** with `generate-tests`
4. **Implement** with `implement-specification`
5. **Evaluate** with `evaluate-implementation`
6. **Review** with `review-implementation`
7. **Archive** with `archive-docs`

---

## Examples

### Example 1: Adding a New Skill

1. Create a new skill directory: `skills/my-new-skill/`
2. Add `SKILL.md` with:
   - Frontmatter with `user-invocable: true`
   - Operational instructions
   - Input/output contracts
3. Add `README.md` with:
   - Skill overview
   - Usage examples
   - Dependencies

### Example 2: Using FreeLLMAPI Integration

See [docs/freellmapi-omp-integration.md](docs/freellmapi-omp-integration.md) for a complete example of integrating FreeLLMAPI as a model gateway.

**Key steps:**

1. Start FreeLLMAPI locally
2. Configure environment variables
3. Update `.omp/config.yml` to route through FreeLLMAPI
4. Use `model_routing` to specify providers

### Example 3: Resolving Artifacts

```bash
# Resolve by canonical ID
python3 bin/resolve_artifact.py SPEC-001 --milestone M7

# Resolve by legacy ID
python3 bin/resolve_artifact.py M7S1 --milestone M7

# Verbose mode
python3 bin/resolve_artifact.py SPEC-001 --milestone M7 --verbose
```

### Example 4: Running the Full Pipeline

```bash
# 1. Create a milestone
hub op:send to:Main message="Create milestone M11: Add Plugin System"

# 2. Generate specification
hub op:send to:Main message="Generate spec from milestone M11"

# 3. Generate verification
hub op:send to:Main message="Generate verification from spec M11S1"

# 4. Generate tests
hub op:send to:Main message="Generate tests from verification M11S1V"

# 5. Implement
hub op:send to:Main message="Implement from spec M11S1"

# 6. Evaluate
hub op:send to:Main message="Evaluate implementation M11S1"

# 7. Review
hub op:send to:Main message="Review implementation M11S1"

# 8. Archive
hub op:send to:Main message="Archive milestone M11"
```

---

## Documentation

- **[AGENTS.md](AGENTS.md)** — Framework overview and agent roles
- **[INDEX.md](INDEX.md)** — Complete skill catalog
- **[docs/FRAMEWORK.md](docs/FRAMEWORK.md)** — Architecture patterns
- **[docs/SKILLS.md](docs/SKILLS.md)** — Comprehensive skill catalog
- **[docs/PLAYBOOK.md](docs/PLAYBOOK.md)** — Operational workflows
- **[docs/ARTIFACT_ARCHITECTURE.md](docs/ARTIFACT_ARCHITECTURE.md)** — Artifact lifecycle and contracts
- **[docs/diagrams/](docs/diagrams/)** — Architecture diagrams

---

## Metrics

- **~50 development milestones** completed
- **22 active skills**
- **36 GitHub stars** (as of 2026-08-24)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Under Development:** This framework is actively being refined based on practical usage. Expect breaking changes as the design matures.
