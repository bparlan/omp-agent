---
id: M{X}
type: milestone
title: Milestone Title
milestone_id: M0
status: draft
derived_from: [user]
legacy_boundaries: []
template_version: 2.0.0
---

# Milestone M{X}

## Milestone Contract

This document is the authoritative contract for milestone M{X}.
Downstream stages SHALL derive their requirements from this document.
Downstream stages MUST NOT introduce behavior, scope, or interfaces
not declared or implied by this document.
Contract violations SHALL emit #NEEDS-CLARIFICATION.

---

## Goal

One concise objective.

---

## Motivation

Why this milestone exists.

---

## Spec Decomposition Plan

This milestone decomposes into exactly N specifications:

- M{X}S1 — [one-line title]
- M{X}S2 — [one-line title]

Each specification SHALL address exactly the scope in its one-line description.
generate-spec MUST NOT create specifications beyond this plan.

---

## Scope

- ...

---

## Out of Scope

- ...

---

## Success Criteria

- [ ]

NOTE: Every success criterion MUST reference an observable system state or artifact.
Criteria using subjective qualifiers (should, appropriate, well-designed) are invalid.

---

## Integration Bindings

| Binding Type | Target | Required By Spec(s) | Description |
|:------------|:-------|:--------------------|:------------|
| binary | bin/command | S1 | Existing CLI tool this milestone consumes |
| fixture | tests/fixtures/path/ | S1 | Static test fixture directory |
| interface | output-schema | S2 | Known API or output contract |

Binding types: binary (pre-existing executable), fixture (static test data), interface (output schema).
When empty, downstream stages discover dependencies via code-search or convention.

---

## Verification Strategy

Verification Method Constraints:
- FR-1: SCRIPT_EXECUTION (binary must exist)

Optional. When present, generate-verification MUST follow these hints
or emit #NEEDS-CLARIFICATION.

---

## Risks

- ...

---

## Notes

- Optional implementation-independent observations.
