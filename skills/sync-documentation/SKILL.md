---
name: sync-documentation
version: 1.2.0
description: Maintain long-lived project documentation by distilling completed engineering work into canonical project documents, including /docs/ingest/ file processing with permission + context workflow.
tools: read, write, edit, bash, glob, grep
user-invocable: true
---

# Documentation Sync: Distill Engineering Work to Canonical Documents

## Auto-Run After Session Audit

After session-audit completes, sync-documentation automatically runs (shows changes, asks for approval).

**What it does**:
1. Reads M{X}SA{Y}.md (Session Audit Report)
2. Identifies documentation changes (skills.md, PLAYBOOK.md, FRAMEWORK.md, EXPERIENCES.md, INDEX.md)
3. Shows diffs for each file changed
4. Asks user: "Apply these changes?" (yes/no)

**Safety**:
- Shows diffs before applying (what WILL change)
- Only applies changes if user says "yes"
- Documentation updates are non-destructive (not behavior-changing)

**Example Output**:
```
sync-documentation: Reading M2SA3.md...
  - Detected 3 documentation changes

sync-documentation: Proposed changes:

  docs/skills.md:
  - Line 15: Added "hotfix-issue" to skills catalog
  - Line 42: Added "session-audit" to framework skills

  docs/PLAYBOOK.md:
  - Line 120: Added "Every Session Workflow" section

sync-documentation: Apply these changes?
  [1] Yes, apply all changes
  [2] No, skip
  [3] No, but apply skills.md only
  [4] Custom selection

Selection: 1
```

## Workflow After session-audit

This skill auto-runs after session-audit completes. It:

1. Reads M{X}SA{Y}.md (Session Audit Report)
2. Identifies documentation changes
3. Shows diffs for each file changed
4. Asks user: "Apply these changes?" (yes/no)
5. Applies changes if user approves

**Example Output**:
```
sync-documentation: Reading M2SA3.md...
  - Detected 3 documentation changes

sync-documentation: Proposed changes:

  docs/skills.md:
  - Line 15: Added "hotfix-issue" to skills catalog
  - Line 42: Added "session-audit" to framework skills

  docs/PLAYBOOK.md:
  - Line 120: Added "Every Session Workflow" section

sync-documentation: Apply these changes?
  [1] Yes, apply all changes
  [2] No, skip
  [3] No, but apply skills.md only
  [4] Custom selection

Selection: 1
```
