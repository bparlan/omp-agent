---
id: WORKED-EXAMPLE-M18S1E
type: worked_example
description: "Structured Findings block for M18S1E.md, reconstructed from AUDIT-001 evidence (no re-execution)"
derived_from: [AUDIT-001]
template_version: 1.0.0
---

# Worked Example: M18S1E.md Structured Findings Block

**Source evidence:** AUDIT-001 §B.4, §D.5, §E.1, §E.3.

**Original M18S1E.md content summary (per AUDIT-001):**

- Lines 23, 54, 70, 85: `**Exit Code:** 1` (multiple test failures)
- Line 241: `**Implementation Status:** ✅ COMPLETE`
- Line 243: `**Test Execution Status:** ⚠️ BLOCKED (No server running)`
- The file has exit codes recorded but no full stdout/stderr command traces
- M18S1_REVIEW.md (cross-reference) identifies: hardcoded HTML vs React spec deviation, architecture ambiguity (wrong server entry point), and claims tests passed when actual exit code was 127 (missing `curl`)

**Reconstructed Structured Findings block** (as the new template would generate it):

```yaml
## Structured Findings

findings:
  - id: F-1
    category: INACCURATE_DOCUMENTATION
    severity: CRITICAL
    affected_files:
      - milestones/M18/M18S1E.md
    classification: process_failure
    raw_evidence: |
      Line 241: "**Implementation Status:** ✅ COMPLETE"
      Line 243: "**Test Execution Status:** ⚠️ BLOCKED (No server running)"
      Lines 23, 54, 70, 85: "**Exit Code:** 1" (multiple test failures)
      The report simultaneously asserts COMPLETE, BLOCKED, and Exit Code: 1.
      These three states are mutually exclusive:
      - Exit Code: 1 means test failures exist
      - BLOCKED means the tests could not fully execute
      - COMPLETE means the milestone is finished
      A milestone with unresolved test failures (Exit Code: 1) and a blocked
      execution environment cannot be COMPLETE.

  - id: F-2
    category: EVIDENCE_GAP
    severity: HIGH
    affected_files:
      - milestones/M18/M18S1E.md
    classification: process_failure
    raw_evidence: |
      Exit codes are recorded (Exit Code: 1 at lines 23, 54, 70, 85) but no
      raw stdout or stderr from any test execution is captured. The file
      contains prose summaries without the command invocations that produced
      them. AUDIT-001 §E.3 confirms: "findings are embedded in prose paragraphs
      rather than tagged with category | severity | affected_file(s)."

  - id: F-3
    category: INACCURATE_DOCUMENTATION
    severity: HIGH
    affected_files:
      - milestones/M18/M18S1E.md
      - tests/M18/test_health_endpoint.sh  (cross-reference from M18S1_REVIEW.md)
    classification: process_failure
    raw_evidence: |
      M18S1_REVIEW.md (cross-referenced audit finding) reports that the
      evaluation claims tests passed, but actual execution shows exit code 127
      (command not found: curl). The evaluation report's claim of test results
      is inconsistent with the ground-truth execution. This is documented in
      AUDIT-001 §E.1: "Evaluation claims tests passed; actual execution shows
      exit code 127 (missing curl)."

  - id: F-4
    category: ARCHITECTURE_AMBIGUITY
    severity: HIGH
    affected_files:
      - src/autonomedia/web/server.py  (claimed entry point)
      - src/web/app.py                 (actual entry point)
    classification: judgment_required
    raw_evidence: |
      M18S1_REVIEW.md identifies that the main application entry point is
      src/web/app.py, but the evaluation and specification reference
      src/autonomedia/web/server.py. These are different files. AUDIT-001 §E.1
      records: "ARCHITECTURE_AMBIGUITY: Main application is src/web/app.py,
      not src/autonomedia/web/server.py."

  - id: F-5
    category: OTHER
    severity: MEDIUM
    affected_files:
      - milestones/M18/M18S1E.md
    classification: judgment_required
    raw_evidence: |
      M18S1_REVIEW.md reports that the implementation uses hardcoded HTML
      instead of the specified React component. This is a scope/architecture
      deviation that affects the evaluation's completeness assessment but does
      not fit neatly into the existing taxonomy categories. Using OTHER with
      this descriptive evidence to capture it without forcing a category.
```

---

## Analysis

**5 findings identified**, spanning 3 categories + OTHER:

| Finding | Category | Classification | Severity | Notes |
|---|---|---|---|---|
| F-1 | INACCURATE_DOCUMENTATION | process_failure | CRITICAL | COMPLETE + Exit Code: 1 + BLOCKED contradiction |
| F-2 | EVIDENCE_GAP | process_failure | HIGH | No raw command traces |
| F-3 | INACCURATE_DOCUMENTATION | process_failure | HIGH | Test claims vs actual exit code 127 |
| F-4 | ARCHITECTURE_AMBIGUITY | judgment_required | HIGH | Wrong entry point |
| F-5 | OTHER | judgment_required | MEDIUM | Hardcoded HTML vs React deviation |

**Routing decisions (per classification):**

- F-1, F-2, F-3 are `process_failure` → route to **stricter human review gate**. The report cannot be trusted as-is.
- F-4, F-5 are `judgment_required` → route to **architectural review**. Someone must decide which entry point is correct and whether to accept hardcoded HTML or require a React implementation.

**Without the structured block**, a reader sees "✅ COMPLETE" at line 241 and may accept the milestone as finished. The contradictions and evidence gaps are buried in prose 200 lines earlier. **With the structured block**, the taxonomy immediately flags 3 `process_failure` findings and 2 `judgment_required` findings — the pipeline knows to block acceptance and route to human review, without needing to interpret the narrative.