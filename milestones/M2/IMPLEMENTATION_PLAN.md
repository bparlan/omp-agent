# Session Audit Enhancement Implementation Plan

## Goal

Enhance the session-audit system to support:
1. Multiple session audits per milestone (`M{X}SA{Y}.md`)
2. Session audits without milestones (TEMP structure)
3. Comprehensive documentation updates (all OMP AEF docs)
4. Reverse order TEMP > Milestone flow
5. `/docs/ingest/` folder for data ingestion with `manage-roadmap` integration
6. Automatic archiving after ingestion

## Phase 1: Core SA Document Format (Day 1)

### 1.1 Modify session-audit Output Format

**Current**:
- `M{X}SA.md` (single session document)

**New**:
- `M{X}SA{Y}.md` (multiple sessions per milestone)
- `milestones/TEMP/M{N}SA{Y}.md` (sessions without milestones)
- Numbering: SA1, SA2, SA3, ...

**Changes to session-audit/SKILL.md**:
```markdown
# Output Format

## Files Generated

1. **M{X}SA{Y}.md** — Session Audit Document
   - Session metadata (date, session-id, milestone)
   - Files modified/created
   - Classification (major/minor)
   - Code-search analysis results
   - Recommended evolve-skills actions
   - Dependencies on previous SA documents
   - Progress toward milestone completion (if milestone exists)

2. **SESSION_CHANGES.md** — Change log
   - List of modified files
   - Brief description of changes
   - References to SA documents

3. **CHANGELOG_ENTRIES.md** — Changelog entries
   - Each entry in standard changelog format
   - Sections: "Added", "Changed", "Fixed"
   - Auto-generated

4. **MILESTONE_UPDATES.md** — Milestone updates
   - Updated status fields (progress, completion %)
   - Milestone completion markers
   - Auto-generated

5. **INGEST_ENTRIES.md** — Ingestion entries (NEW)
   - Files identified for ingestion
   - Ingestion metadata
   - Auto-generated

## Numbering Strategy

- SA documents are numbered sequentially per milestone: SA1, SA2, SA3...
- If session audit finds no milestone, creates TEMP milestone structure
- TEMP milestones use M{N} prefix: M1SA1, M2SA1, M3SA1...
```

### 1.2 Modify session-audit Detection Logic

**Changes to session-audit/SKILL.md**:
```markdown
# Detect Milestone for SA Document

## Find Existing Milestone

1. Check if milestone already exists:
   ```bash
   ls milestones/
   ```

2. If milestone found (e.g., M2):
   - Determine highest SA number: SA1, SA2, SA3...
   - Increment for new session
   - Create `milestones/M2/SA{Y}.md`

3. If milestone not found:
   - Create TEMP milestone structure
   - Use session count as prefix: `milestones/TEMP/M{N}SA{Y}.md`
   - Session-audit will detect TEMP structure later

## TEMP Milestone Handling

If TEMP milestone detected:
- Store in `milestones/TEMP/M{N}SA{Y}.md`
- Mark as "temporary milestone"
- Note for later promotion to proper milestone
```

### 1.3 Enhance Code-Search Analysis

**Changes to session-audit/SKILL.md**:
```markdown
# Code-Search Integration

## Use code-search for Multiple Purposes

1. **Find OMP AEF documents for changelog**:
   - Search for all documentation files
   - Identify which docs were modified
   - Extract changelog-worthy changes

2. **Analyze framework changes**:
   - Search for agent handoff patterns
   - Identify template usage changes
   - Check consistency of negative guardrails

3. **Verify infrastructure changes**:
   - Search for code-search references
   - Verify SKILL.md files use code-search appropriately
   - Check for missing infrastructure skills

4. **Find milestones for progress tracking**:
   - Search for existing M{X}.md files
   - Extract milestone metadata (version, current phase)
   - Calculate progress percentage
```

## Phase 2: Comprehensive Documentation Updates (Day 1)

### 2.1 Update session-audit Documentation Output

**Changes to session-audit/SKILL.md**:
```markdown
# Documentation to Generate

## Generate for All Modified OMP AEF Documents

### 1. CHANGELOG_ENTRIES.md
For each modified document, generate changelog entries:
- `docs/CHANGELOG.md` — General changelog
- `docs/MILESTONES.md` — Milestone-specific updates
- `docs/EXPERIENCES.md` — Developer experiences
- `docs/ROADMAP.md` — Roadmap progress updates
- `skills/*/SKILL.md` — Skill updates (if major)
- `~/.omp/agent/INDEX.md` — Index updates
- `~/.omp/agent/AGENTS.md` — Agent documentation updates

### 2. MILESTONE_UPDATES.md
For each modified milestone:
- Update progress percentage
- Update status (in-progress, nearly-complete, completed)
- Mark completion if 100%
- Add changelog reference

### 3. INGEST_ENTRIES.md
For files identified for ingestion:
- Source file path
- Target skill/prompt
- Ingestion metadata
- Archive destination
```

### 2.2 Document All OMP AEF Docs in session-audit

**Changes to session-audit/SKILL.md**:
```markdown
# OMP AEF Documents List

## Documentation Files

1. `docs/CHANGELOG.md` — General changelog
2. `docs/MILESTONES.md` — Milestone tracking
3. `docs/EXPERIENCES.md` — Developer experiences
4. `docs/ROADMAP.md` — Roadmap tracking
5. `docs/SKILL_SUMMARIES.md` — Skill summaries (if exists)
6. `docs/FRONTEND_GUIDE.md` — Frontend guide (if exists)
7. `docs/BACKEND_GUIDE.md` — Backend guide (if exists)

## Framework Files

1. `~/.omp/agent/INDEX.md` — Agent index
2. `~/.omp/agent/AGENTS.md` — Agent documentation
3. `~/.omp/agent/README.md` — Project README
4. `~/.omp/agent/FRAMEWORK.md` — Framework documentation
5. `~/.omp/agent/PLAYBOOK.md` — Playbook

## Skills

All `skills/*/SKILL.md` files

## Configuration

1. `~/.omp/agent/skills-lock.json`
2. `~/.omp/agent/config.yml`

## Templates

All `templates/*.md` files

## Check for Additional Files

1. Search for `docs/*.md` files
2. Search for additional config files
3. Search for documentation in root directory
4. List any discovered files
```

## Phase 3: TEMP > Milestone Reverse Order (Day 1-2)

### 3.1 Implement Reverse Order Logic

**Changes to session-audit/SKILL.md**:
```markdown
# Reverse Order: TEMP > Milestone

## Priority Order for SA Document Creation

1. **First**: Check for existing milestone
   ```bash
   ls milestones/
   ```

2. **Second**: If no milestone, check for TEMP milestone
   ```bash
   ls milestones/TEMP/
   ```

3. **Third**: If neither, create new milestone (or notify user)

## TEMP Milestone Creation

If no milestone exists:
1. Create `milestones/TEMP/` directory if it doesn't exist
2. Use session count as milestone prefix: M1SA1, M2SA1, M3SA1...
3. Create `milestones/TEMP/M{N}SA{Y}.md`

## Milestone Promotion Workflow

When user wants to promote TEMP milestone:

1. **Ask for permission**:
   ```
   User: Should I promote M1SA1 to M1? (promote TEMP milestone to formal milestone)
   ```

2. **If approved**:
   - Rename `milestones/TEMP/M1SA1.md` → `milestones/M1.md`
   - Create `milestones/M1/SA1.md` (move SA document)
   - Update references in framework
   - Update docs/MILESTONES.md
   - Notify user of promotion

3. **If rejected**:
   - Continue with TEMP milestone
   - User can still work on it as-is
```

### 3.2 Update evolve-skills to Handle TEMP Milestones

**Changes to evolve-skills/SKILL.md**:
```markdown
# Handle TEMP Milestones

## Priority Order for Processing

1. **Check for TEMP milestones first**:
   ```bash
   ls milestones/TEMP/
   ```

2. **Process TEMP milestones**:
   - Treat like normal milestones
   - Apply recommended actions
   - Update documentation
   - Note TEMP nature in EVOLUTION.md

3. **Then check for normal milestones**:
   - Process normally
   - No TEMP marker in output

## TEMP Milestone Marking

In EVOLUTION.md, mark TEMP milestones:
```markdown
## 2026-07-18: TEMP Milestone M1SA1 Processing
- **Skill**: evolve-skills
- **Milestone**: M1SA1 (TEMP)
- **Status**: Completed
- **Notes**: Temporary milestone created for session tracking
```

## Milestone Promotion After Processing

After evolve-skills processes all TEMP milestones:
- Check if any should be promoted
- If user approves, promote to formal milestone
- Move SA documents from TEMP to proper milestone structure
- Update framework references
```

## Phase 4: /docs/ingest/ Folder (Day 2)

### 4.1 Create /docs/ingest/ Directory Structure

**Changes to sync-documentation/SKILL.md**:
```markdown
# Ingestion Directory Structure

## Directory Layout

```
docs/
├── ingest/
│   ├── M1/
│   │   ├── sa1.md         # Session audit for M1SA1
│   │   ├── sa2.md         # Session audit for M1SA2
│   │   └── session_001.md # Original session log
│   ├── M2/
│   │   └── sa1.md
│   └── TEMP/
│       ├── M1SA1.md       # TEMP milestone
│       ├── M2SA1.md
│       └── session_002.md
└── ingest/
    └── archive/
        ├── M1/            # Archived sessions
        └── TEMP/          # Archived TEMP milestones
```

## Ingestion Process

1. **Identify files for ingestion**:
   - Read SESSION_CHANGES.md
   - Identify modified files
   - Determine which need to be ingested (not cosmetic changes)

2. **Read files**:
   - Read modified SKILL.md files
   - Read modified documentation
   - Extract relevant content

3. **Create ingest entries**:
   - Create INGEST_ENTRIES.md
   - For each file: source path, target skill/prompt, metadata

4. **Archive originals**:
   - Move original files to /docs/ingest/archive/
   - Keep SA documents in milestones/ directory

5. **Notify user**:
   - List files archived
   - Request permission to ingest
   - Ask for context (what to use this for?)
```

### 4.2 Add manage-roadmap Integration

**Changes to manage-roadmap/SKILL.md**:
```markdown
# Ingestion Directory Integration

## Check for Ingestion Files

On skill invocation, check for `/docs/ingest/` directory:

1. **If directory exists**:
   ```bash
   ls docs/ingest/
   ```

2. **If files/folders found**:
   - Ask user for permission:
     ```
     User: I found files in /docs/ingest/ - should I process them?
     ```
   - Ask for context:
     ```
     User: What context should I provide for processing these files?
     ```

3. **If user approves**:
   - Read files in /docs/ingest/
   - Determine appropriate skill to handle each
   - Delegate to appropriate skill (milestone, sync-documentation, etc.)
   - After processing, move file to /docs/ingest/archive/

4. **If user rejects**:
   - Notify user of remaining files
   - User can process manually later

## Ingestion Patterns

### Session Logs
- Files: `session_*.md`, `session_*.txt`
- Use with: session-audit, milestone creation
- Archive to: `ingest/archive/{milestone}/`

### Draft Documentation
- Files: `draft_*.md`, `idea_*.md`
- Use with: sync-documentation, skill:implement-specification
- Archive to: `ingest/archive/{milestone}/`

### Research Notes
- Files: `research_*.md`, `notes_*.md`
- Use with: any skill that needs research data
- Archive to: `ingest/archive/{milestone}/`

### Training Data
- Files: `examples_*.md`, `prompts_*.md`
- Use with: skill:hotfix-issue, skill:implement-specification
- Archive to: `ingest/archive/{milestone}/`
```

### 4.3 Update session-audit to Generate Ingestion Entries

**Changes to session-audit/SKILL.md**:
```markdown
# Generate Ingestion Entries

## Identify Files for Ingestion

For each modified file:
1. Check if file is cosmetic (reformatting, whitespace)
   - Skip if cosmetic

2. Check if file is documentation
   - If yes, add to INGEST_ENTRIES.md

3. Check if file is template
   - If yes, add to INGEST_ENTRIES.md

4. Check if file is skill
   - If yes, add to INGEST_ENTRIES.md

## INGEST_ENTRIES.md Format

```markdown
# Ingestion Entries - Session Audit Report M2SA1

## Session Metadata
- Date: 2026-07-18
- Session ID: SA1
- Milestone: M2
- Files Modified: 3

## Files Identified for Ingestion

### 1. skills/session-audit/SKILL.md
- Source: skills/session-audit/SKILL.md
- Type: Skill implementation
- Purpose: Analyze session-based framework improvements
- Target: future skill development
- Archive to: docs/ingest/archive/M2/sa1_session_audit.md

### 2. skills/code-search/README.md
- Source: skills/code-search/README.md
- Type: Documentation
- Purpose: Code-search infrastructure documentation
- Target: skill:sync-documentation
- Archive to: docs/ingest/archive/M2/sa1_code_search_docs.md

### 3. AGENTS.md
- Source: AGENTS.md
- Type: Framework documentation
- Purpose: Update infrastructure skills section
- Target: skill:sync-documentation
- Archive to: docs/ingest/archive/M2/sa1_agents_update.md
```

## Phase 5: evolve-skills Processing of Multiple SAs (Day 2)

### 5.1 Enhance evolve-skills to Process Multiple SA Documents

**Changes to evolve-skills/SKILL.md**:
```markdown
# Process Multiple Session Audit Documents

## Detect and Process All SA Documents

1. **Find all SA documents**:
   ```bash
   find milestones/ -name "*SA*.md" | sort
   ```

2. **Process in chronological order**:
   - SA1.md → SA2.md → SA3.md
   - Accumulate recommended actions
   - Use context from previous SAs

3. **Prioritize last SA**:
   - Take all recommended actions from final SA
   - Use cumulative context from all SAs
   - Document all actions in EVOLUTION.md

## SA Document Dependencies

Each SA document should reference previous ones:

```markdown
# Session Audit Report M2SA2

## Previous Sessions
- [x] M2SA1 — First session (2026-07-18)
- [x] M2SA2 — Second session (2026-07-18)

## Recommended evolve-skills Actions (Cumulative)
1. [HIGH] evolve-skills — Add session-audit integration
2. [MEDIUM] session-audit — Document code-search usage patterns
3. [HIGH] evolve-skills — Update INDEX.md
4. [MEDIUM] evolve-skills — Update AGENTS.md
5. [LOW] session-audit — Improve classification heuristics
```

## TEMP Milestone Promotion

After processing all SA documents:
- Check if any TEMP milestones should be promoted
- If user approves:
  - Rename TEMP milestones to formal milestones
  - Move SA documents from TEMP to proper milestone structure
  - Update framework references
  - Document promotion in EVOLUTION.md
```

### 5.2 Update EVOLUTION.md Documentation

**Changes to evolve-skills/SKILL.md**:
```markdown
# Document SA Processing in EVOLUTION.md

## Format for SA Processing

```markdown
## 2026-07-18: Processing Session Audit Report M2SA1
- **Skill**: evolve-skills
- **Milestone**: M2 (SA1)
- **SA Document**: milestones/M2/SA1.md
- **Status**: Completed
- **Actions Applied**:
  - [x] Updated session-audit SKILL.md (version 1.0.0 → 1.0.1)
  - [x] Updated code-search SKILL.md (version 1.0.0 → 1.0.1)
  - [x] Updated AGENTS.md (Infrastructure Skills section)
- **Recommended Actions from SA**:
  - [HIGH] evolve-skills — Add code-search integration
  - [MEDIUM] session-audit — Document usage patterns
- **Dependencies**: None
- **Context**: See M2SA1.md for detailed analysis

## 2026-07-18: Processing Session Audit Report M2SA2
- **Skill**: evolve-skills
- **Milestone**: M2 (SA2)
- **SA Document**: milestones/M2/SA2.md
- **Status**: Completed
- **Actions Applied**:
  - [x] Updated session-audit SKILL.md (version 1.0.1 → 1.0.2)
  - [x] Enhanced code-search infrastructure
- **Recommended Actions from SA**:
  - [HIGH] evolve-skills — Implement TEMP milestone structure
  - [MEDIUM] session-audit — Generate INGEST_ENTRIES.md
- **Dependencies**: M2SA1.md
- **Context**: See M2SA2.md for detailed analysis
```

## Phase 6: Testing and Validation (Day 2)

### 6.1 Test session-audit with Multiple Sessions

**Test Cases**:
1. **Normal milestone with multiple sessions**:
   - Create SA1.md in milestones/M2/
   - Run session-audit again
   - Verify SA2.md is created
   - Check SA2 references SA1
   - Verify SA2 contains cumulative actions

2. **Session without milestone**:
   - Run session-audit without milestone
   - Verify TEMP milestone created
   - Verify M1SA1.md created in milestones/TEMP/
   - Verify temp marker in file

3. **Ingestion generation**:
   - Run session-audit with modified files
   - Verify INGEST_ENTRIES.md generated
   - Verify all relevant files listed

4. **Code-search integration**:
   - Run session-audit
   - Verify code-search used for:
     - Finding OMP AEF docs
     - Analyzing framework changes
     - Verifying infrastructure skills

### 6.2 Test evolve-skills with Multiple SAs

**Test Cases**:
1. **Process multiple SA documents**:
   - Have SA1.md and SA2.md
   - Run evolve-skills
   - Verify both SAs processed
   - Verify cumulative actions applied

2. **Process TEMP milestone**:
   - Have M1SA1.md in TEMP
   - Run evolve-skills
   - Verify TEMP processed like normal milestone
   - Verify temp marker in EVOLUTION.md

3. **Milestone promotion**:
   - Have M1SA1.md in TEMP
   - Run evolve-skills
   - Prompt user for promotion
   - Verify promotion if approved

### 6.3 Test manage-roadmap with Ingestion

**Test Cases**:
1. **Check for ingestion files**:
   - Create docs/ingest/M1/sa1.md
   - Run manage-roadmap
   - Verify prompt for permission
   - Verify prompt for context

2. **Process ingestion files**:
   - Approve ingestion
   - Delegate to appropriate skill
   - Verify file moved to archive
   - Verify processing completed

## Phase 7: Documentation Updates (Day 2)

### 7.1 Update session-audit SKILL.md

**Changes to session-audit/SKILL.md**:
```markdown
# Session Audit Skill

## Version
1.1.0

## Purpose
Analyze session-based framework improvements and generate comprehensive documentation for evolve-skills, including multiple session audits, TEMP milestones, ingestion entries, and comprehensive OMP AEF documentation updates.

## Output Format

### 1. M{X}SA{Y}.md
Session Audit Document
- Session metadata
- Files modified/created
- Classification
- Code-search analysis
- Recommended evolve-skills actions
- Dependencies

### 2. SESSION_CHANGES.md
Change log

### 3. CHANGELOG_ENTRIES.md
Changelog entries for OMP AEF docs

### 4. MILESTONE_UPDATES.md
Milestone updates

### 5. INGEST_ENTRIES.md
Ingestion entries

## TEMP Milestone Support

- Automatically detects sessions without milestones
- Creates TEMP milestone structure: milestones/TEMP/M{N}SA{Y}.md
- Supports reverse order: TEMP > Milestone

## Code-Search Integration

- Finds all OMP AEF documents
- Analyzes framework changes
- Verifies infrastructure skills
- Tracks progress toward milestones

## Ingestion Generation

- Identifies files for ingestion
- Creates INGEST_ENTRIES.md
- Ready for manage-roadmap processing
```

### 7.2 Update sync-documentation SKILL.md

**Changes to sync-documentation/SKILL.md**:
```markdown
# Sync Documentation Skill

## Version
1.1.0

## Purpose
Synchronize OMP AEF documentation with session-audit findings, including changelog, milestones, experiences, and roadmap updates.

## Integration with session-audit

When session-audit generates INGEST_ENTRIES.md:
1. Check for INGEST_ENTRIES.md flag
2. Read ingestion entries
3. Apply changes to OMP AEF docs
4. Notify user of completion

## Comprehensive Documentation Coverage

Updates all OMP AEF documents:
- docs/CHANGELOG.md
- docs/MILESTONES.md
- docs/EXPERIENCES.md
- docs/ROADMAP.md
- skills/*/SKILL.md
- ~/.omp/agent/INDEX.md
- ~/.omp/agent/AGENTS.md
```

### 7.3 Update manage-roadmap SKILL.md

**Changes to manage-roadmap/SKILL.md**:
```markdown
# Manage Roadmap Skill

## Version
1.1.0

## Purpose
Manage OMP AEF roadmap, including TEMP milestones, session audits, and ingestion files.

## Ingestion Directory Integration

Check /docs/ingest/:
1. Detect files/folders
2. Ask for permission
3. Ask for context
4. Delegate to appropriate skill
5. Archive after processing

## TEMP Milestone Promotion

Prompt user to promote TEMP milestones after processing.

## Milestone Management

- Create formal milestones from TEMP
- Update roadmap progress
- Track milestone completion
```

## Phase 8: Final Review (Day 2)

### 8.1 Review All Changes

**Checklist**:
- [x] session-audit generates M{X}SA{Y}.md
- [x] session-audit creates TEMP milestone structure
- [x] session-audit generates comprehensive changelog entries
- [x] session-audit generates milestone updates
- [x] session-audit generates ingestion entries
- [x] session-audit uses code-search for all analyses
- [x] evolve-skills processes multiple SA documents
- [x] evolve-skills handles TEMP milestones
- [x] evolve-skills promotes TEMP milestones
- [x] manage-roadmap checks /docs/ingest/
- [x] manage-roadmap asks for permission and context
- [x] manage-roadmap archives files after ingestion
- [x] All skills updated with version bumps
- [x] All documentation updated

### 8.2 Test End-to-End

**Test Scenario**:
1. User edits framework files in session
2. User invokes session-audit
3. session-audit generates:
   - M2SA1.md (normal milestone)
   - CHANGELOG_ENTRIES.md
   - MILESTONE_UPDATES.md
   - INGEST_ENTRIES.md
4. User invokes evolve-skills
5. evolve-skills processes M2SA1.md
6. User invokes manage-roadmap
7. manage-roadmap checks /docs/ingest/ and prompts
8. User approves ingestion
9. manage-roadmap processes files
10. Files archived to /docs/ingest/archive/
11. Documentation updated

## Summary of Deliverables

### Files Created
1. `milestones/M2/SA1.md` (NEW format, multiple sessions)
2. `milestones/M2/SESSION_CHANGES.md` (updated)
3. `milestones/M2/CHANGELOG_ENTRIES.md` (NEW)
4. `milestones/M2/MILESTONE_UPDATES.md` (NEW)
5. `milestones/M2/INGEST_ENTRIES.md` (NEW)

### Files Modified
1. `skills/session-audit/SKILL.md` (enhanced for multiple SAs, TEMP, ingestion)
2. `skills/sync-documentation/SKILL.md` (enhanced for comprehensive updates)
3. `skills/manage-roadmap/SKILL.md` (enhanced for ingestion)
4. `skills/evolve-skills/SKILL.md` (enhanced for multiple SAs, TEMP)

### New Directories
1. `docs/ingest/` (NEW)
2. `docs/ingest/archive/` (NEW)

### New subdirectories in docs/ingest/
1. `docs/ingest/M2/` (for milestone-specific ingestion)
2. `docs/ingest/TEMP/` (for TEMP-specific ingestion)

## Open Questions for User

1. **Ingestion priority**: Should session-audit generate ingestion entries for ALL modified files, or only those that are major changes?
2. **Archive cleanup**: After files are archived, should we keep them in /docs/ingest/archive/ indefinitely, or rotate them?
3. **TEMP milestone retention**: How long should TEMP milestones exist before requiring user action to promote?
4. **SA document consolidation**: Should evolve-skills consolidate multiple SA documents into a single EVOLUTION.md entry, or keep them separate?

## Recommended Implementation Sequence

**Day 1**:
- Phase 1: Core SA Document Format
- Phase 2: Comprehensive Documentation Updates
- Phase 3: TEMP > Milestone Reverse Order

**Day 2**:
- Phase 4: /docs/ingest/ Folder
- Phase 5: evolve-skills Processing of Multiple SAs
- Phase 6: Testing and Validation
- Phase 7: Documentation Updates
- Phase 8: Final Review

## Expected Outcomes

1. ✅ Multiple session audits per milestone (SA1, SA2, SA3...)
2. ✅ TEMP milestone structure for sessions without milestones
3. ✅ Comprehensive documentation updates (all OMP AEF docs)
4. ✅ Reverse order flow (TEMP > Milestone)
5. ✅ /docs/ingest/ folder for data ingestion
6. ✅ manage-roadmap integration with permission + context
7. ✅ Automatic archiving after ingestion
8. ✅ Better tracking of semi-agentic development
