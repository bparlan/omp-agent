# OMP AEF Skills Directory

This directory contains all available skills for the OMP Agentic Engineering Framework.

## Active Skills (22)

### Strategic Layer (3)

- **manage-roadmap** — Align `docs/ROADMAP.md` with goals, generate milestones
- **manage-development** — Orchestrate SDD pipeline, report cycles
- **milestone** — Elicit requirements, create `M{X}/M{X}.md`

### Core Development (7)

- **generate-spec** — Milestone → detailed specification (`M{X}S{Y}.md`)
- **generate-verification** — Spec → verification protocol (`M{X}S{Y}V.md`)
- **generate-tests** — Verification → test plan + scripts (`M{X}S{Y}T{Z}.md`)
- **implement-specification** — Spec → working code (`M{X}S{Y}C.md`)
- **evaluate-implementation** — Run tests, auto-fix bugs, generate E.md
- **review-implementation** — Compare implementation to spec, generate R.md
- **investigate-issue** — Analyze implementation issues, produce diagnosis
- **hotfix-issue** — Apply small, targeted bug fixes

### Support & Infrastructure (11)

- **code-search** — Semantic code analysis (used by session-audit)
- **bootstrap-project** — Initialize framework in new repo
- **session-audit** — Generate `SESSION_CHANGES.md` + supporting docs
- **evolve-skills** — Learn from `SESSION_CHANGES.md`, update `SKILL.md`
- **sync-documentation** — Update docs from `SESSION_CHANGES.md`
- **archive-docs** — Archive milestone artifacts and docs to `docs/archived/`
- **diagrammer** — Generates living Mermaid diagrams from codebase reality (docs/diagrams/)

## Documentation

- **[AGENTS.md](../AGENTS.md)** — Framework overview
- **[INDEX.md](../INDEX.md)** — Complete skill catalog
- **[SKILLS.md](../docs/SKILLS.md)** — Comprehensive skill catalog
- **[PLAYBOOK.md](../docs/PLAYBOOK.md)** — Operational workflows
- **[FRAMEWORK.md](../docs/FRAMEWORK.md)** — Architecture patterns

## Skill File Structure

Each skill directory contains:

- **SKILL.md** — Skill definition and operational instructions
- **README.md** — Skill overview and documentation entry point

## Usage

Skills are invoked through the OMP harness based on their `user-invocable: true` flag in the SKILL.md frontmatter. See INDEX.md for the complete skill catalog and AGENTS.md for framework architecture.