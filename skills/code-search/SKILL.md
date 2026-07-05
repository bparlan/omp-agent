---
name: code-search
tools: bash, read, write
user-invocable: true
---

# Code Search Skill

Best for low-token code understanding. Use before reading full files.

## Tools

- `generate_skeletons` — Tree-sitter extraction of signatures/imports
- `refresh_index` — Rebuild vector embeddings (requires ollama)
- `search_code(query, limit?)` — Semantic search

## Capabilities

- semantic repository search
- tree-sitter skeleton generation
- repository indexing

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