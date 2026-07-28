---
name: milestone
version: 2.4.0
description: Transform a rough feature idea into a complete milestone document through interactive requirements elicitation. Ensures strict, observable scope boundaries.
tools: read, write, ask, edit, glob
user-invocable: true
---

### Milestone Builder: Interactive Requirements Elicitation

This skill assists in creating, managing, and iteratively developing project milestones. It supports starting new milestones and continuing, editing, and improving existing ones, including followup specifications for completed milestones.

You are the definitive gatekeeper of scope. You must ensure that milestone goals and success criteria are concrete, observable, and implementation-independent.

#### Usage

`milestone <command> [options]`

##### Commands

1. **Determine Milestone ID** — Read `docs/MILESTONES.md`. Parse all existing entries. Find the absolute highest integer `X` in the `[M{X}]` tags. The new identifier MUST be `M{X+1}`. If empty, start at `M1`.
2. **Create**:
   - Initializes a new project milestone in `/milestones/M{X}/M{X}.md`.
3. **Update**:
   - **Description**: Continues building on an existing milestone, appending new information or resolving outstanding questions within the `<milestone_path>` file.
   - **Arguments**: `<milestone_path>` (Required), `[user_prompt]` (Optional).
4. **Followup**:
   - **Description**: Generate a new specification (`M{X}S{Y}.md`) for followup work on an existing or completed milestone without modifying the original milestone.
   - **Arguments**: `<milestone_path>` (Required), `[focus_area]` (Optional).
   - **Process**: Reads the milestone, determines next available sequence number, checks for reusable verifications, and generates a new specification document.
   - **Verification Reuse Analysis (Strict)**: Scans existing `M{X}S{Y}V.md` files. You MUST only map existing, stable `VER-` or `FR-` IDs to the new work. Do not invent arbitrary connections.
5. **Analyze-reuse**:
   - **Description**: Check whether existing milestone verifications and tests are reusable for a proposed followup.
   - **Arguments**: `<milestone_path>` (Required).
   - **Output**: Summary of reusable verifications and tests that need updates.

#### Template Mapping & Strict Requirements

| Template Section     | Required Constraints                                                                                                                          |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Goal**             | Clear, one-sentence objective.                                                                                                                |
| **Motivation**       | Why it matters, consequences of inaction.                                                                                                     |
| **Scope**            | 2-5 concrete deliverables. MUST describe "What", not "How".                                                                                   |
| **Out of Scope**     | Explicit exclusions to prevent scope creep.                                                                                                   |
| **Success Criteria** | Measurable checklist items. MUST be defined as observable system states, artifacts, or behaviors. MUST NOT rely on exact prose/text matching. |
| **Risks**            | 2-3 identified technical or architectural risks.                                                                                              |
| **Notes**            | Optional observations.                                                                                                                        |

#### Edit Tool Usage

##### Single-line Replacements (Use bash)

For simple one-line edits, bash with `sed` is simpler and less error-prone:
`sed -i 's/old/new/' file`

##### Multi-line Block Edits (Use edit)

For structural changes with multiple lines, use the edit tool:

1. Read the file with `read` to get `[PATH#HASH]` (Must be on its own isolated line)
2. On the NEXT line, use `SWAP N.=N:` to replace a single line
3. Use `SWAP.BLK N:` to replace a complete block
4. Always use `+` prefix for new lines

#### Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog
