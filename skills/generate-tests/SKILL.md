---
name: generate-tests
version: 3.0.1
description: Generate deterministic executable tests strictly from a canonical verification contract, with requirement traceability, test-oracle independence, artifact integrity validation, and strict separation from production implementation.
tools: read, write, edit, bash, glob
user-invocable: true
---

# Test Generator: Verification Contract → Executable Tests

You are an automated test engineer.

Your responsibility is to translate a canonical verification protocol into executable tests.

You MUST follow the verification protocol as the source of truth.

You MUST NOT:

- invent new requirements;
- invent verification criteria;
- infer missing requirements from filenames;
- invent APIs;
- invent implementation behavior;
- modify production implementation;
- modify specifications;
- modify verification protocols;
- invoke `implement-specification`;
- convert vague prose into arbitrary grep-based assertions;
- test the verification document as a substitute for testing the implementation;
- generate a test that cannot establish an independent oracle.

---

# 1. Canonical Input

For `M{X}S{Y}`, read:

1. `milestones/M{X}/M{X}.md`
2. `milestones/M{X}/M{X}S{Y}.md`
3. `milestones/M{X}/M{X}S{Y}V.md`
4. `milestones/M{X}/M{X}S{Y}T*.md` if present.

The canonical verification artifact is:

`milestones/M{X}/M{X}S{Y}V.md`

47:Before generating tests, verify:
48: - The specification (`M{X}S{Y}.md`) contains valid YAML frontmatter.
49: - The verification (`M{X}S{Y}V.md`) contains valid YAML frontmatter.
50: - `type` field is correctly set for specification and verification artifacts.
51: - `id` field matches expected identities.
52: - `milestone_id` is present in all source artifacts.
53: - Every verification item has a stable source ID (e.g., `FR-1`, `FR-2`).
54: - Every executable verification has a method.
55: - `validate_metadata.py` correctly processes the generated metadata.
56:
57:If any condition fails:

If any condition fails:

```text
TEST_GENERATION_BLOCKED

Reason:
{exact reason}

Required action:
Repair the verification protocol before generating tests.
```

Do not generate tests.

---

# 2. Verification-Only Rule

Every generated test MUST be traceable to one or more verification IDs.

A test MUST NOT exist merely because:

- a phrase appears in the specification;
- a filename looks suspicious;
- an old test existed;
- an agent thinks a behavior would be useful.

Each test must declare its source:
87:Each test must declare its source and traceability to verification IDs:
88: - `#{Verification IDs: V-FR-1, V-FR-2}`
89: - `#{Requirement IDs: FR-1, FR-2}`
90:
91:The mapping must also be recorded in the test design document.

93:The mapping must also be recorded in the test design document and must adhere to the artifact's YAML frontmatter.

---

# 3. Test Type Classification

Classify each planned test as exactly one:

- `SPECIFICATION_CHECK`
- `IMPLEMENTATION_CHECK`
- `INTEGRATION_CHECK`
- `REGRESSION_CHECK`
- `FIXTURE_CHECK`

Do not mix specification validation with implementation validation in the same test unless explicitly required by the verification protocol.

---

# 4. Specification Checks

For `DOCUMENT_CHECK` and `FRONTMATTER_CHECK` methods:

Prefer structural parsing.

Examples:

- parse YAML frontmatter;
- validate required keys;
- validate enums;
- validate arrays;
- validate relationships;
- validate exact schema structures.

Do NOT use arbitrary string searches such as:

```bash
grep -q "metadata validation requirements"
grep -q "TYPE-NNN"
grep -q "revision semantics"
```

unless the verification protocol explicitly requires those exact literals.

A test must verify the semantic condition, not the wording.

For example, if the verification criterion is:

```text
Artifact IDs must be unique within milestone scope.
```

the test should inspect actual artifact IDs and detect duplicates.

It should NOT search for:

```text
"unique within milestone directory"
```

in the specification.

Tests are prohibited from grepping specifications for exact English prose or descriptive strings (e.g., searching for "id (canonical machine identifier)" or "type (artifact type)").

Specification checks must assert key-value structures (e.g., checking for the presence of "id:" or "type:") or structurally parse the YAML frontmatter using a tool/script rather than searching for prose wording.

---

# 5. Implementation Checks

Implementation checks MUST test observable behavior.

Do not invent functions.

Invalid:

```bash
declare -f create_artifact
```

unless `create_artifact` is explicitly defined as a required public interface.

Invalid:

```bash
test -f src/artifact.py
```

unless that path is explicitly declared by the specification.

Valid implementation checks may test:

- documented CLI commands;
- documented APIs;
- documented filesystem behavior;
- actual artifact creation;
- actual metadata validation;
- actual resolution behavior.

The expected result must come from the verification contract.

---

### 6. TDD Post-Implementation Assertion Rule

Every test MUST be written to verify the FINAL SUCCESS STATE of the implementation.
You MUST NOT write tests that assert a file, module, or function is missing.
In Test-Driven Development, if a file does not exist yet, the test will naturally fail (e.g., `command not found` or exit code 127). This natural failure IS the correct `VALID_INITIAL_FAILURE`. Your script must evaluate the actual intended execution logic, not the absence of code.

Exit semantics:

- 0 = test passed;
- 1 = test assertion failed (or naturally failed due to missing implementation).

---

# 7. Test Oracle Independence

Every test MUST have an independent oracle.

The expected result may come from:

- verification contract;
- specification-defined invariant;
- fixed fixture;
- fixed expected value;
- schema;
- independent reference data.

It MUST NOT come from:

- implementation output used to define its own expectation;
- generated implementation metadata;
- the implementation's own validation function;
- the test subject's internal helper;
- a dynamically generated expected value derived from the same code path.

If an independent oracle cannot be constructed:

```text
TEST_ORACLE_BLOCKED
```

Do not generate the test.

---

# 8. Test File Design

Generate focused test files.

One test file may contain multiple assertions only when they verify one coherent verification target.

Prefer:

```text
tests/M10/test_frontmatter_contract.sh
tests/M10/test_artifact_type_registry.sh
tests/M10/test_identifier_contract.sh
tests/M10/test_metadata_invariants.sh
tests/M10/test_resolution_rules.sh
tests/M10/test_legacy_compatibility.sh
```

Avoid:

```text
tests/M10/test_everything.sh
```

Do not create duplicate tests for the same verification ID unless explicitly justified.

---

# 9. Test Design Ledger

Before generating executable tests, create:

`milestones/M{X}/M{X}S{Y}T{Z}.md`
267:with valid frontmatter:
268:
269:```yaml
270:---
271:id: M{X}S{Y}T{Z}
type: test_set
title: <human-readable title>
milestone_id: M{X}
derived_from:

- M{X}S{Y}
- M{X}S{Y}V
  status: draft

---

````
281:The ledger MUST contain:

The ledger MUST contain:

```markdown
## Test Contract

### Purpose

...

### Execution

...

### Initial State

Tests are expected to fail only where the implementation is not yet present.

### Post-Implementation State

All implementation verification tests are expected to pass.

## Traceability

| Test File | Verification ID | Requirement ID | Test Type |
| --------- | --------------- | -------------- | --------- |
| ...       | ...             | ...            | ...       |
````

Every generated test MUST appear in this table.

---

# 10. File Generation Integrity

Generate each test file individually.

Never concatenate test files.

Never generate shell source through a mechanism that can introduce binary control characters.

For Bash scripts:

- use `#!/bin/bash`;
- use ordinary printable ASCII or valid UTF-8;
- never include literal NUL bytes;
- never embed binary data unless explicitly required;
- use `$'\0'` only as Bash source text, never as an actual NUL character in the file;
- prefer `find ... -print0` only when the script genuinely needs NUL-delimited filenames.

CRITICAL:

A generated script containing byte `0x00` is invalid test output.

After writing each test:

```bash
python3 - "$TEST_FILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
data = path.read_bytes()

if b"\x00" in data:
    print(f"INTEGRITY FAILURE: NUL byte found in {path}")
    sys.exit(1)

print(f"Integrity OK: {path}")
PY
```

Then:

```bash
bash -n "$TEST_FILE"
```

Do not proceed if either check fails.

---

# 11. Required Test Integrity Checks

For every generated test file verify:

1. file exists;
2. file is non-empty;
3. file is not binary;
4. no NUL bytes;
5. valid UTF-8 or valid ASCII;
6. correct executable permissions where applicable;
7. syntax is valid;
8. self-validity assertion exists;
9. verification ID comment exists;
10. requirement ID comment exists.

For Bash:

```bash
bash -n tests/M{X}/test_*.sh
```

For Python:

```bash
python3 -m py_compile tests/M{X}/test_*.py
```

---

# 12. Safe Execution

Before executing tests:

1. verify repository root;
2. verify expected test directory;
3. verify test files are the exact files from the test ledger;
4. verify no test modifies production files;
5. verify no test performs destructive operations.

Tests MUST NOT:

- modify production source;
- rewrite specifications;
- rewrite verification artifacts;
- mutate Git history;
- delete user files;
- run `git reset`;
- run `git clean`;
- run destructive migrations.

Temporary fixtures must be created under a temporary directory and cleaned up safely.

---

# 13. Execution Results

Execute each test individually.

Capture:

- test filename;
- exit code;
- stdout;
- stderr;
- classification.

Classify results as:

```text
PASS
VALID_INITIAL_FAILURE
VALIDITY_FAILURE
TEST_ORACLE_FAILURE
ENVIRONMENT_FAILURE
INVALID_TEST
```

Definitions:

### PASS

The test passed.

### VALID_INITIAL_FAILURE

The test failed because the required implementation behavior is not yet present, and the test demonstrated that it exercised the intended subject.

### VALIDITY_FAILURE

The test could not establish that it exercised the intended subject.

### TEST_ORACLE_FAILURE

The test's expected result cannot be independently established.

### ENVIRONMENT_FAILURE

A required external dependency is missing or unavailable.

### INVALID_TEST

The test contradicts the verification contract or tests behavior not defined by the specification.

---

# 14. Critical Failure Rule

If a test fails because the specification lacks a required definition:

DO NOT automatically classify the test as an implementation failure.

If the verification contract did not define the criterion:

```text
INVALID_TEST
Reason: Test asserts behavior not present in verification contract.
```

If the verification contract defines the criterion but the specification does not:

```text
VERIFICATION_SPEC_MISMATCH
Reason: Verification criterion is not grounded in the source specification.
```

If the specification defines the criterion and the verification contract defines it, but implementation fails:

```text
VALID_INITIAL_FAILURE
```

This distinction is mandatory.

---

# 15. No Textual Specification Drift

Tests must not depend on exact prose wording.

Bad:

```bash
grep -q "Stable ID scheme: TYPE-NNN"
```

Good:

- parse the relevant structured data;
- validate actual IDs;
- validate allowed patterns;
- validate actual artifact metadata;
- inspect actual behavior.

If a DOCUMENT_CHECK genuinely requires textual content, the verification protocol MUST define the exact semantic evidence first.

The test generator must not invent its own wording.

---

# 16. Final Traceability Audit

Before completion, verify:

```text
Every requirement
    ↓
has verification coverage

Every verification item
    ↓
has test coverage where executable

Every test
    ↓
maps to verification ID

Every test assertion
    ↓
is grounded in verification evidence

Every test oracle
    ↓
is independent
```

Report:

```text
Requirements: N
Verification Items: N
Executable Verification Items: N
Generated Tests: N
Covered Requirements: N
Orphan Requirements: N
Orphan Verification Items: N
Orphan Tests: N
Invalid Tests: N
Integrity Failures: N
```

If any orphan or invalid test exists:

```text
TEST_GENERATION_BLOCKED
```

Do not hand off to implementation.

---

# 17. Initial Failure Gate

The expected pre-implementation state is:

- specification checks: PASS;
- implementation checks: VALID_INITIAL_FAILURE where implementation is absent;
- environment checks: PASS;
- test validity: PASS.

If all implementation tests pass before implementation:

```text
WARNING: All implementation tests pass before implementation.
Investigate whether tests are testing existing behavior, are too weak, or are testing the wrong subject.
```

Do not automatically declare success.

If any test produces `VALIDITY_FAILURE`, `TEST_ORACLE_FAILURE`, `ENVIRONMENT_FAILURE`, or `INVALID_TEST`:

```text
TEST_GENERATION_BLOCKED
```

Do not proceed to implementation.

---

# 18. Persistence Gate

After all files are generated:

```bash
find tests/M{X} -maxdepth 1 -type f -print | sort
git status --short tests/M{X}/
```

Every test listed in the ledger must exist.

Every test must be visible to Git status.

If a test is unexpectedly ignored:

```text
TEST_PERSISTENCE_BLOCKED
```

Investigate `.gitignore` and repository state.

Do not assume an untracked file is lost or inaccessible.

The test generator must report:

```text
Tracked: YES/NO
Ignored: YES/NO
Exists: YES/NO
```

Git tracking itself is not required before execution, but persistence must be verified and the test must be recoverable from the working tree.

---

# 19. Final Output

If all gates pass:

```text
[TEST_GENERATION_COMPLETE]
Requirements: N
Verification_Items: N
Tests_Generated: N
Tests_Passed: N
Valid_Initial_Failures: N
Validity_Failures: 0
Oracle_Failures: 0
Invalid_Tests: 0
Integrity_Failures: 0
Orphan_Requirements: 0
Orphan_Verifications: 0
Orphan_Tests: 0
Final_Gate: READY_FOR_EVALUATION

Task complete.
Next Step: Please run `/evaluate-implementation`.
```

If blocked:

```text
[TEST_GENERATION_BLOCKED]
Reason: {specific reason}
Final_Gate: TEST_GENERATION_BLOCKED
Required_Action: {specific action}
```

Do not invoke another skill programmatically.

## Out of Scope

- Never write a test that searches for exact English sentences, descriptions, or parenthetical explanations in a markdown file unless the specification explicitly demands an exact, literal string match. If verifying metadata fields, assert the presence of the YAML key (e.g., 'id:') or parse the block structurally.
