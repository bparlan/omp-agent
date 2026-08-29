# Structural Damage Report: M9S1 Specification Path Mismatch

**Date:** 2026-08-28
**Milestone:** M9S1
**Status:** BLOCKING — specification paths do not match implementation locations

## Executive Summary

M9S1 cannot be evaluated in its current state. The specification, verification protocol, and test ledger define a non-existent source tree (`src/core/artifacts/`, `src/omp_cli/`), while the actual artifact-system implementation lives under `core/artifacts/` with an additional standalone validator at `bin/validate_metadata.py`. This single path mismatch cascades into 11/11 test failures, broken imports, and an ambiguous package layout.

---

## 1. Repository Structure Snapshot

### 1.1 Actual Implementation Tree
```
core/
  __init__.py
  artifacts/
    __init__.py          # Lazy re-export hub
    creation.py
    errors.py
    metadata.py          # Minimal metadata parsing
    migration.py
    registry.py
    resolution.py
    resolve.py
    types.py
  config.py
  errors.py
  validation.py          # Rich validation module
bin/
  validate_metadata.py   # Standalone validator script
src/
  env_layer/             # Separate env-layer package
  omp_cli/
    validate_metadata.py # Broken import: src.core.artifacts.metadata
```

### 1.2 Specified But Non-Existent Tree
```
src/
  core/
    artifacts/           # Referenced in SPEC/VER/tests — DOES NOT EXIST
      registry.py
      types.py
      resolution.py
      metadata.py
      errors.py
  omp_cli/
    validate_metadata.py # Referenced in SPEC/VER — DOES NOT EXIST
```

### 1.3 Package Configuration
- **No `pyproject.toml`, `setup.py`, or `setup.cfg`** found at project root.
- `core/__init__.py` exists, making `core` importable from project root when `cwd` is the project directory.
- `src/core/` directory exists but is **empty** — confirmed after removal of duplicate artifact tree.

---

## 2. Duplication Inventory

### 2.1 Validator Implementations (3 copies)

| File | Lines | Quality | Status |
|------|-------|---------|--------|
| `core/validation.py` | 137 | **High** | Proper dataclasses, `validate_metadata()`, `validate_artifact()` |
| `bin/validate_metadata.py` | 199 | **Medium** | Standalone script, imports `_frontmatter.py`, has CLI |
| `src/omp_cli/validate_metadata.py` | 73 | **Low** | **BROKEN** — imports non-existent `src.core.artifacts.metadata` |

**Damage:** Three validator implementations with overlapping responsibility. The `src/omp_cli/` version is non-functional due to stale import path. Tests reference `bin/validate_metadata.py`, but the spec references `src/omp_cli/validate_metadata.py`.

### 2.2 Artifact System Implementations

| Directory | Files | Quality | Status |
|-----------|-------|---------|--------|
| `core/artifacts/` | 9 files | **High** | Complete: registry, types, resolution, resolve, metadata, errors, creation, migration |
| `src/core/artifacts/` | 0 files (was 4) | **N/A** | Removed — was an incomplete duplicate |

**Damage:** A parallel `src/core/artifacts/` tree existed with divergent implementations. It has been removed, but the spec/verification/test documents still reference it.

### 2.3 Metadata Module Discrepancy

- `core/artifacts/metadata.py` (27 lines): Provides `parse_metadata()` and `get_metadata_from_file()` only.
- `src/omp_cli/validate_metadata.py` line 12: Imports `validate_artifact_content` and `validate_metadata_files` from `src.core.artifacts.metadata` — **neither function exists** in any actual implementation.

**Damage:** The `src/omp_cli/validate_metadata.py` script is non-functional because it imports symbols that don't exist anywhere in the repository.

---

## 3. Quality Assessment of Actual Implementations

### 3.1 `core/validation.py` — HIGH QUALITY
- Proper `@dataclass` models: `ValidationResult`, `ArtifactValidationResult`
- Clear contract: `validate_metadata(artifact_path, schema?)` returns `{"valid", "errors", "missing_fields"}`
- Validates frontmatter parsing, required keys, metadata sub-object, type constraints, milestone_id regex
- Legacy compatibility: `validate_artifact(metadata)` for in-memory validation
- Abstract `Validator` base class for skill rules

### 3.2 `core/artifacts/registry.py` — HIGH QUALITY
- `ArtifactRegistry` class with type registration/retrieval
- `get_registry()` singleton accessor
- Storage rules with pattern placeholders
- Relationship tracking methods (`store_relationship`, `get_relationships`)

### 3.3 `core/artifacts/resolve.py` / `resolution.py` — HIGH QUALITY
- `resolve_artifact()` with identity/type/metadata_filter/strict parameters
- `construct_canonical_path()` for path construction
- `LEGACY_ARTIFACT_MAPPINGS` dictionary
- `_is_canonical_artifact()` function for frontmatter detection

### 3.4 `core/artifacts/types.py` — HIGH QUALITY
- `CanonicalArtifactType` enum
- `_ARTIFACT_TYPE_DEFINITIONS` with schemas
- Serialization/deserialization methods

### 3.5 `bin/validate_metadata.py` — MEDIUM QUALITY
- Standalone script with CLI
- Imports `_frontmatter.py` from same directory
- Legacy milestone boundary detection
- Template version compatibility checks
- **Issue:** Not importable as a module from project root without `bin/` in `sys.path`

### 3.6 `src/omp_cli/validate_metadata.py` — LOW QUALITY / BROKEN
- Imports from non-existent `src.core.artifacts.metadata`
- Imports `validate_artifact_content` and `validate_metadata_files` — **neither exists**
- Script cannot run or be imported

---

## 4. Test Failure Root Cause Analysis

### 4.1 Path Mismatch Matrix

| Document | References | Actual Location | Status |
|----------|-----------|-----------------|--------|
| SPEC-M9S1.md | `src/core/artifacts/*` | `core/artifacts/*` | **MISMATCH** |
| SPEC-M9S1.md | `src/omp_cli/validate_metadata.py` | `bin/validate_metadata.py` | **MISMATCH** |
| VER-M9S1V.md | `src/core/artifacts/*` | `core/artifacts/*` | **MISMATCH** |
| VER-M9S1V.md | `python src/core/artifacts/resolve.py` | `python core/artifacts/resolve.py` | **MISMATCH** |
| M9S1T1.md | `src/core/artifacts/*` in test paths | `core/artifacts/*` | **MISMATCH** |
| tests/M9/S1/*.sh | `src/core/artifacts/*` | `core/artifacts/*` | **MISMATCH** |
| tests/M9/S1/*.py | `src/core/artifacts/*` | `core/artifacts/*` | **MISMATCH** |

### 4.2 Test Execution Results (11/11 Failed)

| Test | Exit Code | Error |
|------|-----------|-------|
| test_registry_init_001.sh | 127 | `src/core/artifacts/registry.py` not found |
| test_resolver_init_001.sh | 127 | Resolver module import failed |
| test_validator_init_001.sh | 127 | `No module named 'validate_metadata'` |
| test_storage_model_001.sh | 127 | `get_storage_rule` method check failed |
| test_schema_constraints_001.sh | 127 | Validator script not found at `omp_cli/validate_metadata.py` |
| test_resolution_priority_001.sh | 127 | `resolve_artifact` function not found |
| test_legacy_compat_001.sh | 127 | `LEGACY_ARTIFACT_MAPPINGS` not found |
| test_traceability_001.sh | 127 | `ArtifactRegistry` class not found |
| test_types_def_001.py | 127 | `No module named 'core.artifacts'` |
| test_legacy_compat_001.py | 127 | `No module named 'core.artifacts'` |
| test_traceability_001.py | 127 | `No module named 'core.artifacts'` |

---

## 5. Remaining Structural Issues After Duplicate Removal

### 5.1 Empty `src/core/` Directory
- **Issue:** `src/core/` directory exists but is empty.
- **Impact:** Spec documents reference this path, causing test failures.
- **Resolution:** Either remove the directory or update all references to `core/artifacts/`.

### 5.2 Broken `src/omp_cli/validate_metadata.py`
- **Issue:** Imports `validate_artifact_content` and `validate_metadata_files` from `src.core.artifacts.metadata` — neither function exists.
- **Impact:** Script cannot run; tests expecting this path will fail.
- **Resolution:** Either rewrite to import from `core.validation`/`core.artifacts.metadata`, or remove and point to `bin/validate_metadata.py`.

### 5.3 No Package Configuration
- **Issue:** No `pyproject.toml`, `setup.py`, or `setup.cfg` at project root.
- **Impact:** Python package discovery is implicit; `core` is importable only when running from project root.
- **Resolution:** Add package configuration or ensure consistent `PYTHONPATH` in all test/execution contexts.

### 5.4 Spec/Verification/Ledger Divergence
- **Issue:** 75+ references to `src/core/artifacts/` across milestones and tests.
- **Impact:** Any new milestone following this pattern will inherit the same breakage.
- **Resolution:** Choose canonical location (`core/artifacts/` recommended) and bulk-update all docs/tests.

---

## 6. Damage Assessment

### 6.1 Immediate Damage
- **11/11 tests fail** with import errors.
- **0 tests pass** — evaluation cannot proceed.
- **3 validator implementations** exist, only 1 works reliably (`bin/validate_metadata.py`).
- **1 broken script** (`src/omp_cli/validate_metadata.py`) with non-existent imports.

### 6.2 Technical Debt
- **Package ambiguity:** Is the project using `core/` or `src/core/`? The answer is "neither consistently."
- **Validator fragmentation:** Three separate validation entry points with overlapping logic.
- **Specification drift:** Documents reference paths that never existed or were removed.

### 6.3 Risk Assessment
| Risk | Severity | Likelihood | Impact |
|------|----------|------------|--------|
| New milestones inherit wrong paths | **CRITICAL** | High | All tests fail by default |
| Developers edit wrong duplicate tree | **HIGH** | Medium | Work lost or duplicated |
| CI/CD breaks on import errors | **HIGH** | High | Pipeline failure |
| Validator behavior diverges | **MEDIUM** | Medium | Inconsistent validation results |

---

## 7. Recommended Remediation

### 7.1 Canonical Location Decision
**Recommendation:** Use `core/artifacts/` as the single source of truth.

Rationale:
- Implementation already exists and is complete there.
- `core/` is a proper Python package with `__init__.py`.
- `bin/validate_metadata.py` exists and works as a standalone validator.
- `src/core/artifacts/` was incomplete and has been removed.

### 7.2 Immediate Actions Required
1. **Update SPEC-M9S1.md** — Replace all `src/core/artifacts/` with `core/artifacts/`, `src/omp_cli/` with `bin/`.
2. **Update VER-M9S1V.md** — Same path corrections.
3. **Update M9S1T1.md** — Same path corrections.
4. **Fix or remove `src/omp_cli/validate_metadata.py`** — Either rewrite imports or delete.
5. **Remove empty `src/core/` directory** — Eliminates confusion.
6. **Re-run evaluation** — After path alignment.

### 7.3 Long-Term Actions
1. **Add `pyproject.toml`** — Define package structure explicitly.
2. **Consolidate validators** — Choose one validation entry point (`bin/validate_metadata.py` or `core/validation.py`).
3. **Audit all milestones** — Search for `src/core/artifacts/` references across all milestone documents.
4. **Add CI check** — Fail builds if spec paths don't match implementation.

---

## 8. Affected Files

### 8.1 Specification Documents
- `milestones/M9/S1/SPEC-M9S1.md` — 12 references to wrong paths
- `milestones/M9/S1/VER-M9S1V.md` — 7 references to wrong paths
- `milestones/M9/S1/M9S1T1.md` — Test paths reference wrong locations
- `milestones/M9/M9S1C.md` — References `src/core/artifacts/*`

### 8.2 Test Files
- `tests/M9/S1/test_registry_init_001.sh`
- `tests/M9/S1/test_resolver_init_001.sh`
- `tests/M9/S1/test_validator_init_001.sh`
- `tests/M9/S1/test_storage_model_001.sh`
- `tests/M9/S1/test_schema_constraints_001.sh`
- `tests/M9/S1/test_resolution_priority_001.sh`
- `tests/M9/S1/test_legacy_compat_001.sh`
- `tests/M9/S1/test_traceability_001.sh`
- `tests/M9/S1/test_types_def_001.py`
- `tests/M9/S1/test_legacy_compat_001.py`
- `tests/M9/S1/test_traceability_001.py`

### 8.3 Implementation Files Needing Attention
- `src/omp_cli/validate_metadata.py` — Broken imports, needs rewrite or removal
- `src/core/` — Empty directory, should be removed
- `core/artifacts/metadata.py` — Missing `validate_artifact_content` and `validate_metadata_files` functions imported by broken `src/omp_cli/` script

---

## 9. Conclusion

The M9S1 milestone is **blocked by a structural specification error**, not by implementation bugs. The actual `core/artifacts/` implementation is high quality and complete. The path mismatch between specification documents and implementation is the sole cause of all 11 test failures.

**Estimated remediation effort:** 2-4 hours for path alignment across documents and tests, plus 1-2 hours for validator consolidation.

**Recommended next step:** Bulk-update all specification, verification, ledger, and test documents to reference `core/artifacts/` and `bin/validate_metadata.py`, then re-run evaluation.
