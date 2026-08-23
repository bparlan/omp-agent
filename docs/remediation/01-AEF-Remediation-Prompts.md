# AEF Phase 0.5 — Remediation Prompt Pack

Six prompts, derived from `AUDIT-001` findings. Run in the order below — several have hard dependencies. Each prompt states whether it's read-only (safe, no approval needed) or a write task (requires your sign-off on its dry-run output before the next prompt executes anything).

```
1. Audit Self-Verification         [read-only]  — run first, cheap, gates trust in AUDIT-001
2. Type Taxonomy Reconciliation    [read-only]  — design only
3. ID Namespace Design             [read-only]  — depends on 2, design only
4. Combined Type+ID Migration      [WRITE]      — depends on 2+3 AND your explicit approval
5. Structured Eval Schema          [WRITE]      — independent, can run parallel to 2-4
6. Evidence-Floor Gate             [WRITE]      — independent, can run parallel to 2-4
```

Do not run 4 until you've reviewed its dry-run mapping table from 2+3 and explicitly said to proceed. Everything else can run unattended.

---

## Prompt 1 — Audit Self-Verification (read-only)

**Purpose:** `AUDIT-001` (the Phase 0 audit) contains two issues that need resolving before it's trusted as a reference document: an unexplained evidence line in finding D.1, and three sections all headed "Part E."

**Instructions:**

1. Re-open `autonomedia-snapshot/milestones/M18/M18S2R.md` fresh (do not reuse cached findings from `AUDIT-001`) and re-derive what files it actually claims were modified/created. Compare against `AUDIT-001`'s D.1 finding, which includes the line `Files Modified/Created: bin/omp-discover (new)` — a file that has nothing to do with M18S2R's actual subject matter (`router.py`, `healthcheck.py`).
2. Determine the source of that line: is it (a) a genuine artifact from a different milestone/session that got pasted into D.1 by mistake, (b) a real but undocumented side effect of the M18S2R review that the report failed to mention, or (c) something else. Search the repo for `bin/omp-discover` — does it exist, when was it created, what milestone (if any) claims it?
3. Once resolved, correct `AUDIT-001`'s D.1 section: either remove the erroneous line and re-state the verdict cleanly, or if it turns out to be a real artifact, explain what it is and why it appeared in this finding.
4. Merge the three "Part E" headers (lines ~237, ~322, ~338 in the original) into one coherent Part E section with clear subsections, preserving all the underlying evidence — don't drop content, just fix the structure.

**Guardrails:** Read-only against the AEF/BariaDAO/Autonomedia project files. You may edit `AUDIT-001` itself (that's the deliverable). Do not fabricate an explanation for the `bin/omp-discover` line if you can't determine its source — mark it `#NEEDS-CLARIFICATION` and say so plainly.

**Deliverable:** A corrected `AUDIT-001` (bump `version` in frontmatter), plus a short note on what you found for the `bin/omp-discover` line.

---

## Prompt 2 — Type Taxonomy Reconciliation (read-only, design only)

**Purpose:** `AUDIT-001` found artifacts using types not in `validate_metadata.py`'s `valid_types`: `investigation`, `evaluation-report`, `test_ledger`, `session_audit`, `completion_report`, `findings`, `report`. Some of these look like typos/drift of an existing valid type (`evaluation-report` vs `evaluation`); others look like genuinely distinct artifact classes that were never formally registered (`session_audit`, `investigation`). Decide which is which before fixing anything.

**Instructions:**

1. List every type currently in `valid_types`, and every non-conforming type found by the audit, with a count of how many files use each.
2. For each non-conforming type, determine: is this recurring drift of an existing type (propose collapsing it into the canonical type), or a distinct artifact class that shows up repeatedly across milestones and projects (propose formally adding it to `valid_types` with its own ID prefix)? Use recurrence as the signal — a type used once might be a typo; a type used across multiple milestones and projects (like `investigation`, appearing in both `INV-001` and `INV-M10S5I1` patterns) is a real category that was never registered.
3. Specifically resolve the `I`-prefix collision: `investigation` and `implementation` currently share or nearly share the `I`/`INV` namespace. Propose a non-colliding prefix for whichever of the two needs one (don't assume — check what prefix `implementation`-type artifacts actually use today; the audit didn't confirm this).
4. Produce a proposed canonical type table: `type | id_prefix | status (existing / to-add / to-collapse-into-X)`.

**Guardrails:** Read-only. Do not edit `validate_metadata.py` or any milestone file in this step — this is a proposal only, for Prompt 4 to execute after you approve it.

**Deliverable:** The proposed type table, plus a list of every file that would need its `type` field changed under this proposal (grouped by old→new type).

---

## Prompt 3 — ID Namespace Design (read-only, design only)

**Purpose:** `AUDIT-001` found IDs duplicated across projects — `EVAL-1` (6×), `COMP-001` (12×), `TEVAL-1` (6×), and 6 others. These need to become globally unique before any cross-project tooling (telemetry, Ladybug provenance, anything that aggregates across `aef`/`baria`/`autonomedia`) can trust an ID as a stable key.

**Instructions:**

1. Using the canonical type/prefix table from Prompt 2, list every currently-duplicated ID from `AUDIT-001` §A.3, with every file it appears in (project + path).
2. Propose a namespacing scheme. Default recommendation to evaluate: prefix with project short-code, e.g. `aef:EVAL-M10S6` / `baria:EVAL-M5S2` / `autonomedia:EVAL-M18S3`, using the milestone-qualified suffix pattern that's already used correctly in some files (e.g. `EVAL-M10S6E` is well-formed; `EVAL-1` and `COMP-001` are the bare, non-qualified pattern causing collisions). Flag if any existing tooling (Ladybug ingestion, `validate_metadata.py`, any script) assumes IDs are bare strings without a `:` or project segment — that would break under this scheme and needs to be accounted for.
3. For every ID being renamed, trace every `derived_from` reference anywhere in the codebase that points to the old ID, and list what it needs to become. This is the part most likely to be incomplete or wrong if done casually — cross-check against `AUDIT-001` §A.4's dangling-reference list too, since some of those "dangling" references might actually be pointing at one of several same-named duplicates, i.e. not dangling but ambiguous.
4. Flag any case where you cannot confidently determine which of several same-ID files a given `derived_from` reference was originally pointing to. Mark these `#NEEDS-CLARIFICATION` rather than guessing.

**Guardrails:** Read-only. No files modified. This produces the exact mapping Prompt 4 will execute.

**Deliverable:** A full old-ID → new-ID mapping table (one row per affected file), a full derived_from-reference update list, and a list of ambiguous cases needing a human decision before Prompt 4 can run against them.

---

## Prompt 4 — Combined Type + ID Migration (WRITE — requires your sign-off first)

**Do not run this until you've reviewed Prompts 2 and 3's output and told the agent to proceed.**

**Purpose:** Apply the approved type-taxonomy and ID-namespace mapping.

**Instructions:**

1. Before any edit: commit or snapshot the current state of all three project repos so this is fully revertible.
2. Apply the approved `type` corrections from Prompt 2 and `id`/`derived_from` renames from Prompt 3, file by file.
3. For any case flagged `#NEEDS-CLARIFICATION` in Prompt 3, do not guess — skip it, list it separately, and leave the original ID in place pending a human decision.
4. After all edits, re-run the Part A schema/lineage checks from `AUDIT-001` against the full artifact set. Confirm: zero duplicate IDs remain (except explicitly-skipped ambiguous cases), zero new dangling references were introduced by the renames, and all `type` values now validate.
5. Report exactly what changed: file count touched, ID renames applied, `derived_from` references updated, and the before/after duplicate-ID count.

**Guardrails:** This is the one prompt in this pack allowed to write to project files. Every change must be traceable to a specific row in the Prompt 2/3 output — no ad hoc corrections invented mid-run. If the re-validation in step 4 finds a problem your migration caused, report it, don't silently patch around it.

**Deliverable:** A migration report (files changed, renames applied, re-validation result) plus confirmation the repos are in a clean, revertible state.

---

## Prompt 5 — Structured `evaluate-implementation` Output Schema (WRITE — skill/template change)

**Purpose:** `AUDIT-001` §E.3 confirmed `evaluate-implementation`'s output is narrative/prose with no machine-parseable taxonomy, which is the actual blocker to any future automated routing of findings. Fix the template, not a one-off file.

**Instructions:**

1. Locate the current `evaluate-implementation` skill/template definition in AEF (not just its output examples — the thing that generates the output).
2. Design a structured findings block to be appended to every future evaluation report, using the taxonomy `AUDIT-001` already validated as real and recurring: `ARCHITECTURE_AMBIGUITY`, `INVALID_TEST`, `INACCURATE_DOCUMENTATION`, `EVIDENCE_GAP`, `TEST_VALIDATION_BLOCKED`, plus an open-ended category for new findings. Each finding entry needs: `category`, `severity`, `affected_file(s)`, `classification` (`mechanically_auto_fixable` / `judgment_required` / `process_failure`), and a `raw_evidence` field that must be non-empty (see Prompt 6 — this ties directly to the evidence-floor gate).
3. Keep the narrative report as-is alongside the structured block — this is additive, not a replacement of the human-readable format. The structured block is what makes findings routable later; the prose is still what a human reads first.
4. Update the skill template so this structured block is generated going forward. Do not retroactively rewrite old evaluation reports — this is a forward-looking fix, not a Part A-style migration.
5. Produce one example: regenerate the structured block for `M18S3E.md` and `M18S1E.md` (using the same evidence already documented in `AUDIT-001`, not by re-running anything) as a worked example of what the new format produces, so you can sanity-check the schema against real findings before it goes live.

**Guardrails:** This changes the skill's output template, which affects every future milestone — treat it with the same care as any AEF framework-level change (this is exactly the kind of "don't modify OMP internal agents directly" territory noted in your decision log — confirm whether this template lives in project-level skills or a shared AEF core skill, and route the actual edit accordingly).

**Deliverable:** The updated skill template, the schema definition, and the two worked examples.

---

## Prompt 6 — Evidence-Floor Gate (WRITE — template + lint check)

**Purpose:** `AUDIT-001` §C found evaluation/completion reports with zero raw command output (`M18S3E.md`'s six-line shape) alongside others with partial evidence (exit codes but no stdout/stderr). This needs a going-forward gate, not a backfill — you cannot honestly manufacture raw evidence for a check that already happened without it.

**Instructions:**

1. Update the `evaluate-implementation` and completion-report templates to require a `raw_evidence` block per claim: the actual command invoked and its captured stdout/stderr/exit code, not just a summary counter. If a check genuinely can't produce this (e.g. a manual/visual check), the template should require an explicit statement of why, not a silently empty field.
2. Write a mechanical lint check (a script, not an agent judgment call) that can be run against any evaluation/completion report and flags: summary counters present with zero raw evidence attached (the `EVIDENCE_GAP` pattern), and the self-contradiction pattern from `AUDIT-001` Part B — resolution-language (`COMPLETE`, `Exit Code: 0`, `no blocking issues`) co-occurring with pending-language (`PENDING`, `BLOCKED`, `Next Steps`) in the same document without an explicit qualifying scope statement.
3. Decide where this lint check runs — as a pre-commit-style gate before a milestone can be marked complete, or as a standalone script you run on demand. State which you're implementing and why; don't silently pick one without noting the tradeoff (a blocking gate catches this earlier but adds friction to every milestone; on-demand is lower friction but relies on remembering to run it).
4. Do not apply this gate retroactively to flag every historical `EVIDENCE_GAP`/contradiction `AUDIT-001` already found — those are already documented findings, not new work for this prompt. This prompt's job is stopping new instances, not re-litigating old ones.

**Guardrails:** The lint check must be mechanical (regex/structural, not "ask an LLM if this looks contradictory") so its results are deterministic and reproducible — that's the whole point of a gate.

**Deliverable:** Updated templates, the lint script, and a note on where it's wired in (or a recommendation for where, if wiring it in is out of scope for this prompt).
