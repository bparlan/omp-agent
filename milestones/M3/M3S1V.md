# Verification M3S1V

| Property         | Value        |
| ---------------- | ------------ |
| Document Type    | Verification |
| Identifier       | M3S1V        |
| Derived From     | M3S1         |
| template_version | 1.1.0        |

## Success Criteria

- [x] `lbug --version` runs successfully and outputs version information when executed from a shell that agent bash sessions inherit
- [x] `python -c "import ladybug"` works after running `uv add ladybug` in the AEF repo
- [x] `~/devcode/aef/agent/skills/graph-context/` exists with SKILL.md and implements injectability
- [x] Project injection creates `.omp/graph/<name>.lbug` with File and Symbol node types and IMPORTS edge type
- [x] skeleton.md parser successfully converts to Ladybug upsert operations (File nodes from `### File:` sections, Symbol nodes from def/class/async def, IMPORTS edges from import statements)
- [x] `generate-verification` skill includes a scripted hook that:
  - Accepts declared scope (files/components)
  - Queries reachable nodes from those files using Ladybug Python client
  - Compares actual diff against reachable set
  - Fails task if diff touches files outside reachable set
- [x] An agent session successfully runs an ad hoc `lbug` query via bash against the pilot graph (documented and tested)
- [x] BariaDAO's `.omp/graph/baria.lbug` is populated from its `skeleton.md`
- [x] A deliberately out-of-scope edit attempt fails the verification hook (confirms the gate works, not just runs)

---

## Followup Reuse

### Reusable Items from Prior Verifications

- **N/A**: This is the first specification for M3; no prior verifications exist.

### New Verification Required

- **Diff-Scope Verification**: The scripted verifier hook must mechanically validate that all changes are within the reachable set from declared scope, with no LLM judgment.
- **Graph Schema Compliance**: Must verify that the V1 schema (File, Symbol, IMPORTS) is correctly defined and that only these types are present in pilot graphs.
- **Parser Correctness**: Must validate that the skeleton.md parser correctly handles all three entity types (File, Symbol, IMPORTS) and flags unresolved imports.

---

## Functional Validation

### FR-1: lbug CLI Installation & PATH Verification

**Validation Method:** Manual shell execution + Agent bash session test

**Test Steps:**
1. Execute `lbug --version` in the current shell
2. Execute `lbug --version` from a fresh shell (simulating agent environment)
3. Confirm PATH includes the directory where `lbug` was installed

**Expected Output:**
- Command returns version information (e.g., `Ladybug CLI v1.2.3`)

**Failure Criteria:**
- Command returns "command not found"
- Version information missing or corrupted

---

### FR-2: Python Client Installation

**Validation Method:** Python import test + `uv list` verification

**Test Steps:**
1. `cd ~/devcode/aef/agent && uv add ladybug`
2. Execute `python -c "import ladybug; print(ladybug.__version__)"`

**Expected Output:**
- No import errors
- Prints `ladybug` version string

**Failure Criteria:**
- ImportError raised
- Version not detected

---

### FR-3: graph-context Skill Creation

**Validation Method:** File existence check + SKILL.md content verification

**Test Steps:**
1. Verify `~/devcode/aef/agent/skills/graph-context/SKILL.md` exists
2. Read SKILL.md to confirm:
   - Contains injectability instructions
   - Documents usage for `init-graph`, `ingest-skeleton`
   - References `.omp/graph/<name>.lbug` as output location
   - Specifies V1 schema (File, Symbol, IMPORTS)

**Expected Output:**
- SKILL.md file present with all required sections
- Instructions are clear and actionable

**Failure Criteria:**
- Skill file missing
- Schema definition incomplete or incorrect
- No injectability documentation

---

### FR-4: Graph Schema Initialization

**Validation Method:** Direct file inspection + Ladybug schema query

**Test Steps:**
1. Create test project directory: `mkdir -p /tmp/test-ladybug/.omp`
2. Run graph-context injection: `graph-context init test-ladybug`
3. Verify `.omp/graph/test-ladybug.lbug` file exists
4. Query schema via `lbug --db .omp/graph/test-ladybug.lbug schema` and verify:
   - Node type `File` defined
   - Node type `Symbol` defined
   - Edge type `IMPORTS` defined
   - No other node or edge types present

**Expected Output:**
- Graph file created
- Schema query returns only File, Symbol, and IMPORTS

**Failure Criteria:**
- Graph file not created
- Schema includes invalid or missing types
- Extra node/edge types present

---

### FR-5: skeleton.md Parser

**Validation Method:** Integration test with sample skeleton.md

**Test Steps:**
1. Create sample skeleton.md with:
   - Multiple `### File:` sections
   - `def`, `class`, `async def` statements
   - Multiple import statements (some resolved, some unresolved)
2. Run parser: `graph-context ingest --skeleton sample.md --graph .omp/graph/test.lbug`
3. Query graph: `lbug --db .omp/graph/test.lbug cypher "MATCH (n) RETURN count(n)"` to count nodes
4. Run queries to verify:
   - `File` nodes match count of `### File:` sections
   - `Symbol` nodes match count of def/class/async def entries
   - `IMPORTS` edges exist for resolved imports
   - Unresolved imports flagged (e.g., via warning output)

**Expected Output:**
- Correct number of File and Symbol nodes
- IMPORTS edges for resolved imports
- Warning messages for unresolved imports
- No errors during ingestion

**Failure Criteria:**
- Incorrect node counts
- Missing IMPORTS edges for resolved imports
- No warnings for unresolved imports
- Parser crashes

---

### FR-6: generate-verification Scripted Hook

**Validation Method:** Integration test with task specification

**Test Steps:**
1. Create a task spec declaring scope: `--scope src/file1.py,src/file2.py`
2. Modify a file: `echo "# change" >> src/file1.py` (within scope)
3. Run `generate-verification` with the task
4. Verify pass (diff within reachable set)
5. Deliberately modify an out-of-scope file: `echo "# out of scope" >> src/external.py`
6. Run `generate-verification` again
7. Verify task fails with error message indicating the out-of-scope file was detected

**Expected Output:**
- First run: Task passes
- Second run: Task fails with message like "Diff touches files outside reachable set: src/external.py"

**Failure Criteria:**
- Task passes despite out-of-scope modification
- No error message or unclear error
- Task fails for in-scope modification

---

### FR-7: BariaDAO Pilot

**Validation Method:** End-to-end integration test

**Test Steps:**
1. Navigate to BariaDAO project root
2. Run `graph-context init baria`
3. Verify `.omp/graph/baria.lbug` created
4. Run `graph-context ingest --skeleton skeleton.md --graph .omp/graph/baria.lbug`
5. Query graph: `lbug --db .omp/graph/baria.lbug cypher "MATCH (n) RETURN labels(n), count(n)"`
6. Verify all files from skeleton.md are represented
7. Run ad hoc query: `lbug --db .omp/graph/baria.lbug cypher "MATCH (f:File)-[:IMPORTS]->(s:Symbol) WHERE f.name CONTAINS 'core' RETURN f.name, s.name"`
8. Verify agent bash session can execute the query

**Expected Output:**
- Graph populated with correct node and edge counts
- Query returns meaningful results
- Bash execution succeeds

**Failure Criteria:**
- Graph not populated
- Query returns empty or incorrect results
- Bash execution fails

---

## Edge Cases

- **Empty skeleton.md**: Parser should handle files with no File sections gracefully (no nodes created).
- **Single File Project**: Graph should contain only one File node with all its Symbols and IMPORTS.
- **Circular Imports**: Graph may contain cycles; parser should handle without errors.
- **Deeply Nested Imports**: Parser should resolve imports with multiple path components (e.g., `from package.module import function`).
- **Non-Python Import Syntax**: Parser should gracefully handle imports outside Python (e.g., JS `import`, CSS `@import`) without crashing.
- **Symbol Ambiguity**: Multiple symbols with the same name in different Files should be distinguished by file reference.
- **File Path Normalization**: Parser should handle varying path formats (relative vs absolute, trailing slashes).

---

## Failure Scenarios

### Verification Hook Failure

- **Scenario**: Out-of-scope edit passes verification (gate does not gate)
  - **Cause**: Cypher query returns incorrect reachable set
  - **Validation**: Confirm query correctly includes all imports and that actual diff is outside reachable set
  - **Fix**: Adjust Cypher query logic in verification hook

- **Scenario**: In-scope edit fails verification (false positive)
  - **Cause**: Cypher query incorrectly excludes files reachable via imports
  - **Validation**: Verify import resolution logic and edge creation
  - **Fix**: Correct import resolution in parser

### Graph Initialization Failure

- **Scenario**: Graph file not created due to permission errors
  - **Cause**: No write access to `.omp/` directory
  - **Validation**: Check directory permissions before ingestion
  - **Fix**: Grant write access or adjust path

- **Scenario**: Schema definition fails due to malformed Cypher
  - **Cause**: Invalid schema syntax in graph-context SKILL.md
  - **Validation**: Execute schema definition query directly with lbug
  - **Fix**: Correct schema definition syntax

### Parser Failure

- **Scenario**: Unresolved imports cause parser to crash
  - **Cause**: Parser attempts to create edges for non-existent nodes
  - **Validation**: Run parser with verbose output to see error messages
  - **Fix**: Implement defensive handling for unresolved imports

### Bash Access Failure

- **Scenario**: Agent bash session cannot find `lbug` command
  - **Cause**: PATH not configured correctly during skill injection
  - **Validation**: Test from fresh shell in agent session
  - **Fix**: Adjust PATH configuration or installation script

---

## Regression Checklist

### graph-context Skill

- [x] SKILL.md remains complete and navigable
- [x] Injectability instructions do not conflict with other skills
- [x] No changes to existing graph-context functionality if previously modified

### generate-verification Skill

- [x] Original verification steps remain functional
- [x] New scripted hook integrates without breaking existing verification flow
- [x] No changes to agent-facing tool selection logic

### AEF Environment

- [x] `uv add ladybug` does not conflict with existing Python dependencies
- [x] `lbug` CLI does not shadow other command-line tools with same name
- [x] No unintended PATH modifications to global shell environment

---

## Manual Validation

1. **Lbug CLI Installation**:
   - Open a new terminal and run `lbug --version`
   - Confirm version information is displayed correctly
   - Try running `lbug --help` to confirm command is usable

2. **graph-context Skill Documentation**:
   - Read `~/devcode/aef/agent/skills/graph-context/SKILL.md`
   - Confirm injectability instructions are clear
   - Verify schema definition is documented
   - Confirm expected usage patterns are described

3. **Pilot Graph Inspection**:
   - Navigate to BariaDAO project root
   - Open `.omp/graph/baria.lbug` in a text editor
   - Verify file structure matches expected schema (File, Symbol, IMPORTS nodes)
   - Run sample Cypher queries manually to confirm queryability

4. **Verification Hook Validation**:
   - Create a small test project with known scope
   - Make an in-scope change and run generate-verification
   - Confirm the task passes
   - Make an out-of-scope change and run generate-verification again
   - Confirm the task fails with a clear error message

5. **Agent Bash Access**:
   - Start an agent session
   - Attempt to run `lbug --db .omp/graph/baria.lbug cypher "MATCH (n) RETURN count(n)"`
   - Confirm the command executes successfully
   - Try a more complex query (e.g., find imports for a specific file)

---

## Automated Validation

#### Diff-Scope Verification (Pre-Merge Check)

**Command:** `git diff --name-only`

**Assertion:** The output of this command MUST strictly match the "Allowlist" defined in M3S1 Specification. If any file appears in the diff that is not on the Allowlist, the test automatically FAILS. The agent must revert the out-of-scope file before proceeding.

**Allowlist (Files permitted to change):**
- `~/devcode/aef/agent/.omp/config.yml` (if adding ladybug to AEF dependencies)
- `~/devcode/aef/agent/skills/` (create `graph-context/` subdirectory)
- `~/devcode/aef/agent/skills/generate-verification/SKILL.md` (add scripted verifier hook step)
- `<project>/.omp/graph/<name>.lbug` (new graph file created for each project)

**Failure Criteria:**
- Any file outside allowlist appears in git diff
- Out-of-scope files committed or staged

#### Python Client Installation

**Command:** `python -c "import ladybug; print('ladybug installed successfully')"`

**Assertion:** Ladybug Python client must be importable without errors.

**Failure Criteria:**
- ImportError raised
- Import succeeds but `ladybug` module has no attributes

#### graph-context Skill Existence

**Command:** `test -f ~/devcode/aef/agent/skills/graph-context/SKILL.md && echo "SUCCESS"`

**Assertion:** graph-context skill SKILL.md must exist.

**Failure Criteria:**
- File not found
- File exists but is empty or contains only placeholder text

#### Graph Schema Validation

**Command:** 
```bash
mkdir -p /tmp/test-ladybug/.omp
cd /tmp/test-ladybug
graph-context init test-ladybug
lbug --db .omp/graph/test-ladybug.lbug cypher "SHOW SCHEMA"
```

**Assertion:** Schema must define only File, Symbol, and IMPORTS node/edge types.

**Failure Criteria:**
- Schema shows invalid or missing types
- Schema contains extra node/edge types

#### Parser Correctness Test

**Command:** (Create sample skeleton.md, run parser, verify counts)
```bash
cat > /tmp/test-skeleton.md << 'EOF'
### File: /tmp/test-file.py
import os
from pathlib import Path

def foo():
    pass

class Bar:
    def __init__(self):
        self.x = 1

async def baz():
    pass

### File: /tmp/test-file2.py
import sys
EOF

mkdir -p /tmp/test-graph/.omp
cd /tmp/test-graph
graph-context init test
graph-context ingest --skeleton /tmp/test-skeleton.md --graph .omp/graph/test.lbug
lbug --db .omp/graph/test.lbug cypher "MATCH (n) RETURN labels(n), count(n)"
```

**Assertion:** Parser must create correct number of File and Symbol nodes, and IMPORTS edges for resolved imports.

**Failure Criteria:**
- Incorrect node counts
- Missing or incorrect edge types
- Parser crashes with errors

#### Verification Hook Integration Test

**Command:** (Simulate task with in-scope and out-of-scope changes)
```bash
# Create test project with declared scope
mkdir -p /tmp/test-task/src
echo "# in-scope" > /tmp/test-task/src/main.py
echo "# out of scope" > /tmp/test-task/src/external.py

# Declare scope (files in src/main.py)
echo "scope: src/main.py" > /tmp/test-task/task-spec.txt

# Modify in-scope file
echo "# changed" >> /tmp/test-task/src/main.py

# Run verification (should pass)
# ...

# Modify out-of-scope file
echo "# unscoped" >> /tmp/test-task/src/external.py

# Run verification again (should fail)
# ...
```

**Assertion:** Verification hook must pass for in-scope changes and fail for out-of-scope changes.

**Failure Criteria:**
- Verification passes for out-of-scope change
- Verification fails for in-scope change

#### BariaDAO Pilot Validation

**Command:**
```bash
cd /path/to/baria
graph-context init baria
lbug --db .omp/graph/baria.lbug cypher "MATCH (n) RETURN labels(n), count(n)"
lbug --db .omp/graph/baria.lbug cypher "MATCH (f:File) RETURN f.name, count(f)-1"
```

**Assertion:** BariaDAO graph must be populated with correct node and edge counts from skeleton.md.

**Failure Criteria:**
- Graph not created or not populated
- Node/edge counts incorrect
- Query returns empty results

---

## Performance Considerations

- **Graph Size**: For small to medium projects (hundreds of files), graph creation must complete within 5 seconds.
- **Query Performance**: Cypher queries over the graph must execute within 2 seconds for typical patterns (e.g., finding all imports for a file).
- **Parser Scalability**: Parsing skeleton.md with 1000+ lines must not exceed 30 seconds and should complete in under 10 seconds for typical projects.

**Baseline Metrics to Capture:**
- Time to initialize graph for BariaDAO
- Time to parse skeleton.md for BariaDAO
- Query execution time for sample queries (e.g., "find all imports")

**Thresholds:**
- Graph initialization < 5 seconds
- Parser execution < 30 seconds (1000 lines)
- Query execution < 2 seconds

---

## Security Considerations

- **Input Validation**: Parser must sanitize import paths to prevent injection attacks (e.g., preventing `../../etc/passwd` traversal).
- **Path Traversal Prevention**: Graph file paths must be validated to ensure they are within project root.
- **Permission Checks**: graph-context skill must verify write access to `.omp/` directory before creating graph files.
- **Unresolved Import Handling**: Parser should not attempt to create edges for nodes that don't exist (prevents malformed graph state).

**Validation Steps:**
- Test parser with path traversal attempts (e.g., `import ../../../etc/passwd`)
- Test graph creation with restricted write access
- Verify parser does not crash on malicious input

---

## Observability

### Logs That Must Be Emitted

- **Parser Logs**: Status messages indicating progress (e.g., "Processing File: src/main.py", "Import resolved: os", "Unresolved import: nonexistent_module")
- **Verification Hook Logs**: Diff comparison results (e.g., "Diff matches reachable set: PASS", "Diff touches out-of-scope file: src/external.py - FAIL")
- **Error Logs**: Clear error messages for failures (e.g., "Graph initialization failed: permission denied", "Parser crashed: line 45: syntax error")

### Metrics That Must Be Recorded

- **Graph Population Time**: Time to ingest skeleton.md (for performance tracking)
- **Verification Success Rate**: Number of verification passes vs failures (to measure gate effectiveness)
- **Unresolved Import Count**: Number of imports that could not be resolved (to identify potential issues)
- **Parser Runtime**: Execution time of skeleton.md parser (for performance monitoring)

### Debug Output

- Verbose mode (`--verbose` or `-v`) for parser and verification hook to show:
  - All nodes and edges created
  - All diff changes compared against reachable set
  - All import resolution steps (successful and failed)

---

## Expected Outcomes

**Observable Success Indicators:**

1. **Tooling**: Agent sessions can successfully execute `lbug --version` and run ad hoc Cypher queries against BariaDAO's graph.

2. **Skill Injection**: Any AEF project can have `graph-context` injected and initialized with a single command, creating a valid `.omp/graph/<name>.lbug` file.

3. **Parser Correctness**: The skeleton.md parser correctly converts all File, Symbol, and IMPORTS entities into graph nodes and edges, with unresolved imports flagged but not causing crashes.

4. **Verification Gate**: The generate-verification scripted hook mechanically validates that all changes are within the reachable set from declared scope, automatically failing any out-of-scope edit attempt with a clear error message.

5. **Pilot Success**: BariaDAO's graph is fully populated from its current skeleton.md and queryable, with all 10 acceptance criteria satisfied.

**Gate Effectiveness Evidence:**

- An agent session (or user) deliberately creates an out-of-scope edit and the verification hook immediately fails the task, demonstrating that the gate is not just a cosmetic step but an active gatekeeper of scope violations.
- No false positives occur (in-scope edits pass verification correctly).

**Documentation Completeness:**

- graph-context SKILL.md provides clear instructions on injectability, usage, and schema.
- Verification hook integration is documented in generate-verification's pipeline.
- All commands and test procedures are traceable and repeatable.

---

## Next Steps

Advise running `generate-tests` to create executable test scripts and then `implement-specification` to execute the implementation.
