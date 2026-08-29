---
id: VER-M8S2V
type: verification
title: "M8S2 - Discovery Module Verification Protocol"
milestone_id: M8
status: draft
derived_from:
  - M8
  - M8S1
  - SPEC-M8S2
template_version: 1.1.0
---

## Success Criteria

- `discovery.py` exists at the project root and is importable without side effects.
- `discovery.discover_skills(project_root)` returns a deterministic, lexicographically sorted `List[str]` of skill directory basenames under `<project_root>/skills/` that contain a `SKILL.md` file.
- `discovery.find_project_root(start)` returns an absolute `pathlib.Path` resolved to the nearest ancestor containing `skills/`, `package.json`, or `pyproject.toml`; defaults to `Path.cwd()` and never raises for missing markers.
- `discovery.SKILLS_DIR_NAME == "skills"` and is importable as a module-level string constant.
- `discovery.DiscoveryError` is defined as a subclass of `Exception` (optional but specified).
- `discovery.py` declares type hints on every public function and the `SKILLS_DIR_NAME` constant.
- `discovery.py` contains no module-level mutable global state.
- `discovery.py` and its test file import only stdlib + each other; no import of `cli`, `reporting`, `main`, or `core.validation`.
- Diff-scope check: only files in the Allowlist are modified by the implementation.

---

## Followup Context

### Derived From

- `M8` (Milestone - HealthCheck Skill Modular Refactoring)
- `M8S1` (Prior Specification - Core Validation Module; provides `SkillValidator` downstream consumer)
- `SPEC-M8S2` (Source Specification - Discovery Module)

### Reusable Items from Prior Verifications

- **Synthetic fixture pattern (`tests/fixtures/discovery/synthetic_project/skills/`)**: a deterministic directory tree containing valid skills, a directory without `SKILL.md`, a hidden directory, and (optionally) a symlink. Mirrors the `tests/fixtures/synthetic_python` pattern from M8S1.
- **Modular-independence import audit**: assert that `discovery.py` and `tests/M8/S2/test_discovery.py` import only stdlib + `discovery` (no `cli`/`reporting`/`main`/`core.validation`).
- **Diff-scope allowlist gate**: enforce the same `git diff --name-only` allowlist check that M8S1 used, against the M8S2 Allowlist.

### New Verification Required

- Items specific to the discovery contracts: skill enumeration, lexicographic ordering, project-root marker detection, error tolerance (missing `skills/`, unreadable subdir, `None`/empty `start`).
- Initial-failure exit-code contract for pre-implementation gate: 127 (Command Not Found) when `discovery.py` is absent.

---

## Functional Validation

### VI-1: `discover_skills` returns a sorted list of skill basenames

- **Source Requirement ID**: `FR-DISCOVERY_MODULE_EXPORTS`, `FR-SKILL_LISTING_FROM_FIXTURE`, `FR-DETERMINISTIC_SORT_ORDER`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills(project_root)` invoked against the synthetic fixture `tests/fixtures/discovery/synthetic_project/`.
- **Preconditions**: Fixture directory exists with N subdirectories under `skills/`, M of which contain a `SKILL.md` file; M ≥ 2; skill basenames include at least one entry that is NOT in lexicographic order on disk (to prove sorting).
- **Input or fixture**: `Path("tests/fixtures/discovery/synthetic_project")` (a `Path` argument; an equivalent `str` argument is also exercised for type-union coverage).
- **Expected Evidence**: Returned value is a `list` of `str`; length equals M; each entry is a directory basename; `result == sorted(result)` is `True`; the order matches lexicographic ordering of the basenames, not the on-disk order.
- **Failure Condition**: Return is not a list, contains non-string entries, is missing any skill with a `SKILL.md`, includes any directory without a `SKILL.md`, is not lexicographically sorted, or raises any exception.
- **Initial Failure Expectation**: Pre-implementation, the test fails with `ModuleNotFoundError`/`ImportError` for `discovery` (exit code propagated by pytest as non-zero). The harness distinguishes `VALID_INITIAL_FAILURE` (missing module) from `INVALID_TEST` (test loader error).
- **Post-Implementation Success Expectation**: All assertions in the test pass; `pytest tests/M8/S2/test_discovery.py::test_discover_skills_returns_sorted_skill_basenames` exits 0.

### VI-2: `discover_skills` accepts both `Path` and `str` equivalently

- **Source Requirement ID**: `FR-DISCOVERY_MODULE_EXPORTS`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Synthetic fixture in place.
- **Input or fixture**: Call the function once with `Path(...)` and once with `str(...)` for the same root; assert `list_result == str_result`.
- **Expected Evidence**: Both invocations return equal lists; no exception from the `str` call.
- **Failure Condition**: `str` input raises `TypeError`, or results differ.
- **Initial Failure Expectation**: `ModuleNotFoundError` for `discovery`; `pytest` exits non-zero; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Both invocations succeed and return equal lists; exit 0.

### VI-3: `find_project_root` resolves to nearest marker-bearing ancestor

- **Source Requirement ID**: `FR-PROJECT_ROOT_DETECTION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.find_project_root`.
- **Preconditions**: A nested directory tree exists where a deep subdirectory is the test's CWD/starting path and the nearest ancestor contains a `skills/` directory; an alternative tree contains a `package.json`; another contains `pyproject.toml`.
- **Input or fixture**: Three starting directories: one whose nearest marker is `skills/`, one with `package.json`, one with `pyproject.toml`. Each call is invoked with `start=Path(...)`.
- **Expected Evidence**: Returned value is a `pathlib.Path`; `is_absolute() == True`; the resolved path is the nearest ancestor directory that contains the relevant marker (not the marker file/directory itself); the resolved path exists and is a directory.
- **Failure Condition**: Returned value is not a `Path`, is not absolute, does not exist, is not a directory, or does not point to the nearest marker-bearing ancestor.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All three marker cases resolve correctly; exit 0.

### VI-4: `find_project_root` default argument resolves to absolute `Path.cwd()`

- **Source Requirement ID**: `FR-PROJECT_ROOT_DETECTION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.find_project_root()` with no argument and with `start=None`.
- **Preconditions**: Test runs from a directory whose nearest marker-bearing ancestor is the workspace root, or no marker exists (function then returns `Path.cwd().resolve()`).
- **Input or fixture**: No positional argument; `start=None`.
- **Expected Evidence**: Returned value equals `Path.cwd().resolve()` (or the nearest marker ancestor if one is present above CWD); result is absolute; result is a `Path` instance.
- **Failure Condition**: Returned value is not absolute, is not a `Path`, or raises.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Both calls succeed and return the documented value; exit 0.

### VI-5: `find_project_root` with `start=""` and `start=None` defaults to CWD without raising

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.find_project_root`.
- **Preconditions**: None.
- **Input or fixture**: `find_project_root("")` and `find_project_root(None)`.
- **Expected Evidence**: Neither call raises; both return an absolute `Path` equal to `Path.cwd().resolve()` (or the nearest marker ancestor above CWD).
- **Failure Condition**: Either call raises any exception; return is not absolute; return is not a `Path`.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Both calls complete without exception and return the documented value; exit 0.

### VI-6: `discover_skills` returns `[]` when `<project_root>/skills/` is missing

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE`, `FR-SKILL_LISTING_FROM_FIXTURE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: A temporary directory exists that does NOT contain a `skills/` subdirectory.
- **Input or fixture**: `Path(tmp_path)`.
- **Expected Evidence**: Returned value is `[]`; no exception.
- **Failure Condition**: Function raises; return is not a list; return is non-empty.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Return is `[]`; exit 0.

### VI-7: `discover_skills` returns `[]` when `skills/` is empty

- **Source Requirement ID**: `FR-SKILL_LISTING_FROM_FIXTURE`, `FR-DISCOVERY_ERROR_TOLERANCE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Temporary `project_root/skills/` exists but is empty.
- **Input or fixture**: `Path(tmp_path)`.
- **Expected Evidence**: Returned value is `[]`; no exception.
- **Failure Condition**: Function raises; return is not a list; return is non-empty.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Return is `[]`; exit 0.

### VI-8: `discover_skills` silently skips unreadable subdirectories

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE`, `FR-SKILL_LISTING_FROM_FIXTURE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Test environment can simulate a non-readable subdirectory (e.g., `chmod 0` on POSIX). The test is marked `@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission model")`.
- **Input or fixture**: Temporary `project_root/skills/` with two skill subdirectories: one with `SKILL.md` and mode `0o000`; one with `SKILL.md` and normal permissions.
- **Expected Evidence**: Returned list contains the readable skill's basename only; the unreadable one is silently skipped; no exception bubbles.
- **Failure Condition**: Function raises (`PermissionError` or otherwise); the unreadable skill appears in the result; the readable skill is missing.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Return is `[readable_skill_name]`; exit 0.

### VI-9: `discover_skills` excludes hidden directories (names starting with `.`)

- **Source Requirement ID**: `FR-SKILL_LISTING_FROM_FIXTURE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Fixture `skills/` contains a hidden subdirectory (e.g., `.hidden`) that itself contains a `SKILL.md`, plus a normal valid skill.
- **Input or fixture**: Synthetic fixture path.
- **Expected Evidence**: Returned list contains the visible skill; `.hidden` is excluded.
- **Failure Condition**: `.hidden` appears in the result; the visible skill is missing.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Hidden directory excluded; exit 0.

### VI-10: `discover_skills` follows valid directory symlinks and skips broken ones

- **Source Requirement ID**: `FR-SKILL_LISTING_FROM_FIXTURE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Test environment supports symlinks (POSIX). Test is skipped on Windows.
- **Input or fixture**: `skills/` contains a symlink to a directory with `SKILL.md` (valid link) and a symlink to a non-existent target (broken link); a normal valid skill is also present.
- **Expected Evidence**: Returned list contains the real skill basename and the symlink's basename (because the resolved path is a directory with `SKILL.md`); the broken symlink is silently skipped; no exception.
- **Failure Condition**: Broken symlink causes a raise; valid symlink's basename is missing; broken symlink's name appears in the result.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Expected list returned; exit 0.

### VI-11: `discover_skills` is deterministic across repeated invocations

- **Source Requirement ID**: `FR-DETERMINISTIC_SORT_ORDER`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: Synthetic fixture in place.
- **Input or fixture**: Two consecutive calls with the same `Path` argument.
- **Expected Evidence**: `result_a == result_b`; both are `list[str]`; both are sorted; `is` identity is not required, equality is.
- **Failure Condition**: Results differ between calls; either call raises.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Equality holds; exit 0.

### VI-12: `SKILLS_DIR_NAME` constant is `"skills"` and is importable

- **Source Requirement ID**: `FR-SKILL_FIXTURE_PATH_RESOLUTION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.SKILLS_DIR_NAME`.
- **Preconditions**: `discovery` module importable.
- **Input or fixture**: `from discovery import SKILLS_DIR_NAME`.
- **Expected Evidence**: Import succeeds; value is the string `"skills"`; type is `str`.
- **Failure Condition**: `ImportError`; value is not `"skills"`; type is not `str`.
- **Initial Failure Expectation**: `ModuleNotFoundError` on `import discovery`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Constant equals `"skills"`; exit 0.

### VI-13: `DiscoveryError` is an `Exception` subclass

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE` (optional but specified custom error)
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.DiscoveryError`.
- **Preconditions**: `discovery` module importable.
- **Input or fixture**: `from discovery import DiscoveryError`; `issubclass(DiscoveryError, Exception)`.
- **Expected Evidence**: Import succeeds; `issubclass` returns `True`.
- **Failure Condition**: `ImportError`; class is not an `Exception` subclass.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Class exists and inherits from `Exception`; exit 0.

### VI-14: `discovery.py` declares type hints on public functions and constants

- **Source Requirement ID**: `NFR-DISCOVERY_TYPE_HINTS`
- **Verification Method**: `UNIT_TEST` (via `typing.get_type_hints` and `inspect`)
- **Target**: `discovery.discover_skills`, `discovery.find_project_root`, `discovery.SKILLS_DIR_NAME`.
- **Preconditions**: `discovery` module importable.
- **Input or fixture**: Call `typing.get_type_hints(discovery.discover_skills)`, same for `find_project_root`; for the constant, `inspect.get_annotations(discovery, eval_str=True)["SKILLS_DIR_NAME"]` resolves to `str`.
- **Expected Evidence**: `discover_skills` annotations include `project_root` and a `List[str]` return; `find_project_root` annotations include `start` (with `None` default) and a `Path` return; `SKILLS_DIR_NAME` annotation resolves to `str`.
- **Failure Condition**: Any public symbol lacks a type hint; `get_type_hints` raises `NameError`/`TypeError` due to a forward reference; annotation does not match the documented type.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: All three public symbols have correct annotations; exit 0.

### VI-15: `discovery.py` has no module-level mutable global state

- **Source Requirement ID**: `NFR-DISCOVERY_NO_GLOBAL_STATE`
- **Verification Method**: `UNIT_TEST` (AST inspection)
- **Target**: `discovery.py` source.
- **Preconditions**: `discovery.py` exists at the project root.
- **Input or fixture**: Parse `discovery.py` with `ast.parse`; collect module-level `Assign`/`AnnAssign`/`AugAssign` targets whose values are mutable (`list`, `dict`, `set`, or `ast.Call` returning these). Only `SKILLS_DIR_NAME = "skills"` (immutable `str`) and function/class definitions are permitted.
- **Expected Evidence**: The set of module-level mutable bindings is empty; `SKILLS_DIR_NAME` and function/class defs are the only module-level statements.
- **Failure Condition**: Any module-level mutable binding is detected; `from typing import` and other stdlib imports are allowed (treated as binding `sys.modules` references, not as mutable global state of the module).
- **Initial Failure Expectation**: `FileNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: No mutable globals; exit 0.

### VI-16: `discovery.py` and tests import only stdlib + `discovery` (no cross-module deps)

- **Source Requirement ID**: `NFR-DISCOVERY_MODULAR_INDEPENDENCE`
- **Verification Method**: `UNIT_TEST` (AST inspection)
- **Target**: `discovery.py` and `tests/M8/S2/test_discovery.py` source.
- **Preconditions**: Both files exist.
- **Input or fixture**: Parse both files with `ast`; collect every `Import` / `ImportFrom` module name. The forbidden set is `{"cli", "reporting", "main", "core", "core.validation", "healthcheck"}` and any local module that resolves to these names. Stdlib modules and `discovery` are allowed; `pytest` is allowed in the test file.
- **Expected Evidence**: No forbidden imports are present.
- **Failure Condition**: Any forbidden import is detected in either file.
- **Initial Failure Expectation**: `FileNotFoundError` for `discovery.py` and/or test file; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Only allowed imports; exit 0.

### VI-17: `find_project_root` with non-existent `start` returns absolute path without raising

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE`, `FR-PROJECT_ROOT_DETECTION`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.find_project_root`.
- **Preconditions**: None.
- **Expected Evidence**: Function returns the absolute `Path` of the supplied start directory (per FR: "If no marker is found, the function returns the absolute path of the start directory"). Returned value is absolute; function does not raise.
- **Failure Condition**: Function raises; return is not absolute; return differs from the absolute resolved start path.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Returned absolute path; exit 0.

### VI-18: `discover_skills` against a non-existent project root returns `[]`

- **Source Requirement ID**: `FR-DISCOVERY_ERROR_TOLERANCE`
- **Verification Method**: `UNIT_TEST`
- **Target**: `discovery.discover_skills`.
- **Preconditions**: None.
- **Input or fixture**: `Path("/nonexistent/path/unique-marker-abc")`.
- **Expected Evidence**: Returned value is `[]`; no exception.
- **Failure Condition**: Function raises; return is not a list; return is non-empty.
- **Initial Failure Expectation**: `ModuleNotFoundError`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Return is `[]`; exit 0.

### VI-19: Discovery outputs match pre-refactor `healthcheck.py` enumeration on a shared fixture

- **Source Requirement ID**: `NFR-DISCOVERY_BACKWARD_COMPATIBILITY`
- **Verification Method**: `INTEGRITY_TEST` (cross-module equivalence)
- **Target**: `discovery.discover_skills` vs. the legacy enumeration logic in `healthcheck.py`.
- **Preconditions**: `healthcheck.py` remains present (per Denylist, must NOT be modified, but is allowed to be imported read-only by the test). Synthetic fixture in place.
- **Input or fixture**: Call `discovery.discover_skills(fixture_root)`; call the legacy enumeration function (or replicate its skill-name extraction inline) on the same fixture root.
- **Expected Evidence**: Both produce the same `list[str]` (set-equal and order-equal) when the fixture is enumerated.
- **Failure Condition**: Set or order differs; legacy call raises (test should mark the case as `xfail` only if `healthcheck.py` does not expose the function — otherwise the assertion must hold).
- **Initial Failure Expectation**: `ModuleNotFoundError` for `discovery`; `VALID_INITIAL_FAILURE`.
- **Post-Implementation Success Expectation**: Both enumerations match; exit 0.

### VI-20: Diff-scope allowlist enforcement (mechanical pre-merge check)

- **Source Requirement ID**: Spec-level constraint (Strict File Scope)
- **Verification Method**: `SCRIPT_EXECUTION` (`git diff --name-only`)
- **Target**: Repository working tree after implementation.
- **Preconditions**: Test stage of the harness has produced implementation changes; no other agent edits are pending.
- **Input or fixture**: `git diff --name-only` against the merge base.
- **Expected Evidence**: Every file in the diff is a member of the M8S2 Allowlist:
  - `discovery.py`
  - `tests/M8/S2/test_discovery.py`
  - `tests/fixtures/discovery/**` (the synthetic fixture tree)
  No file from the Denylist (`healthcheck.py`, `core/validation.py`, `reporting.py`, `cli.py`, `main.py`, `tests/M8/S1/**`, `tests/M8/integration/**`, any unrelated `*.json`/`index.js`/`skills/<name>/SKILL.md`) appears in the diff.
- **Failure Condition**: Any file outside the Allowlist appears in the diff.
- **Initial Failure Expectation**: Pre-implementation, the diff is empty (or contains only stub scaffolding), and the gate trivially passes; the test runner still records the run.
- **Post-Implementation Success Expectation**: Allowlist-only diff; exit 0.

---

## Edge Cases

- `discover_skills` is called with a `str` containing trailing slashes; result equals the `Path` form.
- `discover_skills` is called with a relative `Path`; result is identical to the absolute form.
- `find_project_root` is called from a directory that IS a marker-bearing root (e.g., the directory itself has `package.json`); returns that directory, not its parent.
- `find_project_root` is called from a directory whose nearest marker is `skills/` and an ancestor also has `package.json`; returns the `skills/`-bearing directory (nearest wins).
- `discover_skills` is called on a `project_root` whose `skills/` contains both a file and a directory with the same basename; the file is ignored, only the directory is enumerated.
- `discover_skills` returns `[]` (not `None`) when nothing matches; the test asserts `isinstance(result, list) and len(result) == 0`.

---

## Failure Scenarios

- Missing `discovery.py` → all VI-1..VI-19 tests fail with `ModuleNotFoundError`; the test runner classifies this as `VALID_INITIAL_FAILURE` and unblocks the pre-implementation gate.
- Implementation present but `discover_skills` raises on missing `skills/` → VI-6, VI-7, VI-18 fail.
- Implementation present but `find_project_root` raises on `None`/empty start → VI-5 fails.
- Implementation present but returns non-`Path` from `find_project_root` → VI-3, VI-4, VI-5, VI-17 fail.
- Implementation present but `discover_skills` returns a `set`/`tuple` instead of a `list` → VI-1, VI-2, VI-6, VI-7, VI-11, VI-18 fail.
- Implementation present but does not sort → VI-1, VI-11 fail.
- Implementation present but does not skip hidden directories → VI-9 fails.
- Implementation present but does not skip broken symlinks → VI-10 fails.
- Implementation present but lacks type hints → VI-14 fails.
- Implementation present but introduces a module-level mutable binding → VI-15 fails.
- Implementation present but imports from `cli`/`reporting`/`main`/`core.validation`/`healthcheck` → VI-16 (or VI-19) fails.
- Implementation modifies `healthcheck.py`, `core/validation.py`, `reporting.py`, `cli.py`, or `main.py` → VI-20 fails the diff-scope check.

---

## Regression Checklist

- [ ] `discover_skills` returns the same set and order as the pre-refactor `healthcheck.py` enumeration on the synthetic fixture (VI-19).
- [ ] `SKILLS_DIR_NAME` value unchanged (`"skills"`).
- [ ] Type hints unchanged in shape (`Path | str`, `List[str]`, `Path`, `Optional[Path] = None`).
- [ ] No new module-level mutable global state introduced (VI-15).
- [ ] No forbidden cross-module imports introduced (VI-16).
- [ ] Denylist files unmodified (VI-20).

---

## Manual Validation

1. From the project root, run `python3 -c "from discovery import discover_skills, find_project_root, SKILLS_DIR_NAME; print(SKILLS_DIR_NAME)"` and confirm output is `skills`.
2. Run `python3 -c "import inspect, discovery; print(inspect.signature(discovery.discover_skills)); print(inspect.signature(discovery.find_project_root))"` and confirm signatures match the specification.
3. Run `python3 -c "from discovery import DiscoveryError; print(issubclass(DiscoveryError, Exception))"` and confirm `True`.
4. On the synthetic fixture, run `python3 -c "from pathlib import Path; from discovery import discover_skills; print(discover_skills(Path('tests/fixtures/discovery/synthetic_project')))"` and confirm a sorted list of skill basenames.

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

_This mechanical check must be executed by `evaluate-implementation` before tests are considered passed._

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the Allowlist defined in `SPEC-M8S2`. The Allowlist is:
  - `discovery.py`
  - `tests/M8/S2/test_discovery.py`
  - `tests/fixtures/discovery/**` (the synthetic fixture tree, including `synthetic_project/skills/`)
  If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

#### Pre-Implementation Initial-Failure Contract

- For every `UNIT_TEST`/`INTEGRITY_TEST` above, the test is expected to FAIL pre-implementation with `ModuleNotFoundError: No module named 'discovery'` (or the equivalent `ImportError`).
- The test runner MUST classify this as `VALID_INITIAL_FAILURE` and unblock the pre-implementation gate.
- The runner MUST NOT classify a `ModuleNotFoundError` whose source is a malformed test file as `INVALID_TEST`; the loader-level failure is the only `INVALID_TEST` signal.

#### Test Commands

- Existing tests: `pytest tests/M8/S1/ -q` (regression; must remain green)
- New tests: `pytest tests/M8/S2/test_discovery.py -v`
- Combined: `pytest tests/M8/ -q`

---

## Expected Outcomes

- All 20 verification items pass.
- `discovery.py` exists, is importable, and exports `discover_skills`, `find_project_root`, `SKILLS_DIR_NAME`, and (optionally) `DiscoveryError`.
- `discover_skills` returns a deterministic, sorted `List[str]` of skill basenames against the synthetic fixture; returns `[]` for missing/empty `skills/`; tolerates unreadable subdirectories and broken symlinks.
- `find_project_root` walks upward to find a marker (`skills/`, `package.json`, or `pyproject.toml`), defaults to `Path.cwd()` on `None`/empty start, and returns an absolute `pathlib.Path` in all cases.
- `SKILLS_DIR_NAME == "skills"`.
- Type hints and modular independence constraints are satisfied.
- The diff-scope allowlist is respected; no Denylist file is modified.
