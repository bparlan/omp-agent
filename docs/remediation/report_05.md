## Deliverable Summary

### Files Modified

**1. `skills/evaluate-implementation/SKILL.md`** — Added `#### Structured Findings (Machine-parseable taxonomy block)` subsection in Section 3. Instructs the evaluator agent to emit a YAML findings block with category, severity, affected_files, classification, and raw_evidence per finding. Also specifies when to self-report `EVIDENCE_GAP` (missing command traces), when to route `TEST_VALIDATION_BLOCKED` vs `INACCURATE_DOCUMENTATION`, and to emit `findings: []` when clean.

**2. `skills/evaluate-implementation/templates/evaluation_template.md`** — Appended `## Structured Findings` section with:

- YAML block template showing the exact schema
- Category definitions table (6 categories)
- Classification meanings table
- Constraints (raw_evidence non-empty, category restricted to 6, explicit empty list)

### Files Created (Worked Examples)

**3. `docs/remediation/example_M18S1E_structured_block.md`** — 5 findings reconstructed from AUDIT-001 evidence: F-1 (INACCURATE_DOCUMENTATION, CRITICAL — COMPLETE + Exit Code: 1 + BLOCKED contradiction), F-2 (EVIDENCE_GAP, HIGH), F-3 (INACCURATE_DOCUMENTATION, HIGH — claimed pass vs actual exit code 127), F-4 (ARCHITECTURE_AMBIGUITY, HIGH — wrong server entry point), F-5 (OTHER, MEDIUM — hardcoded HTML vs React deviation). With routing analysis showing 3 `process_failure` → stricter review gate, 2 `judgment_required` → architectural review.

**4. `docs/remediation/example_M18S3E_structured_block.md`** — 3 findings from a 6-line file: F-1 (EVIDENCE_GAP, HIGH — no command traces), F-2 (EVIDENCE_GAP, MEDIUM — validity gate absent), F-3 (INACCURATE_DOCUMENTATION, HIGH — EXIT_CODE=0 unsupported). All `process_failure` → pipeline rejects the report, requires regeneration.

### Routing Decision

This IS the AEF framework repo (`bparlan/omp-agent`), not a project-level copy. The skills directory is the canonical shared AEF core. Edits applied directly — no indirection needed.
