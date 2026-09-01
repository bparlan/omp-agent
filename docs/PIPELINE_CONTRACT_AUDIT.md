# AEF Pipeline Contract Audit: Prepare for Milestone Evolution

**Date**: 2026-08-09
**Scope**: Read-only architectural audit of the AEF/OhMyPi pipeline
**Audit Type**: Contract discovery, source-of-truth mapping, historical failure verification
**READ-ONLY**: No skills, templates, validators, tests, or production code were modified.

---

## 1. Current Pipeline Map

### Forward Flow (SDD Generation & Implementation)

```
milestone
    ↓  M{X}.md (milestone document)
generate-spec
    ↓  M{X}S{Y}.md (specification with FR-1..FR-N)
generate-verification
    ↓  M{X}S{Y}V.md (verification protocol with V-FR-1..V-FR-N, traceability matrix)
generate-tests
    ↓  M{X}S{Y}T{Z}.md (test plan ledger) + tests/M{X}/test_*.sh|.py
evaluate-tests   (Phase 1 — pre-implementation baseline)
    ↓  M{X}S{Y}TE.md (test evaluation report, EXIT_CODE 0|2)
approve-spec
    ↓  User approval stamp in spec frontmatter
implement-specification
    ↓  M{X}S{Y}C.md (completion report)
evaluate-implementation   (Phase 2 — post-implementation optimizer loop)
    ↓  M{X}S{Y}E.md (evaluation report, EXIT_CODE 0|1|2)
review-implementation
    ↓  M{X}S{Y}R.md (review report)
sync-documentation
    ↓  Updated canonical docs
archive-milestone  (11th stage, defined in manage-development)
```

### Support Flow

```
session-audit → M{X}SA{Y}.md
evolve-skills → Updated SKILL.md files
sync-documentation → Updates CHANGELOG.md, MILESTONES.md, ROADMAP.md
```

### Actual Implemented State

Based on M10 artifacts (`milestones/M10/`), the pipeline IS fully implemented through all 11 stages for at least S1–S10. The `tests/M10/` directory is **empty** — no test files physically exist on disk despite the ledger referencing them.

---

## 2. Contract Inventory

### Explicit Contracts (codified in binaries, schemas, or validators)

| Contract | Enforced By | Scope |
|----------|------------|-------|
| Canonical ID format `TYPE-NNN` | `validate_metadata.py` `CANONICAL_ID_PATTERN` | All artifacts |
| Required frontmatter fields (`id`, `type`, `title`, `milestone_id`, `status`) | `validate_metadata.py` | All artifacts |
| 3-tier artifact resolution | `resolve_artifact.py` | Cross-milestone file lookups |
| Conflict detection (dir vs frontmatter type) | `resolve_artifact.py` `detect_conflict()` | Artifact retrieval |
| Test ledger schema (piped markdown table) | `omp-verify-test-ledger` | Test plan files |
| Traceability header comments in test files | `omp-verify-test-ledger` | Test scripts |
| No-prose-contracts linting | `bin/lint-verification-contract.sh` | Verification artifacts |
| Pre-flight existence trap sanitization | `omp-sanitize-tests.py` | Test scripts |
| Git integrity of test artifacts | `omp-verify-git-integrity` | Test files |
| Approval stamp `#### User Approval` / `[x]` | Skill prompt convention (not code) | Specifications |

### Implicit Contracts (prompt-level, no mechanical enforcement)

| Contract | Source | Risk |
|----------|--------|------|
| Milestone has "Scope" (2-5 deliverables) | `milestone` skill, `milestone_template.md` | Prompt-level; no validator checks scope count |
| Specification FRs are "observable boundaries" | `generate-spec` skill | Prompt-level; agent interprets "observable" |
| DOCUMENT_CHECK only for static artifacts | `generate-verification` skill, `omp-verify-traceability` | `omp-verify-traceability` checks this mechanically BUT only via heuristic regex |
| VALID_INITIAL_FAILURE is exit 127 or 1 | All downstream skills | Convention; no validator verifies the exit code semantics |
| Test ledger traceability columns | `generate-tests` skill | Partially enforced by `omp-verify-test-ledger` |
| No placeholder/TODO/FIXME in specs | `generate-spec` skill postcondition (prompt) | Prompt-level; agent self-checks |
| Test files in tests/M{X}/ match ledger | `evaluate-tests`, `evaluate-implementation` skills | Prompt-level ledger isolation rule; no validator cross-checks file existence |

---

## 3. Contract Gaps

### Information downstream stages must currently infer

| Gap | Downstream Consumer | Current Inference Strategy |
|-----|-------------------|---------------------------|
| Milestone scope granularity | `generate-spec` | Agent reads M{X}.md's 2-5 scope items and decomposes into FRs. No mechanical boundary on FR count or depth. |
| Which existing binaries to reuse | `generate-spec` | Agent scans `bin/` directory. No milestone-level declaration of reuse targets. |
| Which test fixtures exist | `generate-tests`, `implement-specification` | Agent scans `tests/fixtures/`. No fixture manifest in milestone. |
| Legacy file boundaries | `validate_metadata.py` | Hardcoded fallback `active_id = "M10"` in `get_active_milestone_id()`. Milestone `scope` doesn't codify legacy ranges. |
| Verification method choice | `generate-verification` | Agent decides SCRIPT_EXECUTION vs DOCUMENT_CHECK from FR prose. `omp-verify-traceability` only checks DOCUMENT_CHECK misuse via a heuristic `is_active` flag derived from regex-grepping the spec for "CLI" keywords. |
| Test file naming conventions | `generate-tests` | Template-determined. Milestone has no naming contract. |
| Allowlist vs Denylist boundaries | `implement-specification` | Specification defines them. Milestone has no pre-contract. |
| What constitutes "implementation-independent" success criteria | `milestone` → `generate-spec` | Entirely agent judgment in current framework. |

---

## 4. Contradictions

### A. Two milestone templates exist with different idioms

| File | Frontmatter | Structure |
|------|------------|-----------|
| `templates/milestone_template.md` | YAML frontmatter (`id: M{X}`, `type: milestone`, `milestone_id: M0`) | Goal, Motivation, Scope, OOS, Success Criteria, Integration Bindings, Risks, Notes |
| `templates/milestone_focus_template.md` | No YAML frontmatter | Property table (`| Property \| Value \|`), Agentic Understanding, Literal Objective, Execution Directives, Strict Scope, Negative Guardrails |

The `milestone` skill references `milestone_template.md`. The `milestone-focus` skill references `milestone_focus_template.md`. They produce fundamentally different artifacts. The `milestone` artifact has type `milestone`, canonical ID, and Integration Bindings section. The `milestone-focus` artifact has no type, no canonical ID, no Integration Bindings — it's a different shape entirely.

### B. The `id:` in M10.md doesn't match the canonical pattern

M10.md has `id: M10` while the canonical spec says IDs should be `TYPE-NNN` format. The milestone itself uses a legacy `M{X}` identifier rather than a canonical ID format.

### C. M10S1.md's `derived_from: [SPEC-001]` references itself

M10S1.md has `derived_from: [SPEC-001]` which is its own `id`. This is circular — a specification derived from itself rather than from the milestone `M10`.

### D. `specification_template.md` lists `derived_from: []` but has no `approval` section

The `specification_template.md` doesn't include the `#### User Approval` section. The downstream `implement-specification` skill requires this stamp. It must be manually appended by agents during generation.

### E. `review-implementation` SKILL.md has duplicate descriptions and mixed content

The frontmatter has two `description:` fields — one for review, one copy-pasted from `generate-tests`. The body interleaves `review-implementation` instructions with `generate-tests` instructions (stale copy-paste contamination).

### F. `evaluate-implementation` analyzes a hardcoded file path in `run_metadata_validation()`

```python
malformed_yaml_path = Path("/Users/bparlan/devcode/aef/agent/tests/fixtures/malformed_spec/M10S8_malformed.yaml")
```
Also references a hardcoded user home path for the error message. `omp-test` has the same hardcoded path.

### G. `omp-verify-test-ledger` has a hardcoded `SPEC_FILE`

```python
SPEC_FILE = "milestones/M10/M10S4.md"
```
This makes the tool non-portable. It will break for any non-M10 milestone.

---

## 5. Source-of-Truth Conflicts

### Concept: "What is a milestone's required structure?"

Defined in **two places**:
1. `templates/milestone_template.md` — 8-section template with YAML frontmatter, Integration Bindings
2. `templates/milestone_focus_template.md` — Property-table format, no canon ID, different sections

**Primary source**: The `milestone` skill (which uses `milestone_template.md`). The `milestone-focus` skill is an alternative entry point with different output shape.

### Concept: "What must a specification contain?"

Defined in:
1. `templates/specification_template.md` — Template with Frontmatter, Objective, Followup Context, FRs, NFRs, Architecture Impact, Data Flow, Implementation Tasks, Constraints, Assumptions, Acceptance Criteria, Next Steps
2. `generate-spec` SKILL.md — Process steps 1-16 that dictate what the spec must include (Interface Contracts, FR IDs, Allowlist, etc.)
3. `ARTIFACT_ARCHITECTURE.md` — Says specifications have `type: specification` and `id: SPEC-NNN`

**These are aligned but with subtle differences**. The template doesn't mention `#### User Approval`, which `implement-specification` requires. The template says `template_version: 1.2.2`, but the actual generated M10S10.md has `template_version: 1.2.0`.

### Concept: "Verification methods"

Defined in:
1. `generate-verification` SKILL.md — Lists 7 methods
2. `omp-verify-traceability` — Hardcodes 6 methods in a set check
3. `verification_template.md` — Mentions but doesn't enumerate

**Conflict**: `omp-verify-traceability` only checks 6 methods (`SCRIPT_EXECUTION`, `UNIT_TEST`, `DOCUMENT_CHECK`, `FILE_STRUCTURE_CHECK`, `FRONTMATTER_CHECK`, `MANUAL_CHECK`). The `generate-verification` skill lists these plus `INTEGRATION_TEST`. The `generate-verification` out-of-scope section prohibits `LEDGER_CHECK`, `TEST_FILE_PLANNING`, `MANUAL_DOCUMENT_CHECK` — meaning the validator and the skill have different lists of allowed methods.

### Concept: "Canonical artifact types"

Defined in:
1. `docs/ARTIFACT_ARCHITECTURE.md` — Lists 8 types
2. `resolve_artifact.py` `TYPE_DIR_MAP` — Maps type to directory name
3. `validate_metadata.py` — Uses a `CANONICAL_ID_PATTERN` regex but doesn't check against an enumerated list of valid types for everything — only has `ALLOWED_TYPES` which isn't synced with ARTIFACT_ARCHITECTURE.md

### Concept: "Canonical ID format"

Defined in:
1. `resolve_artifact.py` — `CANONICAL_ID_PATTERN = re.compile(r"^(SPEC|VER|TEST|INV|COMP|EVAL|REVIEW|AUDIT)-\d+$")`
2. `docs/ARTIFACT_ARCHITECTURE.md` — Same format but doesn't list `ARCH` prefix
3. `validate_metadata.py` — Has `ARCH` in its pattern but `ARCH` isn't in `ARTIFACT_ARCHITECTURE.md`

**Partial conflict**: The `ARCH` (architecture) prefix exists in code but not in the canonical architecture document.

---

## 6. Historical Issue Status

### YAML/frontmatter parsing collisions

**Status**: PARTIALLY_FIXED
**Evidence**: `HF_20260728_ARCH_FRONTMATTER.md` documents creation of shared `_frontmatter.py` module used by both `validate_metadata.py` and `resolve_artifact.py`. However, `omp-verify-traceability` and `omp-verify-git-integrity` still have their own inline frontmatter parsing (duplicated regex logic). The `M10SA1.md` session audit reports continued metadata type inconsistencies (incorrect `type` fields like `completion_report` instead of `completion`).

### Shebang/traceability ordering conflicts

**Status**: FIXED
**Evidence**: The `generate-tests` SKILL.md now mandates shebang + traceability comment headers on line 1 for test scripts. `omp-verify-test-ledger` validates `# {Verification IDs: ...}` and `# {Requirement IDs: ...}` headers.

### Passive syntax failure/deletion

**Status**: PARTIALLY_FIXED
**Evidence**: `HF_20260727_GENERATE_TESTS_FIX.md` documents allowing test file modifications in generate-tests for syntax self-healing (up to 3 attempts). However, `evaluate-tests` and `implement-specification` still freeze on INVALID_TEST — the self-healing only applies within generate-tests. The `tests/M10/` directory is empty, meaning generated test files from M10S10 were deleted or never written, which represents a passive failure.

### Brownfield false-green detection

**Status**: FIXED
**Evidence**: `evaluate-tests` SKILL.md has explicit `VALID_BROWNFIELD_PASS` detection logic. When a test passes with exit 0, the evaluator checks whether the target binary already exists on disk. If it does and has non-trivial logic, the pass is classified as healthy brownfield rather than a TDD leak.

### Stale test ledger entries

**Status**: PARTIALLY_FIXED
**Evidence**: `omp-sanitize-tests.py` has a `prune_stale_ledger_rows()` function that removes ledger rows referencing non-existent test files. However, this tool is a standalone script not integrated into the pipeline — no skill invokes it. The `tests/M10/` directory is empty, but `milestones/M10/M10S10T1.md` still lists `tests/M10/test_legacy_document_handling.py` and `tests/M10/test_artifact_separation.py`. The `generate-tests` skill has a ledger truncation rule ("completely overwrite or truncate any existing file") — but this only guards against stale rows at generation time, not deletion after generation.

### CLI positional-vs-flag mismatches

**Status**: FIXED
**Evidence**: All CLI binaries (`omp-verify-test-ledger`, `omp-verify-git-integrity`, `resolve_artifact.py`, `validate_metadata.py`, `aef-test-runner`) use argparse with named `--flag` arguments. The old `omp-test.bak` and `omp-verify-traceability.bak` backup files suggest the flag conversion was completed.

### Metadata enum/schema inconsistencies

**Status**: STILL_PRESENT
**Evidence**:
1. `validate_metadata.py` has `ALLOWED_TYPES` but `resolve_artifact.py` has `TYPE_DIR_MAP` — these are separate enum lists not synchronized with `ARTIFACT_ARCHITECTURE.md`.
2. `M10S10TE.md` and `M10S10E.md` use `VALID_TESTS` / `INVALID_TESTS` / `ENVIRONMENT_FAILURE` keys that differ from the evaluation template's `VALID_TESTS` / `INVALID_TESTS` naming (template uses `VALID_TESTS` / `INVALID_TESTS` / no `ENVIRONMENT_FAILURE`).
3. Frontmatter `type` field values vary: `completion`, `evaluation`, `review`, `test_set`, `specification`, `verification`, `milestone`, `session_audit`, `architecture`, `hotfix`. No single canonical list unifies them.
4. The `milestone_template.md` has `template_version: 1.1.0`, `specification_template.md` has `template_version: 1.2.2`, `verification_template.md` has `template_version: 1.1.0` — no mechanism ensures these stay current with skills.

---

## 7. Candidate Milestone Responsibilities

Information that logically belongs in the milestone rather than being inferred downstream:

| Responsibility | Currently Handled By | Belongs In Milestone |
|---------------|---------------------|---------------------|
| **Which existing binaries to reuse** | `generate-spec` scanning `bin/` | Milestone should declare `Integration Bindings` with exact binary paths |
| **Test fixture locations** | `generate-tests` auto-discovery | Milestone should list fixture paths |
| **Legacy milestone ranges** | `validate_metadata.py` `get_active_milestone_id()` fallback (`M10`) | Milestone should declare `Legacy Boundaries` |
| **FR → spec decomposition plan** | `generate-spec` agent judgment | Milestone should outline multi-spec plan (currently optional, needs to be required) |
| **Verification method constraints** | `generate-verification` agent decision | Milestone could specify which FRs require SCRIPT_EXECUTION vs DOCUMENT_CHECK |
| **Approval gate criteria** | Downstream `approve-spec` skill | Milestone could define what constitutes approval |
| **Scope enumeration** | Currently in milestone (2-5 deliverables) | Already belongs here — but needs mechanical validation |
| **Acceptance testable by external tool** | Milestone success criteria + downstream tests | Already partially here — but success criteria need observable verbs |
| **File allowlist/denylist** | Specification `Architecture Impact` section | Milestone could define broad boundaries; spec refines per-sequence |

---

## 8. Recommended Change Boundaries

### MILESTONE (changes isolated to `milestone` skill + `milestone_template.md`)

- Make `Integration Bindings` section required (not optional)
- Add `Legacy Boundaries` section declaring which milestone IDs are "legacy"
- Add `Fixture Inventory` section listing fixture paths
- Add `Spec Decomposition Plan` section (multi-spec breakdown) required for milestones with >3 FRs
- Add `FR Inventory` with machine-readable identifiers (FR-1 title, FR-1 method hint)
- Add `Approval Contract` defining what user approval means for this milestone
- Align `milestone-template.md` and `milestone_focus_template.md` to produce same artifact shape
- Remove the duplicate `steps numbered 1 and 2` in milestone SKILL.md (two `Determine Milestone ID` steps)
- Add validator for milestone structure completeness (Scope exists, Integration Bindings exist, etc.)

### DOWNSTREAM SKILLS (changes isolated to individual SKILL.md files)

- `generate-spec`: Read Integration Bindings from milestone instead of scanning `bin/`; read Fixture Inventory; derive specs from multi-spec plan
- `generate-spec`: Add `#### User Approval` section to specification output (currently implicitly added; should be template-enforced)
- `generate-verification`: Read method hints from milestone FR Inventory instead of agent-deciding
- `generate-tests`: Remove `--spec` flag reliance where hardcoded; derive test fixture paths from milestone
- `evaluate-tests`: Use milestone Legacy Boundaries instead of hardcoded `M10` fallback
- `implement-specification`: Expect `Integration Bindings` from spec (which got them from milestone)
- `review-implementation`: Remove copy-pasted `generate-tests` instructions from SKILL.md (confirmed duplicate contamination)

### VALIDATORS (changes isolated to `bin/` python files)

- `validate_metadata.py`: Replace hardcoded `active_id = "M10"` with milestone-aware legacy boundary check; sync `ALLOWED_TYPES` with `TYPE_DIR_MAP` from `resolve_artifact.py` and `ARTIFACT_ARCHITECTURE.md` into single source
- `resolve_artifact.py`: Stay stable (architecture is mature)
- `omp-verify-test-ledger`: Remove hardcoded `SPEC_FILE = "milestones/M10/M10S4.md"` — read from args or derive from milestone context
- `omp-verify-traceability`: Sync allowed verification methods list with `generate-verification` skill (add `INTEGRATION_TEST`); use shared `_frontmatter.py` instead of inline parsing
- `omp-verify-git-integrity`: Use shared `_frontmatter.py` instead of inline parsing
- `aef-test-runner` / `omp-test`: Remove hardcoded user home paths (`/Users/bparlan/...`)

### TEMPLATES (changes isolated to `templates/`)

- `specification_template.md`: Add `#### User Approval` section
- `milestone_focus_template.md`: Add YAML frontmatter and canonical `id`, `type` fields to match `milestone_template.md` output shape
- `milestone_template.md`: Bump `template_version` to reflect new required sections
- `verification_template.md`: Remove `Diff-Scope Verification` section prepopulate (it's an eval concern, not verification)

### TESTS (changes isolated to `tests/` and M{x}S{y}T{z}.md ledgers)

- Tests/M10/ is empty — verify whether M10S10 tests were intentionally cleaned or accidentally lost
- Add integration tests for cross-milestone portaliby (e.g., `omp-verify-test-ledger` with M9 fixtures)
- Add fixture presence assertions between test plan ledger and physical test file existence

### DOCUMENTATION (changes isolated to `docs/`)

- `ARTIFACT_ARCHITECTURE.md`: Add `ARCH` type; sync ALLOWED_TYPES/type enums with code
- `AGENTS.md`: Update handoff matrix to include `milestone-focus` as alternative entry point
- The `review-implementation` SKILL.md needs its duplicate `description:` field merged and the `generate-tests` copy-paste contamination removed

---

## 9. Specific Vulnerabilities Found

### Critical: `tests/M10/` directory is empty

The M10S10 test plan ledger (`M10S10T1.md`) lists `tests/M10/test_legacy_document_handling.py` and `tests/M10/test_artifact_separation.py`. Neither file exists on disk. The directory is empty (`total 0`). This means:
- If `evaluate-tests` runs on M10S10 today, it would find zero test files and fail
- The pipeline's final state shows artifacts that claim completion but physical test files are missing
- Git status shows no staged changes for tests/M10/

### Hardcoded user home paths

Multiple binaries use `/Users/bparlan/devcode/aef/agent/` hardcoded paths:
- `bin/omp-test` line 48: `malformed_yaml_path = Path("/Users/bparlan/devcode/aef/agent/tests/fixtures/malformed_spec/M10S8_malformed.yaml")`
- `bin/omp-test` line 59: Hardcoded in error message
- `bin/aef-test-runner` line 48: Same hardcoded path

### Stale copy-paste contamination in `review-implementation`

The `review-implementation` SKILL.md has merged its own instructions with `generate-tests` instructions. Line 5 has a second description that says "Generate deterministic executable tests strictly from a canonical verification contract" — this is the `generate-tests` description, not `review-implementation`. Lines 34-39 and beyond contain `generate-tests`-era instructions mixed with review instructions. This will confuse the agent about which role it's playing.

### No validator for milestone structural completeness

No tool validates that a milestone has required sections (Goal, Scope, Success Criteria, etc.). The entire validation is prompt-level — agents self-check against the template. A milestone could be produced without an Integration Bindings section and no downstream process would detect it.

### The approval gate has no mechanical validation

The `#### User Approval` stamp check is a prompt instruction within `implement-specification` SKILL.md. There's no standalone validator that checks for this stamp. The `omp-verify-readiness` binary was planned in M10S7 spec but doesn't exist on disk.

---
