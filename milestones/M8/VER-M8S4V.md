---
derived_from:
- SPEC-M8S4
- M8
id: VER-M8S4V
milestone_id: M8
status: draft
template_version: 1.1.0
title: M8S4 - CLI Module Verification Protocol
type: verification
---

# M8S4 - CLI Module Verification Protocol



## Success Criteria

- `cli.py` exists at the project root and imports without side effects.
- `cli.py` exports all six public functions: `parse_arguments`, `validate_single_skill`, `process_all_skills`, `run_health_check`, `print_help`, `generate_all_reports`.
- `parse_arguments()` produces correct `argparse.Namespace` attributes for `[]`, `['my_skill']`, `['--all']`, and `['--help']` invocations.
- `validate_single_skill("nonexistent")` returns `None` and writes to stderr; `validate_single_skill(valid_name)` returns a result dict matching the `SkillValidator.validate()` output schema.
- `process_all_skills()` returns a list whose length equals `len(discover_skills())`, with batch headers in order (Batch 1: Core, Batch 2: Extensions, Batch 3: Edge Cases).
- `run_health_check()` with no args returns list matching default mode; with `skill_name` delegates to single mode; with `all_flag=True` delegates to batch mode.
- `generate_all_reports()` creates `health_badges.md`, `health_check_report.json`, `processed_skills.json` in the skills directory; stdout contains a summary with correct counts.
- `print_help()` writes to stdout containing all required substrings; `--help` invocation exits with code 0.
- Exceptions during validation are caught, printed to stderr, and an empty list is returned; `KeyboardInterrupt` handled gracefully.
- `python3 skills/healthcheck/healthcheck.py` exits 0 on valid skills, 1 on errors; `index.js` wrapper completes.
- All public functions carry Python type hints.
- `cli.py` imports only from `core.validation`, `discovery`, `reporting`, and stdlib.
- `cli.py` has zero module-level mutable global state.
- Unit tests import only `cli` and stdlib; no import of `main`, `index.js`, or orchestration layers.
