---
name: session-audit
version: 1.3.2
description:
  Capture any session (milestone, hotfix, manual edits, external reports) into
  Session Audit Reports (M{X}SA{Y}.md) that drive documentation updates,
  skill evolution, and quality monitoring. Use when the user says
  "session-audit", "document this session", "capture this session".
tools: code-search, read, ask, write, edit, askuserquestion, bash
user-invocable: true
---

# Session Audit Skill

      Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.

### 1. Milestone Session

**Trigger**: User mentions milestone (M1, M2, etc.) or milestone > development
         - [Date] **Topic:** {topic} | **Issue:** {issue} | **Suggested Fix:** {fix}
         - Analyze the relevant `SKILL.md` file
         - Apply prompt fixes or new Out of Scope guardrails

## Out of Scope (Negative Guardrails)

**Strict Milestone and Project Agnosticism:**

- All instructions, prompt examples, schemas, and file path descriptions must be written in strictly agnostic terms.
- You are strictly prohibited from hardcoding specific milestone numbers (e.g., 'M10') or sequence IDs (e.g., 'M10S4') inside the prompt instructions.
- You must utilize the standard wildcard notation: `M{X}` for milestones, `S{Y}` for specifications, `T{Z}` for test plans, and `M{X}S{Y}` for active sequence identifiers. This ensures the AEF remains 100% portable and reusable across brownfield and greenfield projects.

- Bump the skill version
- Move the item to 'Applied Skill Updates' in `EXPERIENCES.md` documenting what you changed

11. **Session Audit Integration — Multiple SAs and TEMP Milestones**

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

   - "Detected external report pattern in [file]. Summary: [summary]. Is this a new Session Audit (create M{X}SA{Y}.md)?"

**Note**: Do NOT auto-create Session Audit from external reports. Wait for user to explicitly call `session-audit`.

## Automatic Workflow After Session Audit

After generating M{X}SA{Y}.md, automatically trigger:


Each step shows changes clearly before applying.

## Safety

- Only evolve-skills changes require user approval
- sync-documentation and skills-auditor are safe and automatic
- All changes shown with diffs before applying
- External reports require explicit user confirmation
