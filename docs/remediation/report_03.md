# ID Namespace Design — Read-Only Analysis

## 1. Duplicate ID Inventory (from AUDIT-001 §A.3, confirmed via grep on current file tree)

### COMP-001 — 12 files all in **aef** project

| File                            | New proposed ID   |
| ------------------------------- | ----------------- |
| `aef/milestones/M7/M7S2C.md`    | `aef:COMP-M7S2`   |
| `aef/milestones/M7/M7S3C.md`    | `aef:COMP-M7S3`   |
| `aef/milestones/M9/M9S1C.md`    | `aef:COMP-M9S1`   |
| `aef/milestones/M10/M10S1C.md`  | `aef:COMP-M10S1`  |
| `aef/milestones/M10/M10S3C.md`  | `aef:COMP-M10S3`  |
| `aef/milestones/M10/M10S4C.md`  | `aef:COMP-M10S4`  |
| `aef/milestones/M10/M10S5C.md`  | `aef:COMP-M10S5`  |
| `aef/milestones/M10/M10S6C.md`  | `aef:COMP-M10S6`  |
| `aef/milestones/M10/M10S7C.md`  | `aef:COMP-M10S7`  |
| `aef/milestones/M10/M10S8C.md`  | `aef:COMP-M10S8`  |
| `aef/milestones/M10/M10S9C.md`  | `aef:COMP-M10S9`  |
| `aef/milestones/M10/M10S10C.md` | `aef:COMP-M10S10` |

### EVAL-001 — 4 files all in **aef**

| File                           | New proposed ID  |
| ------------------------------ | ---------------- |
| `aef/milestones/M7/M7S2E.md`   | `aef:EVAL-M7S2`  |
| `aef/milestones/M7/M7S3E.md`   | `aef:EVAL-M7S3`  |
| `aef/milestones/M10/M10S1E.md` | `aef:EVAL-M10S1` |
| `aef/milestones/M10/M10S2E.md` | `aef:EVAL-M10S2` |

### EVAL-1 — 4 files across **aef + autonomedia**

| File                                            | New proposed ID          |
| ----------------------------------------------- | ------------------------ |
| `aef/milestones/M10/M10S4E.md`                  | `aef:EVAL-M10S4`         |
| `aef/milestones/M10/M10S7E.md`                  | `aef:EVAL-M10S7`         |
| `aef/milestones/M10/M10S10E.md`                 | `aef:EVAL-M10S10`        |
| `autonomedia-snapshot/milestones/M18/M18S3E.md` | `autonomedia:EVAL-M18S3` |

### TEVAL-1 — 4 files across **aef + autonomedia**

| File                                             | New proposed ID           |
| ------------------------------------------------ | ------------------------- |
| `aef/milestones/M10/M10S10TE.md`                 | `aef:TEVAL-M10S10`        |
| `autonomedia-snapshot/milestones/M18/M18S1TE.md` | `autonomedia:TEVAL-M18S1` |
| `autonomedia-snapshot/milestones/M18/M18S2TE.md` | `autonomedia:TEVAL-M18S2` |
| `autonomedia-snapshot/milestones/M18/M18S3TE.md` | `autonomedia:TEVAL-M18S3` |

### REVIEW-001 — 4 files all in **aef**

| File                           | New proposed ID    |
| ------------------------------ | ------------------ |
| `aef/milestones/M7/M7S2R.md`   | `aef:REVIEW-M7S2`  |
| `aef/milestones/M7/M7S3R.md`   | `aef:REVIEW-M7S3`  |
| `aef/milestones/M10/M10S2R.md` | `aef:REVIEW-M10S2` |
| `aef/milestones/M10/M10S5R.md` | `aef:REVIEW-M10S5` |

### SPEC-001 — 2 files all in **aef**

| File                          | New proposed ID  |
| ----------------------------- | ---------------- |
| `aef/milestones/M9/M9S1.md`   | `aef:SPEC-M9S1`  |
| `aef/milestones/M10/M10S1.md` | `aef:SPEC-M10S1` |

### EVAL-M10S3 — 2 files both in **aef M10** (different types sharing same base ID)

| File                           | New proposed ID                                                                        |
| ------------------------------ | -------------------------------------------------------------------------------------- |
| `aef/milestones/M10/M10S3R.md` | `aef:REVIEW-M10S3` (was `EVAL-M10S3`, but file type is `review` — fix type prefix too) |
| `aef/milestones/M10/M10S3E.md` | `aef:EVAL-M10S3` (type prefix matches)                                                 |

### REVIEW-1 — 2 files both in **aef M10**

| File                            | New proposed ID     |
| ------------------------------- | ------------------- |
| `aef/milestones/M10/M10S4R.md`  | `aef:REVIEW-M10S4`  |
| `aef/milestones/M10/M10S10R.md` | `aef:REVIEW-M10S10` |

### VER-001 — 2 files both in **aef**

| File                           | New proposed ID |
| ------------------------------ | --------------- |
| `aef/milestones/M9/M9S1V.md`   | `aef:VER-M9S1`  |
| `aef/milestones/M10/M10S1V.md` | `aef:VER-M10S1` |

**Count discrepancy from audit report:** The audit claimed EVAL-1 had 6 occurrences (including baria M5/M8) and TEVAL-1 had 6 (including baria M8/M5). The current file tree shows **no** `milestones/` directory under `baria/`. Either those files were removed after the audit, or the audit counted them from a different snapshot. The mapping above reflects what Prompt 4 would actually touch today.

---

## 2. Namespacing Scheme: `{project_code}:{TYPE}-{MILESTONE_QUALIFIER}`

**Recommended pattern:**

```
{project_code}:{PREFIX}-{M}{N}S{N}[SUFFIX]
```

Where:

- `project_code` = `aef`, `baria`, `autonomedia` (lowercase, alphanumeric only)
- `:` = separator (chosen per prompt's recommendation)
- `PREFIX` = `SPEC`, `VER`, `COMP`, `EVAL`, `REVIEW`, `TEVAL`, `INV`
- Milestone qualifier = `M{N}S{N}` (e.g., `M10S6`) — already used correctly in some files
- Optional suffix = `E`, `C`, `R`, `V`, `T1`, `TE` for type disambiguation when a milestone-substep has multiple artifacts of the same type

**Examples:**

- `aef:EVAL-M10S6E` — well-formed evaluation in aef M10S6
- `autonomedia:EVAL-M18S3` — evaluation in autonomedia M18S3
- `aef:COMP-M10S10` — completion report in aef M10S10

**Why this works:**

- Globally unique: no two projects share the same code, no two artifacts within a project share the same milestone-qualified suffix
- Grep-able: `grep "aef:"` finds everything from aef; `grep "COMP-"` still works
- Backward-compatible with the existing well-formed `EVAL-M10S6E` pattern — just prepend the project prefix
- The `:` separator is consistent with standard URI/namespace notation and rarely appears in existing IDs

### Tooling that assumes bare IDs and would break

1. **`bin/validate_metadata.py`** — line 137: regex `^[A-Z]+-[A-Z0-9]+$`. **BREAKS** — would reject `aef:EVAL-M10S6`. Regex needs update to `^[a-z]+:[A-Z]+-[A-Z0-9]+$` (or similar).

2. **`bin/resolve_artifact.py`** — line 50: `CANONICAL_ID_PATTERN = re.compile(r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT)-\d+$")`. **DOUBLY BROKEN**: (a) the pattern only matches `TYPE-NNN` not `TYPE-M{N}S{N}` format, so it already can't resolve milestone-qualified IDs like `SPEC-M10S6`; (b) adding a project prefix exacerbates that. This script needs structural changes to strip the namespace prefix before matching, or to resolve via Tier 1 (full metadata scan) as a fallback.

3. **`core/artifacts/resolution.py`** — line 51: `construct_canonical_path()` uses `artifact_id` directly in filepath: `milestones/{M_ID}/{type}s/{artifact_id}.md`. If artifact_id becomes `aef:COMP-M10S1`, the constructed filename would be `aef:COMP-M10S1.md` — which doesn't match any actual file. Need to strip namespace prefix when constructing paths, or rename filesystem files to match.

4. **`bin/legacy_indexer.py`** — line 116: regex `^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT)-\d+$`. Same `TYPE-NNN` limitation. Would fail silently for namespaced IDs.

5. **Test files** — Heavily reference old IDs:
   - `tests/M5/test_artifact_templates.py` — hardcodes `id: SPEC-001` in 15+ test templates
   - `tests/M5/test_metadata_schema.py` — regex `r'^SPEC-\d+$'`, `r'^EVAL-\d+$'`, etc., and 20+ test cases with `id: SPEC-001`
   - `tests/M6/test_canonical_ids.py` — asserts `SPEC-001`, `VER-001`, `EVAL-001` as valid canonical IDs; also asserts `EVAL-1` as _invalid_ (needs leading zero), which is in tension with renaming those IDs
   - `tests/M6/test_metadata_validation.py` — asserts `SPEC-001`, `VER-001`, `EVAL-001`, `REVIEW-001` as valid ID format
   - `tests/M6/test_skill_integration.py` — asserts generation should produce `SPEC-001`, `VER-001`, `EVAL-001`
   - `tests/M7/test_classify_tier1_frontmatter.sh` = hardcodes `SPEC-001` and `VER-001` in test fixtures and asserts their presence in output
   - `tests/M7/test_integrity_checksum.sh` — hardcodes `SPEC-001` and `VER-001` in test fixtures

---

## 3. Full `derived_from` Reference Update List

Every file whose `derived_from` field points to a now-duplicated old ID, and what it needs to become:

### COMP-001 references

| File                           | Old `derived_from`                            | New `derived_from`                                                |
| ------------------------------ | --------------------------------------------- | ----------------------------------------------------------------- |
| `aef/milestones/M10/M10S5R.md` | `[SPEC-M10S5, VER-M10S5, COMP-001, EVAL-001]` | `[aef:SPEC-M10S5, aef:VER-M10S5, aef:COMP-M10S5, aef:EVAL-M10S5]` |

**Ambiguity analysis:** `COMP-001` appears in 12 files. Which one does `M10S5R.md` reference? It's in `aef/M10/` and references `SPEC-M10S5` and `VER-M10S5` alongside it — both M10S5 artifacts. By proximity pattern, the `COMP-001` reference almost certainly points to `aef/M10/M10S5C.md` (the M10S5 completion report, also `id: COMP-001`). **Resolved: `aef:COMP-M10S5`.**

### EVAL-001 references

| File                            | Old `derived_from`                            | New `derived_from`                                                |
| ------------------------------- | --------------------------------------------- | ----------------------------------------------------------------- |
| `aef/milestones/M7/M7S2R.md`    | `[EVAL-001]`                                  | `[aef:EVAL-M7S2]`                                                 |
| `aef/milestones/M7/M7S3R.md`    | `[EVAL-001]`                                  | `[aef:EVAL-M7S3]`                                                 |
| `aef/milestones/M10/M10S5R.md`  | `[SPEC-M10S5, VER-M10S5, COMP-001, EVAL-001]` | `[aef:SPEC-M10S5, aef:VER-M10S5, aef:COMP-M10S5, aef:EVAL-M10S5]` |
| `aef/milestones/M10/M10S1I1.md` | `[EVAL-001]`                                  | `[aef:EVAL-M10S1]`                                                |

**Ambiguity analysis for M10S5R EVAL-001:** Same file as above. `EVAL-001` is used in 4 files. Since this derived_from also references SPEC-M10S5, VER-M10S5, and COMP-001 in the same line, all other references are M10S5 artifacts. The EVAL-001 here points to `aef/M10/M10S5E.md` — but wait, `M10S5E.md` has NO valid YAML frontmatter (flagged in AUDIT-001 §A.1 as `UNKNOWN`). It may or may not have `id: EVAL-001` (the audit couldn't parse it). This is ** `#NEEDS-CLARIFICATION`** — the M10S5 evaluation file may not even have a parseable ID, making the derived_from ambiguously dangling.

### SPEC-001 references

| File                                                                 | Old `derived_from`           | New `derived_from`                 |
| -------------------------------------------------------------------- | ---------------------------- | ---------------------------------- |
| `aef/milestones/M10/M10S1C.md` (line 49)                             | `[SPEC-001]`                 | `[aef:SPEC-M10S1]`                 |
| `aef/milestones/M10/M10S1E.md`                                       | `[SPEC-001, VER-001]`        | `[aef:SPEC-M10S1, aef:VER-M10S1]`  |
| `aef/milestones/M10/M10S1R.md` (line 81, embedded in YAML body list) | `- derived_from: [SPEC-001]` | `- derived_from: [aef:SPEC-M10S1]` |

**Ambiguity analysis:** All three files live in `aef/M10/` and reference SPEC-001 in the context of M10S1. The SPEC-001 in `aef/M9/M9S1.md` is a different milestone entirely (M9). By milestone proximity, these references unambiguously point to `aef/M10/M10S1.md` → `aef:SPEC-M10S1`. **Resolved.**

### VER-001 references

| File                           | Old `derived_from`    | New `derived_from`                |
| ------------------------------ | --------------------- | --------------------------------- |
| `aef/milestones/M10/M10S1E.md` | `[SPEC-001, VER-001]` | `[aef:SPEC-M10S1, aef:VER-M10S1]` |

**Ambiguity analysis:** Same file, same M10 context. The VER-001 reference points to `aef/M10/M10S1V.md` → `aef:VER-M10S1`. **Resolved.**

### IDs with NO `derived_from` references (no changes needed)

These IDs are used as their own type (evaluations, reviews) but nothing in the codebase points a `derived_from` at them:

- `EVAL-1` — no `derived_from` references anywhere
- `TEVAL-1` — no `derived_from` references anywhere
- `REVIEW-001` — no `derived_from` references
- `REVIEW-1` — no `derived_from` references
- `EVAL-M10S3` — no `derived_from` references

### Cross-check against AUDIT-001 §A.4 dangling-references list

The audit's dangling list shows references like `VER-M10S3V → M7`, `SPEC-M10S3 → M10`, `VER-M10S5 → M10`. These are NOT among the 9 duplicate IDs — they reference milestone IDs directly (`M7`, `M10`), which is a different problem (they're dangling, not ambiguous). They are not affected by this rename.

The audit also shows `EVAL-001 (aef/M7/M7S2E.md): references VER-003 — dangling`. VER-003 is NOT one of the 9 duplicate IDs — it's a separate dangling reference from a file that _has_ a duplicate ID. If we rename M7S2E's `id: EVAL-001` to `aef:EVAL-M7S2`, the `derived_from: [VER-003]` inside it remains dangling (VER-003 never existed). That's a pre-existing issue, not introduced by the rename.

---

## 4. Ambiguous Cases Needing Human Decision

### Case A: M10S5R's `derived_from: [EVAL-001]`

`aef/milestones/M10/M10S5R.md` has `derived_from: [SPEC-M10S5, VER-M10S5, COMP-001, EVAL-001]`. The EVAL-001 here would naturally map to `M10S5E.md` — but the audit flags `M10S5E.md` as having **no valid YAML frontmatter** (AUDIT-001 §A.1: `M10/M10S5E.md | aef | FLAG | No valid YAML frontmatter`). This file may not have a parseable `id` field at all. **`#NEEDS-CLARIFICATION`:** Does M10S5E.md need a frontmatter fix before it can be assigned an ID, or is the derived_from reference pointing to a different EVAL-001 entirely?

### Case B: Audit's claimed baria occurrences for EVAL-1 and TEVAL-1

The audit (§A.3) claims `EVAL-1` occurs in `baria M5/M8` and `TEVAL-1` in `baria M8/M5`. Current file tree shows **no milestones at all** under `baria/`. **`#NEEDS-CLARIFICATION`:** Were the baria milestones restructured/removed after the audit? Should Prompt 4 skip the baria project entirely, or are there latent references elsewhere that still need remapping?

### Case C: M10S10_dummy.md has no ID

`milestones/M10/M10S10_dummy.md` was flagged as `UNKNOWN` (no YAML frontmatter). It contains a test dummy used by M10S10's test infrastructure. Its filename suggests it's associated with M10S10, but without frontmatter it has no `id` field to rename. **`#NEEDS-CLARIFICATION`:** Should this file receive a new frontmatter with e.g., `id: aef:DUMMY-M10S10`, or be excluded from the rename pass?

### Case D: M10S3R has `id: EVAL-M10S3` but file type is `review`

`milestones/M10/M10S3R.md` has `id: EVAL-M10S3` but contains `type: review`. The ID prefix and the type field don't match. This is already flagged as a separate issue in AUDIT-001, but the rename mapping above proposes changing it to `aef:REVIEW-M10S3` (fixing both the namespace collision AND the type prefix mismatch). **`#NEEDS-CLARIFICATION`:** Is it acceptable to fix the type prefix as part of this rename, or should the ID only gain a namespace prefix and keep the wrong type prefix for now?

---

## Executive Summary for Prompt 4

**Scope:**

- 38 files need `id:` field changes across 9 duplicate ID values
- 5 `derived_from` reference arrays need updating (8 individual references)
- 5 tooling/script files need regex/pattern updates
- 14+ test files need assertion updates

**Hard-blockers before Prompt 4 can run:**

1. Case A: Resolve M10S5E.md's missing frontmatter before mapping its EVAL-001 reference
2. Case B: Confirm baria project status
3. Case C: Decide fate of M10S10_dummy.md
4. Case D: Decide on EVAL-M10S3 → REVIEW-M10S3 type-fix
