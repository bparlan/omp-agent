# Verification M8S1V

| Property         | Value                                      |
| ---------------- | ------------------------------------------ |
| Document Type    | Verification                               |
| Identifier       | M8S1V                                      |
| Derived From     | M8, M8S1, M7, M7S1, M7S1V                  |
| template_version | 1.1.0                                      |

---

## Success Criteria

- [ ] **SC-1**: "Valid Evidence" concept codified in canonical AEF documentation (AGENTS.md or FRAMEWORK.md) — definition, six validity criteria, VALID_TEST / INVALID_TEST / UNCERTAIN classification (FR-1.1–1.3).
- [ ] **SC-2**: Core principle appears verbatim and grep-able in docs (FR-1.3, FR-7.1–7.2):
      `Never advance the lifecycle based solely on test exit codes. First establish that the test itself is valid and that its failure is attributable to the intended subject.`
- [ ] **SC-3**: `skills/evaluate-implementation/SKILL.md` contains mandatory validity gate BEFORE test interpretation (FR-2.1–2.4): verdicts (VALID/INVALID/UNCERTAIN), ordering constraint, invalidation report protocol.
- [ ] **SC-4**: `skills/evaluate-implementation/SKILL.md` contains INVALID_TEST stop-gate: pipeline halts on INVALID, produces invalidation report with why/what/repair (FR-4.1–4.4).
- [ ] **SC-5**: `skills/generate-tests/SKILL.md` requires self-validity assertions in all generated tests (FR-3.1–3.5) — mechanical check before test logic, exit code 2 on failure.
- [ ] **SC-6**: `skills/generate-tests/SKILL.md` requires validity metadata in test plans and executable file headers (FR-5.1–5.2).
- [ ] **SC-7**: `skills/review-implementation/SKILL.md` includes "Test Validity" section (FR-6.1) and "Test Valid?" column in compliance matrix (FR-6.3).
- [ ] **SC-8**: `skills/review-implementation/SKILL.md` explicitly distinguishes "test is wrong" from "implementation is wrong" (FR-6.2) and recommends test repair before re-evaluation on INVALID tests (FR-6.4).
- [ ] **SC-9**: `templates/evaluation_template.md` updated with validity gate / invalidation report fields.
- [ ] **SC-10**: `templates/review_template.md` updated with "Test Validity" section.
- [ ] **SC-11**: `templates/test_template.md` updated with "Validity Metadata" section.
- [ ] **SC-12**: Meta-test exists in `tests/M8/` that validates the validity gate — correctly classifies an invalid test (e.g., self-scanning test) as INVALID.
- [ ] **SC-13**: M7's deterministic output preserved (TESTS_RUN/PASSED/FAILED/EXIT_CODE) — M8 extends with VALID_TESTS/INVALID_TESTS, does not remove existing output (NFR-3).
- [ ] **SC-14**: Edge cases documented (AC-14): false positives, infrastructure failures, languages without module systems, external system tests.

---

## Followup Reuse

### Reusable Items from M7S1V

**Regression items:**
- FS-5 (Modified file outside Allowlist) — directly reusable with M8S1 Allowlist
- Diff-Scope Verification pattern — directly reusable with M8S1 Allowlist
- Legacy artifact preservation (M3/M4/M5/M6 unchanged) — still applies

**Automated test patterns:**
- `git diff --name-only` check against Allowlist — directly reusable
- `bash -n` / `python -m py_compile` syntax validation — still applies to generated tests
- Exit-code capture pattern — still applies

**Edge cases:**
- EC-6 (Pre-implementation pass) — relevant to M8's false positive handling
- EC-7 (All tests pass pre-implementation) — relevant to M8's validity criteria
- EC-5 (Production path collision) — still applies to generate-tests

**Failure scenarios:**
- FS-5 (Modified file outside Allowlist) — directly reusable
- FS-6 (Legacy artifact deletion) — still applies

### New Verification Required

- FR-1: Valid Evidence concept definition and six criteria — verify documentation presence and completeness
- FR-2: Validity gate ordering and implementation in evaluate-implementation — verify process structure and verdicts
- FR-3: Self-validity assertions — verify generate-tests instructions include assertion requirements
- FR-4: INVALID_TEST classification and stop-gate — verify pipeline halt and invalidation report
- FR-5: Validity metadata in test artifacts — verify test plan template and executable headers
- FR-6: Validity analysis in review — verify review template and process instructions
- FR-7: Framework documentation — verify literal principle presence and grep-ability
- M8-specific regression: M7's test-first guarantees still function after M8 changes
- M8-specific edge cases: validity criteria edge conditions (languages without modules, external services)

---

## Functional Validation

### FR-1: Define "Valid Evidence" as a Lifecycle Concept

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-1.1 | Manual: grep for `VALID_TEST`, `INVALID_TEST`, `VALIDITY CHECK` | AGENTS.md or FRAMEWORK.md | All three terms defined in documentation |
| FR-1.2 | Manual: grep for all six validity criteria (exercised subject, attributable, deterministic, clean tree, no self-scan, diagnostic) | AGENTS.md or FRAMEWORK.md | Each criterion present with description |
| FR-1.3 | Manual: grep for the verbatim principle string (SC-2) | AGENTS.md or FRAMEWORK.md | Exact literal match — no paraphrasing |
| FR-1.4 | Automated: grep for `#NEEDS-CLARIFICATION` or `NEEDS-CLARIFICATION` marker compatibility | AGENTS.md | M3's uncertainty marker not removed or altered |

### FR-2: Validity Gate in `evaluate-implementation`

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-2.1 | Manual: read process steps in SKILL.md | `skills/evaluate-implementation/SKILL.md` | Validity check appears BEFORE test interpretation step |
| FR-2.2 | Manual: grep for `VALID_TEST`, `INVALID_TEST`, `UNCERTAIN` | `skills/evaluate-implementation/SKILL.md` | All three verdicts documented with descriptions |
| FR-2.3 | Manual: grep for ordering diagram or prose expressing validity → pass/fail order | `skills/evaluate-implementation/SKILL.md` | Validity check must precede pass/fail — clear ordering constraint |
| FR-2.4 | Manual: grep for "attributable to the intended subject" | `skills/evaluate-implementation/SKILL.md` | The core validity question present in the skill process |

### FR-3: Self-Validity Assertions in Generated Tests

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-3.1 | Manual: grep for "self-validity" or "validity assertion" | `skills/generate-tests/SKILL.md` | Requirement for self-validity assertion documented |
| FR-3.2 | Manual: grep for example checks (file_exists, module import, function_exists, output_inspection) | `skills/generate-tests/SKILL.md` | At least two examples of simple mechanical checks |
| FR-3.3 | Manual: grep for `exit 2` or "exit code 2" | `skills/generate-tests/SKILL.md` | Exit code 2 specified for validity failure (distinct from pass=0, fail=1) |
| FR-3.4 | Manual: grep for `VALIDITY FAILURE` message text | `skills/generate-tests/SKILL.md` | Exact error message template documented |
| FR-3.5 | Manual: confirm self-validity assertion appears BEFORE test logic in process order | `skills/generate-tests/SKILL.md` | Assertion before test execution — "top of script" or similar |

### FR-4: INVALID_TEST Classification

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-4.1 | Manual: grep for `INVALID_TEST` | `skills/evaluate-implementation/SKILL.md` | Formal state distinct from PASS and FAIL |
| FR-4.2 | Manual: grep for "pipeline MUST STOP" or "do not advance" or halt/stop instruction | `skills/evaluate-implementation/SKILL.md` | Pipeline halt on INVALID_TEST documented |
| FR-4.3 | Manual: grep for "silent discard" or "automatic retry" → should NOT exist | `skills/evaluate-implementation/SKILL.md` | No instruction permitting silent discard or auto-retry |
| FR-4.4 | Manual: grep for invalidation report fields (why, what, repair) | `skills/evaluate-implementation/SKILL.md` | Report metadata documented: test file path, violated criterion, raw evidence, recommended repair |

### FR-5: Validity Metadata in Test Artifacts

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-5.1 | Manual: read `templates/test_template.md` | `templates/test_template.md` | "Validity Metadata" section present with: subject under test, acceptance criteria, expected failure conditions, environment prerequisites |
| FR-5.2 | Manual: grep for `# VALIDITY:` or `VALIDITY:` in skill instructions | `skills/generate-tests/SKILL.md` | Executable file validity metadata pattern documented |

### FR-6: Validity Analysis in `review-implementation`

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-6.1 | Manual: grep for "Test Validity" | `skills/review-implementation/SKILL.md` | "Test Validity" section heading present in process |
| FR-6.2 | Manual: grep for "test is wrong" and "implementation is wrong" | `skills/review-implementation/SKILL.md` | Both concepts distinguished |
| FR-6.3 | Manual: grep for "Test Valid?" column or matrix | `skills/review-implementation/SKILL.md` | Compliance matrix extension documented |
| FR-6.4 | Manual: grep for "test repair" or "re-evaluation" in context of INVALID | `skills/review-implementation/SKILL.md` | Recommendation for test repair before re-evaluation documented |

### FR-7: Framework Documentation

| Check ID | Method | Input | Expected |
|---|---|---|---|
| FR-7.1 | Automated: grep for the verbatim principle string | AGENTS.md or FRAMEWORK.md | Exact match — single-line literal |
| FR-7.2 | Automated: confirm the string is a literal text node (not in a code block or comment) | AGENTS.md or FRAMEWORK.md | Appears as readable prose, not hidden in code |
| FR-7.3 | Manual: grep for "Valid Evidence" section | AGENTS.md or FRAMEWORK.md | Section defines concept with criteria and classification |

### NFR-1: Determinism

| Check ID | Method | Input | Expected |
|---|---|---|---|
| NFR-1.1 | Manual: grep for "deterministic" in validity gate instructions | `skills/evaluate-implementation/SKILL.md` | Same inputs → same verdict constraint documented |

### NFR-3: M7 Compatibility

| Check ID | Method | Input | Expected |
|---|---|---|---|
| NFR-3.1 | Automated: grep for `TESTS_RUN`, `TESTS_PASSED`, `TESTS_FAILED`, `EXIT_CODE` | `skills/evaluate-implementation/SKILL.md` | All four M7 output variables still present |
| NFR-3.2 | Automated: grep for `VALID_TESTS`, `INVALID_TESTS` | `skills/evaluate-implementation/SKILL.md` | M8 extension variables present |
| NFR-3.3 | Automated: read M7 Test B (initial failure) — verify it still functions | `tests/M7/test_b_initial_failure.sh` | File unchanged, test logic intact |

### NFR-4: Human Override

| Check ID | Method | Input | Expected |
|---|---|---|---|
| NFR-4.1 | Manual: grep for "override" or "human review" in validity gate context | `skills/evaluate-implementation/SKILL.md` | Human override path documented |

---

## Edge Cases

### EC-1: Self-validity assertion on a module that doesn't exist
- **Scenario**: Test targets a module/function that genuinely doesn't exist (valid pre-implementation state)
- **Expected**: Self-validity assertion may fail if it requires the module to be importable. The assertion must distinguish "module genuinely not implemented" from "module path is wrong." If the test knows the module path (from spec), the assertion is: "does the file at this path exist?" not "can I import it?"
- **Verification**: Manual review of self-validity assertion examples in skill docs

### EC-2: Language without module system (e.g., plain Bash without functions)
- **Scenario**: Generated test is a plain `.sh` script testing a plain `.sh` function — no module system exists
- **Expected**: Validity assertion uses file existence + function name check (`type function_name &>/dev/null`), not module import
- **Verification**: Manual review of generate-tests skill for language-appropriate assertion examples

### EC-3: Test that cannot self-validate (e.g., integration test hitting a network endpoint)
- **Scenario**: Test exercises an external system — subject is remote, not local
- **Expected**: Validity assertion checks that the endpoint is reachable (`curl --connect-timeout 5`), not that local code imported
- **Verification**: Manual review of edge case documentation

### EC-4: All tests classified INVALID — pipeline deadlock
- **Scenario**: Every test in the suite fails the validity check
- **Expected**: Pipeline stops. Invalidation report produced for each test. No automatic retry. Human must repair tests or certify them as valid.
- **Verification**: Manual — simulate scenario in meta-test

### EC-5: Mixed verdicts (some VALID, some INVALID, some UNCERTAIN)
- **Scenario**: Test suite contains a mix of valid, invalid, and uncertain tests
- **Expected**: VALID tests proceed to pass/fail. INVALID tests halt pipeline with report. UNCERTAIN tests flagged for human review. No partial advancement.
- **Verification**: Manual — simulate scenario in meta-test

### EC-6: Pre-implementation test passes (false positive — M7 EC-6 intersection)
- **Scenario**: Test passes before implementation
- **Expected**: Validity check determines whether the pass is attributable to the subject. If the test didn't exercise the subject (wrong path, self-scan), it's INVALID. If the test exercised the correct subject and passed, it's VALID(true pass) — WARNING must be produced (M7 requirement).
- **Verification**: Manual — test with already-implemented feature

### EC-7: Dirty working tree with uncommitted changes
- **Scenario**: `git status --porcelain` shows modified files before test execution
- **Expected**: Validity criterion #4 fails — working tree is not clean. Test classified INVALID. Invalidation report recommends `git stash` or commit.
- **Verification**: Automated meta-test — run validity check with dirty tree

### EC-8: Test scans its own source file
- **Scenario**: Test script reads its own contents as part of validation (self-scanning)
- **Expected**: Validity criterion #5 fails — test does not scan itself. Classified INVALID.
- **Verification**: Automated meta-test — create self-scanning test, verify INVALID classification

### EC-9: Exit code 2 already used by test framework
- **Scenario**: The test framework or runtime already uses exit code 2 for its own purposes
- **Expected**: Conflict resolution — either use a different exit code, or document the conflict with guidance
- **Verification**: grep for exit code 2 usage in project test scripts

---

## Failure Scenarios

### FS-1: Validity gate incorrectly classifies VALID test as INVALID (false negative)
- **Scenario**: A test correctly exercises its subject but is classified INVALID due to overly strict validity criteria
- **Impact**: HIGH — pipeline stalls on a good test
- **Mitigation**: Validity criteria must be conservative. Human override path exists.
- **Verification**: Meta-test with known-valid test; verify it passes validity gate

### FS-2: Validity gate incorrectly classifies INVALID test as VALID (false positive)
- **Scenario**: A test that doesn't exercise its subject is classified VALID, and its meaningless pass/fail is treated as evidence
- **Impact**: CRITICAL — defeats the purpose of the validity check entirely
- **Mitigation**: Self-validity assertions in tests as secondary signal. Review analysis as tertiary check.
- **Verification**: Meta-test with known-invalid test (self-scanning, wrong path); verify it fails validity gate

### FS-3: Self-validity assertion passes when test didn't exercise subject
- **Scenario**: Assertion checks file exists (which it does), but test logic never actually calls the subject
- **Impact**: MEDIUM — assertion is true but insufficient
- **Mitigation**: Assertions must check that the subject was INVOKED, not just that it exists. Output inspection checks.
- **Verification**: Manual review of assertion design guidelines in generate-tests skill

### FS-4: Self-validity assertion itself has a bug (false failure)
- **Scenario**: The assertion logic is broken — it fails when the subject is actually available
- **Impact**: MEDIUM — test cannot run
- **Mitigation**: Assertions must be simple, mechanical checks. A broken assertion is itself detectable (the test exits 2, which is different from test-fail 1).
- **Verification**: Meta-test with known-good subject and deliberately broken assertion

### FS-5: Modified file outside M8S1 Allowlist
- **Scenario**: Implementation changes a file outside the Allowlist (e.g., `skills/implement-specification/SKILL.md`)
- **Impact**: CRITICAL — specification violation
- **Verification**: Automated — `git diff --name-only` compared against M8S1 Allowlist

### FS-6: Legacy artifact (M7 tests) broken by M8 changes
- **Scenario**: M8's changes to `evaluate-implementation` or `generate-tests` break the M7 meta-tests (Tests A–G)
- **Impact**: HIGH — M7 regression
- **Verification**: Automated — run `tests/M7/test_b_initial_failure.sh` and `tests/M7/test_g_no_implementation_on_failure.sh`

### FS-7: M7 output format not preserved
- **Scenario**: M8's validity gate changes the machine-readable output format, removing TESTS_RUN/PASSED/FAILED/EXIT_CODE
- **Impact**: HIGH — breaks downstream consumers
- **Verification**: Automated — grep for all four variables in evaluate-implementation SKILL.md

### FS-8: Framework documentation modified without the core principle
- **Scenario**: AGENTS.md is edited but the core principle string is not added
- **Impact**: MEDIUM — SC-1/SC-2 fail
- **Verification**: Automated — grep for the verbatim principle in AGENTS.md or FRAMEWORK.md

---

## Regression Checklist

### RC-1: M7 test-first determinism preserved
- [ ] `skills/generate-tests/SKILL.md` still contains guardrail classification (5 types)
- [ ] `skills/generate-tests/SKILL.md` still contains Test Contract requirements
- [ ] `skills/generate-tests/SKILL.md` still contains test-first enforcement
- [ ] `skills/generate-tests/SKILL.md` still contains machine-readable output format (TESTS_RUN/PASSED/FAILED/EXIT_CODE)
- [ ] `tests/M7/test_b_initial_failure.sh` and `tests/M7/test_g_no_implementation_on_failure.sh` still function

### RC-2: Skills outside M8S1 Allowlist unchanged
- [ ] `skills/generate-spec/SKILL.md` unchanged
- [ ] `skills/generate-verification/SKILL.md` unchanged
- [ ] `skills/implement-specification/SKILL.md` unchanged
- [ ] `skills/manage-development/SKILL.md` unchanged
- [ ] `skills/session-audit/SKILL.md` unchanged
- [ ] `skills/bootstrap-project/SKILL.md` unchanged

### RC-3: Templates outside M8S1 Allowlist unchanged
- [ ] `templates/completion_template.md` unchanged
- [ ] `templates/specification_template.md` unchanged
- [ ] `templates/verification_template.md` unchanged
- [ ] `templates/milestone_template.md` unchanged

### RC-4: Legacy milestone artifacts preserved
- [ ] `milestones/M7/M7S1.md` unchanged
- [ ] `milestones/M7/M7S1V.md` unchanged
- [ ] `milestones/M7/M7S1T1.md` unchanged
- [ ] `tests/M7/` (all files) unchanged
- [ ] `milestones/M3/` artifact tree intact
- [ ] `milestones/M4/` artifact tree intact
- [ ] `milestones/M5/` artifact tree intact

### RC-5: M8S1 Allowlist respected
- [ ] Only files on the Allowlist were modified
- [ ] No files on the Denylist were touched
- [ ] `docs/MILESTONES.md` not modified (already updated during milestone creation)

### RC-6: `evaluate-implementation` base behavior preserved
- [ ] Still reads test artifacts from `tests/M{X}/`
- [ ] Still generates evaluation report at `M{X}S{Y}E.md`
- [ ] Still classifies failures (valid/invalid/environment/specification mismatch)
- [ ] Still auto-fixes minor bugs for valid failures only

### RC-7: `generate-tests` base behavior preserved
- [ ] Still reads verification protocol `M{X}S{Y}V.md`
- [ ] Still produces test design document + executable files
- [ ] Still supports `.sh` and `.py` test types
- [ ] Still runs syntax validation (`bash -n` / `py_compile`)
- [ ] Guardrail breach protocol unchanged

### RC-8: `review-implementation` base behavior preserved
- [ ] Still reads spec, verification, completion, and impl files
- [ ] Still creates compliance matrix
- [ ] Still performs live-state verification
- [ ] Still identifies technical debt
- [ ] Still produces review report at `M{X}S{Y}R.md`

---

## Manual Validation

### MV-1: Concept documentation quality review
**Step**: Read AGENTS.md or FRAMEWORK.md and verify:
- [ ] "Valid Evidence" section exists with clear heading
- [ ] All six validity criteria are individually described with rationale
- [ ] VALID_TEST / INVALID_TEST / UNCERTAIN are defined
- [ ] Core principle appears as a verbatim, grep-able string
- [ ] The principle is in readable prose, not a code block or comment

### MV-2: evaluate-implementation skill structure review
**Step**: Read `skills/evaluate-implementation/SKILL.md` and verify:
- [ ] Validity check is clearly a SEPARATE step from test interpretation
- [ ] Validity check appears BEFORE pass/fail analysis
- [ ] Three verdicts (VALID/INVALID/UNCERTAIN) are documented with what each means
- [ ] Invalidation report structure is defined with fields
- [ ] Pipeline halt instruction is unambiguous
- [ ] Human override path is documented

### MV-3: generate-tests skill structure review
**Step**: Read `skills/generate-tests/SKILL.md` and verify:
- [ ] Self-validity assertion requirement appears as a separate process step
- [ ] At least two concrete check examples are provided (e.g., file exists, module imports)
- [ ] Exit code 2 is specified for validity failure
- [ ] VALIDITY FAILURE message format is specified
- [ ] Validity metadata format for test plans and executable headers is specified
- [ ] Assertion before test logic — ordering constraint

### MV-4: review-implementation skill structure review
**Step**: Read `skills/review-implementation/SKILL.md` and verify:
- [ ] "Test Validity" section appears in the process or output template reference
- [ ] "Test Valid?" column or equivalent appears in compliance matrix
- [ ] Distinction between "test is wrong" and "implementation is wrong" is present
- [ ] INVALID test → recommend test repair before re-evaluation

### MV-5: Template updates review
**Step**: Read each template and verify:
- [ ] `templates/evaluation_template.md` has a validity/invalidation report section
- [ ] `templates/review_template.md` has a "Test Validity" section
- [ ] `templates/test_template.md` has a "Validity Metadata" section

### MV-6: Edge case documentation review
**Step**: Verify edge case guidance exists for:
- [ ] Tests that pass before implementation (false positives)
- [ ] Tests that fail for infrastructure reasons
- [ ] Languages without module systems
- [ ] Tests involving external systems (network, database, file system)

---

## Automated Validation

### Diff-Scope Verification (Pre-Merge Check)

*This mechanical check must be executed by `evaluate-implementation` before tests are considered passed.*

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the Allowlist defined in Specification M8S1. Permitted changes:
  - `skills/evaluate-implementation/SKILL.md`
  - `skills/generate-tests/SKILL.md`
  - `skills/review-implementation/SKILL.md`
  - `AGENTS.md` (or `docs/FRAMEWORK.md`)
  - `templates/evaluation_template.md`
  - `templates/review_template.md`
  - `templates/test_template.md`
  - `tests/M8/` (all files within)
  - `milestones/M8/` (all files within, excluding files from other phases)
- If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

### Existing Tests (from M7)

| Test ID | Command | Expected | Relevance |
|---------|---------|----------|-----------|
| Test B | `bash tests/M7/test_b_initial_failure.sh` | Exit 0 | Verifies M7's test-first guarantee not broken by M8 |
| Test C | `bash tests/M7/test_c_no_production_files.sh` | Exit 0 | Verifies no production files modified during test generation (should still pass with M8 additions) |
| Test G | `bash tests/M7/test_g_no_implementation_on_failure.sh` | Exit 0 | Verifies test failure does not trigger implementation (M8 adds validity check, not implementation trigger) |

### New Tests (created by this milestone)

| Test ID | File | Command | Expected | Purpose |
|---------|------|---------|----------|---------|
| Test H | `tests/M8/test_h_validity_gate_self_scan.sh` | `bash tests/M8/test_h_validity_gate_self_scan.sh` | Exit 0 | Verify self-scanning test is classified INVALID by validity gate |
| Test I | `tests/M8/test_i_validity_gate_wrong_path.sh` | `bash tests/M8/test_i_validity_gate_wrong_path.sh` | Exit 0 | Verify test with wrong subject path is classified INVALID |
| Test J | `tests/M8/test_j_validity_gate_valid_test.sh` | `bash tests/M8/test_j_validity_gate_valid_test.sh` | Exit 0 | Verify valid test passes validity gate (negative test — no false INVALID) |
| Test K | `tests/M8/test_k_validity_gate_dirty_tree.sh` | `bash tests/M8/test_k_validity_gate_dirty_tree.sh` | Exit 0 | Verify dirty working tree causes INVALID classification |
| Test L | `tests/M8/test_l_self_validity_exit_code_2.sh` | `bash tests/M8/test_l_self_validity_exit_code_2.sh` | Exit 0 | Verify self-validity assertion failure exits with code 2 |

### Validation Commands

```bash
# 1. Verify docs contain the core principle verbatim
grep -r "Never advance the lifecycle based solely on test exit codes" AGENTS.md docs/FRAMEWORK.md 2>/dev/null || echo "FAIL: principle not found"

# 2. Verify evaluate-implementation has validity gate
grep -q "VALIDITY CHECK\|validity check\|validity gate\|VALID_TEST\|INVALID_TEST" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"

# 3. Verify validity check BEFORE test interpretation
#    (grep for ordering — look for "before" in relevant context)
grep -q "before" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "WARN: check ordering manually"

# 4. Verify generate-tests has self-validity assertion requirement
grep -q "self-validity\|validity assertion" skills/generate-tests/SKILL.md && echo "PASS" || echo "FAIL"

# 5. Verify exit code 2 for validity failure
grep -q "exit 2\|exit code 2\|EXIT_CODE=2" skills/generate-tests/SKILL.md && echo "PASS" || echo "FAIL"

# 6. Verify review-implementation has validity analysis
grep -q "Test Validity\|test.*valid" skills/review-implementation/SKILL.md && echo "PASS" || echo "FAIL"

# 7. Verify templates updated
grep -q "Validity\|INVALID\|validity" templates/evaluation_template.md && echo "PASS" || echo "FAIL"
grep -q "Test Validity\|test.*valid" templates/review_template.md && echo "PASS" || echo "FAIL"
grep -q "Validity Metadata" templates/test_template.md && echo "PASS" || echo "FAIL"

# 8. Verify M7 compatibility — output format preserved
grep -q "TESTS_RUN" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"
grep -q "TESTS_PASSED" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"
grep -q "TESTS_FAILED" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"
grep -q "EXIT_CODE" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"

# 9. Verify M8 extension output
grep -q "VALID_TESTS\|INVALID_TESTS" skills/evaluate-implementation/SKILL.md && echo "PASS" || echo "FAIL"

# 10. Verify M7 tests unchanged
bash tests/M7/test_b_initial_failure.sh || echo "FAIL: M7 test B regression"
bash tests/M7/test_c_no_production_files.sh || echo "FAIL: M7 test C regression"

# 11. Verify meta-tests exist
ls tests/M8/test_h_* tests/M8/test_i_* tests/M8/test_j_* tests/M8/test_k_* tests/M8/test_l_* 2>/dev/null && echo "PASS" || echo "FAIL: meta-tests missing"

# 12. Diff-scope check
git diff --name-only | while read f; do
  case "$f" in
    skills/evaluate-implementation/SKILL.md|skills/generate-tests/SKILL.md|skills/review-implementation/SKILL.md) ;;
    AGENTS.md|docs/FRAMEWORK.md) ;;
    templates/evaluation_template.md|templates/review_template.md|templates/test_template.md) ;;
    tests/M8/*|milestones/M8/*) ;;
    *) echo "FAIL: out-of-scope file modified: $f" ;;
  esac
done
```

---

## Expected Outcomes

1. **Concept defined**: "Valid Evidence" is a recognized lifecycle concept with formal definition, six validity criteria, and three classifications (VALID/INVALID/UNCERTAIN). The core principle is grep-able verbatim in framework docs.

2. **Validity gate operational**: `evaluate-implementation` runs a mandatory validity check before interpreting test results. Tests are classified as VALID, INVALID, or UNCERTAIN. INVALID tests halt the pipeline with an invalidation report.

3. **Self-validity guaranteed**: Every test generated by `generate-tests` includes a simple mechanical assertion that it exercised its subject. Failure of this assertion exits with code 2 (distinct from test failure = 1).

4. **Review distinguishes validity from correctness**: `review-implementation` includes a "Test Validity" section and "Test Valid?" column in its compliance matrix, explicitly distinguishing "test is wrong" from "implementation is wrong."

5. **Templates equipped**: All three affected templates (evaluation, review, test) carry validity metadata and analysis sections.

6. **M7 preserved**: M7's deterministic output format (TESTS_RUN/PASSED/FAILED/EXIT_CODE) and test-first guarantees remain functional. M8 extends with VALID_TESTS/INVALID_TESTS but does not remove or alter M7's output.

7. **Meta-tests pass**: Five meta-tests (Tests H–L) validate the validity gate end-to-end, testing self-scan, wrong path, valid test, dirty tree, and exit code 2 scenarios.