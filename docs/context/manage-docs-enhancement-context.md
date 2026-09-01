# Manage-Docs Enhancement Context

## Purpose

This document captures the full context for enhancing the AEF DevOps cycle through three coordinated skill updates:
1. `manage-development` — behavioral-vector persona overhaul
2. `manage-roadmap` — enhanced strategic team consolidation
3. `manage-docs` — new operational governance skill

## Current State Analysis

### Tactical Layer (`manage-development`)

**Strengths:**
- Clear 12-stage sequential pipeline
- Team-meet consolidation exists but uses lightweight role-based personas
- Dual recommendation format implemented
- Team consolidation artifacts registered in AEF infra (`team-consolidation` type)

**Gaps:**
- Personas are role-oriented, not behavior-vector-oriented
- No cognitive-shift modeling under pressure
- Team commentary lacks depth of behavioral perspective

### Strategic Layer (`manage-roadmap`)

**Strengths:**
- Roadmap alignment and milestone creation
- `/docs/ingest/` workflow
- Downstream capability validation
- Fact-first code inspections

**Gaps:**
- Personas are lightweight placeholders (TPM, SE, TW)
- No team consolidation with visible commentary
- No dual recommendation format
- No phase-boundary artifact creation

### Operational Layer (MISSING)

**Current State:**
- No skill governs `docs/` folder structure
- `docs/hotfixes/`, `docs/diagrams/`, `docs/solutions/` are ad-hoc
- No intake buffer for unmanaged documents
- No continuous watch mechanism
- `sync-documentation` handles some docs work but lacks governance scope

**Required:**
- New `manage-docs` skill
- Intake buffer (`docs/queue/`)
- Folder governance rules
- Event-driven new file detection
- Operations consolidation artifacts

## Proposed Enhancement: 3-Phase Implementation

### Phase 1: `manage-development` Persona Overhaul

**Goal:** Replace role-oriented personas with behavioral-vector personas

**7 Vector Personas:**

| Persona | Baseline Vector | Under Pressure Shifts To | Optimizes For | Systematically Neglects |
| :--- | :--- | :--- | :--- | :--- |
| **The Auditor** | Stoic | Obsessive | Completeness, traceability, schema compliance | Speed, pragmatic shortcuts |
| **The Critic** | Hostile | Paranoid | Hidden defects, assumption violations, edge cases | Consensus, harmony, "good enough" |
| **The Historian** | Obsessive | Stoic | Pattern matching, precedent, historical accuracy | Novel solutions, breakthrough thinking |
| **The Sentinel** | Aware | Paranoid | Security, boundary enforcement, access control | Convenience, flexibility, user friction |
| **The Pragmatist** | Practical | Stoic | Implementable contracts, maintainability, delivery | Theoretical perfection, elegance |
| **The Skeptic** | Skeptical | Hostile | Testability, evidence requirements, falsifiability | Trust, assumption-making, optimism |
| **The Architect** | Critical | Obsessive | Structure, taxonomy, canonical organization | Ad-hoc solutions, quick fixes |

**Phase-Specific 3-Person Teams:**

| Phase | Team | Rationale |
| :--- | :--- | :--- |
| **Milestone** | The Auditor + The Architect + The Pragmatist | Evidence completeness, structural soundness, practical delivery |
| **Specification** | The Architect + The Skeptic + The Pragmatist | Contract decomposition, assumption challenge, implementability |
| **Verification** | The Skeptic + The Auditor + The Pragmatist | Evidence validation, test quality, practical verification |
| **Tests** | The Critic + The Auditor + The Pragmatist | Failure scenarios, test independence, practical test design |
| **Evaluation/Review** | The Critic + The Skeptic + The Pragmatist | Hidden defects, evidence validation, implementation correctness |
| **Implementation** | The Pragmatist + The Architect + The Critic | Contract execution, architecture integration, defect prevention |

**Deliverables:**
- Updated `skills/manage-development/SKILL.md` with vector personas
- Updated `skills/manage-development/templates/` if needed
- Synced plugin copy
- Updated `skills-ledger.json`

### Phase 2: `manage-docs` Skill Creation

**Goal:** New operational governance skill for `docs/` folder

**Scope:**
- `docs/hotfixes/` — hotfix report intake, classification, archival
- `docs/diagrams/` — diagram drift detection, refresh triggers, versioning
- `docs/solutions/` — solution document cross-reference validation
- `docs/*.md` — official AEF SSD documentation governance
- `docs/queue/` — intake buffer for unmanaged documents

**Intake Buffer Mechanism:**

```
docs/
├── queue/                    ← Unmanaged docs waiting for classification
│   ├── INTake_INDEX.md       ← User-facing view of what's waiting
│   ├── hotfix_20260829_001.md
│   ├── diagram_request.mmd
│   └── solution_note.md
├── hotfixes/                 ← Managed hotfix documents
├── diagrams/                 ← Managed diagrams
├── solutions/                ← Managed solution documents
└── *.md                      ← Official AEF SSD docs
```

**Intake Flow:**
1. File appears in `docs/queue/`
2. `manage-docs` detects it during ops cycle
3. User sees: "3 files waiting for classification"
4. User selects: classify as hotfix/diagram/solution/official
5. File moves to appropriate folder with proper metadata
6. If unknown: user defines new category or rejects

**Trigger Points:**
- Post-`sync-documentation`: validate `docs/` folder state
- Post-`close-milestone`: archive artifacts, update diagrams
- Hotfix detection: `docs/hotfixes/` intake
- Diagram drift: `docs/diagrams/` validation
- Solutions drift: `docs/solutions/` cross-reference validation
- **Continuous watch:** event-driven scan for new files in `docs/`

**7 Vector Personas for Operations:**

| Persona | Baseline Vector | Under Pressure Shifts To | Optimizes For | Systematically Neglects |
| :--- | :--- | :--- | :--- | :--- |
| **The Auditor** | Stoic | Obsessive | Completeness, traceability, schema compliance | Speed, pragmatic shortcuts |
| **The Critic** | Hostile | Paranoid | Hidden defects, assumption violations, edge cases | Consensus, harmony, "good enough" |
| **The Historian** | Obsessive | Stoic | Pattern matching, precedent, historical accuracy | Novel solutions, breakthrough thinking |
| **The Sentinel** | Aware | Paranoid | Security, boundary enforcement, access control | Convenience, flexibility, user friction |
| **The Pragmatist** | Practical | Stoic | Implementable contracts, maintainability, delivery | Theoretical perfection, elegance |
| **The Skeptic** | Skeptical | Hostile | Testability, evidence requirements, falsifiability | Trust, assumption-making, optimism |
| **The Architect** | Critical | Obsessive | Structure, taxonomy, canonical organization | Ad-hoc solutions, quick fixes |

**Operations-Specific Team Assignments:**

| Phase | Team | Rationale |
| :--- | :--- | :--- |
| **Docs Intake** | The Auditor + The Sentinel + The Pragmatist | Completeness, security, implementable classification |
| **Hotfix Governance** | The Critic + The Historian + The Pragmatist | Hidden defects, precedent, practical fixes |
| **Diagram Governance** | The Architect + The Skeptic + The Pragmatist | Structure, testability, maintainable diagrams |
| **Solutions Governance** | The Historian + The Skeptic + The Pragmatist | Pattern matching, evidence, practical solutions |
| **Official Docs** | The Auditor + The Architect + The Pragmatist | Completeness, structure, implementable docs |
| **Folder Hygiene** | The Sentinel + The Auditor + The Pragmatist | Security, completeness, practical organization |

**Artifact Type:** `operations-consolidation`
- Canonical path: `<M_ID>/operations_consolidations/OPS-C-{N}.md`
- Producer: `manage-docs`
- Consumers: `manage-docs`, `sync-documentation`, `close-milestone`

**Deliverables:**
- New `skills/manage-docs/SKILL.md`
- New `skills/manage-docs/templates/` directory
- Artifact type registration in `core/artifacts/artifact_types.py`
- Updated `skills-ledger.json`
- Plugin copy at `/Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/manage-docs/`

### Phase 3: Handoff Contracts & Integration

**Goal:** Establish clear DevOps cycle boundaries and handoff protocols

**Handoff Contracts:**

**Development → Operations:**
```
manage-development → manage-docs:
  "Tactical artifacts ready for documentation.
   Spec M9S2 closed. Evaluation complete.
   docs/ folder validation requested."
```

**Operations → Development:**
```
manage-docs → manage-development:
  "Documentation drift detected.
   Missing diagram for M9S2 config flow.
   Hotfix HF_20260829_001 not referenced in M9S1 closure.
   Requires tactical adjustment."
```

**Roadmap → Development:**
```
manage-roadmap → manage-development:
  "New milestone M9S2 ready for tactical execution.
   Priority: HIGH. Dependencies: M9S1 closed."
```

**Development → Roadmap:**
```
manage-development → manage-roadmap:
  "M9S1 completed with defects.
   Recommend M9S2 priority adjustment.
   New milestone M10 suggested for overflow."
```

**Ops Cycle Integration:**
- Post-`sync-documentation`: `manage-docs` validates `docs/` folder state
- Post-`close-milestone`: artifacts archived/diagrammed/docs-linked
- Hotfix detection: `docs/hotfixes/` intake
- Diagram drift: `docs/diagrams/` validation
- Solutions drift: `docs/solutions/` cross-reference validation
- Continuous watch: event-driven scan for new files in `docs/`

**Deliverables:**
- Updated `skills/manage-development/SKILL.md` with ops handoff points
- Updated `skills/manage-roadmap/SKILL.md` with enhanced personas
- New `skills/manage-docs/SKILL.md` with full ops cycle
- Cross-skill contract documentation
- `docs/queue/` intake directory structure
- Validated circulation flow

## Artifact Registration Requirements

### New Artifact Types

**1. `team-consolidation`** (already registered)
- Path: `<M_ID>/team_consolidations/<SPEC_ID>TC-{N}.md`
- Producer: `manage-development`
- Consumers: `manage-development`, `review-implementation`, `close-spec`

**2. `operations-consolidation`** (new)
- Path: `<M_ID>/operations_consolidations/OPS-C-{N}.md`
- Producer: `manage-docs`
- Consumers: `manage-docs`, `sync-documentation`, `close-milestone`

### Registry Updates Required

**File:** `core/artifacts/artifact_types.py`
- Add `operations-consolidation` to `_RAW_ARTIFACT_TYPE_DEFINITIONS`

**File:** `core/artifacts/registry.py`
- No changes needed; `_ensure_registered_types()` auto-registers new types

## Success Criteria

### Phase 1 Success Criteria
- [ ] `manage-development` personas are behavioral-vector-oriented
- [ ] All 7 vector personas documented with baseline, pressure-shift, optimizes-for, neglects
- [ ] Phase-specific 3-person teams defined for all 6 phases
- [ ] Skill file updated and synced to plugin
- [ ] No regression in existing team consolidation functionality

### Phase 2 Success Criteria
- [ ] `manage-docs` skill created with full operational governance scope
- [ ] Intake buffer mechanism implemented (`docs/queue/`)
- [ ] Event-driven new file detection configured
- [ ] `operations-consolidation` artifact type registered
- [ ] All 7 vector personas defined for operations context
- [ ] Folder governance rules documented
- [ ] Skill file and templates created
- [ ] Plugin copy synced

### Phase 3 Success Criteria
- [ ] Handoff contracts documented between all 3 skills
- [ ] `manage-development` updated with ops handoff points
- [ ] `manage-roadmap` updated with enhanced personas (if proceeding separately)
- [ ] Cross-skill circulation flow validated
- [ ] `docs/queue/` directory structure created
- [ ] End-to-end DevOps cycle tested with M9 or M10

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| Scope creep in `manage-docs` | High | High | Strict scope boundary: `docs/` only, no tactical pipeline |
| Persona redesign breaks existing consolidation | Medium | Medium | Preserve existing report format; only change persona lens |
| Artifact type registration conflicts | Low | High | Verify uniqueness before registration; use `team-consolidation` as template |
| Event-driven scan performance | Medium | Low | Start with manual trigger; add auto-scan only after stable |
| Handoff contract ambiguity | Medium | Medium | Document explicit trigger conditions and artifact formats |

## Dependencies

**Internal:**
- `core/artifacts/artifact_types.py` — artifact type registration
- `core/artifacts/registry.py` — auto-registration mechanism
- `skills/manage-development/SKILL.md` — Phase 1 foundation
- `skills/manage-roadmap/SKILL.md` — Phase 2/3 integration

**External:**
- `milestoner` skill — milestone creation
- `sync-documentation` skill — ops handoff target
- `close-milestone` skill — ops consolidation consumer

## Timeline

**Phase 1:** 1-2 hours (persona rewrite + skill update)
**Phase 2:** 2-3 hours (new skill creation + artifact registration)
**Phase 3:** 1-2 hours (handoff contracts + integration)

**Total:** 4-7 hours of focused implementation

## Recommendation

**Proceed with milestone creation.** This is complex enough to warrant tracked execution, and the 3-phase structure provides natural checkpoints for validation and user review.
