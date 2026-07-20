---
name: milestone
version: 2.3.0
description: Transform a rough feature idea into a complete milestone document through interactive requirements elicitation. Supports followup specifications and verification reuse analysis.
tools: read, write, ask, edit, glob
user-invocable: true
---

# Milestone Builder: Interactive Requirements Elicitation

This skill assists in creating, managing, and iteratively developing project milestones. It supports starting new milestones and continuing, editing, and improving existing ones, including followup specifications for completed milestones.

## Usage

`milestone <command> [options]`

### Commands

-   **`create`**:
    -   Initializes a new project milestone.
    -   Creates a directory and a markdown file for the milestone (e.g., `/milestones/M1/M1.md`).
    -   Sets up a basic structure for the milestone.

-   **`update <milestone_path> [user_prompt]`**:
    -   **Description**: Continues building on an existing milestone, allowing for edits, updates, and improvements to the specified milestone file.
        -   **Preserve and Evaluate**: Reads the existing milestone file, evaluates user-provided data and prompts against milestone requirements, and then appends or refines content. Existing milestone documents are preserved and not deleted.
        -   **Content Update**: Appends new information, refines existing content, or resolves outstanding questions within the `<milestone_path>` file.
    -   **Arguments**:
        -   `<milestone_path>`: (Required) The file path to the existing milestone document that needs to be updated.
        -   `[user_prompt>`: (Optional) A natural language prompt containing the new information, answers, or directives for updating the milestone. The skill will attempt to intelligently parse this prompt for actionable data.

-   **`followup <milestone_path> [focus_area]`**:
    -   **Description**: Generate a new specification (M{X}S{Y}.md) for followup work on an existing or completed milestone. This creates a "new specification" addition without modifying the original milestone.
    -   **Arguments**:
        -   `<milestone_path>`: (Required) The file path to the existing milestone document.
        -   `[focus_area]`: (Optional) A text description of the specific area or aspect to focus on for the followup work. If omitted, prompts the user for clarification.
    -   **Process**:
        -   Reads the milestone and scans for existing specifications.
        -   Determines next available specification sequence number.
        -   Checks for reusable verifications and tests from existing specifications.
        -   Generates a new specification document with appropriate derivation references.
    -   **Verification Reuse Analysis**:
        -   Scans existing M{X}S{Y}V.md files for relevant verification protocols.
        -   Identifies which verification items apply to the followup scope.
        -   Notes reusable automated validation items.
        -   Flags tests that may need updates or re-running.

-   **`analyze-reuse <milestone_path>`**:
    -   **Description**: Check whether existing milestone verifications and tests are reusable for a proposed followup.
    -   **Arguments**:
        -   `<milestone_path>`: (Required) The file path to the existing milestone.
    -   **Output**: Summary of reusable verifications, tests that need updates, and recommendations.

## Core Features

### Iterative Milestone Development
The `milestone` skill is designed for iterative progress:
-   **Continuation**: The `update` command allows users to seamlessly resume work on any milestone by reading its current state from the provided file path.
-   **In-place Editing**: The skill directly modifies and enhances the specified milestone markdown file (`.md`), ensuring changes are persistent.
-   **Data-Driven Updates**: User input is parsed to extract specific data points and answers to relevant questions, ensuring that updates are meaningful and targeted.

### Followup Specifications
-   **New Specification Addition**: The `followup` command creates a followup specification (e.g., M1S2.md) for additional work on an existing milestone.
-   **Verification Reuse Analysis**: When generating followup specifications, the skill automatically analyzes existing verification documents to identify reusable test items.
-   **Text Input Always Available**: All prompts accept free-form text input; users are never restricted to predefined options only.

### Intelligent Prompt Handling
-   The skill intelligently analyzes user prompts to identify key information relevant to milestone progress.
-   It can identify and validate answers against a set of implicit or explicit milestone building questions, ensuring that critical aspects are addressed.

## Question Flow

### Goal
- "What is the single, concrete objective of this milestone?"
- "If this milestone succeeds, what specific capability exists that didn't before?"

### Motivation
- "Why does this milestone matter? What problem does it solve?"
- "What happens if we don't do this?"

### Scope
Ask for specific deliverables:
- "List 2-5 concrete items that will be completed."
- "For each: what does 'done' look like?"

### Out of Scope
- "What will definitively NOT be included?"
- "Are there related features being explicitly excluded?"

### Success Criteria
- "What measurable outcomes define success?"
- "How will we know this milestone is complete?"

### Risks
Probe for:
- Technical unknowns
- Dependency issues
- External factors

### Notes (Optional)
- "Any assumptions, constraints, or observations to record?"

## Rules

- **One question per turn** — Wait for the answer before proceeding.
- **Flag ambiguity** — "That's unclear. Do you mean X or Y?"
- **Challenge scope creep** — When answers widen beyond original intent, ask: "Is this within the original scope, or should we note this as new work?"
- **Detect hidden requirements** — "If we do X, do we also need Y?"
- **Testing implications** — "How would you verify this works?"
- **Always offer text input** — All prompts must include a free-text option; never restrict users to only predefined choices.

## Output

When all required fields have sufficient detail:
1. Generate the milestone document using the template at `~/devcode/aef/agent/templates/milestone_template.md`, based on evaluated data.
2. Write or edit the generated milestone to `milestones/M{X}/M{X}.md` in the `milestones/M{X}/` directory.
3. For followup: Generate specification to `milestones/M{X}/M{X}S{Y}.md` (where Y is next available sequence).
4. Update `docs/MILESTONES.md`: append `- [M{X}] - {goal} (active)` if file missing, add entry if existing.
5. Advise user to run `manage-development` for milestone development phase.
6. Terminate immediately — no further action.

## Template Mapping

| Template Section | Required Questions |
|-----------------|------------------|
| Goal | Clear, one-sentence objective |
| Motivation | Why it matters, consequences of inaction |
| Scope | 2-5 concrete deliverables |
| Out of Scope | Explicit exclusions |
| Success Criteria | Measurable checklist items |
| Risks | 2-3 identified risks |
| Notes | Optional observations |

---
*This documentation outlines the enhanced capabilities for iterative milestone management, including continuation, editing, followup specifications, and verification reuse analysis.*

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
