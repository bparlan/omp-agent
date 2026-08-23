```mermaid
flowchart LR
    subgraph Prompt2[Prompt 2 — Type Corrections]
        direction LR
        T1["M10S6E.md: evaluation-report → evaluation"]
        T2["M10S9T1.md: test_ledger → test_set"]
    end
    subgraph Prompt3[Prompt 3 — ID Renames]
        direction LR
        R1["COMP-001 (13 files) → aef:COMP-M*S* / baria:COMP-M8S1"]
        R2["EVAL-001 (4 files) → aef:EVAL-M*S*"]
        R3["EVAL-1 (6 files) → aef:EVAL-* / baria:EVAL-* / autonomedia:EVAL-*"]
        R4["TEVAL-1 (6 files) → *:TEVAL-*"]
        R5["REVIEW-001 (4) + REVIEW-1 (2) → aef:REVIEW-*"]
        R6["SPEC-001 (2) + VER-001 (2) → aef:SPEC-* / aef:VER-*"]
    end
    subgraph Derived[derived_from Updates]
        D1["M7S2R, M7S3R → aef:EVAL-M7S2/S3"]
        D2["M10S1I1 → aef:EVAL-M10S1"]
        D3["M10S1C → aef:SPEC-M10S1"]
        D4["M10S1E → aef:SPEC-M10S1, aef:VER-M10S1"]
        D5["M10S1R → aef:SPEC-M10S1"]
        D6["M10S5R → aef:COMP-M10S5 (EVAL-001 preserved #ND)"]
    end
```

## Migration Report

### 1. Pre-Migration Snapshots (fully revertible)

| Repo                                                        | Snapshot Commit | Notes                                    |
| ----------------------------------------------------------- | --------------- | ---------------------------------------- |
| **aef** (`~/devcode/aef/agent`)                             | `851f6f8`       | 28 files changed                         |
| **baria** (`~/devcode/BariaDAO`)                            | `d91cc94`       | 77 files committed (pre-commit bypassed) |
| **autonomedia-snapshot** (`~/devcode/autonomedia-snapshot`) | `9fc4396`       | 112 files committed                      |

### 2. Type Corrections Applied (Prompt 2)

| File                        | Old type            | New type     | Source          |
| --------------------------- | ------------------- | ------------ | --------------- |
| `milestones/M10/M10S6E.md`  | `evaluation-report` | `evaluation` | report_02.md §6 |
| `milestones/M10/M10S9T1.md` | `test_ledger`       | `test_set`   | report_02.md §6 |

### 3. ID Renames Applied (Prompt 3)

| ID Group             | Files Touched | Scheme                  | Repos                               |
| -------------------- | ------------- | ----------------------- | ----------------------------------- |
| **COMP-001**         | 13            | `{repo}:COMP-M{N}S{N}`  | aef (12), baria (1)                 |
| **EVAL-001**         | 4             | `aef:EVAL-M{N}S{N}`     | aef only                            |
| **EVAL-1**           | 6             | `{repo}:EVAL-M{N}S{N}`  | aef (3), baria (2), autonomedia (1) |
| **TEVAL-1**          | 6             | `{repo}:TEVAL-M{N}S{N}` | aef (1), baria (2), autonomedia (3) |
| **REVIEW-001**       | 4             | `aef:REVIEW-M{N}S{N}`   | aef only                            |
| **REVIEW-1**         | 2             | `aef:REVIEW-M{N}S{N}`   | aef only                            |
| **SPEC-001**         | 2             | `aef:SPEC-M{N}S{N}`     | aef only                            |
| **VER-001**          | 2             | `aef:VER-M{N}S{N}`      | aef only                            |
| **Total ID renames** | **39**        | —                       | 3 repos                             |

### 4. derived_from References Updated

| File                        | Change                                                | Source                   |
| --------------------------- | ----------------------------------------------------- | ------------------------ |
| `milestones/M7/M7S2R.md`    | `EVAL-001` → `aef:EVAL-M7S2`                          | report_03.md §3          |
| `milestones/M7/M7S3R.md`    | `EVAL-001` → `aef:EVAL-M7S3`                          | report_03.md §3          |
| `milestones/M10/M10S1I1.md` | `EVAL-001` → `aef:EVAL-M10S1`                         | report_03.md §3          |
| `milestones/M10/M10S1C.md`  | `SPEC-001` → `aef:SPEC-M10S1`                         | report_03.md §3          |
| `milestones/M10/M10S1E.md`  | `SPEC-001, VER-001` → `aef:SPEC-M10S1, aef:VER-M10S1` | report_03.md §3          |
| `milestones/M10/M10S1R.md`  | `SPEC-001` → `aef:SPEC-M10S1`                         | report_03.md §3          |
| `milestones/M10/M10S5R.md`  | `COMP-001` → `aef:COMP-M10S5`; `EVAL-001` preserved   | report_03.md §3 + Case A |

### 5. Re-validation Results

**Duplicate ID count: before → after**

| Repo        | Before          | After           | Remaining                                                       |
| ----------- | --------------- | --------------- | --------------------------------------------------------------- |
| aef         | 9 duplicate IDs | **1 remaining** | `EVAL-M10S3` (2x — **skipped per #NEEDS-CLARIFICATION** Case D) |
| baria       | 2 duplicate IDs | **0**           | —                                                               |
| autonomedia | 2 duplicate IDs | **0**           | —                                                               |

**Type validation:** Both corrected types (`evaluation`, `test_set`) are in the canonical `valid_types` list. Three pre-existing invalid types remain (`investigation` x2, `session_audit` x1 in aef; `completion_report` in baria; `findings`, `report`, `session-audit` in autonomedia) — none touched by this migration.

**New dangling references introduced by this migration (reported, not patched):**

| File                        | Dangling ref   | Target                                        | Issue                                |
| --------------------------- | -------------- | --------------------------------------------- | ------------------------------------ |
| `milestones/M10/M10S5I1.md` | `REVIEW-M10S5` | was `id: REVIEW-001` → now `aef:REVIEW-M10S5` | Not in report_03's derived_from list |
| `milestones/M10/M10S7R.md`  | `EVAL-M10S7`   | was `id: EVAL-1` → now `aef:EVAL-M10S7`       | Not in report_03's derived_from list |
| `milestones/M10/M10S2R.md`  | `EVAL-001`     | was `id: EVAL-001` → now `aef:EVAL-M10S2`     | Not in report_03's derived_from list |

These 3 files have `derived_from` references to artifacts whose IDs were renamed, but the references were not listed in report_03's migration plan. Per guardrails: reported, not silently patched.

### 6. Summary Counts

| Metric                              | Value                                                             |
| ----------------------------------- | ----------------------------------------------------------------- |
| Files touched (aef)                 | 33                                                                |
| Files touched (baria)               | 5                                                                 |
| Files touched (autonomedia)         | 4                                                                 |
| **Total files changed**             | **42**                                                            |
| ID renames applied                  | 39                                                                |
| derived_from updates                | 7 (3 partial — EVAL-001 preserved in 1, 3 new dangles reported)   |
| Pre-existing duplicate IDs resolved | **8 of 9**                                                        |
| #NEEDS-CLARIFICATION cases skipped  | 2 (Case A: M10S5E EVAL-001 ref; Case D: EVAL-M10S3 type mismatch) |

All 3 repos are in a clean, fully revertible state via the snapshot commits listed above.
