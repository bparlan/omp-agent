---
id: MILESTONE-M{X}
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


## Spec Layering and Contract Categories

This milestone decomposes into specifications. Each specification MUST own exactly one contract category and MUST NOT redefine the contract category established by this milestone.

| Spec | Ownership | Allowed Contract Categories | Prohibited Contract Categories |
|:-----|:----------|:----------------------------|:-------------------------------|
| S1   | Core artifact infrastructure | Structured Schema, Function/API, CLI Executable | Skill Behavioral |
| S2   | Project configuration | Structured Schema, Filesystem State | CLI Executable for Skills |
| S3+  | Skill integration | Skill Behavioral, Filesystem State | CLI Executable for user-invocable Skills |

Contract categories:

- **Structured Schema Contract** — JSON/YAML schema, frontmatter schema, metadata schema
- **Function / API Contract** — callable interface with typed parameters and return values
- **CLI Executable Contract** — standalone binary or script invoked from shell, with exit codes and stdout/stderr
- **Filesystem State Contract** — observable files/directories/permissions after an operation
- **Skill Behavioral Contract** — observable outcomes after skill invocation, verified by filesystem/artifact state, not by process exit codes

Rules:

- No specification may redefine a `user-invocable: true` Skill as a `CLI Executable Contract`.
- Skill Behavioral Contracts are defined by observable filesystem or artifact outcomes after skill invocation.
- If this milestone describes mode-aware behavior for a Skill, the observable filesystem or artifact outcomes MUST be specified here, not exit codes or stdout JSON.


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
