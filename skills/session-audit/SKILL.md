---
name: session-audit
version: 1.3.1
description:
  Capture any session (milestone, hotfix, manual edits, external reports) into
  Session Audit Reports (M{X}SA{Y}.md) that drive documentation updates,
  skill evolution, and quality monitoring. Use when the user says
  "session-audit", "document this session", "capture this session".
tools: code-search, read, ask, write, edit, askuserquestion, bash
user-invocable: true
---

# Session Audit Skill

1. **Dynamic Internal Path Resolution**: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
   1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
   2. Executing directory search: Resolve relative to the executing skill directory.
   3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/session-audit/CONTRACTS/` (or similar skill-specific path).
      Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
2. **Analyze recent artifacts** — Use `glob` and `read` to scan only the active `milestones/` directory for recent Review Reports (`*R.md`), Completion Reports (`*C.md`), and Investigation Reports (`*I*.md`). Do not scan the `archive/` directory to save context limits.
3. **Identify failure patterns** — Look for recurring themes: missing tool permissions, hallucinated file paths, misunderstood instructions, or repetitive bugs caused by unclear LLM prompts.
4. **Restrict Scope** — You are ONLY permitted to analyze and update the following Spec-Driven Development skills: `archive-milestone`, `bootstrap-project`, `generate-spec`, `generate-verification`, `implement-specification`, `investigate-issue`, `milestone`, `review-implementation`, `sync-documentation`, `hotfix-issue`, `manage-roadmap`, `manage-development`, `evolve-skills`, and `session-audit`.
5. **Draft improvements** — Formulate targeted prompt additions (e.g., negative guardrails in "Out of Scope", missing tool additions, clearer naming conventions) for the specific skills that failed.

### 1. Milestone Session

**Trigger**: User mentions milestone (M1, M2, etc.) or milestone > development
   1. **Apply updates** — Use `edit` to update the targeted `~/devcode/aef/agent/skills/*/SKILL.md` files.
   2. **Bump version** — Find the `version: x.y.z` field in the frontmatter of the skill you are editing. Increment the patch version (e.g., `1.0.0` to `1.0.1`).
   3. **Document the evolution** — Append a log to `~/devcode/aef/agent/skills/evolve-skills/EVOLUTION.md`. Record the date, the skill updated, the old/new version, and the exact rationale derived from the artifacts. Do not place this in the project's `docs/` folder.
      4. **Command: log-experience** — If the user asks to log an experience, append it to the 'Active Friction Points' section in `docs/EXPERIENCES.md` using the format:
         - [Date] **Topic:** {topic} | **Issue:** {issue} | **Suggested Fix:** {fix}
      5. **Command: analyze** — Read the 'Active Friction Points' from `docs/EXPERIENCES.md`. For each point:
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
