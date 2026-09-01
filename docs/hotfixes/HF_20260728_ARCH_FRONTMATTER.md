---
id: HOT-001
type: hotfix
title: "Hotfix: ARCH metadata validation, Tier 3 hardening, shared frontmatter"
milestone_id: M7
status: completed
template_version: 1.0.2
impact: MODERATE
---

#### Literal Checklist Executed

1. **ARCH prefix registration**: Updated `validate_metadata.py` to register `ARCH` as a valid system prefix with `"architecture"` type. Updated `docs/ARTIFACT_ARCHITECTURE.md` `type` from `specification` to `architecture`.

2. **Tier 3 heuristic hardening**: Replaced the loose `fname.startswith(identifier)` + all-letters tuple check in `resolve_artifact.py` with a strict boundary check using `stem` (without extension) and a `VALID_LEGACY_SUFFIXES` frozenset (`{V, T, C, E, R, I, H}`). The character after the identifier must be `.` (via exact stem match) or a valid suffix letter optionally followed by a digit index.

3. **Shared YAML frontmatter module**: Created `bin/_frontmatter.py` with `extract_frontmatter(filepath)` function. Both `validate_metadata.py` and `resolve_artifact.py` now import and use this shared module, ensuring absolute structural consistency in YAML frontmatter parsing.

4. **--cwd CLI documentation**: Added a `CLI Reference` subsection to `docs/ARTIFACT_ARCHITECTURE.md` §6 documenting the `--cwd` argument alongside the other CLI arguments.

#### Mechanical Code Changes

| File | Change | Lines |
|------|--------|-------|
| `bin/_frontmatter.py` | **Created** — shared `extract_frontmatter()` function | 47 |
| `bin/validate_metadata.py` | Replaced `import yaml` + inline YAML parsing with `from _frontmatter import extract_frontmatter`; added `ARCH` to `CANONICAL_ID_PATTERN`; added `"architecture"` to `ALLOWED_TYPES` | +13 -20 |
| `bin/resolve_artifact.py` | Replaced `import yaml` with `from _frontmatter import extract_frontmatter`; reimplemented `resolve_yaml_frontmatter` as thin wrapper; hardened Tier 3 with `stem`-based strict suffix boundary check | +33 -25 |
| `docs/ARTIFACT_ARCHITECTURE.md` | Changed `type: specification` to `type: architecture`; added `CLI Reference` subsection documenting `--cwd` | +17 -1 |

#### Verification Results

- **All 9 M7 tests**: PASS (exit 0)
- **`validate_metadata.py docs/ARTIFACT_ARCHITECTURE.md`**: `OK: docs/ARTIFACT_ARCHITECTURE.md — metadata valid` (exit 0)
- **M1-M9 artifacts untouched**: SHA256 hash of all 80 milestone `.md` files confirmed stable; `git status` shows only `bin/validate_metadata.py` as modified (expected) plus pre-existing changes unrelated to this hotfix.
