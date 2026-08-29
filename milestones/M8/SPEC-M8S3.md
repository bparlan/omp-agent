---
id: SPEC-M8S3
type: specification
title: "M8 - HealthCheck Skill Reporting Module"
milestone_id: M8
status: draft
derived_from:
  - M8
  - M8S1
  - M8S2
template_version: 1.3.0
---

#### Objective

Transform the reporting functionality from the monolithic `healthcheck.py` into a focused `reporting.py` module that generates all three report formats (badges, JSON reports, processed skills) while maintaining backward compatibility and enabling independent testing. This module supplies the structured output consumed by downstream components while preserving identical report generation behavior that users expect.

##### Milestone Complexity & Multi-Spec Plan

Milestone M8 decomposes into exactly 5 sequential specifications:

- **M8S1** (completed): Core validation module (`core/validation.py`)
- **M8S2** (completed): Discovery module (`discovery.py`)
- **M8S3** (this spec): Reporting module (`reporting.py`)
- **M8S4**: CLI module (`cli.py`)
- **M8S5**: Main entry point (`main.py`)

This spec addresses only HCS3 (Reporting). It MUST NOT redefine validation contracts from M8S1, nor discovery contracts from M8S2, nor CLI/main contracts from M8S4/M8S5.

#### Followup Context

##### Derived From

- `M8` (Milestone - HealthCheck Skill Modular Refactoring)
- `SPEC-M8S1` (Prior Specification - Core Validation Module)
- `SPEC-M8S2` (Prior Specification - Discovery Module)

##### Prior Work Completed

- `core/validation.py` exists with abstract `Validator` base class and `SkillValidator` with pure `validate(content: str) -> Dict[str, Any]` interface
- `discovery.py` exports `discover_skills(project_root: Path | str) -> List[str]`, `find_project_root(start: Path | str | None = None) -> Path`, and `SKILLS_DIR_NAME: str = "skills"`

The validation and discovery contracts provide the essential components needed for reporting: validation produces skill health results, and discovery locates skill directories for processing.

##### Remaining Gaps

- M8S3 (this spec): Skill reporting generation for badges, health reports, and processed skills
- M8S4 reporting, M8S5 CLI, and M8S5 main orchestrator remain for subsequent specifications
- Integration of `reporting.py` with `cli.py` and `main.py` is deferred to M8S4/M8S5

---

#### Functional Requirements

##### `FR-REPORTING_MODULE_EXPORTS`

- **Type**: Structured Schema Contract (Python module interface)
- **Interface Contract**: Module `reporting.py` exports four functions: `generate_badges(results: List[Dict[str, Any]]) -> None`, `generate_health_report(results: List[Dict[str, Any]]) -> None`, `generate_processed_skills(results: List[Dict[str, Any]]) -> None`, and `generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]`.
- **Expected Behavior**: Functions accept a list of skill result dictionaries, produce output files in the skills directory using deterministic naming and formatting. No parameters modify behavior after execution begins; side effects are limited to file I/O in the skills directory.
- **Observable Boundary**: Module import succeeds (`import reporting`); all four functions are callable; input of properly structured `List[Dict[str, Any]]` produces side effects (file creation in skills directory) with correct content; output files contain expected data structures.

##### `FR-REPORTING_BADGE_GENERATION`

- **Type**: Filesystem State Contract
- **Interface Contract**: `generate_badges(results: List[Dict[str, Any]]) -> None` creates `<skills_dir>/health_badges.md` with markdown table containing skill name, status emoji, last checked timestamp, validation score (2-decimal format), and stable suffix indicator. File must start with header `# Skill Health Check Badges` and end with table.
- **Expected Behavior**: File content follows exact markdown table format with columns: Skill Name, Status, Last Checked, Validation Score, Has Stable Suffix. Results sorted by skill name for deterministic ordering. Timestamps use ISO-like format.
- **Observable Boundary**: File existence confirmed; content matches expected markdown structure with correct number of lines and column count; skill rows appear in alphabetical order.

##### `FR-REPORTING_HEALTH_REPORT_JSON`

- **Type**: Filesystem State Contract
- **Interface Contract**: `generate_health_report(results: List[Dict[str, Any]]) -> None` creates `<skills_dir>/health_check_report.json` containing metadata (`timestamp`, `total_skills`, counts per status) and array of skill results.
- **Expected Behavior**: JSON contains exactly keys `timestamp`, `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, and `skills`. Timestamp is ISO 8601 format. All counts are integers. Skills array preserves order from input list.
- **Observable Boundary**: Valid JSON parseable; required keys present with correct types; counts match input results; timestamp format valid.

##### `FR-REPORTING_PROCESSED_SKILLS_JSON`

- **Type**: Filesystem State Contract
- **Interface Contract**: `generate_processed_skills(results: List[Dict[str, Any]]) -> None` creates `<skills_dir>/processed_skills.json` mapping skill name to result dictionary.
- **Expected Behavior**: File contains JSON object where each key is skill name and each value is the corresponding result dictionary from input. No extra keys added; values preserved exactly as in input.
- **Observable Boundary**: JSON parseable; object keys match skill names from input; values match original result dictionaries exactly.

##### `FR-REPORTING_SKILL_SUMMARY_FUNCTION`

- **Type**: Structured Schema Contract
- **Interface Contract**: `generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]` returns summary dictionary with `summary` object containing counts and distributions, and `skills` array containing all input results.
- **Expected Behavior**: Summary includes `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, `stable_ready_count`, and `generation_timestamp`. Status distribution object contains arrays of skills grouped by status.
- **Observable Boundary**: Returned dictionary contains required top-level keys; counts match input; distributions group skills correctly by status; timestamp present and recent.

---

#### Non-Functional Requirements

##### `NFR-REPORTING_MODULAR_INDEPENDENCE`

- **Constraint**: `reporting.py` MUST be importable and testable without importing `cli.py`, `main.py`, or `core.validation`. The only allowed cross-module dependency is `discovery` for the skills directory path.
- **Verification**: Unit tests in `tests/M8/S3/` import only `reporting` and standard library modules; no import of `cli`, `main`, or `core.validation` is present in either `reporting.py` or its test files.

##### `NFR-REPORTING_TYPE_HINTS`

- **Constraint**: All public functions annotated with Python type hints (`List[Dict[str, Any]]`, `Dict[str, Any]`, `None`).
- **Verification**: Static inspection via `typing.get_type_hints` confirms annotations on all four public functions.

##### `NFR-REPORTING_BACKWARD_COMPATIBILITY`

- **Constraint**: Reporting output must be structurally equivalent to pre-refactor `healthcheck.py` report formats: identical JSON schema, markdown table format, file naming conventions, and content ordering.
- **Verification**: Unit tests compare output against reference outputs derived from existing `healthcheck_modular_spec.md` criteria; test fixtures contain expected reference content.

##### `NFR-REPORTING_DETERMINISTIC_OUTPUT`

- **Constraint**: Report generation must be deterministic: identical input always produces identical output, with consistent ordering and formatting.
- **Verification**: Multiple invocations of reporting functions with same input produce byte-identical output files; sorting applied where required (skill names in badges table).

---

#### Architecture Impact

##### Strict File Scope (Allowlist & Denylist)

**Allowlist (Files permitted to change):**

- `reporting.py` — New module; all reporting functionality implementation
- `tests/M8/S3/` (or equivalent) — Unit tests for M8S3
- `tests/fixtures/reporting/` — Synthetic results data for testing

**Denylist (Do NOT Touch):**

- `healthcheck.py` — Existing wrapper; preserved for backward compatibility until M8S5
- `core/validation.py` — Implemented in M8S1; do not modify
- `discovery.py` — Implemented in M8S2; do not modify
- `cli.py`, `main.py` — Deferred to M8S4/M8S5
- `tests/M8/S1/`, `tests/M8/S2/` — Existing module tests; no modifications
- All `*.json`, `index.js`, `skills/<name>/SKILL.md` fixture files

##### Affected Modules

- `reporting.py` (new) — Pure reporting module; no modifications to existing modules in this spec.

##### New Modules

- `reporting.py`

  * Export: `def generate_badges(results: List[Dict[str, Any]]) -> None`
  * Export: `def generate_health_report(results: List[Dict[str, Any]]) -> None`
  * Export: `def generate_processed_skills(results: List[Dict[str, Any]]) -> None`
  * Export: `def generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]`
  * Optional: `class ReportingError(Exception)` for structured error signaling

##### Removed Modules

- None — M8S3 creates a new module; no deprecations in this sequence.

##### Public Interfaces

- `reporting.generate_badges(results: List[Dict[str, Any]]) -> None` — Creates `health_badges.md` file
- `reporting.generate_health_report(results: List[Dict[str, Any]]) -> None` — Creates `health_check_report.json` file
- `reporting.generate_processed_skills(results: List[Dict[str, Any]]) -> None` — Creates `processed_skills.json` file
- `reporting.generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]` — Returns summary dictionary
- `reporting.ReportingError` (custom exception, optional)

---

#### Interface Boundaries

##### Module Thresholds

- `reporting.py` receives: structured `List[Dict[str, Any]]` from caller (validation results)
- `reporting.py` returns: `None` (side-effect operations) for three file-generation functions, or `Dict[str, Any]` for summary function
- `reporting.py` consumes no environment variables; all configuration flows through function parameters
- Output files created in skills directory using `discovery.SKILLS_DIR_NAME` constant via `discovery.get_skills_directory()`

##### Schema Contracts

```json
{
  "type": "object",
  "required": ["generate_badges", "generate_health_report", "generate_processed_skills", "generate_skills_summary"],
  "properties": {
    "generate_badges": {
      "type": "function",
      "signature": "(results: List[Dict[str, Any]]) -> None",
      "output": {
        "type": "filesystem",
        "file": "health_badges.md",
        "format": "markdown",
        "contains": ["Skill Name", "Status", "Last Checked", "Validation Score", "Has Stable Suffix"]
      }
    },
    "generate_health_report": {
      "type": "function",
      "signature": "(results: List[Dict[str, Any]]) -> None",
      "output": {
        "type": "filesystem",
        "file": "health_check_report.json",
        "format": "json",
        "schema": {
          "required": ["timestamp", "total_skills", "healthy_count", "needs_review_count", "error_count", "skipped_count", "skills"],
          "properties": {
            "timestamp": {"type": "string", "format": "date-time"},
            "total_skills": {"type": "integer"},
            "healthy_count": {"type": "integer"},
            "needs_review_count": {"type": "integer"},
            "error_count": {"type": "integer"},
            "skipped_count": {"type": "integer"},
            "skills": {"type": "array", "items": {"type": "object"}}
          }
        }
      }
    },
    "generate_processed_skills": {
      "type": "function",
      "signature": "(results: List[Dict[str, Any]]) -> None",
      "output": {
        "type": "filesystem",
        "file": "processed_skills.json",
        "format": "json",
        "schema": {
          "type": "object",
          "additionalProperties": true
        }
      }
    },
    "generate_skills_summary": {
      "type": "function",
      "signature": "(results: List[Dict[str, Any]]) -> Dict[str, Any]",
      "output": {
        "type": "dictionary",
        "keys": ["summary", "skills", "status_distribution"],
        "summary": {
          "required": ["total_skills", "healthy_count", "needs_review_count", "error_count", "skipped_count", "stable_ready_count", "generation_timestamp"]
        }
      }
    }
  }
}
```

---

#### Implementation Tasks

1. Create `reporting.py` defining optional custom error class `ReportingError` `[FR-REPORTING_MODULE_EXPORTS]`
2. Implement `generate_badges(results: List[Dict[str, Any]]) -> None` creating `health_badges.md` with markdown table `[FR-REPORTING_BADGE_GENERATION]`
3. Implement `generate_health_report(results: List[Dict[str, Any]]) -> None` creating `health_check_report.json` with proper schema `[FR-REPORTING_HEALTH_REPORT_JSON]`
4. Implement `generate_processed_skills(results: List[Dict[str, Any]]) -> None` creating `processed_skills.json` mapping skill names to results `[FR-REPORTING_PROCESSED_SKILLS_JSON]`
5. Implement `generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]` returning comprehensive summary dictionary `[FR-REPORTING_SKILL_SUMMARY_FUNCTION]`
6. Add type hints on all public functions and constants per `NFR-REPORTING_TYPE_HINTS`
7. Confirm zero module-level mutable globals; only immutable constants and function definitions at module scope
8. Ensure `reporting.py` imports only from `discovery` (for skills directory) and standard library
9. Create synthetic fixture `tests/fixtures/reporting/` with deterministic `results: List[Dict[str, Any]]` for testing `[FR-REPORTING_BADGE_GENERATION]`, `[FR-REPORTING_HEALTH_REPORT_JSON]`, `[FR-REPORTING_PROCESSED_SKILLS_JSON]`
10. Write `tests/M8/S3/test_reporting.py` covering badge generation, JSON report creation, processed skills mapping, summary generation, and modular independence `[FR-REPORTING_MODULE_EXPORTS]`, `[FR-REPORTING_BADGE_GENERATION]`, `[FR-REPORTING_HEALTH_REPORT_JSON]`, `[FR-REPORTING_PROCESSED_SKILLS_JSON]`, `[FR-REPORTING_SKILL_SUMMARY_FUNCTION]`, `[NFR-REPORTING_MODULAR_INDEPENDENCE]`

---

#### Constraints

- MUST NOT modify `healthcheck.py`, `core/validation.py`, `discovery.py`, `cli.py`, `main.py`, or any binary/fixture not listed in the Allowlist.
- MUST NOT scan or analyze `bin/` directory contents (per skill prohibition); all required properties are derived from the milestone's Integration Bindings table.
- MUST NOT redefine validation contracts from M8S1, nor discovery contracts from M8S2, nor CLI/main contracts from M8S4/M8S5.
- MUST NOT introduce module-level mutable global state.
- MUST NOT require environment variables; all configuration flows through function parameters.
- No sequential numeric FR IDs permitted (semantic IDs used: `FR-REPORTING_MODULE_EXPORTS`, `FR-REPORTING_BADGE_GENERATION`, `FR-REPORTING_HEALTH_REPORT_JSON`, `FR-REPORTING_PROCESSED_SKILLS_JSON`, `FR-REPORTING_SKILL_SUMMARY_FUNCTION`).
- MUST NOT describe internal data routing or algorithm steps beyond interface contracts (no data-flow descriptions inside module).

---

#### Assumptions

- Validation results (from `core.validation.SkillValidator`) are `Dict[str, Any]` with keys: `name`, `status`, `validation_score`, `has_stable_suffix`, `last_checked`, `errors`
- `discovery.SKILLS_DIR_NAME` constant equals `"skills"` and is importable
- The skills directory exists and is writable
- Generated report files should be machine-readable and human-readable
- Timestamps in reports should be recent and consistent
- JSON reports should be properly formatted for external tools

---

#### Acceptance Criteria

- `reporting.py` exists and exports all four reporting functions `[FR-REPORTING_MODULE_EXPORTS]`
- `generate_badges()` creates `health_badges.md` with correct markdown table format and sorted skill names `[FR-REPORTING_BADGE_GENERATION]`
- `generate_health_report()` creates valid JSON with required schema and correct counts `[FR-REPORTING_HEALTH_REPORT_JSON]`
- `generate_processed_skills()` creates JSON mapping skill names to results `[FR-REPORTING_PROCESSED_SKILLS_JSON]`
- `generate_skills_summary()` returns dictionary with summary, skills, and status distributions `[FR-REPORTING_SKILL_SUMMARY_FUNCTION]`
- Type hints present on all public functions per `NFR-REPORTING_TYPE_HINTS`
- Unit tests import only `reporting` and standard library modules; no import of `cli`, `main`, or `core.validation` `[NFR-REPORTING_MODULAR_INDEPENDENCE]`
- No module-level mutable globals introduced in `reporting.py`
- No modifications made to `healthcheck.py`, `core/validation.py`, `discovery.py`, `cli.py`, or `main.py` (scope enforcement)

---

#### User Approval

* [x] Approved for implementation by user

#### Next Steps

Run `/generate-verification` to create the verification protocol (`SPEC-M8S3V.md`) for the reporting contracts defined above, then proceed to `generate-tests` for M8S3.