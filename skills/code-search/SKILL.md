---
name: code-search
version: 1.0.0
description: Semantic repository search and skeleton generation for OMP AEF infrastructure.
tools: bash, read, write
user-invocable: true
---

# Code Search Skill — Infrastructure Core

Best for low-token code understanding. Use before reading full files.

**Role in OMP AEF:**
- Enables semantic repository understanding for all framework operations
- Helps agents understand codebase structure and patterns
- Supports framework improvements and analysis
- Reduces token usage for large codebase navigation

## Tools

- `generate_skeletons` — Tree-sitter extraction of signatures/imports
- `refresh_index` — Rebuild vector embeddings (requires ollama)
- `search_code(query, limit?)` — Semantic search

## Capabilities

- Semantic repository search
- Tree-sitter skeleton generation
- Repository indexing

## Preferred Usage

- Use before reading many source files.
- Prefer semantic search over exhaustive file reading.
- Prefer generated skeletons when architectural understanding is sufficient.
- Only inspect implementation files when additional detail is required.

## Output

- Skeletons: `docs/skeletons/{project}_skeleton.md`
- Vector DB: `code_index_{project}.db` (per-project)

## Requirements

- `tree-sitter` + `tree-sitter-language-pack` (installed)
- Optional: `ollama` + `sqlite-vec` for semantic search

**For detailed usage, patterns, and integration with framework skills, see:**
- **[code-search/README.md](./README.md)** — Complete infrastructure documentation


## Documentation

- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
