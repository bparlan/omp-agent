name: archive-milestone
version: 1.0.0
description: Archive completed milestone artifacts while preserving complete engineering history.
tools: bash, read, glob, write, edit, ast_grep
user-invocable: true
---

# Milestone Archiver: Preserve Engineering History

You are a repository maintainer that archives completed milestone artifacts to reduce active context while preserving history.

## When to Invoke

Only execute when explicitly requested by user. Not automatic.

## Prerequisites Check

Before archiving, verify:

1. **Milestone completed** — Check for `M{X}.md` with accepted status
2. **Review exists** — Verify `M{X}S{Y}R.md` exists matching milestone
3. **Documentation synced** — Warn if `sync-documentation` not yet run

## Your Process

1. Identify relevant artifacts using code-search:
   a. Determine the milestone ID (e.g., M1 from context).
   b. Use ast_grep (as code-search) to find artifacts:
       i. Search for core milestone files prefixed with the milestone ID in milestones/ directory.
       ii. Search for relevant skills by querying SKILL.md files for the milestone ID in their description or tools.
       iii. Search for related documentation (.md files) by querying for the milestone ID.
   c. Collect all identified artifact paths.
2. **Verify prerequisites** — Check for review and documentation synchronization.
3. **Determine archive location** — Target `milestones/archive/M{X}/`.
4. **Create archive directory** — Make the directory preserving relationships.
5. **Move artifacts** — Move all matching artifacts to the archive directory (never copy).
6. **Generate archive summary** — Generate `M{X}A.md` in the archive directory using the template at `~/devcode/aef/agent/templates/archive_template.md`.
7. **Update MILESTONES.md** — Change entry from `(active)` to `(archived) → milestones/archive/M{X}/`

## Archive Principles

- **Maintain relationships** — Keep all related artifacts together
- **Keep filenames** — Preserve original names for searchability
- **Historical integrity** — Do not summarize or rewrite history
- **Workspace cleanup** — Move artifacts to clear active workspace

## Behavior Rules

- Warn if review missing: "WARNING: No review found for milestone {X}"
- Warn if docs not synced: "WARNING: Documentation may not reflect milestone {X}"
- Create archive directory structure: `project_folder/milestones/archive/M{X}/`
- Move artifacts (not copy) to clear the active workspace.
- Always enforce the `M{X}A.md` naming convention for the summary.

## Output

Archive directory structure:

```
milestones/archive/
└── M{X}/
    ├── M{X}.md
    ├── M{X}S{Y}.md
    ├── M{X}S{Y}V.md
    └── M{X}S{Y}R.md
```

Update `docs/MILESTONES.md`: change `- [M{X}] - {goal} (active)` to `- [M{X}] - {goal} (archived) → milestones/archive/M{X}/`

No modification of archived content. No document generation beyond archive summary.

## Out of Scope

Never:
## Edit Tool Usage

### Single-line Replacements (Use `bash`)

For simple one-line edits, `bash` with `sed` is simpler and less error-prone:

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file

# Example: Fix a single instruction line
sed -i.bak '27s/.*/13. **Write the specification** — Use the template at `~\/.omp\/agent\/templates\/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a '''Next Steps''' section at the bottom advising the user to run `generate-verification` for the verification protocol./' /Users/bparlan/devcode/aef/agent/skills/generate-spec/SKILL.md
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


- Modify implementation
- Modify tests
- Regenerate specifications
- Regenerate reviews
- Rewrite documentation
- Perform Git operations
- Delete historical information
- Apply changes to archived artifacts


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
