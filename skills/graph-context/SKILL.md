---
name: graph-context
version: 1.0.0
description: Ingest skeleton.md files into Ladybug graph for AEF projects with V1 schema (File, Symbol, IMPORTS nodes and edges).
tools: read, write, bash, glob, grep, eval
user-invocable: true
---

# Graph Context: Ingest Skeleton into Ladybug Graph

You are a graph context injection agent that transforms skeleton.md files into Ladybug graph upserts using the V1 schema. This skill provides injectability into any AEF project without requiring MCP integration.

## When to Invoke

Use when:
- You need to construct Ladybug graph structures from skeleton.md files
- Working with AEF projects that have code-search skeletons
- Upgrading the graph knowledge layer with source-level semantic information

## Your Process

### Phase 1: Initialize Graph Context (init-graph)

1. **Locate skeleton.md** — Use `glob` to find skeleton files in `~/.omp/skeletons/` or project-specific directories.
2. **Generate skeleton index** — Use code-search to index skeletons if not already present:
   ```bash
   code-search --index --skeletons
   ```
3. **Create graph-context output directory** — Set up a dedicated location for graph upserts:
   ```bash
   mkdir -p graph-context
   ```

### Phase 2: Ingest Skeleton (ingest-skeleton)

For each skeleton.md file:

1. **Parse skeleton.md** — Extract File, Symbol, and IMPORTS edges using the V1 schema parser (see Parser section).
2. **Generate Ladybug upsert JSON** — Format parsed data as Ladybug graph upserts:
   ```json
   {
     "files": [
       {
         "id": "file:///path/to/module.ts",
         "name": "module.ts",
         "path": "path/to/module.ts",
         "language": "typescript",
         "symbols": [
           { "id": "symbol://module.ts:Foo", "name": "Foo", "kind": "function" }
         ]
       }
     ],
* **No startNode() function**: You MUST NOT use a `startNode()` function or equivalent mechanism to initiate graph traversal or node creation; all graph construction must derive from `skeleton.md` parsing.
     "imports": [
       {
         "from": "file:///path/to/module.ts",
         "to": "file:///path/to/dependency.ts"
       }
     ]
   }
   ```
3. **Save to graph-context directory** — Persist upsert JSON for consumption by Ladybug graph.
4. **Flag unresolved imports** — Report any import statements without matching symbols in the codebase.

### Phase 3: Validate and Report

1. **Cross-reference imports** — Verify IMPORTS edges reference existing File nodes.
2. **Generate summary report** — Create a manifest of:
   - Files processed
   - Symbols extracted
   - IMPORTS edges created
   - Unresolved import warnings
3. **Provide next steps** — Advise how to consume graph-context outputs in downstream workflows.

## V1 Schema Definition

### Node Types

#### File Node
Represents a source code file in the graph.

**Properties:**
- `id` (string, required): Unique identifier (e.g., `file:///path/to/module.ts`)
- `name` (string, required): File name
- `path` (string, required): Absolute or relative path
- `language` (string, required): Programming language identifier (e.g., `typescript`, `python`, `rust`)
- `symbols` (array of Symbol nodes, optional): List of symbols defined in this file
- `lineCount` (integer, optional): Total number of lines in the file

**Example:**
```json
{
  "id": "file:///src/auth.module.ts",
  "name": "auth.module.ts",
  "path": "src/auth.module.ts",
  "language": "typescript",
  "symbols": [
    "symbol://auth.module.ts:AuthModule"
  ],
  "lineCount": 42
}
```

#### Symbol Node
Represents a named symbol (function, class, variable, etc.) in source code.

**Properties:**
- `id` (string, required): Unique identifier (e.g., `symbol://module.ts:Foo`)
- `name` (string, required): Symbol name
- `kind` (string, required): Symbol kind (e.g., `function`, `class`, `variable`, `interface`, `enum`, `const`)
- `fileId` (string, required): Reference to File node via `id`
- `lineNumber` (integer, optional): Line number where symbol is defined
- `parentSymbolId` (string, optional): Reference to parent class/interface for nested symbols

**Example:**
```json
{
  "id": "symbol://auth.module.ts:AuthService",
  "name": "AuthService",
  "kind": "class",
  "fileId": "file:///src/auth.module.ts",
  "lineNumber": 5,
  "parentSymbolId": null
}
```

### Edge Types

#### IMPORTS Edge
Represents an import relationship between two files.

**Properties:**
- `id` (string, required): Unique identifier (e.g., `import://module.ts:0->dependency.ts`)
- `from` (string, required): Source File node `id`
- `to` (string, required): Target File node `id`
- `kind` (string, optional): Import kind (e.g., `default`, `named`, `namespace`, `star`)
- `importStatement` (string, optional): Original import statement text

**Example:**
```json
{
  "id": "import://auth.module.ts:0->user.service.ts",
  "from": "file:///src/auth.module.ts",
  "to": "file:///src/user.service.ts",
  "kind": "named",
  "importStatement": "import { UserService } from './user.service'"
}
```

## Parser Documentation

### Parser Function (skeleton_to_graph)

The parser converts skeleton.md content into the V1 graph structure.

**Signature:**
```python
def skeleton_to_graph(skeleton_path: str) -> GraphDocument
```

**Input:**
- `skeleton_path` (str): Path to skeleton.md file

**Output:**
- `GraphDocument` (object):
  - `files`: List of File nodes
  - `imports`: List of IMPORTS edges

**Parser Workflow:**

1. **Read skeleton.md** — Parse YAML/Markdown format with File and Import sections:
   ```yaml
   files:
     - path: src/auth.module.ts
       name: auth.module.ts
       language: typescript
       symbols:
         - name: AuthService
           kind: class
           line: 5
   imports:
     - from: src/auth.module.ts
       to: src/user.service.ts
       kind: named
   ```

2. **Generate File Node IDs** — Convert paths to graph-URI format:
   - `src/auth.module.ts` → `file:///src/auth.module.ts`

3. **Generate Symbol Node IDs** — Combine fileId and symbol name:
   - `file:///src/auth.module.ts` + `AuthService` → `symbol://auth.module.ts:AuthService`

4. **Generate IMPORTS Edge IDs** — Combine `from` and `to`:
   - `file:///src/auth.module.ts` + `file:///src/user.service.ts` → `import://auth.module.ts:0->user.service.ts`

5. **Flag Unresolved Imports** — For each import, verify `to` file exists in File nodes. If not, add to `unresolved` list.

**Return Value:**
```python
{
  "files": [...],
  "imports": [...],
  "unresolved": [...],
  "metadata": {
    "source_path": skeleton_path,
    "file_count": 3,
    "symbol_count": 7,
    "import_count": 5
  }
}
```

**Error Handling:**
- Missing required fields → Skip entry, log warning
- Circular import detection → Flag with warning, continue processing
- Invalid URI format → Sanitize to basic alphanumeric with slashes

### Usage Example

```python
from graph_context.parser import skeleton_to_graph

# Parse a skeleton file
graph = skeleton_to_graph('~/.omp/skeletons/app.skeleton.md')

# Access parsed data
for file in graph['files']:
    print(f"File: {file['name']}")
    for symbol in file['symbols']:
        print(f"  Symbol: {symbol['name']} ({symbol['kind']})")

for imp in graph['imports']:
    print(f"{imp['from']} → {imp['to']}")

# Check unresolved imports
if graph['unresolved']:
    print(f"WARNING: {len(graph['unresolved'])} unresolved imports")
    for imp in graph['unresolved']:
        print(f"  {imp}")
```

## Injectability Instructions

### Requirements

This skill is injectable into any AEF project with minimal dependencies:

1. **Python 3.9+** — Required for parser implementation
2. **No MCP registration** — Skill operates entirely through bash, no agent-facing APIs
3. **Flag unresolved imports** — Conservative approach: report rather than fail

### Installation

1. **Clone or link this skill**:
   ```bash
   cd ~/devcode/aef/agent/skills
   git clone <repo> graph-context
   # or
   ln -s /path/to/graph-context graph-context
   ```

2. **Verify skill directory structure**:
   ```bash
   tree graph-context/
   # Output:
   # graph-context/
   # └── SKILL.md
   ```

3. **Ensure Python parser module exists**:
   ```bash
   # The parser should be bundled or referenced via relative import
   ls -la graph-context/parser.py
   ```

### Usage Without Full AEF Stack

This skill can operate in isolation:

```bash
# Initialize graph context in a project
cd /path/to/project
graph-context init-graph

# Ingest a specific skeleton
graph-context ingest-skeleton ~/.omp/skeletons/auth.skeleton.md

# Ingest all skeletons
graph-context ingest-skeleton --all
```

### Compatibility Notes

- **No code-search integration**: This skill assumes skeleton.md files are already present (generated by code-search or manually authored)
- **No Ladybug-MCP**: Consumed by downstream processes; skill outputs JSON that can be loaded via Ladybug graph API
- **Scope limited to BariaDAO**: This V1 schema is optimized for BariaDAO codebase; extend schema as needed for other projects
- **Graph output location**: Graph files are created in `.omp/graph/<project-name>.lbug` for each project

## CLI Tooling

### init-graph

Initialize graph context structure for a project.

**Usage:**
```bash
graph-context init-graph [options]
```

**Options:**
- `--output-dir PATH` — Output directory for graph files (default: `.omp/graph`)
- `--project-name NAME` — Project name (default: `baria`)

**Steps:**
1. Create output directory
2. Initialize Ladybug graph database with schema (File, Symbol, IMPORTS)
3. Create manifest.json with metadata
4. **Symbol nodes are now enforced (not skipped)**

**Example:**
```bash
cd ~/devcode/BariaDAO
graph-context init-graph --output-dir .omp/graph --project-name baria
# Output: .omp/graph/baria.lbug created
# Output: .omp/graph/manifest.json created
```

### ingest-skeleton

Ingest a skeleton.md file into the Ladybug graph.

**Usage:**
```bash
graph-context ingest-skeleton [options]
```

**Options:**
- `--skeleton PATH` — Path to skeleton.md file (required)
- `--graph-path PATH` — Ladybug graph file path (default: `.omp/graph/baria.lbug`)
- `--verbose` — Enable detailed logging

**Steps:**
1. Read and parse skeleton.md using V1 schema parser
2. Generate File nodes (one per file)
3. Generate Symbol nodes (one per function/class - **NOT SKIPPABLE**)
4. Generate IMPORTS edges (one per import statement)
5. Save to Ladybug graph via lbug CLI
6. Report unresolved import warnings

**Example:**
```bash
graph-context ingest-skeleton \
  --skeleton .omp/graph/skeleton.md \
  --graph-path .omp/graph/baria.lbug \
  --verbose
# Output: Files: 3, Symbols: 7, IMPORTS edges: 5
```

**Critical: Symbol Node Creation**
- Symbol nodes are **NOT SKIPPABLE** - every function, class, and variable defined in source files MUST be represented
- This bug was fixed in v1.0.1: graph recreation previously skipped Symbol table creation
- Verify Symbol nodes exist after ingestion:
  ```bash
  echo "MATCH (s:Symbol) RETURN count(s)" | lbug .omp/graph/baria.lbug
  ```

**Error Handling:**
- Missing skeleton file → Error
- Missing graph file → Error (run init-graph first)
- Parse errors → Report and skip invalid entries
- Circular imports → Report warning, continue processing

**Note:** This skill now provides full CLI implementation (not just documentation) for M3S1R remediation.
## Usage Examples

### Example 1: Initialize Graph Context in New Project

```bash
# Navigate to project
cd ~/devcode/baria-dao/src

# Initialize graph context structure
graph-context init-graph \
  --skeleton-dir ~/.omp/skeletons \
  --output-dir graph-context

# Output: graph-context/manifest.json created
# Output: graph-context/output/ directory created
```

### Example 2: Ingest a Single Skeleton

```bash
# Ingest authentication module skeleton
graph-context ingest-skeleton \
  --skeleton ~/.omp/skeletons/auth.skeleton.md \
  --output graph-context/auth.upsert.json \
  --verbose

# Output: graph-context/auth.upsert.json with File, Symbol, IMPORTS nodes
# Output: console reports: 3 files, 7 symbols, 5 imports, 0 unresolved
```

### Example 3: Ingest All Skeletons

```bash
# Ingest all skeletons for code-search index
graph-context ingest-skeletons \
  --skeleton-dir ~/.omp/skeletons \
  --output-dir graph-context

# Output: Multiple .json files in graph-context/
# Output: manifest.json aggregated statistics
```

### Example 4: Use Parser Programmatically

```python
#!/usr/bin/env python3
"""Example: Use graph-context parser in a script"""

import sys
sys.path.insert(0, '~/devcode/aef/agent/skills/graph-context')

from parser import skeleton_to_graph

# Parse skeleton
graph = skeleton_to_graph('~/.omp/skeletons/app.skeleton.md')

# Extract symbol dependencies
symbol_deps = {}
for imp in graph['imports']:
    if imp['from'] not in symbol_deps:
        symbol_deps[imp['from']] = []
    symbol_deps[imp['from']].append(imp['to'])

# Output dependencies
for file_id, deps in symbol_deps.items():
    print(f"{file_id} depends on: {', '.join(deps)}")

# Check unresolved
if graph['unresolved']:
    print("\nUnresolved imports:")
    for imp in graph['unresolved']:
        print(f"  {imp}")
```

### Example 5: Integrate with Downstream Workflows

```bash
# After ingestion, load into Ladybug graph
ladybug graph upsert graph-context/auth.upsert.json

# Query symbol dependencies
ladybug graph query "MATCH (f:File)-[:IMPORTS]->(t:File) WHERE f.name = 'auth.module.ts' RETURN t.name"
```

## Schema Evolution

### V1 (Current)
- File nodes
- Symbol nodes
- IMPORTS edges only
- No CALLS or RENDERS edges

### Future Extensions (Post-V1)
- CALLS edges (function/method call relationships)
- RENDERS edges (UI component rendering hierarchies)
- Symbol edge attributes (visibility, modifiers, generics)
- Cross-repo references

## References

- [skills.md](../../docs/skills.md) — Comprehensive skill catalog
- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [code-search](./code-search/SKILL.md) — Skeleton generation source
