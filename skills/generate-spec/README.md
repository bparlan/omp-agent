# generate-spec Skill: Specification Generator

## Role in OMP AEF

`generate-spec` transforms an approved milestone document into a detailed implementation specification, supporting followup specifications for existing milestones.

## Usage in Framework Skills

### When generate-spec is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `milestone` | After milestone approved, create specifications | `M{X}.md` → generate-spec |
| `generate-verification` | After spec ready, create verification protocol | `M{X}S{Y}.md` → generate-verification |
| `manage-development` | After spec ready, implement | `M{X}S{Y}.md` → manage-development |

## Integration Points

### Specification Generation Workflow

```bash
# Load milestone
read "milestones/M{X}/M{X}.md"

# Check for existing specs
# Determine next sequence number
# Extract core objective
# Derive functional requirements
# Define non-functional requirements
# Identify architecture impact
# Write specification
```

### Followup Specifications

**For followup specs:**
- Clarify additional work
- Identify reusable verifications
- Derive from existing implementation state

## Requirements

### Prerequisites

1. **Approved Milestone**
   - Milestone document (`M{X}.md`)
   - Acceptance criteria defined

2. **Templates**
   - Specification template: `~/devcode/aef/agent/templates/specification_template.md`

3. **Existing Specifications** (if followup)
   - Prior specifications for context
   - Verification protocols for reuse

### Setup

1. **Read Milestone:**
   ```bash
   read "milestones/M{X}/M{X}.md"
   ```

2. **Check for Existing Specs:**
   ```bash
   glob path="milestones/M{X}/M{X}S*.md"
   ```

3. **Determine Next Sequence:**
   - If `M{X}S1.md` exists, create `M{X}S2.md`
   - Never overwrite existing specifications

## Best Practices

### Before Generating Specification

**Use generate-spec when:**
- Milestone is approved and ready
- You need a detailed implementation specification
- You want to support followup work

**Avoid generate-spec when:**
- You need to create the milestone (use `milestone`)
- You need to implement features (use `implement-specification`)

### Specification Guidelines

**Extract:**
- Core objective from milestone goal
- Functional requirements from scope items
- Non-functional requirements from risks
- Architecture impact from assumptions
- Constraints from out of scope
- Acceptance criteria from success criteria

**For Followups:**
- Focus on incremental additions
- Identify reusable verifications
- Define followup context section

**Output Structure:**
- Objective
- Functional Requirements
- Non-Functional Requirements
- Architecture Impact
- Constraints
- Assumptions
- Acceptance Criteria
- Next Steps

## Output

**Generated Specification:**
- File: `milestones/M{X}/M{X}S{Y}.md`
- Format: Specification template from `templates/specification_template.md`
- Contents: Objective, functional requirements, non-functional requirements, architecture impact, constraints, assumptions, acceptance criteria, next steps

**Followup Context:**
- Section at bottom of spec
- References to prior specs
- Reusable verifications

**Next Steps:**
- Advises user to run `generate-verification`

## Template Reference

- **Specification Template**: `~/devcode/aef/agent/templates/specification_template.md`
