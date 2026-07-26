### Hotfix Focus Report HF_20260726_verify-scope_v2
| Property | Value |
| ------ | ------ |
| Document Type | Hotfix Focus |
| Identifier | HF_20260726_verify-scope_v2 |
| Date | 2026-07-26 |
| Documentation Impact | MODERATE |
| template_version | 1.0.0 |

--------------------------------------------------------------------------------

#### Literal Checklist Executed

1. **File-scope graph traversal** — Extended graph query to run for file scopes too (previously only directory scopes queried the graph). Collapsed two near-duplicate `is_dir()` loops into one.
2. **Ladybug Python client** — Replaced `subprocess.run(['lbug', ...])` + box-drawing `split('│')` parsing with `ladybug.Database` / `ladybug.Connection` Python API. Has `ImportError` fallback to CLI scraping.
3. **`.omp/graph/*.lbug` exclusion** — One regex filter applied right after `get_modified_files()`, before any scope check runs.
4. **`check_scope_compliance()`** — Pasted for exact patch (pending).
5. **Ingest-skeleton Symbol schema** — Removed fabricated `name2`/`kind2`/`file2` suffixes from MERGE statement (now uses `name`/`kind`/`file`). Added `line` property. Ran `ALTER TABLE Symbol ADD line INT64;` against live DB. Re-ran ingestion.

--------------------------------------------------------------------------------

#### Mechanical Code Changes

**File: `skills/graph-context/bin/verify-scope.py`**

| Change | Lines | Description |
| ------ | ----- | ----------- |
| Add `import re` | 8 | Required for `.omp/graph/*.lbug` regex filter. |
| Rewrite `check_graph_reachability()` | 85-157 | Single unified loop builds `scope_filters` for both file and directory scopes. Queries IMPORTS edges via ladybug Python client (with CLI fallback). No dead code. |
| Add `.omp/graph/*.lbug` filter | 201-204 | `modified_files = {f for f in modified_files if not re.search(r'\.omp/graph/.*\.lbug$', f)}` applied after printing but before scope checks. |

**File: `skills/graph-context/bin/ingest-skeleton.py`**

| Change | Lines | Description |
| ------ | ----- | ----------- |
| Fix Symbol Cypher | 125 | `name2: '{name}', kind2: '{kind}', file2: '{file_path}'` → `name: '{name}', kind: '{kind}', file: '{file_path}', line: {symbol.get('line', 0)}` |
| Update comment | 117 | Reflects real schema properties. |

**Database schema change**:
```
ALTER TABLE Symbol ADD line INT64;
```
Applied against `/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug`.

--------------------------------------------------------------------------------

#### Verification

```
$ cd /Users/bparlan/devcode/BariaDAO
$ echo "x = 1" > src/new_file.py
$ /path/to/.venv/bin/python verify-scope.py --scope=src/app_routes.py --graph

Declared scope: ['src/app_routes.py']
Modified files: ['.omp/graph/baria.lbug', 'src/new_file.py']

Running graph-based verification...

FAILURE: Modified file not reachable from scope: src/new_file.py
Reachable files from scope: {'/Users/bparlan/devcode/BariaDAO/src/app_routes.py',
                             '/Users/bparlan/devcode/BariaDAO/src/data/content_loader.py'}

FAILURE: Graph-based verification failed - modified files not reachable from scope
```

Key evidence:
- `.omp/graph/baria.lbug` excluded by filter (printed in initial list but excluded from checks)
- `content_loader.py` in reachable set = graph IMPORTS query actually ran via ladybug
- `src/new_file.py` correctly rejected as not reachable from scope

**`check_scope_compliance()` patch is pending user input.**
