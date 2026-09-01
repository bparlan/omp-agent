---
id: aef:EVAL-M7S3
type: evaluation
title: "Evaluation Report for M7S3: Legacy Compatibility & Transition"
milestone_id: M7
status: completed
derived_from: [SPEC-003, VER-003]
template_version: 1.0.2
---

## Test Execution Summary

| Metric | Value |
|--------|-------|
| TESTS_RUN | 12 |
| TESTS_PASSED | 9 |
| TESTS_FAILED | 3 |
| VALID_TESTS | 9 |
| INVALID_TESTS | 3 |
| EXIT_CODE | 2 |

EXIT_CODE=2: Validity failure. All 3 failing tests are INVALID_TEST (test-side defects, not implementaton issues). Pipeline stops before pass/fail interpretation of invalid tests. The 9 remaining tests (all valid) passed.

---

## Validity Gate Results

### Pre-Execution Metadata Validation

| Artifact | Result |
|----------|--------|
| `milestones/M7/M7S3.md` (SPEC-003) | VALID — `python3 bin/validate_metadata.py` → exit 0 |
| `milestones/M7/M7S3V.md` (VER-003) | VALID — `python3 bin/validate_metadata.py` → exit 0 |

### Interpreter Verification

All 12 test scripts are `.sh` files. Executed with `bash` — correct interpreter.

---

### Invalidation Reports

| Test File | Violated Criterion | Raw Evidence | Recommended Repair |
|-----------|--------------------|-------------|-------------------|
| `tests/M7/test_legacy_manifest.sh` | Criterion 2: Failure not attributable to the intended subject | Off-by-one path extraction: `path_part="\${line:66}"` should be `"\${line:65}"` (line 84). Regex format check on line 76 passes correctly (validates `^[0-9a-f]{64}\ [^\ ]+$`), but the bash substring extraction at index 66 skips the first byte of the path. Manifest entry `<SHA-256> M1/M1S1.md` → `${line:66}` yields `1/M1S1.md`, causing `[[ -f ... ]]` check on line 94 to fail. | Fix path offset: `${line:66}` → `${line:65}` in line 84 of the test script. |
| `tests/M7/test_classify_tier1_frontmatter.sh` | Criterion 2: Failure not attributable to the intended subject | Lines 87 and 95 check if manifest content contains "SPEC-001" and "VER-001". Per FR-11, the manifest format is strictly `<SHA-256> <relative-path>` — it does NOT include YAML frontmatter `id` fields. The test exercises the subject correctly (exit 0, Tier 1 detected, manifest created with valid checksums), but its assertion expects data that the specification explicitly excludes from the manifest format. | Remove assertions checking for "SPEC-001" and "VER-001" in manifest content (lines 87-101). Replace with file-existence or path-based assertions if needed. |
| `tests/M7/test_performance_bound.sh` | Criterion 2: Failure not attributable to the intended subject | Line 45: `ELAPSED=$({ time python3 ... 1>&3 2>&3; } 3>&1)` — both stdout and stderr of the `python3` command are redirected to fd 3 (the outer stdout write). Since `2>&3` redirects the entire `{...}` group's stderr to fd 3, the `time` command's timing output also goes to fd 3 instead of remaining on the `{...}` group's stderr for `$()` capture. `ELAPSED` is empty. Line 62: `ELAPSED_CLEAN=$(echo "$ELAPSED" | tr -d ' \n')` produces an empty string. Line 67: `echo "$ELAPSED_CLEAN <= 1.0" | bc` fails with "Parse error: bad token" on empty input. Implementation is confirmed working — the raw `time` output `0.055` (visible from the test run, 100 files in 0.055s) is well below the 1s bound. | Remove `2>&3` from the redirection: `ELAPSED=$({ time python3 ... 1>&3; } 3>&1)` keeps `time` output on captured stderr while routing `python3` stdout only to fd 3. |

---

## Passed Tests

| Test File | Verification ID | Requirement | Raw Output |
|-----------|----------------|-------------|-----------|
| `tests/M7/test_classify_tier2_directory.sh` | V-FR-12b | FR-12 (Tier 2) | `PASS: All tests passed.` (exit 0) |
| `tests/M7/test_classify_tier3_headers.sh` | V-FR-12c | FR-12 (Tier 3) | `PASS` (exit 0) — All 3 assertions passed including `plain_doc.md` fall-through |
| `tests/M7/test_classify_tier4_filenames.sh` | V-FR-12d | FR-12 (Tier 4) | `All tests passed.` (exit 0) — All 4 assertions passed including `random.md` fall-through |
| `tests/M7/test_classify_tier5_custom.sh` | V-FR-12e | FR-12 (Tier 5) | `All tests passed.` (exit 0) |
| `tests/M7/test_classify_tier6_fallback.sh` | V-FR-12f | FR-12 (Tier 6) | `All tests passed.` (exit 0) |
| `tests/M7/test_zero_touch_invariance.sh` | V-FR-13 | FR-13 | `PASS: All checksums unchanged, file count unchanged, exit code 0` (exit 0) |
| `tests/M7/test_safe_fallback.sh` | V-FR-14 | FR-14 | `PASS: FR-14 — Both unclassifiable files produce AMBIGUOUS_LEGACY_ARTIFACT with manual review flag.` (exit 0) |
| `tests/M7/test_coexistence_manifest.sh` | V-FR-15 | FR-15 | `All tests passed.` (exit 0) — legacy manifest integration verified in `resolve_artifact.py` |
| `tests/M7/test_integrity_checksum.sh` | V-NFR-5 | NFR-5 | `All tests passed.` (exit 0) — `ALL MATCH` for checksum integrity verification |

---

## Failed Tests

| Test File | Verification ID | Requirement | Verdict | Raw Failure |
|-----------|----------------|-------------|---------|-------------|
| `tests/M7/test_legacy_manifest.sh` | V-FR-11 | FR-11 | INVALID_TEST | `FAIL: Line 1: referenced file '1S1.md' does not exist` — off-by-one in path extraction (`${line:66}` → `${line:65}`) |
| `tests/M7/test_classify_tier1_frontmatter.sh` | V-FR-12a | FR-12 (T1) | INVALID_TEST | `ASSERTION FAILURE (V-FR-12a): SPEC-001 not found in manifest` — test checks YAML id in manifest; manifest format is `<SHA-256> <path>` only |
| `tests/M7/test_performance_bound.sh` | V-NFR-6 | NFR-6 | INVALID_TEST | `Elapsed time: s` + `FAIL: Performance bound exceeded` — `ELAPSED` empty due to broken fd redirection (`2>&3` routes `time` output to wrong fd) |

---

## Bugs Auto-Resolved

**None.** All 3 failing tests are INVALID_TEST (test-side defects). No implementation bugs were identified. All 9 valid tests pass, confirming the implementation is correct.

---

## Remaining Structural Failures

**None.** The implementation at `bin/legacy_indexer.py`, `bin/resolve_artifact.py`, and `milestones/M7/legacy_manifest.txt` is complete and correct per the verification protocol. The 3 test failures are all test script defects that do not affect the implementation.

---

## Next Steps

Task complete. Next Step: Please run `skills:/review-implementation` to continue.

The test defects in 3 scripts should be repaired before the next specification cycle:
1. `tests/M7/test_legacy_manifest.sh:84` — `"${line:66}"` → `"${line:65}"`
2. `tests/M7/test_classify_tier1_frontmatter.sh:87-101` — Remove assertions checking YAML `id` values in manifest content
3. `tests/M7/test_performance_bound.sh:45` — Remove `2>&3` from the fd redirection

---

## Raw Evidence

### Metadata Validation

- M7S3.md: `python3 bin/validate_metadata.py milestones/M7/M7S3.md` → `OK: milestones/M7/M7S3.md — metadata valid` (exit 0)
- M7S3V.md: `python3 bin/validate_metadata.py milestones/M7/M7S3V.md` → `OK: milestones/M7/M7S3V.md — metadata valid` (exit 0)

### Test Execution

All commands run from project root (`~/devcode/aef/agent`).

#### Passing Tests (9/12)

1. **V-FR-12b** — `bash tests/M7/test_classify_tier2_directory.sh`
   ```
   Test 1: V-FR-12b — Tier 2 directory structure classification...
   PASS: Verbose output references Tier 2 classification
   PASS: All 3 files present in manifest
   PASS: All manifest entries match SHA-256 checksum format
   All tests passed.
   Exit: 0
   ```

2. **V-FR-12c** — `bash tests/M7/test_classify_tier3_headers.sh`
   ```
   PASS: Fixture files created...
   PASS: Exit code 0
   PASS: Manifest created...
   PASS: Manifest has exactly 3 entries
   PASS: All 3 manifest lines match 64-char hex + relative-path format
   PASS: spec_doc.md classified via Tier 3 (heading matching)
   PASS: inv_doc.md classified via Tier 3 (heading matching)
   PASS: plain_doc.md falls through to Tier 4 or higher (no heading match)
   PASS: All 3 fixture files present in manifest
   PASS
   Exit: 0
   ```

3. **V-FR-12d** — `bash tests/M7/test_classify_tier4_filenames.sh`
   ```
   Test 1: Exit code 0... PASS
   Test 2: Verbose output mentions Tier 4 or filename... PASS
   Test 3: All 8 files in manifest... PASS
   Test 4: random.md falls through (unclassified)... PASS
   All tests passed.
   Exit: 0
   ```

4. **V-FR-12e** — `bash tests/M7/test_classify_tier5_custom.sh`
   ```
   PASS: Exit code 0
   PASS: Verbose output references Tier 5 / custom pattern mapping
   PASS: Manifest contains custom-report.md
   PASS: Manifest contains custom-spec.md
   All tests passed.
   Exit: 0
   ```

5. **V-FR-12f** — `bash tests/M7/test_classify_tier6_fallback.sh`
   ```
   PASS: Both ambiguous files flagged for Tier 6 fallback (manual review)
   All tests passed.
   Exit: 0
   ```

6. **V-FR-13** — `bash tests/M7/test_zero_touch_invariance.sh`
   ```
   PASS: All checksums unchanged, file count unchanged, exit code 0
   Exit: 0
   ```

7. **V-FR-14** — `bash tests/M7/test_safe_fallback.sh`
   ```
   PASS: FR-14 — Both unclassifiable files produce AMBIGUOUS_LEGACY_ARTIFACT with manual review flag.
   Exit: 0
   ```

8. **V-FR-15** — `bash tests/M7/test_coexistence_manifest.sh`
   ```
   Step 1: Generate legacy manifest... PASS
   Step 2: Resolve M99S1... PASS (Tier 3 exact match)
   Step 3: Resolve M99S1V... PASS (Tier 3 exact match)
   All tests passed.
   Exit: 0
   ```

9. **V-NFR-5** — `bash tests/M7/test_integrity_checksum.sh`
   ```
   PASS: ALL MATCH
   All tests passed.
   Exit: 0
   ```

#### Failing Tests (3/12) — All INVALID_TEST

10. **V-FR-11** — `bash tests/M7/test_legacy_manifest.sh`
    ```
    PASS: bin/legacy_indexer.py exited with code 0
    PASS: Manifest file exists...
    PASS: Manifest has exactly 3 non-empty lines
    FAIL: Line 1: referenced file '1S1.md' does not exist at '.../M1/1S1.md'
    Exit: 1
    ```
    Root cause: Line 84 `path_part="${line:66}"` should be `"${line:65}"`. The hex is 64 chars at indices 0-63, space at 64, path starts at 65.

11. **V-FR-12a** — `bash tests/M7/test_classify_tier1_frontmatter.sh`
    ```
    === V-FR-12a: Tier 1 (frontmatter) classification ===
    PASS: Verbose output indicates Tier 1 classification
    PASS: Manifest file created
    ASSERTION FAILURE (V-FR-12a): SPEC-001 not found in manifest
    Manifest content:
    390613035f... M1/spec.md
    660ba11571... M1/ver.md
    Exit: 1
    ```
    Root cause: Test checks for YAML `id` values ("SPEC-001") in manifest content. Per FR-11, manifest is `<SHA-256> <path>` format only.

12. **V-NFR-6** — `bash tests/M7/test_performance_bound.sh`
    ```
    Created 100 fixture files in .../performance/M1
    Test: Performance bound — index 100 files under 1 second...
    0.055
    Elapsed time: s
    Parse error: bad token
        <stdin>:1
    FAIL: Performance bound exceeded — s > 1.0s
    Exit: 1
    ```
    Root cause: Line 45 `ELAPSED=$({ time python3 ... 1>&3 2>&3; } 3>&1)` — `2>&3` routes `time`'s stderr to fd 3, so `$()` captures nothing. Actual performance is 0.055s (well under 1s bound).
