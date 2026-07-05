# Code Search Skill

**Version: 2.1.0**

Low-token code understanding via tree-sitter skeletons and vector search.

## Structure

```
~/.omp/agent/skills/code-search/
├── SKILL.md           # Skill manifest
├── README.md          # This file
├── code_indexer.py    # Main implementation
├── code-search.sh     # CLI wrapper
└── check-health.sh    # Diagnostics
```

## Commands

| Command        | Purpose                              |
| -------------- | ------------------------------------ |
| `--skeletons`  | Generate signatures/imports markdown |
| `--search "q"` | Semantic search via embeddings       |
| `--refresh`    | Rebuild vector index (default)       |

## Output

- `docs/skeletons/{project}_skeleton.md` — Extracted code structure
- `code_index_{project}.db` — sqlite-vec database

## Requirements

- `tree-sitter` + `tree-sitter-language-pack`
- Optional: `ollama` + `sqlite-vec` for semantic search
