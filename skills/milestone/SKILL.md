---
name: milestone
version: 2.4.0
description: Transform a rough feature idea into a complete milestone document through interactive requirements elicitation. Ensures strict, observable scope boundaries.
tools: read, write, ask, edit, glob, bash
user-invocable: true
---

### Milestone Builder: Interactive Requirements Elicitation

This skill assists in creating, managing, and iteratively developing project milestones. It supports starting new milestones and continuing, editing, and improving existing ones, including followup specifications for completed milestones.

You are the definitive gatekeeper of scope. You must ensure that milestone goals and success criteria are concrete, observable, and implementation-independent.

#### Usage

`milestone <command> [options]`

##### Commands

1. **Determine Milestone ID**: Read `docs/MILESTONES.md` (as a canonical artifact). Parse all existing entries (both `(active)` and `(archived)` formats). Find the absolute highest integer `X` in the `[M{X}]` tags. The new milestone identifier MUST be `M{X+1}`. If the file is empty or missing, start at `M1`.
1. **Determine Milestone ID** — Read `docs/MILESTONES.md`. Parse all existing entries. Find the absolute highest integer `X` in the `[M{X}]` tags. The new identifier MUST be `M{X+1}`. If empty, start at `M1`.
1. **Execute Codebase Introspection:** Before writing a single word of the milestone, you MUST run a semantic `code-search` sweep to ground your requirements in the actual state of the codebase. You must execute:
   - Run `generate_skeletons` via the `bash` tool to map out the current structure of public interfaces and executable binaries in the project root.
   - Identify possible "Integration Bindings" (e.g., `bin/omp-discover`), locate those files and use `read` to analyze their inputs, outputs, and JSON/YAML schemas.
   - Your phases may reuse and consume these pre-existing modules rather than inventing parallel, overlapping, or duplicated binaries.

1. **Create**:
   - Initializes a new project milestone in `/milestones/M{X}/M{X}.md`.
   - Initializes a new project milestone in `/milestones/M{X}/M{X}.md`, following the canonical artifact creation protocol.
   - **Canonical Artifact Creation Protocol (7 Steps):**
     1. Determine artifact type (from Artifact Registry or explicit declaration).
     2. Assign or request canonical artifact identity (from Registry or generator).
     3. Generate required metadata (per Artifact Registry schema).
     4. Write canonical frontmatter (type, identity, metadata fields) into `M{X}.md`.
     5. Place artifact in canonical storage location (per Registry storage rules).
     6. Validate the resulting artifact (via canonical validator).
     7. Report the created artifact identity and resolved path (or error if validation fails).
   - **Milestone Artifact Integration**: Ensure newly created milestones have valid canonical frontmatter (type, identity, metadata), canonical identity, `type: milestone` in frontmatter, and are stored/validated per canonical rules.
   - **Canonical Resolution**: Skills must resolve artifacts via the canonical resolution mechanism, not hardcoded paths.
1. **Update**:
   - **Description**: Continues building on an existing milestone, appending new information or resolving outstanding questions within the `<milestone_path>` file.
   - **Arguments**: `<milestone_path>` (Required), `[user_prompt]` (Optional).
1. **Followup**:
   - **Description**: Generate a new specification (`M{X}S{Y}.md`) for followup work on an existing or completed milestone without modifying the original milestone.
   - **Arguments**: `<milestone_path>` (Required), `[focus_area]` (Optional).
   - **Process**: Reads the milestone, determines next available sequence number, checks for reusable verifications, and generates a new specification document.
   - **Verification Reuse Analysis (Strict)**: Scans existing `M{X}S{Y}V.md` files. You MUST only map existing, stable `VER-` or `FR-` IDs to the new work. Do not invent arbitrary connections.
1. **Analyze-reuse**:
   - **Description**: Check whether existing milestone verifications and tests are reusable for a proposed followup.
   - **Arguments**: `<milestone_path>` (Required).
   - **Output**: Summary of reusable verifications and tests that need updates.

#### Template Mapping & Strict Requirements

The milestone document MUST follow the template structure exactly. You MUST output this vertical Markdown table to document requirements mapping:

| Template Section     | Required Constraints                                                                                              |
| :------------------- | :---------------------------------------------------------------------------------------------------------------- |
| **Goal**             | Clear, one-sentence objective.                                                                                    |
| **Motivation**       | Why it matters, and the consequences of inaction.                                                                 |
| **Scope**            | 2-5 concrete deliverables. MUST describe "What", not "How".                                                       |
| **Out of Scope**     | Explicit exclusions to prevent scope creep.                                                                       |
| **Success Criteria** | Measurable checklist items defined as observable system states, artifacts, or behaviors. No exact prose matching. |
| **Risks**            | 2-3 identified technical or architectural risks.                                                                  |
| **Notes**            | Optional implementation-independent observations.                                                                 |

- **No Multi-line Row Collapsing:** You are strictly prohibited from writing table rows side-by-side on a single line. Every row MUST begin on a fresh line starting with the `|` character.

#### Edit Tool Usage

##### Single-line Replacements (Use bash)

For simple one-line edits, bash with `sed` is simpler and less error-prone:
`sed -i 's/old/new/' file`

##### Multi-line Block Edits (Use edit)

For structural changes with multiple lines, use the edit tool:

- Determine Milestone ID: Read `docs/MILESTONES.md` (as a canonical artifact). Parse all existing entries. Find the absolute highest integer `X` in the `[M{X}]` tags. The new identifier MUST be `M{X+1}`. If empty, start at `M1`.

1. Read the file with `read` to get `[PATH#HASH]` (Must be on its own isolated line)
2. On the NEXT line, use `SWAP N.=N:` to replace a single line
3. Use `SWAP.BLK N:` to replace a complete block
4. Always use `+` prefix for new lines

#### Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

#### Integration Bindings

- This tool (`bin/omp-test`) MUST consume the JSON output of `bin/omp-discover` to determine project capabilities.
- This tool's output MUST be parsed by the downstream `evaluate-implementation` pipeline.
