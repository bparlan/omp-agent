---
id: WORKED-EXAMPLE-M18S3E
type: worked_example
description: "Structured Findings block for M18S3E.md, reconstructed from AUDIT-001 evidence (no re-execution)"
derived_from: [AUDIT-001]
template_version: 1.0.0
---

# Worked Example: M18S3E.md Structured Findings Block

**Source evidence:** AUDIT-001 §C.1, §D.2, §E.1, §E.3.

**Original M18S3E.md content (6 lines):**
```
TESTS_RUN=2
TESTS_PASSED=2
TESTS_FAILED=0
VALID_TESTS=0
INVALID_TESTS=0
EXIT_CODE=0
```

**Reconstructed Structured Findings block** (as the new template would generate it):

```yaml
## Structured Findings

findings:
  - id: F-1
    category: EVIDENCE_GAP
    severity: HIGH
    affected_files:
      - milestones/M18/M18S3E.md
    classification: process_failure
    raw_evidence: |
      File content is only 6 summary counters with no command traces:
        TESTS_RUN=2
        TESTS_PASSED=2
        TESTS_FAILED=0
        VALID_TESTS=0
        INVALID_TESTS=0
        EXIT_CODE=0
      No raw stdout, no stderr, no command invocation trace, no environment
      variables, no server startup log. The claim TESTS_RUN=2 / TESTS_PASSED=2
      cannot be independently verified because the commands that produced these
      values are not recorded.

  - id: F-2
    category: EVIDENCE_GAP
    severity: MEDIUM
    affected_files:
      - milestones/M18/M18S3E.md
    classification: process_failure
    raw_evidence: |
      VALID_TESTS=0 and INVALID_TESTS=0 but TESTS_RUN=2. The validity gate
      results are absent — it is unknown whether the 2 executed tests were
      validated or not. This is a structural gap in the evaluation report:
      the validity gate (which classifies each test as VALID_TEST or
      INVALID_TEST) was not recorded, making it impossible to determine
      whether the EXIT_CODE=0 claim is trustworthy.

  - id: F-3
    category: INACCURATE_DOCUMENTATION
    severity: HIGH
    affected_files:
      - milestones/M18/M18S3E.md
    classification: process_failure
    raw_evidence: |
      EXIT_CODE=0 claims all tests passed, but:
      (a) VALID_TESTS=0 and INVALID_TESTS=0 means no test was classified
          through the validity gate. A test run with zero validated tests
          cannot certify correctness.
      (b) AUDIT-001 §D.2 attempted to reproduce the test run and concluded
          "COULD NOT VERIFY — reason: No raw command output in the artifact."
      The EXIT_CODE=0 claim is unsupported and may be inaccurate.
```

---

## Analysis

**3 findings identified** from a 6-line file (all from the same artifact):

| Finding | Category | Classification | Severity | Notes |
|---|---|---|---|---|
| F-1 | EVIDENCE_GAP | process_failure | HIGH | No raw command traces at all |
| F-2 | EVIDENCE_GAP | process_failure | MEDIUM | Validity gate results absent |
| F-3 | INACCURATE_DOCUMENTATION | process_failure | HIGH | EXIT_CODE=0 claim unsupported |

**Routing decisions (per classification):**

- F-1, F-2, F-3 are all `process_failure` → route to **stricter human review gate**. No automated code fix is possible; the report must be regenerated with actual command traces.
- The absence of any `mechanically_auto_fixable` or `judgment_required` findings is itself a signal: the evaluation report is fundamentally empty of executably testable claims.

**Without the structured block**, a reader or automated pipeline sees 6 lines of counters and must manually decide whether this is "done" (TESTS_PASSED=2 says yes) or "blocked" (no evidence says no). **With the structured block**, the taxonomy immediately routes all findings to `process_failure` — the pipeline knows to reject the report and require regeneration, without needing to interpret prose.