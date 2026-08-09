---
id: VER-M10S4V
type: verification
milestone_id: "M10"
derived_from:
  - M10
  - SPEC-M10S4
status: draft
---

# Verification Protocol for Test Ledger Verification Tool Specification (SPEC-M10S4)

## Verification Items

### V-FR-3: Failure Exit Code Verification

*   **Source Requirement:** FR-3
*   **Verification Method:** SCRIPT_EXECUTION
*   **Target:**  CLI tool execution.
*   **Precondition:** A test ledger file that is malformed or references missing files/IDs exists.
*   **Command:** Validating ledger: tests/fixtures/M10/synthetic_ledger_invalid/ledger.md, verification: tests/fixtures/M10/synthetic_ledger_invalid/verification.md, test_dir: tests/fixtures/M10/synthetic_ledger_invalid/tests/
*   **Expected Evidence:** The command exits with status code .
