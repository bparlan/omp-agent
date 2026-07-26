### Hotfix Focus Report HF_20260726_verify-scope
| Property | Value |
| ------ | ------ |
| Document Type | Hotfix Focus |
| Identifier | HF_20260726_verify-scope |
| Date | 2026-07-26 |
| Documentation Impact | MODERATE |
| template_version | 1.0.0 |

--------------------------------------------------------------------------------

#### Literal Checklist Executed

1. Remove unconditional `return True` at line 125 in `check_graph_reachability()` — function must return actual graph query result.
2. Delete dead duplicate code (lines 126-176) entirely, including its hardcoded path `/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug`.
3. Fix `get_graph_path()` to resolve `.omp/graph/<project>.lbug` relative to the project root (walks up parents to find `.git`/`.omp`, then globs existing `.lbug` files or falls back to `<project-name>.lbug`).
4. Ingest README.md as third File node in the real graph.
5. Make genuine out-of-scope edit against the real repo, run the fixed `verify-scope.py`, capture literal terminal output showing rejection.

Also fixed two pre-existing bugs found during testing:
- `get_modified_files()` had bare `try:` with no `except`/`finally` or `return` — added `except Exception: return set()` and `return modified`.
- `normalize_path()` was called but never defined — added the function.

--------------------------------------------------------------------------------

#### Mechanical Code Changes

**File: `skills/graph-context/bin/verify-scope.py`**

| Change | Lines | Description |
| ------ | ----- | ----------- |
| Fix `get_graph_path()` | 10-30 | Replaced `Path.cwd() / 'graph.lbug'` default with parent-walking logic that finds project root via `.git`/`.omp`, then globs `.omp/graph/*.lbug` or constructs `<project-name>.lbug`. |
| Add `normalize_path()` | 45-47 | New function: `return str(Path(path).resolve())`. |
| Fix bare `try:` in `get_modified_files()` | 76-78 | Added `return modified` after the try block and `except Exception: return set()`. |
| Remove unconditional `return True` | 125 (deleted) | Removed the premature `return True` that made 51 lines of dead code unreachable. |
| Delete dead duplicate code | 126-176 (deleted) | Removed the exact duplicate of the `check_graph_reachability` logic with a hardcoded path. |
| Add proper `return True` | 136 | Added final `return True` after success print, at the actual end of the function. |

**Verification (4/7/8/11 tests, 1 real graph ingestion, 1 end-to-end rejection):**

1. **README.md ingestion**: `echo "MERGE (f:File {path: '...README.md'})" | lbug baria.lbug` — 3rd File node confirmed in graph.
2. **Graph-based rejection (file scope)**: `verify-scope.py --scope=src/app_routes.py --graph` rejects `src/new_file.py` as not reachable:
   ```
   FAILURE: Modified file not reachable from scope: src/new_file.py
   Reachable files from scope: {'/Users/bparlan/devcode/BariaDAO/src/app_routes.py'}
   FAILURE: Graph-based verification failed - modified files not reachable from scope
   ```
3. **Scope compliance rejection (root-level file)**: `verify-scope.py --scope=src/app_routes.py` rejects `scratch_root.py`:
   ```
   FAILURE: Diff touches files outside declared scope:
     - .omp/graph/baria.lbug
     - scratch_root.py
   ```

**Note**: The generate full Cypher from `ingest-skeleton.py` fails when Symbol nodes include `name2`/`kind2`/`file2` properties (not in actual lbug schema). File-only MERGEs succeed individually. This is a pre-existing ingest-skeleton.py issue, not part of this hotfix.

**Remaining Pre-existing Bugs** (not in hotfix scope):
- `check_scope_compliance()` treats sibling files (same parent directory) as in-scope for file scopes — masks some out-of-scope rejections.
