Now I'll compile the analysis based on evidence gathered:

---

# Proposed Type Resolution Analysis

## 1. Current Type Landscape

**Valid types in `validate_metadata.py`:**

- `specification` (24 files)
- `verification` (19 files)

**All unique types currently in use (18 total):**

- specification, verification, test_set, evaluation, completion, review, hotfix, milestone, investigation, test_ledger, test_evaluation, session_audit, audit, architecture, Verification Item, Functional Requirement, evaluation-report, not_a_valid_type

## 2. Non-Conforming Types from Audit

| type              | count | files                                                              | evidence                                             |
| ----------------- | ----- | ------------------------------------------------------------------ | ---------------------------------------------------- |
| investigation     | 4     | report_audit.md, M10S5I1.md, M10S1I1.md, investigation_template.md | `INV-001`, `INV-M10S5I1` IDs in use                  |
| evaluation-report | 1     | M10S6E.md                                                          | `EVAL-M10S6E` ID                                     |
| test_ledger       | 1     | M10S9T1.md                                                         | `VER-M10S9T1` ID (misleading prefix)                 |
| session_audit     | 1     | M10SA1.md                                                          | `M10SA1` ID                                          |
| completion_report | 0     | —                                                                  | Historical only (M8S2C.md no longer exists)          |
| findings          | 0     | —                                                                  | Historical only (M18S1_FINDINGS.md no longer exists) |
| report            | 0     | —                                                                  | Historical only (M18S3T1-REPORT.md no longer exists) |

**Note:** `audit` type (used in report_audit.md) is also non-conforming but not part of AUDIT-001's flagged set.

## 3. Classification & Resolution Strategy

### 3.1. `investigation` → **EXISTING TYPE**

- **Evidence:** Used by `investigate-issue` skill with its own template, consistently uses `INV-*` prefix across 3 files.
- **Classification:** Genuine artifact class, not a typo. Represents child artifacts that derive from evaluation reports to investigate specific failures.
- **Resolution:** **Keep as-is** (type = `investigation`, prefix = `INV-*`).

### 3.2. `evaluation-report` → **Collapse into `evaluation`**

- **Evidence:** 1 file (M10S6E.md) using this variant. `evaluate-implementation` skill uses `evaluation` type (confirmed by template listing).
- **Classification:** Drift/typo (en dash instead of space, or misremembered from earlier schema).
- **Resolution:** Rename to `evaluation` (canonical spelling).

### 3.3. `test_ledger` → **Collapse into `test_set`**

- **Evidence:** 1 file (M10S9T1.md) using this variant. `generate-tests` skill uses `test_set` type.
- **Classification:** Drift/typo (ledder instead of set). Note ID `VER-M10S9T1` is also incorrect; should be `TS-M10S9T1` or similar.
- **Resolution:** Rename to `test_set`.

### 3.4. `session_audit` → **ADD to valid_types**

- **Evidence:** 1 file (M10SA1.md) uses this type. No skill template currently exists for it.
- **Classification:** Distinct artifact class (session-level retrospective report). Appears in M10SA1, potentially in other projects.
- **Resolution:** **Add to `valid_types`** in `validate_metadata.py` and add a skill/template for it (recommended, but not blocking for now).

### 3.5. `completion_report` → **Already collapsed**

- **Evidence:** Audit flagged it, but file no longer exists. Current canonical type is `completion` (used by `implement-specification` skill).
- **Resolution:** No action needed (already resolved historically).

### 3.6. `findings` → **Already collapsed**

- **Evidence:** Audit flagged it, but file no longer exists. M18S1_FINDINGS.md referenced in audit is gone.
- **Resolution:** No action needed.

### 3.7. `report` → **Already collapsed**

- **Evidence:** Audit flagged it, but file no longer exists.
- **Resolution:** No action needed.

## 4. I-Prefix Collision Resolution

**Analysis:**

- `investigation` uses `INV-*` prefix (confirmed by M10S1I1: `INV-001`, M10S5I1: `INV-M10S5I1`, template: `INV-{N}`).
- `implementation` does **not** appear as a type. The implementation phase is represented by:
  - `completion` (prefix `COMP-*`)
  - `evaluation` (prefix `EVAL-*`)
  - `review` (prefix `REV-*` or `REVIEW-*`)

**Conclusion:** No collision exists because `implementation` is not a type. The `I`-prefix is solely used by `investigation`.

**Proposal:** Keep `investigation` type with `INV-*` prefix. No rename required.

## 5. Proposed Canonical Type Table

| type                   | id_prefix                      | status                          | justification                                                              |
| ---------------------- | ------------------------------ | ------------------------------- | -------------------------------------------------------------------------- |
| specification          | SPEC-\*                        | existing                        | Used by `generate-spec`, confirmed in 24 files                             |
| verification           | VER-_ or V-_                   | existing                        | Used by `generate-verification`, confirmed in 19 files                     |
| test_set               | TS-_ or T-_                    | existing                        | Used by `generate-tests`, confirmed in 14 files                            |
| evaluation             | EVAL-\*                        | existing                        | Used by `evaluate-implementation` skill                                    |
| completion             | COMP-\*                        | existing                        | Used by `implement-specification` skill                                    |
| review                 | REV-_ or REVIEW-_              | existing                        | Used by `review-implementation` skill                                      |
| hotfix                 | HF-\*                          | existing                        | Used by `hotfix-focus` skill                                               |
| milestone              | M{X}-S{Y}-_ or M{X}S{Y}_       | existing                        | Used by `milestone` skill                                                  |
| investigation          | INV-\*                         | existing                        | Used by `investigate-issue` skill, confirmed 4 files                       |
| session_audit          | M{X}SA\* or SA-{N}             | **to-add**                      | 1 file used (M10SA1), no skill yet. Recommended: add skill/template.       |
| audit                  | AUD-{N} or A-{N}               | **to-add**                      | Used in report_audit.md (self-referential), but not part of core pipeline. |
| architecture           | ARC-\*                         | **to-add**                      | 1 file used (docs/ARTIFACT_ARCHITECTURE.md). Low-frequency.                |
| Functional Requirement | FR-{N}                         | **to-add**                      | Synthetic fixture only.                                                    |
| Verification Item      | VI-{N}                         | **to-add**                      | Synthetic fixture only.                                                    |
| test_evaluation        | TE-{N}                         | **to-collapse-into** `test_set` | Appears in synthetic fixtures only.                                        |
| evaluation-report      | **collapse into** `evaluation` | **to-collapse**                 | Mis-spelled/variant of `evaluation`.                                       |
| test_ledger            | **collapse into** `test_set`   | **to-collapse**                 | Mis-spelled/variant of `test_set`.                                         |
| not_a_valid_type       | —                              | **remove**                      | Invalid test fixture entry.                                                |

## 6. Files Requiring Type Field Changes (by old→new type)

| old_type                        | new_type   | affected_files            |
| ------------------------------- | ---------- | ------------------------- |
| evaluation-report               | evaluation | milestones/M10/M10S6E.md  |
| test_ledger                     | test_set   | milestones/M10/M10S9T1.md |
| (historical: completion_report) | completion | —                         |
| (historical: findings)          | —          | —                         |
| (historical: report)            | —          | —                         |

**Note:** `investigation` and `session_audit` do NOT require changes; they are correctly classified (investigation) or need validation support (session_audit, not renaming).

---

### Summary

**Immediate actions (Prompt 4):**

1. Rename `evaluation-report` → `evaluation` in M10S6E.md.
2. Rename `test_ledger` → `test_set` in M10S9T1.md.
3. Optionally add `session_audit` to `validate_metadata.py` valid_types (recommended but not blocking).
4. No action needed for `investigation` (I-prefix collision resolved; it's correctly `INV-*`).
5. Clean up synthetic fixtures: remove `not_a_valid_type`, `test_evaluation`, and ensure `Functional Requirement` and `Verification Item` use FR-{N} and VI-{N} prefixes.
