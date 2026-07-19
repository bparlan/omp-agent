# OMP Agentic Engineering Framework

## Overview (2 lines)

The OMP Agentic Engineering Framework is a **spec-driven development system** with specialized agents for milestone planning, specification, implementation, and review. All work is tracked in `milestones/M{X}/`.

## Architecture (3 layers, 20 lines)

```
┌─────────────────────────────────────┐
│   Strategic Layer (3 agents)         │
│   manage-roadmap                     │
│   manage-development                 │
│   milestone                          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Core Development (7 agents)        │
│   generate-spec                      │
│   implement-specification            │
│   generate-verification              │
│   generate-tests                     │
│   evaluate-implementation            │
│   review-implementation              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Support & Infrastructure (7 agents)│
│   session-audit                      │
│   investigate-issue / hotfix-issue   │
│   archive-milestone                  │
│   evolve-skills                      │
│   sync-documentation                 │
│   code-search                        │
│   bootstrap-project                  │
└─────────────────────────────────────┘
```

### Key Patterns

- **Handoffs**: User → milestone → generate-spec → implement-specification → ... → review-implementation
- **Artifacts**: All in `milestones/M{X}/` or `tests/M{X}/`
- **Meta-Learning**: Evolve-skills learns from SESSION_CHANGES.md

## Skill Catalog (35 total, 80 lines)

### Strategic Layer (3 agents)

- **manage-roadmap** — Align ROADMAP.md with goals, generate milestones
- **manage-development** — Orchestrate SDD pipeline, report cycles
- **milestone** — Elicit requirements, create M{X}.md

### Core Development (7 agents)

- **generate-spec** — Milestone → detailed specification (`milestones/M{X}/M{X}S{Y}.md`)
- **implement-specification** — Spec → working code (`milestones/M{X}/M{X}S{Y}C.md`)
- **generate-verification** — Spec → verification protocol (`milestones/M{X}/M{X}S{Y}V.md`)
- **generate-tests** — Verification → test plan + scripts (`tests/M{X}/M{X}S{Y}T{Z}.md`)
- **evaluate-implementation** — Run tests, auto-fix bugs, generate `milestones/M{X}/M{X}S{Y}E.md`
- **review-implementation** — Compare implementation to spec, generate `milestones/M{X}/M{X}S{Y}R.md`

### Support & Infrastructure (7 agents)

- **session-audit** — Generate SESSION_CHANGES.md + supporting docs
- **investigate-issue / hotfix-issue** — Debug and fix specific issues
- **archive-milestone** — Archive completed milestone artifacts
- **evolve-skills** — Learn from SESSION_CHANGES.md, update SKILL.md
- **sync-documentation** — Update docs from SESSION_CHANGES.md
- **code-search** — Semantic code analysis (used by session-audit)
- **bootstrap-project** — Initialize framework in new repo

## Workflow (10 lines, link to PLAYBOOK.md)

**Core SDD Pipeline**:

```
User → milestone → generate-spec → implement-specification → generate-verification → generate-tests → evaluate-implementation → review-implementation
```

**Session Flow**:

```
Session → session-audit → SESSION_CHANGES.md → evolve-skills → sync-documentation → manage-roadmap → archive
```

📖 **Detailed Workflows**: See [PLAYBOOK.md](docs/PLAYBOOK.md)

## Architecture Details (5 lines, link to FRAMEWORK.md)

- **Spec-Driven Development** (SDD) patterns
- **Agent-Tool Separation** boundaries
- **Artifact Persistence** principles
- **Meta-Learning Loop** design
- **Code-Search** integration

📖 **Full Architecture**: See [FRAMEWORK.md](docs/FRAMEWORK.md)

## Configuration (5 lines)

- **skills-lock.json** — Skill dependencies & hashes
- **config.yml** — Model routing & settings
- **docs/ROADMAP.md** — Capabilities & timeline

## References

| Document              | Purpose                                 |
| --------------------- | --------------------------------------- |
| `INDEX.md`            | Complete skill catalog (35 skills)      |
| `docs/INDEX.md`       | Skills directory (17 active skills)     |
| `docs/skills.md`      | Comprehensive skill catalog (35 skills) |
| `docs/PLAYBOOK.md`    | Detailed workflows & procedures         |
| `docs/FRAMEWORK.md`   | Architecture patterns & design          |
| `docs/EXPERIENCES.md` | Lessons learned & corrections           |
| `AGENTS.md`           | This navigation hub                     |
