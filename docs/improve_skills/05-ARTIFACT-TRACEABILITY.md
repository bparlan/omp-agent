# AEF Artifact Traceability

## Purpose

AEF uses artifact metadata and `derived_from` lineage to mechanically connect generation stages.

Prompt instructions should support this mechanism rather than attempting to replace it with prose.

## Artifact Lineage

The conceptual lineage is:

```text
Milestone
   ↓
Specification
   ↓
Verification
   ↓
Tests
   ↓
Implementation
```

Each artifact should identify its upstream derivation according to the existing artifact schema.

## Example

```yaml
---
id: VER-000
type: verification
title: Template Verification Protocol
milestone_id: M0
status: draft
derived_from: []
template_version: 1.1.0
---
```

The exact metadata schema is governed by the existing AEF implementation and validators.

Do not invent alternate metadata conventions inside a generation skill.

## `derived_from`

`derived_from` provides mechanical lineage between artifacts.

Its purpose includes:

- traceability;
- dependency visibility;
- downstream auditing;
- regeneration;
- provenance;
- preventing orphaned generation artifacts.

A downstream artifact should be traceable to the upstream artifact(s) from which its requirements were derived.

## Prompt vs Mechanical Enforcement

Use prompts for:

- reasoning;
- interpretation;
- responsibility boundaries;
- evidence handling;
- semantic correctness.

Use mechanical enforcement for:

- required metadata;
- valid identifiers;
- schema shape;
- artifact location;
- structural validity;
- lineage format where validators support it.

Do not duplicate mechanical checks with large amounts of prose unless the prose expresses behavior that cannot be mechanically enforced.

## Traceability Invariant

Every important downstream requirement should be attributable to upstream intent or an established project constraint.

Conversely, important upstream requirements should not silently disappear downstream.

A useful conceptual chain is:

```text
milestone requirement
       ↓
specification contract
       ↓
verification condition
       ↓
test evidence
       ↓
implementation behavior
```

The exact artifact IDs and metadata fields are implementation-specific and should follow the existing AEF validators/templates.

## Traceability Failure

If an artifact cannot establish legitimate upstream lineage:

- do not fabricate lineage;
- do not silently attach it to a convenient artifact;
- do not continue merely because the document looks structurally valid.

Use the existing AEF failure/clarification mechanism appropriate to the stage.

## Improvement Guidance

When optimizing generation skills, inspect the existing artifact templates and validators before adding prompt rules about metadata.

The objective is complementary enforcement, not redundant enforcement.
