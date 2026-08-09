---
id: SPEC-000
type: specification
title: Template Specification
milestone_id: M0
status: draft
derived_from: []
template_version: 1.2.2
---

## Objective

Short summary.

### Milestone Complexity & Multi-Spec Plan

_(Agent Action: Evaluate if this milestone is too large and should be broken into multiple, sequential specifications (e.g., M5S1 for Data/Backend, M5S2 for View/Frontend). If yes, outline the full multi-spec plan here, but ONLY generate the requirements and File Scopes for the current M{X}S{Y} sequence below.)_

---

## Followup Context

_(Include for followup specifications)_

### Derived From

- M{X} (milestone)
- M{X}S{Y-1} (prior specification, if applicable)

### Prior Work Completed

- Summary of completed implementation.

### Remaining Gaps

- What work from the original milestone remains incomplete.

---

## Functional Requirements

- ...

---

## Non-Functional Requirements

- ...

---

## Architecture Impact

### Strict File Scope (Allowlist & Denylist)

_This execution is mechanically constrained to the following files. Any modification outside the Allowlist is a critical failure._

**Allowlist (Files permitted to change):**

- [ ] `path/to/specific_file.ext`

**Denylist (Do NOT Touch):**

- [ ] All `*.html` and `*.css` files (If this is a data/content update only)
- [ ] All `*.json` files (If this is a view/logic update only)

### Affected Modules

- ...

### New Modules

- ...

### Removed Modules

- ...

### Public Interfaces

- ...

---

## Data Flow

If applicable.

---

## Implementation Tasks

1.
2.
3.

---

## Introspection & Code-Search Evidence

- **Workspace Search Queries:** Document the exact semantic search commands executed during the compilation of this specification:
  - [ ] `search_code "<query_1>"` $\rightarrow$ Found: `path/to/file.ext`
  - [ ] `search_code "<query_2>"` $\rightarrow$ Found: `path/to/file.ext`
- **Inspected Signatures:** Document the existing interface contracts or helper functions analyzed before drafting:
  - _E.g., Analysed JSON schema of `bin/omp-discover` to align `bin/omp-test` profiling._

---

## Constraints

- ...

---

## Assumptions

- ...

---

## Acceptance Criteria

- [ ] Checklist

---

## Next Steps

Advise running `generate-verification` to create the verification protocol.
