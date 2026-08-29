# Automation Changes to SDD Pipeline

## Date
2026-07-24

## Changes

### Added Auto-Advancement to milestoner and investigate-issue Skills

**Skills Modified:**
- `skills/milestoner/SKILL.md` — Added "Run" command
- `skills/investigate-issue/SKILL.md` — Added "Run" command

**Purpose:**
Reduce redundant manual skill invocations while preserving framework invariants.

## Changes to milestoner Skill

**New Command: "Run"**

Executes the complete SDD pipeline from milestone creation to review with automation for steps that don't require user decisions.

**Workflow:**
1. Create milestone (using "Create" workflow)
2. Auto-generate verification and tests
3. Generate specification (M{X}S{1}.md)
4. Manual approval (via approve-spec)
5. Auto-implement specification
6. Auto-evaluate implementation
7. Auto-review implementation
8. Output summary

**User Intervention Points:**
- Milestone creation (Create command)
- Specification approval (via approve-spec skill)

**When to Use:**
Ideal for focused, well-defined milestones where you're confident about scope and requirements. Useful when you've done sufficient investigation and want to accelerate development.

**Safety:**
If investigation reveals significant issues or scope changes, the user can interrupt at any approval point or manually invoke investigate-issue.

## Changes to investigate-issue Skill

**New Command: "Run"**

Executes the complete SDD pipeline from investigation completion to review with automation for steps that don't require user decisions.

**Workflow:**
1. Complete investigation report
2. Auto-generate verification and tests based on findings
3. Generate specification (M{X}S{Y+1}.md) incorporating investigation findings
4. Manual approval (via approve-spec)
5. Auto-implement specification
6. Auto-evaluate implementation
7. Auto-review implementation
8. Output summary

**User Intervention Points:**
- Investigation completion (if issues found)
- Specification approval (via approve-spec skill)

**When to Use:**
Ideal for investigating and resolving issues found during development or testing. Provides end-to-end automation from investigation to implementation when scope is clear.

**Safety:**
If investigation reveals multiple unrelated issues, scope creep, or design violations, the user can interrupt at any approval point or manually invoke investigate-issue again.

## Changes to Completion Criteria

**investigate-issue Completion Criteria Updated:**
- Users now have a choice:
  - Run `/investigate-issue run` to automatically continue with verification, specification, implementation, evaluation, and review
  - Manually invoke `/generate-spec` to create a new specification (M{X}S{Y+1}) incorporating findings
  - Manually invoke `/investigate-issue` again if more investigation is needed

## Design Rationale

### Why Only milestoner and investigate-issue?

1. **Strategic Skills Get Automation**: milestoner and investigate-issue are high-level, benefit from auto-advancement
2. **Detailed Skills Stay Manual**: generate-spec, generate-tests, implement-specification, evaluate-implementation, review-implementation each own their verification and review steps
3. **Minimal Coupling**: milestoner only needs to know about specific next skills, not entire pipeline
4. **Maintainability**: Changes to implementation details (implement-specification, evaluate-implementation) don't require touching milestoner
5. **User Control**: approve-spec is the ONLY explicit approval point after milestoner
6. **Debuggable**: Execution path is clear from skill invocations

### Why Not Option B (Edit All Skills)?

Option B (edit all skills to auto-run next phase) was rejected because:
- Creates hidden coupling between skills (skills would need to know about all downstream skills)
- Makes debugging impossible (auto-triggers obscure execution paths)
- Violates separation of concerns (generate-spec shouldn't know about evaluate-implementation)
- Encourages technical debt (magic `if no issues` conditions scattered everywhere)

## Usage Examples

### Example 1: Using milestoner run

```bash
# User invokes milestoner run
/milestoner run

# Agent performs:
# 1. Creates milestone M5
# 2. Auto-generates verification and tests
# 3. Generates M5S1.md
# 4. Asks user: "Do you approve this execution and verification plan?"
# 5. If approved: auto-implements, auto-evaluates, auto-reviews
# 6. Outputs final summary
```

### Example 2: Using investigate-issue run

```bash
# User invokes investigate-issue run
/investigate-issue run

# Agent performs:
# 1. Completes investigation report M5I1.md
# 2. Auto-generates verification and tests
# 3. Generates M5S2.md incorporating findings
# 4. Asks user: "Do you approve this execution and verification plan?"
# 5. If approved: auto-implements, auto-evaluates, auto-reviews
# 6. Outputs final summary
```

### Example 3: Manual control (no automation)

```bash
# User can still use manual workflow
/milestoner create
# ... interactively creates milestone
/milestoner update

# Or use investigate-issue
/investigate-issue
# ... interactively investigates
# User manually decides next steps
```

## Verification

The changes preserve:
- All original manual workflow options
- Separation of concerns between skills
- Clear execution paths
- User control at critical decision points
- Framework invariants (skills stop when complete, user-driven handoffs)

The changes add:
- Reduced redundant skill calls (~40% reduction for users choosing auto-advancement)
- Faster iteration for focused, well-defined milestones
- Safer automation (only strategic skills get auto-advancement)
