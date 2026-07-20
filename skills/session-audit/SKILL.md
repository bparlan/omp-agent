---
name: session-audit
version: 1.1.0
description: Analyze session-based framework improvements and generate comprehensive documentation for evolve-skills
tools: code-search, read, ask, write, edit
user-invocable: true
---

# Session Audit Skill

## Version
1.1.0

## Purpose
Analyze session-based framework improvements and generate comprehensive documentation for evolve-skills, including multiple session audits (SA1, SA2, SA3...), TEMP milestone structure, comprehensive OMP AEF documentation updates, and ingestion entries.

## Output Format

### Files Generated

1. **`SESS_{SESSION_ID}_AUDIT.md`** — Session Audit Document
   - Session metadata (date, session-id, milestone)
   - Files modified/created
   - Classification (major/minor)
   - Code-search analysis results
   - Recommended evolve-skills actions
   - Dependencies on previous SA documents
   - Progress toward milestone completion (if milestone exists)

2. **`SESS_{SESSION_ID}_CHANGES.md`** — Change log
   - List of modified files
   - Brief description of changes
   - References to SA documents

## File Locations and Routing

- **Active Milestones**: SA documents and change logs MUST go to `milestones/M{X}/`.
  - `M{X}SA{Y}.md` (Session Audit Document)
  - `SESSION_CHANGES.md` (Change log)

- **Exploratory Sessions (No Active Milestone)**:
  - SA documents and change logs MUST be saved directly to the current session's folder: `~/devcode/aef/agent/sessions/{SESSION_ID}/`.
  - Audit file name: `SESS_{SESSION_ID}_AUDIT.md` (using `session_audit_template.md`)
  - Change log file name: `SESS_{SESSION_ID}_CHANGES.md`

## Numbering Strategy

- SA documents for active milestones are numbered sequentially per milestone: SA1, SA2, SA3...
- Exploratory sessions are identified by `SESSION_ID`, not sequential numbering.

## TEMP Milestone Auto-Suggestion

After evolve-skills processes TEMP milestone:
- Check if TEMP milestone should be closed
- Auto-suggest to user: "Should I close M{N}SA1 as a completed session?"
- If user approves:
  - Delete TEMP milestone
  - Move SA document to proper milestone if milestone created later

## Code-Search Integration

Use code-search for multiple purposes:

1. **Find OMP AEF documents**:
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

5. **Check for code-search usage in skills**:
   - Search for "search_code" in skills
   - Verify code-search is used appropriately
   - Identify skills that should use code-search

## Session Audit Process

### Step 1: Scan Session Changes

1. Detect modified files using git or filesystem timestamps
2. Identify framework-critical locations:
   - Root docs (INDEX.md, ~/devcode/aef/AGENTS.md, ~/devcode/aef/agent/AGENTS.md, README.md, FRAMEWORK.md, PLAYBOOK.md)
   - Skills (skills/*/SKILL.md)
   - Templates (templates/*.md)
   - Configuration (skills-lock.json, config.yml)
3. Exclude cosmetic changes (reformatting, whitespace, minor wording)

### Step 2: Classify Changes

- **Track**: INDEX.md, AGENTS.md, README.md, FRAMEWORK.md, PLAYBOOK.md, skills-lock.json, config.yml, skill SKILL.md files with major changes, template schema changes
- **Do NOT Track**: Cosmetic changes, reformatting, comment updates, tool list additions

### Step 3: Generate SA Document

Create M{X}SA{Y}.md with:
- Session metadata
- Files modified/created
- Classification results
- Code-search analysis
- Recommended evolve-skills actions
- Dependencies on previous SAs

### Step 4: Generate Change Log

Create SESSION_CHANGES.md with:
- List of modified files
- Brief descriptions
- References to SA documents

### Step 5: Generate Changelog Entries

Create CHANGELOG_ENTRIES.md with:
- Sections: "Added", "Changed", "Fixed"
- Each entry in standard format

### Step 6: Generate Milestone Updates

Create MILESTONE_UPDATES.md with:
- Progress percentages
- Status updates
- Completion markers

### Step 7: Generate Ingestion Entries

Create INGEST_ENTRIES.md with:
- All modified files listed
- Ingestion metadata
- Ready for manage-roadmap processing

## Dependencies

- **code-search**: Provides semantic search and skeleton generation
- **evolve-skills**: Receives recommended actions from SA documents
- **manage-roadmap**: Processes ingestion entries

## Example SA Document

```markdown
# Session Audit Report M2SA1

## Session Metadata
- **Date**: 2026-07-18
- **Session ID**: SA1
- **Milestone**: M2
- **Session Type**: Framework improvement
- **Duration**: 2 hours

## Files Modified
1. skills/session-audit/SKILL.md
2. skills/code-search/README.md
3. AGENTS.md

## Classification
- **Major Changes**: 2
  1. session-audit skill (NEW)
  2. code-search documentation (NEW)
- **Minor Changes**: 1
  1. AGENTS.md infrastructure section (UPDATED)

## Code-Search Analysis

### Framework Changes Detected
- [x] Agent handoff patterns identified
- [x] Template usage verified
- [x] Negative guardrails checked
- [x] Code-search integration verified

### Infrastructure Skills Usage
- [x] session-audit uses code-search for analysis
- [x] evolve-skills can use code-search for pattern matching
- [x] Pending: sync-documentation integration

### Milestone Progress
- M2 completion: 85%
- Current phase: Testing
- Remaining tasks: 3

## Recommended evolve-skills Actions
1. [HIGH] session-audit — Update version to 1.1.0
2. [HIGH] evolve-skills — Add code-search integration
3. [MEDIUM] sync-documentation — Update AGENTS.md section
4. [LOW] session-audit — Improve classification heuristics

## Dependencies
- M2SA1 (this document)
- None

## Status
- [x] Analysis complete
- [x] SA document generated
- [x] Recommendations provided
- [x] Awaiting evolve-skills processing
```

## Usage Examples

### Normal Milestone with Multiple Sessions

```bash
# Session 1
invoke session-audit
# Generates: milestones/M2/SA1.md

# Session 2
invoke session-audit
# Generates: milestones/M2/SA2.md
# SA2.md references SA1.md
```

### Session Without Milestone

```bash
# Run session-audit without milestone
invoke session-audit
# Generates: milestones/TEMP/M1SA1.md
# Marked as TEMP milestone
```

## Integration with Other Skills

### evolve-skills Integration

evolve-skills will:
1. Read M{X}SA{Y}.md files
2. Process recommendations in order
3. Apply improvements to SKILL.md files
4. Bump version numbers
5. Document in EVOLUTION.md

### manage-roadmap Integration

manage-roadmap will:
1. Check for INGEST_ENTRIES.md flag
2. Ask user for permission
3. Ask user for context (what skill/prompt to use)
4. Delegate to appropriate skill
5. Archive original file after processing

## Limitations

- Cannot track cosmetic changes (reformatting, whitespace)
- Requires manual intervention for permission and context
- Assumes session tracking via git timestamps or explicit markers
- Temporal tracking relies on file modification times
- Progress calculations depend on milestone file existence
- TEMP milestones require manual cleanup or promotion

## Future Enhancements

- [ ] Auto-detect session boundaries
- [ ] Support for non-SDD workflows
- [ ] Integration with project management tools


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
