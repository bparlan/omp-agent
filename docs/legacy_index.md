# Legacy Artifact Index

## Overview

The OMP AEF Legacy Artifact Index provides a non-destructive mechanism for
discovering, classifying, and resolving pre-M10 milestone artifacts (M1-M9)
that predate the canonical YAML frontmatter contract.

## Components

### 1. `bin/legacy_indexer.py`

Read-only utility that scans M1-M9 milestone directories, computes SHA-256
checksums for every file, and classifies each artifact via a strict 6-tier
fallback system.

**CLI:**
```
python3 bin/legacy_indexer.py [--milestone-dir <path>] [--output <path>]
                              [--verbose] [--pattern-map <path>]
```

- `--milestone-dir`: Base path for M1-M9 directories (default: `milestones/`)
- `--output`: Output path for legacy manifest (default: `milestones/M7/legacy_manifest.txt`)
- `--verbose`: Print classification trace per file to stderr
- `--pattern-map`: Path to custom filename→type mapping file for Tier 5

**Exit codes:** `0` = success, `1` = failure

### 2. `bin/resolve_artifact.py` (updated)

The resolution engine now includes a Tier 4 fallback that consults the legacy
manifest when Tier 3 (filename heuristics) produces no match.

## 6-Tier Classification Fallback

| Tier | Method | Source | Example |
|------|--------|--------|---------|
| 1 | YAML frontmatter metadata | `type` or `id` field | `type: specification` |
| 2 | Directory structure | Parent directory name | `specifications/` → `specification` |
| 3 | Top-level Markdown headers | `# Heading` on first line | `# Specification` → `specification` |
| 4 | Legacy filename naming | `M{X}S{Y}[SUFFIX][N].md` | `M3S1C.md` → `completion` |
| 5 | Custom pattern mapping | External mapping file | `custom-report.md:investigation` |
| 6 | Human review | No match from tiers 1-5 | `AMBIGUOUS_LEGACY_ARTIFACT` |

## Legacy Manifest Format

The legacy manifest is a text file with one entry per line:

**Classified entry:**
```
<SHA-256> <relative-path>
```

**Unclassified entry (Tier 6):**
```
<SHA-256> <relative-path> unclassified:AMBIGUOUS_LEGACY_ARTIFACT
```

### Example
```
a1b2c3d4e5f6... M2/M2SA1.md
f6e5d4c3b2a1... M3/M3S1C.md
```

## Legacy Filename Patterns (Tier 4)

| Pattern | Artifact Type |
|---------|---------------|
| `M{X}S{Y}.md` | specification |
| `M{X}S{Y}V.md` | verification |
| `M{X}S{Y}T{Z}.md` | test_set |
| `M{X}S{Y}C.md` | completion |
| `M{X}S{Y}E.md` | evaluation |
| `M{X}S{Y}R.md` | review |
| `M{X}S{Y}I{Z}.md` | investigation |
| `M{X}S{Y}H.md` | hotfix |

## Integrity Guarantees

- The indexer is **strictly read-only**: it never creates, renames, moves, or
  writes frontmatter to any M1-M9 file.
- All mappings are recorded solely in the external legacy manifest.
- Post-execution checksum verification can mechanically prove that no files
  were modified.

## Custom Pattern Mapping (Tier 5)

The `--pattern-map` option accepts a text file with one entry per line:
```
<filename>:<artifact_type>
```

Lines starting with `#` are ignored as comments.

## Integration Points

- **`resolve_artifact.py`** — automatically consults the legacy manifest at
  `{base_dir}/legacy_manifest.txt` or `{base_dir}/milestones/{M_id}/legacy_manifest.txt`
  as a Tier 4 fallback after filename heuristics fail.
- **CI/CD** — run `legacy_indexer.py` after any pre-M10 artifact changes to
  keep the manifest in sync.
