# bootstrap-project Skill: Repository Normalizer

## Role in OMP AEF

`bootstrap-project` analyzes an existing repository and normalizes it into standard engineering structure, providing one-time setup for brownfield projects.

## Usage in Framework Skills

### When bootstrap-project is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `manage-roadmap` | After project normalized, start milestone | `milestones/M1/` → manage-roadmap |
| `session-audit` | During normalization, generate session audits | `docs/` → session-audit |

## Integration Points

### Repository Normalization Workflow

```bash
# Discover repository structure
# Analyze build/package management
# Map modules and architecture
# Inventory tests and CI/CD
# Consolidate documentation
# Create missing canonical docs
# Generate root-level entry points
```

## Requirements

### Prerequisites

1. **Existing Repository**
   - Codebase to analyze
   - Build system (npm, Cargo, Makefile, etc.)

2. **Templates**
   - Various template files for documentation

### Setup

1. **Discover Repository:**
   ```bash
   # Map codebase structure
   glob path="**/*"

   # Identify languages and build systems
   glob path="package.json"
   glob path="Cargo.toml"
   glob path="requirements.txt"
   ```

2. **Analyze Build System:**
   ```bash
   # Read package.json, Cargo.toml, etc.
   read "package.json"
   ```

3. **Map Modules:**
   ```bash
   # Use lsp and grep to identify components
   lsp references
   ```

## Best Practices

### Before Bootstrapping

**Use bootstrap-project when:**
- You have an existing repository to normalize
- You need canonical documentation layer
- You want to establish standard structure

**Avoid bootstrap-project when:**
- You need to implement features (use `implement-specification`)
- You have already set up standard structure

### Documentation Principles

**Repository reality first:**
- Code defines truth, docs follow

**Merge, distill, normalize:**
- Combine scattered knowledge into coherent docs

**Cross-reference:**
- Link related sections, avoid duplication

**Preserve knowledge:**
- Keep architectural decisions and rationale

**Eliminate obsolescence:**
- Remove outdated information

## Output

**Generated Documentation:**
- `README.md` — Project overview and quick start
- `AGENTS.md` — Agent entry point, build commands, coding conventions
- `CHANGELOG.md` — Chronological record of changes
- `FRAMEWORK.md` — Architectural patterns, module organization
- `SPEC.md` — Current system architecture
- `ROADMAP.md` — Capabilities and future items
- `PLAYBOOK.md` — How to run/test/deploy
- `DATA.md` — Database schema, configuration
- `MILESTONES.md` — List of active milestones
- `EXPERIENCES.md` — Meta-learning ledger

**Directory Structure:**
```
{repository}/
├── README.md
├── AGENTS.md
├── docs/
│   ├── CHANGELOG.md
│   ├── FRAMEWORK.md
│   ├── SPEC.md
│   ├── ROADMAP.md
│   ├── PLAYBOOK.md
│   ├── DATA.md
│   ├── MILESTONES.md
│   └── EXPERIENCES.md
└── milestones/
    └── archive/
```

## Out of Scope

**Never:**
- Rewrite source code
- Perform refactoring
- Generate milestones, specifications, verifications
- Perform Git operations
- Archive documents
- Modify implementation files

## Change Detection

Update documentation only when material changes occurred:
- Architecture changes
- Public API changes
- Repository structure changes
- Configuration changes
- Operational procedures
- User-visible behavior
- Deployment changes
- Workflow changes
- Supported platforms

## Ingestion Processing

**Process `/docs/ingest/` files only after explicit user permission.**

## Template Reference

- **Documentation Templates**: `templates/*.md` in OMP agent directory
