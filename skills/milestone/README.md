# milestone Skill: Interactive Requirements Elicitation

## Role in OMP AEF

`milestone` transforms a rough feature idea into a complete milestone document through interactive requirements elicitation, supporting followup specifications and verification reuse analysis.

## Usage in Framework Skills

### When milestone is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `manage-roadmap` | After milestone created, start implementation | `M{X}.md` → manage-development |
| `generate-spec` | After milestone, create specifications | `M{X}.md` → generate-spec |
| `session-audit` | During milestone, generate session audits | `M{X}.md` → session-audit |

## Integration Points

### Milestone Creation Workflow

```bash
# Create new milestone
# Interactively elicit requirements
# Generate complete milestone document
# Update MILESTONES.md
```

### Followup Specifications

**Generate followup specs:**
- Creates `M{X}S{Y}.md` without modifying original milestone
- Automatically analyzes reusable verifications
- Identifies applicable tests

## Requirements

### Prerequisites

1. **User Intent**
   - Rough feature idea or improvement
   - Desire for structured milestone

2. **Templates**
   - Milestone template: `~/devcode/aef/agent/templates/milestone_template.md`

### Setup

1. **Invoke Skill:**
   ```bash
   milestone create
   ```

2. **Interactive Requirements Elicitation:**
   - Answer questions about goal, motivation, scope
   - Define success criteria, risks, notes
   - Use free-form text input at all times

## Best Practices

### Before Creating Milestone

**Use milestone when:**
- You have a feature idea or improvement
- You want a structured, approved milestone
- You want to include followup specifications

**Avoid milestone when:**
- You want to implement features directly (use `implement-specification`)
- You need to review existing work (use `review-implementation`)

### Interactive Requirements Elicitation

**Follow this flow:**
1. **Goal:** What is the single, concrete objective?
2. **Motivation:** Why does this milestone matter?
3. **Scope:** List 2-5 concrete deliverables
4. **Out of Scope:** What will NOT be included?
5. **Success Criteria:** Measurable outcomes
6. **Risks:** 2-3 identified risks
7. **Notes:** Optional observations

**Rules:**
- One question per turn
- Always offer text input
- Flag ambiguity
- Challenge scope creep
- Detect hidden requirements

## Output

**Generated Milestone:**
- File: `milestones/M{X}/M{X}.md`
- Format: Milestone template from `templates/milestone_template.md`
- Contents: Goal, motivation, scope, out of scope, success criteria, risks, notes

**Updated MILESTONES.md:**
- Appended `- [M{X}] - {goal} (active)`

**Followup Specification (if created):**
- File: `milestones/M{X}/M{X}S{Y}.md`
- Format: Specification template
- Includes verification reuse analysis

## Commands

**Create:**
```bash
milestone create
```

**Update:**
```bash
milestone update /path/to/milestone.md [user_prompt]
```

**Followup:**
```bash
milestone followup /path/to/milestone.md [focus_area]
```

**Analyze Reuse:**
```bash
milestone analyze-reuse /path/to/milestone.md
```

## Template Reference

- **Milestone Template**: `~/devcode/aef/agent/templates/milestone_template.md`
