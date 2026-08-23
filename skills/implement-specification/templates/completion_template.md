---
id: COMP-000
type: completion
title: Template Completion Report
milestone_id: M0
status: draft
derived_from: []
template_version: 1.0.3
---

##### Completion Report: Implementation Details & Evidence

###### 1. Files Modified

_(List all physical files created or modified with their relative repository paths)_

###### 2. Tests Executed & Pre-Implementation State

_(Document the tests run, their exit codes, and how they validated the pre-implementation state)_

###### 3. Technical Changes Summary

_(A high-level description of code additions, refactorings, or modifications made)_

###### 4. Edge Cases Handled

_(Document how the implementation defends against edge cases and failure scenarios)_

###### 5. Identified Technical Debt

_(Record any shortcuts taken, temporary workarounds, or follow-up tasks required for maintainability)_

---

## Raw Evidence

Every claim in this report MUST be backed by the exact command that produced
it and its captured output. No summary statement is accepted without the
corresponding raw trace below.

### Mandatory Format

For every executable check, record:

- **Command:** the exact shell command invoked
- **Exit Code:** the numeric exit code
- **stdout:** captured standard output (or `(empty)` if none)
- **stderr:** captured standard error (or `(empty)` if none)

```text
[claim: <what this proves>]
$ <command>
Exit Code: <N>
stdout:
<captured stdout, or "(empty)">
stderr:
<captured stderr, or "(empty)">
```

### Manual / Visual Checks

If a claim cannot be backed by an automated command (e.g., visual inspection,
manual UI test), record:

```text
[claim: <what this proves>]
Check type: MANUAL
Why automated not possible: <specific reason>
Evidence: <observed result, screenshot reference, or inspector output>
```

### Constraints

- **EVERY** claim about test execution, file modification, or specification
  conformance MUST have at least one corresponding raw evidence block in this
  section. A report with prose claims but no populated evidence blocks fails
  the evidence-floor gate.
- A manual/visual check MUST state _why_ automation wasn't possible — not
  just "N/A" or empty. A silently empty evidence field is an `EVIDENCE_GAP`
  finding.
- This section is additive to the narrative above it — both must be populated.
