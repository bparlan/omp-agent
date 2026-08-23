All tasks complete. Here's the deliverable.

---

## Deliverable

### 1. Current-State Routing Map (pre-edit)

| Stage | Entry Artifact                    | Next Skill                | Notes               |
| ----- | --------------------------------- | ------------------------- | ------------------- |
| 1     | `M{X}.md` missing                 | `milestone`               | Create milestone    |
| 2     | Only `M{X}.md`                    | `generate-spec`           |                     |
| 3     | Only `M{X}S{Y}.md`                | `generate-verification`   |                     |
| 4     | Only `M{X}S{Y}V.md`               | `generate-tests`          |                     |
| 5     | Tests exist, no `TE.md`           | `evaluate-tests`          | Pre-impl baseline   |
| 6     | `TE.md` exists, no approval stamp | `approve-spec`            | Human gate          |
| 7     | Approved spec, no `C.md`          | `implement-specification` |                     |
| 8     | `C.md`, no `E.md`                 | `evaluate-implementation` | Post-impl optimizer |
| 9     | `E.md`, no `R.md`                 | `review-implementation`   |                     |
| 10    | `R.md`, docs out of sync          | `sync-documentation`      |                     |
| 11    | All specs complete                | `archive-milestone`       | **Terminal**        |

**Gaps discovered:**

- **No failure routing.** evaluate-implementation → review-implementation is a hard transition. Evaluation failures (EXIT_CODE=1) have no routing path — they just sit there.
- **No lint gate.** `bin/lint-evaluation-gate.py` exists but is never called.
- **No close-milestone.** The pipeline ends at archive, with no loop-closure validation.
- **Cycle report template** used a table-based `Identifier: M{X}` — no YAML frontmatter, no namespaced ID per Prompt A.
- **Post-approval orchestration** described in `README.md` (repair loops, routing paths) was not reflected in `SKILL.md` at all — descriptive-only.

---

### 2. Updated `skills/manage-development/SKILL.md`

**Version:** `2.1.0-stable → 2.2.0-stable`

**What changed (10 edits across 4 hunks):**

| Section                        | Change                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontmatter                    | version bump, description updated to 12-stage + lint gate + fix routing + close-milestone                                                                                                                                                                                                                                                    |
| **§1 State Machine**           | Diagram extended: added `lint-evaluation-gate` → `review-implementation` → `sync-documentation` → `close-milestone` → `M{X}CLOSE-{N}.md`. Added horizontal fix-loop subgraph: `evaluation failure` → `hotfix-issue` / `investigate-issue` → `re-evaluate-implementation`. Invariant stages 11-12 added. Post-Evaluation Routing table added. |
| **§2 Your Process**            | Added 4 new transitions: lint-gate auto-call on `EXIT_CODE=0`; MINOR→hotfix→re-eval; COMPLEX→investigate→re-eval; INVALID_TEST_BLOCKED halt. Replaced `archive-milestone` terminal with `close-milestone` terminal. Added re-evaluation loop safety note.                                                                                    |
| **§3 Guardrails**              | Preserved F11.1-F11.4. Added C11.5 (hotfix loop closure gate), C11.6 (bypass awareness — primary enforcement is in close-milestone, this is defense-in-depth), C11.7 (repair limit enforcement).                                                                                                                                             |
| **§4 Validate Artifact State** | Added `review`, `closure`, `investigation`, `hotfix` types to complement existing `test_evaluation` and `evaluation`.                                                                                                                                                                                                                        |
| **§5 Output**                  | Preserved existing example. Added Post-Evaluation Routing Example and Final Stage Example.                                                                                                                                                                                                                                                   |

**Cycle report template** updated to YAML frontmatter with `id: CYCLE-M{X}-{N}`, `type: cycle_report`, `derived_from: [M{X}, CLOSE-M{X}-{N_CLOSE}]`.

---

### 3. Dry Description: Full Milestone Path Through Updated Orchestrator

```
manage-development invoked for target M{X}
```

**Pre-implementation pipeline** (unchanged from current):

```
1. detect M{X}.md missing → /milestone → creates M{X}.md
2. detect spec missing    → /generate-spec → produces M{X}S{Y}.md
3. detect verif missing   → /generate-verification → produces M{X}S{Y}V.md
4. detect tests missing   → /generate-tests → produces M{X}S{Y}T{Z}.md + tests/M{X}/
5. detect TE.md missing   → /evaluate-tests → produces M{X}S{Y}TE.md
6. detect approval missing → /approve-spec → stamps approval in spec
```

**Implementation** (unchanged):

```
7. detect C.md missing → /implement-specification → produces M{X}S{Y}C.md
```

**Post-evaluation routing** (NEW):

```
8. detect E.md missing → /evaluate-implementation → produces M{X}S{Y}E.md

   EXIT_CODE=0 (PASS):
     → auto-run: python3 bin/lint-evaluation-gate.py M{X}S{Y}E.md
     → if lint passes (exit 0): proceed
     → if lint fails (exit 1): warn, record in closure artifact, proceed
     → /review-implementation

   EXIT_CODE=1 (VALID_FAILURES_REMAIN):
     → classify: MINOR → /hotfix-issue → produces M{X}H{Z}.md
                COMPLEX → /investigate-issue → produces M{X}S{Y}I{Z}.md
     → re-invoke /evaluate-implementation against fixed codebase
     → loop bounded by MAX_AUTO_REPAIR_CYCLES (default 2-3)
     → on limit breach: HUMAN_ESCALATION

   EXIT_CODE=2 (INVALID_TEST_BLOCKED):
     → HALT. Report upstream test-generation defect.
```

**Post-review** (NEW terminal gate):

```
9. detect R.md exists, CLOSE-{N}.md missing
   → /close-milestone
     → Step 1: Loop-closure audit
       - Check for existing INV/HOT reports
       - If found: verify newer evaluation AND review exist after them
       - If not: REFUSE closure → user must re-run evaluate-implementation
     → Step 2: Run lint-evaluation-gate.py --milestone M{X}
     → Step 2b: Duplicate-ID / schema check
     → Step 2c: Artifact completeness check
     → Step 3: Derive chain-of-custody
     → Step 4: Write M{X}CLOSE-{N}.md
     → Step 5: Update MILESTONES.md

10. If docs out of sync after closure → /sync-documentation

11. Milestone complete. Optionally → /archive-milestone
```

**Defense-in-depth notes:**

- If a user runs `/close-milestone` directly (bypassing manage-development), the close-milestone skill's Step 1 (loop-closure audit) catches unverified hotfixes — this is the **primary** enforcement point.
- If they run the full pipeline through manage-development, the orchestrator's routing ensures fixes go back through evaluate-implementation before review/closure — this is the **secondary** enforcement layer.

### Files Modified

| File                                                           | Action                                           |
| -------------------------------------------------------------- | ------------------------------------------------ |
| `skills/manage-development/SKILL.md`                           | Rewritten sections 1-5                           |
| `skills/manage-development/templates/cycle_report_template.md` | Added YAML frontmatter with `id: CYCLE-M{X}-{N}` |

### Files Read (snapshot not modified)

| File                                                   | Purpose                                                               |
| ------------------------------------------------------ | --------------------------------------------------------------------- |
| `skills/close-milestone/SKILL.md`                      | Confirmed loop-closure gate design                                    |
| `skills/close-milestone/templates/closure_template.md` | Verified ID scheme compliance                                         |
| `bin/lint-evaluation-gate.py`                          | Confirmed argument signature (`--milestone M{X}` or single file path) |
| All core pipeline skills                               | Verified bypass risk (`user-invocable: true` on all)                  |
| `skills/manage-development/README.md`                  | Cross-checked against existing post-approval design                   |
