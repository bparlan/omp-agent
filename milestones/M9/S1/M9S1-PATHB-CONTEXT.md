---
id: M9S1-PATHB-CONTEXT
type: documentation
title: "Path B Context Report — M9S1 Invalid Test Set"
milestone_id: M9
status: active
derived_from:
  - EVAL-1
  - SPEC-M9S1
  - VER-M9S1V
template_version: 1.0.2
---

## Executive Summary

M9S1 (`SPEC-M9S1` — Artifact Registry & Resolution System) was evaluated against its test plan ledger (`TEST-M9S1T1.md`). **14 of 19 tests are INVALID** due to structural defects unrelated to production code quality. The 5 valid tests pass. The remaining 14 must be replaced via Path B: generate a new, complete test plan using `/generate-tests` against the approved verification protocol (`VER-M9S1V.md`).

This document provides the handoff context for that generation phase.

---

## What Passed (5 VALID_TESTS)

These tests exercised production code successfully and confirm the following FRs are implemented:

| FR | Test File | What Was Verified |
|:---|:---|:---|
| `FR-LEGACY_COMPAT` | `test_legacy_compat_001.py` | `LEGACY_ARTIFACT_MAPPINGS` dict exists; `_is_canonical_artifact(artifact_path)` is callable with correct signature |
| `FR-TRACEABILITY` | `test_traceability_001.py` | `ArtifactRegistry` class exists; `store_relationship(source_id, target_id, relationship_type, metadata?)` and `get_relationships(source_id?)` have correct parameters |
| `FR-TRACEABILITY` | `test_vi6_relationship_fields.py` | Relationship fields (`source_id`, `target_id`, `relationship_type`, `metadata`) follow canonical schema |
| `FR-VALIDATOR_INIT` | `test_vi1_validate_missing_keys.py` | `validate_metadata` correctly identifies 8 required keys: `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`, `metadata` |
| `FR-RESOLVER_INIT` | `test_vi2_ambiguous_resolution.py` | `AmbiguousResolutionError` is importable from `core.artifacts.errors` |

**Confirmed working production modules:**

```
✅ core/validation.py          — validate_metadata()
✅ core/artifacts/resolution.py — LEGACY_ARTIFACT_MAPPINGS, _is_canonical_artifact()
✅ core/artifacts/registry.py  — ArtifactRegistry (store_relationship, get_relationships, list_types)
✅ core/artifacts/errors.py     — AmbiguousResolutionError
✅ core/artifacts/metadata.py  — parse_metadata, get_metadata_from_file (used by resolution)
```

---

## What Failed and Why (14 INVALID_TESTS)

### Category 1: Wrong Interpreter (12 tests — `.sh` files that are Python)

All 12 shell test files in `tests/M9/S1/*.sh` contain Python source code saved with `.sh` extension. When executed with `bash`, the shell attempts to parse Python syntax (`echo`, `if !`, etc.) and fails with `SyntaxError`.

**Critical distinction:** These tests never ran their actual assertions. We do not know if the production code they were meant to verify is correct or broken — the interpreter mismatch prevented any evidence from being collected.

| Test File | FR(s) Targeted | Symptom |
|:---|:---|:---|
| `test_registry_init_001.sh` | `FR-REGISTRY_INIT` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_validator_init_001.sh` | `FR-VALIDATOR_INIT` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_resolver_init_001.sh` | `FR-RESOLVER_INIT` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_storage_model_001.sh` | `NFR-STORAGE_MODEL` | `bash` → Python `SyntaxError`; also `python3 core/artifacts/resolve.py` with no PYTHONPATH → `ImportError: attempted relative import with no known parent package` |
| `test_schema_constraints_001.sh` | `NFR-SCHEMA_CONSTRAINTS` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_resolution_priority_001.sh` | `NFR-RESOLUTION_PRIORITY` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_vi3_artifact_creation.sh` | `FR-ARTIFACT_CREATION` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_vi4_invalid_artifact_failure.sh` | `FR-ARTIFACT_CREATION` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_vi5_milestone_explicit_identity.sh` | `FR-TRACEABILITY` | `bash` → Python heredoc → `SyntaxError: unterminated string literal` |
| `test_vi7_legacy_strict_flag.sh` | `FR-LEGACY_COMPAT` | `bash` → Python heredoc → `SyntaxError: unterminated string literal` |
| `test_vi9_verify_metadata_cli.sh` | `FR-VALIDATOR_INIT` | `bash` → Python `SyntaxError: invalid syntax` |
| `test_vi10_performance_threshold.sh` | `NFR-PERFORMANCE` | `bash` → Python heredoc → `SyntaxError: unterminated string literal` |

**Common root cause:** The tests were written as Python source with bash shebangs (`#!/bin/bash`) and embedded inline Python via `python3 -c "..."` constructs that break when bash parses them.

### Category 2: Import Path Drift (1 test)

| Test File | FR(s) Targeted | Symptom | Root Cause |
|:---|:---|:---|:---|
| `test_types_def_001.py` | `FR-TYPE_DEFS` | `ImportError: cannot import name 'types' from 'core.artifacts'` | Test imports `from core.artifacts.types import ...` but the module was renamed to `artifact_types` by hotfix `HF_20260829_001` to resolve stdlib `types` collision |

This test also checks for `serialize_type_definition` and `deserialize_type_definition` functions (lines 62-72) that do not exist in the implementation. Those assertions would fail even after fixing the import path.

### Category 3: Pre-Implementation Stub (1 test)

| Test File | FR(s) Targeted | Symptom | Root Cause |
|:---|:---|:---|:---|
| `test_vi8_type_consistency.py` | `FR-TYPE_DEFS` | Exits `127` with message `Type validation not implemented or registry empty.` | Test is designed to return exit code 127 when implementation is missing. It never exercises `ArtifactRegistry.list_types()` or `get_artifact_type()`. |

---

## Untested Functional Requirements

The 12 shell test failures mean the following FRs from `SPEC-M9S1` are **unverified**:

| FR ID | Requirement | Current Evidence |
|:---|:---|:---|
| `FR-REGISTRY_INIT` | `ArtifactRegistry` class with type registration | `✅` Imported successfully in `test_traceability_001.py`; methods verified; actual CLI invocation unverified |
| `FR-VALIDATOR_INIT` | `validate_metadata()` / `validate_artifact()` | `✅` `test_vi1_validate_missing_keys.py` passes; CLI exit codes unverified |
| `FR-RESOLVER_INIT` | `resolve_artifact()` with CLI entry | `⚠️` Function exists but CLI invocation broken across all shell tests |
| `FR-TYPE_DEFS` | `CanonicalArtifactType`, `_ARTIFACT_TYPE_DEFINITIONS`, `serialize/deserialize` | `⚠️` Partial: `CanonicalArtifactType` importable; `serialize_type_definition` missing |
| `FR-LEGACY_COMPAT` | `strict` flag behavior, legacy artifact inclusion | `⚠️` Structures verified; strict flag CLI behavior unverified |
| `FR-ARTIFACT_CREATION` | 7-step canonical creation protocol | `⚠️` Module importable; actual creation workflow unverified |
| `FR-CANONICAL_RESOLUTION` | Ambiguous resolution error structure | `⚠️` Import verified; actual behavior unverified |
| `NFR-STORAGE_MODEL` | Artifacts stored at canonical paths | `⚠️` Module importable; CLI broken |
| `NFR-SCHEMA_CONSTRAINTS` | Schema validation rules | `⚠️` Module importable; CLI broken |
| `NFR-RESOLUTION_PRIORITY` | Priority order (identity → type → filter → strict) | `⚠️` Module importable; CLI broken |
| `NFR-PERFORMANCE` | Validation ≤ 5ms, Resolution ≤ 100ms | `⚠️` CLI broken |

---

## What the Next Test Generation Must Cover

Based on `VER-M9S1V.md` and the gap analysis above, the new test plan must produce:

### Shell Tests (`.sh` — must be valid bash)

1. **CLI invocation tests** — invoke `PYTHONPATH=. python3 -m core.artifacts.resolve` and `PYTHONPATH=. python3 -m core.validation` as separate subprocess calls
2. **Storage model test** — verify artifacts are created at canonical paths
3. **Schema constraints test** — verify validation rejects malformed YAML
4. **Resolution priority test** — verify identity > type > filter > strict precedence
5. **Artifact creation test** — verify 7-step protocol creates valid artifact
6. **Invalid artifact failure test** — verify structured error output
7. **Milestone explicit identity test** — verify `id` and `type` fields present
8. **Legacy strict flag test** — verify `strict=True/False` controls inclusion
9. **Metadata CLI test** — verify exit codes 0 (valid) and 1 (invalid)
10. **Performance threshold test** — verify timing under thresholds

### Python Tests (`.py` — must be valid Python)

1. **Type definitions test** — import from `core.artifacts.artifact_types` (not `types`)
2. **Type consistency test** — assert `get_artifact_type()` returns non-null for all 8 known types; assert `ArtifactRegistry.list_types()` matches
3. **Verify missing keys test** — already passing, keep as-is or enhance
4. **Ambiguous resolution test** — assert `AmbiguousResolutionError` raised on multi-match without identity filter
5. **Relationship fields test** — already passing, keep as-is

---

## Key Constraints for `/generate-tests`

1. **Shell tests must be valid bash** — no Python source in `.sh` files. Use `bash script.sh` as invocation. For Python logic, write a separate `.py` test.

2. **Module import paths** — all Python tests must use `PYTHONPATH=.` or `sys.path.insert(0, os.path.join(os.getcwd(), 'core/artifacts'))` correctly. Import from `core.artifacts.artifact_types`, NOT `core.artifacts.types`.

3. **Invocation pattern for CLI tests** — use `subprocess.run(['python3', '-m', 'core.artifacts.resolve'], env={{'PYTHONPATH': '.'}})` or the `PYTHONPATH=. script.py` pattern.

4. **No pre-implementation stubs** — tests must assert against actual implementation behavior, not return `127` when missing.

5. **No `serialize_type_definition` / `deserialize_type_definition`** — these functions do not exist in the implementation. Tests must not assert their existence unless `SPEC-M9S1` explicitly requires them.

6. **Artifact paths** — test fixtures must use real artifact files with correct YAML frontmatter. The canonical fixture pattern is `tests/fixtures/synthetic_metadata_valid/valid_artifact.md`.

---

## File Locations

| Artifact | Path |
|:---|:---|
| This report | `milestones/M9/S1/M9S1-PATHB-CONTEXT.md` |
| Evaluation report | `milestones/M9/S1/M9S1E.md` |
| Spec (read-only) | `milestones/M9/S1/SPEC-M9S1.md` |
| Verification protocol (read-only) | `milestones/M9/S1/VER-M9S1V.md` |
| Existing broken ledger | `milestones/M9/S1/TEST-M9S1T1.md` |

---

## Recommended Next Action

Run `/generate-tests` targeting `VER-M9S1V.md` to produce `TEST-M9S1T2.md` — a new, valid test plan that replaces the broken ledger. After generation, run `/evaluate-tests` (Phase 1 baseline) then `/implement-specification` then `/evaluate-implementation` for a clean M9S1 completion.

> **Note:** The 5 passing tests (`test_legacy_compat_001.py`, `test_traceability_001.py`, `test_vi1_validate_missing_keys.py`, `test_vi2_ambiguous_resolution.py`, `test_vi6_relationship_fields.py`) may be retained as-is in the new ledger if `/generate-tests` does not supersede them. Do not delete the broken tests — the new ledger should supersede the old one entirely.
