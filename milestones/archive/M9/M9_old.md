---
id: M9-OLD
type: milestone
status: archived
template_version: 1.0.0

---

# M9 — AEF Artifact-System Integration & Project Workspace Alignment

## Status

Proposed

## Objective

Integrate the canonical artifact architecture established by M9 into the existing AEF/OMP development infrastructure.

This milestone ensures that AEF skills which create, locate, validate, or update artifacts operate consistently with the canonical artifact identity, type, metadata, lineage, storage, and legacy-compatibility rules defined by M9.

The milestone also establishes project-level workspace isolation so that AEF can be used both to develop AEF itself and to bootstrap and maintain independent application projects such as BariaDAO without leaking AEF-specific documentation, metadata, or development artifacts into those projects.

This milestone focuses on **artifact-system integration and workspace correctness**.

It does **not** redesign AEF's higher-level orchestration model.

---

## Architectural Context

M9 established the canonical artifact architecture.

The resulting infrastructure must now be adopted by the skills that interact with artifacts.

The canonical model is:

```
Project
  │
  ├── Project Configuration
  │     └── .omp/config.yml
  │
  ├── Canonical Artifacts
  │     ├── identity
  │     ├── type
  │     ├── metadata
  │     ├── lineage
  │     └── lifecycle state
  │
  ├── Artifact Registry / Type Definitions
  │
  ├── Artifact Resolver
  │
  └── Artifact Metadata Validator
```

Skills are consumers and producers of this model.

They must not independently invent:

* artifact IDs
* artifact types
* artifact storage locations
* metadata schemas
* frontmatter rules
* resolution precedence
* legacy handling
* project boundaries

Those concerns belong to the canonical artifact system.

---

## Legacy Boundaries

This file represents legacy content that has been migrated to the canonical artifact system but is preserved for backward compatibility and historical reference. It contains architectural context and specifications that have been codified in subsequent milestones but remain relevant for understanding the evolution of the AEF artifact system.