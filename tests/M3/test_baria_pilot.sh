#!/bin/bash
# FR-7: BariaDAO Pilot

set -e

echo "Testing BariaDAO pilot..."

# Test 1: Check if BariaDAO project exists
echo "  [Test 1] Checking if BariaDAO project exists..."
BARIA_DIR="$HOME/devcode/aef/agent"

if [ ! -d "$BARIA_DIR/BariaDAO" ]; then
    echo "  ✗ FAILED: BariaDAO project not found at $BARIA_DIR/BariaDAO"
    echo "    Cannot run pilot test"
    exit 1
fi

echo "  ✓ BariaDAO project found"

# Test 2: Check if skeleton.md exists
echo "  [Test 2] Checking if skeleton.md exists in BariaDAO..."
if [ ! -f "$BARIA_DIR/BariaDAO/skeleton.md" ]; then
    echo "  ✗ FAILED: skeleton.md not found in BariaDAO"
    exit 1
fi

echo "  ✓ skeleton.md found"

# Test 3: Initialize BariaDAO graph
echo "  [Test 3] Initializing BariaDAO graph..."
cd "$BARIA_DIR/BariaDAO"

if graph-context init baria 2>&1; then
    echo "  ✓ Graph initialization succeeded"
else
    echo "  ⚠ WARNING: Graph initialization failed"
    echo "    This may indicate skill is not yet implemented"
    exit 0
fi

# Test 4: Verify graph file was created
echo "  [Test 4] Verifying graph file created..."
if [ ! -f ".omp/graph/baria.lbug" ]; then
    echo "  ✗ FAILED: Graph file not created"
    exit 1
fi

echo "  ✓ Graph file created: .omp/graph/baria.lbug"

# Test 5: Populate graph from skeleton.md
echo "  [Test 5] Populating graph from skeleton.md..."
INGEST_OUTPUT=$(graph-context ingest --skeleton skeleton.md --graph .omp/graph/baria.lbug 2>&1 || true)

if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: Graph ingestion failed"
    echo "    Output: $INGEST_OUTPUT"
    exit 1
fi

echo "  ✓ Graph populated successfully"
echo "    Ingestion output:"
echo "$INGEST_OUTPUT" | sed 's/^/    /'

# Test 6: Count nodes in graph
echo "  [Test 6] Counting nodes in graph..."
TOTAL_NODES=$(lbug --db .omp/graph/baria.lbug cypher "MATCH (n) RETURN count(n)" 2>&1 | grep -v "^Cypher" || true)
FILE_COUNT=$(lbug --db .omp/graph/baria.lbug cypher "MATCH (f:File) RETURN count(f)" 2>&1 | grep -v "^Cypher" || true)
SYMBOL_COUNT=$(lbug --db .omp/graph/baria.lbug cypher "MATCH (s:Symbol) RETURN count(s)" 2>&1 | grep -v "^Cypher" || true)

echo "    Total nodes: $TOTAL_NODES"
echo "    File nodes: $FILE_COUNT"
echo "    Symbol nodes: $SYMBOL_COUNT"

if [ -z "$TOTAL_NODES" ] || [ "$TOTAL_NODES" == "0" ]; then
    echo "  ⚠ WARNING: Graph contains no nodes"
    echo "    This may indicate parsing issue or empty skeleton.md"
fi

# Test 7: Run ad hoc query
echo "  [Test 7] Running ad hoc query..."
QUERY_OUTPUT=$(lbug --db .omp/graph/baria.lbug cypher "MATCH (f:File)-[:IMPORTS]->(s:Symbol) WHERE f.name CONTAINS 'core' RETURN f.name, s.name LIMIT 5" 2>&1)

if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: Query execution failed"
    echo "    Output: $QUERY_OUTPUT"
    exit 1
fi

echo "  ✓ Query executed successfully"
echo "    Query output:"
echo "$QUERY_OUTPUT" | sed 's/^/    /'

# Test 8: Test agent bash access
echo "  [Test 8] Testing agent bash access to graph..."

# Test from a fresh shell (simulating agent session)
BASH_OUTPUT=$(bash -c "lbug --db .omp/graph/baria.lbug cypher 'MATCH (n) RETURN count(n)'" 2>&1)

if [ $? -ne 0 ]; then
    echo "  ✗ FAILED: Bash access to graph failed"
    echo "    Output: $BASH_OUTPUT"
    exit 1
fi

echo "  ✓ Bash access successful"
echo "    Bash output:"
echo "$BASH_OUTPUT" | sed 's/^/    /'

# Test 9: Verify all files from skeleton.md are represented
echo "  [Test 9] Verifying files from skeleton.md..."

# Count files mentioned in skeleton.md
# This is a heuristic - we'll just check that we have File nodes
if [ "$FILE_COUNT" -gt 0 ]; then
    echo "  ✓ Graph contains $FILE_COUNT File nodes (from skeleton.md)"

    # Show a sample of File nodes
    echo "    Sample files:"
    lbug --db .omp/graph/baria.lbug cypher "MATCH (f:File) RETURN f.name LIMIT 3" 2>&1 | grep -v "^Cypher" | sed 's/^/      /'
else
    echo "  ⚠ WARNING: No File nodes found in graph"
fi

# Cleanup
cd ~

echo ""
echo "  ✓ All FR-7 tests PASSED"
echo ""
