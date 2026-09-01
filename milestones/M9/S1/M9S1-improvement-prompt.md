# M9S1 Improvement Prompt

## Context
`milestones/M9/M9.md` is structurally sound. The path breakage is not in this file.

The problematic references are in:
- `milestones/M9/S1/SPEC-M9S1.md`
- `milestones/M9/S1/VER-M9S1V.md`
- `milestones/M9/S1/M9S1T1.md`

These still reference removed or relocated paths from an older infrastructure layout.

## Healthy Canonical Infrastructure (use these)
- `core/validation.py` — canonical validation API: `validate_metadata(artifact_path)`, `validate_artifact(metadata)`, result dataclasses
- `core/artifacts/metadata.py` — frontmatter parsing: `parse_metadata(content)`, `get_metadata_from_file(file_path)`, `extract_frontmatter(filepath)`
- `core/artifacts/registry.py` — type registry: `ArtifactRegistry`, `get_registry()`, `register_type()`, `get_storage_rule()`, relationship tracking
- `core/artifacts/resolution.py` / `core/artifacts/resolve.py` — resolution: `resolve_artifact(...)`, `construct_canonical_path(...)`
- `core/artifacts/types.py` — type definitions and enum
- `core/artifacts/errors.py` — error classes

## Removed / Dead Infrastructure (do not reference)
- `src/core/artifacts/` — removed duplicate tree
- `src/omp_cli/` — removed dead package
- `bin/validate_metadata.py` — removed redundant standalone validator
- `bin/_frontmatter.py` — superseded by `core/artifacts/metadata.py`

## Required Fixes for S1 documents
1. Replace every `src/core/artifacts/...` reference with `core/artifacts/...`
2. Replace every `src/omp_cli/...` reference with `core/validation.py` or `core/artifacts/metadata.py`
3. Update CLI invocation examples from `python src/omp_cli/validate_metadata.py ...` to direct use of `core.validation`
4. Remove checklist items for deleted files: `src/omp_cli/validate_metadata.py`, `src/omp_cli/validators.py`
5. Add a note that `core/validation.py` is the single source of truth for validation behavior

## Suggested Improvement
Keep M9S1 narrow: validation belongs in `core/validation.py`; frontmatter parsing belongs in `core/artifacts/metadata.py`; resolution and registry belong in `core/artifacts/*`. Do not reintroduce parallel `bin/` or `src/` wrappers for these concerns.
EOF
