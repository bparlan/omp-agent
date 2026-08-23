---
id: aef:EVAL-M7S2
type: evaluation
title: Evaluation Report for M7S2
milestone_id: M7
status: completed
derived_from: [SPEC-002, VER-002]
template_version: 1.0.2
---

## Test Execution Summary

- **TESTS_RUN:** 9
- **TESTS_PASSED:** 9
- **TESTS_FAILED:** 0
- **EXIT_CODE:** 0 (PASS)

---

## Validity Gate Results

- **VALID_TESTS:** 9
- **INVALID_TESTS:** 0

### Validity Assessment

All 9 test scripts were inspected for the six validity criteria:

1. **Exercised intended subject**: Each test invokes the correct target (`resolve_artifact.py`, `validate_metadata.py`, or `docs/ARTIFACT_ARCHITECTURE.md`) via `python3` or file reads.
2. **Failure attributable to subject**: Test failures would indicate bugs in the implementation, not infrastructure/environment.
3. **Deterministic environment**: Tests use fixture directories, not live milestone data. The large fixture for performance testing is created at runtime and cleaned up. No dependency on external state.
4. **Working tree is clean**: The implementation (`bin/resolve_artifact.py`, `docs/ARTIFACT_ARCHITECTURE.md`) is committed. Tests read isolated fixture directories.
5. **No self-scanning**: Tests examine fixture directories or the target document, not their own source code.
6. **Diagnostic failure messages**: Each test prints which assertion failed, the expected vs actual values, and the test output.

### Invalidation Reports

None.

---

## Passed Tests

| Test File | Verification ID | Exit Code | Key Findings |
|-----------|----------------|-----------|--------------|
| `test_resolve_canonical_id.sh` | V-FR-7a, V-FR-9 | 0 | SPEC-001 resolved via Tier 1 (YAML metadata). VER-001 resolved via Tier 2 (directory context). Verbose mode reports resolution tier. |
| `test_resolve_legacy_id.sh` | V-FR-7b, V-FR-9 | 0 | M7S1 resolved via Tier 3 (legacy filename heuristic). Verbose mode correctly reports "Tier 3" for legacy IDs. |
| `test_resolve_conflict_detection.sh` | V-FR-8 | 0 | VER-001 in `specifications/` directory detected with exit code 2. Conflict report includes file path, expected type, actual type, and queried identifier. |
| `test_resolve_not_found.sh` | V-FR-7a (not-found) | 0 | SPEC-999 returns exit code 1 with "not found" message. Non-existent milestone directory returns exit code 1. |
| `test_resolve_readonly.sh` | V-NFR-2 | 0 | SHA256 checksums of all fixture files are identical before and after resolution. No files modified. |
| `test_resolve_artifacts.sh` | V-NFR-3, V-NFR-4 | 0 | Performance: resolution completes within 1s (bound: 5s) with 100+ fixture files. Portable path: resolution works from outside project root via `--cwd`. |
| `test_artifact_architecture_docs.sh` | V-FR-6, V-FR-10 | 0 | Canonical directory structure defined (8/8 type subdirectories). 3-tier resolution priority, conflict detection, and dual query support all referenced. |
| `test_spec_metadata_contract.sh` | (M7S1) | 0 | All specification contract checks pass (canonical identifiers, YAML frontmatter mandate, required fields, semantic qualifier prohibition). |
| `test_validate_metadata_script.sh` | (M7S1) | 0 | `validate_metadata.py` executes correctly with valid and invalid fixtures, producing expected exit codes. |

---

## Failed Tests

None.

---

## Bugs Auto-Resolved

### Bug 1: Conflict detection not triggered in Tier 1

**Symptom**: `test_resolve_conflict_detection.sh` failed with exit code 0 instead of expected 2. The file at `tests/M7/fixtures/resolve_conflict/M99/specifications/VER-001.md` has `type: verification` in its frontmatter but lives in `specifications/` directory. Tier 1 (YAML metadata scan) found the file by its `id: VER-001` and returned it immediately without running conflict detection.

**Fix**: Added `detect_conflict()` call to the Tier 1 handler in `main()` (line 292-299 of `bin/resolve_artifact.py`). Conflict detection now runs on all three tiers, not just Tier 2 and Tier 3.

**Verification**: After fix, `test_resolve_conflict_detection.sh` exits with code 0 and reports "PASS: Conflict detected correctly with exit code 2".

### Bug 2: `DIR_TO_TYPE` mapping used prefixes instead of full type names

**Symptom**: Fixing Bug 1 broke `test_resolve_canonical_id.sh`. The `detect_conflict()` function compared the directory-derived expected type (`SPEC`) against the YAML frontmatter type (`specification`), triggering a false conflict on all valid files.

**Root cause**: `DIR_TO_TYPE` was initialized as `{v: k for k, v in TYPE_DIR_MAP.items()}` which maps directory names to type prefixes (e.g., `specifications` → `SPEC`). But the YAML `type` field uses full type names (e.g., `specification`, `verification`).

**Fix**: Replaced the computed `DIR_TO_TYPE` dict with an explicit mapping from directory names to YAML type names:

```python
DIR_TO_TYPE = {
    "specifications": "specification",
    "verifications": "verification",
    "tests": "test_set",
    ...
}
```

**Verification**: After fix, all 7 M7S2 tests pass.

---

## Remaining Structural Failures

None.

---

## Next Steps

All 9 tests pass. The implementation of `bin/resolve_artifact.py` (3-tier resolution, conflict detection, dual query support) and `docs/ARTIFACT_ARCHITECTURE.md` (formalized directory structure contract) is complete and verified. No remaining failures.

---

## Raw Evidence

- **Metadata validation**: `python3 bin/validate_metadata.py milestones/M7/M7S2.md milestones/M7/M7S2V.md milestones/M7/M7S2C.md`
  → `OK: milestones/M7/M7S2.md — metadata valid` (x3)

- **Canonical ID resolution**: `bash tests/M7/test_resolve_canonical_id.sh`
  → `All tests passed.` (exit 0)

- **Legacy ID resolution**: `bash tests/M7/test_resolve_legacy_id.sh`
  → `All tests passed.` (exit 0)

- **Conflict detection**: `bash tests/M7/test_resolve_conflict_detection.sh`
  → `All tests passed.` (exit 0)

- **Not found handling**: `bash tests/M7/test_resolve_not_found.sh`
  → `All tests passed.` (exit 0)

- **Read-only constraint**: `bash tests/M7/test_resolve_readonly.sh`
  → `All tests passed.` (exit 0)

- **Performance & portable path**: `bash tests/M7/test_resolve_artifacts.sh`
  → `All tests passed.` (exit 0)

- **Architecture docs contract**: `bash tests/M7/test_artifact_architecture_docs.sh`
  → `All tests passed.` (exit 0)

- **Spec metadata contract**: `bash tests/M7/test_spec_metadata_contract.sh`
  → `All specification checks passed.` (exit 0)

- **Validate metadata script**: `bash tests/M7/test_validate_metadata_script.sh`
  → `Test for script execution outcome completed.` (exit 0)