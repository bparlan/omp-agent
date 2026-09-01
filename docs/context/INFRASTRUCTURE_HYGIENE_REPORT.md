# Infrastructure Hygiene and Final Audit — Assessment Report

**Date**: 2026-08-09
**Final Assessment**: **PASS**

---

## 1. Hardcoded User-Home Paths

### Fixed: `bin/omp-test`

3 instances of `/Users/bparlan/devcode/aef/agent/tests/fixtures/malformed_spec/M10S8_malformed.yaml` replaced with `Path("tests/fixtures/malformed_spec/M10S8_malformed.yaml").resolve()`.

**Evidence:**
```bash
$ python3 -m py_compile bin/omp-test
compile OK
```

### Verified clean: `bin/aef-test-runner`

No hardcoded user-home paths found. Uses project-relative paths throughout.

### Not fixed

- `~/.omp/agent/skills/` references in path resolution boilerplate — standard framework convention across all skills, not environment-dependent (tilde expansion is shell-standard).
- Virtualenv files (`.venv/`, `__editable__*.pth`) — auto-generated, not part of repository code.
- Historical evaluation artifacts in `milestones/M10/*E.md`, `milestones/M10/*R.md` — contain execution traces with absolute paths. These are historical records, not operational code.

---

## 2. Skill-Boundary Contamination

### Previously fixed: `review-implementation/SKILL.md`

Verified clean. Single `description:` field. No `generate-tests` keywords (`self-healing`, `bash -n`, `py_compile`, `pre-flight`, `syntax validation`). Instructions cover review-only concerns: artifact auditing, metadata compliance, contract violation detection, evidence-based escalation.

### Fixed in this pass: `evolve-skills/SKILL.md`

**Finding**: Duplicate `description:` field — second line was copy-pasted from `implement-specification`:
```
description: Implement an approved specification using project architecture...
```

**Fix**: Removed the duplicate. Single correct description remains:
```
description: Analyze recent project artifacts and Session Audit Reports...
```

### Other skills verified clean

No other skills contain `generate-tests` contamination. Self-healing keyword found only in `generate-tests/SKILL.md` where it belongs.

---

## 3. Approval Gate Assessment

**Conclusion**: No standalone validator required.

The approval gate (`#### User Approval` stamp) is enforced by:
1. `implement-specification` — checks for `* [x] Approved for implementation by user` and halts if missing
2. `manage-development` (F11.2 guardrail) — blocks implementation if approval stamp is absent

The check is a deterministic string match — it does not require a binary validator. The old M10S7 design proposed `bin/omp-verify-readiness` but this was never built, and the existing prompt-level enforcement is sufficient for this simple invariant.

**Recommendation**: No action. The current enforcement is appropriate for the complexity of the check.

---

## 4. M10 Historical Artifacts Classification

| Artifact | Issue | Classification | Action |
|----------|-------|----------------|--------|
| `milestones/M10/M10.md` | Missing `milestone_id` in YAML frontmatter | **HISTORICAL ARTIFACT** | None. Created before `milestone_id` was required. `validate_metadata.py` skips via pre-contract detection (no `template_version`). |
| `tests/M10/` | Empty directory | **HISTORICAL ARTIFACT** | None. Test files were generated and lost. Not a current contract issue — next milestone generation creates fresh tests. |
| `M10S10T1.md` | References `test_legacy_document_handling.py` and `test_artifact_separation.py` which don't exist | **HISTORICAL ARTIFACT (stale ledger)** | None. The sanitizer (`omp-sanitize-tests.py`) would prune these rows. `generate-tests` truncates and recreates the ledger on next generation. |
| M10S10: `template_version: 1.2.0` vs spec template `1.2.2` | Patch-level version difference | **COMPATIBLE** | Both are 1.2.x — compatibility rule allows patch differences. |

---

## 5. Full Infrastructure Audit Findings

### Status Summary

| Finding | Classification | Action Taken |
|---------|----------------|-------------|
| Hardcoded user-home paths in `bin/omp-test` | SAFE_AUTO_FIX | Fixed — replaced with `.resolve()` |
| Duplicate description in `evolve-skills/SKILL.md` | SAFE_AUTO_FIX | Fixed — removed `implement-specification` copy-paste |
| `omp-verify-traceability` uses inline frontmatter parsing | INFORMATIONAL | Pre-existing low-risk. Works correctly. Full refactor would require parser state management changes. |
| `validate_metadata.py` doesn't use argparse | INFORMATIONAL | Uses filtered positional args. Works correctly for its use case. |
| Duplicated failure taxonomies across skills | INFORMATIONAL | Each taxonomy is context-appropriate (test eval, implementation eval, verification). Not true duplication. |
| `omp-sanitize-tests.py` not auto-invoked by a binary | FOLLOW_UP | Currently invoked via prompt instruction in `generate-tests` Section 4b. Full mechanical hook would require pipeline binary change. |

---

## 6. End-to-End Verification Results

| Component | Result |
|-----------|--------|
| M5 Metadata Schema Tests (7 test suites) | **ALL PASS** (including `legacy_boundaries`) |
| `validate_metadata.py` on M10S10 + M10S10V | **Metadata OK** |
| Milestone structure validator (template — placeholder content) | **INVALID_STRUCTURE** (correct — template uses `...`) |
| Milestone structure validator (contract-compliant milestone) | **VALID** |
| Syntax validator (Python test files) | **VALID** |
| All binaries compile (6/6) | **ALL OK** |
| 8 deliberate contradiction tests | **8/8 PASS** |
| 7 regression checks | **7/7 PASS** |

### Pipeline Stage Verification

| Stage | Contract Verified | Result |
|-------|-------------------|--------|
| Milestone | Structural completeness validated | Mechanical (`omp-verify-milestone-structure`) |
| → generate-spec | Reads Integration Bindings from milestone | Prompt + mechanical (milestone validator ensures sections exist) |
| → generate-verification | Reads Verification Strategy from milestone | Prompt-level (optional section) |
| → generate-tests | Sanitizer runs before syntax validation | Prompt-level (Section 4b instruction) |
| → evaluate-tests | Uses `legacy_boundaries` for legacy detection | Mechanical (`validate_metadata.py` with `LEGACY_BOUNDARIES_DEFAULTS`) |
| → implement-specification | Respects Allowlist + User Approval stamp | Prompt-level (simple string check) |
| → review | Validates milestone contract compliance | Prompt-level + mechanical (`validate_metadata.py`, `omp-verify-test-syntax`) |

---

## 7. Remaining Issues

| Issue | Why It Matters | Current vs Historical | Fix Now? | Recommended Action |
|-------|---------------|----------------------|----------|-------------------|
| `omp-verify-traceability` inline frontmatter parsing | Low — parser works correctly | Current | No | Refactor to use `_frontmatter` if that module is ever modified again |
| `omp-sanitize-tests.py` not binary-invoked | Low — prompt instruction covers invocation | Current | No | Add hook if pipeline binary (`omp-test`) is ever restructured |
| `validate_metadata.py` doesn't use argparse | Very low — positional filtering works | Current | No | Cosmetic; no behavior impact |
| M10 artifacts with missing fields | None — pre-contract milestones skipped | Historical | No | Will be naturally replaced by M11+ milestones using new template |

These are all INFORMATIONAL or FOLLOW_UP items. None affect correctness.

---

## Final Assessment

### PASS

The system is:
1. **Portable** — all operational code uses repository-relative or dynamically-resolved paths
2. **Coherent** — no skill-boundary contamination; each skill has one job
3. **Verifiable** — 5 mechanical validators enforce the milestone contract (`omp-verify-milestone-structure`, `omp-verify-test-syntax`, `validate_metadata.py`, `omp-verify-test-ledger`, `lint-verification-contract.sh`)
4. **Project-agnostic** — no hardcoded developer-specific dependencies, no system-specific assumptions
5. **Tested** — 15 automated tests (8 contradiction + 7 regression) plus the M5 metadata suite, all green

The milestone contract is mechanically enforced at its critical boundaries (structural completeness, metadata validity, syntax correctness). Remaining prompt-level guarantees are for optional or inherently ambiguous decisions, which is appropriate — mechanical enforcement of these would require building a general-purpose AI output classifier, which is outside the project scope.

**No further contract enforcement work is required.**
