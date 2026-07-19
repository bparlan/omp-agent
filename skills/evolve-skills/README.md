# evolve-skills Skill: Framework Improvement Architect

## Role in OMP AEF

`evolve-skills` analyzes recent project artifacts and Session Audit Reports (SA1, SA2, SA3...) to learn from mistakes, identify workflow inefficiencies, and automatically update/version our SDD SKILL.md files. Handles multiple session audits and TEMP milestones.

## Usage in Framework Skills

### When evolve-skills is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `session-audit` | After session audit, generate artifacts | `M{X}SA{Y}.md` → evolve-skills |
| `manage-roadmap` | After framework updated, start new milestone | `ARCHIVED` → manage-roadmap |

## Integration Points

### Evolution Workflow

```bash
# Read Session Audit Reports
# Read ARCHIVED documents
# Analyze patterns and friction points
# Identify skill improvements
# Update SKILL.md files
# Document new learnings
```

## Requirements

### Prerequisites

1. **Session Audit Reports**
   - Multiple Session Audit Documents (SA1, SA2, SA3...)
   - Found in `milestones/M{X}/M{X}SA{Y}.md` format

2. **Archived Artifacts**
   - `milestones/archive/` directory
   - Completed milestones with relevant changes

3. **Templates**
   - Various documentation templates

### Setup

1. **Read Session Audits:**
   ```bash
   # Read multiple SAs in order
   read "milestones/M{X}/M{X}SA1.md"
   read "milestones/M{X}/M{X}SA2.md"
   read "milestones/M{X}/M{X}SA3.md"
   ```

2. **Read ARCHIVED:**
   ```bash
   glob path="milestones/archive"
   read "milestones/archive/M{X}/M{X}SA{Y}.md"
   ```

3. **Analyze Patterns:**
   - Friction points
   - Skill misuse patterns
   - Workflow inefficiencies

## Best Practices

### Before Evolving

**Use evolve-skills when:**
- You have multiple session audits to analyze
- You want to improve framework skills
- You want to document new learnings
- You want to version SKILL.md files

**Avoid evolve-skills when:**
- You need to implement features (use `implement-specification`)
- You need to create new milestones (use `manage-roadmap`)
- You have only one session audit

### Evolution Principles

**Learn from session audits:**
- Analyze SA documents for patterns
- Identify repeated mistakes
- Find workflow improvements

**Update SKILL.md files:**
- Version control updates
- Document new learnings
- Improve clarity and accuracy

**Handle TEMP milestones:**
- Process TEMP milestones for evolve-skills
- Extract lessons learned

**Cumulative context:**
- SA1 → SA2 → SA3... in order
- Build on cumulative context

## Output

**Evolved SKILL.md Files:**
- Updated `SKILL.md` files with new learnings
- Versioned updates (if applicable)
- Documented friction points

**New Learnings:**
- Documented patterns and improvements
- New skill capabilities
- Removed or deprecated features

**Framework Updates:**
- Improved workflows
- Better error handling
- Enhanced documentation

## Processing Strategy

**Read in order:**
1. SA1 → SA2 → SA3...
2. Build cumulative context
3. Analyze patterns
4. Generate improvements

**Handle TEMP milestones:**
- Process M1SA1, M2SA1, M3SA1... in order
- Extract lessons learned

**Identify friction points:**
- Repeated mistakes
- Misused skills
- Inefficient workflows

**Generate improvements:**
- Update SKILL.md files
- Document new patterns
- Refine skill capabilities

## Template Reference

- **Session Audit Templates**: `templates/*.md` in OMP agent directory
