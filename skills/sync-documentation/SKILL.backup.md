---
name: sync-documentation
version: 1.3.1
description: Maintain long-lived project documentation by distilling completed engineering work into canonical project documents, including /docs/ingest/ file processing with permission + context workflow.
tools: read, write, edit, bash, glob, grep
user-invocable: true
---

# Documentation Sync: Distill Engineering Work to Canonical Documents

### 1. Ingestion of All Artifacts
The skill MUST scan and parse all files in the active `milestones/M{X}/` folder (including specs, verifications, test plan ledgers, completions, evaluations, reviews, and closures) before updating any canonical documents.

### 2. Surgical Reconcile Duty
Compare completed codebase realities against `SPEC.md`, `DATA.md`, `PLAYBOOK.md`, and `CHANGELOG.md` to surgically update public class signatures, SQL schemas, and changelog entries.

### 3. Post-Ingestion Diagram Check (MANDATORY)
Immediately after successfully ingesting and syncing project files, execute the 'diagrammer' command to rebuild the visual index. Diffs of modified diagrams (docs/diagrams/*.mmd) must be presented to the user alongside standard markdown diffs for approval.

## Auto-Run After Session Audit

After session-audit completes, sync-documentation automatically runs (shows changes, asks for approval).

1. Identifies documentation changes (skills.md, PLAYBOOK.md, FRAMEWORK.md, EXPERIENCES.md, INDEX.md)
2. **Post-Ingestion Diagram Check**: Execute the 'diagrammer' command to rebuild the visual index (docs/diagrams/*.mmd).
3. Shows diffs for each file changed, including diagram files.
4. Asks user: "Apply these changes?" (yes/no)
5. Applies changes if user approves

## Dynamic Internal Path Resolution

When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
  1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
  2. Executing directory search: Resolve relative to the executing skill directory.
  3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/sync-documentation/CONTRACTS/` (or similar skill-specific path).
  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.

## Safety & Workflow

**Safety**:
- Shows diffs before applying (what WILL change)
- Only applies changes if user says "yes"
- Documentation updates are non-destructive (not behavior-changing)

**Project Convention Adherence**: Respect project conventions and architecture, especially for application projects.

**Example Output**:
```
sync-documentation: Reading M2SA3.md...
  - Detected 3 documentation changes.
  - Identified changes impacting workspace boundary and canonical resolution.
  - Proposed changes:
    - docs/skills.md:
      - Line 15: Added "hotfix-issue" to skills catalog
      - Line 42: Added "session-audit" to framework skills
    - docs/PLAYBOOK.md:
      - Line 120: Added "Every Session Workflow" section
    - docs/diagrams/system_snapshot.mmd:
      - Regenerated via diagrammer (diff presented for approval)
    - Reconciled artifact references using canonical resolution.
sync-documentation: Apply these changes?
   Yes, apply all changes
   No, skip
   No, but apply skills.md only
   Custom selection

Selection: 1
```

## Out of Scope (Negative Guardrails)

**Strict Milestone and Project Agnosticism:**
- All instructions, prompt examples, schemas, and file path descriptions must be written in strictly agnostic terms.
- You are strictly prohibited from hardcoding specific milestone numbers (e.g., 'M10') or sequence IDs (e.g., 'M10S4') inside the prompt instructions.
- You must utilize the standard wildcard notation: `M{X}` for milestones, `S{Y}` for specifications, `T{Z}` for test plans, and `M{X}S{Y}` for active sequence identifiers. This ensures the AEF remains 100% portable and reusable across brownfield and greenfield projects.
