# Milestone Contract Design: Authoritative Downstream Generation Contract

**Design Document** — Pre-implementation specification for milestone evolution.

**READ-ONLY**: This document defines what must change. It does not implement those changes.

---

## Table of Contents

1. [Design Constraints](#1-design-constraints)
2. [Proposed Milestone Contract](#2-proposed-milestone-contract)
3. [Structured Schema Proposal](#3-structured-schema-proposal)
4. [Authority and Precedence Rules](#4-authority-and-precedence-rules)
5. [Downstream Obligations](#5-downstream-obligations)
6. [Clarification Rules](#6-clarification-rules)
7. [Failure Taxonomy](#7-failure-taxonomy)
8. [Compatibility Impact](#8-compatibility-impact)
9. [Migration Strategy](#9-migration-strategy)
10. [Regression Strategy](#10-regression-strategy)
11. [Explicitly Rejected Changes](#11-explicitly-rejected-changes)

---

## 1. Design Constraints

### 1.1 What we're keeping

- The existing **SDD pipeline stages** (`generate-spec` → `generate-verification` → `generate-tests` → etc.)
- The existing **artifact metadata system** (YAML frontmatter with `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`)
- The existing **3-tier artifact resolution** (`resolve_artifact.py`)
- The existing **FR/VER numbering** (FR-1, V-FR-1, etc.)
- The existing **test ledger format** and traceability headers
- The existing **VALID_INITIAL_FAILURE / VALID_TEST / INVALID_TEST** classification semantics
- The existing **validators** (`validate_metadata.py`, `lint-verification-contract.sh`, `omp-verify-test-ledger`)
- The existing **`.md` milestone output format** (no new serialization)

### 1.2 What we're changing

- **Milestone goes from passive requirements document to active downstream contract.**
- `milestone_template.md` and `milestone_focus_template.md` converge to one canonical shape.
- The milestone gains **structured metadata** for the fields downstream stages need most.
- Downstream skills get **explicit obligations** to read specific milestone fields.
- **No** new binary, validator, or runtime CLI for the milestone itself — the contract is in its structure.

### 1.3 What we're NOT changing

- No new schema language (JSON Schema, XML, Protobuf). YAML frontmatter stays.
- No new pipeline stage. The milestone is not a gate; it's a contract.
- No new failure classification codes — we reuse existing.
- No removal of existing validators or templates — we extend and converge.
- No requirement for 100% machine enforcement. Prompt-level contracts are acceptable when mechanical enforcement would cost more than it saves.

### 1.4 Minimality rule

Every change must answer: **"Does a downstream stage currently guess this?"**

If the answer is no — the information is already explicit in the spec, verification, or test plan — we do not add it to the milestone.

---

## 2. Proposed Milestone Contract

### 2.1 Frontmatter (unchanged except `version` field meaning)

Current:
```yaml
id: M{X}
type: milestone
title: Milestone Title
milestone_id: M0
status: draft
derived_from: [user]
template_version: 1.1.0
```

Add one optional field:
```yaml
legacy_boundaries: ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]
```

`legacy_boundaries` enumerates which milestone IDs use the pre-canonical artifact format (no frontmatter, no canonical IDs). This replaces the hardcoded `active_id = "M10"` fallback in `validate_metadata.py`.

Rationale: Hardcoded `"M10"` is a bug waiting to happen. The milestone itself knows which milestones are legacy.

### 2.2 Contract sections (added to template)

The following sections are **REQUIRED** in every milestone. Each section constrains downstream behavior without duplicating implementation detail.

#### A. `## Milestone Contract`

This new root-level section establishes the milestone as a contract:

```markdown
## Milestone Contract

This document is the authoritative contract for milestone M{X}.
Downstream stages SHALL derive their requirements from this document.
Downstream stages MUST NOT introduce behavior, scope, or interfaces
not declared or implied by this document.

Contract violations SHALL emit #NEEDS-CLARIFICATION.
```

This is boilerplate. Every milestone gets the exact same text. It gives downstream agents a mechanical rule to stop on.

#### B. `## Spec Decomposition Plan` (was optional, now REQUIRED)

```markdown
## Spec Decomposition Plan

This milestone decomposes into exactly N specifications:

- M{X}S1 — [one-line title, e.g., "Project Context & Discovery Contract"]
- M{X}S2 — [one-line title]
- ...

Each specification SHALL address exactly the scope in its one-line description.
generate-spec MUST NOT create specifications beyond this plan.
```

**Why**: Currently `generate-spec` decides whether a milestone needs multiple specs and what each one covers. This is agent judgment with no upstream constraint. The user who designs the milestone already knows this decomposition.

**Constraint enforcement**: If a milestone has 10 specs, there are 10 bullet points. If it has 1 spec, there's 1 bullet point. `generate-spec` must follow the plan.

#### C. `## Integration Bindings` (currently optional checkboxes, now REQUIRED table)

Current:
```markdown
- **Existing Tool Dependencies:** List any pre-existing binaries...
  - [ ] E.g., `bin/omp-discover` (from M10S1)
```

Replace with structured table:

```markdown
## Integration Bindings

| Binding Type | Target | Required By Spec(s) | Description |
|:------------|:-------|:--------------------|:------------|
| binary | bin/omp-discover | S1, S2 | Project context discovery |
| binary | bin/omp-verify-metadata | S2, S10 | Artifact metadata validation |
| fixture | tests/fixtures/synthetic_python/ | S1 | Synthetic Python project fixture |
```

**Three binding types**, all optional but when present MUST be exact:
- `binary` — pre-existing executables the implementation must consume
- `fixture` — static test fixture paths
- `interface` — known output schemas or APIs (e.g., JSON schema of `bin/omp-discover`)

**Why**: Currently `generate-spec` scans `bin/` and discovers binaries. `generate-tests` scans `tests/fixtures/` to find fixture paths. Both are agent-driven auto-discovery. The milestone should declare what's available so the agent doesn't guess or miss things.

#### D. `## Verification Strategy` (NEW — optional guidelines)

```markdown
## Verification Strategy

Verification Method Constraints:
- FR-1, FR-2: SCRIPT_EXECUTION (binary must exist)
- FR-3: UNIT_TEST (library function)
- FR-4: DOCUMENT_CHECK (static schema)
```

**Why**: Currently `generate-verification` agent-decides which method to use for each FR. The `omp-verify-traceability` validator then attempts to check this via heuristic regex (grepping for "CLI" in spec text). This section gives deterministic hints.

**Optional**: Not all milestones need this. When absent, `generate-verification` uses its current agent judgment. When present, agent MUST follow the hint or emit `#NEEDS-CLARIFICATION`.

#### E. `## Success Criteria` (unchanged structure, new observability rule)

```markdown
## Success Criteria

- [ ] `bin/omp-discover` exits with code 0 on a valid path
- [ ] `bin/omp-discover` exits with code 1 on an invalid path
- [ ] `bin/omp-discover` produces valid JSON conforming to the schema in M10.md
```

**New invariant**: Every success criterion MUST reference an observable system state or artifact. Criteria using "should", "appropriate", "well-designed", or similar subjective qualifiers are invalid. The milestone builder (agent) MUST stop and ask the user for concrete criteria when only vague wording exists.

This is the most important change. The current milestone template says *"Measurable checklist items defined as observable system states"* but this is prompt-level only. We codify it as a mechanical postcondition: the agent scans its own output for subjective qualifiers and halts.

### 2.3 What stays unchanged

- `## Goal` — unchanged
- `## Motivation` — unchanged
- `## Scope` — unchanged (2-5 deliverables)
- `## Out of Scope` — unchanged
- `## Risks` — unchanged
- `## Notes` — unchanged
- `## Required Negative Guardrails` — unchanged (already effective)

---

## 3. Structured Schema Proposal

### 3.1 Current metadata

Existing YAML frontmatter handles most identity needs. We add ONE optional field:

```yaml
legacy_boundaries: ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]
```

### 3.2 Why not full structured YAML for contract sections?

I considered a fully structured YAML section (e.g., `contract:` with sub-keys for integration bindings, spec decomposition, etc.). **Rejected**, because:

1. It creates a parallel representation to the prose. Every field would need a prose equivalent for human readability, doubling maintenance.
2. It fragments the artifact's primary format (Markdown + frontmatter) into something hybrid.
3. The Integration Bindings table is already Markdown. Adding a YAML equivalent would mean two sources of truth for the same data.
4. M10 upstream already demonstrated that Markdown tables work well for structured data in milestone artifacts.

### 3.3 What the schema covers

| Field | Where | Required | Enforced By |
|-------|-------|----------|-------------|
| `id` | frontmatter | yes | `validate_metadata.py` |
| `type: milestone` | frontmatter | yes | `validate_metadata.py` |
| `title` | frontmatter | yes | `validate_metadata.py` |
| `milestone_id` | frontmatter | yes | `validate_metadata.py` |
| `status` | frontmatter | yes | `validate_metadata.py` |
| `derived_from` | frontmatter | yes | `validate_metadata.py` |
| `legacy_boundaries` | frontmatter | optional | skill prompt + validator update |
| Spec Decomposition Plan | `##` section | yes | skill prompt (postcondition check) |
| Integration Bindings | `##` section | required when public interfaces exist | skill prompt |
| Success Criteria | `##` section | yes | skill prompt (observability check) |

### 3.4 Single authoritative source

After this design, each concept has exactly one canonical location:

| Concept | Canonical Source |
|---------|-----------------|
| Artifact types | `docs/ARTIFACT_ARCHITECTURE.md` + `resolve_artifact.py` TYPE_DIR_MAP (these must be synced) |
| Milestone structure | `templates/milestone_template.md` (one template, not two) |
| FR ID format | Convention (`FR-N`) — no schema needed |
| Verification methods | `generate-verification` SKILL.md — single list |
| Test ledger schema | `omp-verify-test-ledger` — code is schema |
| Failure classifications | This document §7 — single taxonomy |

---

## 4. Authority and Precedence Rules

### 4.1 The chain

```
MILESTONE SECTIONS
    contract (boilerplate)
    spec decomposition plan           ── REQUIRED
    integration bindings              ── REQUIRED when public interfaces exist
    verification strategy             ── OPTIONAL (hints, not requirements)
    success criteria                  ── REQUIRED, must be observable
    scope + out of scope             ── REQUIRED
    |
    constrains │
    v
SPECIFICATION
    derives FRs from milestone scope + decomposition plan
    refines but does not contradict
    
    MAY: add implementation detail (file paths, CLI args, schemas)
    MUST NOT: add scope not in milestone
    MUST NOT: remove deliverables declared in milestone
    
    |
    constrains │
    v
VERIFICATION
    derives V-FRs from specification FRs
    
    MUST: trace every V-FR to an FR
    MUST NOT: invent requirements not in specification
    MUST NOT: assign DOCUMENT_CHECK to requirements the milestone marked as SCRIPT_EXECUTION
    
    |
    constrains │
    v
TESTS
    derives test scripts from verification items
    
    MUST: trace every test to a V-FR and FR
    MUST NOT: create tests for non-existent requirements
    
    |
    constrains │
    v
IMPLEMENTATION
    limited to specification's Strict File Scope Allowlist
    
    MUST NOT: modify tests/
    MUST NOT: create files outside Allowlist
```

### 4.2 Precedence rules

| Rule | Assertion |
|------|-----------|
| PRECEDENCE_1 | Milestone scope is the outermost boundary. No downstream stage may exceed it. |
| PRECEDENCE_2 | A downstream stage MAY refine a contract (add detail, add structure). It MUST NOT contradict it. |
| PRECEDENCE_3 | If a downstream stage contradicts an upstream contract, the upstream contract wins. |
| PRECEDENCE_4 | If two downstream stages disagree, the earlier stage wins (spec > verification > test > implementation). |
| PRECEDENCE_5 | The `Integration Bindings` table is authoritative. If a binary is not listed, it is not a dependency. If a binary is listed, the spec MUST consume it. |
| PRECEDENCE_6 | The `Spec Decomposition Plan` is authoritative. Spec sequences beyond the plan are invalid. |

### 4.3 Contract violation handling

When a downstream stage detects a precedence violation:

1. **If the violation is in the current stage's own output**: Fix it before writing. (Example: generate-spec sees it's creating FRs beyond milestone scope — don't.)
2. **If the violation is in an upstream stage's output**: Emit `#NEEDS-CLARIFICATION` and halt. Do NOT silently expand scope to "fix" the upstream.
3. **If the violation is ambiguous (could be either)**: Emit `#NEEDS-CLARIFICATION`.

---

## 5. Downstream Obligations

### 5.1 `generate-spec` obligations

| Obligation | Source Milestone Field | Current Behavior |
|------------|----------------------|------------------|
| Must follow Spec Decomposition Plan | `## Spec Decomposition Plan` | Agent-decomposes freely |
| Must consume declared Integration Bindings | `## Integration Bindings` | Scans `bin/` directory |
| Must scope FRs to milestone Scope + OOS | `## Scope`, `## Out of Scope` | Agent-estimated (prompt-level) |
| Must reject non-observable success criteria | `## Success Criteria` | No check exists |
| Must add `#### User Approval` section | Not in milestone — convention | Agent must remember |

**New deterministic rules**:
- After generating the spec, scan for `#### User Approval` section. If absent, add it.
- After generating FRs, validate against Spec Decomposition Plan spec count. If extra specs would be required, halt.

### 5.2 `generate-verification` obligations

| Obligation | Source | Current |
|------------|--------|---------|
| Follow Verification Strategy hints | `## Verification Strategy` | Agent-decides method |
| Trace every V-FR to an FR | Spec FR section | Already done |
| Reject DOCUMENT_CHECK for active requirements | Spec FRs + Verification Strategy | Validated by `omp-verify-traceability` (heuristic) |

**New rule**: If `## Verification Strategy` exists and marks FR-1 as SCRIPT_EXECUTION, agent MUST NOT assign DOCUMENT_CHECK. `omp-verify-traceability` should be updated to read the verification strategy from the milestone (future concern).

### 5.3 `generate-tests` obligations

| Obligation | Source | Current |
|------------|--------|---------|
| Use declared fixture paths | `## Integration Bindings` (fixture type) | Agent-scans `tests/fixtures/` |
| Trace to V-FR and FR | Verification traceability matrix | Already done |
| Write full ledger with correct column types | Verification protocol | Already done |
| No pre-flight binary existence traps | Skill instruction | Already enforced |

**New deterministic rule**: Before creating test scripts, read the milestone's Integration Bindings for fixture paths. Use those instead of scanning `tests/fixtures/`. If no fixture bindings exist, fall back to scanning.

### 5.4 `implement-specification` obligations

| Obligation | Source | Current |
|------------|--------|---------|
| Stay within spec Allowlist | Spec Strict File Scope | Already enforced |
| Read Integration Bindings from spec (which got them from milestone) | Spec (derived from milestone) | Agent scans `bin/` independently |
| Do not modify tests/ | Skill instruction | Already enforced |
| Verify user approval stamp exists | Spec `#### User Approval` section | Already enforced |

**No new obligations**. `implement-specification` already has the strongest isolation rules in the pipeline (Allowlist, test isolation, no test modification). It gets its constraints from the specification, not directly from the milestone — that's correct.

### 5.5 `evaluate-tests` obligations

| Obligation | Source | Current |
|------------|--------|---------|
| Read test plan ledger | `{X}S{Y}T{Z}.md` | Already done |
| Classify VALID_INITIAL_FAILURE / INVALID_TEST | Skill instruction | Already done |
| Resolve legacy boundaries | Milestone `legacy_boundaries` frontmatter | Hardcoded `"M10"` fallback |

**New rule**: Read `legacy_boundaries` from the milestone frontmatter. If absent, fall back to the hardcoded `"M10"` (existing behavior). This one-line change eliminates the hardcoded path while maintaining backward compatibility.

### 5.6 `evaluate-implementation` obligations

No new obligations. Already reads from test ledger, not milestone.

### 5.7 `review-implementation` obligations

**Must have its duplicate `generate-tests` instructions removed** (critical: currently the SKILL.md contains copy-pasted test generation instructions embedded in review instructions, which will cause conflicting behavior).

---

## 6. Clarification Rules

### 6.1 When to emit `#NEEDS-CLARIFICATION`

A downstream stage MUST emit `#NEEDS-CLARIFICATION` and halt when:

| Condition | Example |
|-----------|---------|
| **C1**: Required milestone section is absent or empty | `## Integration Bindings` section exists but is empty for a milestone that declares `binary: bin/omp-*` dependencies |
| **C2**: Required field has ambiguous values | `legacy_boundaries: ["M1", "M7", "M10"]` — non-contiguous range |
| **C3**: Contract statements contradict | Spec Decomposition Plan says 3 specs but Integration Bindings reference specs S4-S7 |
| **C4**: Scope expansion would be required | Milestone Scope lists 3 deliverables but any single spec covers all 3 (valid only if 1-spec plan exists) |
| **C5**: Multiple materially different interpretations | "Support both JSON and YAML output" — not clear which is required vs optional |
| **C6**: External interfaces referenced but undefined | Identifier bindings list `bin/omp-discover` but it doesn't exist in `bin/` |
| **C7**: Implementation boundaries unclear | Allowlist in spec says `bin/` but milestone has no Integration Bindings and no existing binaries to consume |
| **C8**: Metadata ambiguity | Milestone has no `legacy_boundaries` and validator can't determine legacy vs active |

### 6.2 When NOT to emit `#NEEDS-CLARIFICATION`

| Condition | Example | Why |
|-----------|---------|-----|
| Existing project convention covers it | Test file naming: `tests/M{X}/test_*.sh` | Convention is well-known |
| Deterministic technical inference works | FR defines `bin/omp-test` → verification method is SCRIPT_EXECUTION | Determined by FR content |
| Optional field is absent and doesn't cause contradiction | No `Verification Strategy` section | Agent falls back to default behavior |
| Upstream ambiguity can be resolved by applying existing convention | Milestone doesn't specify `legacy_boundaries` → default to `["M1"..."M9"]` | Convention exists |

### 6.3 Resolution hierarchy

```
1. explicit contract (milestone → spec → verification → test → implementation)
2. existing project convention (AGENTS.md, ARTIFACT_ARCHITECTURE.md, SKILL.md instructions)
3. deterministic technical inference (FR describes a CLI → method is SCRIPT_EXECUTION)
4. #NEEDS-CLARIFICATION
```

A downstream stage MUST attempt levels 1-3 before falling through to level 4.

---

## 7. Failure Taxonomy

### 7.1 Existing classifications (reuse these)

The following are already defined and in active use by `evaluate-tests` and `evaluate-implementation`:

| Classification | Use | Origin |
|---------------|-----|--------|
| `VALID_INITIAL_FAILURE` | Test failed naturally on blank codebase | evaluate-tests |
| `VALID_BROWNFIELD_PASS` | Test passed because implementation already exists | evaluate-tests |
| `VALID_TEST` | Test correctly exercises its subject | evaluate-tests, evaluate-implementation |
| `INVALID_TEST` | Test is defective (syntax, self-scanning, false-pass) | evaluate-tests, evaluate-implementation |
| `ENVIRONMENT_FAILURE` | Missing system utility (git, pytest, etc.) | evaluate-tests, evaluate-implementation |
| `TDD_LEAK` | Implementation check passes prematurely on blank codebase | evaluate-tests |
| `VALIDITY_FAILURE` | Structural problem (syntax error, NUL bytes, wrong shebang) | evaluate-tests |

### 7.2 New classifications

These are the minimal additions needed, based on audit findings:

| Classification | Definition | Raisable By |
|---------------|-----------|-------------|
| `CONTRACT_FAILURE` | A downstream artifact contradicts an upstream contract | generate-spec, generate-verification, generate-tests, implement-specification |
| `AMBIGUITY` | Required information exists but has multiple materially different interpretations | Any stage |

**Rationale for not introducing the full proposed taxonomy**:

The audit proposed `PRECONDITION_FAILURE, CONTRACT_FAILURE, SPECIFICATION_FAILURE, VERIFICATION_FAILURE, TEST_GENERATION_FAILURE, TEST_EXECUTION_FAILURE, IMPLEMENTATION_FAILURE, VALIDATION_FAILURE, ENVIRONMENT_FAILURE, TOOLING_FAILURE, AMBIGUITY`.

Of these:
- `ENVIRONMENT_FAILURE` already exists
- `VALIDITY_FAILURE` covers spec/test structural issues
- `INVALID_TEST` covers test-level failures
- The remaining granularity (SPEC vs VERIFICATION vs TEST_GENERATION vs IMPLEMENTATION) is already implicit in which stage detected the failure — no new code needed
- `TOOLING_FAILURE` is too vague to be actionable
- `PRECONDITION_FAILURE` is the same as `VALIDITY_FAILURE` with more specific context — not distinct enough

### 7.3 Recovery classifications

| Classification | Definition | Used By |
|---------------|-----------|---------|
| `SAFE_AUTO_FIX` | Bug is a minor logic slip, typo, or import — can be corrected without changing the contract | evaluate-implementation (Optimizer Loop) |
| `NEEDS_CLARIFICATION` | Blocking ambiguity or contract violation — human must decide | Any stage |
| `BLOCKED` | Pipeline cannot proceed past this point without upstream repair | Any stage |

`SAFE_AUTO_FIX` is already implemented by evaluate-implementation's Optimizer Loop.
`NEEDS_CLARIFICATION` is already defined in AGENTS.md.
`BLOCKED` is already the natural state when a gate fails.

### 7.4 Classification mapping

```
Downstream discovers contract violation
    │
    ├─ Violation fixable by deterministic rule? → SAFE_AUTO_FIX
    │
    └─ Violation not fixable by deterministic rule?
        │
        ├─ Violation is a contradiction → CONTRACT_FAILURE → #NEEDS-CLARIFICATION → BLOCKED
        │
        └─ Violation is an ambiguity → AMBIGUITY → #NEEDS-CLARIFICATION → BLOCKED
```

---

## 8. Compatibility Impact

### 8.1 Artifact impact

| Artifact | Change | Breaking? |
|----------|--------|-----------|
| `milestone_template.md` | Add `Milestone Contract` section, `Spec Decomposition Plan`, structured `Integration Bindings`, `Verification Strategy`, observability rule for Success Criteria | NO — all additions are optional within the template; existing milestones still parse |
| `M10.md` | Would need updated Integration Bindings format and Spec Decomposition Plan | NO — existing M10.md works without changes; new milestones use new format |
| `M9.md` and earlier | Unchanged | NO — covered by `legacy_boundaries` |

### 8.2 Skill impact

| Skill | Change Required | Scope |
|-------|----------------|-------|
| `milestone` SKILL.md | Add instructions for new template sections; remove duplicate steps | Single file |
| `milestone-focus` SKILL.md | Reference `milestone_template.md` instead of `milestone_focus_template.md` | Single file |
| `generate-spec` SKILL.md | Read Integration Bindings from milestone; follow Spec Decomposition Plan | Prompt-level additions |
| `generate-verification` SKILL.md | Read Verification Strategy hints from milestone if present | Prompt-level addition |
| `generate-tests` SKILL.md | Read fixture paths from milestone Integration Bindings | Prompt-level addition |
| `evaluate-tests` SKILL.md | Read `legacy_boundaries` from milestone frontmatter | Prompt-level addition |
| `implement-specification` SKILL.md | No change — already reads from spec, not milestone | — |
| `evaluate-implementation` SKILL.md | No change | — |
| `review-implementation` SKILL.md | Remove copy-pasted `generate-tests` contamination | Cleanup |

### 8.3 Validator impact

| Validator | Change Required | Breaking? |
|-----------|----------------|-----------|
| `validate_metadata.py` | Accept `legacy_boundaries` in frontmatter; remove hardcoded `active_id = "M10"` fallback | NO — new field is optional; fallback remains when field absent |
| `omp-verify-traceability` | Add `INTEGRATION_TEST` to allowed methods; use shared `_frontmatter.py` | NO — additive change |
| `lint-verification-contract.sh` | No change | — |
| `omp-verify-test-ledger` | Remove hardcoded `SPEC_FILE = "milestones/M10/M10S4.md"` | NO — reading from args |
| `omp-sanitize-tests.py` | No change | — |
| `resolve_artifact.py` | No change (architecture is mature) | — |
| `aef-test-runner` / `omp-test` | Remove hardcoded `/Users/bparlan/...` paths | NO — path resolution should be relative or passed |

### 8.4 Template impact

| Template | Change |
|----------|--------|
| `milestone_template.md` | Add new contract sections; bump `template_version` to 2.0.0 |
| `milestone_focus_template.md` | Retire or converge to use `milestone_template.md` shape (add YAML frontmatter, canonical fields) |
| `specification_template.md` | Add `#### User Approval` section |
| `verification_template.md` | Remove `Diff-Scope Verification` prepopulate (addressed by evaluate-implementation, not verification) |
| `test_template.md` | No change |
| `evaluation_template.md` | No change |
| `review_template.md` | No change |
| `completion_template.md` | No change |

### 8.5 Documentation impact

| Document | Change |
|----------|--------|
| `docs/ARTIFACT_ARCHITECTURE.md` | Add `ARCH` type to type table; sync ALLOWED_TYPES with `validate_metadata.py`; document `legacy_boundaries` frontmatter field |
| `docs/PIPELINE_CONTRACT_AUDIT.md` | Already written (this audit) |
| `docs/AGENTS.md` | Update handoff matrix; add clarification rules from §6 |

---

## 9. Migration Strategy

### 9.1 Principles

1. **No existing milestone is modified.** Past milestones (M1-M10) keep their current format. `legacy_boundaries` covers them.
2. **New milestones (M11+) use the new template.** The transition is natural — the next `milestone` invocation picks up the updated template.
3. **The `milestone_focus_template.md` becomes an alias** for the main `milestone_template.md` rather than a separate shape. This eliminates the structural contradiction.
4. **Validators accept both old and new format.** The `legacy_boundaries` field is optional. Existing behavior is the fallback.

### 9.2 Step-by-step migration

```
Phase A: Template + Skill (single change)
    └─ Update milestone_template.md with new sections
    └─ Update milestone-focus to reference milestone_template.md
    └─ Update milestone SKILL.md to drive the new template
    └─ Remove duplicate "Determine Milestone ID" steps

Phase B: Validator update (single change)
    └─ validate_metadata.py: add legacy_boundaries support
    └─ omp-verify-test-ledger: remove hardcoded SPEC_FILE
    └─ omp-test + aef-test-runner: remove hardcoded user home paths

Phase C: Downstream skill updates (independent changes)
    └─ generate-spec: add Integration Bindings reading
    └─ generate-verification: add Verification Strategy reading
    └─ generate-tests: add fixture path reading from milestone
    └─ evaluate-tests: add legacy_boundaries reading

Phase D: Cleanup (independent, can be done anytime)
    └─ review-implementation: remove duplicate generate-tests content
    └─ omp-verify-traceability: add INTEGRATION_TEST; use shared _frontmatter.py
    └─ docs/ARTIFACT_ARCHITECTURE.md: add ARCH type; sync enums
    └─ specification_template.md: add User Approval section

Phase E: First new milestone (verification)
    └─ Create M11 using new template
    └─ Run full SDD pipeline
    └─ Verify no regressions in M1-M10
```

### 9.3 No migration for legacy milestones

Milestones M1-M9 (and M10 as-is) remain in their current format. The `legacy_boundaries` field in new milestones tells validators not to enforce canonical schema on them. This is the same approach M10S10 already established for legacy document handling — we extend it to work by milestone declaration rather than hardcoded constants.

---

## 10. Regression Strategy

### 10.1 What to test

| Test | What It Catches | Existing Coverage |
|------|----------------|-------------------|
| Validate all M1-M10 artifacts against `validate_metadata.py` | Schema regression for legacy milestones | No — M5 test_metadata_schema.py tests generic schema, not real artifacts |
| `resolve_artifact.py` against M10 identifiers | Resolution regression | No dedicated test exists |
| `omp-verify-test-ledger` against M10 ledgers | Ledger parsing regression | M4 test_state_machine.py has placeholder tests only |
| Full SDD pipeline on new milestone | End-to-end contract enforcement | No — M5/M6 tests are unit-level |
| `generate-spec` with Integration Bindings | Milestone-to-spec data flow | No |
| No milestone artifacts outside designated path | Scope enforcement | No |
| `legacy_boundaries` acceptance in validator | Schema extension | No |

### 10.2 Required regression tests

The following tests MUST be created or updated before milestone contract implementation is considered complete:

1. **`tests/M5/test_metadata_schema.py`** — Add test that validates all existing milestone artifacts (M1-M10) pass `validate_metadata.py`. Currently this file tests abstract metadata objects but never runs against real artifacts.

2. **`tests/M9/test_artifact_resolution.sh`** — Currently tests resolution logic. Add test case for resolution with `legacy_boundaries` being read from milestone frontmatter.

3. **`tests/M10/`** — Populate with the M10S10 test files that are currently missing. These are essential regression tests. The empty `tests/M10/` directory is a critical pipeline gap.

4. **New test suite: `tests/M11/`** — A full end-to-end integration test against a new milestone using the updated template. This would be the authoritative regression suite.

### 10.3 Mitigation strategy

| Risk | Mitigation |
|------|-----------|
| New template breaks existing milestone agents | Template section additions are optional in parse terms. Existing agents that don't fill them produce milestones without those sections. Validators accept both. |
| `legacy_boundaries` field missed by downstream validators | The field is a hint, not a requirement. Default `active_id = "M10"` fallback stays. |
| Spec Decomposition Plan too constraining for complex milestones | Agent can emit `#NEEDS-CLARIFICATION` if the plan is too rigid. Human revises. Plan is limited to N bullet points — zero structural risk. |
| Integration Bindings duplication (agent ignores and re-scans `bin/`) | Both sources will align for correct agents. The binding is advisory for the same reason M10 avoids mechanical CPAs: the prompt is the enforcement mechanism for data that changes with every milestone. |

---

## 11. Explicitly Rejected Changes

| Change | Reason for Rejection |
|--------|---------------------|
| **Full YAML schema for integration bindings** | Duplicates Markdown table. Adds a second source of truth. No mechanical advantage for data that doesn't need cross-file reference. |
| **New CLI binary for milestone validation** | The milestone is a planning artifact, not a runtime tool. Validating it through prompt-level postconditions is correct — the agent reads its own output. |
| **Machine-enforced FR count** | Milestone scope is 2-5 deliverables but each deliverable may produce multiple FRs in the spec. The count is a guideline, not a lock. Mechanical enforcement would incorrectly reject valid specs. |
| **Automatic cross-milestone dependency graph** | Currently each milestone is self-contained. Introducing cross-milestone resolution would require a new artifact type. The 3-tier resolver handles this when needed. |
| **Removing `milestone-focus` as a concept** | The skill serves a different use case (literal checklist translation without interactive elicitation). It should converge to the same output shape, not be removed. |
| **Adding verification method constraints as frontmatter** | The `## Verification Strategy` section as Markdown prose is readable, editable, and checkable. Frontmatter would require a new schema and create a second location for the same information. |
| **UUID-based milestone IDs** | `M{X}` is the existing convention across all M1-M10 artifacts. Changing to UUIDs would require renaming every artifact. No benefit gained. |
| **Global FR numbering across milestones** | FR-1 inside M10 and FR-1 inside M11 are unrelated. Global numbering would require cross-milestone coordination that doesn't exist. The existing per-spec FR numbering is correct — `M10S1 FR-1`, `M10S2 FR-1`. |
| **Removing `Out of Scope` section** | It's the most effective scope-limiting mechanism in the current milestone. Removing it would increase downstream guesswork. |
| **Requiring `Verification Strategy` section** | Not all milestones need it. The 10-spec M10 had an implicit strategy that worked. Making it required would force unnecessary detail on simple milestones. |
| **Adding milestone-level test count or coverage targets** | Test coverage is a verification concern, not a planning concern. The milestone should constrain what, not how many. |
| **Adding risk mitigation section** | Risks are in the milestone. Mitigation strategies belong in the specification and implementation. Bloating the milestone with mitigation prose contradicts the "what not how" rule. |

---

## Appendix: Rationale for Each Audited Contract Gap

| Audit Finding | How This Design Addresses It |
|---------------|------------------------------|
| Milestone scope granularity not mechanically bounded | Spec Decomposition Plan (section 2.2.B) constrains spec count and scope per spec. Still prompt-level but now agent has explicit bullets to follow. |
| Existing binaries discovered by `generate-spec` scanning `bin/` | Integration Bindings (section 2.2.C) declares them exactly, removing the scan. |
| Test fixtures discovered by `generate-tests` scanning `tests/fixtures/` | Integration Bindings fixture type declares paths (section 2.2.C). |
| Legacy boundaries hardcoded as `active_id = "M10"` | `legacy_boundaries` frontmatter field (section 2.1) moves this to the milestone. |
| Verification method agent-decided | Optional Verification Strategy (section 2.2.D) provides hints; clarification semantics (section 6) catch contradictions. |
| Allowlist/Denylist defined only in spec | Spec derives from milestone scope+OOS. Not moved to milestone because per-sequence paths are implementation details. |
| `review-implementation` contaminated with `generate-tests` | Called out as Phase D cleanup (section 8.2). |
| Hardcoded paths in binaries | Called out as Phase B validator update (section 9.2). |
| `milestone_focus_template.md` different shape | Converged to `milestone_template.md` shape (section 3.4). |