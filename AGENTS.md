# OMP Agent Directives

## Core Principles

- Follow YAGNI principles, and one-liner solutions.
- Optimize for correctness first, then for the next maintainer.

## Tooling Rules

### NEVER Overwrite Without Reading First
- **ALWAYS `read` before `write`** — Check if file exists with manual edits
- **Use `edit` for existing files** — Never use `write` on a file you haven't read in the same turn
- **`write` = new file only** — Reserve `write` for truly new files, not updates

### Skill Editing Protocol
- Read skill file before ANY modification
- Manual edits by user may be present
- Preserve human intent alongside skill instructions

### Artifact Preservation
- Never delete user files or directories
- Never overwrite custom templates without explicit approval
- Archive paths: move artifacts, don't overwrite originals

## Preferences

- Templates in `~/.omp/agent/templates/`
- Skills in `~/.omp/agent/skills/`
- Agents in `~/.omp/agent/agents/`

## Tool Policy

- LSP for code intelligence
- `read` for file inspection
- `edit` for surgical changes
- `write` for new files
- `bash` for git/terminal operations