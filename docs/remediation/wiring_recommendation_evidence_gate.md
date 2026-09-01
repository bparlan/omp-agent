---
id: WIRING-RECOMMENDATION-evidence-gate
type: recommendation
description: "Where and how to wire bin/lint-evaluation-gate.py into the AEF workflow"
derived_from: [AUDIT-001, PROMPT-6]
template_version: 1.0.0
---

# Wiring Recommendation: Evidence-Floor Gate

## Decision

**Implement as on-demand standalone script** (`bin/lint-evaluation-gate.py`),
with a recommendation to add it as a CI gate in the next workflow update.
Do NOT wire it as a pre-commit hook today.

## Why not pre-commit

| Factor | Pre-commit hook | Standalone script |
|---|---|---|
| Catch-before-land | Catches before merge | Catches on manual run |
| Friction per milestone | Every commit must pass | Only when explicitly run |
| Git hook installation | `git init` / `git clone` doesn't install hooks | No setup needed |
| Team adoption | Requires every contributor to run `git config core.hooksPath` | Just run the script |
| False-positive impact | Blocks commit on false positive | Only blocks if run intentionally |

The AEF team currently has no pre-commit infrastructure (`.githooks/` directory
doesn't exist). Adding one is a separate infrastructure task. The existing
validation scripts (`bin/validate_metadata.py`, `bin/lint-verification-contract.sh`)
are all on-demand — this script follows the same pattern for consistency.

## Recommended integration order

1. **Immediate** — Manual use. Run `bin/lint-evaluation-gate.py` against
   any evaluation or completion report before marking a milestone complete.
   The exit code is actionable (0 = pass, 1 = findings, 2 = file error).

2. **Short-term** — Add to CI. In the CI config, run:
   ```
   bin/lint-evaluation-gate.py milestones/M{X}/M{X}S{Y}E.md milestones/M{X}/M{X}S{Y}C.md
   ```
   as a blocking check before merge. This catches violations without requiring
   local hook setup.

3. **Medium-term** — If friction from CI failures becomes an issue, add a
   `--warning-only` flag that exits 0 but prints findings. This lets CI surface
   findings without blocking, while the manual run (default) remains blocking.

## Wiring into the SDD pipeline

The template itself is the primary enforcement mechanism — section 3 of
`SKILL.md` and the `templates/evaluation_template.md` both now require
raw evidence. The lint script is the mechanical gate that verifies the
template was followed. The handoff contract in `SKILL.md` could be updated
to say:

> Before handing off to `review-implementation`, run:
> ```
> bin/lint-evaluation-gate.py milestones/M{X}/M{X}S{Y}E.md
> ```

But that's a note for the SKILL.md, not script wiring.

## Tradeoff accepted

On-demand means the gate is only as effective as the discipline to run it.
The audit found `M18S3E.md` with zero evidence — that report was generated
by an agent following a template that, until this prompt, had no evidence
requirement. With the template now requiring raw evidence, the primary
defense is the template itself, not the script. The script is the last
line of defense (catches human or agent error). Accepting on-demand means
we rely on process discipline until CI is wired.
