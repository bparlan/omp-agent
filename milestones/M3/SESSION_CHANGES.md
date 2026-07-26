# Session Changes — M3SA1

## Modified Files

### Documentation Framework
- `docs/FRAMEWORK.md` — Added "The Uncertainty Marker" architectural section
- `AGENTS.md` — Added Uncertainty Marker + Mechanical Tooling Stack subsections

### Skills (SKILL.md)
- `skills/implement-specification/SKILL.md` — Added `#NEEDS-CLARIFICATION` marker to "When uncertain"
- `skills/review-implementation/SKILL.md` — Added zero-trust standing rule + Live State Verification
- `skills/investigate-issue/SKILL.md` — Added evidence-based debugging rule (2 placements)
- `skills/evaluate-implementation/SKILL.md` — Added evidence-based debugging rule
- `skills/bootstrap-project/SKILL.md` — Added Mechanical Tooling Stack step (step 8)

### Templates
- `templates/review_template.md` — Added "## Live State Verification" section
- `templates/completion_template.md` — Appended "## Raw Evidence" section
- `templates/evaluation_template.md` — Appended "## Raw Evidence" section

## Created Files

### New Utility
- `bin/ground-truth-check.sh` — Read-only live-state verification utility (5 commands)

### Milestone Artifacts (M3S2)
- `milestones/M3/M3S2.md` — Specification
- `milestones/M3/M3S2V.md` — Verification protocol
- `milestones/M3/M3S2T1.md` — Test plan
- `milestones/M3/M3S2C.md` — Completion report
- `milestones/M3/M3S2E.md` — Evaluation report
- `milestones/M3/M3S2R.md` — Review report (ACCEPTED)
- `milestones/M3/M3SA1.md` — Session audit document

### Test Scripts
- `tests/M3/test_uncertainty_marker.sh` — FR-1 test
- `tests/M3/test_zero_trust_review.sh` — FR-2 test
- `tests/M3/test_evidence_debugging.sh` — FR-3 test
- `tests/M3/test_raw_evidence_mandate.sh` — FR-4 test
- `tests/M3/test_ground_truth_helper.sh` — FR-5 test
- `tests/M3/test_tooling_stack.sh` — FR-6 test
- `tests/M3/run_all_m3s2_tests.sh` — Test runner

## References
- M3SA1 — Session Audit Document
- M3S2C — Completion Report
- M3S2E — Evaluation Report
- M3S2R — Review Report (Accepted)
