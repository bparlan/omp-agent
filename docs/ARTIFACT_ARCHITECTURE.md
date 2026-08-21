---
id: ARCH-001
type: architecture
title: "Canonical Artifact Architecture"
milestone_id: M7
status: active
derived_from: [M7, SPEC-002]
---

# Canonical Artifact Architecture

This document defines the canonical architecture for artifacts within the OMP Agentic Engineering Framework (AEF).

---

## 1. Core Principle

AEF artifacts must clearly delineate between project/workspace namespace, milestone identity, artifact type, artifact identity, artifact lineage, lifecycle state, revision/version, and human-readable title. Filenames must not encode all of these concepts.

The conceptual model is:

```
<project-scope>/
    ↓
    milestone
        ↓
        artifact type
            ↓
            artifact identity
                ↓
                metadata
                    ↓
                    lineage / relationships
```

## 2. Canonical Artifact Types

The following artifact types are defined for the AEF:

| Type ID | Human Name | Description | Producer Skill | Consumer Skill |
|---------|-----------|-------------|----------------|----------------|
| SPEC | Specification | Detailed implementation specification | generate-spec | implement-specification |
| VER | Verification | Protocol defining correctness evaluation | generate-verification | generate-tests |
| TEST | Test Set | Executable test scripts and plans | generate-tests | evaluate-implementation |
| INV | Investigation | Issue investigation findings | investigate-issue | implement-specification |
| COMP | Completion Report | Implementation completion report | implement-specification | review-implementation |
| EVAL | Evaluation | Test execution results and bug fixes | evaluate-implementation | review-implementation |
| REVIEW | Review | Implementation vs specification comparison | review-implementation | manage-development |
| AUDIT | Audit | Session audit records | session-audit | evolve-skills |

### Required Metadata

Every artifact must include YAML frontmatter with the following six fields:
1. `id` — Canonical machine identifier (e.g., `SPEC-001`)
2. `type` — Artifact type from the table above
3. `title` — Human-readable title
4. `milestone_id` — Associated milestone identifier (e.g., `M7`)
5. `status` — Lifecycle state (`draft`, `active`, `completed`, `superseded`)
6. `derived_from` — List of source artifact IDs (lineage)

### Milestone-Specific Optional Fields

Milestone artifacts (`type: milestone`) accept an additional optional field:

1. `legacy_boundaries` — List of milestone IDs that use the pre-canonical artifact format (no YAML frontmatter).
   - Example: `legacy_boundaries: ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"]`
   - When present, `validate_metadata.py` treats files in those milestone directories as legacy-compatible, exempt from strict frontmatter validation.
   - When absent, the hardcoded default legacy boundaries apply (M1-M9).

## 3. Artifact Identity and Naming

Artifact identity is separated from milestone identity. Identifiers are stable and unique within their defined namespace. Semantic qualifiers (e.g., `-CORRECTED`, `-v2`, `-FINAL`) are prohibited in artifact IDs.

### Canonical ID Scheme

The canonical ID format is `TYPE-NNN` where:
- `TYPE` is a four-letter uppercase type prefix (e.g., `SPEC`, `VER`)
- `NNN` is a zero-padded sequential number (e.g., `001`, `002`)

Stable ID prefixes:
- `SPEC-NNN`: Specifications
- `VER-NNN`: Verification protocols
- `TEST-NNN`: Test sets / Test plans
- `INV-NNN`: Investigations
- `COMP-NNN`: Implementation completion reports
- `EVAL-NNN`: Evaluations
- `REVIEW-NNN`: Reviews
- `AUDIT-NNN`: Audits

Numbering is deterministic and sequential within a given type and namespace. Global UUIDs are not introduced unless a requirement for globally distributed artifact identity emerges.

## 4. Canonical Storage Model (Formal Contract)

**This section defines the canonical directory structure contract for AEF artifact storage. All AEF artifacts MUST conform to this structure.**

### Base Path

The base path for all milestone artifacts is:

```
milestones/{M_ID}/
```

Where `{M_ID}` is the milestone identifier (e.g., `M7`, `M8`).

### Artifact Type Subdirectories

Within each milestone directory, artifact type subdirectories are OPTIONAL but when present MUST follow this naming convention:

```
milestones/{M_ID}/
  specifications/     (SPEC-NNN)
  verifications/      (VER-NNN)
  tests/              (TEST-NNN)
  investigations/     (INV-NNN)
  implementations/    (COMP-NNN)
  evaluations/        (EVAL-NNN)
  reviews/            (REVIEW-NNN)
  audits/             (AUDIT-NNN)
```

Each type subdirectory houses artifacts of that type. The directory structure provides deterministic structural context for artifact resolution.

### Contract Enforcement

1. All artifacts MUST have a canonical `id` in their YAML frontmatter.
2. The `id` field MUST match the canonical format (`TYPE-NNN`).
3. Artifacts MAY be placed in type subdirectories for organizational clarity.
4. When an artifact is placed in a type subdirectory, its YAML `type` field MUST be consistent with the directory name.
5. Inconsistencies between directory location and YAML metadata are detected and reported by the artifact resolution system (see Section 6).

## 5. Artifact Lineage and Relationships

Relationships between artifacts are documented through the `derived_from` field in YAML frontmatter. This field contains a list of source artifact IDs that the current artifact was derived from. For example:

```yaml
derived_from:
  - M7
  - SPEC-002
```

The lineage chain is:
```
Milestone → Specification → Verification → Tests → Implementation → Evaluation → Review
```

## 6. Artifact Resolution (3-Tier Priority)

Artifact resolution is performed by `bin/resolve_artifact.py` (implemented per FR-7, FR-9). The resolution system uses a strict 3-tier priority to map an artifact identifier to a file path:

### Tier 1: Explicit YAML Metadata

Scan YAML frontmatter of all `.md` files in the milestone directory tree. If a file's `id` field matches the queried canonical identifier, return that file path immediately.

**Scope**: Canonical IDs only (e.g., `SPEC-001`, `VER-002`).

### Tier 2: Canonical Directory Context

Infer the artifact type from the identifier prefix (e.g., `SPEC-` → `specifications/`, `VER-` → `verifications/`). Search within the corresponding type subdirectory of `milestones/{M_ID}/` for a file whose name contains the identifier.

**Scope**: Canonical IDs only.

### Tier 3: Legacy Filename Heuristics

Apply legacy filename heuristics to match against pre-M10 naming patterns:
- `M{X}S{Y}.md`
- `M{X}S{Y}V.md`
- `M{X}S{Y}T{Z}.md`
- `M{X}S{Y}I{Z}.md`
- `M{X}S{Y}C.md`

**Scope**: Legacy IDs only (e.g., `M7S1`, `M7S1V`).

### Resolution Method Reporting

The resolution method (which tier produced the match) is reported in verbose mode output. This enables consumers to understand which resolution strategy was used.

### CLI Reference

The resolution script is invoked as:

```
python3 bin/resolve_artifact.py <identifier> --milestone <M_ID> [--verbose] [--cwd <path>]
```

| Argument | Description |
|----------|-------------|
| `identifier` | Canonical ID (`SPEC-001`) or legacy ID (`M7S1`) |
| `--milestone <M_ID>` | Target milestone directory (e.g., `M7`) |
| `--verbose` | Print resolution trace to stderr |
| `--cwd <path>` | Base directory containing the milestone subdirectory (used for testing with fixture directories; defaults to the project root) |

Exit codes: `0` = resolved, `1` = not found, `2` = conflict detected.

## 7. Conflict Detection

When a file is resolved through Tier 2 or Tier 3, the resolution system checks that the file's YAML `type` field is consistent with its directory location (per FR-8). If a file at `milestones/M7/specifications/` has `type: verification` in its frontmatter, the system flags this as a conflict and exits with code 2.

The conflict report includes:
- File path
- Expected type (inferred from directory)
- Actual type (from YAML frontmatter)
- Queried identifier

## 8. Lifecycle State and Revision Semantics

Each artifact has defined lifecycle states:

| State | Description |
|-------|-------------|
| `draft` | Initial state, work in progress |
| `active` | Approved and in use |
| `completed` | Final state, no further changes expected |
| `superseded` | Replaced by a newer artifact |

## 9. Completion Reports

Completion reports (`COMP-NNN`) are classified under the `implementations/` type directory. They document the implementation of a specification and include file modification records, test results, and edge case handling.

## 10. References

- FR-6: Canonical directory structure contract (Section 4)
- FR-7: 3-tier resolution priority (Section 6)
- FR-8: Conflict detection (Section 7)
- FR-9: Dual query support (canonical + legacy IDs) (Section 6)
- `bin/resolve_artifact.py`: Resolution implementation
- `bin/validate_metadata.py`: Metadata validation
