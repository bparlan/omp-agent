# implement-specification Skill: Implementation Orchestrator

## Role in OMP AEF

`implement-specification` transforms approved specifications into working code using OMP's native capabilities, orchestrating implementation without redundant documentation generation.

## Usage in Framework Skills

### When implement-specification is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `generate-verification` | After spec ready, create verification protocol | `M{X}S{Y}.md` → generate-verification |
| `generate-tests` | After verification ready, generate tests | `M{X}S{Y}V.md` → generate-tests |
| `evaluate-implementation` | After tests, execute and verify | `M{X}S{Y}T{Z}.md` → evaluate-implementation |

## Integration Points

### Implementation Workflow

```bash
# Load spec and verification
read "milestones/M{X}/M{X}S{Y}.md"
read "milestones/M{X}/M{X}S{Y}V.md"

# Create todo list
# Spawn task subagents for parallel changes
# Verify implementation
# Generate completion report
```

### Task Orchestration

**Parallel Subagents:**
- Each subagent handles ≤5 files
- Includes change description, APIs/patterns, acceptance criteria
- Track progress via Todo list

## Requirements

### Prerequisites

1. **Approved Specification**
   - Milestone (`M{X}S{Y}.md`)
   - Verification protocol (`M{X}S{Y}V.md`)

2. **Project Context**
   - `AGENTS.md` for conventions
   - Codebase structure via `lsp` and `code-search`

3. **Project Architecture**
   - Known modules and interfaces
   - Existing implementations

### Setup

1. **Resolve Artifacts:**
   ```bash
   # Load specification
   read "milestones/M{X}/M{X}S{Y}.md"

   # Load verification
   read "milestones/M{X}/M{X}S{Y}V.md"

   # Load project context
   read "AGENTS.md"
   ```

2. **Analyze Specification:**
   - Identify Functional Requirements
   - Analyze Architecture Impact
   - Inspect existing code

3. **Create Todo List:**
   ```markdown
   todo init: [
     { phase: "Foundation", items: ["Understand requirement X", "Identify module Y"] },
     { phase: "Implementation", items: ["FR-1: Implement Z", "FR-2: Add validation"] },
     { phase: "Verification", items: ["Run tests", "Check edge cases"] }
   ]
   ```

## Best Practices

### Before Implementing

**Use implement-specification when:**
- Specification and verification protocol are approved
- You need to implement working code
- You want to maintain architectural constraints

**Avoid implement-specification when:**
- You need to generate specs or verifications (use `generate-spec`, `generate-verification`)
- You need to review or sync documentation
- You want to archive milestones

### Implementation Principles

**Before modifying code:**
- Read surrounding context for each affected module
- Identify reusable components via `lsp references`
- Respect architectural constraints
- Expand TODO list to unblock issues

**During implementation:**
- Preserve module boundaries
- Keep changes minimal and localized
- Extend existing components when practical
- Maintain coding consistency

**When uncertain:**
- Ask concise clarification via `ask` before proceeding

## Output

**Completion Report:**
- File: `milestones/M{X}/M{X}S{Y}C.md`
- Format: Completion template from `templates/completion_template.md`
- Contents: Files modified, tests executed, issues found

**Implementation Code:**
- Modified implementation files
- Updated test scripts (if applicable)

## Out of Scope

**Never:**
- Generate milestones, specifications, verification plans
- Write reviews or sync documentation
- Archive milestones
- Perform Git operations
- Modify unrelated files
- Redesign architecture
- Introduce unjustified dependencies
- Create README.md, SUMMARY.md, .txt files, or generic documentation

## Verification

Execute:
- Commands from Verification → Automated Validation
- Any existing test suite
- Edge case checks from VERIFICATION document

Do not claim verification unless tests actually run and pass.

## Template Reference

- **Completion Template**: `~/devcode/aef/agent/templates/completion_template.md`
