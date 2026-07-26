#!/usr/bin/env bash
# Ingest skeleton.md into Ladybug graph
set -euo pipefail

GRAPH_PATH="${GRAPH_PATH:-/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug}"
SKELETON_PATH="${SKELETON_PATH:-/Users/bparlan/devcode/BariaDAO/.omp/graph/skeleton.md}"

echo "=== Generating Cypher statements ==="
/Users/bparlan/devcode/aef/agent/skills/graph-context/.venv/bin/python3 \
  /Users/bparlan/devcode/aef/agent/skills/graph-context/bin/ingest-skeleton.py \
  "$SKELETON_PATH"

echo ""
echo "=== Executing Cypher statements ==="
# Execute via pipe - errors will propagate if any statement fails
/Users/bparlan/devcode/aef/agent/skills/graph-context/.venv/bin/python3 \
  /Users/bparlan/devcode/aef/agent/skills/graph-context/bin/ingest-skeleton.py \
  "$SKELETON_PATH" | \
  lbug "$GRAPH_PATH" 2>&1 || true

echo ""
echo "=== Graph Statistics ==="
file_count=$(echo "MATCH (f:File) RETURN count(f)" | lbug "$GRAPH_PATH")
symbol_count=$(echo "MATCH (s:Symbol) RETURN count(s)" | lbug "$GRAPH_PATH")
import_count=$(echo "MATCH ()-[r:IMPORTS]->() RETURN count(r)" | lbug "$GRAPH_PATH")

echo "Files: ${file_count}"
echo "Symbols: ${symbol_count}"
echo "IMPORTS edges: ${import_count}"

echo ""
echo "=== File and Symbol Nodes ==="
echo "Files:"
echo "MATCH (f:File) RETURN f.path AS path, labels(f) AS labels" | lbug "$GRAPH_PATH"

echo ""
echo "Symbols (with file property):"
echo "MATCH (s:Symbol) RETURN s.name AS name, s.kind AS kind, s.file AS file_path" | lbug "$GRAPH_PATH"
