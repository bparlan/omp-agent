# AEF Phase 0 — Pipeline Stability & Implementation-Phase Audit

**Type of task:** Read-only investigative audit. **No code, spec, or milestone file may be modified, fixed, or "corrected" as part of this task.** Your only deliverable is a report. If you find yourself editing something to make a check pass, stop — that belongs in a separate hotfix/remediation milestone, not this audit.

**Standing rules that apply to this task specifically:**
- No simulated, hypothetical, or "should work" tool output. Every claim in your report must be backed by a command you actually ran and its actual captured output (stdout/stderr/exit code), or by a file you actually opened and quoted. If you cannot run something (missing dependency, server not started, environment unavailable), say so explicitly — do not infer or guess the result.
- If evidence is ambiguous or a judgment call is needed, mark it `#NEEDS-CLARIFICATION` and move on rather than resolving it silently.
- Distinguish clearly, per finding, between "confirmed via reproduction" (you ran it yourself, right now) and "confirmed via source inspection" (you read the code/artifact and reasoned about it, but did not execute it). Do not blur these two confidence levels together.
- Use the existing raw-evidence-completeness standard already established for this project's completion/review reports. This audit report is itself subject to that standard.

---

## Scope

Run this across every AEF-managed project with milestone artifacts: the AEF meta-repo itself (`~/devcode/aef/agent/`), BariaDAO, and Autonomedia. If `bparlan-thirdwave` has no `milestones/` directory or AEF integration, note that and skip it rather than fabricating findings for it.

Cover all milestones present (M1 through the latest, currently M18), not just the ones already known to have issues.

---

## Part A — Mechanical Schema & Lineage Audit

For every artifact file under each project's `milestones/**/*.md`:

1. Parse frontmatter using the same logic as `validate_metadata.py` (or the validator itself, if it can be invoked directly and non-destructively). Record: `id`, `type`, `milestone_id`, `derived_from`, and file path.
2. Flag any artifact with: missing or invalid frontmatter, missing `id`, a `type` code that is ambiguous or collides with another meaning (the known example: single-letter `I` used for both Investigation and Implementation — check whether this pattern recurs elsewhere), or a duplicate `id` across the codebase (including across different projects, since the earlier M5S1 namespace collision was cross-project).
3. For every `derived_from` reference, confirm the referenced ID actually resolves to a real, existing artifact with a matching ID. Flag any that don't resolve (dangling references) and any ID that resolves to more than one file (duplicate IDs).

**Output:** a table — `artifact_id | file_path | project | status (OK / FLAG) | issue`.

---

## Part B — Self-Contradiction Scan

For every review, evaluation, and completion report (`type: review`, `type: evaluation`, or completion-report-shaped files):

1. Search for co-occurrence, within the same document, of resolution-language (`COMPLETE`, `RESOLVED`, `Exit Code: 0`, `no blocking issues`, `✅`, `APPROVED`) and pending-language (`PENDING`, `BLOCKED`, `requires`, `Next Steps`, `awaiting`, `TBD`).
2. For every co-occurrence, quote both the resolution claim and the nearby pending item verbatim (with line references), and classify:
   - `GENUINE_CONTRADICTION` — the document asserts something is fully resolved/unblocked while its own body shows a real prerequisite (a test that never ran, a server that was never started, a check that was never executed) that would normally block that conclusion.
   - `ACCEPTABLE_PARTIAL` — the document is honestly scoped (e.g. "critical issues resolved, manual/integration testing still pending" stated as a caveat, not buried under a blanket "no blocking issues" claim).
3. Known prior examples of `GENUINE_CONTRADICTION` in this codebase: M7S1R (pre-commit shown running successfully in one section, "tool not installed" claimed in another), M18S2R (`Exit Code: 0 / No blocking issues remain` next to `TEST_VALIDATION_BLOCKED`). Use these as calibration examples of what you're looking for, not as an exhaustive list — actively search for others, don't stop once you've reconfirmed the known ones.

**Output:** list of flagged files with classification and the quoted evidence for each.

---

## Part C — Evidence-Floor Check

For every `type: evaluation` and completion-report artifact:

1. Does it contain actual captured command output (raw stdout/stderr/exit codes), or only summary counters and prose claims with nothing to verify them against?
2. Flag any with zero raw-evidence content as `EVIDENCE_GAP`. Known example of this shape: M18S3E.md (six lines, `TESTS_RUN=2 / TESTS_PASSED=2 / EXIT_CODE=0`, no command trace).
3. Note whether `EVIDENCE_GAP` correlates with milestone recency — is this an old-artifact problem that's already been fixed going forward, or is it still happening in the most recent milestones?

**Output:** list of flagged files, with a note on whether the gap is historical or current.

---

## Part D — Bounded Ground-Truth Spot Check

Pick up to 5 artifacts flagged `GENUINE_CONTRADICTION` or `EVIDENCE_GAP` in the **most recent** milestone(s) (prioritize recency over severity — we care most about whether current output can be trusted).

For each: actually re-run whatever the report claims was run, using the exact command if stated, or the obvious equivalent if not. Diff the real output against the report's claim. If it can't be re-run (missing server, missing env, destructive), say so explicitly and explain why, rather than skipping silently.

**Output:** for each spot-check, the command run, the raw output, and a verdict (`CONFIRMED` / `CONTRADICTED` / `COULD NOT VERIFY — reason`).

---

## Part E — Implementation-Phase Deep Dive

This is the priority section. The working hypothesis, based on recent milestones, is: `generate-spec`, `generate-verification`, and `generate-tests` are performing reliably, but `implement-specification` produces most of the real defects, `evaluate-implementation` only grades/reports on those defects without fixing them, and `review-implementation` is currently the only stage that actually performs remediation. Confirm, refine, or refute this, with evidence — do not just assume it's true because it's the working hypothesis.

1. **Inventory implementation failures.** Across all milestones with an `implement-specification` → `evaluate-implementation` → `review-implementation` chain, list every defect that was found at the evaluate or review stage but originated in implementation. For each, classify root cause. Reuse the categories this project has already been using informally in its own review reports where they fit (`ARCHITECTURE_AMBIGUITY`, `INVALID_TEST`, `INACCURATE_DOCUMENTATION`), and add categories as needed for patterns you find — candidates based on prior history include: environment/dependency not installed, hallucinated or non-existent API/function used, scope creep (edited files outside declared scope), misdiagnosed a real error as something else (e.g. treating a schema error as a documentation gap), fabricated evidence in its own completion report, invented undeclared schema/tables beyond what was specced.

2. **Compare failure rates by stage.** Does `generate-spec`/`generate-verification`/`generate-tests` genuinely fail less often, or does it just fail more *quietly* (e.g. because those artifacts are graded structurally/leniently rather than by actually executing anything)? Distinguish "implementation is genuinely harder" from "implementation is the first stage where claims get checked against a live, stateful system." This distinction matters for what kind of fix is appropriate.

3. **Assess whether `evaluate-implementation`'s output is currently structured or narrative-only.** Look at its actual output artifacts (not just what the skill is supposed to produce). Is each finding tagged with a machine-parseable category, severity, and affected file(s), or is it prose that a human (or `review-implementation`) has to re-interpret? This is the actual bottleneck for automation: you cannot route a finding to an automated fix without a structured taxonomy to route on.

4. **For each root-cause category found in step 1, classify it as one of:**
   - `MECHANICALLY_AUTO-FIXABLE` — deterministic, no judgment call needed (e.g. missing dependency → run install command; a known-bad syntax pattern → deterministic lint/fix).
   - `JUDGMENT_REQUIRED` — needs architectural or scope decisions a fresh review pass should make (e.g. two implementations of the same endpoint, which one is canonical).
   - `PROCESS_FAILURE` — not a code defect at all, but a report/evidence-quality problem (fabrication, missing raw evidence) that no amount of auto-fixing addresses; the fix is a stricter gate, not a patch.

   This classification is the deliverable that actually matters — it's what determines which categories are worth building automated remediation for, versus which should keep routing to a human-directed review/hotfix pass.

5. **Do not propose or implement an auto-fix mechanism as part of this task.** Report the taxonomy and the auto-fixable/judgment-required split as findings. The decision about what to automate, and how, is a separate design step once this evidence exists.

**Output:** a failure taxonomy table (`category | count | example milestone(s) | MECHANICALLY_AUTO-FIXABLE / JUDGMENT_REQUIRED / PROCESS_FAILURE`), plus a short written answer to: *is `implement-specification` actually the weakest stage, or is it the first stage where weaknesses become visible?*

---

## Deliverable

Produce a single report artifact following this project's own conventions — valid frontmatter, a real `id` (use `type: audit`, not `investigation`, to avoid the known `I`-code ambiguity; if the metadata validator rejects `type: audit` as unrecognized, report that as a finding rather than silently falling back to `investigation`). No `derived_from` (this audit isn't derived from a single spec/verification pair — it's cross-cutting).

Structure: Part A–D findings first (schema/lineage/contradiction/evidence-floor/spot-check), Part E (implementation deep dive) last, since it's the section this audit was primarily commissioned to answer. Every finding needs a file path and, where applicable, a line reference or quoted excerpt — no unsupported summary claims.
