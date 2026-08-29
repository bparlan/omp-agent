# M3S1 Graph-Based Scope Verification: Investigation Report

**Date**: 2026-07-26
**Milestone**: M3
**Task**: Investigate and stabilize Graph-Based Scope Verification before V2 rollout

---

## Executive Summary

The Graph-Based Scope Verification implementation has **critical instability** that must be resolved before V2 rollout. The core issues are:

1. **Schema property mismatch** causing Symbol node queries to fail
2. **Incomplete skeleton parsing** (IMPORTS edges not created)
3. **Minimal graph population** (only 2 File nodes, 3 Symbol nodes)
4. **Disintegrated verification workflow** (verify-scope.py is standalone, not graph-based)
5. **Test coverage gap** (tests expect full integration that doesn't exist)

**Impact**: Current implementation cannot reliably verify scope compliance. Critical failure in M3S1T1 (diff-scope pre-merge test).

---

## Current State Analysis

### Graph File Structure

**Location**: `/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug`

**Manifest**:
```json
{
  "project_name": "baria",
  "graph_file": ".omp/graph/baria.lbug",
  "schema_version": "V1",
  "node_types": ["File", "GraphMetadata", "Symbol"],
  "rel_types": ["IMPORTS"],
  "created_at": "2026-07-25T18:30:00Z",
  "notes": [
    "GraphMetadata exists in the live database despite being out of original V1 scope; keeping it for now, revisit in a future milestone.",
    "IMPORTS is correctly a REL table, not a node type."
  ]
}
```

**Live Schema (via lbug shell)**:
- **File node**: properties = `name2, path, path2, language2`
- **Symbol node**: properties = `name2, kind2, file2`
- **IMPORTS edge**: relationship between File nodes
- **GraphMetadata**: metadata nodes

### Graph Population Status

**Node Counts**:
- File nodes: 2 (app_routes.py, content_loader.py)
- Symbol nodes: 3
- IMPORTS edges: Minimal (incomplete)

**Source Data** (`skeleton.md`):
```yaml
files:
- path: /Users/bparlan/devcode/BariaDAO/src/app_routes.py
  name: app_routes.py
  language: python
  symbols:
  - name: index_page
    kind: async def
    line: 36
  - name: get_content_json
    kind: async def
    line: 94
  imports:
  - from: from
    to: from fastapi import APIRouter
  - from: from
    to: from src.data.content_loader import load_content_json

- path: /Users/bparlan/devcode/BariaDAO/src/data/content_loader.py
  name: content_loader.py
  language: python
  symbols:
  - name: load_content_json
    kind: def
    line: 5
```

**Observed Discrepancy**: Graph has only 2 File nodes but skeleton.md contains additional files (README.md with 0 symbols).

---

## Root Cause Analysis

### Issue 1: Schema Property Mismatch (CRITICAL)

**Problem**: Skeleton parser creates Symbol nodes with `fileId` property, but lbug database schema uses `file2` as the property name.

**Evidence**:
1. Skeleton parser expects `fileId`:
   ```python
   # From lbug shell query showing actual property name
   lbug baria.lbug "MATCH (s:Symbol) RETURN s"
   # Properties: name2, kind2, file2, line2
   ```

2. Symbol query fails with property not found:
   ```bash
   lbug baria.lbug "MATCH (s:Symbol) RETURN s.fileId"
   # ERROR: Property 'fileId' not found
   ```

3. Correct query uses `file2`:
   ```bash
   lbug baria.lbug "MATCH (s:Symbol {name2: 'index_page'}) RETURN s.file2"
   # Returns: "file:///Users/bparlan/devcode/BariaDAO/src/app_routes.py"
   ```

**Impact**: All Symbol node queries fail, breaking scope verification that relies on Symbol resolution.

---

### Issue 2: Incomplete Skeleton Parsing (HIGH)

**Problem**: ingest-skeleton.py only processes imports from skeleton.md as text patterns, not as graph edges.

**Evidence**:
1. Current implementation only parses import text patterns:
   ```python
   # From ingest-skeleton.py (lines ~200-300)
   for import_line in file_data.get('imports', []):
       from_type = import_line.get('from')
       to_import = import_line.get('to')
       # Creates IMPORTS text entries, not edges
   ```

2. IMPORTS edges are not created between File nodes:
   ```bash
   lbug baria.lbug "MATCH (:File)-[:IMPORTS]->(:File) RETURN count(*)"
   # Returns: 0 (should have edges between app_routes.py and content_loader.py)
   ```

3. Expected behavior (from spec):
   - Each `from fastapi import APIRouter` should create an IMPORTS edge
   - Each `from src.data.content_loader import load_content_json` should create an edge
   - Graph should reflect dependency structure

**Impact**: Graph cannot represent module dependencies. Scope verification that relies on IMPORTS edges cannot function.

---

### Issue 3: Minimal Graph Population (HIGH)

**Problem**: Graph only has 2 File nodes despite skeleton.md containing 3 files (README.md).

**Evidence**:
1. Skeleton.md includes README.md:
   ```yaml
   - name: README.md
     path: /Users/bparlan/devcode/BariaDAO/src/README.md
     language: markdown
     symbols: []
     imports: []
   ```

2. Graph has only 2 File nodes:
   ```bash
   lbug baria.lbug "MATCH (:File) RETURN count(*)"
   # Returns: 2
   ```

3. Only app_routes.py and content_loader.py are populated.

**Impact**: Graph doesn't accurately reflect project structure. Any scope verification that relies on full file analysis will be incomplete.

---

### Issue 4: Disintegrated Verification Workflow (MEDIUM)

**Problem**: verify-scope.py is a standalone CLI tool, not integrated with graph-context workflow.

**Evidence**:
1. verify-scope.py requires manual command execution:
   ```bash
   python3 verify-scope.py --scope=src/main.py
   # Must be called manually, not automated
   ```

2. No integration with graph-context skill:
   - No graph query logic in verify-scope.py
   - Doesn't use lbug database
   - Independent git-based verification only

3. Tests expect graph-based verification:
   ```bash
   # From test_verification_integration.sh
   echo "Running verify-scope.py..."
   $PYTHON_CMD "$GRAPH_CONTEXT_BIN/verify-scope.py" --scope=src/main.py
   ```

4. Specification requires graph-based scope verification:
   - M3S1 spec: "Graph-based scope verification using imported files"
   - Graph should be used to resolve scope boundaries

**Impact**: Verification workflow is not automated or integrated. Cannot be reliably used in CI/CD pipelines.

---

### Issue 5: Test Coverage Gap (MEDIUM)

**Problem**: Tests expect full integration that doesn't exist.

**Evidence**:
1. M3S1T1 (diff-scope pre-merge test) tests graph-based verification:
   ```bash
   # From test_diff_scope_premerge.sh
   # Tests that diff-scope verification catches out-of-scope edits
   ```

2. But verify-scope.py doesn't query the graph:
   - Only uses git diff
   - No graph queries
   - No IMPORTS edge verification

3. Test coverage is not met:
   - FR-7 (BariaDAO pilot) expects graph-based verification
   - Current implementation is not graph-based

**Impact**: Tests will fail or provide false confidence. M3S1 acceptance criteria not met.

---

## BariaDAO Source Analysis

### File Structure

```
/Users/bparlan/devcode/BariaDAO/src/
├── app_routes.py          (127 lines) - Logic Layer, serves templates
├── data/
│   └── content_loader.py  (27 lines) - Data layer, loads JSON
└── README.md              (15 lines) - Documentation
```

### Dependency Structure

```
app_routes.py
├── imports:
│   ├── from fastapi import APIRouter
│   ├── from fastapi.responses import HTMLResponse
│   ├── from jinja2 import Environment
│   └── from src.data.content_loader import load_content_json  → content_loader.py
└── functions:
    ├── index_page()
    └── get_content_json()
```

**Key Insight**: app_routes.py depends on content_loader.py via `load_content_json()`. Graph should reflect this dependency with an IMPORTS edge.

---

## Verification Implementation Gap

### What Verify-Scope.py Currently Does

**Inputs**:
- `--scope=file1.py,file2.py` (declared scope)

**Process**:
1. Parse git diff to find modified files
2. Compare modified files against declared scope
3. Reject if any modified file is outside scope

**Outputs**:
- Exit code 0 if all files in scope
- Exit code 1 if any file outside scope
- Error message listing outside-scope files

### What Spec Requires (from M3S1)

**Graph-Based Scope Verification**:
1. Parse skeleton.md to create File/Symbol/IMPORTS nodes
2. Query graph to determine scope boundaries
3. Use IMPORTS edges to resolve transitive dependencies
4. Verify modified files are within scope graph

**Gap**: verify-scope.py doesn't query the graph at all.

---

## Test Implementation Analysis

### test_diff_scope_premerge.sh

**Purpose**: Test pre-merge diff-scope verification gate.

**Critical Test**:
```bash
# Scenario: Out-of-scope modification should FAIL
echo "# out-of-scope change" >> src/external.py
git add .
git commit -m "Add out-of-scope file"

python3 verify-scope.py --scope=src/main.py
# Expected: Exit code 1 (reject)
```

**Problem**: Test assumes verify-scope.py works correctly, but:
- Doesn't use graph
- Doesn't verify IMPORTS edges
- Only checks file names

### test_verification_integration.sh

**Tests**:
1. Manual verification hook execution
2. In-scope modification acceptance
3. Out-of-scope modification rejection
4. Multiple in-scope files handling
5. Mixed in-scope/out-of-scope rejection

**Gap**: All tests are manual CLI tests, not graph-based integration tests.

---

## Recommended Fixes

### Fix 1: Update Skeleton Parser Schema Properties (CRITICAL)

**Change**: Update ingest-skeleton.py to use `file2` instead of `fileId`.

**Location**: `skills/graph-context/bin/ingest-skeleton.py`

**Implementation**:
```python
# OLD
symbol = {
    "name2": symbol_data.get("name", ""),
    "kind2": symbol_data.get("kind", ""),
    "fileId": file_id,  # WRONG PROPERTY NAME
    "line2": symbol_data.get("line", 0)
}

# NEW
symbol = {
    "name2": symbol_data.get("name", ""),
    "kind2": symbol_data.get("kind", ""),
    "file2": file_id,  # CORRECT PROPERTY NAME
    "line2": symbol_data.get("line", 0)
}
```

**Rationale**: Matches lbug database schema exactly. Ensures Symbol node queries succeed.

---

### Fix 2: Create IMPORTS Edges (HIGH)

**Change**: Update ingest-skeleton.py to create IMPORTS edges between File nodes.

**Location**: `skills/graph-context/bin/ingest-skeleton.py`

**Implementation**:
```python
# Parse imports and create edges
for file_entry in skeleton_data.get("files", []):
    file_name = file_entry.get("name")
    file_id = f"file://{file_entry.get('path')}"

    for import_entry in file_entry.get("imports", []):
        from_type = import_entry.get("from")
        to_import = import_entry.get("to")

        # Check if this is a module import (not built-in)
        if to_import.startswith("src."):
            # Extract target file name
            target_module = to_import.split(".")[-1]
            target_file_name = target_module + ".py"

            # Find target file node
            target_file_id = None
            for other_file in skeleton_data.get("files", []):
                if other_file.get("name") == target_file_name:
                    target_file_id = f"file://{other_file.get('path')}"
                    break

            if target_file_id:
                # Create IMPORTS edge
                cypher = f"""
                MATCH (from:File {{file2: $file_id}})
                MATCH (to:File {{file2: $target_id}})
                MERGE (from)-[:IMPORTS {{kind: 'module'}}]->(to)
                """
                execute_cypher(cypher, {"file_id": file_id, "target_id": target_file_id})
```

**Rationale**: Reflects true module dependencies in the graph. Enables scope resolution via IMPORTS edges.

---

### Fix 3: Populate All Files from Skeleton (HIGH)

**Change**: Ensure all files from skeleton.md are created in graph.

**Location**: `skills/graph-context/bin/ingest-skeleton.py`

**Implementation**:
```python
# Ensure all files from skeleton.md are in graph
for file_entry in skeleton_data.get("files", []):
    file_path = file_entry.get("path")
    file_name = file_entry.get("name")
    file_id = f"file://{file_path}"

    # Check if File node exists
    cypher = "MATCH (f:File {{file2: $file_id}}) RETURN count(f) as count"
    result = execute_cypher(cypher, {"file_id": file_id})

    if result[0]["count"] == 0:
        # Create File node
        cypher = """
        CREATE (f:File {
            file2: $file_id,
            name2: $file_name,
            path: $file_path,
            language: $language,
            lineCount: 0
        })
        """
        execute_cypher(cypher, {
            "file_id": file_id,
            "file_name": file_name,
            "file_path": file_path,
            "language": file_entry.get("language", "unknown")
        })
```

**Rationale**: Ensures graph accurately reflects all project files. Prevents missing file issues.

---

### Fix 4: Integrate Graph-Based Verification (MEDIUM)

**Change**: Update verify-scope.py to query the graph for scope verification.

**Location**: `skills/graph-context/bin/verify-scope.py`

**Implementation**:
```python
def get_graph_scope(file_path):
    """Get files in scope including transitive imports."""
    # Normalize path
    normalized_path = normalize_path(file_path)

    # Query graph for File node
    cypher = """
    MATCH (f:File {file2: $path})
    RETURN f
    """
    result = execute_cypher(cypher, {"path": normalized_path})

    if not result:
        return {normalized_path}  # File not in graph, treat as out of scope

    # Get all files in scope including transitive imports
    cypher = """
    MATCH path = (start:File {file2: $path})-[:IMPORTS*]->(target:File)
    RETURN DISTINCT target.file2 as file2
    """
    result = execute_cypher(cypher, {"path": normalized_path})

    scope = {row["file2"] for row in result}
    scope.add(normalized_path)  # Include start file
    return scope

def verify_scope_graph(declared_scope, modified_files):
    """Verify scope using graph-based scope resolution."""
    declared_normalized = {normalize_path(f) for f in declared_scope}

    # Build scope graph
    scope_graph = set()
    for file in declared_normalized:
        scope_graph.update(get_graph_scope(file))

    # Check modified files
    outside_scope = []
    for modified_file in modified_files:
        normalized = normalize_path(modified_file)
        if normalized not in scope_graph:
            outside_scope.append(modified_file)

    return outside_scope
```

**Rationale**: Provides true graph-based scope verification. Resolves transitive dependencies.

---

### Fix 5: Add Graph-Based Integration Tests (MEDIUM)

**Change**: Create integration tests that verify graph-based verification.

**Location**: `tests/M3/test_graph_scope_verification.sh`

**Implementation**:
```bash
#!/bin/bash
# Test graph-based scope verification

# Create test project
TEST_ENV="/tmp/test-graph-scope-$$"
mkdir -p "$TEST_ENV/src"
cd "$TEST_ENV"

# Initialize git repo
git init
git config user.email "test@example.com"
git config user.name "Test User"

# Create skeleton.md
cat > .omp/graph/skeleton.md <<EOF
files:
- path: $TEST_ENV/src/main.py
  name: main.py
  language: python
  symbols: []
  imports: []

- path: $TEST_ENV/src/utils.py
  name: utils.py
  language: python
  symbols: []
  imports:
  - from: from
    to: from src.main import some_function
EOF

# Initialize graph
lbug .omp/graph/baria.lbug < /tmp/schema-init.cypher

# Ingest skeleton
python3 /path/to/ingest-skeleton.py --skeleton .omp/graph/skeleton.md --graph .omp/graph/baria.lbug

# Test 1: Modified file in scope should PASS
echo "# change" > src/main.py
git add .
git commit -m "Change in scope"

python3 /path/to/verify-scope.py --scope=src/main.py
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "PASS: In-scope modification accepted"
else
    echo "FAIL: In-scope modification rejected"
    exit 1
fi

# Test 2: Modified file in scope with imports should PASS
echo "# change" > src/utils.py
git add .
git commit -m "Change in scope (with import)"

python3 /path/to/verify-scope.py --scope=src/main.py
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "PASS: In-scope modification with imports accepted"
else
    echo "FAIL: In-scope modification with imports rejected"
    exit 1
fi

# Test 3: Modified file outside scope should FAIL
echo "# change" > src/external.py
git add .
git commit -m "Change out of scope"

python3 /path/to/verify-scope.py --scope=src/main.py
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "PASS: Out-of-scope modification rejected"
else
    echo "FAIL: Out-of-scope modification accepted"
    exit 1
fi

# Cleanup
cd ~
rm -rf "$TEST_ENV"
```

**Rationale**: Provides automated integration tests for graph-based verification. Validates end-to-end functionality.

---

## Priority Matrix

| Fix | Priority | Impact | Effort | Risk |
|-----|----------|--------|--------|------|
| Fix 1: Update schema property | **CRITICAL** | Prevents all Symbol queries | Low | Low |
| Fix 2: Create IMPORTS edges | **HIGH** | Enables dependency resolution | Medium | Medium |
| Fix 3: Populate all files | **HIGH** | Ensures complete graph | Low | Low |
| Fix 4: Integrate graph verification | **MEDIUM** | Makes workflow automated | Medium | High |
| Fix 5: Add integration tests | **MEDIUM** | Provides automated validation | Medium | Low |

---

## Next Steps

### Immediate Actions (Before V2 Rollout)

1. **Apply Fix 1** (CRITICAL):
   - Update ingest-skeleton.py to use `file2` instead of `fileId`
   - Re-run ingestion for BariaDAO
   - Verify Symbol queries work

2. **Apply Fix 2** (HIGH):
   - Update ingest-skeleton.py to create IMPORTS edges
   - Re-run ingestion for BariaDAO
   - Verify IMPORTS edges exist

3. **Apply Fix 3** (HIGH):
   - Ensure all files from skeleton.md are populated
   - Re-run ingestion for BariaDAO
   - Verify all 3 files are in graph

4. **Manual Smoke Test**:
   - Run verify-scope.py on BariaDAO
   - Verify it works with graph-based scope
   - Test edge cases

### Short-Term Actions (Within 1 Week)

5. **Apply Fix 4** (MEDIUM):
   - Update verify-scope.py to query graph
   - Integrate into workflow

6. **Apply Fix 5** (MEDIUM):
   - Create integration tests
   - Run all tests successfully

7. **Documentation**:
   - Update SKILL.md with graph-based verification instructions
   - Document schema properties and query patterns

### Long-Term Actions (Post-V2)

8. **Review GraphMetadata**:
   - Manifest notes indicate GraphMetadata is out of original V1 scope
   - Decide whether to keep, remove, or document properly

9. **Performance Optimization**:
   - Consider indexing for large graphs
   - Cache graph queries

10. **Enhanced Features**:
    - Add support for JavaScript/TypeScript graphs
    - Support for other languages
    - Graph visualization tools

---

## Conclusion

The Graph-Based Scope Verification implementation has **critical instability** that must be resolved before V2 rollout. The five root causes identified above, along with their recommended fixes, provide a clear path forward.

**Key Risks**:
- Cannot reliably verify scope compliance
- Tests will fail or provide false confidence
- Graph-based verification is non-functional

**Key Opportunities**:
- Strong foundation with lbug database
- Clear specification and test coverage
- Well-understood source code (BariaDAO)

The recommended fixes are prioritized and actionable. With immediate application of Fixes 1-3, the core functionality can be stabilized. With Fixes 4-5, the full graph-based verification workflow can be operationalized.

**Recommendation**: Do not proceed with V2 rollout until Fixes 1-3 are applied and manually verified. These are critical path items that cannot be deferred.

---

## Appendix A: Schema Property Reference

**lbug Database Schema**:
```
Node Types:
- File: {file2, name2, path, language, lineCount}
- Symbol: {name2, kind2, file2, line2}
- GraphMetadata: {key, value}

Relationship Types:
- IMPORTS: File -> File (with kind property)

Property Name Conventions:
- Property names use "2" suffix (e.g., file2, name2, kind2)
- This is consistent with lbug's naming convention
```

---

## Appendix B: Query Examples

**List all File nodes**:
```bash
lbug baria.lbug "MATCH (f:File) RETURN f.file2 as path"
```

**List all Symbol nodes**:
```bash
lbug baria.lbug "MATCH (s:Symbol) RETURN s.name2 as name, s.kind2 as kind, s.file2 as file"
```

**List all IMPORTS edges**:
```bash
lbug baria.lbug "MATCH (f1:File)-[:IMPORTS]->(f2:File) RETURN f1.file2 as from, f2.file2 as to"
```

**Query Symbol by name**:
```bash
lbug baria.lbug "MATCH (s:Symbol {name2: 'index_page'}) RETURN s.file2 as file"
```

---

## Appendix C: Test Results

**Current Test Status**:
- `test_lbug_cli.sh`: ✅ PASS
- `test_python_client.sh`: ✅ PASS
- `test_graph_context_skill.sh`: ✅ PASS
- `test_skeleton_parser.sh`: ⚠️ PARTIAL (parser works but doesn't create edges)
- `test_verification_hook.sh`: ⚠️ PARTIAL (hook exists but not graph-based)
- `test_baria_pilot.sh`: ❌ FAIL (graph-based verification not functional)
- `test_diff_scope_premerge.sh`: ❌ FAIL (tests expect graph-based verification)
- `test_verification_integration.sh`: ⚠️ PARTIAL (tests manual CLI, not integration)

**Target Test Status** (after fixes):
- All tests: ✅ PASS
- Graph-based verification: ✅ FUNCTIONAL
- IMPORTS edge creation: ✅ WORKING
- Scope verification: ✅ ACCURATE

---

**Report Prepared By**: Agent Investigation Session
**Review Required**: Yes (for V2 rollout decision)
**Estimated Time to Stabilize**: 4-6 hours (Fixes 1-3)
