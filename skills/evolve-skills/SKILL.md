---
name: evolve-skills
version: 1.3.1
description: Analyze recent project artifacts and Session Audit Reports (SA1, SA2, SA3...) to learn from mistakes, identify workflow inefficiencies, and automatically update/version our SDD SKILL.md files. Handles multiple session audits and TEMP milestones.
description: Implement an approved specification using project architecture, conventions, and verification plan. Orchestrates implementation workflow with native understanding of LLM-as-Execution-Engine meta-engineering.
tools: read, edit, write, glob, grep, bash
user-invocable: true
---

### Skill Evolution: Meta-Learning and Prompt Refinement

You are an AI systems engineer responsible for improving the prompt architecture of the OMP framework based on empirical evidence from the active milestone.

#### Your Process
1. **Analyze recent artifacts** — Use `glob` and `read` to scan only the active `milestones/` directory for recent Review Reports (`*R.md`), Completion Reports (`*C.md`), and Investigation Reports (`*I*.md`). Do not scan the `archive/` directory to save context limits.
15:2. **Dynamic Internal Path Resolution**: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
16:  1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
17:  2. Executing directory search: Resolve relative to the executing skill directory.
18:  3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/evolve-skills/CONTRACTS/` (or similar skill-specific path).
19:  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
20:3. **Identify failure patterns** — Look for recurring themes: missing tool permissions, hallucinated file paths, misunderstood instructions, or repetitive bugs caused by unclear LLM prompts.
4.  **Restrict Scope**  — You are ONLY permitted to analyze and update the following Spec-Driven Development skills: archive-milestone, bootstrap-project, generate-spec, generate-verification, implement-specification, evaluate-tests, evaluate-implementation, investigate-issue, milestone, review-implementation, sync-documentation, hotfix-issue, manage-roadmap, manage-development, evolve-skills, and session-audit.
22:5. **Draft improvements** — Formulate targeted prompt additions (e.g., negative guardrails in "Out of Scope", missing tool additions, clearer naming conventions) for the specific skills that failed.

3. **Identify failure patterns** — Look for recurring themes: missing tool permissions, hallucinated file paths, misunderstood instructions, or repetitive bugs caused by unclear LLM prompts.

4. **Restrict Scope** — You are ONLY permitted to analyze and update the following Spec-Driven Development skills: `archive-milestone`, `bootstrap-project`, `generate-spec`, `generate-verification`, `implement-specification`, `investigate-issue`, `milestone`, `review-implementation`, `sync-documentation`, `hotfix-issue`, `manage-roadmap`, `manage-development`, `evolve-skills`, and `session-audit`.

5. **Draft improvements** — Formulate targeted prompt additions (e.g., negative guardrails in "Out of Scope", missing tool additions, clearer naming conventions) for the specific skills that failed.

6. **Apply updates** — Use `edit` to update the targeted `~/devcode/aef/agent/skills/*/SKILL.md` files.
- Load M{X}S{Y}V.md (Verification)
31:- Load M{X}S{Y}V.md (Verification)
- Load AGENTS.md for project conventions
32:  If any required artifact is missing: Stop and report exactly which file cannot be found.
33:
#### Your Process
34:
1.  **Resolve artifacts** — Find spec and verification documents by identifier.
35:    - Check the specification for the `#### User Approval` stamp. If it is missing, STOP immediately. Instruct the user to run the `approve-spec` skill.
36:2.  **Read project context** — Load AGENTS.md and understand conventions (including HF01 Evidence First Contract).
37:
## **Dynamic Internal Path Resolution**: When loading static framework assets (templates, contracts), implement a multi-tier path resolution check:
  1. Local checkout search: `~/devcode/aef/agent/CONTRACTS/` and `~/devcode/aef/agent/templates/`.
  2. Executing directory search: Resolve relative to the executing skill directory.
  3. Fallback plugin search: `~/.omp/plugins/node_modules/omp-aef/skills/implement-specification/CONTRACTS/` (or similar skill-specific path).
  Prefer local dev paths. Do not crash on path resolution failure without attempting all tiers.
4. **Analyze specification & Scope** — Identify Functional Requirements, Architecture Impact, and explicitly read the **Strict File Scope (Allowlist & Denylist)**.

9. **Command: log-experience** — If the user asks to log an experience, append it to the 'Active Friction Points' section in `docs/EXPERIENCES.md` using the format:
   `- [Date] **Topic:** {topic} | **Issue:** {issue} | **Suggested Fix:** {fix}`
3. **Analyze specification & Scope** — Identify Functional Requirements, Architecture Impact, and explicitly read the **Strict File Scope (Allowlist & Denylist)**.
38:4. **Inspect existing code** — Use `lsp` to find affected modules. **If `lsp` is unavailable, you MUST fallback to using `code-search`, `ast_grep`, or `grep`.** Remember that `SKILL.md` and `templates/` ARE your modules in meta-engineering tasks.
39:5. **Create Todo list** — One task per Functional Requirement, grouped by module.
40:6. **Validate Test Preconditions & Enforce Boundaries:** — Verify that the generated tests are valid:
41:    - Locate the existing test files in `tests/M{X}/`.
42:    - Execute the tests against the current (pre-implementation) codebase to verify the baseline.
43:    - If ANY test fails due to a syntax error, malformed test plan table, or test integrity failure: STOP immediately. You are strictly forbidden from editing the tests to make them pass. Treat this as an INVALID_TEST and halt.
44:    - _Note: Natural failures due to missing binaries or assertion failures (exit code 1 or 127) are healthy TDD VALID INITIAL FAILURES and represent a green light to implement your production code._
45:
7.  **Orchestrate implementation** — Execute localized changes using `edit` or `write`. If the specification requires updating the "generation logic" of other skills, you must directly edit their `SKILL.md` instructions and `templates/*.md` files.
46:
8.  **Verify implementation** — Execute verification commands and run tests.
47:

11. **Session Audit Integration — Multiple SAs and TEMP Milestones**
    
    When processing Session Audit Reports (`M{X}SA{Y}.md`) generated by `session-audit` skill:
    
    a. **Restricted Scope** — Always include `session-audit` in your scope of skills to analyze and update (line 27 already lists it).
    
    b. **Detect all SA documents**:
       - Use `glob` to find all SA documents: `glob path="milestones/ -name "*SA*.md"`
       - Sort documents chronologically by SA number
       - Prioritize TEMP milestone SAs if present
    
    c. **Process in chronological order**:
       - Start with earliest SA (lowest Y number)
       - Apply cumulative context from all previous SAs
       - Track dependencies between SAs (e.g., SA2 may reference SA1)
       - Use most recent SA as primary context for current changes
    
    d. **Apply cumulative context**:
       - For each SA read, capture "Recommended evolve-skills Actions"
       - Build cumulative list of recommended updates
       - Merge duplicates (e.g., if both SA1 and SA2 recommend same version bump)
       - Prioritize HIGH recommendations first
    
    e. **TEMP milestone handling**:
       - If TEMP milestone detected (M{X}SA{Y}.md in `milestones/TEMP/`), process first
       - Mark TEMP status in `EVOLUTION.md`
       - After processing, prompt user for milestone promotion to formal milestone
       - If promoted, rename TEMP folder and update SA references
    
    f. **Version tracking**:
       - Track version changes from session-audit output (`CHANGELOG_ENTRIES.md`)
       - Ensure `evolve-skills` version matches expected version from M2SA1
- Current version: 1.3.0
    
    g. **Output documentation**:
       - Create or update CHANGELOG_ENTRIES.md with session-audit entries
       - Create MILESTONE_UPDATES.md for progress tracking
       - Create INGEST_ENTRIES.md for ingestion workflow
       - Update AGENTS.md with Infrastructure Skills section

#### Auto-Run After Session Audit

#### Out of Scope
85:#### Out of Scope

##### Strict Test Isolation Guardrail (CRITICAL)
86:
- You are STRICTLY PROHIBITED from writing, editing, regenerating, or modifying any test scripts (e.g., `tests/M{X}/test_*.sh`, `test_*.py`) or test plan documents (e.g., `milestones/M{X}/M{X}S{Y}T{Z}.md`).
87:- Your filesystem modification capabilities are mechanically locked to the "Allowlist" of the active specification. Test plan files and test scripts are NEVER on the implementation Allowlist and must be treated as strictly read-only.
88:- If a test fails during your verification step because the test script is syntax-broken, contains NUL bytes, or the test plan markdown table is structurally invalid, you must NOT attempt to fix it. This is an INVALID_TEST upstream blocker. You MUST immediately halt execution, emit the #NEEDS-CLARIFICATION marker, and hand back control to the user.
89:
#### Edit Tool Usage
90:
##### Multi-line Block Edits (Use edit)
91:
2. Identifies skill improvements based on "Recommended evolve-skills Actions"
3. Shows diffs for each SKILL.md file
4. For each skill, asks user: "Apply changes to [skill-name]?" (yes/no)
5. Applies only approved changes

**Safety**:
- Shows diffs before applying (what WILL change)
- Only applies changes if user approves
- SKILL.md files must have version bump after changes

**Example Output**:
```
evolve-skills: Reading M2SA3.md...
  - Detected 3 action types (milestone, hotfix, external report)
  - Analyzing skill impacts

evolve-skills: Proposed changes:

  hotfix-issue SKILL.md:
  - Line 2: Added user-invocable: true to frontmatter
  - Line 45: Added "Use when: hotfix, bug fix, issue resolution"
  - Line 78: Added integration table in README

  session-audit SKILL.md:
  - Line 15: Expanded scope to capture hotfix and ad-hoc sessions
  - Line 120: Added external report detection
  - Line 150: Added auto-workflow section

evolve-skills: Apply changes to hotfix-issue?
  [1] Yes, apply all changes
  [2] No, skip
  [3] No, but apply session-audit only
  [4] Custom selection

Selection: 1

evolve-skills: Applying changes to hotfix-issue...
evolve-skills: hotfix-issue updated to 1.1.0
```

**Fallback (Option C)**:
If user cancels or skips all changes:
1. Stop workflow (don't auto-run skills-auditor)
2. Show summary of proposed changes
3. Ask user: "What would you like to do next?"
4. Options:
   - "Continue without evolve-skills"
   - "Apply changes manually"
   - "Run skills-auditor audit only"
   - "Run both evolve-skills and skills-auditor"


### Phase 4: Skill Health Audit Layer

Add automated quality monitoring for evolve-skills dependencies using skills-auditor.

**What it does**:
1. Identifies all evolve-skills dependencies (from line 26)
2. Runs skills-auditor audit on each dependency
3. Collects health metrics (priority ratings, issues, recommendations)
4. Generates health report in `evolve-skills/health/*.yaml`

**Health Report Structure** (`evolve-skills/health/{skill-name}.yaml`):
```yaml
skill: hotfix-issue
version: "1.1.0"
last_audited: "2026-07-23"

priority: "HIGH"
priority_reason: "Used for critical bug fixes"

issues:
  - type: "missing_integration"
    description: "Missing integration table in README"
    severity: "MEDIUM"
  - type: "version_mismatch"
    description: "SKILL.md version 1.0.0, expected 1.1.0"
    severity: "LOW"

recommendations:
  - "Add integration table to README"
  - "Update version to 1.1.0"

status: "needs_improvement"
```

**Priority Scale**:
- **HIGH**: Critical functionality, high usage
- **MEDIUM**: Important but not critical
- **LOW**: Nice to have, low usage

**Status Values**:
- `healthy` — All checks pass
- `needs_improvement` — Minor issues, no blocking problems
- `degraded` — Significant issues, functional but problematic
- `critical` — Major issues, requires immediate attention
#### Evolution Principles
217:#### Evolution Principles
* **Evidence-based** — Every prompt change must be tied directly to a documented failure or inefficiency in a recent artifact.
218:* **Negative Guardrails** — Prioritize adding explicit "Never do X" rules to the "Out of Scope" sections over adding complex positive instructions.
219:* **Do Not Touch Core Tools** — Never modify non-SDD skills (like code-search, bash tools, etc.).
220:* **Cumulative Processing** — Process multiple SAs in order, building on cumulative context.
221:* **TEMP First** — Always process TEMP milestones before formal milestones.
222:
## Out of Scope (Negative Guardrails)
225:## Out of Scope (Negative Guardrails)

**Strict Milestone and Project Agnosticism:**
227:- All instructions, prompt examples, schemas, and file path descriptions must be written in strictly agnostic terms.
- You are strictly prohibited from hardcoding specific milestone numbers (e.g., 'M10') or sequence IDs (e.g., 'M10S4') inside the prompt instructions.
228:- You must utilize the standard wildcard notation: `M{X}` for milestones, `S{Y}` for specifications, `T{Z}` for test plans, and `M{X}S{Y}` for active sequence identifiers. This ensures the AEF remains 100% portable and reusable across brownfield and greenfield projects.
229:
230:
231:
- Can be invoked manually: `evolve-skills audit`

#### Command: audit

Run skills-auditor to check health of all evolve-skills dependencies.

**Usage**: `evolve-skills audit`

**What it does**:
1. Audits all 14 evolve-skills dependencies
2. Generates individual YAML health reports in `evolve-skills/health/`
3. Shows dashboard with priority ratings and status

**Output**:
- `evolve-skills/health/{skill-name}.yaml` — Individual health report
- Console dashboard — Summary of all skills

**Safety**:
- Read-only, no changes to skills
- Runs on-demand only, not continuous

**Note**: Do NOT auto-run skills-auditor if user cancels evolve-skills changes. Let user decide what to do next.
#### Evolution Principles

* **Evidence-based** — Every prompt change must be tied directly to a documented failure or inefficiency in a recent artifact.
* **Negative Guardrails** — Prioritize adding explicit "Never do X" rules to the "Out of Scope" sections over adding complex positive instructions.
* **Do Not Touch Core Tools** — Never modify non-SDD skills (like code-search, bash tools, etc.).
* **Cumulative Processing** — Process multiple SAs in order, building on cumulative context.
* **TEMP First** — Always process TEMP milestones before formal milestones.

#### Output

1. Edited `SKILL.md` files (with incremented version numbers).
2. An updated `~/devcode/aef/agent/skills/evolve-skills/EVOLUTION.md` ledger.

#### Example SA Processing Workflow

```bash
# Session 1: M2SA1.md
# 1. Read M2SA1.md
# 2. Identify recommended actions (session-audit updated, code-search added)
# 3. Apply updates to evolve-skills and session-audit
# 4. Bump versions
# 5. Document in EVOLUTION.md

# Session 2: M2SA2.md (2 weeks later)
# 1. Read all SAs: M2SA1.md, M2SA2.md
# 2. Process cumulatively (use SA2 as primary, reference SA1)
# 3. Apply new recommendations
# 4. Bump versions
# 5. Document in EVOLUTION.md with references to both SAs
```

#### EVOLUTION.md Structure

```markdown
# Skill Evolution Log

## [Date] - M{X}SA{Y}

### Skill: {skill-name}
- **Old Version**: {x.y.z}
- **New Version**: {x.y.z}
- **Rationale**: Session-audit detected framework improvement needed
- **Changes**:
  - {description of changes}
- **References**: `M{X}SA{Y}.md`, `M{X}SA{Y-1}.md` (if applicable)

### TEMP Milestone: M{N}SA{Y}
- **Status**: Processed (incomplete)
- **Action Taken**: Applied framework improvements
- **Next Step**: Prompt user for milestone promotion
- **References**: `M{N}SA{Y}.md`

### TEMP Milestone: M{N}SA{Y} (Closed)
- **Status**: Closed as completed
- **Action Taken**: Deleted TEMP milestone
- **References**: M{N}SA{Y}.md
```

## Edit Tool Usage

### Single-line Replacements (Use `bash`)

For simple one-line edits, `bash` with `sed` is simpler and less error-prone:

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file

# Example: Fix a single instruction line
sed -i.bak '27s/.*/13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current {Y} sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol./' skills/generate-spec/SKILL.md
```

### Multi-line Block Edits (Use `edit`)

For structural changes with multiple lines, use the `edit` tool:

**Steps**:
1. Read the file with `read` to get `[PATH#HASH]`
2. Use `SWAP N.=N:` to replace a single line
3. Use `SWAP.BLK N:` to replace a complete block
4. Always use `+` prefix for new lines

**Example**:
```
[SKILL.md#ABC123]
SWAP 27.=27:
+13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current `{Y}` sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol.
```

## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
