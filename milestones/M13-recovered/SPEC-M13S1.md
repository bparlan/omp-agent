---
id: SPEC-M13S1
type: specification
title: "M13S1 — Pipeline State Validation"
milestone_id: M13
status: draft
derived_from:
  - M13
template_version: 1.3.0
metadata:
  created_at: 2026-09-01T03:22:00
  updated_at: 2026-09-01T03:22:00
  artifact_identity: SPEC-M13S1
  artifact_type: specification
---

#### Objective
*(Define and enforce deterministic pipeline state validation that ensures all artifacts meet canonical contracts before phase progression. This specification establishes the foundational validation system for the M13 SDD pipeline stabilization.)*

#### Followup Context
*(This is the first specification in the M13 spec decomposition plan.)*

##### Derived From
*   `M13` (Milestone)

##### Prior Work Completed
*   None - This is the first specification in the M13 pipeline stabilization sequence.

##### Remaining Gaps
*   Pipeline state validation gates and enforcement mechanisms
*   Artifact naming convention validation
*   Frontmatter compliance validation
*   Gate progression coordination
*   Integration validation with core AEF artifact infrastructure

#### Functional Requirements

##### `FR-PIPELINE_STATE_VALIDATION`
*   **Type**: Function/API Contract
*   **Interface Contract**: `manage_development_skill.main(milestone_id: str = "M13") -> int`
*   **Expected Behavior**: Returns exit code 0 when validation passes, 1 when validation fails, with detailed logging of gate outcomes. Must discover and validate all specification artifacts through the complete 6-stage pipeline without manual skip.
*   **Observable Boundary**: Exit codes and file system state validation of pipeline artifacts (`VER-M13S{n}V{m}.md`, `TEST-M13S{n}T{p}.md`, `EVA-M13S{n}.md`, `REV-M13S{n}.md`, `CLOSE-M13-N.md`)

##### `FR-PIPELINE_DIAGNOSTICS`
*   **Type**: Filesystem State Contract
*   **Interface Contract**: `PIPELINE-STATE.md` file generation with structured gate outcomes logging
*   **Expected Behavior**: Creates `PIPELINE-STATE.md` in milestone directory containing structured JSON-like records of each gate validation, with timestamps, validation status, artifact paths, and error details. Format must match pattern defined in milestone scope.
*   **Observable Boundary**: File system presence and content of `PIPELINE-STATE.md` with validated JSON structure for auditability

#### Non-Functional Requirements

##### `NFR-PIPELINES_STABILITY`
*   **Constraint**: Validation must be deterministic with no manual bypasses; all gate artifacts must be validated through canonical validation contracts before progression
*   **Verification**: Monitor validation orchestrator and gate enforcement middleware for deterministic progression through all 6 stages

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**
*   [ ] `milestones/M13/SPEC-M13S1.md` — This specification
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
*   None — no module deprecation; M13S1 is additive integration.

##### Public Interfaces
*   `core/validation.py::validate_metadata(artifact_path: str, schema: Optional[Dict] = None) -> Dict[str, Any]` — canonical validation (binding)
*   `core/validation.py::validate_artifact(metadata: Dict[str, Any]) -> Dict[str, Any]` — artifact-level validation (binding)
*   `core/artifacts/metadata.py::extract_frontmatter(file_path: str) -> Dict[str, Any]` — frontmatter parsing (binding)
*   `core/artifacts/metadata.py::parse_metadata(content: str) -> Dict[str, Any]` — content parsing (binding)
*   `core/artifacts/artifact_types.py::get_artifact_type(identifier: str) -> Optional[CanonicalArtifactType]` — type resolution by identifier (binding; used by resolution layer)
*   `core/artifacts/registry.py::get_registry() -> Dict` — full registry (binding)
*   `core/artifacts/creation.py::create_artifact(name: str, content: str, artifact_type: str, metadata: Dict) -> str` — artifact emission (binding)

--------------------------------------------------------------------------------

#### Interface Boundaries

##### Module Thresholds
*   `skills/manage-development` reads `milestones/M13/` directory, validates artifact naming conventions (`SPEC-M13S{n}.md`, `VER-M13S{n}V{m}.md`, etc.), and invokes `core/validation.py::validate_metadata()` and `core/artifacts/metadata.py::extract_frontmatter()` per artifact before allowing stage progression.
*   `core/validation.py` validates frontmatter against canonical schema; produces structured result dict consumed by `manage-development` which writes to `PIPELINE-STATE.md`.
*   `core/artifacts/registry.py` registers produced artifacts; `get_artifact_type()` confirms naming-pattern compliance for each pipeline stage.

##### Schema Contracts
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["valid", "errors", "missing_fields", "artifact_path", "milestone_id"],
  "properties": {
    "valid": { "type": "boolean" },
    "errors": { "type": "array", "items": { "type": "string" } },
    "missing_fields": { "type": "array", "items": { "type": "string" } },
    "artifact_path": { "type": "string" },
    "milestone_id": { "type": "string", "enum": ["M13"] }
  }
}
```

--------------------------------------------------------------------------------

#### Implementation Tasks

1.  Implement `PipelineStateValidator` class with comprehensive validation logic per FR contracts.
2.  Implement `validate_specification(spec_id)` for frontmatter parsing and artifact validation.
3.  Implement `validate_gate_artifacts()` to discover VER/EVA/REV/CLOSE patterns and return validation status.
4.  Implement `validate_stage_progression()` to validate deterministic progression through 6 pipeline stages.
5.  Implement `generate_pipeline_state()` to write structured `PIPELINE-STATE.md` with gate outcomes.
6.  Implement `main(milestone_id: str = "M13") -> int` orchestrating complete deterministic validation sequence.

#### Constraints

*   No binary analysis (`bin/` directory) — forbidden by guardrails
*   No prose contracts — every FR defines CLI/file/registry observable boundary
*   No cross-milestone file mutation — denylist enforces `M13/` isolation
*   All `core/` interactions must use existing interfaces (`validate_metadata`, `get_artifact_type`, `extract_frontmatter`, `create_artifact`) — no internal data-flow description permitted
*   Pipeline artifacts must reference `derived_from: [M13]` (or appropriate prior spec) and maintain `milestone_id: M13`
*   No sequential numeric FR IDs used — all have semantic identifiers

--------------------------------------------------------------------------------

#### Assumptions

*   `core/validation.py`, `core/artifacts/metadata.py`, `core/artifacts/registry.py`, `core/artifacts/creation.py` exist and expose the interfaces listed in Milestone Integration Bindings (verified by `read` + `lsp` in this session)
*   `manage-development` skill has access to `milestones/M13/` and can write `PIPELINE-STATE.md`
*   All M13 pipeline artifacts use naming patterns from Milestone Scope (verified by existing `SPEC-M13S1.md` through `SPEC-M13S4.md`)
*   Canonical frontmatter schema (`id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`, `metadata`) is stable (from M13S2 and `core/validation.py` line 39-46)

--------------------------------------------------------------------------------

#### Acceptance Criteria

*   [ ] `manage-development` invokes `core/validation.py::validate_metadata()` on all `milestones/M13/` artifacts; `PIPELINE-STATE.md` shows `valid == true`, `errors == []` for 100% of artifacts in completed stages
*   [ ] `get_artifact_type()` resolves all six pipeline naming patterns (`SPEC-`, `VER-`, `TEST-`, `EVA-`, `REV-`, `CLOSE-`) without exception; registry confirms entries
*   [ ] `extract_frontmatter()` produces complete dict (all required keys) for every pipeline artifact; `milestone_id == "M13"`; `metadata` sub-keys all present
*   [ ] Passing stage emits next-stage artifact via `create_artifact()`; emitted file passes `validate_metadata()` with `valid == true`; registry updated; `PIPELINE-STATE.md` records creation
*   [ ] `PIPELINE-STATE.md` exists with structured per-artifact entries (path, valid, errors, missing_fields, timestamp, stage) for all six pipeline stages; zero errors at milestone closure

#### User Approval

* [x] Approved for implementation by user