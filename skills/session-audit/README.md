# session-audit Skill: Session Analysis and Documentation

## Role in OMP AEF

`session-audit` analyzes session-based framework improvements and generates comprehensive documentation for evolve-skills, including multiple session audits (SA1, SA2, SA3...), TEMP milestone structure, and ingestion entries.

## Usage in Framework Skills

### When session-audit is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `evolve-skills` | After session audit, apply improvements | `M{X}SA{Y}.md` → evolve-skills |
| `manage-roadmap` | After session audit, handle ingestion | `INGEST_ENTRIES.md` → manage-roadmap |

## Integration Points

### Session Audit Workflow

```bash
# Scan session changes
# Classify changes
# Generate SA document
# Generate change log
# Generate changelog entries
# Generate milestone updates
# Generate ingestion entries
```

## Requirements

### Prerequisites

1. **Session Artifacts**
   - Modified files from git or filesystem timestamps
   - Framework-critical locations

2. **Templates**
   - Various documentation templates

### Setup

1. **Scan Session Changes:**
   ```bash
   # Detect modified files
   git status --short
   # Or filesystem timestamps
   ```

2. **Classify Changes:**
   - Track: INDEX.md, AGENTS.md, README.md, FRAMEWORK.md, PLAYBOOK.md, skills-lock.json, config.yml, skill SKILL.md files
   - Do NOT Track: Cosmetic changes, reformatting, comment updates

## Best Practices

### Before Auditing

**Use session-audit when:**
- You want to analyze session-based framework improvements
- You need to generate comprehensive documentation
- You want to identify patterns for evolve-skills

**Avoid session-audit when:**
- You need to implement features (use `implement-specification`)
- You need to review existing work (use `review-implementation`)

### Session Audit Principles

**Evidence-based:**
- Every change must have a documented reason

**Restricted Scope:**
- Analyze and update only Spec-Driven Development skills

**Cumulative Processing:**
- Process multiple SAs in order, building on cumulative context

## Output

**Session Audit Documents:**
- `M{X}SA{Y}.md` — Session Audit Document with metadata, files modified, classification, code-search analysis, recommended actions
- `SESSION_CHANGES.md` — Change log with list of modified files and descriptions
- `CHANGELOG_ENTRIES.md` — Changelog entries in "Added", "Changed", "Fixed" sections
- `MILESTONE_UPDATES.md` — Milestone updates with progress percentages and status updates
- `INGEST_ENTRIES.md` — Ingestion entries with all modified files and metadata

**File Locations:**
- **Normal milestone**: `milestones/M{X}/`
- **TEMP milestone**: `milestones/TEMP/M{N}SA{Y}.md`

## Numbering Strategy

- SA documents are numbered sequentially per milestone: SA1, SA2, SA3...
- If session audit finds no milestone, creates TEMP milestone structure
- TEMP milestones use M{N} prefix: M1SA1, M2SA1, M3SA1...
- Numbering is incremental based on session count

## Code-Search Integration

**Use code-search for:**
1. Find OMP AEF documents
2. Analyze framework changes
3. Verify infrastructure changes
4. Find milestones for progress tracking
5. Check for code-search usage in skills

## Template Reference

- **Session Audit Templates**: `templates/*.md` in OMP agent directory
