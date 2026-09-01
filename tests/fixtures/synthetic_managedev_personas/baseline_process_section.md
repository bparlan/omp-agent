#### 2. Your Process: Tactical Orchestration & Handoffs

    *   No `M{X}.md` exists → Invoke `milestone` to create the milestone.

    *   Only `M{X}.md` exists → Invoke `generate-spec` to generate the specification.

    *   Only `M{X}S{Y}.md` exists (no verification) → Invoke `generate-verification`.

    *   Tests and `M{X}S{Y}T{Z}.md` exist on disk, but no `M{X}S{Y}TE.md` exists → Invoke **`evaluate-tests`** to verify baseline failures.

    *   `M{X}S{Y}TE.md` exists but the specification lacks `#### User Approval` → Invoke `approve-spec` to present baseline results and stamp approval.

    *   Approved spec exists, but no `M{X}S{Y}C.md` exists → Invoke `implement-specification`.

    *   `M{X}S{Y}C.md` exists but no `M{X}S{Y}E.md` exists → Invoke **`evaluate-implementation`** (Phase 2 optimizer).

    *   `M{X}S{Y}E.md` exists with `EXIT_CODE=0` → **Auto-run `python3 ~/devcode/aef/agent/bin/lint-evaluation-gate.py`** against the evaluation report. If the lint gate passes (exit 0), proceed. If it fails (exit 1), emit the lint failures as a warning but do not block — record them in the closure artifact later. Then invoke `review-implementation`.

    *   `M{X}S{Y}E.md` exists with `EXIT_CODE=1` (VALID_FAILURES_REMAIN) → Route based on failure classification:

        - **MINOR_IMPLEMENTATION_DEFECT** → Invoke `hotfix-issue`, then re-invoke `evaluate-implementation` on the hotfixed codebase.

        - **COMPLEX_OR_UNCLEAR_ISSUE** → Invoke `investigate-issue`, then re-invoke `evaluate-implementation` on the fixed codebase.

        - **HUMAN_ESCALATION** → Present escalation report and wait for user decision.

    *   `M{X}S{Y}E.md` exists with `EXIT_CODE=2` (INVALID_TEST_BLOCKED) → Halt. Report upstream test-generation defect. Do not proceed.

    *   `M{X}S{Y}R.md` exists but no `M{X}S{Y}CLOSE-{N}.md` exists → Invoke **`close-spec`** to validate the spec's loop-closure and produce the spec closure artifact.

    *   `M{X}S{Y}CLOSE-{N}.md` exists but no `M{X}CLOSE-{N_M}.md` exists → Check whether all specs in `M{X}.md` have their own `M{X}S{Y}CLOSE-{N}.md` artifacts. If yes, invoke **`close-milestone`** to run milestone-level loop-closure validation and produce the milestone closure artifact.

    *   `M{X}CLOSE-{N_M}.md` exists but canonical docs are out of sync → Invoke **`sync-documentation`**:

        1. Integrate review changes into roadmap, changelogs, and indices.

    *   `M{X}CLOSE-{N_M}.md` exists and all checks pass → **END** (milestone closure successful)
