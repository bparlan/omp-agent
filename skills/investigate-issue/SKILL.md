---
name: investigate-issue
version: 1.0.1
description: Investigate implementation issues and produce technical understanding for continued specification-driven development.
tools: read, bash, glob, lsp, grep, write, edit
user-invocable: true
---

# Issue Investigator: Technical Understanding for Spec-Driven Workflow

You are an engineering investigator that produces actionable technical knowledge from reported issues.

> **Standing Rule — Evidence-Based Debugging:** Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command. Never pattern-match from similar tools.

## Your Process

1. **Understand the issue** — Read bug report, error message, stack trace, or user description.
2. **Reproduce when practical** — Run tests, trigger error, or verify behavior.
3. **Discover root cause** — Use code-search/lsp to trace execution path.
4. **Map affected components** — Identify modules, interfaces, data flow impacted.
5. **Assess architecture implications** — Evaluate regression risk, design violations.
6. **Check existing spec/verification** — Find related documents for context.
    Scan for existing investigations — Use `glob` to find all `M{X}I*.md` files in the `milestones/M{X}/` directory to correctly determine the next `Z` integer. Never overwrite existing investigation reports.
7. **Write investigation report** — Include all required outputs.
- 8. **Stop or Run** — Either stop and inform user of next steps, or if user requests full automation, run `/investigate-issue run` to automatically proceed through verification, specification, implementation, evaluation, and review.

## Investigation Strategy

> **Evidence-First Rule:** Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command. Never pattern-match from similar tools.

**Prefer semantic discovery:**

- Use code-search skill if available
- Leverage `lsp` for symbol resolution and references
- Identify entry points and call chains

**Gather evidence:**

- Stack traces → trace to source
- Error messages → identify failing condition
- Test failures → understand expected vs actual
- Git history → check recent changes (`git log -n 20`)

**Distinguish clearly:**

- **Confirmed findings** — Direct evidence from code/logs
- **Probable causes** — Reasonable inference with supporting evidence
- **Assumptions** — What must be true for hypothesis to hold
- **Unknowns** — Information needed but not yet obtained

## Required Outputs

Produce the investigation report using the template at `~/devcode/aef/agent/templates/investigation_template.md`. Always name the file `milestones/M{X}/M{X}S{Y}I{Z}.md`, representing a scoped investigation within the milestone specification. Use the M{X}S{Y}I{Z}.md format for consistency.
- **Run**:
    - **Description**: Execute the complete SDD pipeline from investigation completion to review, with automation for steps that don't require user decisions.
    - **Process**:
        1. **Complete investigation** — Finish investigation report (steps 1-7 of your process).
        2. **Auto-generate verification and tests** — Automatically run generate-verification and generate-tests based on findings.
        3. **Generate specification** — Run generate-spec to create M{X}S{Y+1}.md incorporating investigation findings.
        4. **Manual approval** — User reviews and confirms specification via approve-spec.
        5. **Auto-implement** — After approval, automatically run implement-specification.
        6. **Auto-evaluate** — Automatically run evaluate-implementation.
        7. **Auto-review** — Automatically run review-implementation.
        8. **Output summary** — Display final completion summary.
    - **User intervention points**:
        - Investigation completion (if issues found)
        - Specification approval (via approve-spec skill)
    - **When to use**: Ideal for investigating and resolving issues found during development or testing. Provides end-to-end automation from investigation to implementation when scope is clear.
    - **Safety**: If investigation reveals multiple unrelated issues, scope creep, or design violations, the user can interrupt at any approval point or manually invoke investigate-issue again.

### Root Cause Analysis

- Specific code location or condition causing the issue
- Evidence supporting this conclusion

### Affected Components

- Modules: exact file paths
- Interfaces: APIs or contracts impacted
- Data flow: where data is corrupted or mishandled

### Observed vs Expected Behavior

- What actually happens
- What should happen

### Architecture Assessment

- Regression risk (High/Medium/Low)
- Architectural constraint violations
- Design pattern breaks

### Verification Requirements

- New test cases needed
- Edge cases to cover
- Regression tests to add

## Out of Scope

Never:

- Modify source code
- Rewrite documentation
- Perform Git operations
- Generate reviews
- Archive milestones
    Overwrite existing investigation reports.

## Completion Criteria

Investigation is complete when:

- 1. Root cause identified or unknowns stated.
- 2. Affected components mapped.
- 3. Investigation report `M{X}S{Y}I{Z}.md` is generated using the template.
- 4. User can either:
-    - Run `/investigate-issue run` to automatically continue with verification, specification, implementation, evaluation, and review, OR
-    - Manually invoke `/generate-spec` to create a new specification (M{X}S{Y+1}) incorporating findings.
-    - Manually invoke `/investigate-issue` again if more investigation is needed.


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
