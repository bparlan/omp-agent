# Core Artifacts Package

This package provides the foundational definitions and utilities for managing artifacts within the Agentic Engineering Framework (AEF), aligning with the canonical model defined in Milestone M9.

## Canonical Storage Structure

The canonical storage structure organizes artifacts within a project-scoped, milestone-centric hierarchy. This structure aims to provide deterministic context and separate artifact types.

### Project Scope

Artifacts are organized under a project scope, which is typically the root directory of the repository or a designated project workspace.

### Milestone Organization

Within the project scope, milestones are housed in a `milestones/` directory. Each milestone is represented by a directory named after its ID (e.g., `M1/`, `M9/`).

```
<project-scope>/
  milestones/
    M1/
    M2/
    ...
    M9/
```

### Artifact Type Directories

Inside each milestone directory, artifacts are further categorized into directories based on their canonical type. This promotes clarity and prevents mixed semantic types within a single directory.

```
milestones/<M_ID>/
  <M_ID>.md  # Milestone definition itself

  specifications/
    SPEC-001.md
    SPEC-002.md
    ...

  verifications/
    VER-001.md
    ...

  tests/
    TEST-001.md  # Test plan document
    # ... script files go into tests/<M_ID>/test_*.py

  investigations/
    INV-001.md
    ...

  implementations/
    IMP-001.md
    ...

  evaluations/
    EVAL-001.md
    ...

  reviews/
    REVIEW-001.md
    ...

  audits/
    AUDIT-001.md
    ...
```

### Artifact Naming Convention

Artifacts within their respective type directories should follow a naming convention based on their canonical ID and type, often including a version or sequence number (e.g., `SPEC-001.md`, `INV-001.md`). The `id` field in the metadata provides the definitive identifier.

## Key Principles

*   **Deterministic Resolution**: The combination of metadata, directory location, and a defined resolution algorithm ensures artifacts can be reliably identified.
*   **Separation of Concerns**: Artifact identity, type, lineage, and lifecycle state are managed through metadata and directory structure, not encoded solely in filenames.
*   **Legacy Compatibility**: The structure must allow for the discovery and interpretation of existing artifacts, even if they do not conform to the canonical model.

## Metadata Serialization

Metadata is primarily managed using YAML frontmatter, as defined in `core/artifacts/metadata.py`.
