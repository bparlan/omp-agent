---
id: SPEC-M13S3
type: specification
title: "M13S3 — Gate Enforcement Middleware"
milestone_id: M13
status: draft
derived_from:
  - M13
  - SPEC-M13S1
  - SPEC-M13S2
template_version: 1.3.0
metadata:
  created_at: 2026-09-01T03:22:00
  updated_at: 2026-09-01T03:22:00
  artifact_identity: SPEC-M13S3
  artifact_type: specification
---

#### Objective
*(Define and enforce deterministic gate validation logic that ensures pipeline progression through comprehensive artifact validation before advancing to subsequent stages. This specification establishes the middleware contracts for gate enforcement within the M13 SDD pipeline stabilization.)*

#### Followup Context
*(This is the third specification in the M13 spec decomposition plan, building on Pipeline State Validation and Artifact Naming & Frontmatter Compliance.)*

##### Derived From
*   `M13` (Milestone)
*   `SPEC-M13S1` (Pipeline State Validation)
*   `SPEC-M13S2` (Artifact Naming & Frontmatter Compliance)

##### Prior Work Completed
*   Pipeline state validation gates and enforcement mechanisms (M13S1)
*   Artifact naming convention validation (M13S2)
*   Basic frontmatter compliance validation framework

##### Remaining Gaps
*   Direct filesystem-state integration with `core/artifacts/registry.py` for artifact type registration of M13 outputs
*   Metadata extraction (`core/artifacts/metadata.py`) validated against pipeline artifacts
*   Artifact creation pipeline (`core/artifacts/creation.py`) wired into `manage-development` gate flow
*   Canonical validation results aggregated into `PIPELINE-STATE.md` via `core/validation.py`

#### Functional Requirements

##### `FR-AEF-CANONICAL-VALIDATION-INTEGRATION`
*   **Type**: Filesystem State Contract
*   **Interface Contract**: `core/validation.py::validate_metadata(artifact_path: str, schema: Optional[Dict] = None) -> Dict[str, Any]` invoked by `manage-development` on each pipeline artifact path (`milestones/M13/SPEC-M13S{n}.md`, `VER-M13S{n}V{m}.md`, `TEST-M13S{n}T{p}.md`, `EVA-M13S{n}.md`, `REV-M13S{n}.md`, `CLOSE-M13-N.md`)
*   **Expected Behavior**: For every artifact under `milestones/M13/`, `validate_metadata()` returns `{"valid": <bool>, "errors": [str], "missing_fields": [str]}` with `valid == true` and empty `errors`/`missing_fields` for all artifacts that satisfy canonical frontmatter ([`id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`, `metadata`]). Failures are recorded to `PIPELINE-STATE.md`. Zero validation errors required for milestone closure.
*   **Observable Boundary**: `PIPELINE-STATE.md` entry per artifact containing `artifact_path`, `valid`, `errors[]`, `missing_fields[]`; exit code from `manage-development` = 1 when any `valid == false`; exit code = 0 when all artifacts in stage pass.

##### `FR-AEF-REGISTRY-TYPE-REGISTRATION`
*   **Type**: Function/API Contract (filesystem observable via registry output)
*   **Interface Contract**: `core/artifacts/artifact_types.py::get_artifact_type(identifier: str) -> Optional[CanonicalArtifactType]` (also referenced via `core/artifacts/resolution.py`) resolves `SPEC-M13S{n}` → `"specification"`, `VER-M13S{n}V{m}` → `"verification"`, `TEST-M13S{n}T{p}` → `"test_set"`, `EVA-M13S{n}` → `"evaluation"`, `REV-M13S{n}` → `"review"`, `CLOSE-M13-N` → `"closure"`. Registry entry existence confirmed by `core/artifacts/registry.py::get_registry()`.
*   **Expected Behavior**: Every M13 pipeline artifact name matches a registered artifact type; `get_artifact_type()` returns non-empty string for all six naming patterns; `get_registry()` includes M13 artifacts in its active registry set.
*   **Observable Boundary**: Registry query result (dict or list of registered names/paths) containing entries for all six pipeline patterns under `milestones/M13/`; absence of `KeyError`/`None` on any pipeline artifact name lookup.

##### `FR-AEF-METADATA-EXTRACTION`
*   **Type**: Function/API Contract (filesystem observable via parsed frontmatter)
*   **Interface Contract**: `core/artifacts/metadata.py::extract_frontmatter(file_path: str) -> Dict[str, Any]` and `parse_metadata(content: str) -> Dict[str, Any]` executed by gate middleware against each `milestones/M13/*` artifact.
*   **Expected Behavior**: Extracted frontmatter contains required keys (`id`, `type`, `milestone_id`, `spec_id`, `status`, `derived_from`, `template_version`, `metadata` with `created_at`, `updated_at`, `artifact_identity`, `artifact_type`) for 100% of M13 artifacts; `metadata.version` present; `derived_from` references valid milestone/spec IDs; `milestone_id == "M13"`.
*   **Observable Boundary**: Per-artifact parsed frontmatter dict with all required keys present (no missing); `metadata.created_at` and `updated_at` present; `id` matches filename stem; `milestone_id == "M13"`.

##### `FR-AEF-ARTIFACT-CREATION-PIPELINE`
*   **Type**: Filesystem State Contract
*   **Interface Contract**: `core/artifacts/creation.py::create_artifact(name: str, content: str, artifact_type: str, metadata: Dict) -> str` (confirmed via `lsp` / `read`) invoked by `manage-development` when stage gate passes, to emit new pipeline artifacts (e.g., generating verification artifact after spec is validated).
*   **Expected Behavior**: When a gate passes (all artifacts of preceding stage valid), `create_artifact()` produces the next-stage artifact at the correct `milestones/M13/` path with correct naming convention, canonical frontmatter, and registry registration; file exists with non-zero size; registry reflects new entry.
*   **Observable Boundary**: New artifact file at expected path (`VER-M13S{n}V{m}.md` after `SPEC-M13S{n}.md` validated); file frontmatter passes `validate_metadata()` with `valid == true`; registry contains new entry; `PIPELINE-STATE.md` records creation timestamp and validation result.

#### Non-Functional Requirements

##### `NFR-AEF-VALIDATION-DETERMINISM`
*   **Constraint**: All `core/validation.py` calls on identical M13 artifact inputs must produce identical `{"valid": bool, "errors": [], "missing_fields": []}` outputs across repeated executions; no randomness or environment-dependent variability.
*   **Verification**: Execute validation twice per artifact, compare dict equality; assert identical outputs.

##### `NFR-AEF-FILESYSTEM-ISOLATION`
*   **Constraint**: `core/` integration must not modify files outside `milestones/M13/` or `core/`; pipeline artifacts must not alter source code outside allowlist; denylist enforced.
*   **Verification**: `find milestones/M13/ -newer core/` (before/after comparison) confirms only M13 artifacts changed; `core/` source untouched.

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**
*   [ ] `milestones/M13/SPEC-M13S3.md` — This specification
*   [ ] `milestones/M13/PIPELINE-STATE.md` — Gate outcome records (output of integration)
*   [ ] `skills/manage-development/__init__.py` — Gate middleware that calls `core/validation.py`, `core/artifacts/metadata.py`, `core/artifacts/registry.py`, `core/artifacts/creation.py` (from Milestone Integration Bindings)
*   [ ] `core/validation.py` — Read-only / validation invocation interface (binding, not source edit required; if edit needed for schema extension, explicitly listed)
*   [ ] `core/artifacts/metadata.py`, `core/artifacts/registry.py`, `core/artifacts/creation.py` — Binding interfaces; read/invoke only unless registry schema extension explicitly required by `FR-AEF-REGISTRY-TYPE-REGISTRATION`

**Denylist (Do NOT Touch):**
*   [ ] All `milestones/` directories outside `M13/` (prevent cross-milestone contamination)
*   [ ] All `tests/` directories and test fixtures (test generation belongs to M13S5, not this integration spec)
*   [ ] `bin/` directory (binary naming conventions are out of scope per guardrails)
*   [ ] All specification files outside `milestones/M13/` (scope enforcement)
*   [ ] Source modules unrelated to AEF artifact infrastructure (`core/` modules beyond those listed in Integration Bindings)

##### Affected Modules
*   `core/validation.py` — `validate_metadata()` invoked by gate middleware (binding, interface contract)
*   `core/artifacts/metadata.py` — `extract_frontmatter()`, `parse_metadata()` invoked by gate middleware
*   `core/artifacts/registry.py` — `get_registry()`, `get_artifact_type()` invoked by gate middleware
*   `core/artifacts/creation.py` — `create_artifact()` invoked when stage passes
*   `skills/manage-development` — Gate middleware enhanced to integrate all four `core/` bindings

##### New Modules
*   None required — all `core/artifacts/` modules exist per Integration Bindings; this spec defines integration contracts, not new code buildings. If registry extension needed (new `ML13_PIPELINE` artifact type), it is a minimal schema addition within `core/artifacts/artifact_types.py`, documented below.

##### Removed Modules
*   None — no module deprecation; M13S3 is additive integration.

##### Public Interfaces
*   `core/validation.py::validate_metadata(artifact_path: str, schema: Optional[Dict] = None) -> Dict[str, Any]` — canonical validation (binding)
*   `core/validation.py::validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]` — artifact-level validation (binding)
*   `core/artifacts/metadata.py::extract_frontmatter(file_path: str) -> Dict[str, Any]` — frontmatter parsing (binding)
*   `core/artifacts/metadata.py::parse_metadata(content: str) -> Dict[str, Any]` — content parsing (binding)
*   `core/artifacts/artifact_types.py::get_artifact_type(identifier: str) -> Optional[CanonicalArtifactType]` — type resolution by identifier (binding; used by resolution layer)
*   `core/artifacts/registry.py::get_registry() -> Dict` — full registry (binding)
*   `core/artifacts/creation.py::create_artifact(name: str, content: str, artifact_type: str, metadata: Dict) -> str` — artifact emission (binding)

#### Implementation Tasks

1.  Wire `manage-development` gate middleware to invoke `core/validation.py::validate_metadata()` on each `milestones/M13/*` artifact before stage progression
2.  Integrate `core/artifacts/registry.py::get_artifact_type()` and `get_registry()` to confirm all six naming patterns resolve correctly; record registry status to `PIPELINE-STATE.md`
3.  Invoke `core/artifacts/metadata.py::extract_frontmatter()` per artifact; assert all required keys present; write parsed results to `PIPELINE-STATE.md`
4.  Configure `create_artifact()` call within `manage-development` so that passing a stage emits the next-stage artifact with canonical frontmatter and registry entry; validate with `validate_metadata()` after creation
5.  Aggregate all validation/registry/extraction/creation outcomes into `milestones/M13/PIPELINE-STATE.md` with timestamp, artifact path, result dict, and stage identifier; ensure zero `errors` for milestone closure

#### Constraints

*   No binary analysis (`bin/` directory) — forbidden by guardrails
*   No prose contracts — every FR defines CLI/file/registry observable boundary
*   No cross-milestone file mutation — denylist enforces `M13/` isolation
*   All `core/` interactions must use existing interfaces (`validate_metadata`, `get_artifact_type`, `extract_frontmatter`, `create_artifact`) — no internal data-flow description permitted
*   Pipeline artifacts must reference `derived_from: [M13, SPEC-M13S3]` (or appropriate prior spec) and maintain `milestone_id: M13`
*   No sequential numeric FR IDs used — all four FRs have semantic identifiers

#### User Approval

* [x] Approved for implementation by user