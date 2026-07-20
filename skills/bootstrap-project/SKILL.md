---
name: bootstrap-project
version: 1.0.1
description: Analyze an existing repository and normalize it into standard engineering structure. One-time setup for brownfield projects.
tools: read, write, bash, glob, grep, lsp
user-invocable: true
---

# Project Bootstrap: Normalize Repository Structure

You are a repository analyzer that transforms existing codebases into the project's canonical knowledge layer.

## When to Invoke

Typically executed once per repository or after major architectural changes.

## Your Process

1. **Discover repository structure** — Use `glob` to map the codebase, identify languages/build systems.
2. **Analyze build/package management** — Read `package.json`, `Cargo.toml`, `requirements.txt`, `Makefile`, etc.
3. **Map modules and architecture** — Use `lsp` and `grep` to identify components, entry points, interfaces.
4. **Identify tests and CI/CD** — Find test patterns, configuration files, workflows.
5. **Inventory existing documentation** — Read `README.md`, `docs/`, any project guides.
6. **Consolidate and normalize** — Merge documentation into canonical layer, remove duplication.
7. **Create missing documents in the `docs/` directory** — Generate `CHANGELOG.md`, `FRAMEWORK.md`, `SPEC.md`, `ROADMAP.md`, `PLAYBOOK.md`, `DATA.md`, `MILESTONES.md`, and `EXPERIENCES.md` as needed.
8. **Create root-level entry point documents** — Generate `README.md` and `AGENTS.md` (repository overview, build commands, preferred tool patterns) as needed.
9. **Create milestones directory structure** — Ensure `milestones/` and `milestones/archive/` directories exist.
10. **Produce documentation gap analysis** — Note what canonical docs still need attention.
11. **Recommend first milestone** — Suggest appropriate starting scope.

## Discovery Priority

1. **Project manifest** — `package.json`, `Cargo.toml`, `pom.xml`, `requirements.txt`
2. **Source structure** — `src/`, `lib/`, `pkg/`, root files
3. **Configuration** — `.env`, `config/`, deployment files
4. **Tests** — `test/`, `spec/`, `pytest.ini`, test scripts
5. **Documentation** — `README.md`, `docs/`, wiki content
6. **CI/CD** — `.github/workflows/`, `.gitlab-ci.yml`, etc.

## Code Analysis Strategy

**Prefer semantic discovery:**

- Use `code-search` skill if available: `~/devcode/aef/agent/skills/code-search/code-search.sh --skeletons`
- Generate index and skeletons before reading full files
- Identify entry points via `main` functions, route handlers, public APIs

**Read selectively:**

- Configuration to understand integration points
- Key module boundaries only when structural understanding insufficient
- Test setup to understand verification patterns

## Document Creation

### AGENTS.md

- Repository overview and entry point for agents
- Build and test commands
- Coding conventions if detectable
- Preferred tool patterns

### README.md

- Project overview and purpose
- Quick start guide
- Build and run instructions
- Link to canonical documentation layer

### CHANGELOG.md (docs/)

- Chronological record of changes
- Milestone releases with links to archived artifacts
- Version history and significant updates

### FRAMEWORK.md

- Architectural patterns
- Module organization
- Component relationships
- Extension guidelines

### SPEC.md

- Current system architecture as specification
- Public APIs and interfaces
- Data models

### ROADMAP.md

- Existing capabilities as completed items
- Known gaps as future items

### PLAYBOOK.md

- How to run/test/deploy
- Operational procedures
- Common tasks

### DATA.md

- Database schema (if any)
- Configuration schema
- Data flow patterns

### MILESTONES.md

- List all active milestones (initially empty)
- Format: `- [M{X}] - {goal} (active)` for active work
- Format: `- [M{X}] - {goal} (archived) → milestones/archive/M{X}/` for archived work

### EXPERIENCES.md

- Meta-learning ledger tracking framework friction and applied skill updates
- Two sections: "Active Friction Points" and "Applied Skill Updates (Resolved)"
- Record issues and solutions during skill evolution and hotfix scenarios
- Distill learnings into AGENTS.md or PLAYBOOK.md when they establish new coding conventions

## Documentation Principles

- **Repository reality first** — Code defines truth, docs follow
- **Merge, distill, normalize** — Combine scattered knowledge into coherent docs
- **Cross-reference** — Link related sections, avoid duplication
- **Preserve knowledge** — Keep architectural decisions and rationale
- **Eliminate obsolescence** — Remove outdated information

## Output Structure

```
{repository}/
├── README.md          # Created or updated with project overview and quick start
├── AGENTS.md          # Created or updated (agent entry point)

{repository}/docs/
├── CHANGELOG.md       # Created (chronological record of changes)
├── FRAMEWORK.md       # Created if missing
├── SPEC.md            # Created or updated
├── ROADMAP.md         # Created or updated
├── PLAYBOOK.md        # Created or updated
├── DATA.md            # Created if data components exist
├── MILESTONES.md      # Created (empty initially)
└── EXPERIENCES.md     # Created with Active Friction Points and Applied Skill Updates

{repository}/milestones/
├── archive/           # Created for archived milestones
└── M{X}/              # Future milestone directories
```

- Documentation gap analysis summary
## Documentation Principles

- **Repository reality first** — Code defines truth, docs follow
- **Merge, distill, normalize** — Combine scattered knowledge into coherent docs
- **Cross-reference** — Link related sections, avoid duplication
- **Preserve knowledge** — Keep architectural decisions and rationale
- **Eliminate obsolescence** — Remove outdated information

## Output Structure

```
{repository}/
├── README.md          # Created or updated with project overview and quick start
├── AGENTS.md          # Created or updated (agent entry point)

{repository}/docs/
├── CHANGELOG.md       # Created (chronological record of changes)
├── FRAMEWORK.md       # Created if missing
├── SPEC.md            # Created or updated
├── ROADMAP.md         # Created or updated
├── PLAYBOOK.md        # Created or updated
├── DATA.md            # Created if data components exist
└── MILESTONES.md      # Created (empty initially)

{repository}/milestones/
├── archive/           # Created for archived milestones
└── M{X}/              # Future milestone directories
```

- Documentation gap analysis summary

## Out of Scope

Never:
## Edit Tool Usage

### Single-line Replacements (Use `bash`)

For simple one-line edits, `bash` with `sed` is simpler and less error-prone:

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file

# Example: Fix a single instruction line
sed -i.bak '27s/.*/13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current {Y} sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol./' skills/generate-spec/SKILL.md
```

### Multi-line Block Edits (Use `edit`)

For structural changes with multiple lines, use the `edit` tool:

**Steps**:
1. Read the file with `read` to get `[PATH#HASH]`
2. Use `SWAP N.=N:` to replace a single line
3. Use `SWAP.BLK N:` to replace a complete block
4. Always use `+` prefix for new lines

**Example**:
```
[SKILL.md#ABC123]
SWAP 27.=27:
+13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol.
```


- Rewrite source code
- Perform refactoring
- Generate milestones, specifications, verification
- Perform Git operations
- Archive documents
- Modify implementation files


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
