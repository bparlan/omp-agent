---
## Final Deliverable: Prompt A — ID-Minting Compliance + `implement-specification` Evidence Integration

### Snapshot
Commit `5a25900` on `851f6f8` baseline (47 files, +1181 -53). All existing report_04/05/06 changes are included. Edit applied from this baseline.
---

### Part 1: ID-Minting Location Inventory & Compliance

| #   | Skill / Template                                |                    Current ID Format | Location (SKILL line) | Compliance vs report_04 scheme (`{repo}:PREFIX-M{N}S{N}`)                                                                                       |
| --- | ----------------------------------------------- | -----------------------------------: | --------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **generate-spec** / `specification_template.md` |                      `SPEC-M{X}S{Y}` |      SKILL §1 line 25 | ✅ Milestone-qualified but **no repo prefix**. The `M{X}` qualifier prevents bare collisions, but lacks `aef:` / `baria:` repo-namespace.       |
| 2   | **generate-verification** SKILL                 |                      `VER-M{X}S{Y}V` |      SKILL §3 line 86 | ✅ Same — milestone-qualified, no repo prefix.                                                                                                  |
| 3   | **generate-tests** SKILL                        |                  `TSET-M{X}S{Y}T{Z}` |      SKILL §3 line 68 | ✅ Same — milestone-qualified, no repo prefix.                                                                                                  |
| 4   | **implement-specification** SKILL               |     **`COMP-{N}`** (bare sequential) |      SKILL §6 line 73 | ❌ **Bare sequential — no milestone qualifier, no repo prefix.** Produces `COMP-1`, `COMP-2` — will collide within same repo across milestones. |
| 5   | **implement-specification** template            |    **`COMP-000`** (bare placeholder) |       template line 2 | ❌ Same — bare sequential.                                                                                                                      |
| 6   | **evaluate-implementation** SKILL               |     **`EVAL-{N}`** (bare sequential) |      SKILL §3 line 45 | ❌ Same — bare sequential.                                                                                                                      |
| 7   | **evaluate-implementation** template            |     **`EVAL-{N}`** (bare sequential) |       template line 2 | ❌ Same — bare sequential.                                                                                                                      |
| 8   | **evaluate-tests** SKILL                        |    **`TEVAL-{N}`** (bare sequential) |      SKILL §4 line 74 | ❌ Same — bare sequential.                                                                                                                      |
| 9   | **evaluate-tests** template                     |                      **`TEVAL-{N}`** |       template line 2 | ❌ Same — bare sequential.                                                                                                                      |
| 10  | **investigate-issue** SKILL                     |      **`INV-{N}`** (bare sequential) |        SKILL line 128 | ❌ Bare sequential.                                                                                                                             |
| 11  | **investigation_template.md**                   |                        **`INV-{N}`** |                line 2 | ❌ Bare sequential.                                                                                                                             |
| 12  | **hotfix_template.md**                          |                        **`HOT-{N}`** |                line 2 | ❌ Bare sequential.                                                                                                                             |
| 13  | **review_template.md**                          |   `REVIEW-M10S9` (hardcoded example) |                line 2 | ⚠️ Template hardcodes `M10S9`. Skill doesn't give explicit ID minting instructions — agent infers from template.                                |
| 14  | **`bin/omp`** CLI                               | `TSET-{milestone_id}{sequence_id}T1` |             § line 92 | ⚠️ Milestone-qualified but no repo prefix. Separate implementation from SKILL templates (see finding B).                                        |

---

### Part 2: `implement-specification` SKILL.md — Raw Evidence Update

**Applied:** Both copies of the "Generate Completion Report" instruction (line 73 and line 78) now include evidence-capture directives. The step 9 "Verify Implementation" instruction also gained an inline capture requirement. Changes:

- **Line 73 (step 11.0):** Added "Populate the `## Raw Evidence` section with every command you ran, its exit code, captured stdout, and captured stderr — record these as you execute each step, not reconstructed after the fact. Every claim in the report MUST be backed by a corresponding raw evidence block."

- **Line 78 (step 9 compressed):** Added "As you run each verification command, immediately capture its exit code, stdout, and stderr — store these inline in the completion report as you go, never reconstruct evidence after the fact from memory."

- **Line 78 (step 11 compressed):** Added "Populate the `## Raw Evidence` section with the command traces captured during step 9 — every claim about test execution or specification conformance MUST have a corresponding raw evidence block."

The template (`completion_template.md`) already has the `## Raw Evidence` section from report_06 — the SKILL now requires the agent to populate it as verification runs.

---

### Part 3: Finding A — Scattered ID-Minting (Flag for Human Decision)

ID minting is **not centralized**. It lives in at least **six independent locations** with zero shared logic:

1. **`generate-spec` SKILL** — hardcodes `SPEC-M{X}S{Y}` in inline example
2. **`generate-verification` SKILL** — hardcodes `VER-M{X}S{Y}V` in §3
3. **`generate-tests` SKILL** — hardcodes `TSET-M{X}S{Y}T{Z}` in §3
4. **`evaluate-implementation` / `implement-specification` / `evaluate-tests` / `investigate-issue`** — each has its own bare `PREFIX-{N}` pattern
5. **`bin/omp` CLI** — separate implementation `TSET-{milestone_id}{sequence_id}T1` in Python CLI tool
6. **Templates** — each has its own placeholder pattern, often overridden by SKILL instructions

**Verdict:** Three distinct ID schemes coexist — milestone-qualified (`SPEC-M{X}S{Y}`), bare sequential (`COMP-{N}`, `EVAL-{N}`, `INV-{N}`, `HOT-{N}`), and a standalone CLI implementation (`bin/omp`). A shared helper in `bin/` (e.g., `bin/gen-id.py`) would eliminate drift but requires coordination across all skills. Recommend human decision before consolidating.

---

### Part 4: `derived_from` Compatibility — Both Directions

#### Direction A: `implement-specification` template → `evaluate-implementation` template

| Artifact                                         | Current `derived_from` Template Value         |                                          Correct Value for M19S3 |                                                                                      Status |
| ------------------------------------------------ | --------------------------------------------- | ---------------------------------------------------------------: | ------------------------------------------------------------------------------------------: |
| implement-specification `completion_template.md` | `derived_from: []` (empty)                    |                                    Should reference spec/ver IDs |                                       ⚠️ No instruction means agent likely omits or guesses |
| evaluate-implementation `evaluation_template.md` | `derived_from: [SPEC-{Y}, VER-{Y}]`           | `[SPEC-M19S3, VER-M19S3V]` or `[aef:SPEC-M19S3, aef:VER-M19S3V]` | ❌ **BUG: template uses `{Y}`-only, missing `M{X}` qualifier** — produces `[SPEC-3, VER-3]` |
| evaluate-tests `test-evaluation_template.md`     | `derived_from: [SPEC-{Y}, VER-{Y}, TSET-{Z}]` |                         `[SPEC-M19S3, VER-M19S3V, TSET-M19S3T1]` |                                                     ❌ **Same bug: `{Y}`-only, `{Z}`-only** |

Note: `evaluate-tests` SKILL has a hand-wavy resolution instruction ("resolve `SPEC-?` to `SPEC-M10S10`") but the template still carries the broken `{Y}` pattern, creating a reliance on the agent to catch the mismatch.

#### Direction B: Parsing namespaced IDs downstream

Three tools parse artifact IDs. Their regex compatibility against the three ID schemes:

| Tool                            |                    Regex | Bare Sequential `SPEC-001` |    Milestone-qualified `SPEC-M10S4` |       Full Namespaced `aef:SPEC-M10S4` |
| ------------------------------- | -----------------------: | -------------------------: | ----------------------------------: | -------------------------------------: |
| `validate_metadata.py` line 137 |     `^[A-Z]+-[A-Z0-9]+$` |                    ✅ PASS |                             ✅ PASS | ❌ **REJECTS** (`:` not in char class) |
| `resolve_artifact.py` line 50   | `^(SPEC\|…\|AUDIT)-\d+$` |                    ✅ PASS | ❌ **REJECTS** (no alpha after `-`) |                         ❌ **REJECTS** |
| `legacy_indexer.py` line 116    |   `^(SPEC\|…\|HOT)-\d+$` |                    ✅ PASS |                      ❌ **REJECTS** |                         ❌ **REJECTS** |

**Bugs found:**

1. **`evaluate-implementation` / `evaluate-tests` templates:** `derived_from: [SPEC-{Y}, VER-{Y}]` uses bare `{Y}` sequence number instead of `M{X}S{Y}`. If spec artifacts have IDs `SPEC-M19S3`, the derived_from references `SPEC-3` won't match anything. This is a forward bug independent of the repo-prefix question — it will create dangling references for M19+.

2. **`validate_metadata.py`:** Regex `^[A-Z]+-[A-Z0-9]+$` will reject any artifact ID using the full `{repo}:PREFIX-M{N}S{N}` scheme that report_04 established. If M19 specs are generated with repo-prefixed IDs, validate_metadata.py will fail on them.

3. **`resolve_artifact.py`:** `CANONICAL_ID_PATTERN = r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT)-\d+$"` already rejects the current milestone-qualified `SPEC-M10S4` format. This tool is broken for ALL artifacts produced by the current templates.

---

### Summary of Required Fixes (forward-looking, M19+)

| Issue                                                                  |                                      Severity |                                       Affects |
| ---------------------------------------------------------------------- | --------------------------------------------: | --------------------------------------------: |
| implement-specification emits bare `COMP-{N}` (no milestone qualifier) |                         HIGH — collision risk |                       M19+ completion reports |
| evaluate-implementation emits bare `EVAL-{N}` (no milestone qualifier) |                         HIGH — collision risk |                       M19+ evaluation reports |
| evaluate-tests emits bare `TEVAL-{N}` (no milestone qualifier)         |                         HIGH — collision risk |                  M19+ test evaluation reports |
| investigate-issue emits bare `INV-{N}`                                 |     MEDIUM — collision risk across milestones |                      Any investigation report |
| hotfix emits bare `HOT-{N}`                                            |                  LOW — parallel hotfixes rare |                                Hotfix reports |
| `derived_from: [SPEC-{Y}, VER-{Y}]` missing `M{X}` qualifier           |                    HIGH — dangling references | evaluation & test evaluation reports for M19+ |
| `validate_metadata.py` rejects `aef:` repo-prefixed IDs                | HIGH — blocks validation if prefix is adopted |                       All artifact validation |
| `resolve_artifact.py` rejects milestone-qualified IDs (`SPEC-M10S4`)   |           MEDIUM — breaks artifact resolution |                     resolve_artifact.py users |
| ID minting scattered across 6+ locations                               |                   MEDIUM — maintenance burden |                                    All skills |
