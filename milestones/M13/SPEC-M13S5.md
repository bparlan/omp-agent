---
id: SPEC-M13S5
type: specification
title: "M13S5 — Behavior Validation via Unit & Integration Tests"
milestone_id: M13
status: draft
derived_from:
  - M13
  - SPEC-M13S1
  - SPEC-M13S2
  - SPEC-M13S3
  - SPEC-M13S4
template_version: 1.3.0
metadata:
  created_at: 2026-09-01T03:22:00
  updated_at: 2026-09-01T03:22:00
  artifact_identity: SPEC-M13S5
  artifact_type: specification
---

#### Objective
*(Define and enforce deterministic behavior validation through comprehensive unit and integration test suites that ensure all pipeline artifacts meet observable contract requirements before milestone closure. This specification establishes the testable verification protocol and test contract framework for the M13 SDD pipeline stabilization.)*

#### Followup Context
*(This is the 5th specification in the M13 spec decomposition plan, building on Pipeline State Validation, Artifact Naming & Frontmatter Compliance, Gate Enforcement Middleware, and Core AEF Integration.)*

##### Derived From
*   `M13` (Milestone — Pipeline Stabilization & Gate Enforcement)
*   `SPEC-M13S1` (Pipeline State Validation — established validation orchestrator)
*   `SPEC-M13S2` (Artifact Naming & Frontmatter Compliance — canonical frontmatter contract)
*   `SPEC-M13S3` (Gate Enforcement Middleware — implemented stage progression logic)
*   `SPEC-M13S4` (Integration with Core AEF Artifact System — integrated validation APIs)

##### Prior Work Completed
*   Pipeline state validation gates and enforcement mechanisms established (M13S1)
*   Artifact naming convention validation (M13S2)
*   Gate progression logic implemented (M13S3)
*   Core AEF artifact integration completed (M13S4)
*   All six pipeline stage artifacts validated and registered in `core/artifacts/registry.py`
*   `PIPELINE-STATE.md` generated with validation results

##### Remaining Gaps
*   Comprehensive unit test suite covering all M13 pipeline artifacts and their validation contracts
*   Integration test suite ensuring deterministic behavior across the full 6-stage validation pipeline
*   Automated test generation for verification artifacts (`VER-M13S{n}V{m}.md`) and test set artifacts (`TEST-M13S{n}T{p}.md`)
*   Test reporting integration with `PIPELINE-STATE.md` for audit trail completeness

#### Functional Requirements

##### `FR-TEST-GENERATION-CONTRACT`
*   **Type**: Test Set Contract
*   **Interface Contract**: `generate-tests` CLI tool that reads specification artifacts and produces deterministic test suites; `generate-tests.execute(spec_path: str) -> List[TestCase]` with each `TestCase` containing `name: str`, `expected_output: Dict[str, Any]`, `artifact_paths: List[str]`, `validation_contract: str`
*   **Expected Behavior**: Generates test cases that validate each pipeline artifact against its observable contract from prior specifications (S1-S4). Each test case must verify observable boundaries: file existence, canonical frontmatter validation (`validate_metadata()` returns `{"valid": true, "errors": [], "missing_fields": []}`), registry type resolution, frontmatter extraction, and artifact creation. Tests must run deterministically with identical outputs across executions.
*   **Observable Boundary**: Generated test files (`TEST-M13S5T{p}.md`) containing serialized test cases with deterministic content; `generate-tests` exit code 0 when all contract tests pass; `generate-tests` exit code 1 when any test fails validation.

##### `FR-VALIDATION-ORCHESTRATION-CONTRACT`
*   **Type**: Test Set Contract
*   **Interface Contract**: `evaluate-tests` orchestrator that executes generated test suites and produces validation artifacts (`EVA-M13S5.md`). Interface: `evaluate-tests.run(test_set_path: str) -> Dict[str, Any]` with output containing `total_tests: int`, `passed_tests: int`, `failed_tests: int`, `test_results: List[Dict[str, Any]]` where each result includes `test_name`, `status`, `artifact_validation`, `contract_compliance`, `error_details: Optional[str]`
*   **Expected Behavior**: Executes all generated test cases from `TEST-M13S5T{p}.md` files, validating each test case's expected behavior against actual artifact validation results from `core/validation.py`, registry lookups, and frontmatter extraction. Test cases must verify deterministic validation orchestration and artifact creation pipeline integrity across all six stages.
*   **Observable Boundary**: Generated evaluation artifact `EVA-M13S5.md` containing structured test results with deterministic ordering; `evaluate-tests` exit code 0 when all tests pass with `passed_tests == total_tests`; exit code 1 when any test fails.

#### Non-Functional Requirements

##### `NFR-TEST-DETERMINISM`
*   **Constraint**: All test execution must be deterministic with identical results across multiple runs on identical inputs; no environment-dependent variability in test outcomes; test ordering must be stable and deterministic.
*   **Verification**: Execute test suites twice on identical artifact state; compare `EVA-M13S5.md` content; assert identical outputs; verify `passed_tests == total_tests` in both executions.

##### `NFR-TEST-SCOPE-ISOLATION`
*   **Constraint**: Test execution must not modify pipeline artifacts or source code outside `milestones/M13/` and `core/`; tests must read-only validate existing artifacts; test generation must not produce artifacts outside `milestones/M13/`.
*   **Verification**: `find milestones/M13/ -newer core/ -name "TEST-M13S5T*.md"` confirms only generated test artifacts change; `core/` source untouched; `git status` shows only new test files.

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**
*   [ ] `milestones/M13/SPEC-M13S5.md` — This specification
*   [ ] `milestones/M13/PIPELINE-STATE.md` — Gate outcome records (output of test validation)
*   [ ] `skills/generate-tests/__init__.py` — Test generation skill that creates deterministic test cases from specification contracts
*   [ ] `skills/evaluate-tests/__init__.py` — Test orchestration skill that executes generated test suites and produces evaluation artifacts
*   [ ] `milestones/M13/TEST-M13S5T*.md` — Generated test set artifacts (output of test generation)
*   [ ] `milestones/M13/EVA-M13S5.md` — Generated evaluation artifact (output of test execution)

**Denylist (Do NOT Touch):**
*   [ ] All `milestones/` directories outside `M13/` (prevent cross-milestone contamination)
*   [ ] All `skills/` directories outside `generate-tests` and `evaluate-tests` (test generation is scoped to these skills)
*   [ ] `core/` directory beyond the artifact validation interfaces (`validate_metadata`, `extract_frontmatter`, `get_artifact_type`, `create_artifact`) — only read/validation interactions allowed
*   [ ] All existing pipeline artifacts (`SPEC-M13S1.md` through `SPEC-M13S4.md`, `VER-*`, `EVA-*`, `REV-*`, `CLOSE-*`) must not be modified by tests
*   [ ] Any `bin/` directory contents (test execution must use existing skill binaries, not analyze them)

##### Affected Modules
*   `skills/generate-tests` — Test generation skill that produces deterministic test suites from specification contracts
*   `skills/evaluate-tests` — Test orchestration skill that executes test suites and produces evaluation artifacts
*   `core/validation.py` — Validation interface (`validate_metadata()`) invoked by generated tests to verify canonical frontmatter
*   `core/artifacts/registry.py` — Registry interface (`get_artifact_type()`) invoked by tests to validate artifact type resolution
*   `core/artifacts/metadata.py` — Metadata interface (`extract_frontmatter()`) invoked by tests to verify frontmatter extraction
*   `core/artifacts/creation.py` — Creation interface (`create_artifact()`) invoked by tests to verify artifact creation pipeline

##### New Modules
*   `skills/generate-tests/` — Test generation skill that reads specification contracts (S1-S4) and produces deterministic test suites
*   `skills/evaluate-tests/` — Test orchestration skill that executes generated test suites and produces evaluation artifacts
*   `milestones/M13/TEST-M13S5T{p}.md` — Generated test set artifacts (output of test generation, deterministic content)
*   `milestones/M13/EVA-M13S5.md` — Generated evaluation artifact (output of test execution, deterministic results)

##### Removed Modules
*   None — no module deprecation; M13S5 is additive for test generation and validation.

##### Public Interfaces
*   `skills/generate-tests.execute(spec_path: str) -> List[TestCase]` — Generates deterministic test cases from specification contracts
*   `skills/evaluate-tests.run(test_set_path: str) -> Dict[str, Any]` — Executes test suites and produces evaluation artifacts
*   `core/validation.py::validate_metadata(artifact_path: str) -> Dict[str, Any]` — Validation interface for canonical frontmatter verification
*   `core/artifacts/registry.py::get_artifact_type(identifier: str) -> Optional[CanonicalArtifactType]` — Registry interface for artifact type resolution validation
*   `core/artifacts/metadata.py::extract_frontmatter(file_path: str) -> Dict[str, Any]` — Metadata interface for frontmatter extraction validation
*   `core/artifacts/creation.py::create_artifact(name: str, content: str, artifact_type: str, metadata: Dict) -> str` — Creation interface for artifact creation validation

#### Implementation Tasks

1.  Implement `test_generator` class in `skills/generate-tests/__init__.py` that reads all M13 specification artifacts (S1-S4) and generates deterministic test cases against their contracts `[FR-TEST-GENERATION-CONTRACT]`
2.  Implement `test_orchestrator` class in `skills/evaluate-tests/__init__.py` that executes generated test suites and produces `EVA-M13S5.md` with deterministic results `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
3.  Integrate `core/validation.py::validate_metadata()` calls within generated tests to verify canonical frontmatter compliance `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
4.  Integrate `core/artifacts/registry.py::get_artifact_type()` calls within generated tests to verify artifact type resolution `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
5.  Integrate `core/artifacts/metadata.py::extract_frontmatter()` calls within generated tests to verify frontmatter extraction completeness `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
6.  Integrate `core/artifacts/creation.py::create_artifact()` calls within generated tests to verify artifact creation pipeline functionality `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
7.  Ensure generated test artifacts (`TEST-M13S5T*.md`) and evaluation artifact (`EVA-M13S5.md`) follow M13 naming conventions and contain deterministic content `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`

#### Constraints

*   No binary analysis (`bin/` directory) — forbidden by guardrails
*   No prose contracts — every FR defines observable test execution boundary
*   No cross-milestone file mutation — denylist enforces `M13/` isolation
*   All test execution must use existing validation interfaces (`validate_metadata`, `get_artifact_type`, `extract_frontmatter`, `create_artifact`) — no internal data-flow description permitted
*   Generated test artifacts must reference `derived_from: [M13, SPEC-M13S5]` and maintain `milestone_id: M13`
*   No sequential numeric FR IDs used — all two FRs have semantic identifiers
*   Test generation must be deterministic — identical inputs must produce identical test artifacts across multiple runs

#### Assumptions

*   `skills/generate-tests` and `skills/evaluate-tests` skills exist with basic execution capabilities
*   `core/validation.py`, `core/artifacts/registry.py`, `core/artifacts/metadata.py`, `core/artifacts/creation.py` exist and expose the interfaces listed in prior specifications
*   All M13 pipeline artifacts from S1-S4 exist and have valid canonical frontmatter
*   `PIPELINE-STATE.md` exists with validated entries for completed stages
*   Test generation and orchestration skills have access to `milestones/M13/` directory for reading/writing artifacts
*   Generated test suites must produce deterministic, reproducible results across multiple executions

#### Acceptance Criteria

*   [ ] `generate-tests` skill executes successfully and produces `TEST-M13S5T*.md` test artifacts with deterministic content that validate all six pipeline stages against their specification contracts (S1-S4) `[FR-TEST-GENERATION-CONTRACT]`
*   [ ] `evaluate-tests` skill runs all generated test cases and produces `EVA-M13S5.md` with `passed_tests == total_tests` and zero `error_details` for all contract validations `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
*   [ ] Generated test artifacts follow M13 naming conventions and contain canonical frontmatter with `derived_from: [M13, SPEC-M13S5]` and `milestone_id: M13` `[FR-TEST-GENERATION-CONTRACT]`
*   [ ] Generated evaluation artifact `EVA-M13S5.md` includes structured test results with deterministic ordering and complete validation of each test case's expected behavior against actual validation interfaces `[FR-VALIDATION-ORCHESTRATION-CONTRACT]`
*   [ ] Test execution is deterministic — running `generate-tests` followed by `evaluate-tests` produces identical `EVA-M13S5.md` content across multiple executions with no environment-dependent variability `[NFR-TEST-DETERMINISM]`
*   [ ] Test execution does not modify any source code outside `milestones/M13/` or `core/` directories; only test artifacts are created/modified `[NFR-TEST-SCOPE-ISOLATION]`

#### Next Steps

Advise running `/generate-tests` to create test plans for M13S5 (if not already run)
---

*Followup Context:* This specification builds directly on M13S1 (Pipeline State Validation, which established the validation orchestrator), M13S2 (Artifact Naming & Frontmatter Compliance, which defined canonical frontmatter contracts), M13S3 (Gate Enforcement Middleware, which implemented stage progression), and M13S4 (Integration with Core AEF Artifact System, which integrated validation APIs). S5 focuses exclusively on behavior validation through comprehensive unit and integration test suites that ensure deterministic contract compliance across the complete pipeline.

---

#### User Approval

* [x] Approved for implementation by user
