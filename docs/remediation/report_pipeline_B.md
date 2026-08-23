Deliverable complete. Here's the full report.

---

## Step 1 — Routing Map (Investigation Results)

**The gap is confirmed.** Here's the actual routing today:

```
review-implementation  ──exit code 0──→ sync-documentation → archive-docs
                        └─exit code 1──→ [no defined handoff — issues found, reports them, stops]
                                          ↓ (user action)
                                          investigate-issue  ──diagnoses──→ M{X}S{Y}I{Z}.md
                                                               └─auto-fix──→ (fixes code, re-runs failing command)
                                                                              │
                                                                              ↓ (user action)
                                                                              hotfix-issue  ──syntax check──→ test pass
                                                                                                             ↓
                                                                                                    M{X}H{Z}.md
                                                                                                    [DEAD END]
```

Specific evidence:

| Skill                   | Dead-ends?                                                                                                                                                         | Evidence                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| `review-implementation` | Yes — exits code 1 when issues found, no `investigate-issue` or `hotfix-issue` handoff in its SKILL.md                                                             | SKILL.md mentions no downstream skill invocation                                            |
| `investigate-issue`     | Partially — auto-fix is local+limited; "Run" mode does chain through generate→implement→evaluate→review but is an _optional_ automation path, not a forced routing | SKILL.md Step 10: "Stop or Run" — the run is opt-in; `allowed-fix-scope: local, reversible` |
| `hotfix-issue`          | **Yes, fully confirmed.** After writing `M{X}H{Z}.md`, nothing forces re-evaluation or re-review                                                                   | SKILL.md ends at test verification and "Next Steps" are advisory only (no forced handoff)   |

**The `manage-development` state machine** confirms this: its 11-step pipeline ends at `archive-milestone` with **no re-evaluation loop** for hotfixed milestones.

**Additional finding from M10 forensics:** `M10H1.md` has **zero YAML frontmatter** — no `id`, no `derived_from`, no `type`. Even if the routing existed, automated traceability through metadata chains is impossible for this artifact.

---

## Step 2 — Designed Skill: `close-milestone`

### Files created

| Path                                                   | Purpose                    |
| ------------------------------------------------------ | -------------------------- |
| `skills/close-milestone/SKILL.md`                      | Canonical skill definition |
| `skills/close-milestone/templates/closure_template.md` | Closure artifact template  |
| `milestones/M10/M10CLOSE-1.md`                         | Worked example for M10     |

### Architecture

The skill sits at the **terminal gate** in the SDD pipeline, after `review-implementation` (and after any investigate/hotfix cycles). It has five sequential steps:

```
Step 1: Loop-Closure Investigation
  ├── Scan for M{X}*I*.md and M{X}*H*.md
  ├── If found: compare mtimes against post-fix EVAL + REVIEW
  ├── Gap found? → REFUSE CLOSURE (#NEEDS-CLARIFICATION), EXIT_CODE=1
  └── Gap clean? → proceed

Step 2: Mechanical Re-Validation
  ├── 2a: bin/lint-evaluation-gate.py --milestone M{X}
  ├── 2b: Duplicate-ID / schema check (Python: extract IDs, detect collisions)
  └── 2c: Artifact completeness (spec→verif→compl→eval→review per spec seq)

Step 3: Chain-of-Custody Tracing
  └── Walk every artifact's derived_from backward from closure to milestone

Step 4: Produce Closure Artifact
  └── milestones/M{X}/M{X}CLOSE-{N}.md with id: CLOSE-M{X}-{N}

Step 5: Status Doc Update
  └── MILESTONES.md → set status, link closure artifact. Only place this is done.

Step 6: Handoff
```

### Key design decisions

1. **Loop-closure enforcement** — Not optional. If a hotfix exists without a subsequent evaluation+review, the skill refuses closure and tells the user exactly which gate is missing.

2. **Three statuses**, not two — `CLOSED` / `CLOSED_WITH_DEFECTS` / `REFUSED`. The `CLOSED_WITH_DEFECTS` status allows closing a milestone with documented non-blocking issues (e.g., missing frontmatter on pre-existing artifacts), preventing the "all-or-nothing" trap that would leave milestones perpetually open.

3. **Timestamp-based tracing fallback** — Since `M10H1.md` and other real artifacts lack YAML frontmatter, the skill uses mtime comparison as a secondary verification method. This handles the real-world case of pre-metadata artifacts.

4. **ID minting (Prompt A compliance)** — `CLOSE-M{X}-{N}` with no semantic qualifiers; supersedes used for replacements. Global uniqueness enforced.

---

## Step 3 — Worked Example: `milestones/M10/M10CLOSE-1.md`

Already written to disk. Key findings from applying `close-milestone` to M10:

| Check                   | Result                                                           |
| ----------------------- | ---------------------------------------------------------------- |
| Hotfix detected         | `M10H1.md` (Aug 4) — no YAML frontmatter                         |
| Loop-closure evaluation | ✅ `M10S1E.md` (Aug 23) — post-hotfix                            |
| Loop-closure review     | ✅ `M10S1R.md` (Aug 23) — post-hotfix                            |
| Investigation M10S5I1   | ⚠️ Post-dates its review, but diagnostic-only (no fix)           |
| Lint gate               | ✅ Pass                                                          |
| Duplicate IDs           | ✅ None — but 3 artifacts lack any frontmatter                   |
| Artifact completeness   | ✅ All 10 spec sequences present                                 |
| **Final status**        | **CLOSED_WITH_DEFECTS** — F-1: 3 artifacts lack YAML frontmatter |

The worked example demonstrates:

- A hotfix that _was_ re-verified (M10H1 → S1 eval/review timestamps confirm)
- An investigation that post-dates its review but is diagnostic-only (graceful handling)
- Pre-existing metadata gaps (M10H1, M10S1R, M10S8E) that don't block closure but are documented
- The complete lineage DAG for S1 showing the hotfix cycle
- Full artifact table for all 10 spec sequences with `derived_from` chains

### What would have been different for M18

Had M18 existed with proper YAML frontmatter on all artifacts, the duplicate-ID check would have been cleaner (no pre-metadata findings), the `derived_from` chain would be fully traceable through metadata (no timestamp-hacks needed), and `M18CLOSE-1.md` would have received `status: CLOSED` rather than `CLOSED_WITH_DEFECTS`.
