# OMP Milestone 10: Multi-Spec Strategic Planning Blueprint (S7–S10)

This blueprint details the concrete objectives, interface contracts, and implementation architectures for the remaining four sequences under Milestone 10 (`M10.md`), providing the system with a clear development track to complete the project-agnostic SDD assembly line.

---

## **Sequence 1: M10S7 — Safe-to-Proceed Implementation Gate**

### **1. Objective & Value Proposition**
Prevent the implementation agent (`implement-specification`) from starting code modifications or guessing baseline test states if upstream gates are incomplete, red, or missing human approval. S7 introduces a mechanical pre-flight verification step that blocks the agent from touching a single line of code until approval is explicitly verified and baseline tests are in a verified TDD state.

### **2. Interface Contract & CLI Signature**
*   **Target binary:** `bin/omp-verify-readiness` (Python utility)
*   **CLI signature:**
    ```bash
    bin/omp-verify-readiness --spec milestones/M10/M10S7.md --test-dir tests/M10/
    ```
*   **Expected Exit Codes:**
    *   `0 (PASS)`: The specification has a valid user approval stamp AND all tests are in a healthy `VALID_INITIAL_FAILURE` or `SPECIFICATION_CHECK` pass state.
    *   `1 (BLOCKED)`: The user approval stamp is missing or the tests contain uncompiled/syntax-broken code (invalid state).
    *   `2 (VALIDITY_FAILURE)`: Missing specification file, missing test plan ledger, or incorrect path arguments.

### **3. Schema Verification (#### User Approval)**
The readiness verifier must extract YAML frontmatter from the target spec and confirm:
1. The specification has been approved by checking for the exact block at the bottom of the file:
   ```markdown
   #### User Approval
   * [x] Approved for implementation by user
   ```
2. If the user approval stamp is absent, the script writes `BLOCKED: Specification lacks human approval` to stderr and exits with `1`.

### **4. Files Permitted to Change (Allowlist)**
*   `bin/omp-verify-readiness`
*   `skills/implement-specification/SKILL.md` (Update process to run `omp-verify-readiness` first)
*   `milestones/M10/M10S7.md` (The specification file)

---

## **Sequence 2: M10S8 — Failure Classification & Diagnostic Contract**

### **1. Objective & Value Proposition**
Prevent cascading test errors from obscuring the root cause of execution failures. When a root-level dependency or compiler syntax error occurs during a test sweep, S8 mandates that the test execution engine immediately terminates execution, suppresses downstream trace noise, and outputs a high-fidelity diagnostic block.

### **2. Interface Contract & Execution Rules**
*   **Component modified:** `bin/omp-test` (and strategy adapters)
*   **The Termination Rule:** When executing tests, if the runner detects a syntax compiler failure (non-zero compilation check) or a critical system crash (such as missing files or timeout), it must:
    1. Immediately halt further test script execution.
    2. Suppress natural-language python tracebacks on stdout.
    3. Output a structured, single-line diagnostic summary to stderr matching:
       `CRITICAL_FAILURE: <failing_file> | <error_class> | <error_line>`
    4. Set overall metrics output with `EXIT_CODE=2` (VALIDITY_FAILURE).
*   **Diagnostic Logs:**
    *   The complete, multi-line error dump is written to `/workspace/scratch/omp_test_critical.log` for developer auditing, keeping the terminal output clean and bounded.

### **3. Files Permitted to Change (Allowlist)**
*   `bin/omp-test`
*   `agent/core/testing/execution_strategies.py`
*   `milestones/M10/M10S8.md` (The specification file)

---

## **Sequence 3: M10S9 — Artifact Persistence & Git Integrity Contract**

### **1. Objective & Value Proposition**
Eliminate the "false-progress trap" where agents generate test files and complete milestone reports but fail to commit or track them in the workspace index. S9 establishes a post-generation Git integrity gate, ensuring that all newly created specifications, verification protocols, test plans, and test scripts are actively registered in the repository's working tree.

### **2. Interface Contract & Git Integrity Gate**
*   **Target binary:** `bin/omp-verify-git-integrity` (POSIX shell script)
*   **CLI signature:**
    ```bash
    bin/omp-verify-git-integrity --milestone M10 --spec S9
    ```
*   **Execution Logic:**
    1. Executes `git status --short` to inspect the workspace.
    2. Identifies all generated files for the sequence (e.g., `milestones/M10/M10S9*.md` and `tests/M10/`).
    3. Verifies that no generated files are marked as ignored (`git check-ignore`).
    4. If any newly created test file is untracked (shows as `??` in status) or uncommitted, it automatically adds them to the Git staging index (`git add`).
    5. If any required file is missing or untracked and cannot be added, it logs `GIT_INTEGRITY_FAILURE` to stderr and exits with `1`.
*   **Exit Codes:**
    *   `0`: All artifacts exist, are non-empty, and are actively staged/tracked in the Git repository index.
    *   `1`: Git tracking failure or untracked files cannot be resolved.

### **3. Files Permitted to Change (Allowlist)**
*   `bin/omp-verify-git-integrity`
*   `skills/generate-tests/SKILL.md` (Update persistence step)
*   `milestones/M10/M10S9.md` (The specification file)

---

## **Sequence 4: M10S10 — Multi-Project Compatibility & Migration Contract**

### **1. Objective & Value Proposition**
Support backward compatibility with legacy OMP/AEF repositories. The metadata validator must be able to operate in multi-project environments without breaking or silently mutating older historical documents that lack YAML frontmatter.

### **2. Interface Contract & Compatibility Layer**
*   **Component modified:** `bin/omp-verify-metadata` (Python metadata extraction utility)
*   **The Compatibility Layer Rule:**
    *   When called on an artifact path, the verifier must first scan for a frontmatter block.
    *   If the file contains no frontmatter and is located under a designated legacy folder (e.g., `milestones/archive/` or older directories), the tool must bypass schema enforcement and report the file as `LEGACY_COMPATIBLE` (returning exit code `0`) instead of crashing or exiting with code `1`.
    *   If a newly generated file (located in active `milestones/M10/` or `tests/`) lacks valid frontmatter, it is strictly rejected with exit code `1`.
*   **Legacy Allowlist:**
    *   The tool reads a local JSON configuration `.omp/legacy_exclusions.json` listing historic files that are exempt from frontmatter validation.

### **3. Files Permitted to Change (Allowlist)**
*   `bin/omp-verify-metadata`
*   `milestones/M10/M10S10.md` (The specification file)
