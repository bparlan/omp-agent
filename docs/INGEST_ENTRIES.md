# Ingestion Entries

This document explains which skills generate which artifacts and where they are located.

## Artifact Generation by Skill

### Session Audit (session-audit)

**Location**: `milestones/M{X}/` or `milestones/TEMP/`

**Artifacts Generated**:
- `M{X}SA{Y}.md` — Session Audit Document (main artifact)
- `SESSION_CHANGES.md` — Session change log
- `CHANGELOG_ENTRIES.md` — Changelog entries
- `MILESTONE_UPDATES.md` — Milestone updates
- `INGEST_ENTRIES.md` — Ingestion entries

**Purpose**: 
- Document session changes and artifacts generated
- Track what was modified, created, or updated
- Prepare files for ingestion into main documentation

### Evolve Skills (evolve-skills)

**Location**: Updates existing SKILL.md files in `skills/` directory

**Artifacts Generated**:
- Updated `skills/*_SKILL.md` files
- `SESSION_CHANGES.md` (via session-audit)
- `CHANGELOG_ENTRIES.md` (via session-audit)
- `MILESTONE_UPDATES.md` (via session-audit)
- `INGEST_ENTRIES.md` (via session-audit)

**Purpose**:
- Read session artifacts from milestones/
- Analyze changes
- Update SKILL.md files
- Propose improvements to framework

### Sync Documentation (sync-documentation)

**Location**: Reads from `milestones/` or `milestones/TEMP/`, processes artifacts

**Artifacts Processed**:
- `SESSION_CHANGES.md` — Updates skills documentation
- `CHANGELOG_ENTRIES.md` — Updates CHANGELOG.md
- `MILESTONE_UPDATES.md` — Updates MILESTONES.md
- `INGEST_ENTRIES.md` — Processes files for `/docs/ingest/`

**Purpose**:
- Integrate session artifacts into canonical documentation
- Update CHANGELOG.md
- Update MILESTONES.md
- Move processed files to `/docs/ingest/` for archival

### Manage Roadmap (manage-roadmap)

**Location**: Uses `/docs/ingest/` for archival

**Artifacts Processed**:
- Reads from `docs/ingest/` (files moved by sync-documentation)
- Updates main documentation
- Archives milestones

**Purpose**:
- Coordinate documentation flow
- Handle user permission for ingestion
- Update canonical documentation
- Archive processed files

## Workflow

```
Session runs (milestone work)
        ↓
session-audit generates artifacts in milestones/M{X}/
        ↓
evolve-skills reads session artifacts, updates skills
        ↓
sync-documentation reads session artifacts, updates docs
        ↓
sync-documentation moves files to docs/ingest/M{X}/
        ↓
manage-roadmap processes docs/ingest/, updates docs
        ↓
manage-roadmap archives processed files
```

## File Locations

### Session Artifacts
- **Primary**: `milestones/M{X}/` (for active milestones) or `milestones/TEMP/` (for TEMP sessions)
- **Content**: All session-generated artifacts

### Ingestion/Archival
- **Processing**: `docs/ingest/M{X}/` (organized by milestone)
- **Archived**: `docs/ingest/archived/` (after processing)

### Canonical Documentation
- **Framework Docs**: `docs/` (AGENTS.md, INDEX.md, FRAMEWORK.md, etc.)
- **Roadmap**: `docs/ROADMAP.md`
- **Milestones**: `docs/MILESTONES.md`

### Skills
- **Skill Definitions**: `skills/*_SKILL.md`

## Template Files

Templates are located in `templates/` directory:

- `session_changes_template.md` — For SESSION_CHANGES.md
- `changelog_entries_template.md` — For CHANGELOG_ENTRIES.md
- `milestone_updates_template.md` — For MILESTONE_UPDATES.md
- `ingest_entries_template.md` — For INGEST_ENTRIES.md

Skills can read these templates and generate artifacts based on session data.

## Naming Conventions

### Session Artifacts
- **Main SA Document**: `M{X}SA{Y}.md` (e.g., M2SA1.md for Milestone 2, Session 1)
- **Short Names**: SESSION_CHANGES.md, CHANGELOG_ENTRIES.md, MILESTONE_UPDATES.md, INGEST_ENTRIES.md

### Convention Rationale
- Main SA document has `M{X}SA{Y}.md` prefix for easy identification
- Supporting documents use short, descriptive names
- No `M{X}SA{Y}` prefix for short names to avoid redundancy
- Location-specific: All artifacts in milestone folder, not in `/docs/ingest/`

---

**Last Updated**: 2026-07-18
