---
id: M9
type: milestone
title: "M9 — Simplified AEF Artifact-System Integration"
milestone_id: M9
status: draft
derived_from:
  - M9
supersedes: []
template_version: 1.0.0
---

# M9 — Simplified AEF Artifact-System Integration

## Status

Draft — Single-Mode Philosophy

## Objective

Establish a **minimal, stable artifact architecture** for AEF by integrating canonical artifact management into existing skills without introducing complex mode-aware systems.

**Core Philosophy:** Keep infrastructure **stable and minimal**. A single, consistent artifact system for all projects.

---

## Motivation

The original M9 proposal included a dual-mode bootstrapping system (Framework vs Application) that added unnecessary complexity. If AEF tooling is needed, use AEF directly—not a simplified application mode. The complexity of two modes isn't justified.

**Simplified Approach:**

- Single mode for all projects
- Consistent artifact creation protocol
- Standard project configuration
- Minimal optional enhancements

---

## Scope

### In Scope

### 1. Core Artifact Infrastructure

Integrate the canonical artifact architecture established by M9S1 into AEF skills.

**Components:**

- **Artifact Registry**: Centralized type definitions and storage rules
- **Artifact Resolver**: Unified resolution mechanism (replaces hardcoded paths)
- **Artifact Metadata Validator**: Single validation authority
- **Canonical Artifact Types**: Standard definitions (milestone, spec, verification, test, completion, evaluation, review, closure)

**Integration Points:**

- `generate-spec` → Creates spec artifacts via canonical protocol
- `generate-verification` → Uses canonical metadata validator
- `generate-tests` → Persists tests as canonical artifacts
- `implement-specification` → Integrates with artifact registry
- `review-implementation` → Validates against canonical contract

### 2. Standard Project Configuration

Establish a minimal project configuration system.

**`.omp/config.yml` Schema:**

```yaml
project_id: <unique-identifier>
project_slug: <url-safe-name>
version: <semantic-version>
```

**Note:** Project configuration is intentionally minimal. No mode field, no technology stack declaration. Configuration evolves as needed.

### 3. Artifact Lifecycle Integration

Ensure skills create artifacts through the canonical 7-step protocol:

1. Determine artifact type
2. Assign/request canonical identity
3. Generate required metadata
4. Write canonical frontmatter
5. Place in canonical storage location
6. Validate resulting artifact
7. Report created artifact

### 4. Legacy Compatibility

Existing artifacts remain readable. New artifacts use canonical rules. No mass migration.

---

### Out of Scope

**Removed from Original M9:**

- ❌ Dual-mode bootstrapping (Framework vs Application)
- ❌ Mode-specific artifact generation rules
- ❌ Mode-conditioned documentation rules
- ❌ Technology stack detection
- ❌ Application-specific agent guidance generation
- ❌ Project-mode switching

**Rationale:** Complex mode logic isn't needed for basic AEF usage. If AEF tooling is needed, use AEF directly.

---

## Specifications

Sequential spec ownership for this milestone:

- **M9bS1** — Core artifact infrastructure integration: Registry, Resolver, Validator, Types
- **M9bS2** — Standard project configuration: `.omp/config.yml` schema and validation
- **M9bS3** — Skill integration: How affected skills consume canonical APIs

---

## Functional Requirements

### FR-1 — Canonical Artifact Contract Adoption

All artifact-producing and artifact-consuming skills must use the M9 canonical artifact model.

**Acceptance Criteria:**

- No competing canonical artifact schemas
- Artifact decisions originate from canonical system
- Skills consume canonical metadata, not filenames

### FR-2 — Canonical Artifact Resolution

Affected skills must resolve artifacts through the canonical resolver.

**Acceptance Criteria:**

- No hardcoded milestone-specific paths
- Resolution works with canonical storage model
- Failures are explicit and actionable

### FR-3 — Canonical Artifact Creation

All artifact-producing skills must create artifacts conforming to canonical metadata contract.

**Acceptance Criteria:**
Every successful creation includes:

- Canonical identity
- Canonical type
- Required metadata
- Valid frontmatter
- Canonical storage
- Successful validation

### FR-4 — Standard Project Configuration

`bootstrap-project` creates minimal project configuration.

**Acceptance Criteria:**

```
.omp/config.yml
```

contains valid project configuration.

### FR-5 — Artifact Validation Before Completion

Artifact-producing skills must validate output before reporting completion.

**Acceptance Criteria:**

- Invalid artifacts cause skill failure
- Partial creation is not reported as success
- Validation through canonical validator

### FR-6 — Legacy Compatibility

Existing artifacts remain readable.

**Acceptance Criteria:**

- No automatic mass-migration
- Legacy artifacts discoverable via resolution
- New artifacts use canonical rules

---

## Negative Requirements

The implementation MUST NOT:

1. Redesign AEF orchestration
2. Introduce autonomous orchestration engine
3. Modify OMP internal agent implementations
4. Create competing artifact registries
5. Create competing metadata validators
6. Require immediate migration of all historical artifacts
7. Infer artifact type exclusively from filenames
8. Silently fabricate missing relationships
9. Treat file creation as successful artifact creation without validation
10. Introduce complex mode-aware bootstrapping logic

---

## Verification Strategy

### Level 1 — Artifact Contract

Verify:

- Identity
- Type
- Metadata
- Frontmatter
- Relationships
- Lifecycle state

### Level 2 — Skill Integration

Verify:

- Resolution
- Creation
- Validation
- Artifact lifecycle

### Level 3 — Integration Testing

Verify canonical artifact system integrates correctly with existing skills.

---

## Success Criteria

M9b is complete when:

1. AEF skills consume the M9 canonical artifact model
2. Canonical resolution replaces skill-specific path guessing
3. Artifact creation produces validated canonical artifacts
4. Metadata validation occurs before successful completion
5. `.omp/config.yml` establishes minimal project configuration
6. New milestones are canonical artifacts
7. Legacy artifacts remain readable
8. No competing artifact registries introduced
9. Integration tests execute in isolated fixtures

---

## Implementation Order

```
1. Confirm M9 canonical artifact APIs
       ↓
2. Integrate canonical resolver
       ↓
3. Integrate canonical metadata validator
       ↓
4. Update artifact creation primitives
       ↓
5. Update milestone creation
       ↓
6. Update generate-spec
       ↓
7. Update generate-verification
       ↓
8. Update generate-tests
       ↓
9. Update implement/evaluate/review consumers
       ↓
10. Verify integration
```

---

## Comparison: M9 vs M9b

| Aspect           | M9 (Original)                | M9b (Simplified)     |
| ---------------- | ---------------------------- | -------------------- |
| Mode System      | Dual (Framework/Application) | Single (Standard)    |
| Bootstrapping    | Mode-aware routing           | Standard protocol    |
| Complexity       | High                         | Low                  |
| Configuration    | Complex `.omp/config.yml`    | Minimal config       |
| Documentation    | Mode-specific rules          | Standard rules       |
| Enhancement Path | Built-in modes               | Optional future work |
| Effort           | High                         | Moderate             |
| Maintenance      | Dual code paths              | Single code path     |

---

## Rationale

### Why Remove Dual-Mode System?

1. **Unnecessary Complexity**: Two code paths to maintain
2. **Minimal Benefit**: Basic AEF usage doesn't need mode differentiation
3. **OMP Integration**: If AEF tooling is needed, use OMP directly
4. **User Request**: "I don't need two mode implementations"
5. **Stability Focus**: Keep infrastructure minimal and stable

### What We Keep

- Core artifact infrastructure (registry, resolver, validator, types)
- Standard 7-step creation protocol
- Minimal project configuration
- Legacy compatibility
- Skill integration via canonical APIs

### Future Enhancements (Optional)

If complex mode logic is later needed:

1. Add mode field to `.omp/config.yml`
2. Implement mode-specific handlers as optional modules
3. Keep core behavior standard for all modes

---

## Completion Gate

M9b may not be considered complete merely because modified skills execute.

Completion requires evidence that:

```
canonical artifact contract
        ↓
canonical resolver
        ↓
canonical validator
        ↓
skill integration
        ↓
legacy compatibility
        ↓
integration testing
```

all operate consistently.

---

## Notes

- M9b is a simplification of M9, not a replacement
- If M9S1 infrastructure is already implemented, M9b focuses on integration
- Removed features (dual-mode) can be added as optional enhancements if needed
- Goal: Stable, minimal, maintainable artifact system
