# manage-development Skill: Tactical SDD Orchestrator

## Role in OMP AEF

`manage-development` is a Tactical Engineering Manager that orchestrates the Spec-Driven Development (SDD) pipeline for an active milestone, with cycle reporting and roadmap integration.

## Usage in Framework Skills

### When manage-development is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `manage-roadmap` | After cycle completes, generate next milestone | `M{X}C.md` → manage-roadmap |
| `review-implementation` | After evaluation passes, perform review | `M{X}S{Y}E.md` → review-implementation |
| `sync-documentation` | After review passes, sync to docs | `M{X}S{Y}R.md` → sync-documentation |
| `archive-milestone` | After all specs reviewed, archive | `M{X}S{Y}R.md` → archive-milestone |

## Integration Points

### SDD Pipeline Sequence

```bash
# Milestone → Specification → Verification → Tests → Implementation → Evaluation → Review → Sync → Archive
# Orchestrate each step automatically based on detected artifacts
```

### Pipeline Stage Detection

- Milestone (`M{X}.md`) → requires `generate-spec`
- Specification (`M{X}S{Y}.md`) → requires `generate-verification`
- Verification (`M{X}S{Y}V.md`) → requires `generate-tests`
- Test Scripts → requires `implement-specification`
- Completion Report → requires `evaluate-implementation`
- Evaluation Report → requires `investigate-issue` or `hotfix-issue`
- Evaluation Report passed → requires `review-implementation`
- Review Report → requires `sync-documentation`
- All specs reviewed → requires `archive-milestone` or `cycle-report`

## Requirements

### Prerequisites

1. **Active Milestone**
   - Milestone directory exists: `milestones/M{X}/`
   - Active milestone status in `docs/MILESTONES.md`

2. **SDD Templates**
   - Cycle report template: `~/devcode/aef/agent/templates/cycle_report_template.md`

3. **Project Documentation**
   - `docs/ROADMAP.md`
   - `docs/MILESTONES.md`

### Setup

1. **Assess Active State:**
   ```bash
   # Scan milestones/M{X}/ directory
   glob path="milestones/M{X}/*"
   ```

2. **Determine Pipeline Stage:**
   - Analyze presence of artifacts
   - Identify next required skill
   - Execute next action

## Best Practices

### Before Managing Development

**Use manage-development when:**
- You have an active milestone
- You want to follow the SDD pipeline sequentially
- You want cycle reporting and roadmap integration

**Avoid manage-development when:**
- You need to create a new milestone (use `manage-roadmap`)
- You want to perform a specific SDD phase manually (use the appropriate skill directly)

### Pipeline Orchestration Guidelines

**Strict Sequence:**
1. Milestone → Specification → Verification → Tests → Implementation → Evaluation → Review → Sync → Archive

**Auto-Invocation:**
- Automatically determine and invoke the next required skill
- Invoke `investigate-issue` or `hotfix-issue` based on evaluation failures

**Cycle Reporting:**
- When milestone cycle completes
- Generate cycle report using template
- Include roadmap context

## Output

**Cycle Report:**
- File: `milestones/M{X}/M{X}C.md`
- Format: Cycle report template
- Contents: Summary of all artifacts, completion status, recommendations

**Orchestrated Skills:**
- `generate-spec`
- `generate-verification`
- `generate-tests`
- `implement-specification`
- `evaluate-implementation`
- `review-implementation`
- `sync-documentation`
- `archive-milestone`
- `investigate-issue` or `hotfix-issue`

## Out of Scope

**You are:**
- An orchestrator and state-tracker
- Responsible for detecting artifacts and determining next steps
- Will never generate artifacts yourself

**Never:**
- Generate specifications, verifications, tests, implementations
- Write code or implement features
- Modify existing `M{X}.md` files without explicit permission
