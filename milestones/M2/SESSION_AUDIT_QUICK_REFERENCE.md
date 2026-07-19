---
quick-reference-type: Session-Audit Workflow
version: 1.0.0
purpose: Quick reference for session-audit workflow
---

# Session-Audit Quick Reference

## Overview

Session-audit is a template-driven workflow that generates 5 output formats for every session, ensuring comprehensive documentation and traceable changes.

## Workflow Overview

```
Session Work → session-audit → 5 Output Formats → /docs/ingest/ → evolve-skills → Updates
```

## 5 Output Formats

### 1. M{X}SA{Y}.md — Session Audit Document
- **Purpose**: Primary session audit report
- **Content**: Session metadata, classification, recommendations, progress
- **Location**: `milestones/{milestone}/M{X}SA{Y}.md`
- **Example**: `milestones/M2/M2SA1.md`

### 2. SESSION_CHANGES.md — Change Log
- **Purpose**: Summary of changes made in the session
- **Content**: File list, descriptions, deliverables
- **Location**: `milestones/{milestone}/SESSION_CHANGES.md`
- **Example**: `milestones/M2/SESSION_CHANGES.md`

### 3. CHANGELOG_ENTRIES.md — Changelog
- **Purpose**: Auto-generated changelog entries
- **Content**: "Added", "Changed", "Fixed" sections
- **Location**: `milestones/{milestone}/CHANGELOG_ENTRIES.md`
- **Example**: `milestones/M2/CHANGELOG_ENTRIES.md`

### 4. MILESTONE_UPDATES.md — Milestone Updates
- **Purpose**: Progress tracking and milestone status
- **Content**: Progress percentages, activity summary, version updates
- **Location**: `milestones/{milestone}/MILESTONE_UPDATES.md`
- **Example**: `milestones/M2/MILESTONE_UPDATES.md`

### 5. INGEST_ENTRIES.md — Ingestion Entries
- **Purpose**: File identification for /docs/ingest/ workflow
- **Content**: Files identified, suggested actions, delegated skills, workflow steps
- **Location**: `milestones/{milestone}/INGEST_ENTRIES.md`
- **Example**: `milestones/M2/INGEST_ENTRIES.md`

## Integration with Skills

### session-audit
- **Role**: Generates 5 output formats using templates
- **Trigger**: At end of every session
- **Output**: 5 companion files for each SA document

### manage-roadmap
- **Role**: Checks INGEST_ENTRIES.md, processes with permission + context
- **Trigger**: When INGEST_ENTRIES.md exists
- **Output**: Processed files, archived files, updated INGEST_ENTRIES.md

### evolve-skills
- **Role**: Reads SA documents, processes recommendations
- **Trigger**: When SA documents are processed
- **Output**: Updated SKILL.md files, EVOLUTION.md

### sync-documentation
- **Role**: Updates /docs/ingest/ files
- **Trigger**: When delegated by manage-roadmap
- **Output**: Updated documentation files

### code-search
- **Role**: Provides semantic analysis for SA documents
- **Trigger**: When invoked by session-audit
- **Output**: Analysis results for SA documents

## Directory Structure

### SA Documents
```
milestones/
├── M2/
│   ├── M2SA.md (original manual)
│   ├── M2SA1.md (new generated)
│   ├── M2SA2.md (future)
│   ├── SESSION_CHANGES.md
│   ├── CHANGELOG_ENTRIES.md
│   ├── MILESTONE_UPDATES.md
│   ├── INGEST_ENTRIES.md
│   └── [other M2 docs]
├── TEMP/
│   ├── TEMP_M1SA1.md
│   ├── SESSION_CHANGES.md
│   ├── CHANGELOG_ENTRIES.md
│   ├── MILESTONE_UPDATES.md
│   └── INGEST_ENTRIES.md
└── archive/
    └── [archived files]
```

### Ingestion Files
```
docs/ingest/
├── TEMP/ (TEMP milestone files)
├── M1/ (M1 milestone files)
├── M2/ (M2 milestone files)
├── M3/ (M3 milestone files)
└── archived/ (original files after processing)
```

## TEMP Milestone

### When to Use TEMP
- Sessions without formal milestone
- Exploration sessions
- Planning sessions
- Pre-milestone work

### TEMP Milestone Structure
- **File Naming**: `M{N}SA{Y}.md` in `milestones/TEMP/`
- **Example**: `TEMP_M1SA1.md`
- **Features**:
  - Reverse order flow (TEMP > Milestone)
  - Auto-suggestion for closure/promotion
  - Can be promoted to formal milestone later

### TEMP Milestone Promotion
1. Rename TEMP_M1SA1 to M1SA1
2. Move from `milestones/TEMP/` to `milestones/M1/`
3. Update all references
4. Delete original from TEMP after approval

## Usage Examples

### Example 1: Framework Improvement Session

**Session Work**:
```bash
# User completes session work on framework
```

**Session-Audit Generation**:
```bash
# Run session-audit skill
session-audit
```

**Outputs Generated**:
- `milestones/M2/M2SA2.md` — Session audit document
- `milestones/M2/SESSION_CHANGES.md` — Change log
- `milestones/M2/CHANGELOG_ENTRIES.md` — Changelog
- `milestones/M2/MILESTONE_UPDATES.md` — Milestone updates
- `milestones/M2/INGEST_ENTRIES.md` — Ingestion entries

**Ingestion Workflow**:
```bash
# Run manage-roadmap
manage-roadmap
```

**Processing**:
- manage-roadmap checks INGEST_ENTRIES.md
- Presents files to user
- User approves with context
- Files written to /docs/ingest/M2/
- Original files archived
- INGEST_ENTRIES.md updated

**Evolution**:
```bash
# Run evolve-skills
evolve-skills
```

**Processing**:
- evolve-skills reads M2SA2.md
- Processes recommendations (ordered by priority)
- Applies changes to SKILL.md files
- Bumps version numbers
- Documents in EVOLUTION.md

## Key Benefits

### 1. Consistency
- All sessions follow same pattern
- All outputs use same templates
- Easy to find and parse information

### 2. Automation
- 5 output formats generated automatically
- No manual documentation required
- Templates ensure completeness

### 3. Traceability
- Every change is documented
- Dependencies tracked between SAs
- Complete audit trail

### 4. Integration
- Seamless integration with existing skills
- Well-defined integration points
- Clear handoffs between skills

### 5. Scalability
- Supports multiple SAs per milestone
- Cumulative context across sessions
- TEMP milestone support

## Classification System

### Major Changes
- New skills
- Significant structure changes
- Template modifications
- Core framework changes
- Breaking changes

### Minor Changes
- Bug fixes
- Small improvements
- Documentation updates
- Cosmetic changes
- Non-breaking changes

## Progress Tracking

### Session Progress
```
Session 1 of X: ████████░░░░░░ 80%
Session 2 of X: ██████░░░░░░░ 50%
Session 3 of X: ██░░░░░░░░░░░ 20%
```

### Milestone Completion
```
M2: ███████████████████░░ 85%
M3: ░░░░░░░░░░░░░░░░░░░░ 0%
```

## Recommended Actions

### High Priority
- [HIGH] Apply recommended evolve-skills actions
- [HIGH] Process INGEST_ENTRIES.md
- [HIGH] Archive original files

### Medium Priority
- [MEDIUM] Continue session work
- [MEDIUM] Process remaining INGEST_ENTRIES.md entries

### Low Priority
- [LOW] Clean up temporary files
- [LOW] Update documentation

## Quick Commands

### Run Session-Audit
```bash
session-audit
```

### Run Manage-Roadmap
```bash
manage-roadmap
```

### Run Evolve-Skills
```bash
evolve-skills
```

### List All SA Reports
```bash
find milestones -name "*SA*.md" | sort
```

## Common Patterns

### Pattern 1: SA1 First SA for Milestone
- Cumulative context: None (build on previous SAs)
- Dependencies: None
- Progress tracking: Start at 0%

### Pattern 2: SA2+ for Milestone
- Cumulative context: Build on SA1, SA2, SA3...
- Dependencies: Track previous SAs
- Progress tracking: Continue from previous session

### Pattern 3: TEMP Milestone
- Cumulative context: None (first SA for TEMP)
- Dependencies: None
- Progress tracking: TEMP milestones don't have progress
- Special handling: Auto-suggest closure/promotion

## Best Practices

### ✅ Do
- Run session-audit at end of every session
- Classify changes correctly (major vs minor)
- Use TEMP for exploration sessions
- Process INGEST_ENTRIES.md regularly
- Archive original files after processing
- Read previous SAs before creating new ones

### ❌ Don't
- Skip session-audit for small changes
- Use session-audit for temporary exploration
- Leave SA documents without processing
- Forget to archive original files
- Ignore recommended actions

## Troubleshooting

### Issue: SA Document Not Generated
**Solution**: Check git status for uncommitted changes, ensure session-audit skill is up to date

### Issue: INGEST_ENTRIES.md Not Found
**Solution**: Ensure session-audit was run, check milestone directory structure

### Issue: evolve-skills Not Processing
**Solution**: Check SA document recommendations, ensure evolve-skills is up to date

### Issue: Files Not Archived
**Solution**: Check manage-roadmap processing status, verify archive directory permissions

## Conclusion

Session-audit provides a template-driven, well-integrated method for session-focused development that ensures comprehensive documentation and traceable changes. By following this workflow, you maintain a complete audit trail while leveraging the existing skill ecosystem.

---

**Document Type**: Quick Reference
**Version**: 1.0.0
**Created**: 2026-07-18
**Status**: Complete
