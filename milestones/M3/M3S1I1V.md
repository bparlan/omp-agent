# Verification M3S1I1V

| Property         | Value        |
| ---------------- | ------------ |
| Document Type    | Verification |
| Identifier       | M3S1I1V      |
| Derived From     | M3S1, M3S1_INVESTIGATION, M3S1V |
| template_version | 1.1.0        |

## Success Criteria

- ingest-skeleton.py uses `file2` property for Symbol nodes (not `fileId`)
- ingest-skeleton.py creates IMPORTS edges between File nodes
- All files from skeleton.md are populated (3 files, not 2)
- Symbol queries work with correct property names: `lbug baria.lbug "MATCH (s:Symbol {name2: 'index_page'}) RETURN s.file2"`
- IMPORTS edges exist: `lbug baria.lbug "MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)"` returns > 0
- All File nodes exist: `lbug baria.lbug "MATCH (:File) RETURN count(*)"` returns 3
- verify-scope.py queries graph for reachable files
- verify-scope.py resolves transitive imports
- verify-scope.py fails for out-of-scope modifications
- verify-scope.py passes for in-scope modifications
- test_graph_scope_verification.sh passes all test scenarios
- All existing tests still pass (no regressions)
- M3S1 verification protocol acceptance criteria now met

---

## Followup Reuse

### Reusable Items from M3S1V

**Regression Checklist**:
- graph-context SKILL.md completeness (from M3S1V)
- generate-verification skill compatibility (from M3S1V)
- AEF environment conflicts (from M3S1V)

**Automated Test Patterns**:
- lbug CLI path verification pattern (from M3S1V FR-1)
- Graph schema validation pattern (from M3S1V FR-4)
- skeleton.md parser integration test pattern (from M3S1V FR-5)
- BariaDAO pilot verification pattern (from M3S1V FR-7)

**Edge Cases**:
- Empty skeleton.md (from M3S1V)
- Single file project (from M3S1V)
- Circular imports (from M3S1V)
- Deeply nested imports (from M3S1V)
- Non-Python import syntax (from M3S1V)
- File path normalization (from M3S1V)

**Failure Scenarios**:
- Out-of-scope edit passing verification (from M3S1V)
- In-scope edit failing verification (from M3S1V)
- Graph file not created (from M3S1V)
- Parser crashing on unresolved imports (from M3S1V)
- lbug command not found (from M3S1V)

### New Verification Required

**Specific to M3S1I1**:
- Schema property name correctness (file2 vs fileId)
- IMPORTS edge creation between File nodes
- Complete file population from skeleton.md (3 files)
- Graph-based reachable set resolution in verify-scope.py
- Integration tests for graph-based verification workflow

---

## Functional Validation

### FR-I1: Update ingest-skeleton.py to use `file2` property

**Verification Method**: Code inspection + Graph query

**Test Steps**:
1. Inspect `ingest-skeleton.py` source code
2. Search for Symbol node creation logic
3. Verify property name is `file2` (not `fileId`)
4. Run ingestion for BariaDAO: `graph-context ingest --skeleton .omp/graph/skeleton.md --graph .omp/graph/baria.lbug`
5. Query Symbol nodes with correct property: `lbug baria.lbug "MATCH (s:Symbol {name2: 'index_page'}) RETURN s.file2"`
6. Verify query returns file path (not error)

**Expected Output**:
- Source code uses `file2` property
- Query returns file path as string
- No "Property 'fileId' not found" error

**Failure Criteria**:
- Source code uses `fileId` property
- Query returns error or null
- Property name mismatch detected

---

### FR-I2: Implement IMPORTS edge creation

**Verification Method**: Graph query + Edge count validation

**Test Steps**:
1. Inspect `ingest-skeleton.py` for IMPORTS edge creation logic
2. Verify code creates edges between File nodes from import statements
3. Run ingestion for BariaDAO
4. Query IMPORTS edges: `lbug baria.lbug "MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)"`
5. Verify count > 0 (should have at least app_routes.py → content_loader.py)
6. Query specific edge: `lbug baria.lbug "MATCH (f1:File {name2: 'app_routes.py'})-[r:IMPORTS]->(f2:File) RETURN f1.name2, f2.name2, r.kind"`

**Expected Output**:
- Code implements IMPORTS edge creation
- Edge count > 0
- Edge returns from/To pairs with kind property

**Failure Criteria**:
- Edge count = 0
- No edge found when querying specific import
- Code doesn't create edges

---

### FR-I3: Ensure all files from skeleton.md are populated

**Verification Method**: Node count validation + File list comparison

**Test Steps**:
1. Read `skeleton.md` and count `### File:` sections (should be 3: app_routes.py, content_loader.py, README.md)
2. Query all File nodes: `lbug baria.lbug "MATCH (:File) RETURN f.name2 as name, f.path"`
3. Compare returned file names against skeleton.md
4. Verify count = 3 (not 2)
5. Check that README.md is present (often missed)

**Expected Output**:
- Graph has 3 File nodes
- All file names match skeleton.md entries
- README.md included

**Failure Criteria**:
- File count != 3
- Missing file(s) from skeleton.md
- Extra file(s) not in skeleton.md

---

### FR-I4: Integrate graph-based scope verification

**Verification Method**: Code inspection + Integration test

**Test Steps**:
1. Inspect `verify-scope.py` source code
2. Search for graph query functions (e.g., `get_graph_scope`)
3. Verify imports `ladybug` or uses lbug CLI
4. Run integration test scenario:
   - Modify `src/app_routes.py` (in-scope)
   - Run `verify-scope.py --scope=src/app_routes.py`
   - Verify exit code 0 (pass)
   - Modify `src/external.py` (out-of-scope)
   - Run `verify-scope.py --scope=src/app_routes.py`
   - Verify exit code 1 (fail) with error message

**Expected Output**:
- verify-scope.py queries graph
- In-scope modification passes
- Out-of-scope modification fails with error message

**Failure Criteria**:
- verify-scope.py doesn't query graph
- Both pass (gate doesn't work)
- Both fail (false positive)

---

### FR-I5: Create integration tests for graph-based verification

**Verification Method**: Test execution + Test coverage review

**Test Steps**:
1. Create `tests/M3/test_graph_scope_verification.sh`
2. Implement test scenarios:
   - In-scope modification (should pass)
   - Out-of-scope modification (should fail)
   - Multiple in-scope files (should pass)
   - Mixed in-scope/out-of-scope (should fail)
3. Run all test scenarios
4. Verify all tests pass
5. Review test code for completeness and clarity

**Expected Output**:
- All test scenarios pass
- Tests cover critical edge cases
- Error messages are clear

**Failure Criteria**:
- Any test fails
- Tests don't cover key scenarios
- Error handling missing

---

## Edge Cases

- **Property name variants**: Verify code handles both `fileId` and `file2` gracefully during migration
- **Multiple files in skeleton.md**: Parser must handle any number of files without errors
- **No imports section**: Files without imports should still be created as File nodes
- **Empty imports list**: IMPORTS edge count should remain 0 if no imports defined
- **Duplicate file entries**: Parser should deduplicate or handle gracefully
- **Missing dependencies**: Import statements pointing to non-existent files should be flagged (not crash)
- **Circular imports**: IMPORTS edges may form cycles; graph query should handle without infinite loops
- **Deeply nested paths**: File paths with many components should parse correctly
- **Symbol name collisions**: Multiple symbols with same name in different files must be distinguishable by file reference

---

## Failure Scenarios

### Property Name Mismatch

- **Scenario**: ingest-skeleton.py uses `fileId` but database has `file2`
  - **Detection**: Graph query returns "Property 'fileId' not found" error
  - **Validation**: Compare source code property names against lbug schema documentation
  - **Fix**: Update property names in ingest-skeleton.py to match schema

- **Scenario**: verify-scope.py uses wrong property name in Cypher query
  - **Detection**: Query returns property not found error
  - **Validation**: Run lbug queries with correct and incorrect property names side-by-side
  - **Fix**: Update Cypher queries to use correct property names

### Import Edge Creation Failure

- **Scenario**: IMPORTS edges not created despite import statements
  - **Detection**: Query `MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)` returns 0
  - **Validation**: Review ingest-skeleton.py edge creation logic
  - **Fix**: Implement IMPORTS edge creation in parser

- **Scenario**: Unresolved imports cause parser crash
  - **Detection**: Parser exits with error when processing imports
  - **Validation**: Run parser with verbose output
  - **Fix**: Implement defensive error handling

### Graph Population Incomplete

- **Scenario**: Only 2 of 3 files from skeleton.md are in graph
  - **Detection**: Query File node count returns 2 instead of 3
  - **Validation**: Compare skeleton.md against graph File nodes
  - **Fix**: Ensure all files are processed during ingestion

- **Scenario**: Missing README.md file node
  - **Detection**: README.md not in graph despite being in skeleton.md
  - **Validation**: Read both files side-by-side
  - **Fix**: Add missing file processing logic

### Verification Hook Failure

- **Scenario**: verify-scope.py doesn't query graph
  - **Detection**: verify-scope.py only checks file names, not graph
  - **Validation**: Inspect verify-scope.py source code
  - **Fix**: Integrate graph queries into verify-scope.py

- **Scenario**: Out-of-scope edit passes verification (gate doesn't gate)
  - **Detection**: Task passes despite touching files outside declared scope
  - **Validation**: Run verification with deliberately out-of-scope edit
  - **Fix**: Implement graph-based reachable set resolution

- **Scenario**: In-scope edit fails verification (false positive)
  - **Detection**: Task fails despite touching only in-scope files
  - **Validation**: Check import resolution and edge creation
  - **Fix**: Correct reachable set calculation

### Integration Test Failure

- **Scenario**: Integration tests don't pass
  - **Detection**: Test execution returns exit code != 0
  - **Validation**: Review test output and error messages
  - **Fix**: Fix failing tests or update expectations

---

## Regression Checklist

### graph-context Skill (ingest-skeleton.py)

- [ ] Symbol node creation uses correct property names (file2, name2, kind2)
- [ ] IMPORTS edge creation logic still works
- [ ] File node creation logic unchanged
- [ ] Parser doesn't break existing functionality
- [ ] Error handling remains robust

### graph-context Skill (verify-scope.py)

- [ ] Git diff detection still works
- [ ] File path normalization still works
- [ ] Scope comparison logic still works
- [ ] Graph-based verification added without breaking existing logic

### tests/M3 Test Suite

- [ ] Existing test_lbug_cli.sh still passes
- [ ] Existing test_python_client.sh still passes (if used)
- [ ] Existing test_graph_context_skill.sh still passes
- [ ] Existing test_skeleton_parser.sh still passes
- [ ] Existing test_verification_hook.sh still passes

### AEF Environment

- [ ] lbug CLI still works after changes
- [ ] Graph file operations unchanged
- [ ] No unintended side effects on other skills
- [ ] Backward compatibility maintained

---

## Manual Validation

1. **Code Review**:
   - Review `ingest-skeleton.py` changes
   - Verify property names are correct (`file2` not `fileId`)
   - Verify IMPORTS edge creation logic exists
   - Verify all skeleton.md files are processed

2. **Graph Inspection**:
   - Navigate to BariaDAO project root
   - Run ingestion: `graph-context ingest --skeleton .omp/graph/skeleton.md --graph .omp/graph/baria.lbug`
   - Inspect graph file: `lbug baria.lbug "MATCH (:File) RETURN f.name2, f.path"`
   - Inspect symbols: `lbug baria.lbug "MATCH (s:Symbol) RETURN s.name2, s.kind2, s.file2"`
   - Inspect edges: `lbug baria.lbug "MATCH (:File)-[:IMPORTS]->(:File) RETURN f1.name2, f2.name2"`

3. **Verification Hook Test**:
   - Create a temporary file outside scope
   - Run verify-scope.py with scope boundary
   - Verify gate fails appropriately
   - Remove out-of-scope file
   - Run verify-scope.py again
   - Verify gate passes

4. **Integration Test Review**:
   - Read `test_graph_scope_verification.sh`
   - Verify test scenarios cover all cases
   - Verify error messages are clear
   - Verify cleanup logic is correct

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

_Mechanical check must be executed by evaluate-implementation before tests are considered passed._

- **Command**: `git diff --name-only`
- **Assertion**: The output of this command MUST strictly match the "Allowlist" defined in M3S1I1 Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

- Existing tests
  - `tests/M3/test_lbug_cli.sh`
  - `tests/M3/test_python_client.sh`
  - `tests/M3/test_graph_context_skill.sh`
  - `tests/M3/test_skeleton_parser.sh`
  - `tests/M3/test_verification_hook.sh`
  - `tests/M3/test_diff_scope_premerge.sh`
  - `tests/M3/test_baria_pilot.sh`

- New tests
  - `tests/M3/test_graph_scope_verification.sh`

#### Graph Property Verification

- **Command**: `grep -n "fileId" ~/devcode/aef/agent/skills/graph-context/bin/ingest-skeleton.py`
- **Assertion**: No matches found (verify uses `file2`)

- **Command**: `lbug baria.lbug "MATCH (s:Symbol) RETURN s.file2"`
- **Assertion**: Returns valid file paths, no errors

#### IMPORTS Edge Verification

- **Command**: `lbug baria.lbug "MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)"`
- **Assertion**: Returns count > 0

- **Command**: `lbug baria.lbug "MATCH (f1:File {name2: 'app_routes.py'})-[r:IMPORTS]->(f2:File) RETURN f1.name2, f2.name2"`
- **Assertion**: Returns app_routes.py → content_loader.py

#### File Population Verification

- **Command**: `lbug baria.lbug "MATCH (:File) RETURN count(*)"`
- **Assertion**: Returns 3

- **Command**: `lbug baria.lbug "MATCH (:File) RETURN f.name2"`
- **Assertion**: Returns ['app_routes.py', 'content_loader.py', 'README.md']

#### Verification Hook Integration

- **Command**: `cd /Users/bparlan/devcode/BariaDAO && echo "# out-of-scope" >> src/external.py`
- **Command**: `python3 ~/devcode/aef/agent/skills/graph-context/bin/verify-scope.py --scope=src/app_routes.py`
- **Assertion**: Exit code 1, error message mentions src/external.py

- **Command**: `rm src/external.py`
- **Command**: `echo "# in-scope" >> src/app_routes.py`
- **Command**: `python3 ~/devcode/aef/agent/skills/graph-context/bin/verify-scope.py --scope=src/app_routes.py`
- **Assertion**: Exit code 0

#### Test Execution

- **Command**: `cd ~/devcode/aef/agent && ./tests/M3/test_graph_scope_verification.sh`
- **Assertion**: All test scenarios pass

---

## Expected Outcomes

### Graph Correctness

- All 3 files from skeleton.md are present in the graph
- All symbols from all files are present
- IMPORTS edges correctly represent dependencies
- Property names match lbug schema (file2, name2, kind2)

### Verification Functionality

- verify-scope.py queries the graph
- Reachable set calculation includes transitive imports
- Out-of-scope modifications are rejected
- In-scope modifications are accepted

### Test Coverage

- Integration tests cover all critical scenarios
- Tests pass reliably
- Error messages are clear and actionable

### No Regressions

- All existing tests still pass
- No breaking changes to existing functionality
- Backward compatibility maintained

---

## Considerations

### Performance Considerations

- **Graph Query Performance**: Queries should be optimized for large graphs. Consider indexing on File nodes if graphs become large (>100 files).
- **Import Resolution Speed**: Import resolution should handle all imports efficiently, even with deeply nested modules.
- **Test Execution Speed**: Integration tests should complete within reasonable time (< 60 seconds total).

### Security Considerations

- **Path Injection Prevention**: Import resolution must validate paths to prevent directory traversal attacks.
- **Graph Query Safety**: Cypher queries should use parameterized values to prevent injection attacks.
- **File System Access**: verify-scope.py should only read files it has permission to access.

### Observability

- **Error Messages**: All error messages should clearly indicate which property or file caused the failure.
- **Debug Output**: Parser should have verbose mode for debugging edge cases.
- **Logging**: Verification hook should log the reachable set for manual inspection.

---

## Followup Requirements

After M3S1I1 fixes are applied, proceed to **M3S2** to add CALLS and RENDERS edges for true blast-radius queries.

**M3S2 Prerequisites**:
- M3S1I1 stability fixes must be verified working
- Graph must be queryable and accurate
- Verification hook must successfully gate out-of-scope edits

---

## Next Steps

Advise running `generate-tests` to create executable test scripts for M3S1I1, then `implement-specification` to execute the stability fixes.

**Critical Path**: Fix 1-3 (schema property, IMPORTS edges, all files) must pass before proceeding to M3S2 verification.
