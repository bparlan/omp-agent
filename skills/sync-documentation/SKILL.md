---
name: sync-documentation
version: 1.2.1
description: Maintain long-lived project documentation by distilling completed engineering work into canonical project documents, including /docs/ingest/ file processing with permission + context workflow.
tools: read, write, edit, bash, glob, grep
user-invocable: true
---

# Documentation Sync: Distill Engineering Work to Canonical Documents

## Auto-Run After Session Audit

After session-audit completes, sync-documentation automatically runs (shows changes, asks for approval).

1. Reads M{X}SA{Y}.md (Session Audit Report)
15:2. **Dynamic Internal Path Resolution**: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
16:  1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
17:  2. Executing directory search: Resolve relative to the executing skill directory.
18:  3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/sync-documentation/CONTRACTS/` (or similar skill-specific path).
19:  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
20:2. Identifies documentation changes (skills.md, PLAYBOOK.md, FRAMEWORK.md, EXPERIENCES.md, INDEX.md)
21:3. Shows diffs for each file changed
22:4. Asks user: "Apply these changes?" (yes/no)

    5.1. **Workspace Awareness**: Distinguish between AEF framework documentation and project documentation.
25:    5.2. **Project Convention Adherence**: Respect project conventions and architecture, especially for application projects.
- Shows diffs before applying (what WILL change)
27:- Shows diffs before applying (what WILL change)
- Only applies changes if user says "yes"
28:- Only applies changes if user says "yes"
- Documentation updates are non-destructive (not behavior-changing)
29:
**Example Output**:
30:```
**Example Output**:
```
sync-documentation: Reading M2SA3.md...
  - Detected 3 documentation changes

sync-documentation: Proposed changes:

  docs/skills.md:
  - Line 15: Added "hotfix-issue" to skills catalog
  - Line 42: Added "session-audit" to framework skills
  docs/PLAYBOOK.md:
41:  docs/PLAYBOOK.md:
  - Line 120: Added "Every Session Workflow" section
42:
sync-documentation: Apply these changes?
43:
sync-documentation: Apply these changes?
  [1] Yes, apply all changes
46:  [1] Yes, apply all changes
  [2] No, skip
47:  [2] No, skip
  [3] No, but apply skills.md only
48:  [3] No, but apply skills.md only
  [4] Custom selection
49:  [4] Custom selection
Selection: 1
50:Selection: 1
```
51:```
sync-documentation: Reading M2SA3.md...
  - Detected 3 documentation changes.
  - Identified changes impacting workspace boundary and canonical resolution.
  - Proposed changes:
    - docs/skills.md:
      - Line 15: Added "hotfix-issue" to skills catalog
      - Line 42: Added "session-audit" to framework skills
    - docs/PLAYBOOK.md:
      - Line 120: Added "Every Session Workflow" section
    - Reconciled artifact references using canonical resolution.
sync-documentation: Apply these changes?
  [1] Yes, apply all changes
  [2] No, skip
  [3] No, but apply skills.md only
  [4] Custom selection
Selection: 1
```

## Workflow After session-audit
74:## Workflow After session-audit

This skill auto-runs after session-audit completes. It:
75:
1. Reads M{X}SA{Y}.md (Session Audit Report)
76:2. Identifies documentation changes
77:3. Shows diffs for each file changed
78:4. Asks user: "Apply these changes?" (yes/no)
79:5. Applies changes if user approves
80:
## Out of Scope (Negative Guardrails)

**Strict Milestone and Project Agnosticism:**
- All instructions, prompt examples, schemas, and file path descriptions must be written in strictly agnostic terms.
- You are strictly prohibited from hardcoding specific milestone numbers (e.g., 'M10') or sequence IDs (e.g., 'M10S4') inside the prompt instructions.
- You must utilize the standard wildcard notation: `M{X}` for milestones, `S{Y}` for specifications, `T{Z}` for test plans, and `M{X}S{Y}` for active sequence identifiers. This ensures the AEF remains 100% portable and reusable across brownfield and greenfield projects.

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
