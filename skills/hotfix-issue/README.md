# hotfix-issue Skill: Fast-Track Bug Resolution

## Role in OMP AEF

`hotfix-issue` implements small, targeted bug fixes directly from an investigation report without the full specification lifecycle.

## Usage in Framework Skills

### When hotfix-issue is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `evaluate-implementation` | If evaluation found major bugs | `M{X}S{Y}E.md` → hotfix-issue |
| `review-implementation` | After hotfix, perform final review | `M{X}S{Y}H{Z}.md` → review-implementation |

## Integration Points

### Hotfix Workflow

```bash
# Read investigation report
# Read project context
# Perform code search & dependency analysis
# Execute the fix
# Verify the fix
# Generate hotfix report
```

## Requirements

### Prerequisites

1. **Investigation Report**
   - Investigation report: `M{X}S{Y}I{Z}.md`
   - Root cause identified

2. **Project Context**
   - `AGENTS.md` for coding conventions
   - Codebase structure

3. **Code-Search Tools**
   - `grep` and `ast_grep` for analysis

### Setup

1. **Read Investigation:**
   ```bash
   read "milestones/M{X}/M{X}S{Y}I{Z}.md"
   ```

2. **Read Project Context:**
   ```bash
   read "AGENTS.md"
   ```

3. **Perform Code Search:**
   ```bash
   # Use grep and ast_grep
   grep pattern="bug" path="src"
   ast_grep pattern="error" path="src"
   ```

## Best Practices

### Before Hotfixing

**Use hotfix-issue when:**
- Investigation report identifies a clear bug
- Fix is small and targeted
- No architecture changes needed
- Zero new features

**Avoid hotfix-issue when:**
- Fix requires architecture changes
- Fix involves public API changes
- Fix is a new feature
- Fix modifies specifications

### Hotfix Principles

**Surgical precision:**
- Only modify exact lines/files causing the issue

**No architecture changes:**
- If fix requires new modules, public API changes, or architectural shifts, abort

**Zero new features:**
- Absolutely no feature development

## Output

**Hotfix Report:**
- File: `milestones/M{X}/M{X}H{Z}.md`
- Format: Hotfix template from `templates/hotfix_template.md`
- Contents: Root cause, files modified, tests executed

**Hotfix Execution:**
- Modified implementation files
- Verification of fix

## Out of Scope

**Never:**
- Implement new features
- Modify architecture or public APIs
- Modify specifications or milestone documents
- Run `sync-documentation` or generate specifications

## Edit Tool Usage

### Single-line Replacements (Use `bash`)

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file
```

### Multi-line Block Edits (Use `edit`)

```bash
# Use SWAP or SWAP.BLK operations
# Always use + prefix for new lines
```

## Hotfix Principles

**If the fix requires:**
- New modules → Abort and use `generate-spec`
- Public API changes → Abort and use `generate-spec`
- Architectural shifts → Abort and use `generate-spec`
- New features → Do NOT implement

**If you cannot define a rollback strategy:**
- Do not execute
