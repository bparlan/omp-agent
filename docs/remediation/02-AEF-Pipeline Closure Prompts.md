# AEF Phase 1 — Pipeline Closure Prompts

Three prompts, in dependency order. A is foundational (fixes a live data-integrity gap); B and C both depend on A's outcome, and C depends on B existing.

```
A.  ID-Minting + implement-specification Evidence Integration   [WRITE]
A.5 Sweep remaining P0.5 loose ends (optional, bundle or defer) [WRITE]
B.  New terminal skill: close-milestone                          [WRITE]  — depends on A
C.  manage-development orchestration update                      [WRITE]  — depends on A + B
```

---

## Prompt A — ID-Minting Compliance + `implement-specification` Evidence Integration

**Purpose:** Two related gaps. First: report_04 fixed 39 _existing_ ID collisions but never touched the logic that _mints new IDs_ — if that logic still produces bare `SPEC-001`-style IDs, M19+ will recreate the same collisions immediately. Second: report_06 added a `## Raw Evidence` section to `completion_template.md`, but a template section only works if the skill's own instructions actually direct the agent to populate it — report_05 did this for `evaluate-implementation`'s SKILL.md; `implement-specification`'s SKILL.md has not had the equivalent update.

**Instructions:**

1. Find every place in the AEF skill set that mints a new artifact ID — this is likely not just `implement-specification`. Check `generate-spec`, `generate-verification`, `generate-tests`, `evaluate-implementation`, and `review-implementation` too; ID minting could live in each skill's own SKILL.md instructions, in a shared template, or in a helper script. Report all of them — don't assume it's centralized if you haven't confirmed that.
2. For each one found, confirm whether it already emits the namespaced scheme from report_04 (`{repo}:PREFIX-M{N}S{N}`) or still produces bare/ambiguous IDs. If instructions reference the old bare pattern anywhere (examples in prose, template placeholders, etc.), update them to the namespaced form.
3. If ID minting is scattered across multiple skills with duplicated logic (rather than one shared source), flag that as its own finding — don't silently consolidate it as part of this prompt unless it's trivial; report it and let a human decide if it's worth a shared helper.
4. Now, specifically for `implement-specification`: update its `SKILL.md` to require populating the `## Raw Evidence` block added in report_06 — every claim in the completion report must be backed by the actual command run and its captured output, mirroring the requirement report_05 wrote into `evaluate-implementation`. Do not just point at the template; the skill's own procedure needs to instruct the agent to run its verification steps and capture output as it goes, not reconstruct evidence after the fact from memory.
5. Confirm compatibility both directions: `implement-specification`'s completion reports reference `derived_from` IDs (spec, verification, tests) — confirm those references will already be in the new namespaced form once M19 specs are generated per step 2, and confirm `evaluate-implementation` (already updated in report_05) can correctly parse a namespaced ID when checking `derived_from` chains. If either direction has an unhandled edge case (e.g. a regex that assumes no `:` in an ID), report it as a bug, don't silently patch it into a bigger change.

**Guardrails:** Same as the P0.5 prompts — this touches shared AEF core (confirmed canonical repo per report_05), so treat every change as framework-wide. Snapshot/commit before editing. Do not retroactively rewrite old completion reports; this is forward-looking only.

**Deliverable:** Inventory of every ID-minting location and its current compliance status, the `implement-specification` SKILL.md update, and a report on the derived_from-compatibility check in both directions.

---

## Prompt A.5 — Sweep Remaining P0.5 Items (optional — run now or defer, your call)

**Purpose:** Close the three items report_04 left open, so they don't compound while Prompts A–C are in flight.

**Instructions:**

1. **Dangling refs** (`M10S5I1.md` → `REVIEW-M10S5`, `M10S7R.md` → `EVAL-M10S7`, `M10S2R.md` → `EVAL-M10S2`): confirm each target ID actually exists post-migration under its new namespaced form (it should — these are artifacts that _were_ renamed, just not tracked in the original derived_from update list). If it exists, this is a one-line fix per file: update the stale reference. If it doesn't exist, escalate — that would mean the rename broke a real reference, which report_04's own re-validation should have caught and didn't.
2. **Remaining duplicate** (`EVAL-M10S3` ×2, Case D): resurface what the type-mismatch actually is (report_04 doesn't say). Determine whether the two `EVAL-M10S3` artifacts are genuinely the same evaluation duplicated, or two different evaluations that happen to share a milestone/sub-milestone number and need an additional disambiguator (e.g. a suffix).
3. **Undecided ad hoc types**: for `investigation`, `session_audit`, `completion_report`, `findings`, `report` (and any `session-audit` variant spelling found in autonomedia) — make the actual decision Prompt 2 was supposed to produce: register as canonical types with prefixes, or collapse into an existing type. Apply it. Don't leave this a third time.

**Guardrails:** Same write-task guardrails as report_04's execution — snapshot first, report anything ambiguous rather than guessing.

**Deliverable:** Confirmation all three items are closed, or an escalation report for whichever isn't resolvable without a judgment call from you.

---

## Prompt B — New Terminal Skill: `close-milestone`

**Purpose:** `review-implementation` currently branches to `investigate-issue` or `hotfix-issue` when it finds problems, and nothing happens after that. The real gap this creates: if a hotfix is applied, there's currently nothing that forces it back through evaluation/review before the milestone can be considered done — a milestone could end on an unverified fix. Before designing the new skill, confirm this is actually how the current routing behaves; don't assume.

**Instructions:**

1. **Investigate first, read-only.** Read `review-implementation`, `investigate-issue`, and `hotfix-issue`'s SKILL.md files. Map the actual current routing: does `investigate-issue` only diagnose (handing off to `hotfix-issue` or back to a human), or can it also fix? Does `hotfix-issue`'s output loop back into `review-implementation` or `evaluate-implementation` for re-verification anywhere today, or does it genuinely dead-end? Report what you find before designing anything — the fix depends on which of these is true.
2. **Design `close-milestone`** as the new terminal skill, invoked after `review-implementation` (and, if step 1 confirms a dead-end, after `investigate-issue`/`hotfix-issue` too). Its job:
   - **Loop-closure check (the core purpose):** if this milestone ever went through `investigate-issue` or `hotfix-issue`, confirm the resulting change was re-evaluated/re-reviewed before this skill runs. If it wasn't, `close-milestone` must refuse to close the milestone and say why — it should not be possible to mark a milestone done on the strength of an unverified hotfix.
   - **Mechanical re-validation:** re-run `bin/lint-evaluation-gate.py` (report_06) and a duplicate-ID/schema check (Part A style, from `AUDIT-001`) against every artifact this milestone produced, before allowing closure.
   - **Canonical closure artifact:** produce one artifact chaining the full lineage for this milestone (spec → verification → tests → implementation → evaluation → review → any investigate/hotfix cycle) via `derived_from`, rather than leaving status scattered across separate reports the way `M18S1_REVIEW_COMPLETE.md`'s ✅-COMPLETE-headers-next-to-open-CRITICAL-items pattern did. This is the single place a milestone's real status gets asserted.
   - **Status doc updates:** if MILESTONES.md-style docs get touched, this should be the only place that happens for milestone-completion status, to avoid the earlier ambiguity between "documentation about the fix is done" and "the fix is done."
3. Use the ID-minting fix from Prompt A so this new skill's own closure artifacts are namespaced correctly from day one.

**Guardrails:** Don't assume the loop-closure gap exists without confirming it in step 1 — if `investigate-issue`/`hotfix-issue` already loop back somewhere, design `close-milestone` around what's actually missing, not around an assumed gap.

**Deliverable:** The routing map from step 1, the new `close-milestone` SKILL.md + template, and a worked example against one already-closed milestone (M18, since you have full context on it) showing what its closure artifact would have looked like.

---

## Prompt C — `manage-development` Orchestration Update

**Purpose:** Wire the full cycle together so it runs as one orchestrated sequence rather than requiring someone to remember to invoke each gate manually.

**Instructions:**

1. Read-only first: map `manage-development`'s current orchestration logic — what does it actually sequence today, and where does it stop?
2. Extend it to run the full cycle: milestone → `generate-spec` → `generate-verification` → `generate-tests` → `implement-specification` → `evaluate-implementation` → `review-implementation` → (`investigate-issue`/`hotfix-issue` loop, if triggered) → `close-milestone` (Prompt B).
3. Insert `bin/lint-evaluation-gate.py` as an **automatic** call after `evaluate-implementation` produces output, before the orchestrator allows progression to `review-implementation`. This is the connection report_06 left open: it recommended on-demand-not-pre-commit because no pre-commit infra exists — `manage-development` calling the script itself, at the right point in the sequence, gets you the equivalent of a gate without needing git hook infra.
4. If a milestone enters the `investigate-issue`/`hotfix-issue` branch, the orchestrator must route the result back through `evaluate-implementation` before `close-milestone` can run — this enforces Prompt B's loop-closure requirement at the orchestration level, not just inside `close-milestone` itself, so a milestone can't skip the orchestrator and call `close-milestone` directly to bypass it. Confirm whether that's actually possible (can skills be invoked directly, bypassing `manage-development`?) — if so, the loop-closure check needs to live in `close-milestone` itself regardless (as designed in Prompt B), with the orchestrator update as defense in depth, not the only enforcement point.
5. Confirm `manage-development`'s own artifacts (whatever it produces to track orchestration state) use the namespaced ID scheme from Prompt A.

**Guardrails:** This is the highest-blast-radius change in this pack — it's the thing that runs everything else. Snapshot before editing, and if step 1's mapping reveals `manage-development` is more complex or does more than described here, report that before changing it rather than assuming your prior understanding was complete.

**Deliverable:** Current-state routing map, the updated `manage-development` SKILL.md, and a dry description (not a live run, unless you want to actually test it end-to-end) of what a milestone's full path through the updated orchestration looks like.
