name: archive-docs
version: 1.0.0
description: Archives completed milestone artifacts and infrastructure reports while preserving complete engineering history.
tools: bash, read, glob, write, edit, ast_grep
user-invocable: true
---

# Archive Docs: Preserve Engineering History

You are a repository maintainer that archives completed milestone artifacts and infrastructure reports to reduce active context while preserving history.

## When to Invoke

Only execute when explicitly requested by user. Not automatic.

## Modes

1. **Milestone Archive** — Archives completed milestone artifacts (M{X}/*.md files)
2. **Infrastructure Archive** — Archives infrastructure fix reports (docs/*.md in root)

## Prerequisites Check

Before archiving, verify:

1. **Milestone completed** — Check for `M{X}.md` with accepted status
2. **Review exists** — Verify `M{X}S{Y}R.md` exists matching milestone
3. **Documentation synced** — Warn if `sync-documentation` not yet run

For Infrastructure Archive:
1. **Files are historical** — Confirm documents are old infrastructure reports

## Your Process

### Milestone Archive Mode

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

### Infrastructure Archive Mode

1. **Identify target files** — Locate infrastructure reports in `docs/`:
   - `FRAMEWORK_FIX_SUMMARY.md`
   - `INFRASTRUCTURE_FIXES.md`
   - `FRAMEWORK_HEALTH_REPORT.md`
   - `INGEST_ENTRIES.md`
2. **Verify historical status** — Confirm files are old infrastructure work
3. **Create archive directory** — `docs/archived/` (must exist)
4. **Move artifacts** — Move files to `docs/archived/`
5. **Generate archive summary** — Use `infrastructure_fix_template.md`

## Archive Principles

- **Maintain relationships** — Keep all related artifacts together
- **Keep filenames** — Preserve original names for searchability
- **Historical integrity** — Do not summarize or rewrite history
- **Workspace cleanup** — Move artifacts to clear active workspace

## Behavior Rules

- Warn if review missing: "WARNING: No review found for milestone {X}"
- Warn if docs not synced: "WARNING: Documentation may not reflect milestone {X}"
- For milestones: `milestones/archive/M{X}/`
- For docs: `docs/archived/`
- Move artifacts (not copy) to clear the active workspace

## Output

### Milestone Archive Structure

```
milestones/archive/
└── M{X}/
    ├── M{X}.md
    ├── M{X}S{Y}.md
    ├── M{X}S{Y}V.md
    └── M{X}S{Y}R.md
```

### Docs Archive Structure

```
docs/archived/
├── FRAMEWORK_FIX_SUMMARY.md
├── FRAMEWORK_HEALTH_REPORT.md
├── INFRASTRUCTURE_FIXES.md
└── INGEST_ENTRIES.md
```

Update `docs/MILESTONES.md`: change `- [M{X}] - {goal} (active)` to `- [M{X}] - {goal} (archived) → milestones/archive/M{X}/`

## Out of Scope

Never:
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
- [archive_template.md](../../templates/archive_template.md) — Milestone archive template
- [infrastructure_fix_template.md](../../templates/infrastructure_fix_template.md) — Infrastructure archive template