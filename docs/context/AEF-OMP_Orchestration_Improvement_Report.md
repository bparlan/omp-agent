# AEF-OMP Orchestration Improvement Report

## 1. Structural & Orchestration Fixes

### 1.1. Test Directory Isolation (FR-TEST_FOLDERING)
**Problem:** Tests for multiple specification sequences ($S_Y$) are currently stacked in `tests/M{X}/`, leading to namespace collisions and confusion during evaluation.
**Proposed Fix:** Mandate `tests/M{X}/S{Y}/` as the canonical test directory in `generate-tests` and `evaluate-tests`.

### 1.2. Interactive Selection Gates (`ask` Tool)
**Problem:** Skills conclude with static text instructions (e.g., "Next Step: run /evaluate-tests"). This relies on the user to remember and type the next command correctly.
**Proposed Fix:** Replace trailing prose with interactive `ask` prompts that suggest the next logical SDD step as a pre-written selection.

### 1.3. Artifact Validation & Completion Reports
**Problem:** `implement-specification` often fails to generate or validate the `M{X}S{Y}C.md` completion report, leading to "ghost implementations" where code is written but the framework cannot verify the state.
**Proposed Fix:**
- Add a mandatory **"Completion Report Verification"** step to `implement-specification`.
- The skill MUST NOT conclude until `M{X}S{Y}C.md` is physically on disk and valid.

## 2. SDD Pipeline Optimization

### 2.1. `evaluate-tests` (Phase 1) Criticality
**Problem:** Pre-implementation evaluations are sometimes too lenient, missing "False-Pass" leaks where a test passes against non-existent code (e.g., due to circular mocking or incorrect grepping).
**Proposed Fix:**
- **Zero-Pass Mandate:** Any `IMPLEMENTATION_CHECK` or `INTEGRATION_CHECK` that passes on a blank codebase triggers an immediate `INVALID_TEST` (Status: `TDD_LEAK`).
- **Problem Report Artifact:** On failure, generate a `FIX-VERIFICATION-M{X}S{Y}.md` report that maps exactly what needs to be repaired in the verification or test generation.

### 2.2. Deterministic Tool Usage (`todo`, `task`, `hub`)
**Problem:** Complex implementation tasks often lose track of state during long turns.
**Proposed Fix:**
- Use `todo` to initialize the implementation checklist from the spec.
- Use `task` to parallelize independent module implementations.
- Use `hub` to coordinate between sub-agents if a task is split.
