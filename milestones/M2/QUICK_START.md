# Quick Start: Session-Based Framework Improvement

## Overview

This system enables you to edit framework files in a session without using milestone > development structure, while ensuring major changes are properly tracked and documented.

## One-Page Workflow

### After Your Session

```mermaid
graph LR
    A[Complete framework work] --> B[Run session-audit]
    B --> C[Review M{X}SA.md]
    C --> D{Approve changes?}
    D -->|Yes| E[Invoke evolve-skills]
    D -->|No| F[Modify session-audit or manual]
    E --> G[evolve-skills applies changes]
    G --> H[Verify framework consistency]
    H --> I[Done]
```

## Step-by-Step Guide

### Step 1: Complete Your Framework Work

Edit framework files as needed:
- `~/.omp/agent/INDEX.md`
- `~/.omp/agent/AGENTS.md`
- `~/.omp/agent/skills/*/SKILL.md`
- `~/.omp/agent/skills-lock.json`
- `~/.omp/agent/config.yml`
- Templates (`~/.omp/agent/templates/*.md`)

**Do NOT worry about documentation** — session-audit will handle it.

### Step 2: Run session-audit

```
User: Invoke session-audit skill
```

**What session-audit will do:**
- Scan your session changes
- Classify changes (major vs minor)
- Use code-search to understand impact
- Generate `M{X}SA.md` report

**Example output:**
```
Session Audit Report: M2
- Files Modified: 3
- Files Created: 2
- Major Changes: 2
  1. session-audit skill (NEW)
  2. code-search documentation (NEW)
```

### Step 3: Review the Session Audit Report

Open `milestones/M2/M2SA.md`.

**What to look for:**

1. **Major Changes** — These will require evolve-skills action
   ```markdown
   ### 1. Infrastructure Skill Addition — session-audit
   Files Modified:
   - skills/session-audit/SKILL.md (NEW)
   Impact: Enables proper tracking...
   ```

2. **Recommended evolve-skills Actions**
   ```markdown
   1. [HIGH] evolve-skills — Add code-search integration
   2. [MEDIUM] session-audit — Document code-search usage patterns
   ```

3. **Consistency Checks**
   - [✅] INDEX.md and AGENTS.md stay in sync
   - [✅] skills-lock.json matches actual skills

**Approve or request changes:**
- If approved: Move to Step 4
- If rejected: Modify session-audit output or make manual changes

### Step 4: Invoke evolve-skills

```
User: Invoke evolve-skills skill
```

**What evolve-skills will do:**
- Read `M2SA.md` report
- Identify skills to update
- Apply documented improvements
- Document intervention in EVOLUTION.md
- Verify framework-critical files are consistent

**Example output:**
```
Processing session-audit report M2SA.md
✓ Identified 2 skills to update
✓ Updated session-audit SKILL.md (version 1.0.0 → 1.0.1)
✓ Updated code-search SKILL.md (version 1.0.0 → 1.0.1)
✓ Documented in EVOLUTION.md
✓ Verified framework-critical files consistency
```

### Step 5: Verify Changes

**Check that evolve-skills did the right thing:**

1. **Verify SKILL.md files were updated**
   ```bash
   grep -A 5 "session-audit" ~/.omp/agent/skills/session-audit/SKILL.md
   grep -A 5 "code-search" ~/.omp/agent/skills/code-search/SKILL.md
   ```

2. **Check EVOLUTION.md**
   ```bash
   tail -50 ~/.omp/agent/skills/evolve-skills/EVOLUTION.md
   ```

3. **Verify framework-critical files are consistent**
   ```bash
   # Check INDEX.md and AGENTS.md are in sync
   diff ~/.omp/agent/INDEX.md ~/.omp/agent/AGENTS.md | wc -l
   # Should be 0 (no differences)

   # Check skills-lock.json matches actual skills
   ls ~/.omp/agent/skills/
   ```

4. **Test framework functionality**
   - Try running a SDD skill
   - Verify code-search works
   - Check that session-audit is available

## Common Patterns

### Pattern 1: Adding a New Skill

**Your session:**
```bash
# You add a new skill
mkdir ~/.omp/agent/skills/my-new-skill
cat > ~/.omp/agent/skills/my-new-skill/SKILL.md <<'EOF'
---
name: my-new-skill
...
EOF
```

**session-audit will detect:**
```markdown
### 1. New Skill Addition — my-new-skill

Files Created:
- skills/my-new-skill/SKILL.md (NEW)

Impact: New infrastructure skill added...
```

**evolve-skills will:**
- Add my-new-skill to AGENTS.md
- Add to INDEX.md
- Document in EVOLUTION.md

### Pattern 2: Modifying an Existing Skill

**Your session:**
```bash
# You update an existing skill
sed -i.bak 's/OLD/NEW/' ~/.omp/agent/skills/generate-spec/SKILL.md
```

**session-audit will classify:**
- Major change (if behavior/functionality changed)
- Minor change (if just formatting/wording)

**evolve-skills will:**
- Apply the change
- Bump version number
- Document in EVOLUTION.md

### Pattern 3: Updating Documentation

**Your session:**
```bash
# You update INDEX.md
echo "### New Agent" >> ~/.omp/agent/INDEX.md
```

**session-audit will detect:**
- INDEX.md modification
- Auto-generated structure
- Changes to agent list

**evolve-skills will:**
- Ensure INDEX.md and AGENTS.md are in sync
- Update AGENTS.md accordingly
- Document the change

## What session-audit Tracks

### Major Changes (Always Track)

**Framework-critical files:**
- `~/.omp/agent/INDEX.md`
- `~/.omp/agent/AGENTS.md`
- `~/.omp/agent/README.md`
- `~/.omp/agent/FRAMEWORK.md`
- `~/.omp/agent/PLAYBOOK.md`
- `~/.omp/agent/skills-lock.json`
- `~/.omp/agent/config.yml`

**Skills:**
- Any `SKILL.md` when:
  - New agent/role added
  - Out of Scope section modified
  - Negative guardrails added
  - Tool permissions changed
  - Process steps significantly updated

**Templates:**
- Any `templates/*.md` when:
  - Schema changes (new fields)
  - Template version updated
  - Required sections added/removed

### Minor Changes (Do NOT Track)

**Cosmetic:**
- Reordering of bullets/sections
- Changing "use tool" to "use X tool"
- Adding/removing verbose descriptions
- Comment reformatting
- Whitespace/formatting changes

**Content-only:**
- Expanding examples in SKILL.md
- Clarifying wording without changing behavior
- Adding historical context in AGENTS.md
- Fixing typos in docs

## What evolve-skills Applies

From session-audit reports, evolve-skills will:

1. **Apply improvements to SKILL.md files**
   - Based on recommended actions
   - Using evidence from artifacts

2. **Bump version numbers**
   - Increment patch version for minor changes
   - Increment minor version for major changes
   - Document in EVOLUTION.md

3. **Document interventions**
   - Record date, skill updated, old/new version, rationale
   - Link to session-audit report

4. **Verify consistency**
   - Check INDEX.md and AGENTS.md
   - Verify skills-lock.json matches actual skills
   - Ensure all framework-critical files are in sync

## Troubleshooting

### Issue: session-audit doesn't detect changes

**Solution:**
- Make sure you're using git or the modification is recent (last 24 hours)
- Check that the file is in the OMP AEF directory
- Try running session-audit again

### Issue: evolve-skills doesn't apply changes

**Solution:**
- Check that M{X}SA.md exists in milestones/M{X}/
- Verify evolve-skills has read access to the file
- Check evolve-skills logs for errors
- Manually apply changes if needed

### Issue: INDEX.md and AGENTS.md are out of sync

**Solution:**
- This should not happen if both tools are working correctly
- Manually sync them or run session-audit again
- Check evolve-skills logs for verification failures

## Best Practices

### Do
- ✅ Run session-audit after completing framework work
- ✅ Review M{X}SA.md before running evolve-skills
- ✅ Verify changes after evolve-skills completes
- ✅ Test framework functionality after changes
- ✅ Keep session-audit reports for future reference

### Don't
- ❌ Try to manually track changes across multiple files
- ❌ Forget to run session-audit after framework work
- ❌ Skip reviewing M{X}SA.md before evolve-skills
- ❌ Assume evolve-skills will apply all changes automatically
- ❌ Ignore consistency check failures

## Resources

### Documentation
- **session-audit SKILL.md** — Complete skill documentation
- **code-search README.md** — Code-search infrastructure documentation
- **M2SA.md** — Session audit report for this session
- **IMPLEMENTATION_SUMMARY.md** — Comprehensive implementation guide

### Skills to Know
- **session-audit** — Analyzes session-based framework improvements
- **evolve-skills** — Applies improvements from session-audit reports
- **code-search** — Provides semantic search and skeleton generation

## Getting Help

If you encounter issues:

1. **Check the logs** — Both skills should log their progress
2. **Review the reports** — M{X}SA.md and EVOLUTION.md contain details
3. **Check documentation** — SKILL.md files have comprehensive documentation
4. **Ask for help** — Use irc to ask other agents for assistance

---

**Remember**: The goal is to let you edit framework files freely in a session while ensuring major changes are properly tracked and documented. session-audit and evolve-skills handle the tedious part so you can focus on building.
