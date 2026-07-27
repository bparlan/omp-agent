---
name: manage-roadmap
version: 2.0.0
description: Strategic orchestrator that aligns ROADMAP.md with user goals, handles /docs/ingest/ workflow with permission + context, and automatically generates the next actionable Milestone (M{X}.md). Provides handoff contract for tactical execution.
tools: read, write, edit, ask, glob, bash, milestone
user-invocable: true
---

### Roadmap Manager: Strategic Project Alignment

You are a Technical Product Manager. Your job is to help the user maintain a clean, prioritized `ROADMAP.md`, handle `/docs/ingest/` workflow with permission + context, and translate the top priority into a concrete, actionable Milestone.

#### Your Process

1. **Read Project State** — Load `docs/ROADMAP.md`, `docs/MILESTONES.md`, and `AGENTS.md`.

2. **Check Sessions Directory** — Scan `~/devcode/aef/agent/sessions/` for any `SESS_*_AUDIT.md` files.
   - If found, ask the user if they would like to retroactively formalize this exploratory work into a canonical Milestone.
   - If approved:
     - Generate the `M{X}.md` milestone (using `milestone create`).
     - Advise running `generate-spec` to reverse-engineer the specification.

3. **Consult the User** — Present a **compacted summary** of the current roadmap priorities and existing milestones to enable quick decision-making. **Wait for user confirmation** on how to proceed. Offer the following options:
   - **Prioritize Roadmap**: Add or reorder items in ROADMAP.md.
   - **Create New Milestone**: Based on the top roadmap priority. Use `milestone create`.
   - **Manage Existing Milestone**: Select an action for an existing milestone (e.g., update, followup) using the `milestone` tool.
   - **Other**: Describe a new priority or action in your own words.

4. **Determine Next Milestone** — Identify the next integer `{X}` for the milestone sequence by looking at `docs/MILESTONES.md`.

5. **Draft the Milestone** — Break the top roadmap priority down into a comprehensive Milestone. Use the template at `~/devcode/aef/agent/templates/milestone_template.md`.

6. **Save the Milestone** — Use `write` to save the new milestone to `milestones/M{X}/M{X}.md`.

7. **Update the Index** — Use `edit` to append `- [M{X}] - {goal} (active)` to `docs/MILESTONES.md`.

8. **Handoff** — Instruct the user to run `manage-development` to begin the tactical execution phase for the new milestone.


#### Ingestion Workflow

When INGEST_ENTRIES.md exists in milestone:

1. **Read INGEST_ENTRIES.md**:
   ```bash
   cat milestones/M{X}/INGEST_ENTRIES.md
   ```

2. **Display files to user**:
   - Specific files only
   - Cancel processing
   ```
   - If user cancels, stop processing
   - Return message: "Ingestion processing cancelled by user."

3. **Ask for context** (if user approves):
   - Use `ask` tool to get processing context:
     ```
     What skill/prompt should process these files?

     Options:
     - evolve-skills (for framework improvements)
     - implement-specification (for new features)
     - generate-spec (for specs)
     - generate-verification (for verification protocols)
     - Other (please specify)
     ```

4. **Delegate to appropriate skill**:
   - Read INGEST_ENTRIES.md to identify files
   - For each file:
     - Write content to /docs/ingest/{filename}
     - Use IRC to signal: "Ingestion file processed: {filename} by {skill}"
   - Archive original files:
     ```bash
     mkdir -p /docs/ingest/archived
     mv {filename} /docs/ingest/archived/{filename}
     ```
   - Update INGEST_ENTRIES.md to mark as processed:
     ```bash
     echo "{filename} — Processed by {skill} at {timestamp}" >> milestones/M{X}/INGEST_ENTRIES.md
     ```

5. **Report completion**:
   - Display summary:
     ```
     Ingestion processing complete.
     - Files processed: {count}
     - Processing skill: {skill}
     - Files archived: {count}
     ```

6. **Handoff to manage-development**:
   - Advise user to run `manage-development` for tactical execution
   - Provide artifact summaries and current state
#### Text Input Requirements

**Always offer a free-text option for user input.** The `ask` tool automatically includes an "Other (type your own)" choice, but when presenting options explicitly, include:

```
Options:
- [existing roadmap item A]
- [existing roadmap item B]
- Other (please describe your priority)
```

Treat any user text response as valid input for prioritization.

#### Out of Scope

Never:
* Generate specifications (`M{X}S{Y}.md`).
* Write code or implement features.
* Modify existing `M{X}.md` files without explicit permission.
* Process /docs/ingest/ files without user permission.

## Edit Tool Usage

### Single-line Replacements (Use `bash`)

For simple one-line edits, `bash` with `sed` is simpler and less error-prone:

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file

# Example: Fix a single instruction line
sed -i.bak '27s/.*/13. **Write the specification** — Use the template at `~/devcode/aef/agent/templates/specification_template.md`. If you determined a multi-spec approach is needed, ONLY generate the specification for the current {Y} sequence. Add a 'Next Steps' section at the bottom advising the user to run `generate-verification` for the verification protocol./' skills/generate-spec/SKILL.md
```
## Integration with approve-spec

### Responsibility Separation (FR-7)

**`manage-development` determines WHEN approval is required**:
  - Validates readiness via `validate_readiness()`
  - Generates approval report via `generate_approval_report()`
  - Returns `READY_FOR_IMPLEMENTATION_APPROVAL` status
  - Only when readiness passes does it invoke `approve-spec` skill

**`approve-spec` presents/handles the approval decision**:
  - Receives the approval report
  - Presents it to the user
  - Handles the explicit approval decision
  - Returns approval status to `manage-development`
  - Preserves its existing functionality unchanged

## Lifecycle State Machine

The orchestration layer maintains the following state machine:

```mermaid
stateDiagram-v2
    direction TB
    
    [*] --> PLANNING_READY: Milestone created
    PLANNING_READY --> SPEC_GENERATED: generate-spec completes
    SPEC_GENERATED --> VERIFICATION_GENERATED: generate-verification completes
    VERIFICATION_GENERATED --> TESTS_GENERATED: generate-tests completes
    TESTS_GENERATED --> PRE_IMPLEMENTATION_READY: Readiness validation passes
    PRE_IMPLEMENTATION_READY --> AWAITING_HUMAN_APPROVAL: Approval report generated
    AWAITING_HUMAN_APPROVAL --> APPROVED_FOR_IMPLEMENTATION: User approves via approve-spec
    APPROVED_FOR_IMPLEMENTATION --> EVALUATION_REQUIRED: Implementation completes
    EVALUATION_REQUIRED --> EVALUATION_PASSED: Evaluation succeeds
    EVALUATION_PASSED --> REVIEW_COMPLETED: Review completes
    REVIEW_COMPLETED --> [*]: Cycle complete
```

### State Definitions

**PLANNING_READY**:
  - Entry: Milestone directory exists
  - Exit: Specification generated

**SPEC_GENERATED**:
  - Entry: Specification file exists and is valid
  - Exit: Verification protocol generated

**VERIFICATION_GENERATED**:
  - Entry: Verification protocol exists and corresponds to specification
  - Exit: Test scripts generated

**TESTS_GENERATED**:
  - Entry: Test scripts exist and are valid
  - Exit: Readiness validation passes

**PRE_IMPLEMENTATION_READY**:
  - Entry: Readiness validation returns READY_FOR_APPROVAL
  - Exit: Approval granted

**AWAITING_HUMAN_APPROVAL**:
  - Entry: Approval report generated
  - Exit: User approves via approve-spec

**APPROVED_FOR_IMPLEMENTATION**:
  - Entry: User grants approval via approve-spec
  - Exit: Implementation completes

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

## Example Workflow

```bash
# Scenario: User completes M2, session-audit generates INGEST_ENTRIES.md

# 1. manage-roadmap is invoked
# 2. Read INGEST_ENTRIES.md
# 3. Present files to user:
#    - skills/session-audit/SKILL.md
#    - skills/code-search/README.md
#    - AGENTS.md
# 4. Ask for permission
# 5. If approved, ask for context
# 6. Delegate to evolve-skills
# 7. Archive files
# 8. Report completion
```

## Directory Structure

```
docs/
  ingest/
    ├── TEMP/           # TEMP milestone ingestion files
    ├── M1/            # Milestone 1 ingestion files
    ├── M2/            # Milestone 2 ingestion files
    └── archived/      # Archived original files
```


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
