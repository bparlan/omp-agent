---
id: CONTEXT-AUDIT-1
type: specification
title: "OMP/AEF Infrastructure Context Audit & General Checkup Blueprint"
milestone_id: M10
status: completed
derived_from: [M10, SPEC-M10S10, EVAL-1, TEVAL-1]
---

# OMP/AEF Infrastructure Context Audit & General Checkup Blueprint

This context report compiles all the technical "hickups," structural deadlocks, and validation collisions encountered during the implementation and execution of **Milestone 10, Sequence 10 (Multi-Project Compatibility & Migration Contract)**.

Use this document to prime any advanced LLM (such as Claude) with the necessary technical history and provide concrete, copy-paste prompts to execute a **Unified System Checkup** across the OMP Agentic Engineering Framework (AEF).

---

## 1. Executive Summary of the Pipeline Blockades
During the transition from test generation to final review in Sequence 10, the "fail-closed" mechanics of the Spec-Driven Development (SDD) pipeline triggered repeated halts. While these gates successfully protected the codebase from broken builds, they revealed several **prompt-driven contradictions** where one agent's output strictly violated another agent's validation parser.

Because agents operate under a **Strict Test Isolation Guardrail**, they are forbidden from modifying files outside their immediate allowlists during active execution turns. When a contradiction occurred, the pipeline deadlocked—requiring manual file edits or filename overrides.

---

## 2. Comprehensive Failure Analysis (The 7 Core "Hickups")

### Issue A: The YAML Anchor Scanner Collision (`ScannerError`)
*   **The Cause:** In PyYAML (and safe loaders), special characters like `&` and `:` are reserved control operators used for defining anchors or maps. When the Spec Generator (`generate-spec`) or Verification Generator (`generate-verification`) produced titles with unquoted special characters (e.g., `title: Multi-Project Compatibility & Migration Contract`), PyYAML crashed on execution with a `ScannerError`.
*   **The Impact:** The validation check (`validate_metadata.py`) would fail silently or crash with a traceback, locking the precondition gates and preventing test execution.
*   **The Cure:** Pre-process the frontmatter strings inside the parsing utility, or enforce strict double-quoting rules on all text values in templates.

### Issue B: The Shebang-Comment Header Collision (Line 1 Constraint)
*   **The Cause:** The `generate-tests` skill (Section 4) strictly mandated that *every* test file must start with `# {Verification IDs: ...}` comments on Line 1. However, the `evaluate-tests` linter (Section 2) mandated that all executable Python scripts must contain a valid shebang line (`#!/usr/bin/env python3`) on **line 1** to prevent interpreter mismatches.
*   **The Impact:** The test generator placed metadata comments on Line 1 and shifted the shebang to Line 2. The linter flagged the Python test script as `INVALID_TEST` (missing shebang on Line 1) and locked the precheck gate.
*   **The Cure:** Update the generator's instructions to place the language-appropriate shebang on Line 1 (`#!/bin/bash` or `#!/usr/bin/env python3`) and the traceability metadata on subsequent lines.

### Issue C: Passive Deletion on Spacing / Indentation Errors
*   **The Cause:** When the test generator ran `py_compile` on its generated Python scripts and encountered a minor indentation typo (caused by Markdown code-fence nesting), its instructions told it to **"delete the file and halt"**.
*   **The Impact:** Instead of adjusting the whitespace and fixing the syntax, the agent deleted its own test files and threw a blocked pipeline exception, forcing the user to rewrite tests by hand.
*   **The Cure:** Upgrade the test-generator's instructions from a passive gatekeeper to an active **Self-Healing Compiler** that reads the traceback, edits the file, and retries up to 3 times.

### Issue D: The "False-Green" Paradox (TDD Leak on Brownfield)
*   **The Cause:** The pre-implementation test linter (`evaluate-tests`) has a strict safety rule: if an active code test (`IMPLEMENTATION_CHECK`) passes with exit code `0` *before* coding begins, it assumes the test is a "false-pass leak" (due to a circular mock or empty assertion) and locks the pipeline.
*   **The Impact:** When executing on a **brownfield codebase** (where the validator/binary was already pre-written and functional on disk), the tests naturally passed. The linter incorrectly flagged this success as a security leak, blocking implementation.
*   **The Cure:** Introduce a `VALID_BROWNFIELD_PASS` exception that checks if the implementation binary is already present and functional on disk.

### Issue E: Stale "Ghost" Entries in the Test Ledger (`M10S10T1.md`)
*   **The Cause:** When test files were deleted, renamed, or converted (e.g., from `.sh` to `.py`), the outdated paths remained in the ledger's markdown table because the generator lacked a strict **Over-write/Truncation** rule.
*   **The Impact:** The precheck auditor parsed the ledger, saw a file that no longer existed on disk (like `test_legacy_handling.sh`), and triggered an immediate `INVALID_TEST` halt.
*   **The Cure:** Mandate that `generate-tests` completely overwrites or truncates the ledger file at initialization, mapping only successfully written test files.

### Issue F: Positional Arguments vs. Flag Option (`--spec`) Mismatches
*   **The Cause:** In Milestone 10, Sequence 2 (`M10S2`), the `bin/omp-verify-metadata` contract was strictly defined to accept *positional* file arguments only (e.g., `bin/omp-verify-metadata file1 file2`). However, other system-level skills (like `M10S7` and `evaluate-implementation`) invoke the validation suite using explicit option flags (e.g., `--spec file1 --verification file2`).
*   **The Impact:** The delegate script `validate_metadata.py` forwarded `sys.argv[1:]` (including the `--spec` and `--verification` flags) directly to the binary, which crashed with an `unrecognized arguments` error.
*   **The Cure:** Implement transparent argument filtering in the delegate wrapper to strip out double-dash options and pass only positional paths.

### Issue G: Wording-Based Metadata Schema Inconsistencies
*   **The Cause:** Skill instructions and templates defined contradictory types for transition reports (e.g., `type: completion_report` or `type: test_evaluation`), while the validator strictly enforced single-word enums (`completion`, `evaluation`).
*   **The Impact:** The metadata validator failed-closed, throwing an exit-code 1 error during the final review phase.
*   **The Cure:** Standardize all schema definitions and templates to use strictly canonical types.

---

## 3. General Checkup Prompts for Claude / OMP

To run a general system health-check and permanently apply these self-healing capabilities across your AEF project, run these **three sequential prompts** in your active OMP developer chat:

### Prompt 1: Overhaul the Test Generator (`generate-tests`)
```text
/edit skills/generate-tests/SKILL.md

Please apply these structural updates to the "generate-tests" skill:

1. Under "Section 3. Test Plan Ledger Generation Precedence (FR-1, FR-2)", add:
"Ledger Truncation Rule (CRITICAL): When initializing the test plan ledger file, you MUST completely overwrite or truncate any existing file at that path. You are strictly prohibited from appending to or merging with an existing ledger file. This ensures that any obsolete or renamed test mappings from prior runs are completely purged, eliminating ghost entries."

2. Under "Section 4. Verification-Only & Traceability Rules", SWAP the "Traceability Comment Headers" block:
"Traceability Comment Headers: Every executable test script MUST begin with a valid language-specific shebang followed immediately by metadata comments.
* For Bash scripts (.sh), line 1 MUST be:
#!/bin/bash
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-Y}
# Test Type: IMPLEMENTATION_CHECK

* For Python scripts (.py), line 1 MUST be:
#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-Y}
# Test Type: IMPLEMENTATION_CHECK"

3. Under "Section 5. Test Strategy & Syntax Validation", SWAP the "Syntax Check Postcondition" block:
"Self-Healing Syntax Compiler Check (CRITICAL): Immediately after writing a test script, run a syntax compiler check matching the language. If the check fails with an IndentationError or SyntaxError:
1. Do NOT delete the file or halt.
2. Read the compiler's error output to identify the exact line number.
3. Use your edit tool to correct the spacing or syntax in the file.
4. Re-run the syntax compiler check.
You are authorized to execute this self-healing loop up to 3 times per file. If compilation still fails, delete the file, halt, and report the validation error."
```

### Prompt 2: Upgrade the Pre-Implementation Auditor (`evaluate-tests`)
```text
/edit skills/evaluate-tests/SKILL.md

Please apply these structural updates to the "evaluate-tests" skill:

1. Under "Section 1. Preconditions & Schema Integrity (MANDATORY)", update Step 2 (Verify File Integrity):
    *   Ensure the script contains **zero literal NUL bytes (`0x00`)**.
    *   Ensure the script has a valid shebang line on line 1 (e.g., `#!/bin/bash` or `#!/usr/bin/env python3`).
    *   Ensure there are **no pre-flight binary existence traps** (e.g., checking if `bin/omp-test` exists on disk). If a trap is present, classify the test as `INVALID_TEST` immediately.

2. Under "Section 4. Generate the Test Evaluation Report (TEVAL-{N})", add:
"Deterministic Path Resolution: When writing the Test Evaluation Report, you MUST programmatically resolve all wildcards (M{X}, S{Y}, T{Z}) by scanning the milestones/ directory on disk. You are strictly prohibited from guessing or writing question marks (?) in the frontmatter or path fields (e.g. resolve SPEC-? to SPEC-M10S10, and TSET-? to TSET-M10S10T1)."
```

### Prompt 3: Align the Transition Templates
```text
/edit templates/test-evaluation_template.md

Please update the hardcoded type field to use the canonical "evaluation" value:

SWAP.BLK
---
id: TEVAL-0
type: test_evaluation
title: Template Test Evaluation Report
=======
---
id: TEVAL-0
type: evaluation
title: Template Test Evaluation Report
```

---

## 4. The General Checkup and Verification Protocol
After Claude finishes editing the skill files, execute this command suite to clean the workspace and verify that the precheck compiler runs completely hands-free:

```bash
# 1. Clean up any historical "ghost" test scripts
rm -rf tests/M10/*

# 2. Re-run the updated generator
/generate-tests M10S10

# 3. Audit your baseline state
/evaluate-tests M10S10
```

*Expected Successful Outcome:*
The test generator will write shebang-compliant, 4-space indented Python Pytest scripts, initialize a truncated ledger `M10S10T1.md`, and compile perfectly. The auditor will successfully validate the metadata using flag-immune positional mappings, report a healthy `VALID_BROWNFIELD_PASS` (or natural `VALID_INITIAL_FAILURE` if code is cleared), and advance the pipeline to the implementation stage with **zero manual interventions required**!
