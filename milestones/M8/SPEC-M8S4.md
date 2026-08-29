---
derived_from:
- M8
- SPEC-M8S1
- SPEC-M8S2
- SPEC-M8S3
id: SPEC-M8S4
milestone_id: M8
status: draft
template_version: 1.2.0
type: specification
---

# Title



#### Objective

Transform the CLI argument parsing and orchestration logic from the existing monolithic wrapper into a focused `cli.py` module at the project root. This module provides the command-line interface contract, orchestrates validation discovery and execution across single-skill and batch modes, and coordinates report generation — while maintaining backward compatibility with the existing `python3 healthcheck.py [skill_name]` and `python3 healthcheck.py --all` invocation patterns.

##### Milestone Complexity & Multi-Spec Plan

Milestone M8 decomposes into exactly 5 sequential specifications:

- **M8S1** (completed): Core validation module (`core/validation.py`)
- **M8S2** (completed): Discovery module (`discovery.py`)
- **M8S3** (completed): Reporting module (`reporting.py`)
- **M8S4** (this spec): CLI module (`cli.py`) — argument parsing and orchestration
- **M8S5**: Main entry point (`main.py`) with minimal glue logic

This spec addresses only HCS4 (CLI). It MUST NOT redefine validation contracts from M8S1, discovery contracts from M8S2, nor reporting contracts from M8S3.

#### Followup Context

##### Derived From

- `M8` (Milestone - HealthCheck Skill Modular Refactoring)
- `SPEC-M8S1` (Prior Specification - Core Validation Module)
- `SPEC-M8S2` (Prior Specification - Discovery Module)
- `SPEC-M8S3` (Prior Specification - Reporting Module)

##### Prior Work Completed

- `core/validation.py` exports `SkillValidator` with `validate(content: str) -> Dict[str, Any]`, `Validator` base class, `ValidationError`, `validate_skill_content(content: str) -> Dict[str, Any]`, and `ValidationResult` dataclass.
- `discovery.py` exports `discover_skills(project_root: Path | str) -> List[str]`, `find_project_root(start: Path | str | None = None) -> Path`, `get_skills_directory(project_root: Path | str | None = None) -> Path`, `SKILLS_DIR_NAME: str = "skills"`, and `DiscoveryError`.
- `reporting.py` exports `generate_badges(results: List[Dict[str, Any]]) -> None`, `generate_health_report(results: List[Dict[str, Any]]) -> None`, `generate_processed_skills(results: List[Dict[str, Any]]) -> None`, `generate_skills_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]`, and `ReportingError`.

##### Remaining Gaps

- M8S4 (this spec): CLI argument parsing, single-skill validation, batch processing (3 batches), default mode, and report generation orchestration.
- M8S5: Main entry point orchestrator and integration with `skills/healthcheck/healthcheck.py` wrapper and `skills/healthcheck/index.js`.
