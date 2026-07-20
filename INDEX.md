# OMP Agentic Engineering Framework Index

## Overview

The OMP Agentic Engineering Framework is a set of specialized subagents that orchestrate different phases of the software development lifecycle (SDLC). Each agent has a specific role, scope, and operational boundaries.

## Skills Catalog

All 36 skills are documented in detail in `docs/SKILLS.md`.

### Quick Reference by Layer

**Strategic Layer (3 agents)**:
- manage-roadmap — Align ROADMAP.md with goals, generate milestones
- manage-development — Orchestrate SDD pipeline, report cycles
- milestone — Elicit requirements, create M{X}.md

**Core Development (7 agents)**:
- generate-spec — Milestone → detailed specification (M{X}S{Y}.md)
- implement-specification — Spec → working code (M{X}S{Y}C.md)
- generate-verification — Spec → verification protocol (M{X}S{Y}V.md)
- generate-tests — Verification → test plan + scripts (M{X}S{Y}T{Z}.md)
- evaluate-implementation — Run tests, auto-fix bugs, generate E.md
- review-implementation — Compare implementation to spec, generate R.md

**Support & Infrastructure (8 agents)**:
- session-audit — Generate SESSION_CHANGES.md + supporting docs
- investigate-issue / hotfix-issue — Debug and fix specific issues
- archive-docs — Archive milestone artifacts and docs to docs/archived/
- evolve-skills — Learn from SESSION_CHANGES.md, update SKILL.md
- sync-documentation — Update docs from SESSION_CHANGES.md
- code-search — Semantic code analysis (used by session-audit)
- bootstrap-project — Initialize framework in new repo
- diagrammer — Generates living Mermaid diagrams from codebase reality

📖 **Detailed Catalog**: See `docs/SKILLS.md`

## Agent Interaction Pipeline

The framework orchestrates agent interactions through a well-defined pipeline:

```
User → milestone → generate-spec → implement-specification → generate-verification → generate-tests → evaluate-implementation → review-implementation
```

Each agent handoffs to the next, maintaining clear boundaries and avoiding redundant work.

## Quick Links

- **[SKILLS.md](../docs/SKILLS.md)** — Comprehensive skill catalog (36 skills)
- **[AGENTS.md](./AGENTS.md)** — Lightweight navigation hub (~110 lines)
- **[ROADMAP.md](../docs/ROADMAP.md)** — Project roadmap and feature planning
- **[MILESTONES.md](../docs/MILESTONES.md)** — Completed milestone artifacts and history
- **[FRAMEWORK.md](../docs/FRAMEWORK.md)** — Architecture patterns and design
- **[PLAYBOOK.md](../docs/PLAYBOOK.md)** — Operational playbook and workflows
- **[EXPERIENCES.md](../docs/EXPERIENCES.md)** — Lessons learned and corrections
- **[skills-lock.json](./skills-lock.json)** — Skill configuration and dependencies
- **[config.yml](./config.yml)** — Model routing and framework configuration

## Search

Use the search functionality in your IDE or markdown viewer to find specific agents.
