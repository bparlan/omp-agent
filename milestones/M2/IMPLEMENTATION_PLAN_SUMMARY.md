# Implementation Plan Summary

## Overview

Enhanced session-audit system with:
1. **Multiple session audits** — `M{X}SA{Y}.md` format
2. **TEMP milestones** — Sessions without formal milestones
3. **Comprehensive documentation** — All OMP AEF docs updated
4. **Reverse order flow** — TEMP > Milestone
5. **Ingestion folder** — `/docs/ingest/` with manage-roadmap integration

## Key Changes

### 1. SA Document Format
**Before**: `M{X}SA.md`
**After**: `M{X}SA{Y}.md` (multiple sessions per milestone)

### 2. TEMP Milestone Support
**Before**: Only formal milestones
**After**: TEMP milestones for sessions without milestones

Directory structure:
```
milestones/
├── M2/
│   ├── SA1.md
│   ├── SA2.md
│   └── SA3.md
└── TEMP/
    ├── M1SA1.md
    ├── M2SA1.md
    └── M3SA1.md
```

### 3. Multiple Output Files from session-audit

For each session, session-audit now generates:

1. **`M{X}SA{Y}.md`** — Session Audit Document
2. **`SESSION_CHANGES.md`** — Change log
3. **`CHANGELOG_ENTRIES.md`** — Changelog entries
4. **`MILESTONE_UPDATES.md`** — Milestone updates
5. **`INGEST_ENTRIES.md`** — Ingestion entries (NEW)

### 4. /docs/ingest/ Folder

```
docs/ingest/
├── M2/
│   ├── sa1.md
│   └── sa2.md
├── TEMP/
│   ├── M1SA1.md
│   └── M2SA1.md
└── archive/
    └── (archived files)
```

### 5. manage-roadmap Integration

When `/docs/ingest/` contains files:
1. Prompt user for **permission**
2. Prompt user for **context**
3. Delegate to appropriate skill
4. Archive file after processing

## Implementation Phases

### Phase 1: Core SA Document Format (Day 1)
- Modify session-audit output to `M{X}SA{Y}.md`
- Add TEMP milestone detection
- Enhance code-search integration

### Phase 2: Comprehensive Documentation (Day 1)
- Generate changelog entries for all OMP AEF docs
- Generate milestone updates
- Identify files for ingestion

### Phase 3: TEMP > Milestone (Day 1-2)
- Implement reverse order logic
- Update evolve-skills to handle TEMP
- Add milestone promotion workflow

### Phase 4: /docs/ingest/ (Day 2)
- Create directory structure
- Add ingestion logic to sync-documentation
- Add manage-roadmap integration
- Archive files after processing

### Phase 5: evolve-skills Enhancement (Day 2)
- Process multiple SA documents
- Handle TEMP milestones
- Promote TEMP to formal milestones

### Phase 6: Testing (Day 2)
- Test multiple SA processing
- Test TEMP milestone handling
- Test ingestion workflow
- Test code-search integration

### Phase 7: Documentation Updates (Day 2)
- Update session-audit SKILL.md
- Update sync-documentation SKILL.md
- Update manage-roadmap SKILL.md

### Phase 8: Final Review (Day 2)
- Review all changes
- Test end-to-end
- Validate deliverables

## Skills to Modify

1. **session-audit** (NEW enhancements):
   - Multiple SA document format
   - TEMP milestone detection
   - Ingestion entries generation
   - Comprehensive changelog/milestone updates

2. **evolve-skills** (ENHANCED):
   - Process multiple SA documents
   - Handle TEMP milestones
   - Promote TEMP to formal milestones
   - Document in EVOLUTION.md

3. **sync-documentation** (ENHANCED):
   - Comprehensive documentation updates
   - Handle ingestion entries

4. **manage-roadmap** (ENHANCED):
   - Check /docs/ingest/ directory
   - Ask for permission + context
   - Archive files after processing

## Documentation Coverage

session-audit now updates all OMP AEF documents:

**Documentation**:
- `docs/CHANGELOG.md`
- `docs/MILESTONES.md`
- `docs/EXPERIENCES.md`
- `docs/ROADMAP.md`
- `docs/SKILL_SUMMARIES.md` (if exists)
- `docs/FRONTEND_GUIDE.md` (if exists)
- `docs/BACKEND_GUIDE.md` (if exists)

**Framework**:
- `~/.omp/agent/INDEX.md`
- `~/.omp/agent/AGENTS.md`
- `~/.omp/agent/README.md`
- `~/.omp/agent/FRAMEWORK.md`
- `~/.omp/agent/PLAYBOOK.md`

**Skills**:
- All `skills/*/SKILL.md`

**Configuration**:
- `~/.omp/agent/skills-lock.json`
- `~/.omp/agent/config.yml`

**Templates**:
- All `templates/*.md`

## Benefits

✅ **Multiple sessions tracked** — SA1, SA2, SA3... per milestone
✅ **TEMP milestones** — Handle sessions without formal milestones
✅ **Comprehensive documentation** — All OMP AEF docs stay in sync
✅ **Reverse order flow** — TEMP > Milestone, works both ways
✅ **Ingestion folder** — Centralized data ingestion
✅ **manage-roadmap integration** — Permission + context before processing
✅ **Archiving** — Original files archived after ingestion
✅ **Semi-agentic development** — SA documents serve as "milestone" for development

## Deliverables

### Files Created
1. `milestones/M2/SA1.md` (NEW format)
2. `milestones/M2/CHANGELOG_ENTRIES.md` (NEW)
3. `milestones/M2/MILESTONE_UPDATES.md` (NEW)
4. `milestones/M2/INGEST_ENTRIES.md` (NEW)

### Files Modified
1. `skills/session-audit/SKILL.md` (enhanced)
2. `skills/sync-documentation/SKILL.md` (enhanced)
3. `skills/manage-roadmap/SKILL.md` (enhanced)
4. `skills/evolve-skills/SKILL.md` (enhanced)

### Directories Created
1. `docs/ingest/` (NEW)
2. `docs/ingest/archive/` (NEW)
3. `docs/ingest/M2/` (NEW)
4. `docs/ingest/TEMP/` (NEW)

## Next Steps

1. **Review Implementation Plan** — Read `IMPLEMENTATION_PLAN.md` for detailed breakdown
2. **Approve Approach** — Confirm the TEMP > Milestone approach
3. **Start Phase 1** — Modify session-audit for multiple SA format
4. **Implement All Phases** — Follow the 8-phase plan
5. **Test Thoroughly** — Verify all functionality works end-to-end

## Questions for You

1. **Ingestion priority**: Should all modified files be candidates for ingestion, or only major changes?
2. **Archive retention**: Should archived files be kept indefinitely, or rotated/removed?
3. **TEMP milestone retention**: How long should TEMP milestones exist before requiring user action?
4. **SA consolidation**: Should evolve-skills consolidate multiple SA documents or keep them separate?

---

**Status**: Implementation plan created — awaiting your approval
**Next Action**: Review `IMPLEMENTATION_PLAN.md` and approve approach
