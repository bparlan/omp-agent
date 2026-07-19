# sync-documentation Skill: Documentation Synchronizer

## Role in OMP AEF

`sync-documentation` maintains long-lived project documentation by distilling completed engineering work into canonical project documents, including `/docs/ingest/` file processing with permission + context workflow.

## Usage in Framework Skills

### When sync-documentation is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `review-implementation` | After review passes, sync to docs | `M{X}S{Y}R.md` → sync-documentation |
| `manage-roadmap` | After ingestion processed, update roadmap | `ARCHIVED` → manage-roadmap |

## Integration Points

### Documentation Sync Workflow

```bash
# Read completed artifacts
# Examine repository state
# Check for /docs/ingest/ entries
# Identify material changes
# Update documentation files
# Propose roadmap updates
# Write revision summary
```

## Requirements

### Prerequisites

1. **Completed Artifacts**
   - Milestone, specs, verifications, reviews
   - Completion reports, investigation reports
   - `EXPERIENCES.md`

2. **Templates**
   - Various documentation templates

### Setup

1. **Read Completed Artifacts:**
   ```bash
   read "milestones/M{X}/M{X}.md"
   read "milestones/M{X}/M{X}S{Y}.md"
   read "milestones/M{X}/M{X}S{Y}V.md"
   read "milestones/M{X}/M{X}S{Y}R.md"
   read "milestones/M{X}/M{X}S{Y}C.md"
   read "EXPERIENCES.md"
   ```

2. **Examine Repository State:**
   ```bash
   glob path="docs"
   grep path="docs"
   ```

3. **Check for Ingestion Entries:**
   ```bash
   if [ -f "INGEST_ENTRIES.md" ]; then
     # Handle ingestion workflow
   fi
   ```

## Best Practices

### Before Syncing

**Use sync-documentation when:**
- You want to update project documentation
- Milestone is complete and reviewed
- You want to handle `/docs/ingest/` files

**Avoid sync-documentation when:**
- You need to create new milestones (use `manage-roadmap`)
- You need to implement features (use `implement-specification`)
- Only cosmetic changes occurred

### Documentation Principles

**Describe reality:**
- Documentation reflects actual repository state

**Summarize, don't copy:**
- Extract essence, avoid duplication

**Remove obsolete:**
- Delete outdated information

**Be concise:**
- Every line should add value

**Match style:**
- Preserve existing tone and conventions

**Incremental updates:**
- Prefer targeted edits over rewrites

## Output

**Updated Documentation Files:**
- `MILESTONES.md` — Update milestone status
- `AGENTS.md` — Update build/test commands, coding patterns
- `DATA.md` — Update data models, configuration
- `ROADMAP.md` — Add completed milestones, propose future work
- `SPEC.md` — Update architecture, public interfaces
- `FRAMEWORK.md` — Update workflows, remove deprecated practices
- `PLAYBOOK.md` — Add procedures, update operational steps
- `CHANGELOG.md` — Append milestone summaries
- `README.md` — Update usage, remove deprecated features
- `EXPERIENCES.md` — Update friction points and skill updates

**Ingestion Workflow:**
- Processed files in appropriate directories
- Original files archived

**Roadmap Updates:**
- Proposed updates to `ROADMAP.md`
- User-approved changes applied

## Change Detection

Update documentation only when material changes occurred:
- Architecture changes
- Public API changes
- Repository structure changes
- Configuration changes
- Operational procedures
- User-visible behavior
- Deployment changes
- Workflow changes
- Supported platforms

## Ingestion Processing

**Process `/docs/ingest/` files only after explicit user permission.**

**Workflow:**
1. Read INGEST_ENTRIES.md
2. Display files to user
3. Ask for permission
4. Ask for context (what skill/prompt to use)
5. Delegate to appropriate skill
6. Archive original files after processing

## Template Reference

- **Documentation Templates**: `templates/*.md` in OMP agent directory
