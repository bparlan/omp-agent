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

1. **Reproduce the failure** — Before any edits or source inspection, reproduce the exact failure. Run the failing command, test, or scenario in the exact context where it failed.

2. **Capture evidence** — Record: exact command, working directory, exit code, stderr, full traceback, and relevant file diff. This is the raw material for all diagnosis.

3. **Do not infer from source alone** — Source inspection comes after failure capture. Do not form conclusions from reading code without first observing runtime behavior.

4. **Inspect filesystem state** — Only after capturing the failing command, examine filesystem state: file contents, timestamps, expected artifacts, generated state.

5. **Classify the failure** — Choose exactly one category from the Failure Classification Taxonomy below.

6. **Compare against historical failures** — Use `glob` to find all `*I*.md` investigation reports in `milestones/`. Cross-reference by failure class. Check if this failure matches a known pattern.

7. **Apply automatic fix (if safe)** — If the fix is deterministic, local, reversible, and within this skill's tool allowlist, apply it automatically. Otherwise proceed through the SDD pipeline.

8. **Verify the fix** — Re-run the exact failing command from step 1. Report exit code and output.

9. **Report** — Investigation report with: root cause, evidence, fix applied (or "none"), verification result, prevention recommendation.

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

1. `glob` for investigation reports: `**/milestones/**/*I*.md`
2. Extract `type: investigation` files
3. Compare current failure class against previous investigations of same class
4. If a known fix exists, reference the prior report's prevention recommendation
5. If same failure class recurs across milestones, flag as systemic

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
    1. **Complete investigation** — Finish investigation report (steps 1-9 of your process).
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

1. Failure reproduced and captured.
2. Failure classified into exactly one taxonomy category.
3. Historical investigations checked for matching patterns.
4. Fix applied (auto-fix) or explicitly deferred to SDD pipeline.
5. Verification re-run confirms fix (or failure reproduced for SDD).
6. Investigation report `M{X}S{Y}I{Z}.md` written with all 5 required sections.
7. User can either:
   - Run `/investigate-issue run` for SDD automation, OR
   - Invoke `/generate-spec` manually, OR
   - Invoke `/investigate-issue` again.

## Rationale & Identifier Rules (CRITICAL)

Your investigation report may recommend creating new specifications to address the issue. However:

1. You are STRICKLY FORBIDDEN from prescribing or suggesting specification identifiers that contain semantic qualifiers, version numbers, or correction tags (e.g., do NOT recommend `SPEC-001-CORRECTED` or `M5S1I1-CORRECTED`).
2. You must instruct the downstream specification generator (`generate-spec`) to allocate a clean, sequential specification ID (e.g., `SPEC-002`).
3. The relationship to this investigation and the original specification must be documented purely in the new specification's metadata fields:
   derived_from: [INV-{N}]
   supersedes: [SPEC-{Y}]

## Out of Scope (Negative Guardrails)

- **Strict Sequence Target Lock:** You are strictly prohibited from evaluating error logs, stack traces, or failures from previous milestone sequences during an active investigation. You MUST parse ONLY the evaluation report (`M{X}S{Y}E.md`) or review report (`M{X}S{Y}R.md`) that explicitly matches the active sequence `{Y}` under investigation.

### Auto-Fix Rules

This skill MAY apply automatic fixes ONLY when ALL conditions are met:

1. **Deterministic** — The fix is clear from the evidence (e.g., typo, wrong path, missing import).
2. **Local** — The fix touches only one file, and the change is self-contained.
3. **Reversible** — The fix can be reverted with a single `git checkout`.
4. **Within allowlist** — The fix is within the tools declared in frontmatter.

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
