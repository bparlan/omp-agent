---
id: CLOSE-M{X}-{N}
type: closure
title: "Milestone Closure Report for M{X}"
milestone_id: M{X}
status: CLOSED  # or CLOSED_WITH_DEFECTS | REFUSED
derived_from:
  - M{X}
  - SPEC-M{X}S{Y}
  - VER-M{X}S{Y}V
  - TSET-M{X}S{Y}T{Z}
  - EVAL-{N_EVAL}
  - REVIEW-M{X}S{Y}
  # If fix cycle occurred:
  # - INV-{N_INV}
  # - HOT-{N_HOT}
  # - EVAL-{N_RE_EVAL}
  # - REVIEW-M{X}S{Y}-V{N_REVIEW}
supersedes: []  # e.g., [CLOSE-M{X}-{N_PREVIOUS}] if this replaces an earlier closure
template_version: 1.0.0
---

# Milestone Closure Report — M{X}

**Closure ID:** CLOSE-M{X}-{N}
**Status:** CLOSED | CLOSED_WITH_DEFECTS | REFUSED
**Date:** {YYYY-MM-DD}

---

## 1. Loop-Closure Assurance

### Investigation / Hotfix Detection

```
[evidence: list of investigation and hotfix reports found, or "none"]
```

### Post-Fix Re-Evaluation Evidence

```
[evidence: evaluation report filename and timestamp after the latest hotfix, or "none required — no fixes occurred"]
```

### Post-Fix Re-Review Evidence

```
[evidence: review report filename and timestamp after the latest evaluation, or "none required — no fixes occurred"]
```

### Assurance Statement

> **This milestone has no unverified fixes.** Every fix applied through investigation/hotfix was re-evaluated by `evaluate-implementation` and re-reviewed by `review-implementation` before closure.
>
> OR
>
> **No fixes were applied during this milestone.** The standard spec → verification → tests → implementation → evaluation → review pipeline completed without deviation.

---

## 2. Mechanical Validation Results

### 2a. Lint Evaluation Gate

```
[command: python3 bin/lint-evaluation-gate.py --milestone M{X}]
[exit code: N]
[stdout: captured output or "(empty)"]
[stderr: captured output or "(empty)"]
```

### 2b. Duplicate-ID / Schema Check

```
[command: python3 -c "....."]
[exit code: N]
[output: captured output or "(empty)"]
```

### 2c. Artifact Completeness Check

```
[command: python3 -c "....."]
[exit code: N]
[output: captured output or "(empty)"]
```

### Findings Summary

| Check | Status | Finding |
|---|---|---|
| Lint Evaluation Gate | ✅ PASS / ⚠️ WARN / ❌ FAIL | Brief description |
| Duplicate-ID / Schema | ✅ PASS / ⚠️ WARN / ❌ FAIL | Brief description |
| Artifact Completeness | ✅ PASS / ⚠️ WARN / ❌ FAIL | Brief description |

---

## 3. Lineage Chain (DAG)

Full artifact DAG for this milestone, traced from the closure artifact backward through every `derived_from` edge.

### Artifacts by Spec Sequence

```
M{X}/  (Milestone)
│
├── M{X}S{Y}.md              — SPEC-{Y}  (specification)
│   └── M{X}S{Y}V.md         — VER-{Y}   (verification)
│       └── M{X}S{Y}T{Z}.md  — TSET-{Y}  (test plan)
│           └── M{X}S{Y}TE.md     — EVAL-TEST-{N}  (test evaluation)
│               └── M{X}S{Y}C.md  — COMP-{N}  (implementation)
│                   └── M{X}S{Y}E.md  — EVAL-{N}  (evaluation)
│                       └── M{X}S{Y}R.md  — REVIEW-M{X}S{Y}  (review)
│                           └── (fix cycle, if applicable)
│                               ├── M{X}S{Y}I{Z}.md  — INV-{N}  (investigation)
│                               ├── M{X}H{Z}.md       — HOT-{N}  (hotfix)
│                               ├── M{X}S{Y}E-V{N}.md — EVAL-{N}  (re-evaluation)
│                               └── M{X}S{Y}R-V{N}.md — REVIEW-M{X}S{Y}-V{N}  (re-review)
│
└── M{X}CLOSE-{N}.md         — CLOSE-M{X}-{N}  (closure)
```

### Full Artifact Table

| File | ID | Type | Status | derived_from | Filepath |
|---|---|---|---|---|---|
| (filename) | (id) | (type) | (status) | [sources] | (relative path) |

---

## 4. Status Assertion

**Milestone M{X} is [CLOSED | CLOSED_WITH_DEFECTS | REFUSED].**

- All specification requirements have been implemented, evaluated, and reviewed.
- [If CLOSED_WITH_DEFECTS]: The following known issues remain, but do not block closure: [list issues]
- [If REFUSED]: The loop-closure gate was not satisfied. See section 1 for details.

---

## 5. Raw Evidence

Every claim above is backed by the exact command that produced it and its captured output.

### Mandatory Format

```
[claim: <what this proves>]
$ <command>
Exit Code: <N>
stdout:
<captured stdout, or "(empty)">
stderr:
<captured stderr, or "(empty)">
```

### Constraints

- **EVERY** status assertion in section 2 and section 4 MUST have at least one corresponding raw evidence block in this section.
- A report with summary statements but no populated evidence blocks fails the evidence-floor gate.
- This section is additive to the structured findings above — both must be populated.