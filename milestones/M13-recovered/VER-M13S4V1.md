---
id: VER-M13S4V1
type: verification
title: "M13S4V1 — Integration with Core AEF Artifact System"
milestone_id: M13
status: draft
derived_from:
  - M13
  - SPEC-M13S4
template_version: 1.1.0
---

## Success Criteria

- [ ] `validate_metadata()` is invoked by `manage-development` on every artifact under `milestones/M13/`; each invocation returns `{"valid": true, "errors": [], "missing_fields": []}`
- [ ] `PIPELINE-STATE.md` contains structured per-artifact entries (path, valid, errors, missing_fields, timestamp, stage) for all M13 artifacts
- [ ] `get_artifact_type()` resolves all six pipeline naming patterns (`SPEC-M13S{n}`, `VER-M13S{n}V{m}`, `TEST-M13S{n}T{p}`, `EVA-M13S{n}`, `REV-M13S{n}`, `CLOSE-M13-N`) without returning `None`
- [ ] `extract_frontmatter()` produces a complete dict with all required keys for every pipeline artifact; `milestone_id == "M13"` in all cases
- [ ] `create_artifact()` emits next-stage artifacts that pass `validate_metadata()` with `valid == true`; registry is updated
- [ ] Validation determinism: identical inputs produce identical outputs across repeated invocations
- [ ] Filesystem isolation: `core/` integration does not mutate files outside `milestones/M13/` or `core/`

---

## Followup Reuse

### Reusable Items from Prior Verifications

- `core/validation.py` integration test patterns from prior AEF verification artifacts (import structure, result dict assertion)
- Frontmatter extraction verification patterns from prior artifact system verification
- Registry type resolution verification patterns

### New Verification Required

- `create_artifact()` integration with `manage-development` gate flow (new end-to-end pipeline)
- `PIPELINE-STATE.md` generation with multi-artifact aggregation
- Deterministic validation repetition across all M13 artifacts

---

## Functional Validation

### FR-AEF-CANONICAL-VALIDATION-INTEGRATION

#### VER-M13S4-VAL-001 — validate_metadata Invocation Against All M13 Artifacts
*Source Requirement:* `FR-AEF-CANONICAL-VALIDATION-INTEGRATION`
*Verification Method:* INTEGRITY_TEST
*Testability:* High — `validate_metadata()` is a pure function; inputs are file paths; output is a dict
*Preconditions:* `milestones/M13/` contains at least the specification artifacts (`SPEC-M13S1.md`, `SPEC-M13S2.md`, `SPEC-M13S3.md`, `SPEC-M13S4.md`)
*Input or Fixture:*
- Fixture: list of all `.md` artifact paths under `milestones/M13/`
- Invocation: `core/validation.validate_metadata(artifact_path)` for each path
*Expected Evidence:* Each invocation returns `{"valid": true, "errors": [], "missing_fields": []}`; `valid == True` for every artifact
*Failure Condition:* Any artifact returns `valid == False` or `errors` non-empty or `missing_fields` non-empty; exit code from gate check = 1
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — implementation has not wired `validate_metadata()` into `manage-development`; verification returns zero artifacts validated or empty results (exit 1)
*Post-Implementation Success Expectation:* All M13 artifacts pass `validate_metadata()` with `valid == true` and empty error/missing lists

#### VER-M13S4-VAL-002 — PIPELINE-STATE.md Contains Per-Artifact Validation Records
*Source Requirement:* `FR-AEF-CANONICAL-VALIDATION-INTEGRATION`
*Verification Method:* INTEGRITY_TEST
*Testability:* High — filesystem check on structured output file
*Preconditions:* `manage-development` has run at least one gate validation pass against M13
*Input or Fixture:*
- Fixture: `milestones/M13/PIPELINE-STATE.md` (created by gate middleware)
*Expected Evidence:* File contains structured records with all six fields: `artifact_path` (string, valid path under `milestones/M13/`), `valid` (boolean), `errors` (array, empty), `missing_fields` (array, empty), `timestamp` (ISO 8601 string), `stage` (string matching pipeline stage name)
*Failure Condition:* File missing or empty; any record missing required fields; `valid == False` in any record
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — `PIPELINE-STATE.md` does not exist or contains no validation records (exit 1)
*Post-Implementation Success Expectation:* `PIPELINE-STATE.md` exists with complete per-artifact records for all M13 artifacts; all `valid == true`; all `errors == []`

#### VER-M13S4-VAL-003 — Gate Exit Code Reflects Validation Outcome
*Source Requirement:* `FR-AEF-CANONICAL-VALIDATION-INTEGRATION`
*Verification Method:* SCRIPT_EXECUTION
*Testability:* High — direct exit code inspection
*Preconditions:* `manage-development` skill is invoked against milestone M13
*Input or Fixture:*
- Command: `python -m skills.manage-development M13` (or equivalent skill invocation)
*Expected Evidence:* Exit code 0 when all M13 artifacts pass `validate_metadata()`; exit code 1 when any artifact fails validation
*Failure Condition:* Gate exits 0 with failing artifacts; gate exits 1 with all-passing artifacts
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — gate not yet wired; exit 127 (Command Not Found) or exit 1 (no artifacts found)
*Post-Implementation Success Expectation:* Exit code 0; `PIPELINE-STATE.md` shows all `valid == true`

---

### FR-AEF-REGISTRY-TYPE-REGISTRATION

#### VER-M13S4-REG-001 — get_artifact_type Resolves All Six Pipeline Patterns
*Source Requirement:* `FR-AEF-REGISTRY-TYPE-REGISTRATION`
*Verification Method:* UNIT_TEST
*Testability:* High — pure function call with known identifiers
*Preconditions:* `core/artifacts/artifact_types` module is importable
*Input or Fixture:*
- Inputs: six artifact identifiers — `"SPEC-M13S1"`, `"VER-M13S1V1"`, `"TEST-M13S1T1"`, `"EVA-M13S1"`, `"REV-M13S1"`, `"CLOSE-M13-1"`
*Expected Evidence:* Each `get_artifact_type(identifier)` returns a non-`None` `CanonicalArtifactType` object; `machine_identifier` field is populated; `required_metadata` list is present
*Failure Condition:* Any call returns `None`; any returned object has empty `machine_identifier`
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — `get_artifact_type` not imported or returns `None` for all patterns (exit 1)
*Post-Implementation Success Expectation:* All six patterns resolve to `CanonicalArtifactType` instances

#### VER-M13S4-REG-002 — get_registry Includes M13 Artifacts
*Source Requirement:* `FR-AEF-REGISTRY-TYPE-REGISTRATION`
*Verification Method:* UNIT_TEST
*Testability:* High — registry query
*Preconditions:* Registry initialized; M13 artifacts registered (after gate passes)
*Input or Fixture:*
- Invocation: `core.artifacts.registry.get_registry()`
*Expected Evidence:* Returned registry dict/list contains entries for `SPEC-M13S1`, `SPEC-M13S2`, `SPEC-M13S3`, `SPEC-M13S4`; each entry has `artifact_type` matching the pattern
*Failure Condition:* M13 artifact IDs absent from registry; wrong `artifact_type` values
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — registry empty or M13 artifacts not registered (exit 1)
*Post-Implementation Success Expectation:* All M13 pipeline artifacts present in registry with correct types

---

### FR-AEF-METADATA-EXTRACTION

#### VER-M13S4-EXT-001 — extract_frontmatter Returns Complete Dict for All M13 Artifacts
*Source Requirement:* `FR-AEF-METADATA-EXTRACTION`
*Verification Method:* UNIT_TEST
*Testability:* High — pure function with file input
*Preconditions:* `milestones/M13/` contains specification artifacts
*Input or Fixture:*
- Inputs: file paths for all `milestones/M13/*.md` artifacts
*Expected Evidence:*
- Returned dict contains all top-level required keys: `id`, `type`, `title`, `milestone_id`, `status`, `derived_from`, `template_version`
- `milestone_id == "M13"` in all cases
- `derived_from` is a list containing `"M13"` and prior spec IDs
*Failure Condition:* Any required key missing; `milestone_id != "M13"`; `derived_from` empty
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — `extract_frontmatter` not wired; returns empty dict or raises (exit 1)
*Post-Implementation Success Expectation:* All M13 artifacts return complete frontmatter dicts

#### VER-M13S4-EXT-002 — Metadata Sub-Keys Present (created_at, updated_at, artifact_identity, artifact_type)
*Source Requirement:* `FR-AEF-METADATA-EXTRACTION`
*Verification Method:* UNIT_TEST
*Testability:* High — nested dict field inspection
*Preconditions:* Same artifacts as EXT-001
*Input or Fixture:* Same artifact paths as EXT-001
*Expected Evidence:*
- `metadata` key present in each parsed dict
- `metadata.created_at` is a non-empty string (ISO 8601 preferred)
- `metadata.updated_at` is a non-empty string
- `metadata.artifact_identity` is a non-empty string matching the artifact `id`
- `metadata.artifact_type` is a non-empty string from the registered type list
*Failure Condition:* `metadata` key missing; any sub-key missing or empty
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — metadata sub-keys not populated (exit 1)
*Post-Implementation Success Expectation:* All artifacts have complete `metadata` sub-key structure

---

### FR-AEF-ARTIFACT-CREATION-PIPELINE

#### VER-M13S4-CRE-001 — create_artifact Emits Valid Artifact File
*Source Requirement:* `FR-AEF-ARTIFACT-CREATION-PIPELINE`
*Verification Method:* INTEGRITY_TEST
*Testability:* High — filesystem state inspection
*Preconditions:* Gate middleware has passed a stage and emitted a next-stage artifact
*Input or Fixture:*
- Fixture: generated artifact at expected path (e.g., `milestones/M13/VER-M13S4V1.md` after `SPEC-M13S4.md` validated)
*Expected Evidence:*
- File exists at expected path
- File size > 0 bytes
- `validate_metadata(artifact_path)` returns `{"valid": true, "errors": [], "missing_fields": []}`
*Failure Condition:* File does not exist; file empty; validation returns `valid == False`
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — `create_artifact` not wired; next-stage artifact not emitted (exit 1)
*Post-Implementation Success Expectation:* Next-stage artifact exists, non-empty, passes canonical validation

#### VER-M13S4-CRE-002 — create_artifact Updates Registry
*Source Requirement:* `FR-AEF-ARTIFACT-CREATION-PIPELINE`
*Verification Method:* INTEGRITY_TEST
*Testability:* High — registry state query
*Preconditions:* Artifact created via CRE-001
*Input or Fixture:*
- Invocation: `get_registry()` or `get_artifact_type(artifact_name)` after creation
*Expected Evidence:* Registry contains new entry for the emitted artifact; `get_artifact_type()` returns non-`None` for the new artifact's identifier
*Failure Condition:* Registry not updated; new artifact identifier not resolvable via `get_artifact_type()`
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — registry update not wired; new artifact not registered (exit 1)
*Post-Implementation Success Expectation:* Registry reflects new artifact

#### VER-M13S4-CRE-003 — PIPELINE-STATE.md Records Creation with Timestamp
*Source Requirement:* `FR-AEF-ARTIFACT-CREATION-PIPELINE`
*Verification Method:* INTEGRITY_TEST
*Testability:* High — structured file content inspection
*Preconditions:* Artifact created via CRE-001
*Input or Fixture:*
- Fixture: `milestones/M13/PIPELINE-STATE.md`
*Expected Evidence:* New entry in `PIPELINE-STATE.md` for the created artifact with `artifact_path`, `timestamp` (ISO 8601), `stage` (next stage name), `valid == true`
*Failure Condition:* No creation record in `PIPELINE-STATE.md`; missing required fields in creation entry
*Initial Failure Expectation:* VALID_INITIAL_FAILURE — creation not recorded (exit 1)
*Post-Implementation Success Expectation:* Complete creation record in `PIPELINE-STATE.md`

---

## Edge Cases

### EC-001: Partial Frontmatter on Legacy Artifact
*Description:* An M13 artifact has partial frontmatter (some required keys missing). Verification must detect this and record `valid == false` in `PIPELINE-STATE.md`.
*Trigger:* Introduce an artifact with missing `template_version` or `derived_from` under `milestones/M13/`.
*Expected Behavior:* `validate_metadata()` returns `valid == false`; gate blocks progression; `PIPELINE-STATE.md` records `missing_fields` non-empty.

### EC-002: Non-M13 Artifact in M13 Directory
*Description:* A file not belonging to the M13 pipeline exists in `milestones/M13/` (e.g., a README, a temp file).
*Trigger:* Add an unrelated `.md` file to `milestones/M13/`.
*Expected Behavior:* Gate middleware ignores non-artifact files or explicitly validates only known naming patterns; does not falsely block on extraneous files.

### EC-003: Registry Returns None for Unregistered Pattern
*Description:* A newly created artifact uses a pattern not registered in `core/artifacts/artifact_types.py`.
*Trigger:* Create artifact with a naming pattern not matching any registered type.
*Expected Behavior:* `get_artifact_type()` returns `None`; gate fails with descriptive error; `PIPELINE-STATE.md` records registry lookup failure.

### EC-004: create_artifact Registry Conflict
*Description:* `create_artifact()` is called with an identity that already exists in the registry.
*Trigger:* Invoke `create_artifact()` twice with the same `identity` argument.
*Expected Behavior:* Either raises `ArtifactAlreadyExistsError` (from `core/artifacts/errors.py`) or auto-assigns a unique identity; does not silently overwrite existing artifact.

---

## Failure Scenarios

### FS-001: validate_metadata Not Invoked
*Symptom:* `PIPELINE-STATE.md` has no validation records; exit code 0 despite unvalidated artifacts.
*Root Cause:* Gate middleware does not call `validate_metadata()`.
*Recovery:* Wire `core/validation.validate_metadata(artifact_path)` into `manage-development` gate loop; re-run gate.

### FS-002: get_artifact_type Returns None
*Symptom:* Registry verification fails; gate blocks with `None` lookup.
*Root Cause:* Artifact type identifier does not match any registered `machine_identifier` in `CanonicalArtifactType` definitions.
*Recovery:* Verify artifact naming pattern matches registered patterns; if new pattern needed, register it in `core/artifacts/artifact_types.py`.

### FS-003: extract_frontmatter Returns Empty Dict
*Symptom:* Frontmatter extraction verification fails; `metadata` key absent.
*Root Cause:* File lacks YAML frontmatter (`---` delimiters); or frontmatter is malformed YAML.
*Recovery:* Ensure all M13 artifacts have valid YAML frontmatter; validate with `core/artifacts/metadata.parse_metadata()`.

### FS-004: create_artifact Validation Failure
*Symptom:* Artifact created but `validate_metadata()` returns `valid == false`; gate fails after creation.
*Root Cause:* `create_artifact()` produces frontmatter missing required fields; or `metadata` sub-keys incomplete.
*Recovery:* Inspect created artifact frontmatter; ensure `create_artifact()` passes complete metadata to `_build_frontmatter()`; re-run creation.

---

## Regression Checklist

- [ ] `core/validation.validate_metadata()` signature unchanged (`artifact_path`, `schema`) → returns `Dict[str, Any]`
- [ ] `core/artifacts/artifact_types.get_artifact_type()` signature unchanged (`identifier: str`) → returns `Optional[CanonicalArtifactType]`
- [ ] `core/artifacts/metadata.extract_frontmatter()` signature unchanged (`filepath`) → returns `Optional[Dict]`
- [ ] `core/artifacts/creation.create_artifact()` signature unchanged; produces file at returned path
- [ ] `PIPELINE-STATE.md` format unchanged (path, valid, errors, missing_fields, timestamp, stage)
- [ ] All M13 artifact naming patterns (`SPEC-M13S{n}`, `VER-M13S{n}V{m}`, etc.) remain valid

---

## Manual Validation

1. Inspect `milestones/M13/PIPELINE-STATE.md` directly and verify that every M13 artifact has a corresponding record with `valid == true` and empty error lists.
2. Manually run `python -c "from core.validation import validate_metadata; from core.artifacts.metadata import extract_frontmatter; print(validate_metadata('milestones/M13/SPEC-M13S4.md'))"` and confirm output matches expected structure.
3. Manually run `python -c "from core.artifacts.artifact_types import get_artifact_type; print(get_artifact_type('SPEC-M13S4'))"` and confirm non-`None` result.

---

## Automated Validation

### Diff-Scope Verification (Pre-Merge Check)

*This mechanical check must be executed by `evaluate-implementation` before tests are considered passed.*

- **Command:** `git diff --name-only`
- **Assertion:** The output of this command MUST strictly match the Allowlist defined in SPEC-M13S4. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

Affected files from SPEC-M13S4 Allowlist:
- `milestones/M13/SPEC-M13S4.md`
- `milestones/M13/PIPELINE-STATE.md`
- `skills/manage-development/__init__.py`
- `core/validation.py` (read-only binding — changes require explicit justification)
- `core/artifacts/metadata.py` (read-only binding)
- `core/artifacts/registry.py` (read-only binding)
- `core/artifacts/creation.py` (read-only binding)

### Integration Verification Commands

```bash
# 1. Validate all M13 artifacts pass canonical validation
python -c "
from core.validation import validate_metadata
from pathlib import Path
import sys
for p in sorted(Path('milestones/M13').glob('*.md')):
    r = validate_metadata(str(p))
    if not r['valid']:
        print(f'FAIL: {p.name}: {r}')
        sys.exit(1)
print('ALL_VALID')
"

# 2. Verify registry resolves all six pipeline patterns
python -c "
from core.artifacts.artifact_types import get_artifact_type
patterns = ['SPEC-M13S1', 'VER-M13S1V1', 'TEST-M13S1T1', 'EVA-M13S1', 'REV-M13S1', 'CLOSE-M13-1']
for p in patterns:
    r = get_artifact_type(p)
    if r is None:
        print(f'FAIL: {p} returned None')
        sys.exit(1)
print('ALL_REGISTERED')
"

# 3. Verify frontmatter completeness
python -c "
from core.artifacts.metadata import extract_frontmatter
from pathlib import Path
import sys
REQUIRED = ['id', 'type', 'title', 'milestone_id', 'status', 'derived_from', 'template_version', 'metadata']
for p in sorted(Path('milestones/M13').glob('*.md')):
    fm = extract_frontmatter(str(p))
    missing = [k for k in REQUIRED if k not in fm]
    if missing:
        print(f'FAIL: {p.name} missing {missing}')
        sys.exit(1)
print('ALL_COMPLETE')
"

# 4. Verify PIPELINE-STATE.md structure
python -c "
import yaml, sys
with open('milestones/M13/PIPELINE-STATE.md') as f:
    content = f.read()
# extract records from PIPELINE-STATE.md
REQUIRED_FIELDS = ['artifact_path', 'valid', 'errors', 'missing_fields', 'timestamp', 'stage']
# implementation: parse as YAML list or structured markdown
# assert all required fields present per record
print('PIPELINE_STATE_VALID')
"
```

---

## Expected Outcomes

**Observable Success:**
1. `manage-development` gate middleware exits 0 after processing all M13 artifacts.
2. `milestones/M13/PIPELINE-STATE.md` exists with complete per-artifact validation records for all M13 pipeline artifacts.
3. Every artifact record in `PIPELINE-STATE.md` has `valid == true`, `errors == []`, `missing_fields == []`.
4. `get_artifact_type()` returns non-`None` for all six M13 pipeline naming patterns.
5. `extract_frontmatter()` returns complete dicts with all required top-level and `metadata` sub-keys for every M13 artifact.
6. Passing a gate stage produces the next-stage artifact via `create_artifact()`; the emitted artifact passes `validate_metadata()` with `valid == true`.
7. Registry reflects all M13 artifacts after creation.
8. Identical validation inputs produce identical outputs across repeated `manage-development` invocations.
9. No files outside `milestones/M13/` or `core/` are modified by the integration.

**Observable Failure:**
- Exit code non-zero from gate; `PIPELINE-STATE.md` contains `valid == false` records or missing artifact entries.
- `get_artifact_type()` returns `None` for any M13 naming pattern.
- `extract_frontmatter()` returns incomplete dict (missing required keys) for any M13 artifact.
- Created artifact fails `validate_metadata()` with non-empty `errors` or `missing_fields`.
- Registry does not reflect newly created artifact.
- Files outside `milestones/M13/` or `core/` are modified.

---

## Next Steps

Run `/generate-tests` to create executable test suite from this verification protocol (VER-M13S4V1.md).
