---
id: VER-002
type: verification
title: "Verification Protocol for M7S2: Artifact Resolution & Canonical Storage"
milestone_id: M7
status: draft
derived_from:
  - M7
  - SPEC-002
template_version: 1.1.0
---

# Verification Protocol for M7S2: Artifact Resolution & Canonical Storage

## Requirement Inventory

| Requirement ID | Source     | Requirement |
|----------------|------------|-------------|
| FR-6           | SPEC-002 §51 | Define the canonical directory structure contract for AEF artifact storage: base path `milestones/{M_ID}/` with optional type subdirectories (`specifications/`, `verifications/`, `tests/`, `investigations/`, `implementations/`, `evaluations/`, `reviews/`, `audits/`). |
| FR-7           | SPEC-002 §53 | Implement `resolve_artifact.py` in `bin/` with 3-tier priority resolution: 1. Explicit YAML metadata, 2. Canonical Directory Context, 3. Filename heuristics (Legacy only). |
| FR-8           | SPEC-002 §58 | Implement conflict detection: when a file's YAML `type` field disagrees with its directory location, flag with exit code 2. |
| FR-9           | SPEC-002 §60 | Support querying by both canonical IDs (`SPEC-001`) and legacy IDs (`M7S1`). Report which resolution tier produced the match. |
| FR-10          | SPEC-002 §62 | Update `docs/ARTIFACT_ARCHITECTURE.md` to formalize the directory structure as a contract with definitive language, referencing FR-6 through FR-9 and the 3-tier resolution priority. |
| NFR-2          | SPEC-002 §68 | The resolution script MUST NOT modify or move any files. Read-only utility. |
| NFR-3          | SPEC-002 §69 | Complete search within 5 seconds for a milestone directory with up to 100 artifact files. |
| NFR-4          | SPEC-002 §70 | Invocable from any working directory with portable path resolution relative to project root. |

---

## Followup Reuse

### Prior Sources

- M7S1 (SPEC-001)
- M7S1V (VER-001)

### Reusable Verification Patterns

- **SCRIPT_EXECUTION** pattern for `bin/` scripts — reused from V-FR-5 (validate_metadata.py). The same fixture-based execution pattern applies to `resolve_artifact.py`.
- **FRONTMATTER_CHECK** pattern for YAML metadata validation — reused from V-FR-3. The conflict detection in FR-8 depends on the frontmatter contract already established by SPEC-001.

### New Verification Required

- V-FR-6: DOCUMENT_CHECK for canonical directory structure contract in ARTIFACT_ARCHITECTURE.md
- V-FR-7a: SCRIPT_EXECUTION for canonical ID resolution (Tier 1 + Tier 2)
- V-FR-7b: SCRIPT_EXECUTION for legacy ID resolution (Tier 3)
- V-FR-8: SCRIPT_EXECUTION for conflict detection
- V-FR-9: SCRIPT_EXECUTION for dual query support
- V-FR-10: DOCUMENT_CHECK for ARTIFACT_ARCHITECTURE.md formalization
- V-NFR-2: SCRIPT_EXECUTION for read-only verification
- V-NFR-3: SCRIPT_EXECUTION for performance bound
- V-NFR-4: SCRIPT_EXECUTION for portable path resolution

---

## Verification Items

### V-FR-6

**Source Requirement:** FR-6

**Verification Method:** DOCUMENT_CHECK

**Target:**
`docs/ARTIFACT_ARCHITECTURE.md`

**Precondition:**
The file `docs/ARTIFACT_ARCHITECTURE.md` exists and is readable.

**Fixture Requirements:**
None.

**Command:**
None.

**Evidence Required:**
The document defines the canonical directory structure with:
1. Base path pattern `milestones/{M_ID}/`
2. Optional artifact type subdirectory convention
3. All 8 type subdirectory names listed: `specifications/`, `verifications/`, `tests/`, `investigations/`, `implementations/`, `evaluations/`, `reviews/`, `audits/`

**Pass Condition:**
All three structural elements are present in the document as definitive specification language (not "Proposed" or "Future").

**Fail Condition:**
One or more structural elements are absent, or the language remains provisional (e.g., "Proposed", "Future", "Idea").

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-7a

**Source Requirement:** FR-7 (Tier 1 + Tier 2 — Canonical ID Resolution)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
The script `bin/resolve_artifact.py` exists and is executable. The Python environment has `PyYAML` installed.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/resolve/M99/` containing:
  - `specifications/SPEC-001.md` — A file with YAML frontmatter containing `id: SPEC-001` and `type: specification`
  - `specifications/SPEC-099.md` — A file with YAML frontmatter containing `id: SPEC-099` and `type: specification` (used for NOT_FOUND test)
  - `verifications/VER-001.md` — A file with YAML frontmatter containing `id: VER-001` and `type: verification`
  - A flat file `M7S1.md` with YAML frontmatter containing `id: M7S1` (legacy format)

**Command:**
`python3 bin/resolve_artifact.py SPEC-001 --milestone M99 --cwd tests/M7/fixtures/resolve`

**Expected Evidence:**
1. Exit code `0`
2. Output contains the resolved file path ending in `specifications/SPEC-001.md`

**Fail Condition:**
Non-zero exit code, or output does not contain the expected path.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-7b

**Source Requirement:** FR-7 (Tier 3 — Legacy ID Resolution)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a.

**Fixture Requirements:**
Same fixture directory as V-FR-7a.

**Command:**
`python3 bin/resolve_artifact.py M7S1 --milestone M99 --cwd tests/M7/fixtures/resolve`

**Expected Evidence:**
1. Exit code `0`
2. Output contains the resolved file path ending in `M7S1.md`

**Fail Condition:**
Non-zero exit code, or output does not contain the expected path.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-8

**Source Requirement:** FR-8

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/resolve_conflict/M99/` containing:
  - `specifications/VER-001.md` — A file in `specifications/` directory with YAML frontmatter containing `id: VER-001` and `type: verification` (TYPE MISMATCH — directory says `specifications`, YAML says `verification`)

**Command:**
`python3 bin/resolve_artifact.py VER-001 --milestone M99 --cwd tests/M7/fixtures/resolve_conflict`

**Expected Evidence:**
1. Exit code `2`
2. Output contains the conflict report including: file path, expected type (`specification`), actual type (`verification`), and queried identifier (`VER-001`)

**Fail Condition:**
Exit code is not `2`, or the conflict report is missing required fields.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-9

**Source Requirement:** FR-9

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a.

**Fixture Requirements:**
- Same fixture directory as V-FR-7a (contains both canonical and legacy files).
- Create a second fixture `tests/M7/fixtures/resolve_verbose/M99/specifications/SPEC-005.md` with frontmatter `id: SPEC-005`, `type: specification`.

**Commands:**
1. `python3 bin/resolve_artifact.py SPEC-005 --milestone M99 --cwd tests/M7/fixtures/resolve_verbose --verbose`
2. `python3 bin/resolve_artifact.py M7S1 --milestone M99 --cwd tests/M7/fixtures/resolve_verbose --verbose`

**Expected Evidence:**
1. Both commands exit with code `0`.
2. In verbose mode, the output includes the resolution tier (e.g., "Tier 1: YAML metadata match" or "Tier 3: Legacy filename heuristic match").

**Fail Condition:**
Either command exits with non-zero code, or verbose output does not report the resolution tier.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-10

**Source Requirement:** FR-10

**Verification Method:** DOCUMENT_CHECK

**Target:**
`docs/ARTIFACT_ARCHITECTURE.md`

**Precondition:**
The file `docs/ARTIFACT_ARCHITECTURE.md` exists and is readable.

**Fixture Requirements:**
None.

**Command:**
None.

**Evidence Required:**
The document contains:
1. Definitive language (not "Proposed" or "Future") for the canonical directory structure
2. References to the 3-tier resolution priority (FR-7)
3. References to conflict detection (FR-8)
4. References to dual query support (FR-9)

**Pass Condition:**
All four elements are present with definitive, specification-level language.

**Fail Condition:**
One or more elements are absent, or use provisional language.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-NFR-2

**Source Requirement:** NFR-2

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a.

**Fixture Requirements:**
- Same fixture as V-FR-7a.
- Record SHA256 checksums of all fixture files before execution.

**Command:**
1. `python3 bin/resolve_artifact.py SPEC-001 --milestone M99 --cwd tests/M7/fixtures/resolve`
2. Compare checksums of all fixture files before and after execution.

**Expected Evidence:**
1. Exit code `0`
2. All fixture file checksums are identical before and after execution.

**Fail Condition:**
Any fixture file checksum changes after script execution.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-NFR-3

**Source Requirement:** NFR-3

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a.

**Fixture Requirements:**
- A fixture directory with 100+ artifact files (can be generated by test script).

**Command:**
`timeout 5 python3 bin/resolve_artifact.py SPEC-001 --milestone M99 --cwd tests/M7/fixtures/resolve_large`

**Expected Evidence:**
The command completes within 5 seconds (exit code `0`).

**Fail Condition:**
Command times out (exit code 124 from `timeout`) or exits with non-zero code.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-NFR-4

**Source Requirement:** NFR-4

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
Same as V-FR-7a. The project root is discoverable via `--cwd` or automatic detection of `milestones/` directory.

**Fixture Requirements:**
- Same fixture as V-FR-7a, accessible from a different working directory.

**Commands:**
1. `cd /tmp && python3 <project_root>/bin/resolve_artifact.py SPEC-001 --milestone M99 --cwd <project_root>/tests/M7/fixtures/resolve`

**Expected Evidence:**
Exit code `0` with correct path resolution when invoked from a directory outside the project root.

**Fail Condition:**
Non-zero exit code or incorrect path when invoked from outside the project root.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

## Edge Cases

| Edge Case | Verification | Expected Behavior |
|-----------|-------------|-------------------|
| Identifier not found in any tier | V-FR-7a, AC-4 | Exit code 1, "not found" message |
| Empty milestone directory | V-FR-7a | Exit code 1, "not found" |
| Non-existent milestone directory | V-FR-7a | Exit code 1, graceful error message |
| Malformed YAML in target file | V-FR-8 | Exit code 1 with YAML parse error (Tier 1 fails gracefully, falls through) |
| ID with leading zeros (SPEC-000) | V-FR-7a | Should resolve same as SPEC-001 |
| `--milestone` flag with path separator | V-FR-7a | Should reject or sanitize |
| Both canonical and legacy ID match same file | V-FR-9 | Tier 1 match takes priority (YAML metadata) |
| No `--cwd` flag provided | V-NFR-4 | Default to current working directory |
| Concurrent resolution requests | NFR-2 | Read-only; no lock contention |

---

## Failure Scenarios

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| `resolve_artifact.py` not found | V-FR-7a precondition | Create file at `bin/resolve_artifact.py` |
| `PyYAML` not installed | V-FR-7a precondition | `pip install pyyaml` |
| Specified milestone directory does not exist | V-FR-7a | Script must handle gracefully, exit 1 |
| Fixture directory missing | Test harness | Create fixture directory in test setup |
| Checksum mismatch (file modified) | V-NFR-2 | Bug in script — must be read-only |
| Timeout on large directory | V-NFR-3 | Performance regression — optimize resolution |

---

## Regression Checklist

- [ ] `bin/validate_metadata.py` still passes all existing tests (no regression from script updates)
- [ ] `validate_metadata.py` ID pattern still accepts `SPEC-NNN`, `VER-NNN`, `TEST-NNN`, `INV-NNN` formats
- [ ] Existing M7S1 tests still pass (no regression from metadata contract changes)

---

## Test File Planning

| Test File | Verification Items | Description |
|-----------|-------------------|-------------|
| `tests/M7/test_resolve_canonical_id.sh` | V-FR-7a, V-FR-9 | Canonical ID resolution via YAML metadata and directory context |
| `tests/M7/test_resolve_legacy_id.sh` | V-FR-7b, V-FR-9 | Legacy ID resolution via filename heuristics |
| `tests/M7/test_resolve_conflict_detection.sh` | V-FR-8 | Conflict detection with exit code 2 |
| `tests/M7/test_resolve_not_found.sh` | V-FR-7a, AC-4 | Not-found behavior with exit code 1 |
| `tests/M7/test_resolve_readonly.sh` | V-NFR-2 | Checksum verification before/after resolution |
| `tests/M7/test_resolve_artifacts.sh` | V-NFR-3, V-NFR-4 | Performance bound and portable path resolution |
| `tests/M7/test_artifact_architecture_docs.sh` | V-FR-6, V-FR-10 | ARTIFACT_ARCHITECTURE.md contract verification |

---

## Traceability Matrix

| Requirement | Verification | Method | Test File | Initial Failure | Status |
|------------|-------------|--------|-----------|----------------|--------|
| FR-6 | V-FR-6 | DOCUMENT_CHECK | test_artifact_architecture_docs.sh | POSSIBLE | READY |
| FR-7 | V-FR-7a | SCRIPT_EXECUTION | test_resolve_canonical_id.sh | POSSIBLE | READY |
| FR-7 | V-FR-7b | SCRIPT_EXECUTION | test_resolve_legacy_id.sh | POSSIBLE | READY |
| FR-8 | V-FR-8 | SCRIPT_EXECUTION | test_resolve_conflict_detection.sh | POSSIBLE | READY |
| FR-9 | V-FR-9 | SCRIPT_EXECUTION | test_resolve_canonical_id.sh, test_resolve_legacy_id.sh | POSSIBLE | READY |
| FR-10 | V-FR-10 | DOCUMENT_CHECK | test_artifact_architecture_docs.sh | POSSIBLE | READY |
| NFR-2 | V-NFR-2 | SCRIPT_EXECUTION | test_resolve_readonly.sh | POSSIBLE | READY |
| NFR-3 | V-NFR-3 | SCRIPT_EXECUTION | test_resolve_artifacts.sh | POSSIBLE | READY |
| NFR-4 | V-NFR-4 | SCRIPT_EXECUTION | test_resolve_artifacts.sh | POSSIBLE | READY |

---

## Final Readiness Gate

- [X] Canonical specification has valid frontmatter.
- [X] Verification artifact has valid frontmatter.
- [X] Every requirement has an ID.
- [X] Every requirement has verification coverage.
- [X] Every verification item has a method.
- [X] Every executable verification has deterministic evidence.
- [X] No verification relies on invented APIs.
- [X] No verification relies on arbitrary prose matching.
- [X] No circular oracle exists.
- [X] Every executable verification has an initial failure assessment.
- [X] Every test planned has a traceability mapping.
- [X] No orphan requirements.
- [X] No orphan verification items.
- [X] No orphan test plans.
- [X] Specification verification is separated from implementation verification.

---

Task complete.
Final Gate: READY_FOR_TEST_GENERATION
Next Step: Please run `/generate-tests`.