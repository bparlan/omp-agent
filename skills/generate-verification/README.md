# generate-verification Skill: Verification Protocol Generator

## Role in OMP AEF

`generate-verification` transforms an implementation specification into a verification protocol defining how correctness will be evaluated, supporting followup specifications with multiple sources.

## Usage in Framework Skills

### When generate-verification is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `generate-spec` | After milestone approved, create specification | `M{X}.md` → generate-spec |
| `generate-tests` | After verification ready, generate tests | `M{X}S{Y}V.md` → generate-tests |
| `implement-specification` | After verification ready, implement | `M{X}S{Y}V.md` → implement-specification |

## Integration Points

### Verification Generation Workflow

```bash
# Load specification
read "milestones/M{X}/M{X}S{Y}.md"

# Check for followup context
# Extract success criteria
# Define functional validation
# Identify edge cases
# Define failure scenarios
# Write verification protocol
```

### Followup Verification Reuse

**For followup specifications:**
- List derived references
- Identify reusable verification items
- Apply cumulative context from prior verifications

## Requirements

### Prerequisites

1. **Approved Specification**
   - Specification document (`M{X}S{Y}.md`)
   - Functional requirements
   - Acceptance criteria

2. **Context Documents**
   - Prior specifications (if followup)
   - Verification files for reuse

3. **Templates**
   - Verification template: `~/devcode/aef/agent/templates/verification_template.md`

### Setup

1. **Read Specification:**
   ```bash
   read "milestones/M{X}/M{X}S{Y}.md"
   ```

2. **Check for Followup Context:**
   ```bash
   # Read existing verification files
   glob path="milestones/M{X}/M{X}S*.md"
   ```

3. **Extract Success Criteria:**
   - From Acceptance Criteria
   - Reframe as verification targets

## Best Practices

### Before Generating Verification

**Use generate-verification when:**
- Specification is approved and ready
- You need to define testable verification criteria
- Implementation will follow (implement-specification)

**Avoid generate-verification when:**
- You need to generate the specification (use `generate-spec`)
- You need to create test scripts (use `generate-tests`)

### Verification Design Guidelines

**Functional Validation:**
- Define specific inputs and expected outputs
- Specify verification method (unit test, integration test, manual check)
- Reference exact specification requirement ID

**Edge Cases:**
- Empty/null inputs
- Maximum/minimum bounds
- Simultaneous conflicting operations
- Race conditions
- Invalid state transitions

**Failure Scenarios:**
- Security violations
- Resource exhaustion
- External service unavailability
- Invalid configuration

**Regression Checklist:**
- Critical behaviors that must remain unchanged
- Public interfaces that must maintain compatibility
- Performance characteristics

**Manual Validation:**
- UI/UX verification
- Output quality assessment
- Integration with external systems

**Automated Validation:**
- Commands to run (lint, type-check, test commands)
- Existing tests to re-run
- Test patterns to create

## Output

**Verification Document:**
- File: `milestones/M{X}/M{X}S{Y}V.md`
- Format: Verification template from `templates/verification_template.md`
- Contents: Success criteria, functional validation, edge cases, failure scenarios

**Followup Reuse Section:**
- Reusable items from prior verifications
- New verification required

## Template Reference

- **Verification Template**: `~/devcode/aef/agent/templates/verification_template.md`

**Template Mapping:**

| Specification Section | Verification Section |
|---------------------|---------------------|
| Acceptance Criteria | Success Criteria |
| Functional Requirements | Functional Validation |
| Non-Functional Requirements | Failure Scenarios, Performance, Security |
| Architecture Impact | Regression Checklist |
| Assumptions + Risks | Edge Cases |
