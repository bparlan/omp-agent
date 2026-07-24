# Archive Docs Skill

Version: 1.3.0
Author: OMP Framework
Purpose: Archive completed milestone artifacts, infrastructure reports, and enforce 3-layer registry pattern structure

## Features

### 1. Milestone Archive
Archives completed milestone artifacts to `milestones/archive/M{X}/` with:
- Automatic artifact detection
- Review verification
- Archive summary generation
- MILESTONES.md updates

### 2. Infrastructure Archive
Archives infrastructure reports to `docs/archived/` with:
- Historical report management
- Archive summary generation
- Reference preservation

### 3. Structure Cleanup (NEW)
Enforces 3-layer registry pattern and cleans up project structure:
- Pre-cleanup verification
- File type mapping validation
- Layer separation enforcement
- Material change detection
- User approval workflow
- Automated execution
- Post-cleanup validation
- Rollback mechanism
- Compliance reporting

## Usage

### Milestone Archive

Archive completed milestone artifacts:
```
/archive-docs
```

Skill will:
1. Scan for milestone artifacts
2. Verify review and documentation exist
3. Create archive directory
4. Move artifacts
5. Generate archive summary
6. Update MILESTONES.md

### Infrastructure Archive

Archive infrastructure reports:
```
/archive-docs (mode: infrastructure)
```

Skill will:
1. Identify target infrastructure files
2. Verify historical status
3. Move to docs/archived/
4. Generate archive summary

### Structure Cleanup

Enforce 3-layer registry pattern:
```
/archive-docs (mode: structure-cleanup)
```

Skill will:
1. Scan for misplaced files
2. Detect violations
3. Present manifest to user
4. Execute approved changes
5. Validate functionality
6. Generate compliance report

## Validation Rules

### File Type Mapping

**Layer 1 (Data)**: `.json`, `.yaml`, `.yml`, `.sqlite`
**Layer 2 (View)**: `.html`, `.css`, `.js` (web/ or templates/)
**Layer 3 (Logic)**: `.py`, `.js` (src/ or tests/)
**Documentation**: `.md` (docs/ or root for README.md, AGENTS.md)
**Archived**: `.backup`, `.bak`
**Build Artifacts**: `.pyc`, `__pycache__`, `.pytest_cache`

### Directory Structure

```
PROJECT/
├── data/           # Layer 1: Data
├── src/            # Layer 3: Logic
├── web/            # Layer 2: View
├── templates/      # Template backups
├── scripts/        # Utilities
├── tests/          # Test suites
├── docs/           # Documentation
│   ├── content/
│   ├── milestones/
│   ├── hotfixes/
│   └── ingest/
└── README.md       # Entry point
```

## Output Formats

### Structure Cleanup Report

Comprehensive report including:
- Changes made (relocations, archives, deletions)
- Validation results per layer
- Functionality test results
- Rollback instructions
- Compliance status

### Archive Summary

Standardized archive summary for milestones and infrastructure.

## Safety Features

- **User Approval**: All structural changes require approval
- **Backups**: Original files preserved during relocation
- **Validation**: Functionality tested after changes
- **Rollback**: Clear rollback instructions provided
- **Audit Trail**: All changes logged and reported

## When to Use

### Structure Cleanup

After major refactors:
- Adding new features
- Merging branches
- Preparing for deployment
- Onboarding new contributors
- When structure has drifted

After hotfixes:
- Fixing routing issues
- Resolving template loading problems
- Cleaning up test artifacts

Regular maintenance:
- Weekly cleanup
- Pre-commit hook (optional)
- Pre-merge validation

## Compliance Reporting

The skill generates a comprehensive compliance report showing:

1. **Layer 1 Compliance**: All data files in correct location
2. **Layer 2 Compliance**: All view files in correct location
3. **Layer 3 Compliance**: All logic files in correct location
4. **Functionality Tests**: Server, homepage, API validation

## Examples

See the SKILL.md for detailed examples including:
- Cleanup after major refactor
- Cleanup before deployment
- Repeated cleanup for ongoing maintenance

## Integration

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
source ~/.omp/agent/skills/archive-docs/structure-cleanup.sh
```

### Pre-Merge Validation

```bash
#!/bin/bash
# CI/CD pre-merge check
source ~/.omp/agent/skills/archive-docs/structure-cleanup.sh --validate-only
```

## References

- [SKILL.md](SKILL.md) — Complete skill documentation
- [archive_template.md](../../templates/archive_template.md) — Archive template
- [infrastructure_fix_template.md](../../templates/infrastructure_fix_template.md) — Infrastructure template
