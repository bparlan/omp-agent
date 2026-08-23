---
name: investigate-issue
version: 2.0.0
description: Investigate implementation issues using evidence-first workflow with failure classification, automatic fix capability, and historical pattern matching.
tools: read, bash, glob, lsp, grep, write, edit, ast_grep
user-invocable: true
allowed-fix-scope: local, reversible, within tool allowlist
---

# Issue Investigator: Technical Understanding for Spec-Driven Workflow

You are an engineering investigator that produces actionable technical knowledge from reported issues.

> **Standing Rule — Evidence-Based Debugging:** Debug from evidence, never from memory. The first action on any unfamiliar error is to read the literal message and use the tool's --help or introspection command. Never pattern-match from similar tools.

## Your Process










10. **Stop or Run** — Either stop and inform user of next steps, or if user requests full automation, run `/investigate-issue run` to automatically proceed through verification, specification, implementation, evaluation, and review.

## Investigation Strategy

> **Evidence-First Rule:** Capture before diagnosis. Never state a root cause without captured evidence from the failing command.

### Structured Capture Contract

Before any diagnosis, record these exact fields:

| Field | Description |
|---|---|
| Command | Exact shell command that failed |
| Cwd | Working directory at time of failure |
| Exit code | Numeric exit code |
| Stderr | Full stderr output |
| Traceback | Full stack trace (if applicable) |
| Diff | Relevant file diff from last known good state |

### Failure Classification Taxonomy

Classify the failure as exactly **one** of:

| Class | Description |
|---|---|
| `parser/metadata` | Frontmatter parsing, YAML/JSON syntax, metadata validation |
| `cwd/path resolution` | Wrong working directory, missing file, incorrect path |
| `missing artifact/precondition` | Required artifact (spec, verification, ledger) doesn't exist |
| `stale generated state` | Cache, `__pycache__`, generated files out of date |
| `contract mismatch` | Interface change without updating callers, API contract drift |
| `implementation defect` | Logic bug, off-by-one, race condition, wrong conditional |
| `environment/tooling` | Missing dependency, wrong interpreter, OS incompatibility |

### Historical Failure Comparison


### Evidence Framework

- **Observation**: Raw, factual data. MUST NOT contain interpretation.
- **Hypothesis (Competing)**: Plausible explanations with supporting/contradicting evidence.
- **Expectation**: What should happen based on spec or known behavior.
- **Difference**: Actual vs expected.
- **Interpretation**: Analysis of the difference, clearly separated from observation.
- **Conclusion**: Root cause, only if supported by conclusive evidence. Otherwise: UNKNOWN.

## Required Outputs

Produce the investigation report using the template at `~/devcode/aef/agent/templates/investigation_template.md`. Name the file `milestones/M{X}/M{X}S{Y}I{Z}.md`.

The report MUST include these sections:

- **Root Cause**: Specific code location or condition. "UNKNOWN" if inconclusive.
- **Evidence**: Captured fields from the Structured Capture Contract.
- **Fix Applied**: "none" or the exact change (file path + diff).
- **Verification Result**: Re-run exit code and output summary.
- **Prevention Recommendation**: How to prevent this failure class in the future.

- **Run**:
  - **Description**: Execute the complete SDD pipeline from investigation completion to review, with automation for steps that don't require user decisions.
  - **Process**:
  - **User intervention points**:
    - Investigation completion (if issues found)
    - Specification approval (via approve-spec skill)
  - **When to use**: Ideal for investigating and resolving issues found during development or testing. Provides end-to-end automation from investigation to implementation when scope is clear.
  - **Safety**: If investigation reveals multiple unrelated issues, scope creep, or design violations, the user can interrupt at any approval point or manually invoke investigate-issue again.

### Root Cause

Specific code location or condition causing the issue. "UNKNOWN" if evidence is insufficient.

### Evidence

Captured fields from the Structured Capture Contract: command, cwd, exit code, stderr, traceback, diff.

### Fix Applied

- "none" — if no fix was automatically applied (deferred to SDD pipeline)
- Exact change — file path, diff, and rationale if auto-fix was applied

### Verification Result

- Re-run exit code
- Output summary
- Pass/fail status

### Prevention Recommendation

How to avoid this failure class in the future. What tooling, validation, or process change would catch it earlier.

## Completion Criteria

Investigation is complete when:

   - Run `/investigate-issue run` for SDD automation, OR
   - Invoke `/generate-spec` manually, OR
   - Invoke `/investigate-issue` again.

## Rationale & Identifier Rules (CRITICAL)

Your investigation report may recommend creating new specifications to address the issue. However:

   derived_from: [INV-{N}]
   supersedes: [SPEC-{Y}]

## Out of Scope (Negative Guardrails)

- **Strict Sequence Target Lock:** You are strictly prohibited from evaluating error logs, stack traces, or failures from previous milestone sequences during an active investigation. You MUST parse ONLY the evaluation report (`M{X}S{Y}E.md`) or review report (`M{X}S{Y}R.md`) that explicitly matches the active sequence `{Y}` under investigation.

### Auto-Fix Rules

This skill MAY apply automatic fixes ONLY when ALL conditions are met:


When conditions are met:
- Apply the fix without creating a new specification/implementation cycle.
- Document the fix in the investigation report under "Fix Applied."
- Re-run the failing command to verify.

When conditions are NOT met:
- Do NOT modify source code.
- Defer to the SDD pipeline (Run → generate-spec → implement-specification).

This skill NEVER:
- Rewrites documentation
- Performs Git operations (beyond local `git checkout` for reversal)
- Generates reviews
- Archives milestones
- Overwrites existing investigation reports

## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
