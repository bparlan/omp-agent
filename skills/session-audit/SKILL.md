---
name: session-audit
version: 1.3.0
description: >
  Capture any session (milestone, hotfix, manual edits, external reports) into
  Session Audit Reports (M{X}SA{Y}.md) that drive documentation updates,
  skill evolution, and quality monitoring. Use when the user says
  "session-audit", "document this session", "capture this session".
tools: code-search, read, ask, write, edit, askuserquestion, bash
user-invocable: true
---

# Session Audit Skill

## Version
1.3.0
## Purpose
Capture any session (milestone, hotfix, manual edits, external reports) into
Session Audit Reports (M{X}SA{Y}.md) that drive documentation updates, skill
evolution, and quality monitoring.

## Session Types Detected

### 1. Milestone Session
**Trigger**: User mentions milestone (M1, M2, etc.) or milestone > development

**Captures**:
- Milestone progression
- Review/Investigation/Completion reports
- Framework changes within milestone scope

### 2. Hotfix Session
**Trigger**: User mentions hotfix, hotfix-focus, bug fix, or issue resolution

**Captures**:
- Issue description
- Steps taken to fix
- Files changed
- Lessons learned

### 3. Manual Edit Session
**Trigger**: No specific command, but files were modified

**Captures**:
- Files modified (git diff)
- Change description (from git log or user clarification)
- Session context

### 4. External Report Session
**Trigger**: User imports or references an external document

**Captures**:
- External report source (PR merge, external issue, etc.)
- Summary of changes
- Impact on framework

### 5. Ad-Hoc Session
**Trigger**: No milestone, hotfix, or manual edits detected

**Captures**:
- Session duration
- Context summary (from conversation)
- Any small improvements

## External Report Detection

Auto-detect external report patterns and ask user for clarification:

1. Check for external file references (PR files, external issue docs, etc.)
2. If detected, show summary and ask:
   - "Detected external report pattern in [file]. Summary: [summary]. Is this a new Session Audit (create M{X}SA{Y}.md)?"
3. If user confirms → create Session Audit
4. If user declines → don't create Session Audit (this is a separate document)

**Note**: Do NOT auto-create Session Audit from external reports. Wait for user to explicitly call `session-audit`.

## Automatic Workflow After Session Audit

After generating M{X}SA{Y}.md, automatically trigger:

1. **sync-documentation** (shows doc changes, no approval needed)
2. **evolve-skills** (shows skill changes, requires per-skill approval)
3. **skills-auditor audit** (read-only health check)

Each step shows changes clearly before applying.

## Safety

- Only evolve-skills changes require user approval
- sync-documentation and skills-auditor are safe and automatic
- All changes shown with diffs before applying
- External reports require explicit user confirmation
---
