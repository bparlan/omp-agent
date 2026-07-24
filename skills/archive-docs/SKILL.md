---
name: archive-docs
version: 1.3.0
description: Archives completed milestone artifacts and infrastructure reports while preserving complete engineering history. Includes Structure Cleanup mode to enforce 3-layer registry pattern.
tools: bash, read, glob, write, edit, ast_grep, ask
user-invocable: true
---

# Archive Docs: Preserve Engineering History

You are a repository maintainer that archives completed milestone artifacts and infrastructure reports to reduce active context while preserving history. You also enforce 3-layer registry pattern structure.

## When to Invoke

Only execute when explicitly requested by user. Can be invoked for:
- **Documentation Archive**: Archiving completed milestones
- **Infrastructure Archive**: Archiving old infrastructure reports
- **Structure Cleanup**: Enforcing 3-layer registry pattern and cleaning up project structure

## Modes

### 1. Milestone Archive

Archives completed milestone artifacts (M{X}/*.md files) to `milestones/archive/M{X}/`.

**Process**:
1. Identify relevant artifacts using code-search
2. Verify prerequisites (review exists, docs synced)
3. Create archive directory
4. Move artifacts
5. Generate archive summary
6. Update MILESTONES.md

### 2. Infrastructure Archive

Archives infrastructure fix reports to `docs/archived/`.

**Process**:
1. Identify target files (FRAMEWORK_FIX_SUMMARY.md, INFRASTRUCTURE_FIXES.md, etc.)
2. Verify historical status
3. Create archive directory
4. Move artifacts
5. Generate archive summary

### 3. Structure Cleanup (NEW)

Enforces 3-layer registry pattern and cleans up project structure.

**When to Invoke**:
- When project structure doesn't comply with 3-layer pattern
- After major refactors
- When preparing for deployment
- Onboarding new contributors

**Pre-Cleanup Verification**:
1. Scan project for Layer 1, Layer 2, Layer 3 files
2. Verify file type mapping
3. Check file location compliance
4. Detect violations (e.g., Layer 2 file in root, Layer 1 file in src/)
5. Verify 3-layer separation rules

**Material Change Detection**:
- Files that need relocation
- Files that need archiving
- Files that can be safely deleted
- Import references that may need updating

**User Approval**:
Present manifest showing:
- Files to relocate with current and target paths
- Files to archive with reason
- Files to delete with warning
- Files unaffected

Request approval for each category or all.

**Execution**:
- Move files to correct locations
- Update import statements automatically where possible
- Create backup of original location
- Generate relocation log

**Post-Cleanup Validation**:
- Re-scan for 3-layer compliance
- Run smoke tests (server startup, homepage, API)
- Generate compliance report

**Rollback Mechanism**:
- Keep original file locations in backup
- Provide rollback command
- Log all changes for traceability

## Validation Rules

### File Type Mapping

**Layer 1 (Data)**: `.json`, `.yaml`, `.yml`, `.sqlite`
**Layer 2 (View)**: `.html`, `.css`, `.js` (only in `web/` or `templates/`)
**Layer 3 (Logic)**: `.py`, `.js` (only in `src/` or `tests/`)
**Documentation**: `.md` (only in `docs/` or root for README.md, AGENTS.md)
**Archived**: `.backup`, `.bak`
**Build Artifacts**: `.pyc`, `__pycache__`, `.pytest_cache`

### File Location Rules

1. Data files must be in `data/`
2. Templates must be in `web/` or `templates/`
3. Logic files must be in `src/` or `tests/`
4. Documentation must be in `docs/`
5. Backups must be in `docs/ingest/archived/` or `templates/*.backup`
6. Build artifacts must be excluded from source folders

### Layer Separation Rules

1. **No direct imports between Layer 1 and Layer 3**: Data files must be loaded through Layer 3
2. **Layer 2 files must be logic-less**: No Python/JS logic in HTML/CSS
3. **Layer 3 files must not directly read/write Layer 1 files**: All data access must go through proper loaders
4. **Templates**: `web/*.html` for served templates, `templates/*.html.j2` for Jinja2 sources

### Directory Structure Standards

```
PROJECT/
├── data/                    # Layer 1: Data (JSON/YAML)
│   └── {data_file}.json     # Source of truth
├── src/                     # Layer 3: Logic (Python/JS)
│   ├── {logic_file}.py      # Backend functions
│   └── module/              # Feature modules
├── web/                     # Layer 2: View (HTML/CSS)
│   ├── {template}.html      # Logic-less templates
│   └── static/              # Assets (images, fonts)
├── templates/               # Template backups
│   └── {template}.html.j2.backup
├── scripts/                 # Utilities
├── tests/                   # Test suites
├── docs/                    # Documentation
│   ├── content/             # All .md files
│   ├── milestones/          # Milestone artifacts
│   ├── hotfixes/            # Hotfix reports
│   ├── ingest/              # Temporary/Archived
│   │   └── archived/        # Archived files
│   └── skeletons/           # Design skeletons
└── README.md                # Entry point
```

## Structure Cleanup Process

### Step 1: Pre-Cleanup Verification

Scan the workspace to identify violations:

```bash
# Scan for misplaced files
find . -type f \( -name "*.md" \) -not -path "./docs/*" -not -path "./.git/*" -not -path "./README.md" -not -path "./AGENTS.md"
find . -type f \( -name "*.html" -o -name "*.css" \) -not -path "./web/*" -not -path "./templates/*"
find . -type f \( -name "*.json" -o -name "*.yaml" \) -not -path "./data/*"
find . -type f \( -name "*.py" -o -name "*.js" \) -not -path "./src/*" -not -path "./tests/*"
find . -type f \( -name "*.backup" -o -name "*.bak" \) -not -path "./templates/*" -not -path "./docs/ingest/*"

# Scan for build artifacts
find . -type d -name "__pycache__"
find . -type d -name ".pytest_cache"
find . -name "*.pyc"

# Scan for duplicates
find . -name "*.py" | xargs -n1 basename | sort | uniq -d
```

### Step 2: Material Change Detection

Compare findings against expected structure. Generate a manifest of changes needed.

**Categories**:
- **Relocations**: Files in wrong directory
- **Archivals**: Files to move to backup/archive
- **Deletions**: Build artifacts, temporary files
- **Ignored**: Root README.md, AGENTS.md, docs/ content

### Step 3: User Approval

Present manifest to user and request approval:

```
Structure Cleanup Manifest

Total Changes Detected: 23

Relocations:
- 12 .md files from root to docs/content/
- 1 milestone from root to docs/milestones/

Archivals:
- 3 backup files to docs/ingest/archived/
- 1 template backup to templates/

Deletions:
- 15 build artifacts (__pycache__, .pyc)
- 2 test reports

Action Required:
[ ] Approve all changes
[ ] Approve specific categories
[ ] Cancel cleanup
```

### Step 4: Execution

Execute approved changes:

```bash
# Move .md files to docs/content/
mv *.md docs/content/ 2>/dev/null || true

# Move milestones to docs/milestones/
mv milestones/ docs/milestones/ 2>/dev/null || true

# Move backups to archive
mkdir -p docs/ingest/archived
mv *.backup docs/ingest/archived/ 2>/dev/null || true
mv *.bak docs/ingest/archived/ 2>/dev/null || true

# Remove build artifacts
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Remove test reports (user approval required for this)
rm -f test_report.json 2>/dev/null || true
```

### Step 5: Post-Cleanup Validation

Verify compliance and functionality:

```bash
# Re-scan for 3-layer compliance
# (Run the same scan commands from Step 1)

# Test server startup
python3 main_demo.py &

# Test homepage
curl http://localhost:8000 | head -20

# Test API endpoint
curl http://localhost:8000/api/content
```

### Step 6: Generate Compliance Report

Create `docs/structure-compliance-report.md` with results.

## Output

### Structure Cleanup Report

```markdown
# Project Structure Cleanup Report

**Date:** YYYY-MM-DD
**Status:** ✅ COMPLETED / ❌ ABORTED

## Changes Made

### Relocations
| File | From | To |
|------|------|-----|
| `project/cleanup_guide.md` | `/` | `docs/content/` |

### Archives
| File | Reason | Archived To |
|------|--------|-------------|
| `templates/index.html.j2` | Backup | `templates/index.html.j2.backup` |

### Deletions
| File | Reason |
|------|--------|
| `__pycache__/file.pyc` | Build artifact |
| `test_report.json` | Temporary file |

## Validation Results

### Layer 1 Compliance
- ✅ All files in `data/` are JSON/YAML
- ✅ No files in `src/` or `web/` are JSON/YAML

### Layer 2 Compliance
- ✅ All HTML/CSS in `web/`
- ✅ Templates in `templates/` or `web/`

### Layer 3 Compliance
- ✅ All Python/JS in `src/` or `tests/`
- ✅ No misplaced logic files

### Functionality Tests
- ✅ Server starts: `python3 main_demo.py`
- ✅ Homepage loads: http://localhost:8000
- ✅ API endpoint: http://localhost:8000/api/content

## Rollback Instructions

To revert all changes:
```bash
git restore --source=HEAD docs/content/cleanup_guide.md
```

## Files Affected

**Total Changes:** 3 relocations, 1 archive, 5 deletions
**Original State:** 47 files
**Final State:** 39 files

## Compliance Status

**3-Layer Registry Pattern:** ✅ COMPLIANT
**Layer Separation:** ✅ ENFORCED
**Documentation Centralized:** ✅ YES
**Build Artifacts Clean:** ✅ YES
```

### Milestone Archive Structure

```
milestones/archive/
└── M{X}/
    ├── M{X}.md
    ├── M{X}S{Y}.md
    ├── M{X}S{Y}V.md
    └── M{X}S{Y}R.md
```

### Docs Archive Structure

```
docs/archived/
├── FRAMEWORK_FIX_SUMMARY.md
├── FRAMEWORK_HEALTH_REPORT.md
├── INFRASTRUCTURE_FIXES.md
└── INGEST_ENTRIES.md
```

## Change Detection

Update documentation only when material changes occurred:

| Triggers documentation update | Ignored items          |
| ----------------------------- | ---------------------- |
| Architecture changes          | Refactoring            |
| Public API changes            | Formatting changes     |
| Repository structure changes  | Implementation details |
| Configuration changes         | Temporary experiments  |
| Operational procedures        | Review comments        |
| User-visible behavior         | Internal discussions   |
| Deployment changes            |                        |
| Workflow changes              |                        |
| Supported platforms           |                        |
| Ingestion entries processed   | Cosmetic changes       |
| Architectural Drift            | Triggers documentation update AND diagrammer regeneration |

## Archive Principles

- **Maintain relationships** — Keep all related artifacts together
- **Keep filenames** — Preserve original names for searchability
- **Historical integrity** — Do not summarize or rewrite history
- **Workspace cleanup** — Move artifacts to clear active workspace
- **Enforce structure** — Keep project organized and maintainable

## Behavior Rules

- Warn if review missing: "WARNING: No review found for milestone {X}"
- Warn if docs not synced: "WARNING: Documentation may not reflect milestone {X}"
- For milestones: `milestones/archive/M{X}/`
- For docs: `docs/archived/`
- Move artifacts (not copy) to clear the active workspace

## Out of Scope

Never:
- Modify implementation
- Modify tests
- Regenerate specifications
- Regenerate reviews
- Rewrite documentation
- Perform Git operations
- Delete historical information, UNLESS the user has explicitly approved the deletion of duplicate/orphaned files during Cleanup Mode.
- Apply changes to archived artifacts

## Quality Checklist

Before writing:
- [ ] Changes are material (not cosmetic)
- [ ] No duplication of spec/review content
- [ ] Style matches existing documentation
- [ ] Internally consistent across documents
- [ ] Repository-oriented, not plan-oriented
- [ ] Ingestion entries processed with user permission
- [ ] Original files archived after processing
- [ ] 3-layer validation passed
- [ ] Functionality tests passed
- [ ] Rollback mechanism documented

## Examples

### Example 1: Cleanup After Major Refactor

**Trigger**: After refactoring project to 3-layer pattern

**Steps**:
1. Run `/archive-docs` (mode: structure-cleanup)
2. Review manifest of misplaced files
3. Approve relocation of .md files to docs/
4. Approve archival of backup files
5. Approve deletion of build artifacts
6. Skill executes changes
7. Skill validates server startup
8. Skill generates compliance report

**Result**: Project structure compliant with 3-layer pattern, all functionality preserved

### Example 2: Cleanup Before Deployment

**Trigger**: Preparing for production deployment

**Steps**:
1. Run `/archive-docs` (mode: structure-cleanup)
2. Focus on build artifacts and temporary files
3. Approve cleanup of __pycache__, .pyc, test reports
4. Review remaining structure
5. Approve if compliant
6. Skill validates all endpoints
7. Generate deployment-ready report

**Result**: Clean repository structure, minimal artifacts, ready for deployment

## Documentation

- **[SKILLS.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
- [archive_template.md](../../templates/archive_template.md) — Milestone archive template
- [infrastructure_fix_template.md](../../templates/infrastructure_fix_template.md) — Infrastructure archive template
