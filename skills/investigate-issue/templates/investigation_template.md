---
id: INV-{N}
type: investigation
title: Investigation Report for Issue {Z}
milestone_id: M{X}
status: completed
derived_from: [EVAL-{N}]
template_version: 2.0.0
---

## Root Cause

{Specific code location or condition. "UNKNOWN" if inconclusive.}

---

## Evidence

### Capture Contract

| Field | Value |
|---|---|
| Command | |
| Cwd | |
| Exit code | |
| Stderr | |
| Traceback | |
| Diff | |

### Failure Classification

Class: {one of: parser/metadata, cwd/path resolution, missing artifact/precondition, stale generated state, contract mismatch, implementation defect, environment/tooling}

### Historical Comparison

{Cross-reference to prior investigation reports of same class, or "none found."}

---

## Fix Applied

{ "none" — deferred to SDD pipeline | Exact change with file path and diff. }

---

## Verification Result

- Re-run exit code:
- Output summary:
- Status: {PASS / FAIL}

---

## Prevention Recommendation

{How to prevent this failure class in the future. Tooling, validation, or process change.}
