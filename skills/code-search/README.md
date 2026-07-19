# code-search Skill: Infrastructure Core

## Role in OMP AEF

`code-search` is an essential infrastructure skill that provides semantic repository understanding for all framework operations. It enables:

- **Rapid Codebase Understanding** — Understand structure and patterns without reading every file
- **Agent Coordination** — Helps agents understand how they fit into the broader framework
- **Framework Improvements** — Analyzes impact of changes across the entire codebase
- **Semantic Documentation** — Finds implicit knowledge patterns that are hard to search with text

## Usage in Framework Skills

### When code-search is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `evolve-skills` | Analyze failure patterns across artifacts | `search_code "Out of Scope"` |
| `session-audit` | Understand impact of framework changes | `search_code "agent handoff"` |
| `implement-specification` | Find existing patterns in codebase | `search_code "TODO:"` |
| `sync-documentation` | Verify documentation consistency | `search_code "template_version"` |
| Any agent | Understand codebase structure | `generate_skeletons` |

### Integration Points

**Agent Handoff Patterns:**
```bash
search_code "->" --limit 50
```
Identifies how agents reference each other in the framework.

**Negative Guardrails:**
```bash
search_code "Never:" --limit 20
```
Finds all out-of-scope restrictions across skills.

**Template Usage:**
```bash
search_code "template_version"
```
Checks template version consistency across the framework.

**Code-Search Itself:**
```bash
search_code "code-search" --limit 20
```
Ensures code-search is properly integrated and documented.

## Requirements

### Prerequisites

1. **tree-sitter** + **tree-sitter-language-pack**
   ```bash
   pip install tree-sitter tree-sitter-language-pack
   ```

2. **Optional: ollama** + **sqlite-vec** (for semantic search)
   ```bash
   ollama serve
   pip install sqlite-vec
   ```

### Setup

1. **Initialize repository index:**
   ```bash
   refresh_index --project OMP-AEF
   ```

2. **Generate skeletons:**
   ```bash
   generate_skeletons --project OMP-AEF --output docs/skeletons
   ```

3. **Verify installation:**
   ```bash
   search_code "test" --limit 5
   ```

## Output

**Skeletons:**
- `docs/skeletons/OMP-AEF_skeleton.md` — Tree-sitter extracted signatures and imports

**Vector Database:**
- `code_index_OMP-AEF.db` — Semantic search index (per-project)

## Capabilities

### Semantic Search

```bash
search_code "agent handoff" --limit 20
```

**Returns:**
- File paths
- Line numbers
- Semantic relevance score
- Extracted context

### Skeleton Generation

```bash
generate_skeletons --project OMP-AEF
```

**Returns:**
- Structure overview
- Function/class signatures
- Import relationships
- Module dependencies

### Repository Indexing

```bash
refresh_index --project OMP-AEF
```

**Updates:**
- Tree-sitter AST for all source files
- Vector embeddings for semantic search
- File metadata and relationships

## Best Practices

### Before Reading Files

**Use code-search when:**
- You need to understand codebase structure
- You're searching for specific patterns
- You want to find all usages of a function/agent
- You're doing framework improvements

**Avoid code-search when:**
- You need exact line-by-line details
- You're working on specific implementation files
- You already have file context

### Pattern Finding

**Common patterns to search:**

1. **Agent handoffs:**
   ```bash
   search_code "milestone -> generate-spec"
   ```

2. **Out of scope restrictions:**
   ```bash
   search_code "Never:" --limit 20
   ```

3. **Template references:**
   ```bash
   search_code "template at" --limit 30
   ```

4. **Skill invocation patterns:**
   ```bash
   search_code "invoke" --limit 20
   ```

5. **Tool usage:**
   ```bash
   search_code "Use.*tool" --limit 20
   ```

## Integration with session-audit

When using `session-audit` for framework improvements:

1. **Scan for code-search usage:**
   ```bash
   search_code "code-search" --limit 20
   ```

2. **Identify gaps:**
   - Which skills should use code-search?
   - Are there implicit patterns not documented?

3. **Document findings:**
   - Add to Session Audit Report
   - Suggest integration points in `evolve-skills`

## Troubleshooting

**Index not found:**
```bash
refresh_index --project OMP-AEF
```

**Search returns no results:**
```bash
# Check if index is up to date
ls -la code_index_OMP-AEF.db
```

**Tree-sitter errors:**
```bash
# Reinstall tree-sitter-language-pack
pip install --upgrade tree-sitter tree-sitter-language-pack
```

## Maintenance

**Keep index updated:**
```bash
# After major framework changes
refresh_index --project OMP-AEF
```

**Review skeletons:**
```bash
cat docs/skeletons/OMP-AEF_skeleton.md
```

**Monitor usage:**
```bash
# Check which skills reference code-search
search_code "code-search" --limit 50
```
