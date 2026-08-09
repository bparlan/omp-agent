---
id: VER-003
type: verification
title: "Verification Protocol for M7S3: Legacy Compatibility & Transition"
milestone_id: M7
status: draft
derived_from:
  - M7
  - SPEC-003
template_version: 1.1.0
---

# Verification Protocol for M7S3: Legacy Compatibility & Transition

## Requirement Inventory

| Requirement ID | Source       | Requirement |
|----------------|--------------|-------------|
| FR-11          | SPEC-003 §52 | Provide a utility (`bin/legacy_indexer.py`) that maps every pre-M10 file path to its SHA-256 checksum and records the mapping in `milestones/M7/legacy_manifest.txt`. Each manifest entry MUST be a single line formatted as `<SHA-256> <relative-path>`. |
| FR-12          | SPEC-003 §54 | Implement 6-tier classification fallback: 1. Existing frontmatter metadata, 2. Directory structure, 3. Top-level Markdown headers, 4. Legacy filename naming conventions, 5. Custom filename pattern mapping, 6. Human review. |
| FR-13          | SPEC-003 §69 | The indexing engine is strictly read-only. Forbidden from renaming, moving, or writing frontmatter to any M1-M9 file. All mappings recorded solely in external legacy index. |
| FR-14          | SPEC-003 §71 | Any file that cannot be classified through tiers 1-5 MUST resolve to `AMBIGUOUS_LEGACY_ARTIFACT` and be flagged for human review. |
| FR-15          | SPEC-003 §73 | `resolve_artifact.py` MUST integrate queries against the legacy index so legacy files are discoverable as valid targets. The resolution engine MUST consult the legacy manifest as a fallback tier equivalent to Tier 3. |
| NFR-5          | SPEC-003 §79 | Post-execution verification MUST prove that SHA-256 checksums of all M1-M9 files match the legacy baseline manifest exactly. |
| NFR-6          | SPEC-003 §81 | Consulting the legacy index MUST NOT add more than 1 second of latency to resolution for a milestone directory with up to 100 indexed legacy files. |

---

## Followup Reuse

### Prior Sources

- M7S2 (SPEC-002)
- M7S2V (VER-002)

### Reusable Verification Patterns

- **SCRIPT_EXECUTION** pattern for `bin/` scripts — reused from V-FR-7a through V-FR-9. The same fixture-based execution pattern applies to `legacy_indexer.py` and the updated `resolve_artifact.py`.
- **FILE_STRUCTURE_CHECK** pattern for verifying manifest existence — adapted from V-FR-6 design.
- **Read-only invariance** pattern — reused from V-NFR-2. Checksum-based verification before/after execution applies to both `legacy_indexer.py` and `resolve_artifact.py`.

### New Verification Required

- V-FR-11: SCRIPT_EXECUTION for legacy manifest generation (SHA-256 + path)
- V-FR-12a: SCRIPT_EXECUTION for Tier 1 (frontmatter) classification
- V-FR-12b: SCRIPT_EXECUTION for Tier 2 (directory structure) classification
- V-FR-12c: SCRIPT_EXECUTION for Tier 3 (Markdown headers) classification
- V-FR-12d: SCRIPT_EXECUTION for Tier 4 (legacy filename) classification
- V-FR-12e: SCRIPT_EXECUTION for Tier 5 (custom pattern) classification
- V-FR-12f: SCRIPT_EXECUTION for Tier 6 fallback (human review marker)
- V-FR-13: SCRIPT_EXECUTION for zero-touch invariance (read-only)
- V-FR-14: SCRIPT_EXECUTION for safe fallback (`AMBIGUOUS_LEGACY_ARTIFACT`)
- V-FR-15: SCRIPT_EXECUTION for legacy manifest integration in resolve_artifact.py
- V-NFR-5: SCRIPT_EXECUTION for post-execution checksum verification
- V-NFR-6: SCRIPT_EXECUTION for performance bound (≤1s)

---

## Verification Items

### V-FR-11

**Source Requirement:** FR-11

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable. The Python environment has `hashlib` (stdlib) and `PyYAML` installed.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/legacy_indexer/M1/` containing:
  - `M1S1.md` — A pre-M10 artifact file with some content (e.g., `echo "spec content" > M1S1.md`)
  - `M1S1V.md` — A second artifact file with different content
  - `M1S1T1.md` — A third artifact file

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/legacy_indexer --output tests/M7/fixtures/legacy_indexer/legacy_manifest.txt
```

**Expected Evidence:**
1. Exit code `0`
2. File `tests/M7/fixtures/legacy_indexer/legacy_manifest.txt` is created
3. Manifest contains exactly one line per fixture file
4. Each line matches the format `<SHA-256> <relative-path>` where:
   - SHA-256 is a valid 64-character hex string
   - Relative path corresponds to one of the fixture files

**Fail Condition:**
Non-zero exit code, manifest not created, incorrect line count, or malformed entry format.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12a

**Source Requirement:** FR-12 (Tier 1 — Existing frontmatter metadata)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier1/M1/` containing:
  - `spec.md` — A file with YAML frontmatter containing `id: SPEC-001` and `type: specification`, then content `# Specification\n\nBody text.`
  - `ver.md` — A file with YAML frontmatter containing `id: VER-001` and `type: verification`, then content `# Verification\n\nBody text.`

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier1 --output tests/M7/fixtures/classify_tier1/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates both files classified via Tier 1 (frontmatter metadata)
3. Both files appear in the manifest with correct SHA-256 checksums

**Fail Condition:**
Non-zero exit code, or files not classified via Tier 1, or files missing from manifest.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12b

**Source Requirement:** FR-12 (Tier 2 — Directory structure)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier2/M1/` containing:
  - `specifications/spec.md` — A file with NO YAML frontmatter, content `# Some Document\n\nBody.`
  - `verifications/ver.md` — A file with NO YAML frontmatter, content `# Some Document\n\nBody.`
  - `tests/test.md` — A file with NO YAML frontmatter, content `# Some Document\n\nBody.`

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier2 --output tests/M7/fixtures/classify_tier2/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates files classified via Tier 2 (directory structure)
3. All files appear in the manifest

**Fail Condition:**
Non-zero exit code, or files not classified via Tier 2, or files missing from manifest.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12c

**Source Requirement:** FR-12 (Tier 3 — Top-level Markdown headers)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier3/M1/` containing:
  - `spec_doc.md` — A file with NO YAML frontmatter, NO directory context, content `# Specification\n\nThis is the main specification document.`
  - `inv_doc.md` — A file with NO YAML frontmatter, NO directory context, content `# Investigation\n\nThis is an investigation report.`
  - `plain_doc.md` — A file with NO YAML frontmatter, NO directory context, content `# Notes\n\nJust some notes.`

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier3 --output tests/M7/fixtures/classify_tier3/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates `spec_doc.md` classified via Tier 3 as specification
3. Verbose output indicates `inv_doc.md` classified via Tier 3 as investigation
4. `plain_doc.md` (header `# Notes`) does not match Tier 3 and falls through to Tier 4

**Fail Condition:**
Non-zero exit code, or files misclassified, or Tier 3 matching not reported in verbose output.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12d

**Source Requirement:** FR-12 (Tier 4 — Legacy filename naming conventions)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier4/M1/` containing:
  - `M1S1.md` — A file with NO YAML frontmatter, NO directory context, NO heading match, content `# Random\n\nBody.`
  - `M1S1V.md` — Same pattern
  - `M1S1T1.md` — Same pattern
  - `M1S1C.md` — Same pattern
  - `M1S1E.md` — Same pattern
  - `M1S1R.md` — Same pattern
  - `M1S1I1.md` — Same pattern
  - `random.md` — A file with NO YAML frontmatter, NO directory context, NO heading match, NO legacy naming pattern

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier4 --output tests/M7/fixtures/classify_tier4/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates each `M1S1*.md` file classified via Tier 4 with correct artifact type mapping
3. `random.md` falls through Tier 4 (no legacy pattern match) to Tier 5

**Fail Condition:**
Non-zero exit code, or any `M1S1*.md` file not classified via Tier 4, or `random.md` incorrectly classified as a known type.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12e

**Source Requirement:** FR-12 (Tier 5 — Custom filename pattern mapping)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable. The script accepts a `--pattern-map` or equivalent option for custom patterns.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier5/M1/` containing:
  - `custom-report.md` — A file with NO YAML frontmatter, NO directory context, NO heading match, NO legacy naming
  - `custom-spec.md` — Same pattern
- A custom mapping file `tests/M7/fixtures/classify_tier5/pattern_map.txt` containing:
  - `custom-report.md:investigation`
  - `custom-spec.md:specification`

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier5 --output tests/M7/fixtures/classify_tier5/legacy_manifest.txt --verbose --pattern-map tests/M7/fixtures/classify_tier5/pattern_map.txt
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates both files classified via Tier 5 (custom pattern mapping)
3. Both files appear in the manifest

**Fail Condition:**
Non-zero exit code, or files not classified via Tier 5, or files missing from manifest.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-12f

**Source Requirement:** FR-12 (Tier 6 — Human review / AMBIGUOUS_LEGACY_ARTIFACT)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/classify_tier6/M1/` containing:
  - `unknown_1.xyz` — A file with NO YAML frontmatter, NO directory context, NO heading match, NO legacy naming, NO custom mapping
  - `data.bin` — A file with NO YAML frontmatter, NO directory context, NO heading match, NO legacy naming, NO custom mapping

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier6 --output tests/M7/fixtures/classify_tier6/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. Verbose output indicates both files classified as `AMBIGUOUS_LEGACY_ARTIFACT` via Tier 6
3. Stderr contains a flag or warning about both files requiring manual review

**Fail Condition:**
Non-zero exit code, or any file assigned a guessing category instead of `AMBIGUOUS_LEGACY_ARTIFACT`, or no stderr flag for manual review.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-13

**Source Requirement:** FR-13 (Zero-Touch Invariance)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/zero_touch/M1/` containing:
  - `M1S1.md` — A pre-M10 artifact file
  - `M1S1V.md` — A second artifact file
  - `M1S1T1.md` — A third artifact file
- Record SHA-256 checksums of all fixture files BEFORE execution.

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/zero_touch --output tests/M7/fixtures/zero_touch/legacy_manifest.txt
```

**Expected Evidence:**
1. Exit code `0`
2. After execution, all fixture file SHA-256 checksums match the pre-execution baseline.
3. No new files were created inside the `M1/` directory (only the manifest in the output path).
4. No files were renamed or moved inside the `M1/` directory.

**Fail Condition:**
Non-zero exit code, or any fixture file checksum changes, or any fixture file renamed/moved, or any new file created inside the fixture directory.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-14

**Source Requirement:** FR-14 (Safe Fallback)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py`

**Precondition:**
Same as V-FR-12f (same fixture).

**Fixture Requirements:**
Same fixture as V-FR-12f: `tests/M7/fixtures/classify_tier6/M1/` containing `unknown_1.xyz` and `data.bin`.

**Command:**
```
python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/classify_tier6 --output tests/M7/fixtures/classify_tier6/legacy_manifest.txt --verbose
```

**Expected Evidence:**
1. Exit code `0`
2. The manifest entries for unclassifiable files contain the category `AMBIGUOUS_LEGACY_ARTIFACT` (not a guessed type like `specification` or `investigation`)
3. Stderr flags both files as requiring manual review

**Fail Condition:**
Any file is assigned a guessed type instead of `AMBIGUOUS_LEGACY_ARTIFACT`.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-FR-15

**Source Requirement:** FR-15 (Coexistence)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/resolve_artifact.py`

**Precondition:**
The script `bin/resolve_artifact.py` exists and is executable. The legacy manifest has been generated by `legacy_indexer.py` for the fixture directory.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/coexistence/M99/` containing:
  - `M99S1.md` — A file with NO YAML frontmatter, filename matches legacy pattern `M99S1`
  - `M99S1V.md` — A file with NO YAML frontmatter
- A legacy manifest `tests/M7/fixtures/coexistence/legacy_manifest.txt` generated by `legacy_indexer.py` containing entries for the above files.

**Commands:**
1. `python3 bin/resolve_artifact.py M99S1 --milestone M99 --cwd tests/M7/fixtures/coexistence --verbose`
2. `python3 bin/resolve_artifact.py M99S1V --milestone M99 --cwd tests/M7/fixtures/coexistence --verbose`

**Expected Evidence:**
1. Both commands exit with code `0`
2. Output contains the resolved file path for each queried ID
3. Verbose output indicates the resolution tier (either Tier 3 filename heuristics or the legacy manifest fallback)

**Fail Condition:**
Non-zero exit code for either query, or resolved path does not match the expected file, or verbose output does not report the resolution mechanism.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-NFR-5

**Source Requirement:** NFR-5 (Immutable Integrity)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py` (post-execution checksum verification)

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable. The legacy manifest exists for the fixture directory.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/integrity/M1/` containing:
  - `M1S1.md` — A pre-M10 artifact file
  - `M1S1V.md` — A second artifact file
- Run `legacy_indexer.py` to generate `legacy_manifest.txt`

**Command:**
```
python3 -c "
import hashlib, os
manifest = 'tests/M7/fixtures/integrity/legacy_manifest.txt'
base = 'tests/M7/fixtures/integrity'
mismatches = []
with open(manifest) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        expected_hash, rel_path = line.split(' ', 1)
        full_path = os.path.join(base, rel_path)
        actual_hash = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
        if actual_hash != expected_hash:
            mismatches.append(f'{rel_path}: expected {expected_hash}, got {actual_hash}')
if mismatches:
    print('MISMATCHES:', '\n'.join(mismatches))
    exit(1)
else:
    print('ALL MATCH')
    exit(0)
"
```

**Expected Evidence:**
1. Exit code `0`
2. Output contains `ALL MATCH`

**Fail Condition:**
Exit code `1`, or any checksum mismatch reported.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

### V-NFR-6

**Source Requirement:** NFR-6 (Resolution Performance)

**Verification Method:** SCRIPT_EXECUTION

**Target:**
`bin/legacy_indexer.py` (implicitly, the manifest generation that feeds into resolution)

**Precondition:**
The script `bin/legacy_indexer.py` exists and is executable.

**Fixture Requirements:**
- A temporary milestone directory `tests/M7/fixtures/performance/M1/` containing 100+ files. Generate fixture files programmatically:
  - 100 files with legacy naming patterns (e.g., `M1S1.md` through `M1S100.md`)
  - Each file containing minimal content

**Command:**
```
time python3 bin/legacy_indexer.py --milestone-dir tests/M7/fixtures/performance --output tests/M7/fixtures/performance/legacy_manifest.txt
```

**Expected Evidence:**
1. Exit code `0`
2. The `time` output indicates total elapsed real time ≤ 1 second

**Fail Condition:**
Non-zero exit code, or resolution time exceeds 1 second.

**Initial Failure Expectation:**
VALID_INITIAL_FAILURE_POSSIBLE

**Post-Implementation Expectation:**
PASS

---

## Traceability Matrix

| Requirement | Verification | Method         | Test File (planned)            | Initial Failure | Status |
|-------------|-------------|----------------|--------------------------------|-----------------|--------|
| FR-11       | V-FR-11     | SCRIPT_EXECUTION | test_legacy_manifest.sh        | POSSIBLE        | READY  |
| FR-12 (T1)  | V-FR-12a    | SCRIPT_EXECUTION | test_classify_tier1_frontmatter.sh | POSSIBLE    | READY  |
| FR-12 (T2)  | V-FR-12b    | SCRIPT_EXECUTION | test_classify_tier2_directory.sh   | POSSIBLE    | READY  |
| FR-12 (T3)  | V-FR-12c    | SCRIPT_EXECUTION | test_classify_tier3_headers.sh     | POSSIBLE    | READY  |
| FR-12 (T4)  | V-FR-12d    | SCRIPT_EXECUTION | test_classify_tier4_filenames.sh   | POSSIBLE    | READY  |
| FR-12 (T5)  | V-FR-12e    | SCRIPT_EXECUTION | test_classify_tier5_custom.sh      | POSSIBLE    | READY  |
| FR-12 (T6)  | V-FR-12f    | SCRIPT_EXECUTION | test_classify_tier6_fallback.sh    | POSSIBLE    | READY  |
| FR-13       | V-FR-13     | SCRIPT_EXECUTION | test_zero_touch_invariance.sh      | POSSIBLE    | READY  |
| FR-14       | V-FR-14     | SCRIPT_EXECUTION | test_safe_fallback.sh              | POSSIBLE    | READY  |
| FR-15       | V-FR-15     | SCRIPT_EXECUTION | test_coexistence_manifest.sh       | POSSIBLE    | READY  |
| NFR-5       | V-NFR-5     | SCRIPT_EXECUTION | test_integrity_checksum.sh         | POSSIBLE    | READY  |
| NFR-6       | V-NFR-6     | SCRIPT_EXECUTION | test_performance_bound.sh          | POSSIBLE    | READY  |

---

## Test File Planning

Planned test files:

```text
tests/M7/test_legacy_manifest.sh
tests/M7/test_classify_tier1_frontmatter.sh
tests/M7/test_classify_tier2_directory.sh
tests/M7/test_classify_tier3_headers.sh
tests/M7/test_classify_tier4_filenames.sh
tests/M7/test_classify_tier5_custom.sh
tests/M7/test_classify_tier6_fallback.sh
tests/M7/test_zero_touch_invariance.sh
tests/M7/test_safe_fallback.sh
tests/M7/test_coexistence_manifest.sh
tests/M7/test_integrity_checksum.sh
tests/M7/test_performance_bound.sh
```

---

## Final Readiness Gate

- [x] Canonical specification has valid frontmatter.
- [x] Verification artifact has valid frontmatter.
- [x] Every requirement has an ID.
- [x] Every requirement has verification coverage.
- [x] Every verification item has a method.
- [x] Every executable verification has deterministic evidence.
- [x] No verification relies on invented APIs.
- [x] No verification relies on arbitrary prose matching.
- [x] No circular oracle exists.
- [x] Every executable verification has an initial failure assessment.
- [x] Every test planned has a traceability mapping.
- [x] No orphan requirements.
- [x] No orphan verification items.
- [x] No orphan test plans.
- [x] Specification verification is separated from implementation verification.

**Final Gate: READY_FOR_TEST_GENERATION**

Next Step: Please run `/generate-tests`.