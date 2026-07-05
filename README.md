# OhMyPi (OMP) Agent Framework

Specification-Driven Development infrastructure for Oh My Pi. Skills transform artifacts through a deterministic engineering workflow.

## Architecture

```
omp/
├── agent/
│   ├── skills/           ← Lifecycle skills (this document)
│   ├── templates/        ← Document templates
│   ├── AGENTS.md         ← This framework reference
│   ├── state/            ← Runtime state
│   └── workflows/        ← Execution workflows
├── skills/               ← Project-agnostic skill catalog (deprecated, use agent/skills)
└── agents/               ← Specialized agent profiles (deprecated)
```

## Lifecycle Overview

```
bootstrap-project
        │
        ▼
milestone
        │
        ▼
generate-spec
        │
        ▼
generate-verification
        │
        ▼
implement-specification
        │
        ▼
review-implementation
        │
        ▼
sync-documentation
        │
        ▼
archive-milestone

investigate-issue
        │
        └──────────────► generate-spec
```

## Core Principles

1. **One Transform at a Time** — Each skill has exactly one responsibility. No skill orchestrates another skill's domain.
2. **Deterministic Outputs** — Given the same input, same output every time.
3. **Artifact Persistence** — Engineering history preserved in:
   - Milestone: `M{X}.md` (in `milestones/M{X}/`)
   - Specification: `M{X}S{Y}.md` (in `milestones/M{X}/`)
   - Verification: `M{X}S{Y}V.md` (in `milestones/M{X}/`)
   - Review: `M{X}S{Y}R.md` (in `milestones/M{X}/`)
   - Investigation: `M{X}I{Z}.md` or `M{X}S{Y}I{Z}.md` (in `milestones/M{X}/`)
   - Completion: `M{X}S{Y}C.md` (in `milestones/M{X}/`)
   - Summary: `M{X}S{Y}Summary.md` (in `milestones/M{X}/`)
   - Archive: `M{X}A.md` (in `milestones/archive/M{X}/`)

## Directory Standards

| Purpose | Path |
|---------|------|
| System templates | `~/.omp/agent/templates/` |
| System skills | `~/.omp/agent/skills/` |
| Project canonical docs | `project_folder/docs/` (AGENTS.md, FRAMEWORK.md, SPEC.md, ROADMAP.md, PLAYBOOK.md, DATA.md, MILESTONES.md) |
| Active artifacts | `project_folder/milestones/M{X}/` |
| Archived artifacts | `project_folder/milestones/archive/M{X}/` |
| Code search database | `project_folder/code_index_{project}.db` |

## Global Index

`docs/MILESTONES.md` is the single source of truth:

```markdown
# Engineering Milestones

## Active
- [M1] - User authentication system (active)
- [M2] - API rate limiting (active)

## Archived
- [M0] - Initial setup (archived) → milestones/archive/M0/
```

## Lifecycle Skills

| Skill | Purpose | Input → Output |
|-------|---------|---------------|
| **`bootstrap-project`** | Analyze repository, create canonical documentation layer | Repository → docs/ |
| **`milestone`** | Interactive requirements elicitation for feature ideas | Rough idea → M{X}.md + update docs/MILESTONES.md |
| **`generate-spec`** | Derive specification from approved milestone | M{X}.md → M{X}S{Y}.md |
| **`generate-verification`** | Create verification protocol from specification | M{X}S{Y}.md → M{X}S{Y}V.md |
| **`implement-specification`** | Implement specification using existing architecture | M{X}S{Y}.md + M{X}S{Y}V.md → Code + M{X}S{Y}C.md |
| **`review-implementation`** | Audit implementation against specification | Code + artifacts → M{X}S{Y}R.md |
| **`sync-documentation`** | Update canonical docs from completed work | Artifacts → docs/ + M{X}S{Y}Summary.md |
| **`archive-milestone`** | Archive completed milestone artifacts | Active artifacts → milestones/archive/M{X}/ + update docs/MILESTONES.md |
| **`investigate-issue`** | Investigate bugs/issues, route to specification | Issue → M{X}I{Z}.md + recommend spec updates |

## Support Skills

| Skill | Purpose |
|-------|---------|
| **`code-search`** | Semantic code understanding via tree-sitter and vector embeddings |
| **`safe-update`** | Package update safety with supply chain research |
| **`careful`** | High-risk operation pre-flight checklist |
| **`humanizer`** | Remove AI-generated writing patterns from text |
| **`brave-search`** | Web search via Brave Search API |
| **`last30days`** | Research recent conversation about topics |

## Templates

| Template | Document Type |
|----------|---------------|
| `milestone_template.md` | Milestone (M{X}.md) |
| `specification_template.md` | Specification (M{X}S{Y}.md) |
| `verification_template.md` | Verification (M{X}S{Y}V.md) |
| `review_template.md` | Review (M{X}S{Y}R.md) |
| `summary_template.md` | Summary (M{X}S{Y}Summary.md) |
| `archive_template.md` | Archive (M{X}A.md) |
| `investigation_template.md` | Investigation (M{X}[S{Y}]I{Z}.md) |
| `completion_template.md` | Completion Report (M{X}S{Y}C.md) |

## Stability Rules

1. Never overwrite existing specifications — `generate-spec` increments Y automatically
2. Investigation reports never trigger direct implementation — route through `generate-spec`
3. Implementation always produces `M{X}S{Y}C.md` completion report
4. Archive operations move (not copy) and update `docs/MILESTONES.md`
5. `sync-documentation` reads Investigation Reports for major architectural updates

## For Agents

Invoke skills via `task` tool with appropriate role. See each SKILL.md for detailed process.