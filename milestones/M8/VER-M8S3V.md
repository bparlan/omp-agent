---
id: VER-M8S3V
type: verification
title: "M8S3 - Reporting Module Verification Protocol"
milestone_id: M8
status: draft
derived_from:
  - M8
  - SPEC-M8S3
template_version: 1.1.0
---

## Success Criteria

- `reporting.py` exists at the project root and is importable without side effects.
- `reporting.py` exports four functions: `generate_badges`, `generate_health_report`, `generate_processed_skills`, `generate_skills_summary`.
- `generate_badges(results)` creates `skills/health_badges.md` with a markdown table containing columns: Skill Name, Status, Last Checked, Validation Score, Has Stable Suffix; skill rows sorted alphabetically; file starts with `# Skill Health Check Badges`.
- `generate_health_report(results)` creates `skills/health_check_report.json` with keys `timestamp` (ISO 8601), `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, `skills` (array); all counts are integers; skills array preserves input order.
- `generate_processed_skills(results)` creates `skills/processed_skills.json` mapping skill name strings to their result dictionaries; values preserved exactly as input.
- `generate_skills_summary(results)` returns a dict with keys `summary`, `skills`, `status_distribution`; `summary` contains `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, `stable_ready_count`, `generation_timestamp`; `status_distribution` groups skills by status.
- All four public functions carry Python type hints (`List[Dict[str, Any]]`, `Dict[str, Any]]`, `None`).
- `reporting.py` contains no module-level mutable global state.
- `reporting.py` and its test file import only stdlib + `discovery`; no import of `cli`, `main`, `core.validation`, or `healthcheck`.
- Identical input to any reporting function produces byte-identical output across repeated invocations.
- Diff-scope allowlist enforcement: only Allowlist files appear in the implementation diff.

---

## Followup Context

### Derived From

- `M8` (Milestone - HealthCheck Skill Modular Refactoring)
- `SPEC-M8S3` (Source Specification - Reporting Module)

### Reusable Items from Prior Verifications

- **Synthetic fixture pattern**: a deterministic `results: List[Dict[str, Any]]` in `tests/fixtures/reporting/` containing at least 4 skill entries spanning different statuses (`healthy`, `needs_review`, `error`, `skipped`), with explicit `name`, `status`, `validation_score`, `has_stable_suffix`, `last_checked`, and `errors` keys.
- **Modular-independence import audit**: AST-level inspection of `reporting.py` and its test file for forbidden imports.
- **No-mutable-globals AST inspection**: Same pattern used in M8S2 VI-15, adapted for `reporting.py`.
- **Diff-scope allowlist gate**: `git diff --name-only` checked against the M8S3 Allowlist.

### New Verification Required

- File-generation side effects for each of the three output files (`health_badges.md`, `health_check_report.json`, `processed_skills.json`).
- Markdown table structure and alphabetical sorting in `health_badges.md`.
- JSON schema validation for `health_check_report.json` (required keys, types, count correctness).
- Identity-preserving mapping in `processed_skills.json` (skill name → original result dict).
- Summary dictionary structure and distribution grouping from `generate_skills_summary`.
- Deterministic byte-identical output across repeated invocations.
- Type hint coverage on all four public functions via `typing.get_type_hints`.

---

## Functional Validation

### VI-1: `reporting` module imports and exports all four functions

- **Source Requirement ID**: `FR-REPORTING_MODULE_EXPORTS`
- **Verification Method**: `UNIT_TEST`
- **Target**: `reporting` module namespace.
- **Preconditions**: `reporting.py` exists at the project root.
- **Input or fixture**: `import reporting`; inspect `dir(reporting)` for the four function names.
- **Expected Evidence**: `hasattr(reporting, "generate_badges")`, `hasattr(reporting, "generate_health_report")`, `hasattr(reporting, "generate_processed_skills")`, `hasattr(reporting, "generate_skills_summary")` all return `True`; each is callable.
- **Failure Condition**: Import raises `ModuleNotFoundError`/`ImportError`; any function is missing or not callable.
- **Initial Failure Expectation**: `ModuleNotFoundError: No module named 'reporting'`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All four functions present and callable; exit 0.

### VI-2: `generate_badges` creates `health_badges.md` with correct markdown table

- **Source Requirement ID**: `FR-REPORTING_BADGE_GENERATION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `reporting.generate_badges`.
- **Preconditions**: `reporting.py` importable; a temporary writable skills directory exists; synthetic fixture results loaded.
- **Input or fixture**: A `results` list with at least 4 entries spanning statuses `healthy`, `needs_review`, `error`, `skipped`; each entry has keys `name`, `status`, `validation_score` (float), `has_stable_suffix` (bool), `last_checked` (ISO 8601 string), `errors` (list or None). The `name` values are NOT in alphabetical order on disk to prove sorting. Call `generate_badges(results)`.
- **Expected Evidence**: File `skills/health_badges.md` exists; first line is `# Skill Health Check Badges`; file contains a markdown table with header row `| Skill Name | Status | Last Checked | Validation Score | Has Stable Suffix |`; separator row uses `|---|`; skill rows appear in alphabetical order by `name`; `validation_score` formatted to exactly 2 decimal places; `has_stable_suffix` rendered as a boolean indicator.
- **Failure Condition**: File does not exist; header incorrect; column count mismatches; rows not sorted alphabetically; score format incorrect.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: File content matches all structural requirements; exit 0.

### VI-3: `generate_health_report` creates `health_check_report.json` with correct schema

- **Source Requirement ID**: `FR-REPORTING_HEALTH_REPORT_JSON`
- **Verification Method**: `UNIT_TEST`
- **Target**: `reporting.generate_health_report`.
- **Preconditions**: `reporting.py` importable; temporary writable skills directory exists; same synthetic fixture results as VI-2.
- **Input or fixture**: Same `results` list as VI-2. Call `generate_health_report(results)`.
- **Expected Evidence**: File `skills/health_check_report.json` exists; parses as valid JSON; top-level keys are exactly: `timestamp`, `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, `skills`; `timestamp` matches ISO 8601 format (`datetime.fromisoformat` parses without error); `total_skills` equals `len(results)`; `healthy_count` equals count of entries where `status == "healthy"`; `needs_review_count` equals count of `"needs_review"`; `error_count` equals count of `"error"`; `skipped_count` equals count of `"skipped"`; `skills` is a `list` with length equal to `total_skills` and preserves the input order.
- **Failure Condition**: File missing or invalid JSON; required keys absent; counts incorrect; types wrong; order not preserved.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: JSON schema and counts verified; exit 0.

### VI-4: `generate_processed_skills` creates `processed_skills.json` mapping skill names to results

- **Source Requirement ID**: `FR-REPORTING_PROCESSED_SKILLS_JSON`
- **Verification Method**: `UNIT_TEST`
- **Target**: `reporting.generate_processed_skills`.
- **Preconditions**: `reporting.py` importable; temporary writable skills directory exists; same synthetic fixture results.
- **Input or fixture**: Same `results` list. Call `generate_processed_skills(results)`.
- **Expected Evidence**: File `skills/processed_skills.json` exists; parses as valid JSON; top-level type is `dict`; number of keys equals `len(results)`; every key matches a `name` value from the input; for each key, the corresponding value is `dict`-equal to the original result dictionary from the input list (deep equality); no extra keys introduced.
- **Failure Condition**: File missing; not a dict; key count mismatch; any value differs from the original result dict; extra keys present.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Identity-preserving mapping verified; exit 0.

### VI-5: `generate_skills_summary` returns correct summary dictionary

- **Source Requirement ID**: `FR-REPORTING_SKILL_SUMMARY_FUNCTION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `reporting.generate_skills_summary`.
- **Preconditions**: `reporting.py` importable; same synthetic fixture results.
- **Input or fixture**: Same `results` list. Call `result = generate_skills_summary(results)`.
- **Expected Evidence**: `result` is a `dict`; top-level keys are exactly `summary`, `skills`, `status_distribution`; `summary` is a dict with keys `total_skills`, `healthy_count`, `needs_review_count`, `error_count`, `skipped_count`, `stable_ready_count`, `generation_timestamp`; `total_skills` equals `len(results)`; `healthy_count`/`needs_review_count`/`error_count`/`skipped_count` match counts from input; `stable_ready_count` equals count of entries where `has_stable_suffix` is `True`; `generation_timestamp` is a recent ISO 8601 string; `skills` is a list with length equal to `total_skills`; `status_distribution` is a dict whose keys are the unique statuses in the input, and each value is a list of skill names with that status.
- **Failure Condition**: Missing top-level keys; count values incorrect; `stable_ready_count` absent or wrong; timestamp absent or unparseable; `status_distribution` groups incorrect.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All keys, counts, and distributions verified; exit 0.

### VI-6: All public functions carry Python type hints

- **Source Requirement ID**: `NFR-REPORTING_TYPE_HINTS`
- **Verification Method**: `UNIT_TEST` (via `typing.get_type_hints`)
- **Target**: `reporting.generate_badges`, `reporting.generate_health_report`, `reporting.generate_processed_skills`, `reporting.generate_skills_summary`.
- **Preconditions**: `reporting.py` importable.
- **Input or fixture**: Call `typing.get_type_hints` on each of the four functions.
- **Expected Evidence**: Each function's annotations include a `results` parameter typed as `List[Dict[str, Any]]`; return annotation matches the documented type (`None` for the three file-generation functions, `Dict[str, Any]` for the summary function).
- **Failure Condition**: Any public function lacks annotations; `get_type_hints` raises `NameError`/`TypeError`; parameter or return type does not match the specification.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All four functions have correct annotations; exit 0.

### VI-7: `reporting.py` and its test file import only stdlib + `discovery`

- **Source Requirement ID**: `NFR-REPORTING_MODULAR_INDEPENDENCE`
- **Verification Method**: `UNIT_TEST` (AST inspection)
- **Target**: `reporting.py` source and `tests/M8/S3/test_reporting.py` source.
- **Preconditions**: Both files exist.
- **Input or fixture**: Parse both files with `ast`; collect every `Import`/`ImportFrom` module name. The forbidden set is `{"cli", "main", "core", "core.validation", "healthcheck", "reporting"}` (self-import excluded). Stdlib modules, `discovery`, `typing`, `json`, `pathlib`, `datetime`, and `pytest` (test file only) are allowed.
- **Expected Evidence**: No forbidden import detected in either file.
- **Failure Condition**: Any forbidden import is present.
- **Initial Failure Expectation**: `FileNotFoundError` for one or both files; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Only allowed imports; exit 0.

### VI-8: `reporting.py` has no module-level mutable global state

- **Source Requirement ID**: NFR-level constraint (no module-level mutable globals)
- **Verification Method**: `UNIT_TEST` (AST inspection)
- **Target**: `reporting.py` source.
- **Preconditions**: `reporting.py` exists at the project root.
- **Input or fixture**: Parse `reporting.py` with `ast.parse`; collect module-level `Assign`/`AnnAssign`/`AugAssign` targets whose values are mutable types (`list`, `dict`, `set`) or calls returning them. Only `ReportingError` class definition, function definitions, and immutable constants (strings, numbers, tuples of immutables) are permitted.
- **Expected Evidence**: The set of module-level mutable bindings is empty.
- **Failure Condition**: Any module-level mutable binding (list, dict, set literal or call) is detected.
- **Initial Failure Expectation**: `FileNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: No mutable globals; exit 0.

### VI-9: Reporting output is deterministic across repeated invocations

- **Source Requirement ID**: `NFR-REPORTING_DETERMINISTIC_OUTPUT`
- **Verification Method**: `UNIT_TEST`
- **Target**: All four reporting functions invoked twice with identical input.
- **Preconditions**: `reporting.py` importable; two separate temporary writable skills directories (or clean/reset between calls).
- **Input or fixture**: Same `results` list. Call each function twice against clean output directories.
- **Expected Evidence**: For `generate_badges`: both `health_badges.md` files are byte-identical. For `generate_health_report`: both `health_check_report.json` files are byte-identical. For `generate_processed_skills`: both `processed_skills.json` files are byte-identical. For `generate_skills_summary`: both return values are `==`-equal.
- **Failure Condition**: Any pair of outputs differs; any invocation raises.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All four functions produce identical output on repeated invocation; exit 0.

### VI-10: Diff-scope allowlist enforcement

- **Source Requirement ID**: Spec-level constraint (Strict File Scope)
- **Verification Method**: `SCRIPT_EXECUTION` (`git diff --name-only`)
- **Target**: Repository working tree after implementation.
- **Preconditions**: Implementation changes are present in the working tree.
- **Input or fixture**: `git diff --name-only`.
- **Expected Evidence**: Every file in the diff is a member of the M8S3 Allowlist:
  - `reporting.py`
  - `tests/M8/S3/test_reporting.py`
  - `tests/fixtures/reporting/**`
  No file from the Denylist (`healthcheck.py`, `core/validation.py`, `discovery.py`, `cli.py`, `main.py`, `tests/M8/S1/**`, `tests/M8/S2/**`, any unrelated `*.json`/`index.js`/`skills/<name>/SKILL.md`) appears in the diff.
- **Failure Condition**: Any file outside the Allowlist appears in the diff.
- **Initial Failure Expectation**: Pre-implementation diff is empty or contains only stub scaffolding; gate trivially passes.
- **Post-Implementation Success Expectation**: Allowlist-only diff; exit 0.

---

## Edge Cases

- `generate_badges` called with an empty `results` list → `health_badges.md` contains only the header and table header (no data rows); no exception.
- `generate_health_report` called with an empty `results` list → `health_check_report.json` has all counts set to `0` and `skills` as `[]`.
- `generate_processed_skills` called with an empty `results` list → `processed_skills.json` is an empty JSON object `{}`.
- `generate_skills_summary` called with an empty `results` list → all counts are `0`, `skills` is `[]`, `status_distribution` is `{}`.
- `generate_badges` called with results containing a `validation_score` of `0.0` → formatted as `0.00` (not `.00` or `0.0`).
- `generate_badges` called with results containing a `validation_score` of `1.0` → formatted as `1.00` (not `1` or `1.0`).
- `generate_badges` called with `has_stable_suffix=True` and `False` → both rendered correctly in the table.
- Skill names containing special characters (hyphens, underscores, dots) → rendered verbatim in badge table and used as keys in `processed_skills.json`.
- `generate_skills_summary` with all results sharing the same status → `status_distribution` has exactly one key.
- Output files are overwritten without error on repeated invocation (idempotent).

---

## Failure Scenarios

- Missing `reporting.py` → all VI-1..VI-9 tests fail with `ModuleNotFoundError: No module named 'reporting'`; classified as `VALID_INITIAL_FAILURE`.
- `generate_badges` produces incorrect markdown structure → VI-2 fails.
- `generate_health_report` produces JSON with wrong keys or incorrect counts → VI-3 fails.
- `generate_processed_skills` loses data fidelity (values differ from input) → VI-4 fails.
- `generate_skills_summary` missing `stable_ready_count` or `status_distribution` → VI-5 fails.
- `reporting.py` imports from `cli`, `main`, `core.validation`, or `healthcheck` → VI-7 fails.
- `reporting.py` contains a module-level mutable list/dict/set → VI-8 fails.
- Output not byte-identical on repeated invocation → VI-9 fails.
- Implementation modifies files outside the Allowlist → VI-10 fails the diff-scope check.
- Type hints absent or incorrect on any public function → VI-6 fails.

---

## Regression Checklist

- [ ] `generate_badges` produces the same markdown structure as pre-refactor `healthcheck.py` badge generation (NFR-REPORTING_BACKWARD_COMPATIBILITY).
- [ ] `generate_health_report` JSON schema matches pre-refactor `health_check_report.json` schema.
- [ ] `generate_processed_skills` JSON structure matches pre-refactor output mapping.
- [ ] `generate_skills_summary` includes `stable_ready_count` not present in prior monolithic output (new capability, not regression).
- [ ] Type hints present on all four public functions (VI-6).
- [ ] No module-level mutable global state introduced (VI-8).
- [ ] No forbidden cross-module imports introduced (VI-7).
- [ ] Denylist files unmodified (VI-10).
- [ ] Deterministic output verified (VI-9).

---

## Manual Validation

1. Run `python3 -c "import reporting; print(dir(reporting))"` and confirm all four function names are present.
2. Run `python3 -c "import inspect, reporting; print(inspect.signature(reporting.generate_badges)); print(inspect.signature(reporting.generate_skills_summary))"` and confirm signatures match the specification.
3. Run `python3 -c "import typing, reporting; print(typing.get_type_hints(reporting.generate_badges)); print(typing.get_type_hints(reporting.generate_skills_summary))"` and confirm type annotations are present and correct.
4. Create a temporary skills directory, populate a `results` list with 3 sample skill dicts, call `generate_badges(results)`, then `cat skills/health_badges.md` and confirm the markdown table with alphabetically sorted rows.
5. Call `generate_health_report(results)` then `cat skills/health_check_report.json | python3 -m json.tool` and confirm valid JSON with correct counts.
6. Call `generate_processed_skills(results)` then `cat skills/processed_skills.json | python3 -m json.tool` and confirm key-to-dict mapping.
7. Call `summary = generate_skills_summary(results)` and inspect `summary["summary"]` keys and `summary["status_distribution"]` grouping.
8. Run `python3 -c "import ast; src = open('reporting.py').read(); tree = ast.parse(src); mutable = [n for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign)) and isinstance(getattr(n, 'value', None) or getattr(n, 'annotation', None), (ast.List, ast.Dict, ast.Set))]; print('Mutable globals:', len(mutable))"` and confirm output is `0`.

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

_This mechanical check must be executed by `evaluate-implementation` before tests are considered passed._

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the Allowlist defined in `SPEC-M8S3`. The Allowlist is:
  - `reporting.py`
  - `tests/M8/S3/test_reporting.py`
  - `tests/fixtures/reporting/**` (synthetic fixture tree)
  If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

#### Pre-Implementation Initial-Failure Contract

- For every `UNIT_TEST` verification item above, the test is expected to FAIL pre-implementation with `ModuleNotFoundError: No module named 'reporting'` (or the equivalent `ImportError`).
- The test runner MUST classify this as `VALID_INITIAL_FAILURE` and unblock the pre-implementation gate.
- The runner MUST NOT classify a `ModuleNotFoundError` whose source is a malformed test file as `INVALID_TEST`; the loader-level failure is the only `INVALID_TEST` signal.

#### Test Commands

- Regression: `pytest tests/M8/S1/ -q` and `pytest tests/M8/S2/ -q` (must remain green)
- New tests: `pytest tests/M8/S3/test_reporting.py -v`
- Combined: `pytest tests/M8/ -q`

---

## Expected Outcomes

- All 10 verification items pass.
- `reporting.py` exists, is importable, and exports `generate_badges`, `generate_health_report`, `generate_processed_skills`, and `generate_skills_summary`.
- `generate_badges` creates `skills/health_badges.md` with a markdown table: header row, separator row, and skill data rows sorted alphabetically; validation scores formatted to 2 decimal places.
- `generate_health_report` creates `skills/health_check_report.json` with valid ISO 8601 timestamp, correct integer counts, and an ordered skills array.
- `generate_processed_skills` creates `skills/processed_skills.json` mapping each skill name to its original result dictionary with no data loss.
- `generate_skills_summary` returns a dictionary with `summary` (counts + timestamp), `skills` (full input list), and `status_distribution` (status-keyed skill name lists).
- All four public functions have Python type hints verified via `typing.get_type_hints`.
- `reporting.py` imports only from stdlib and `discovery`; no cross-module dependencies on `cli`, `main`, `core.validation`, or `healthcheck`.
- No module-level mutable global state in `reporting.py`.
- Identical input produces byte-identical output across repeated invocations (deterministic).
- The diff-scope allowlist is respected; no Denylist file is modified.
- Existing M8S1 and M8S2 tests remain green (regression check).
