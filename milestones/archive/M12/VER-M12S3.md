---
id: VER-M12S3-1
type: verification
title: "Verification Protocol for M12S3"
milestone_id: M12
status: draft
derived_from:
  - M12.md
  - M12S3.md
template_version: 1.1.0
---

## Success Criteria

- Handoff contracts between `manage-roadmap`, `manage-development`, and `manage-docs` are explicitly documented.
- `manage-development` contains ops handoff points and trigger conditions for `manage-docs` and `sync-documentation`.
- `manage-docs` documents manual watch trigger procedure and cross-skill circulation notes.
- `operations-consolidation` artifact type is registered with required metadata schema and storage rule.
- End-to-end circulation validation completes with status `0` and records handoff boundary checks.
- Plugin copies for both skills are byte-identical to source skill files.

---

## Followup Reuse

### Reusable Items from Prior Verifications
- M12S2 verification patterns for skill file presence, directory structure, and artifact registration.
- M12S2 test approach for marker-based repo root resolution.

### New Verification Required
- Handoff contract presence in `manage-development` and `manage-docs`.
- End-to-end circulation validation report.
- Plugin byte-identity checks for both skills.

---

## Functional Validation

### VI-M12S3-1: Handoff Contracts Documented
- **Source Requirement**: `FR-HANDOFF_ROADMAP_TO_DEVELOPMENT`, `FR-HANDOFF_DEVELOPMENT_TO_DOCS`
- **Verification Method**: `DOCUMENT_CHECK`
- **Target**: `skills/manage-development/SKILL.md`, `skills/manage-docs/SKILL.md`
- **Preconditions**: Files exist
- **Input**: Read file contents
- **Expected Evidence**: Both files contain section markers for handoff contracts, trigger conditions, and recipient skills.
- **Failure Condition**: Missing section markers or recipient skill names.
- **Initial Failure Expectation**: N/A (documentation absence)
- **Post-Implementation Success Expectation**: Sections present with required content.

### VI-M12S3-2: Ops Handoff Points in Manage-Development
- **Source Requirement**: `FR-OPS_HANDOFF_POINTS_IN_MANAGE_DEVELOPMENT`
- **Verification Method**: `DOCUMENT_CHECK`
- **Target**: `skills/manage-development/SKILL.md`
- **Preconditions**: File exists
- **Input**: Read file contents
- **Expected Evidence**: File includes explicit ops handoff points for `manage-docs` and `sync-documentation` with trigger conditions and artifact format references.
- **Failure Condition**: Missing ops handoff section or incomplete trigger documentation.
- **Initial Failure Expectation**: N/A
- **Post-Implementation Success Expectation**: Section present with trigger conditions and artifact schema keys.

### VI-M12S3-3: Event-Driven Watch Trigger Specified
- **Source Requirement**: `FR-EVENT_DRIVEN_WATCH_TRIGGER`
- **Verification Method**: `DOCUMENT_CHECK`
- **Target**: `skills/manage-docs/SKILL.md`
- **Preconditions**: File exists
- **Input**: Read file contents
- **Expected Evidence**: File specifies manual trigger procedure, scan output format, and opt-in activation method. Auto-scan remains disabled by default.
- **Failure Condition**: Missing trigger procedure or auto-scan enabled by default.
- **Initial Failure Expectation**: N/A
- **Post-Implementation Success Expectation**: Trigger procedure documented with disabled-by-default semantics.

### VI-M12S3-4: Operations-Consolidation Artifact Registration
- **Source Requirement**: `FR-OPERATIONS_CONSOLIDATION_ARTIFACT`
- **Verification Method**: `INTEGRITY_TEST`
- **Target**: `core/artifacts/artifact_types.py`
- **Preconditions**: File exists
- **Input**: Read file contents
- **Expected Evidence**: `operations-consolidation` type registered with required metadata fields and storage rule expressed via the dataclass field `canonical_storage_location`.
- **Failure Condition**: Type missing or schema incomplete.
- **Initial Failure Expectation**: N/A
- **Post-Implementation Success Expectation**: Registry exposes type with schema and canonical storage location field.
### VI-M12S3-5: End-to-End Circulation Validation
- **Source Requirement**: `FR-END_TO_END_CIRCULATION_VALIDATION`
- **Verification Method**: `SCRIPT_EXECUTION`
- **Target**: Validation report artifact
- **Preconditions**: Existing milestone artifact from M9 or M10 available
- **Input**: Execute circulation validation script/command
- **Expected Evidence**: Validation report records each handoff boundary check; exit code `0`.
- **Failure Condition**: Missing boundary checks or non-zero exit code.
- **Initial Failure Expectation**: Exit code `127` or `1` (validation script missing or assertion failure).
- **Post-Implementation Success Expectation**: Exit code `0` with complete boundary report.

### VI-M12S3-6: Plugin Copy Byte-Identity
- **Source Requirement**: `NFR-SCOPE_BOUNDARY_DOCS_ONLY`
- **Verification Method**: `INTEGRITY_TEST`
- **Target**: Plugin copies of `manage-development` and `manage-docs` skill files
- **Preconditions**: Source and plugin files exist
- **Input**: Compare byte content
- **Expected Evidence**: Plugin copies are byte-identical to source skill files.
- **Failure Condition**: Content mismatch.
- **Initial Failure Expectation**: N/A
- **Post-Implementation Success Expectation**: Byte-identical confirmation.

---

## Edge Cases

- Missing or incomplete handoff section markers in skill files.
- Plugin copy path resolution failure on non-standard installations.
- Circulation validation with malformed existing milestone artifacts.

---

## Failure Scenarios

- `skills/manage-development/SKILL.md` missing ops handoff section.
- `skills/manage-docs/SKILL.md` missing manual trigger procedure.
- `operations-consolidation` type not registered or schema incomplete.
- End-to-end circulation validation exits non-zero due to missing boundary checks.
- Plugin copies not synchronized with source files.

---

## Regression Checklist

- M12S2 skill validation still passes.
- M12S2 docs queue structure intact.
- M12S2 artifact registration intact.
- M12S2 folder governance rules intact.

---

## Manual Validation

1. Review `skills/manage-development/SKILL.md` for ops handoff section presence and completeness.
2. Review `skills/manage-docs/SKILL.md` for handoff contracts and watch trigger documentation.
3. Inspect `core/artifacts/artifact_types.py` for `operations-consolidation` registration.
4. Inspect end-to-end circulation validation report for boundary coverage.

---

## Automated Validation

### Diff-Scope Verification (Pre-Merge Check)

This mechanical check must be executed by `evaluate-implementation` before tests are considered passed.

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the "Allowlist" defined in the Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

---

## Expected Outcomes

Observable success:
- Handoff contracts are explicitly documented in both skill files.
- `manage-development` includes ops handoff points with trigger conditions.
- `manage-docs` documents manual watch trigger and cross-skill circulation.
- `operations-consolidation` artifact type is registered with schema and storage rule.
- End-to-end circulation validation exits `0` and records boundary checks.
- Plugin copies are byte-identical to source files.
