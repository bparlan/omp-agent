---
structure-type: Session-Audit Integration Guide
created-date: 2026-07-18
version: 1.0.0
purpose: Document-driven development workflow using session-audit
---

# Documentation-Driven Development with Session-Audit

## Overview

This guide explains how to use the session-audit workflow to create a well-integrated, template-driven method for session-focused development that supports documentation-driven development (DDD) principles.

## Core Concept

**Session-Audit as DDD Framework**:
Session-audit provides the structure, templates, and integration points needed to make every session result in comprehensive documentation automatically. This enables:

1. **Automatic Documentation Generation**: Every session produces 5 standardized output formats
2. **Audit Trail**: Complete history of all changes and decisions
3. **Well-Integrated Workflow**: Seamless integration with existing skills
4. **Documentation-Driven Evolution**: Changes are always documented before being applied

---

## Template-Driven Architecture

### Session-Audit Skill Structure

The session-audit skill provides a template-driven workflow:

```
Session Work → Session-Audit → 5 Output Formats → /docs/ingest/ → evolve-skills → SKILL.md Updates
```

### 5 Output Formats (Templates)

Each SA document generates 5 standardized output formats:

#### 1. M{X}SA{Y}.md — Primary Session Audit Document
- **Template Location**: skills/session-audit/templates/SA_document_template.md
- **Required Sections**:
  - Frontmatter (metadata)
  - Overview
  - Files Modified/Created
  - Classification (major/minor)
  - Code-Search Analysis
  - Dependencies
  - Recommended Actions
  - Progress Tracking
  - Status

#### 2. SESSION_CHANGES.md — Change Log
- **Template Location**: skills/session-audit/templates/SESSION_CHANGES_template.md
- **Required Sections**:
  - Session header (date, type)
  - Major Changes list
  - Skills Updated
  - Documentation Created
  - Framework Integration
  - Tools Updated
  - Session Deliverables
  - Key Benefits
  - Next Steps

#### 3. CHANGELOG_ENTRIES.md — Changelog
- **Template Location**: skills/session-audit/templates/CHANGELOG_template.md
- **Required Sections**:
  - "Added" section (new skills, features, docs)
  - "Changed" section (version updates, modifications)
  - "Fixed" section (bugs, issues, missing features)

#### 4. MILESTONE_UPDATES.md — Milestone Updates
- **Template Location**: skills/session-audit/templates/MILESTONE_UPDATES_template.md
- **Required Sections**:
  - Session Metadata
  - Progress Tracking
  - File Counts
  - Version Updates
  - Activity Summary
  - Dependencies
  - Recommended Actions
  - Progress Indicators

#### 5. INGEST_ENTRIES.md — Ingestion Entries
- **Template Location**: skills/session-audit/templates/INGEST_ENTRIES_template.md
- **Required Sections**:
  - Ingestion Metadata
  - Files Identified (status, action, context, delegated-to)
  - Output Documents
  - Directory Structure Created
  - Ingestion Workflow (8 steps)
  - Processing Schedule
  - File Sizes
  - Handoff to manage-roadmap

---

## Integration with Existing Skills

### Skill Ecosystem

```
session-audit (generates templates)
    ↓
INGEST_ENTRIES.md (template-based file list)
    ↓
manage-roadmap (permission + context workflow)
    ↓
docs/ingest/ (write files)
    ↓
Delegated Skills (sync-documentation, evolve-skills)
    ↓
Archived files + EVOLUTION.md (track what was processed)
```

### Skill Integration Points

#### 1. session-audit
- **Role**: Generates 5 output formats using templates
- **Tools**: read, write, edit
- **Dependencies**: code-search, evolve-skills (for recommendations)
- **Outputs**: M{X}SA{Y}.md, SESSION_CHANGES.md, CHANGELOG_ENTRIES.md, MILESTONE_UPDATES.md, INGEST_ENTRIES.md

#### 2. manage-roadmap
- **Role**: Checks INGEST_ENTRIES.md, processes with permission + context
- **Tools**: read, write, edit, ask
- **Dependencies**: All skills (for delegation)
- **Outputs**: Processed files in /docs/ingest/, archived files, updated INGEST_ENTRIES.md

#### 3. evolve-skills
- **Role**: Reads SA documents, processes recommendations, updates SKILL.md files
- **Tools**: read, edit, lsp
- **Dependencies**: session-audit (for recommendations), code-search (for analysis)
- **Outputs**: Updated SKILL.md files, EVOLUTION.md documentation

#### 4. sync-documentation
- **Role**: Updates /docs/ingest/ files with new content
- **Tools**: read, edit, write, lsp
- **Dependencies**: session-audit (for files to update), manage-roadmap (for delegation)
- **Outputs**: Updated documentation files in /docs/ingest/

#### 5. code-search
- **Role**: Provides semantic analysis for session-audit
- **Tools**: search_code, ast_grep
- **Dependencies**: session-audit (for queries), evolve-skills (for results)
- **Outputs**: Analysis results for SA documents

---

## Document-Driven Development Workflow

### Phase 1: Session Work
```
User completes session work on framework
```

### Phase 2: Session-Audit Generation
```
session-audit skill is invoked
    ↓
Detects changes (git or filesystem timestamps)
    ↓
Classifies changes (major vs minor)
    ↓
Generates 5 output formats using templates
    ↓
Creates INGEST_ENTRIES.md with file list
```

### Phase 3: Ingestion Workflow
```
manage-roadmap skill checks for INGEST_ENTRIES.md
    ↓
Presents files to user with suggested actions
    ↓
User approves processing
    ↓
User selects context (which skill to use, what changes needed)
    ↓
manage-roadmap writes files to /docs/ingest/{milestone}/
    ↓
manage-roadmap delegates to appropriate skills
    ↓
manage-roadmap archives original files
    ↓
manage-roadmap updates INGEST_ENTRIES.md
```

### Phase 4: Evolution
```
evolve-skills reads SA documents
    ↓
Processes recommendations (ordered by priority)
    ↓
Applies changes to SKILL.md files
    ↓
Bumps version numbers
    ↓
Documents in EVOLUTION.md
    ↓
User verifies changes
```

### Phase 5: Review and Continue
```
User reviews changes in EVOLUTION.md
    ↓
User approves changes
    ↓
Proceed to next session or complete milestone
```

---

## Benefits of Template-Driven DDD

### 1. Consistency
- All SA documents follow same structure
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
- TEMP milestone support for sessions without formal milestones

---

## Template Structure Details

### SA Document Template (M{X}SA{Y}.md)

**Frontmatter**:
```yaml
---
session-id: SA1
milestone: M2
session-type: Framework improvement
duration: 2 hours
date: 2026-07-18
class: major
priority: HIGH
---
```

**Required Sections**:
- Session Metadata
- Overview
- Files Modified/Created
- Classification
- Code-Search Analysis
- Dependencies
- Recommended evolve-skills Actions
- Progress Tracking
- Status

### SESSION_CHANGES.md Template

**Structure**:
- Session header (date, type)
- Major Changes list
- Skills Updated
- Infrastructure Documentation
- Framework Integration
- Tools Updated
- Session Deliverables
- Key Benefits
- Next Steps

### CHANGELOG_ENTRIES.md Template

**Structure**:
- "Added" section (new skills, features, docs)
- "Changed" section (version updates, modifications)
- "Fixed" section (bugs, issues, missing features)

### MILESTONE_UPDATES.md Template

**Structure**:
- Session Metadata
- Progress Tracking
- File Counts
- Version Updates
- Activity Summary
- Dependencies
- Recommended Actions
- Progress Indicators

### INGEST_ENTRIES.md Template

**Structure**:
- Ingestion Metadata
- Files Identified (status, action, context, delegated-to)
- Output Documents
- Directory Structure Created
- Ingestion Workflow (8 steps)
- Processing Schedule
- File Sizes
- Handoff to manage-roadmap

---

## Integration Examples

### Example 1: Framework Improvement Session

**Session Work**:
User adds new skill `doc-validator` to framework

**Session-Audit Generation**:
- Detects: skills/doc-validator/SKILL.md (NEW)
- Classifies: Major (new skill)
- Generates: 5 output formats

**Ingestion Workflow**:
- manage-roadmap presents: skills/doc-validator/SKILL.md
- Action: sync-documentation — Add doc-validator to INDEX.md
- Context: "Add new skill to INDEX.md skills list"

**Evolution**:
- evolve-skills reads M2SA2.md
- Processes recommendation: Add doc-validator to INDEX.md
- Updates INDEX.md
- Documents in EVOLUTION.md

### Example 2: Bug Fix Session

**Session Work**:
User fixes bug in `session-audit` skill

**Session-Audit Generation**:
- Detects: skills/session-audit/SKILL.md (MODIFIED)
- Classifies: Minor (bug fix)
- Generates: 5 output formats

**Ingestion Workflow**:
- manage-roadmap presents: skills/session-audit/SKILL.md
- Action: evolve-skills — Fix bug
- Context: "Fix bug in session-audit SKILL.md line 42"

**Evolution**:
- evolve-skills reads M2SA3.md
- Processes recommendation: Fix bug
- Updates session-audit SKILL.md
- Bumps version: 1.1.0 → 1.1.1
- Documents in EVOLUTION.md

---

## Usage Guidelines

### When to Use Session-Audit

✅ **Use session-audit when**:
- Working on framework improvements
- Making significant changes to skills
- Modifying templates or core structure
- Working on OMP AEF documentation
- Working on multiple files in one session

❌ **Don't use session-audit when**:
- Doing quick fixes or small changes
- Making cosmetic changes only
- Working on non-framework code
- Temporary exploration sessions

### Best Practices

1. **Run session-audit at end of every session**
   - Generates complete documentation
   - No need to remember to do it later

2. **Use proper session types**
   - Framework improvement
   - Bug fix
   - Feature addition
   - Documentation update
   - Refactoring

3. **Classify changes correctly**
   - Major: New skills, significant structure changes
   - Minor: Bug fixes, small improvements

4. **Use TEMP milestone for exploration**
   - Sessions without formal milestone
   - Can be promoted to formal milestone later

5. **Process INGEST_ENTRIES.md regularly**
   - Use manage-roadmap
   - Approve with permission + context
   - Archive original files

---

## Future Enhancements

### Potential Improvements

1. **SA Consolidation Logic**
   - Merge similar recommendations across SAs
   - Identify duplicate actions
   - Group related changes

2. **SA as Milestone Format**
   - Convert SA documents to milestone format
   - Use SAs as milestone completion criteria
   - Link SAs to specific milestone objectives

3. **Advanced TEMP Handling**
   - Auto-promote TEMP when criteria met
   - Auto-close TEMP after completion
   - Alert user when TEMP needs attention

4. **Integration with Test Suite**
   - Run tests after SA recommendations
   - Verify changes work correctly
   - Document test results in SA documents

5. **Documentation-Driven Testing**
   - Generate test cases from SA recommendations
   - Link tests to specific changes
   - Maintain test documentation in SA format

---

## Conclusion

Session-audit provides a template-driven, well-integrated method for session-focused development that supports documentation-driven development principles. By generating 5 standardized output formats, integrating seamlessly with existing skills, and maintaining a complete audit trail, session-audit ensures that every session results in comprehensive, traceable documentation.

This structure enables:
- **Consistent**: All sessions follow same pattern
- **Automated**: Documentation generated automatically
- **Traceable**: Complete history of all changes
- **Integrated**: Seamless with existing skills
- **Scalable**: Supports multiple sessions, milestones, and TEMP structures

The session-audit workflow is ready for production use and can be applied to any session-based development workflow.

---

**Document Type**: Integration Guide
**Version**: 1.0.0
**Created**: 2026-07-18
**Status**: Complete
