---
generated-from: M2SA1.md
generated-date: 2026-07-18
original-file: milestones/M2/IMPLEMENTATION_PLAN.md
ingestion-folder: M2
delegated-to: evolve-skills
context: Read and document — Review implementation plan
action: CREATED
file-size: 22914 bytes
---

# Implementation Plan: Enhanced Session-Audit System

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

**Goal**: Modify session-audit to generate `M{X}SA{Y}.md`

**Steps**:
1. Update `session-audit` to detect milestone existence
2. Generate `M{X}SA{Y}.md` format instead of `M{X}SA.md`
3. Add TEMP milestone detection logic
4. Enhance code-search integration for semantic analysis

**Output**:
- Session Audit Document with SA1, SA2, SA3... numbering
- TEMP milestone structure support

**Testing**:
- Test with existing session
- Verify multiple SA numbering
- Verify TEMP milestone detection

### Phase 2: Comprehensive Documentation (Day 1)

**Goal**: Generate comprehensive documentation for all OMP AEF docs

**Steps**:
1. Update `session-audit` to generate CHANGELOG_ENTRIES.md
2. Update `session-audit` to generate MILESTONE_UPDATES.md
3. Update `session-audit` to generate INGEST_ENTRIES.md
4. Add comprehensive examples for all document types

**Output**:
- CHANGELOG_ENTRIES.md for all OMP AEF docs
- MILESTONE_UPDATES.md with progress tracking
- INGEST_ENTRIES.md with ingestion metadata

**Testing**:
- Generate outputs for all OMP AEF docs
- Verify format consistency
- Test with existing session

### Phase 3: TEMP > Milestone (Day 1-2)

**Goal**: Implement reverse order flow and TEMP milestone handling

**Steps**:
1. Enhance TEMP milestone detection in session-audit
2. Add priority flag for TEMP milestones
3. Implement reverse order flow (TEMP > Milestone)
4. Create TEMP milestone handling in session-audit
5. Add TEMP milestone auto-suggestion for closure
6. Update evolve-skills to handle TEMP milestones

**Output**:
- Reverse order flow implemented
- TEMP milestone structure support
- Milestone promotion workflow

**Testing**:
- Test TEMP milestone detection
- Test reverse order flow
- Test evolve-skills TEMP handling

### Phase 4: /docs/ingest/ (Day 2)

**Goal**: Create directory structure and integration

**Steps**:
1. Create directory structure (`/docs/ingest/{TEMP,M1,M2,M3,archived}/`)
2. Enhance `sync-documentation` v1.1.0 with ingestion processing workflow
3. Enhance `manage-roadmap` v1.2.0 with ingestion workflow integration
4. Implement permission + context workflow
5. Add archiving after processing
6. Document ingestion processing workflow

**Output**:
- `/docs/ingest/` directory structure
- Ingestion processing workflow
- Permission + context workflow
- Archiving procedure

**Testing**:
- Test directory creation
- Test permission + context workflow
- Test archiving procedure
- Test sync-documentation integration

### Phase 5: evolve-skills Enhancement (Day 2)

**Goal**: Process multiple SA documents and handle TEMP milestones

**Steps**:
1. Enhance `evolve-skills` v1.2.0
2. Add multiple SA detection and processing
3. Implement cumulative context processing
4. Add TEMP milestone priority handling
5. Create milestone promotion workflow
6. Create TEMP milestone closure workflow
7. Enhance EVOLUTION.md structure

**Output**:
- Multiple SA document processing
- Cumulative context processing
- TEMP milestone priority handling
- Milestone promotion workflow
- TEMP milestone closure workflow
- Enhanced EVOLUTION.md structure

**Testing**:
- Test multiple SA processing
- Test cumulative context
- Test TEMP milestone handling
- Test evolve-skills integration

### Phase 6: Testing and validation (Day 2)

**Goal**: Verify all functionality works end-to-end

**Steps**:
1. Verify skill integration (4 skills working together)
2. Validate multiple SA processing workflow
3. Test TEMP milestone handling
4. Verify ingestion workflow
5. Confirm documentation generation outputs
6. Validate all integration points

**Testing Matrix**:
- [ ] session-audit generates 5 output formats
- [ ] Multiple SA documents processed correctly
- [ ] TEMP milestones detected and handled
- [ ] Ingestion workflow works end-to-end
- [ ] All skills integrated properly
- [ ] Documentation generated correctly

**Output**:
- Comprehensive test results
- Integration validation
- Documentation verification

### Phase 7: Documentation Updates (Day 2)

**Goal**: Update all skill documentation

**Steps**:
1. Update `session-audit` SKILL.md v1.1.0 (enhanced)
2. Update `evolve-skills` SKILL.md v1.2.0 (enhanced)
3. Update `sync-documentation` SKILL.md v1.1.0 (enhanced)
4. Update `manage-roadmap` SKILL.md v1.2.0 (enhanced)
5. Add Infrastructure Skills section to AGENTS.md
6. Document all changes and features

**Output**:
- Updated SKILL.md files
- Updated AGENTS.md
- Complete documentation coverage

**Testing**:
- Verify all SKILL.md files updated
- Verify AGENTS.md updated
- Test links and references

### Phase 8: Final Review (Day 2)

**Goal**: Review all changes and validate deliverables

**Steps**:
1. Review all skills and documentation
2. Verify end-to-end workflow
3. Validate all deliverables
4. Confirm requirements met

**Review Criteria**:
- [ ] All 8 phases completed
- [ ] All deliverables created
- [ ] All requirements met
- [ ] Documentation updated
- [ ] Integration tested

**Output**:
- Final review report
- Deliverables verification
- Recommendations for next steps

## Skills to Modify

### 1. session-audit (NEW enhancements)

**New Features**:
- Multiple SA document format (M{X}SA{Y}.md)
- TEMP milestone detection and structure
- Ingestion entries generation (INGEST_ENTRIES.md)
- Comprehensive changelog/milestone updates
- SA dependency tracking across multiple sessions
- Session classification (major/minor changes)

**Documentation**:
- Comprehensive usage examples
- TEMP milestone handling guide
- Multiple SA workflow documentation
- Integration patterns with code-search

### 2. evolve-skills (ENHANCED)

**New Features**:
- Process multiple SA documents with cumulative context
- Handle TEMP milestones with priority
- Promote TEMP to formal milestones
- Create TEMP milestone closure workflow
- Enhanced EVOLUTION.md structure

**Documentation**:
- Multiple SA processing guide
- TEMP milestone workflow
- Milestone promotion/closure procedures

### 3. sync-documentation (ENHANCED)

**New Features**:
- Comprehensive documentation updates for all OMP AEF docs
- Handle ingestion entries from INGEST_ENTRIES.md
- Archive files after processing
- Permission + context workflow

**Documentation**:
- Comprehensive documentation update guide
- Ingestion processing workflow
- Archiving procedures

### 4. manage-roadmap (ENHANCED)

**New Features**:
- Check `/docs/ingest/` directory
- Ask for permission + context
- Delegate to appropriate skills
- Archive files after processing
- Update INGEST_ENTRIES.md status

**Documentation**:
- Ingestion workflow guide
- Permission + context workflow
- Archiving procedures

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
- `~/devcode/aef/agent/INDEX.md`
- `~/devcode/aef/agent/AGENTS.md`
- `~/devcode/aef/agent/README.md`
- `~/devcode/aef/agent/FRAMEWORK.md`
- `~/devcode/aef/agent/PLAYBOOK.md`

**Skills**:
- All `skills/*/SKILL.md`

**Configuration**:
- `~/devcode/aef/agent/skills-lock.json`
- `~/devcode/aef/agent/config.yml`

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
1. `milestones/M2/SA1.md` (NEW format with multiple sessions)
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

## Success Criteria

### Must Have (All Required)
✅ session-audit generates `M{X}SA{Y}.md`
✅ session-audit creates TEMP milestone structure
✅ session-audit generates comprehensive changelog entries
✅ session-audit generates milestone updates
✅ session-audit generates ingestion entries
✅ session-audit uses code-search for all analyses
✅ evolve-skills processes multiple SA documents
✅ evolve-skills handles TEMP milestones
✅ evolve-skills promotes TEMP to formal milestones
✅ manage-roadmap checks /docs/ingest/
✅ manage-roadmap asks for permission + context
✅ manage-roadmap archives files after processing
✅ All skills updated with version bumps
✅ All documentation updated

## Timeline Estimate

**Total Time**: ~25-30 hours over 2 days

- Day 1: ~14 hours (Phases 1-3)
- Day 2: ~14 hours (Phases 4-8)

## Next Steps

1. **Review Implementation Plan** — Read `IMPLEMENTATION_PLAN.md` for detailed breakdown
2. **Approve Approach** — Confirm the TEMP > Milestone approach
3. **Start Phase 1** — Modify session-audit for multiple SA format
4. **Implement All Phases** — Follow the 8-phase plan
5. **Test Thoroughly** — Verify all functionality works end-to-end
