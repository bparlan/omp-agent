# Investigation Report — Contamination Root Cause Analysis

| Property         | Value                                      |
| ---------------- | ------------------------------------------ |
| Document Type    | Investigation                              |
| Identifier       | M7INVESTIGATION                            |
| Derived From     | M7S1                                       |
| Status           | Complete                                   |
| template_version | 1.0.0                                      |

---

## FR-1.1: Root Cause — Why does `generate-tests` see implementation-like content?

The root cause is a missing mechanical boundary between test generation and production implementation in the `generate-tests` skill instruction set. The skill (v1.1.0) defines an open-ended generation process with no file classification step, no guardrails against production paths, and no test-first enforcement.

**Primary causes:**

1. **No file classification step** — The process says "Generate Executable Tests" but never requires the agent to classify each proposed write target before writing. Without a classification step, the agent has no mechanical signal to distinguish "test artifact" from "production implementation."

2. **No boundary guardrails** — The "Out of Scope" section says "Never: Modify the core implementation code" but this is a soft suggestion in a bullet list. It is not a mechanically enforced step in the process flow. The agent can read the process steps, generate tests, and if the model drifts toward implementation, nothing in the process stops it.

3. **Open-ended examples** — Step 2 says "test scripts (e.g., Python `pytest`, bash dry-runs, or UI scripts)". The use of "e.g." is open-ended, and listing Python first signals Python as the default test language even when the verification specifies shell tests.

4. **No requirement to run tests** — The current process says "Stop — Do not execute the tests." This means `generate-tests` never validates its own output. If it generates invalid or implementation-like code, there's no self-check.

5. **No machine-readable output contract** — Without a required output format (TESTS_RUN/PASSED/FAILED/EXIT_CODE), downstream agents cannot mechanically verify what was produced.

---

## FR-1.2: Contaminated Files and Templates

### Files containing contamination

| File | Contamination Type | Severity |
|------|-------------------|----------|
| `skills/generate-tests/SKILL.md` (v1.1.0) | Missing guardrails; open-ended process; no classification step; no test-first enforcement; no machine-readable output | HIGH |
| `templates/test_template.md` (v1.0.0) | Contains Python class definitions inside `.sh` example code blocks (labeled "Invalid" but still present as runnable code the model may copy) | MEDIUM |

### Files confirmed clean

| File | Status |
|------|--------|
| `tests/M5/*.sh` (8 scripts) | Clean — valid bash syntax, no Python cross-contamination |
| `tests/M5/*.py` (6 scripts) | Clean — valid Python, properly separated from bash tests |
| `tests/M6/*.py` (9 scripts) | Clean — valid Python with test-first docstrings |
| `tests/M6/run_all_tests.sh` | Clean — valid bash runner script |
| `milestones/M5/M5S1T1.md` | Documentation only, no implementation-like code |
| `milestones/M6/M6S1V.md` | Verification protocol only |
| `skills/generate-spec/SKILL.md` | Out of scope — not consumed by `generate-tests` |
| `skills/generate-verification/SKILL.md` | Out of scope — not consumed by `generate-tests` |

### test_template.md contamination details

The template's "Invalid" example block shows:
```bash
#!/bin/bash
# WRONG: Python class in bash file
class Mock:
    def __init__(self):
        pass
```

While this is labeled as an invalid pattern, the Python code is present verbatim in a code block inside a skill template. A model invoking this template may treat the `class Mock: …` block as legitimate syntax suggestions rather than anti-patterns, particularly when the template is referenced during the "Generate Executable Tests" step without explicit language-filtering instructions.

---

## FR-1.3: Instructions That Cause Boundary Crossing

### Critical passage in `skills/generate-tests/SKILL.md`:

```
2. **Generate Executable Tests** — Write programmatic use-case files, test scripts
   (e.g., Python `pytest`, bash dry-runs, or UI scripts), and localized testing
   utilities that directly validate the success criteria.
```

**Why this causes boundary crossing:**
- The phrase "localized testing utilities" is undefined — an agent may interpret this as creating helper modules, mock classes, or test infrastructure that resembles production code.
- The examples (`pytest`, `bash`, `UI scripts`) suggest multiple language options without a decision rule for which to use.
- No instruction says "only write test files, never write implementation."
- No instruction says "classify the file before writing."

### Missing instruction (the gap):

There is no step between "Read Verification Protocol" and "Generate Executable Tests" for:
- File classification
- Path validation
- Production boundary check

Without this step, the model has only a soft "Never: Modify the core implementation code" in a distant "Out of Scope" section, which is not part of the active process flow.

### test_template.md contribution:

The template provides language-specific examples that help maintain language consistency. However, the "Invalid" example includes Python code in a bash block. Even labeled as invalid, the presence of Python code patterns in a template referenced during test generation may prime the model to generate similar patterns.

---

## FR-1.4: Executable Test Gap — Why Tests Are Not Reliably Created

The current SKILL.md requires saving test scripts and verifying syntax:

```
- Save the actual Python/JS/bash test scripts to `tests/M{X}/` directory.
- Verify Syntax — Run syntax validation on all test scripts
```

However, it is missing:

1. **Execution requirement** — The skill explicitly says "Do not execute the tests." This means:
   - Exit codes are never captured
   - Failed syntax does not halt the process
   - There's no way to know if the generated tests actually work
   - There's no pre-implementation baseline

2. **No "must fail" requirement** — Tests can be generated that accidentally pass against the current codebase, hiding the fact that the feature under test already exists or the test is too weak.

3. **No language selection rule** — When the verification protocol doesn't specify `.sh` vs `.py`, the skill has no default behavior documented. The open-ended `(e.g., Python pytest, bash dry-runs, or UI scripts)` encourages Python-first generation even for shell-test scenarios.

4. **No file count requirement** — The skill doesn't specify a minimum number of test files or require one test per verification item.

---

## FR-1.5: Pseudo-Code in Test Artifacts

Pseudo-code appears in generated test artifacts because:

1. **The test_template.md contains code blocks with Python** — Even as "invalid" examples, the template literal `class Mock: def __init__(self): pass` appears verbatim. A model that pattern-matches template content may regenerate similar patterns.

2. **The SKILL.md provides no pseudo-code prohibition** — There is no step saying "test files must contain only valid syntax for their declared language." The syntax validation step (`bash -n`/`py_compile`) catches actual syntax errors but does not prevent a `.sh` file from containing valid-in-Python-but-nonsense-in-bash code like `class Mock:`.

3. **No language consistency check** — The skill has no step verifying that `.sh` files contain only bash constructs and `.py` files contain only Python constructs. The test_template.md now has "Language Extension Consistency" rules, but the SKILL.md doesn't enforce them.

---

## FR-1.6: Artifact Status — M6/M6S1/M6S1V

| Artifact | Status | Checksum |
|----------|--------|----------|
| `milestones/M6/M6.md` | PRESERVED — unchanged | `a7d7ca0d8ad09938b73b415c7c7d49147c66a7b7ce419c9b85b33287031fdc97` |
| `milestones/M6/M6S1.md` | PRESERVED — unchanged | `d641f29ea5ee7b7cb2aa1e5b583d0572e1e259e6ac7aef29df2b260c233b5881` |
| `milestones/M6/M6S1V.md` | PRESERVED — unchanged | `d1f0ba06548891e211b11145bead95054329f34e4b815a83287c20a9947dbbcd` |
| `milestones/M5/M5.md` | PRESERVED — unchanged | `87968e1813f2faddb60edac1788843337dc2a27263e063442cafe21dd8abc18d` |
| `milestones/M5/M5S1.md` | PRESERVED — unchanged | `c65520c8323749ed2e6faeadebbd4b13b8d8db9ca8ce0bb4ef1070db004ae1fc` |

No M6/M6S1/M6S1V artifacts were deleted, renamed, or modified during any phase of M7.

All M4 artifacts are also present and unmodified.

---

## FR-1.7: Smallest Safe Fix

The smallest safe fix is a three-part change to `skills/generate-tests/SKILL.md` only:

### Part A — Add file classification step (new step 2)

Before any file is written, the agent MUST classify it as one of:
- `TEST_ARTIFACT` — A test design document or test plan (`.md` in `milestones/M{X}/`)
- `TEST_FIXTURE` — A test data file or configuration for test execution
- `TEST_HELPER` — A utility script required to run tests, clearly separated from production
- `PRODUCTION_IMPLEMENTATION` — **FORBIDDEN**: halt with error
- `DOCUMENTATION` — A documentation or informational artifact

If a file is classified as `PRODUCTION_IMPLEMENTATION`, the agent MUST stop with the error: `"STOP: generate-tests attempted to write production implementation. This is prohibited. Required action: defer implementation to implement-specification."`

### Part B — Replace "Stop — Do not execute" with test-first enforcement (new step 5)

Replace the current "Stop — Do not execute the tests" with:
- Run the generated tests
- Capture exit codes
- If all tests pass pre-implementation: emit `WARNING: PRE-IMPLEMENTATION TEST PASSES`
- Output machine-readable summary: `TESTS_RUN=N`, `TESTS_PASSED=N`, `TESTS_FAILED=N`, `EXIT_CODE=N`
- STOP — Do not proceed to implementation

### Part C — Add executable test requirements and output contract

Document in the process:
- Language-specific syntax rules
- File extension matching syntax language
- Minimum output: test design document + executable files + machine-readable summary

### test_template.md changes (optional, lower priority)

The template currently has good language consistency rules. The Python-in-bash "Invalid" example is labeled clearly. Removing the Python code block entirely and replacing it with a text-only description would eliminate the residual risk of pattern-matching contamination.

---

## Additional Findings

### M5/M6 Test Contamination Check

All M5 and M6 executable test files were scanned for:
- Python class definitions in `.sh` files → **None found**
- Python method definitions with `self` in `.sh` files → **None found**
- Python `if __name__` guards in `.sh` files → **None found**
- Top-level Python imports in `.sh` files → **None found**
- Implementation snippets (class defs, production write patterns) in test files → **None found**

**Conclusion**: The M5 and M6 test suites are clean. The contamination concern is primarily about what `generate-tests` *would produce* under the current skill instructions, not about what existing artifacts contain.

### Git State During Investigation

The working tree had pre-existing unstaged changes:
- `README.md`, `docs/MILESTONES.md`, `skills/generate-tests/SKILL.md`, `skills/manage-development/*`, `templates/test_template.md` — All unstaged modifications from prior sessions

These are NOT changes caused by this investigation. All M7-created files are untracked (`tests/M7/`, `milestones/M7/`).

---

## Summary

| Question | Answer |
|----------|--------|
| Root cause | Missing mechanical boundary — no file classification step, no guardrails, no test-first enforcement |
| Primary contaminated file | `skills/generate-tests/SKILL.md` (v1.1.0) — process has no classification or guardrails |
| Secondary file | `templates/test_template.md` — contains Python-in-bash code block that may be pattern-matched |
| Boundary-crossing instruction | Step 2 "Generate Executable Tests" — open-ended, no classification, no path validation |
| Executable test gap | Step "Stop — Do not execute" prevents self-validation of generated tests |
| Pseudo-code cause | No language consistency enforcement in SKILL.md; Python code present in template |
| M6/M6S1/M6S1V status | All preserved — checksums match pre-M7 state |
| Smallest safe fix | Add file classification step (Part A), test-first enforcement (Part B), output contract (Part C) |