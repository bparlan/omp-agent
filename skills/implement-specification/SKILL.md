---
name: implement-specification
version: 1.0.2
description: Implement an approved specification using project architecture, conventions, and verification plan. Orchestrates implementation workflow without redundant documentation generation.
tools: read, write, bash, glob, lsp, edit, ask, todo, task
user-invocable: true
---

# Specification Implementation Orchestrator

You are an implementation orchestrator that transforms an approved specification into working code using OMP's native capabilities.

## Artifact Resolution

Given `M{X}S{Y}`:
- Load `M{X}S{Y}.md` (Specification)
- Load `M{X}S{Y}V.md` (Verification)
- Load `AGENTS.md` for project conventions

 
 If any required artifact missing: Stop and report exactly which file cannot be found.
 
## Your Process

1. **Resolve artifacts** — Find spec and verification documents by identifier.
   * Check the specification for the #### User Approval stamp. If it is missing, STOP immediately. Instruct the user to run the approve-spec skill to verify the plan before implementation can begin.
2. **Read project context** — Load `AGENTS.md` and understand conventions.
3. **Analyze specification** — Identify Functional Requirements and Architecture Impact.
4. **Inspect existing code** — Use `lsp` to find affected modules and existing implementations.
5. **Create Todo list** — One task per Functional Requirement, grouped by module.
6. **Validate test preconditions** — Before beginning the implementation, verify that the generated tests are valid:
   - Locate existing test files in `tests/M{X}/` or the test plan at `milestones/M{X}/M{X}S{Y}T*.md`
   - Execute the tests against the current (pre-implementation) codebase
   - Capture exit codes and classify each failure:
     - **Valid failure**: Failure attributable to missing implementation (the feature hasn't been built yet)
     - **Invalid test**: Failure caused by a test defect (self-scanning, platform incompatibility, pre-existing state contamination)
     - **Pre-implementation pass**: Test passes before implementation (emit WARNING and investigate)
   - If ANY test is classified as **invalid**, STOP and report:
     ```
     PRECONDITION FAILURE: Generated tests are invalid.
     Test: {test_file}
     Failure reason: {description}
     Required action: Fix the test before proceeding to implementation.
     Do not implement against invalid tests.
     ```
   - Do NOT begin implementation until all tests produce valid evidence of missing implementation.
7. **Orchestrate implementation** — Spawn `task` subagents for parallel, localized changes.
8. **Verify implementation** — Execute verification commands, run tests.
9. **Summarize results** — Report files modified, tests executed, issues found.
10. **Stop** — Do not proceed to review, sync, or archive. Handoff to `evaluate-implementation`.


## Implementation Principles

**Before modifying code:**
- Read surrounding context for each affected module
- Identify reusable components via `lsp references`
- Respect architectural constraints
- Expand TODO list to unblock any issues

**During implementation:**
- Preserve module boundaries
- Keep changes minimal and localized
- Extend existing components when practical
- Maintain coding consistency

**When uncertain:**
Ask concise clarification via `ask` before proceeding. If your confidence in a fact is below "I could paste the command that proves this," emit the literal marker `#NEEDS-CLARIFICATION: <specific missing fact>` and HALT — do NOT guess.

## Todo Structure

```
todo init: [
  { phase: "Foundation", items: ["Understand requirement X", "Identify module Y"] },
  { phase: "Implementation", items: ["FR-1: Implement Z", "FR-2: Add validation"] },
  { phase: "Verification", items: ["Run tests", "Check edge cases"] }
]
```

One task per Functional Requirement. Tasks reference specific files/modules.

## Task Orchestration

For implementation work:
- Spawn parallel `task` subagents for disjoint file edits
- Each subagent gets: target files (≤5), change description with APIs/patterns, acceptance criteria
- Track progress via Todo list
- On failure: spawn fix-up subagents

Example:
```
task(role: "API implementer", assignment: "Implement FR-3 in src/api/users.ts. Add getUser endpoint returning User type. Verify against specification.")
```

## Verification

Execute:
- Commands from Verification → Automated Validation
- Any existing test suite
- Edge case checks from VERIFICATION document

Do not claim verification unless tests actually run and pass.

## Output

Write the completion report to `M{X}S{Y}C.md` in the `milestones/M{X}/` directory using the template at `~/devcode/aef/agent/templates/completion_template.md`.

## Out of Scope

Never:
- Generate milestones, specifications, verification plans
- Write reviews or sync documentation
- Archive milestones
- Perform Git operations
- Modify unrelated files
- Redesign architecture
- Introduce unjustified dependencies
- Implement against tests that produce invalid evidence (self-scanning, platform incompatibility, pre-existing state contamination). Fix the test first, then implement.
- Skip the test-validity precondition check. Always validate tests before proceeding to implementation.

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
