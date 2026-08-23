---
id: EVAL-{N}  # Sequential integer matching the evaluation run
type: evaluation
title: Evaluation Report for M{X}S{Y}
milestone_id: M{X}
status: completed
derived_from: [SPEC-{Y}, VER-{Y}]
template_version: 1.0.2
---

## Test Execution Summary

---

## Validity Gate Results

- **VALID_TESTS:** <count>
- **INVALID_TESTS:** <count>

### Invalidation Reports (if any)

| Test File | Violated Criterion | Raw Evidence              | Recommended Repair |
| --------- | ------------------ | ------------------------- | ------------------ |
| <path>    | <criterion>        | <exit_code+stdout+stderr> | <repair action>    |

---

## Passed Tests

---

## Failed Tests

---

## Bugs Auto-Resolved

---

## Remaining Structural Failures

---

## Next Steps

---

## Raw Evidence

Every "done" claim in this report MUST be backed by the exact command that
produced it and its captured output. This section is the evidence floor — no
summary counter is accepted without the corresponding raw trace below.

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

- **EVERY** summary counter (`TESTS_RUN=N`, `TESTS_PASSED=N`, `EXIT_CODE=N`,
  `TESTS_FAILED=N`) MUST have at least one corresponding raw evidence block
  in this section. A report with counters but no populated evidence blocks
  fails the evidence-floor gate.
- A manual/visual check MUST state _why_ automation wasn't possible — not
  just "N/A" or empty. A silently empty evidence field is an `EVIDENCE_GAP`
  finding.
- This section is additive to the `## Structured Findings` block — both
  must be populated. The structured block provides machine-parseable routing;
  this section provides the human-readable raw traces.

## Structured Findings

Machine-parseable findings block for automated routing. Each finding maps to one
category from the validated taxonomy (AUDIT-001 §E.4). Populated by the
evaluator agent during report generation.

Format: YAML block (consistent with YAML frontmatter convention).

```yaml
findings:
  - id: F-1
    category: ARCHITECTURE_AMBIGUITY  # ARCHITECTURE_AMBIGUITY | INVALID_TEST | INACCURATE_DOCUMENTATION | EVIDENCE_GAP | TEST_VALIDATION_BLOCKED | OTHER
    severity: HIGH                     # CRITICAL | HIGH | MEDIUM | LOW
    affected_files:
      - path/to/affected_file.py
    classification: judgment_required  # mechanically_auto_fixable | judgment_required | process_failure
    raw_evidence: |                    # Non-empty. Exact command, stdout, stderr, exit code, or file excerpt.
      <exact command output or file excerpt proving the finding>
```

### Category Definitions

| Category | Meaning | Typical classification |
|-------------------------------|-----------------------------------------------------------------|-------------------------|
| `ARCHITECTURE_AMBIGUITY` | Conflicting or unclear architectural boundaries (e.g., duplicate endpoints, wrong entry point) | judgment_required |
| `INVALID_TEST` | Test script has syntax errors, bad shebang, or defective logic | mechanically_auto_fixable |
| `INACCURATE_DOCUMENTATION` | Report or claim contradicts actual state (e.g., claims PASS when tests failed) | process_failure |
| `EVIDENCE_GAP` | Raw command output missing; claims unsupported by captured evidence | process_failure |
| `TEST_VALIDATION_BLOCKED` | Test could not execute due to missing runtime dependency (e.g., server not running) | mechanically_auto_fixable |
| `OTHER` | Open-ended category for findings not covered above | — |

### Classification Meanings

- `mechanically_auto_fixable`: Deterministic fix (syntax patch, start server). Route to automated fix script.
- `judgment_required`: Requires architectural or scope decision. Route to review gate.
- `process_failure`: Report/evidence quality problem. Route to stricter human review gate; cannot be fixed by code patch alone.

### Constraints

- `raw_evidence` MUST be non-empty. A finding with empty evidence is invalid and MUST be recorded as a separate `EVIDENCE_GAP` finding (or attached to the parent finding if the parent is the gap itself).
- `category` MUST be one of the 6 defined values. Custom subcategories go in `OTHER` with differentiating prose in `raw_evidence`.
- If no findings were identified, populate `findings: []` explicitly (empty list).
- This block is machine-parseable — the prose narrative above it remains the primary human-readable section.
