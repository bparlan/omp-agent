---
id: TEST-000
type: test_set
title: Template Test Set
milestone_id: M0
status: draft
derived_from: []
template_version: 1.1.0
---

## Validity Metadata

- **Subject under test:** <exact file path, module name, or function name>
- **Validity acceptance criteria:** <how is "exercised the subject" determined?>
- **Expected failure conditions:** <what would a valid failure look like?>
- **Environment prerequisites:** <tools, files, state required for validity>

---

#### Test Environment

- **Testing Framework:** (e.g., Pytest, Jest, Playwright)
- **Setup Requirements:** (e.g., Environment variables, mock databases needed)

---

#### Output Format Constraints

**Language-Specific Requirements:**

1. **Bash Scripts (`.sh`)**:
   - Use bash function syntax: `function test_name() { ... }`
   - Use bash variables: `TESTS_RUN++`, `TESTS_PASS++`, `TESTS_FAIL++`
   - Use bash exit codes: `exit 0` for success, `exit 1` for failure
   - Include valid shebang: `#!/bin/bash` or `#!/usr/bin/env bash`

2. **Python Scripts (`.py`)**:
   - Use Python function syntax: `def test_name():`
   - Use pytest fixtures and assertions
   - Use proper imports: `from ... import ...`
   - Include `if __name__ == "__main__":` guard for standalone execution

**Mock Code Rules:**

1. **Separation**: Mock objects and test utilities MUST be defined in separate files or bash functions. They CANNOT be embedded as raw Python class definitions in bash files.
2. **Language Consistency**: Mock code must follow the same language as the test script:
   - Bash scripts: Mock objects must be bash functions (`function mock_name() { ... }`)
   - Python scripts: Mock objects must be Python classes/functions (`class Mock:`, `def mock_func():`)
3. **Execution**: All test scripts MUST be executable (bash) or importable (Python) before marking the test plan as complete.

**Language Extension Consistency:**

- File extension MUST match language of syntax:
  - `.sh` files MUST use bash syntax only (no Python classes/methods)
  - `.py` files MUST use Python syntax only (no bash functions or commands)

**Example:**

**Invalid (Bash file with Python syntax):**

```bash
#!/bin/bash
# WRONG: Python class in bash file
class Mock:
    def __init__(self):
        pass
```

**Valid (Bash file with bash syntax):**

```bash
#!/bin/bash
# CORRECT: Bash function for mock
function mock_function() {
    return 0
}

function test_example() {
    TESTS_RUN++
    if mock_function; then
        TESTS_PASS++
    else
        TESTS_FAIL++
    fi
    exit 0
}
```

---

#### Executable Scripts Generated

_(List the actual code scripts generated and saved to the `tests/M{X}/` directory)_

- `tests/M{X}/...` - Description of what this script executes.

---

#### Expected Coverage

_(Map the generated scripts back to the Verification Protocol)_

- **Functional Validation:** ...
- **Edge Cases Covered:** ...
- **Failure Scenarios Covered:** ...

---

#### Execution Instructions

_(Exact bash commands required for the `evaluate-implementation` agent to run these tests)_

- `...`
