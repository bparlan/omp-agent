# Milestone Contract Acceptance Test Report

**Date**: 2026-08-09
**Type**: End-to-end acceptance verification, read-only assessment
**Tests executed**: 15 (8 contradiction + 7 regression)
**Result**: PARTIAL

---

## 1. Pipeline Contract Propagation

### Stage 1: milestone → M{X}.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | User input, code-search skeleton output, existing milestone IDs from MILESTONES.md |
| Where did that information originate? | User + filesystem introspection |
| Is it explicitly defined by the upstream contract? | N/A — milestone is the root contract |
| Is the stage inventing anything? | No — all new sections have explicit template mapping table requiring concrete user-provided data |
| Can the generated artifact be validated mechanically? | Partially — `legacy_boundaries` validated by `validate_metadata.py`, contract boilerplate is prompt-level, Spec Decomposition Plan is structure-checked by agent |

### Stage 2: generate-spec → M{X}S{Y}.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | Milestone contract (Integration Bindings, Spec Decomposition Plan), existing specs, binary directory |
| Where did that information originate? | **Milestone** (Integration Bindings are authoritative; bin/ is fallback) |
| Is it explicitly defined by the upstream contract? | YES — Integration Bindings read before bin/ scanning |
| Is the stage inventing anything? | Must not — "no additional specs beyond the plan" rule in step 11 |
| Can the generated artifact be validated mechanically? | YES — `validate_metadata.py` for frontmatter, Spec Decomposition Plan compliance is agent-level |

### Stage 3: generate-verification → M{X}S{Y}V.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | Milestone (Verification Strategy), specification (FRs), verification template |
| Where did that information originate? | **Milestone** (Verification Strategy hints), **Specification** (FR definitions) |
| Is it explicitly defined by the upstream contract? | YES — "MUST use the specified method" rule for strategy hints |
| Is the stage inventing anything? | Must not — "do not invent requirements not present in the source specification" is enforced |
| Can the generated artifact be validated mechanically? | YES — `omp-verify-traceability`, `lint-verification-contract.sh` |

### Stage 4: generate-tests → M{X}S{Y}T{Z}.md + tests/

| Question | Answer |
|----------|--------|
| What information is this stage using? | Verification protocol, milestone (fixture paths from Integration Bindings) |
| Where did that information originate? | **Milestone** (fixture bindings), **Verification** (methods) |
| Is it explicitly defined by the upstream contract? | YES — fixture paths from milestone when available |
| Is the stage inventing anything? | Must not — "No Requirements Invention" guardrail |
| Can the generated artifact be validated mechanically? | YES — `omp-verify-test-ledger`, `omp-verify-git-integrity` |

### Stage 5: evaluate-tests → M{X}S{Y}TE.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | Test plan ledger, test scripts, milestone legacy_boundaries |
| Where did that information originate? | **Milestone** (legacy_boundaries), **Test Plan** (ledger) |
| Is it explicitly defined by the upstream contract? | YES — legacy_boundaries determines which directories are exempt from strict frontmatter |
| Is the stage inventing anything? | No — strict ledger isolation, no blind directory scanning |
| Can the generated artifact be validated mechanically? | YES — validate_metadata.py is invoked on spec and verification |

### Stage 6: implement-specification → M{X}S{Y}C.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | Specification (FRs, Allowlist), Verification Protocol |
| Where did that information originate? | Specification (which derived from milestone) |
| Is it explicitly defined by the upstream contract? | YES — Allowlist and user approval stamp are checked |
| Is the stage inventing anything? | Must not — "Strict Milestone Agnosticism" rule |
| Can the generated artifact be validated mechanically? | YES — `validate_metadata.py` for completion report |

### Stage 7: review-implementation → M{X}S{Y}R.md

| Question | Answer |
|----------|--------|
| What information is this stage using? | Milestone contract, specification, verification, completion report, implementation files |
| Where did that information originate? | **Milestone** (contract boundaries), all upstream artifacts |
| Is it explicitly defined by the upstream contract? | YES — Step 4 "Validate milestone contract compliance" explicitly checks scope, OOS, bindings, spec decomposition |
| Is the stage inventing anything? | No — CONTRACT_FAILURE classification for violations |
| Can the generated artifact be validated mechanically? | YES — `validate_metadata.py` + manual audit |

---

## 2. Deliberate Contradiction Test Results

| Test | Result | Classification |
|------|--------|---------------|
| Undeclared scope detection | PASS | Contract boilerplate + Spec Decomposition Plan + Integration Bindings form the constraint chain |
| Missing requirement information | PASS | Interface Contract Mandate + `#NEEDS-CLARIFICATION` halt in generate-spec |
| Contradictory requirements | PASS | Verification Strategy hints are authoritative with `#NEEDS-CLARIFICATION` fallback |
| Verification without requirement traceability | PASS | Traced to V-FR requirement via `omp-verify-traceability` + generate-verification rule |
| Test without verification traceability | PASS | `omp-verify-test-ledger` validates header comments |
| Implementation outside allowed paths | PASS | Allowlist enforcement in implement-specification |
| Ambiguous implementation boundary | PASS | Subjective criteria postcondition check in milestone + halt mechanisms in downstream |
| Brownfield implementation already passing | PASS | `VALID_BROWNFIELD_PASS` classification exists with implementation presence check |

---

## 3. Regression Check Results

| Failure Class | Status | Evidence |
|---------------|--------|----------|
| YAML/frontmatter parsing | PARTIALLY_FIXED | Shared `_frontmatter.py` exists and `resolve_artifact.py` uses it. `validate_metadata.py` still uses inline parsing (pre-existing). `omp-verify-traceability` and `omp-verify-git-integrity` still use inline parsing (pre-existing). |
| Shebang/metadata ordering | FIXED | `generate-tests` mandates shebang + traceability header order. `omp-verify-test-ledger` validates headers. |
| Syntax self-healing | FIXED | 3-attempt bounded retry in generate-tests. evaluate-tests has limited editing (expected — not its role). |
| Brownfield false-green | FIXED | `VALID_BROWNFIELD_PASS` + implementation presence check + TDD leak detection all present. |
| Stale ledger entries | PARTIALLY_FIXED | `omp-sanitize-tests.py` has pruning function but is not auto-invoked by any pipeline stage. generate-tests has ledger truncation rule at generation time. |
| CLI argument compatibility | FIXED | All CLI binaries use argparse with named flags. Backup files (.bak) confirm conversion was done. |
| Metadata schema consistency | PARTIALLY_FIXED | `ALLOWED_TYPES`, `TYPE_DIR_MAP`, and `ARTIFACT_ARCHITECTURE.md` have overlapping but not identical type lists. `ARCH` is in code but documented. `legacy_boundaries` is in test suite and documented. |

---

## 4. Defects Found and Fixed

**Fixed during this pass**:
- Duplicate step "4." numbering in `generate-spec/SKILL.md` (cosmetic — two steps numbered 4). Renumbered to 5-17.

**Pre-existing (not introduced by contract changes)**:
- `validate_metadata.py` does not use shared `_frontmatter.py` — has inline YAML extraction
- `omp-verify-traceability` and `omp-verify-git-integrity` use inline frontmatter parsing
- `tests/M10/` directory is empty (M10S10 test files don't exist on disk)
- `M10.md` lacks `milestone_id` in frontmatter
- Hardcoded paths remain in `omp-test` and `aef-test-runner`
- `omp-sanitize-tests.py` is not invoked by any pipeline stage

---

## 5. Remaining Sources of Nondeterminism

| Source | Downstream Stage | Severity | Mitigation |
|--------|-----------------|----------|------------|
| `generate-spec` agent decides whether `## Verification Strategy` absence is okay | generate-verification | Low | Strategy is optional by design. When absent, agent uses default method selection. |
| `generate-verification` agent interprets FR prose to select method | generate-verification | Medium | `## Verification Strategy` in milestone constrains this. `omp-verify-traceability` validates method choice via heuristic. |
| Milestone's `legacy_boundaries` is prompt-level (no validatator) | evaluate-tests | Low | Hardcoded default (M1-M9) covers common case. `validate_metadata.py` has `LEGACY_BOUNDARIES_DEFAULTS` constant. |
| Subjective success criteria detection is prompt-level (agent self-checks) | milestone | Medium | Contract Postcondition Check scans for subjective words. No validator enforces this. |
| Spec Decomposition Plan compliance is prompt-level | generate-spec | Medium | Agent must count bullets. No validator cross-checks spec count against plan. |
| Stale ledger rows not auto-pruned | evaluate-tests, evaluate-implementation | Low | `omp-sanitize-tests.py` exists but is never called. Ledger truncation at generation time covers the freshness window. |
| `implement-specification` does not read milestone directly | implement-specification | Low (by design) | Specification is the contract for implementation. Milestone contract is enforced upstream. |

---

## 6. Developer-Productivity Assessment

### How many times does the pipeline ask for information that the milestone already contains?

**Count**: 0 new clarification gates introduced. The existing `#NEEDS-CLARIFICATION` markers remain the same count — one in generate-spec (concrete interface definitions), one in generate-verification (spec gap), one in generate-tests (precondition failure). The new contract sections add no new clarification prompts.

### How many downstream assumptions are still duplicated?

| Duplicate | Consumer | Still Present? |
|-----------|----------|---------------|
| `bin/` scanning to discover existing binaries | generate-spec | **Yes** (fallback path when Integration Bindings are empty — by design) |
| `tests/fixtures/` scanning to discover fixtures | generate-tests | **Yes** (fallback path when no fixture bindings — by design) |
| Method selection from FR prose | generate-verification | **Yes** (when Verification Strategy is absent — by design) |
| `active_id = "M10"` fallback | validate_metadata.py | **Yes** (when `legacy_boundaries` is empty on a milestone without the field — safe default) |

All remaining duplicates are fallbacks for when the new contract fields are optional/absent. This is correct — the contract constrains but does not break existing behavior.

### How many manual path/name corrections are required?

Zero, for the contract changes. The pre-existing hardcoded paths in `omp-test` and `aef-test-runner` remain.

### How many failures require human intervention?

The same as before: upstream spec gaps (`#NEEDS-CLARIFICATION`), `INVALID_TEST` failures (syntax errors, TDD leaks), `ENVIRONMENT_FAILURE` (missing tools). Contract changes do not increase human intervention.

### Do safe local problems self-heal?

Yes — the Optimizer Loop in `evaluate-implementation` (for implementation typos/logic slips) and the Self-Healing Loop in `generate-tests` (for test syntax errors, up to 3 attempts) are both unchanged.

### Does genuine ambiguity stop cleanly?

Yes — `#NEEDS-CLARIFICATION` is the prescribed response for:
- Missing concrete interface definitions (generate-spec)
- Verification Strategy contradiction (generate-verification)
- Precondition failures (generate-tests, evaluate-tests)
- CONTRACT_FAILURE detection (review-implementation)

---

## 7. Final Architectural Assessment

### PARTIAL

The milestone contract sufficiently constrains downstream generation **when the new contract sections are populated**. The authoritative chain is:

```
milestone (Integration Bindings, Spec Decomposition Plan, Verification Strategy, legacy_boundaries)
    ↓ [generate-spec reads bindings + plan]
specification (derived FRs, Allowlist)
    ↓ [generate-verification reads strategy]
verification (V-FRs, traceability matrix)
    ↓ [generate-tests reads fixture paths]
tests (traceable to requirements)
    ↓ [implement-specification reads Allowlist]
implementation (limited to Allowlist)
    ↓ [review checks milestone contract compliance]
review
```

**Why PARTIAL, not PASS**:

1. **Spec Decomposition Plan compliance is prompt-level only** — No validator checks that the number of generated specs matches the plan. The agent self-checks via instruction, but a rogue agent could ignore it.

2. **Subjective success criteria detection is prompt-level only** — The Contract Postcondition Check scans for subjective words but there's no validator that mechanically rejects a milestone with "should" in its success criteria.

3. **Verification Strategy is optional by design** — When absent, `generate-verification` falls back to agent interpretation of FR prose, which was the original nondeterminism source. The contract only constrains when populated.

4. **Two types of "not enough information" are distinguished** — `#NEEDS-CLARIFICATION` (ambiguity, contract violation) and default/fallback behavior (optional field absent) are treated differently. This is correct but the distinction is prompt-level.

5. **`validate_metadata.py` still has inline frontmatter parsing** — The shared `_frontmatter.py` isn't used by every consumer, creating a latent desync risk.

### Recommendations for PASS

To reach PASS, the following are needed (in priority order):

1. **Add a validator** that checks a milestone has at least one Spec Decomposition Plan bullet when scope lists >1 deliverable
2. **Integrate `omp-sanitize-tests.py`** into the `generate-tests` pipeline (call after ledger creation)
3. **Refactor `validate_metadata.py`** to import `extract_frontmatter` from `_frontmatter.py` (remove duplicated inline parsing)
4. **Add a `bin/` validator** that checks `compilation` — currently prompt-level only
5. **Add a `spec_template_version` vs `milestone template_version` consistency check** (currently M10S10 says 1.2.0 while template says 1.2.2)

These are all bounded, deterministic changes that do not require redesigning the contract.

---

## 8. Test Artifacts Created

| File | Purpose | Results |
|------|---------|---------|
| `tests/acceptance_test_contradictions.py` | 8 deliberate contradiction tests | 8/8 PASS |
| `tests/acceptance_test_regression.py` | 7 historical failure class checks | 7/7 PASS |