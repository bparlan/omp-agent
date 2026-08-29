# AEF Fix — Specification Gap Gate False Positive + bin/ Tooling Distribution

Two independent prompts. Neither depends on the other.

---

## Prompt E — Fix `generate-verification`'s Specification Gap Gate

**Purpose:** The gate is conflating "target doesn't exist on disk yet" (expected, pre-implementation, normal) with "target isn't concretely specified" (a real gap). `M16S1V.md` itself is well-formed — every item already documents an Initial Failure Expectation — so the gate blocking on its own correctly-generated output is the bug, not the artifact.

**Instructions:**

1. Read-only: find "Section 2 / Specification Gap Gate" in `generate-verification`'s `SKILL.md`, and read its exact current logic.
2. Confirm directly from `milestones/M16/M16S1.md` (don't take the `#NEEDS-CLARIFICATION` report's word for it) whether the spec concretely names `autonomedia-test` and its subcommands/arguments/observable contracts, or whether it's vaguer than the report implied.
3. If the spec does concretely define the interface: the gate is checking the wrong thing. Redesign it to gate on **specification concreteness** (does the spec name a real command, its arguments, and its expected observable behavior?), not **filesystem existence** (does a file at that path currently exist?). A concretely-specified-but-not-yet-built target is exactly the normal pre-implementation state every other verification item in this codebase already documents via "Initial Failure Expectation" — it must not block. A vaguely-specified target (no concrete command name, no defined arguments, no observable contract) is the actual gap this gate should catch.
4. Check whether this same conflation exists anywhere else the gate logic might be duplicated (e.g. if `evaluate-tests` or `generate-tests` re-implements a similar check rather than sharing this one).
5. Fix the template footer bug: confirm the `[SPECIFICATION_GENERATION_COMPLETE]... Please run /generate-verification` line at the end of `M16S1V.md` is copy-pasted residue from `generate-spec`'s template (it should read something like `[VERIFICATION_GENERATION_COMPLETE]... run /generate-tests`). Fix it, and spot-check `generate-tests` and `evaluate-tests`'s templates for the same kind of stale copy-paste banner while you're in there — cheap to check now, easy to miss later.
6. Re-run `generate-verification` against M16S1 to confirm it no longer false-positives. Then construct a deliberately vague spec (a functional requirement with no concrete interface named) and confirm the gate still correctly refuses that case — the fix needs to stop the false positive without disabling the gate's real purpose.

**Guardrails:** Read the actual spec and skill files before concluding anything — don't infer the fix purely from the `#NEEDS-CLARIFICATION` report's framing. Snapshot before editing (canonical AEF core). No fabricated re-test output.

**Deliverable:** The gate-logic fix, the template footer fix (plus any other instances found), and evidence from both re-tests (M16 passing, the deliberately-vague case still correctly refusing).

---

## Prompt F — Distribute Required `bin/` Tooling Across AEF-Using Projects

**Purpose:** `bin/lint-verification-contract.sh` exists but was never propagated into rebalancer-bot. This will recur for every future shared script unless there's an actual distribution mechanism, not ad hoc per-project creation.

**Instructions:**

1. Read-only: inventory every `bin/*` script (and any shared templates) that AEF skills currently depend on — `lint-evaluation-gate.py`, `lint-verification-contract.sh`, `validate_metadata.py`, and any others you find — across the canonical AEF core repo and every project (`aef`, `baria`, `autonomedia`, `rebalancer-bot`). Build a script × project presence matrix.
2. Determine why rebalancer-bot didn't get this one: is there a bootstrap/sync step that's supposed to propagate required tooling into a project and it just didn't get re-run after the script was added, or does no such mechanism exist at all? Report which, with evidence — don't assume.
3. Design the structural fix: a bootstrap/sync check (a skill, or an early step inside `manage-development`'s pipeline) that verifies required AEF-core tooling is present and current in whatever project it's running in, and pulls/updates from the canonical source if missing. This is the same "which repo is the single source of truth" question already answered once for `SKILL.md` edits — resolve it once for `bin/` tooling too, don't just copy this one file and call it done.
4. Apply the immediate fix (get `lint-verification-contract.sh` into rebalancer-bot) plus the structural mechanism from step 3.
5. Re-run `generate-verification` for rebalancer-bot M1 to confirm the lint step now passes.

**Guardrails:** Snapshot before editing each project touched. No fabricated re-test output.

**Deliverable:** The tooling inventory matrix, the root-cause finding on why distribution failed, the bootstrap/sync mechanism, and confirmation rebalancer-bot M1 is unblocked.
