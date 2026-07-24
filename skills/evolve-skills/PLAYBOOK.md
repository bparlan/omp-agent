# Evolve-Skills Playbook

This playbook provides the standard workflow for using the evolve-skills skill in everyday development sessions.

## Every Session

Before starting work on an SDD milestone, run the following to ensure all evolve-skills dependencies are healthy:

1. **Audit evolve-skills dependencies**:
   ```bash
   cd ~/devcode/aef/agent/skills/evolve-skills
   python3 skills-auditor.py audit
   ```

2. **Review health dashboard**:
   ```bash
   python3 skills-auditor.py list
   ```

3. **Address critical issues** (if any):
   - Skills with status **CRITICAL** require immediate attention
   - Skills with status **NEEDS_IMPROVEMENT** should be addressed in the current or next session
   - Skills with status **HEALTHY** are in good shape

## Common Workflows

### Single-Skill Audit

To audit a specific skill:
```bash
python3 skills-auditor.py audit <skill-name>
```

Example:
```bash
python3 skills-auditor.py audit session-audit
```

### Reading a Health Report

To view the health report for a specific skill:
```bash
cat ~/devcode/aef/agent/skills/evolve-skills/health/<skill-name>.yaml
```

Example:
```bash
cat ~/devcode/aef/agent/skills/evolve-skills/health/session-audit.yaml
```

## Health Report Structure

Each health report (`evolve-skills/health/{skill-name}.yaml`) contains:

- `skill`: Name of the skill
- `version`: Version number from SKILL.md frontmatter
- `last_audited`: Date of the most recent audit
- `priority`: HIGH/MEDIUM/LOW based on issues found
- `priority_reason`: Summary of issues causing the priority
- `issues`: List of all detected issues
- `recommendations`: Suggestions for fixing issues
- `status`: CRITICAL/NEEDS_IMPROVEMENT/HEALTHY

## Priority Scale

- **HIGH**: Critical functionality, high usage, or blocking issues
- **MEDIUM**: Important but not critical
- **LOW**: Nice to have, low usage, or informational only

## Status Values

- **HEALTHY**: All checks pass, no issues found
- **NEEDS_IMPROVEMENT**: Minor issues, no blocking problems
- **DEGRADED**: Significant issues, functional but problematic
- **CRITICAL**: Major issues, requires immediate attention

## Integration with Other Skills

### Session Audit (session-audit)

After running a session audit:
1. Review `session-audit.yaml` for findings
2. If critical issues are found, use `evolve-skills audit` to prioritize fixes
3. Address issues in the evolved skills based on recommendations

### Evolve-Skills

When evolving skills after session audits:
1. Run `evolve-skills audit` to check health after changes
2. Use `evolve-skills list` to verify no new issues were introduced
3. Address any newly flagged issues before committing changes
