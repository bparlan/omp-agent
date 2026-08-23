## Deliverable Summary

### Files Modified

**1. `skills/evaluate-implementation/templates/evaluation_template.md`** — Rewrote `## Raw Evidence` section from a one-line placeholder to a full specification requiring:

- Every claim backed by exact command + exit code + stdout + stderr
- Mandatory format with `[claim:]` / `$ command` / `Exit Code:` / `stdout:` / `stderr:` blocks
- Manual/visual checks must state _why_ automation wasn't possible
- Constraint: summary counters with zero populated evidence blocks = EVIDENCE_GAP

**2. `skills/implement-specification/templates/completion_template.md`** — Added `## Raw Evidence` section with identical requirements. The completion template previously had no evidence requirement at all — just placeholder prose sections.

### Files Created

**3. `bin/lint-evaluation-gate.py`** — Mechanical (regex-based, no LLM) lint check running two independent checks:

| Check              | Pattern                                                                                                                                                                                                                                  | Exit code |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| EVIDENCE_GAP       | Counter patterns (`TESTS_RUN=N`, `EXIT_CODE=N`, etc.) present BUT zero raw evidence blocks (`[claim:`, `$ `, `raw_evidence:`, populated `- [x]` checklist, stdout/stderr capture)                                                        | 1         |
| SELF_CONTRADICTION | Resolution language (`✅ COMPLETE`, `Exit Code: 0`, `RESOLVED`, etc.) co-occurs with pending language (`⚠️ BLOCKED`, `⚠️ PENDING`, `TEST_VALIDATION_BLOCKED`, etc.) without a qualifying scope statement (`scope:`, `applies to:`, etc.) | 1         |

Exit code 0 = pass, 1 = findings, 2 = file error.

**4. `docs/remediation/wiring_recommendation_evidence_gate.md`** — Analysis of pre-commit vs on-demand tradeoff. Recommendation: **on-demand standalone script** (no pre-commit infra exists yet; existing validation scripts like `validate_metadata.py` are also on-demand), with CI integration as the short-term next step.

### Smoke Test Results (all passing)

| Scenario                              | Expected                | Actual   |
| ------------------------------------- | ----------------------- | -------- |
| Empty counters (M18S3E.md shape)      | EVIDENCE_GAP            | ✓ exit 1 |
| COMPLETE + BLOCKED (M18S1E.md shape)  | SELF_CONTRADICTION      | ✓ exit 1 |
| Counters + populated evidence blocks  | pass                    | ✓ exit 0 |
| COMPLETE + BLOCKED + scope qualifier  | pass                    | ✓ exit 0 |
| BLOCKED only, no resolution           | pass                    | ✓ exit 0 |
| COMPLETE only, no BLOCKED             | pass                    | ✓ exit 0 |
| Counters+evidence+contradiction mixed | only SELF_CONTRADICTION | ✓ exit 1 |
