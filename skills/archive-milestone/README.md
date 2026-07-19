# archive-milestone Skill: Milestone Archiver

## Role in OMP AEF

`archive-milestone` archives completed milestone artifacts while preserving complete engineering history.

## Usage in Framework Skills

### When archive-milestone is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `review-implementation` | After review passes, archive milestone | `M{X}S{Y}R.md` → archive-milestone |
| `sync-documentation` | Before archiving, ensure docs are synced | `M{X}S{Y}R.md` → sync-documentation |

## Integration Points

### Archiving Workflow

```bash
# Verify prerequisites
# Identify artifacts
# Create archive directory
# Move artifacts
# Generate archive summary
# Update MILESTONES.md
```

## Requirements

### Prerequisites

1. **Milestone Completed**
   - Milestone with accepted status (`M{X}.md`)
   - Review report exists (`M{X}S{Y}R.md`)

2. **Documentation Synced**
   - Sync-documentation has run
   - Documentation reflects milestone

3. **Templates**
   - Archive template: `~/devcode/aef/agent/templates/archive_template.md`

### Setup

1. **Verify Prerequisites:**
   ```bash
   # Check for accepted milestone
   grep "accepted" milestones/M{X}/M{X}.md

   # Verify review exists
   [ -f "milestones/M{X}/M{X}S{Y}R.md" ]
   ```

2. **Identify Artifacts:**
   ```bash
   # Find all artifacts using code-search
   ast_grep pattern="M{X}" path="milestones/M{X}"
   ```

3. **Determine Archive Location:**
   - Target: `milestones/archive/M{X}/`

## Best Practices

### Before Archiving

**Use archive-milestone when:**
- All specifications for the milestone are completed and reviewed
- Documentation is synced
- You want to preserve history while clearing active workspace

**Avoid archive-milestone when:**
- Milestone is not complete
- Review is missing
- Documentation is not synced
- You are still working on the milestone

### Archiving Principles

**Maintain relationships:**
- Keep all related artifacts together

**Keep filenames:**
- Preserve original names for searchability

**Historical integrity:**
- Do not summarize or rewrite history

**Workspace cleanup:**
- Move artifacts to clear active workspace

## Output

**Archive Directory Structure:**
```
milestones/archive/
└── M{X}/
    ├── M{X}.md
    ├── M{X}S{Y}.md
    ├── M{X}S{Y}V.md
    └── M{X}S{Y}R.md
```

**Archive Summary:**
- File: `milestones/archive/M{X}/M{X}A.md`
- Format: Archive template from `templates/archive_template.md`
- Contents: Summary of archived artifacts

**Updated MILESTONES.md:**
- Changed from `(active)` to `(archived) → milestones/archive/M{X}/`

## Out of Scope

**Never:**
- Modify implementation
- Modify tests
- Regenerate specifications
- Regenerate reviews
- Rewrite documentation
- Perform Git operations
- Delete historical information
- Apply changes to archived artifacts

## Behavior Rules

**Warn if:**
- Review missing: "WARNING: No review found for milestone {X}"
- Docs not synced: "WARNING: Documentation may not reflect milestone {X}"

**Create archive directory structure:**
- `project_folder/milestones/archive/M{X}/`

**Move artifacts (not copy):**
- Clear the active workspace

**Always enforce M{X}A.md naming convention:**
- For the summary file
