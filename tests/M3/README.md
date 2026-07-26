# M3S1 Test Suite

Test suite for M3S1 - Ladybug install, scripted verification, no MCP.

## Overview

This directory contains automated test scripts that validate:
- lbug CLI installation and PATH configuration
- Python client installation
- graph-context skill creation and injectability
- Graph schema initialization (File, Symbol, IMPORTS)
- skeleton.md parser functionality
- generate-verification scripted hook integration
- BariaDAO pilot deployment
- Diff-scope verification (pre-merge gate)

## Test Scripts

### Core Tests

1. **test_lbug_cli.sh** - FR-1
   - Tests lbug CLI installation
   - Verifies PATH accessibility
   - Checks version output
   - Tests from fresh shell (agent session simulation)

2. **test_python_client.sh** - FR-2
   - Tests Python import of ladybug
   - Verifies version detection
   - Checks uv package list

3. **test_graph_context_skill.sh** - FR-3, FR-4
   - Verifies graph-context SKILL.md existence
   - Checks injectability documentation
   - Validates schema specification
   - Tests graph initialization
   - Queries schema for V1 types (File, Symbol, IMPORTS)

4. **test_skeleton_parser.sh** - FR-5
   - Creates sample skeleton.md with multiple files
   - Tests parser with def/class/async def
   - Validates File and Symbol node counts
   - Verifies IMPORTS edge creation
   - Tests edge case handling (empty skeleton)

5. **test_verification_hook.sh** - FR-6
   - Tests generate-verification scripted hook integration
   - Simulates in-scope and out-of-scope changes
   - Verifies pass/fail behavior
   *(Full integration test deferred to implementation phase)*

6. **test_baria_pilot.sh** - FR-7
   - Tests BariaDAO pilot deployment
   - Initializes graph from skeleton.md
   - Validates graph population
   - Runs ad hoc queries
   - Tests agent bash access

### Critical Tests

7. **test_diff_scope_premerge.sh** - Pre-Merge Check
   - **CRITICAL**: Validates diff-scope verification gate
   - Tests out-of-scope file detection
   - Validates in-scope file acceptance
   - Verifies verification hook integration
   - Provides clear error messages for failures
   - Can be run standalone to validate gate behavior

## Running Tests

### Run All Tests

```bash
./tests/M3/run_all_tests.sh
```

### Run Individual Tests

```bash
./tests/M3/test_lbug_cli.sh
./tests/M3/test_python_client.sh
./tests/M3/test_graph_context_skill.sh
./tests/M3/test_skeleton_parser.sh
./tests/M3/test_verification_hook.sh
./tests/M3/test_baria_pilot.sh
./tests/M3/test_diff_scope_premerge.sh
```

### Run with Verbose Output

```bash
./tests/M3/test_lbug_cli.sh --verbose
./tests/M3/test_skeleton_parser.sh --verbose
```

## Test Environment

- **Shell**: Bash 4.0+
- **Required Tools**:
  - lbug CLI (must be on PATH)
  - Python 3.8+
  - uv (Python package manager)
  - graph-context skill (must exist)

- **Test Directories**: All tests use `/tmp/test-*/` for isolated testing

## Expected Coverage

### Functional Validation (7 Requirements)

- FR-1: lbug CLI installation ✓
- FR-2: Python client installation ✓
- FR-3: graph-context skill creation ✓
- FR-4: Graph schema initialization ✓
- FR-5: skeleton.md parser ✓
- FR-6: verification hook integration ✓
- FR-7: BariaDAO pilot ✓

### Edge Cases (7 Cases)

- Empty skeleton.md
- Single file project
- Circular imports
- Deeply nested imports
- Non-Python import syntax
- Symbol ambiguity
- File path normalization

### Failure Scenarios (4 Categories)

- Verification hook failure (gate not gating)
- Graph initialization failure
- Parser failure (unresolved imports)
- Bash access failure (PATH issue)

### Regression Checklist (3 Areas)

- graph-context SKILL.md completeness
- generate-verification skill compatibility
- AEF environment conflicts

## Running Tests Before Merge

### Critical Pre-Merge Test

Run the diff-scope verification test before merging changes:

```bash
./tests/M3/test_diff_scope_premerge.sh
```

This test validates:
- Out-of-scope files are detected
- Clear error messages are provided
- The gate prevents out-of-scope changes
- The verification is mechanical (no LLM judgment)

## Next Steps

After implementation:

1. Run all tests: `./tests/M3/run_all_tests.sh`
2. Verify all tests pass
3. Address any failures
4. Run diff-scope premerge test before merge

## Notes

- Some integration tests are marked as "deferred to implementation phase"
  (e.g., full verification hook integration)
- These tests have placeholder logic that will be completed during implementation
- All tests are designed to be deterministic and repeatable

## Integration with Implementation

During `implement-specification`:
- These tests will validate the implementation
- The verification hook integration will be tested
- BariaDAO pilot will be validated end-to-end

During `evaluate-implementation`:
- Tests will be executed
- Results will be analyzed
- Any bugs will be auto-fixed
- Evaluation report will be generated
