# Ingestion Entries — M7

| Property | Value |
|----------|-------|
| Session | SA1 |
| Milestone | M7 |
| Date | 2026-07-27 |
| Status | Ready for manage-roadmap processing |

## Artifacts for Ingestion

### Skills
| File | Type | Description |
|------|------|-------------|
| `skills/generate-tests/SKILL.md` | Skill (v2.0.0) | Updated generate-tests skill with guardrails, test-first enforcement, language rules, machine-readable output |

### Milestone Artifacts
| File | Type | Description |
|------|------|-------------|
| `milestones/M7/M7.md` | Milestone definition | Restore Determinism milestone |
| `milestones/M7/M7S1.md` | Specification | M7S1 specification (approved) |
| `milestones/M7/M7S1V.md` | Verification | M7S1 verification protocol |
| `milestones/M7/M7S1T1.md` | Test plan | M7S1 test plan |
| `milestones/M7/M7S1C.md` | Completion report | Implementation completion report |
| `milestones/M7/M7S1E.md` | Evaluation report | Evaluation report |
| `milestones/M7/M7S1R.md` | Review report | Review report |
| `milestones/M7/M7INVESTIGATION.md` | Investigation | Contamination root cause analysis |
| `milestones/M7/M7SA1.md` | Session audit | SA1 session audit with lifecycle postmortem |
| `milestones/M7/SESSION_CHANGES.md` | Change log | Session changes |
| `milestones/M7/CHANGELOG_ENTRIES.md` | Changelog | Changelog entries |
| `milestones/M7/MILESTONE_UPDATES.md` | Milestone updates | Milestone progress |
| `milestones/M7/INGEST_ENTRIES.md` | Ingestion | This file |

### Tests
| File | Type | Description |
|------|------|-------------|
| `tests/M7/test_a_executable_files.sh` | Meta-test | Verifies generate-tests creates executable files |
| `tests/M7/test_b_initial_failure.sh` | Meta-test | Verifies generated tests initially fail |
| `tests/M7/test_c_no_production_files.sh` | Meta-test | Verifies no production files modified |
| `tests/M7/test_d_no_pseudo_code.sh` | Meta-test | Verifies no pseudo-code leakage |
| `tests/M7/test_e_no_implementation_snippets.sh` | Meta-test | Verifies no implementation snippets |
| `tests/M7/test_f_existing_artifacts_preserved.sh` | Meta-test | Verifies existing artifacts preserved |
| `tests/M7/test_g_no_implementation_on_failure.sh` | Meta-test | Verifies test failure does not trigger implementation |

## Key Architectural Findings (for Framework Documentation)

The M7 lifecycle postmortem (M7SA1.md) documents 10 architectural findings that should be preserved in canonical framework documentation:

1. Test failure != valid evidence
2. Test validity must be established before interpreting failures
3. Test harnesses must never scan themselves
4. Tests requiring repository state need isolated baselines
5. Platform assumptions matter (grep behaviour on macOS)
6. Meta-tests and generated project tests are different layers
7. Orchestrator must not infer artifact type from filenames
8. Existing artifacts must be treated as protected state
9. Implementation must never be inferred as the next step solely from a failed test
10. A lifecycle transition needs validated preconditions
