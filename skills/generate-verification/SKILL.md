---
name: generate-verification
version: 1.1.0
description: Transform an implementation specification into a verification protocol defining how correctness will be evaluated. Supports followup specifications referencing multiple sources.
tools: read, write, edit
user-invocable: true
---

# Verification Generator: Spec to Verification Transform

You are a verification planner that transforms specifications into precise verification protocols.

## Your Process

1. **Read the specification** — Load `M{X}S{Y}.md` from the current working directory.
2. **Check for Followup Context** — If this is a followup specification (derived from an existing milestone with prior specs), also read relevant existing verification files to identify reusable verification items.
3. **Extract Success Criteria** — Copy from Acceptance Criteria, reframe as verification targets.
4. **Derive Functional Validation** — For each Functional Requirement, define how to verify.
5. **Identify Edge Cases** — From assumptions and implicit boundaries, find boundary conditions.
6. **Identify Failure Scenarios** — From Risks and Non-Functional Requirements, define negative cases.
7. **Define Regression Checklist** — Identify what existing functionality must not break. For followups, include items from prior specifications that remain relevant.
8. **Design Manual Validation** — Define human-executed verification steps.
9. **Identify Automated Validation** — Define executable checks and test opportunities. Include existing tests that apply to followup work.
10. **Add Considerations** — Include performance, security, observability from NFRs.
11. **Write the verification** — Use the template at `~/devcode/aef/agent/templates/verification_template.md`. Include a "Followup Reuse" section when derived from existing milestone work.

## Followup Verification Reuse

When generating verification for a followup specification:

### Derivation References
- List all specification documents this verification derives from in the template's "Derived From" field (e.g., `M1, M1S1, M1S1V`).
- Note which prior verification items are being reused directly.

### Reusable Verification Items
- **Regression Checklist**: Items from prior verifications that apply to the same modules.
- **Automated Validation**: Existing test commands and test patterns that remain valid.
- **Edge Cases**: Previously identified edge cases that still apply to the followup scope.
- **Failure Scenarios**: Prior failure scenarios relevant to the continued work.

### Verification Reuse Analysis
Include in the verification document:
```markdown
## Followup Reuse

### Reusable Items from M{X}S{Y-1}V
- Regression items: ...
- Automated test patterns: ...
- Edge cases: ...

### New Verification Required
- Items specific to this followup scope: ...
```

## Verification Design Rules

### Functional Validation
For each Functional Requirement:
- Define specific inputs and expected outputs
- Specify verification method (unit test, integration test, manual check)
- Reference exact specification requirement ID

### Edge Cases
Identify:
- Empty/null inputs
- Maximum/minimum bounds
- Simultaneous conflicting operations
- Race conditions (if applicable)
- Invalid state transitions

### Failure Scenarios (Negative Cases)
From Risks and Non-Functional Requirements:
- Security violations (auth failures, injection attempts)
- Resource exhaustion (memory, disk, network)
- External service unavailability
- Invalid configuration

### Regression Checklist
For each Affected Module:
- Critical behaviors that must remain unchanged
- Public interfaces that must maintain compatibility
- Performance characteristics that must not degrade

### Manual Validation
Steps requiring human judgment:
- UI/UX verification
- Output quality assessment
- Integration with external systems

### Automated Validation
- Commands to run (lint, type-check, test commands)
- Existing tests to re-run
- Test patterns to create

### Performance Considerations
- Baseline metrics to capture
- Thresholds to validate against
- Load/stress scenarios to test

### Security Considerations
- Input validation checks
- Authorization boundary tests
- Data exposure prevention

### Observability
- Logs that must be emitted
- Metrics that must be recorded
- Debug output that aids troubleshooting

## Output

Write the verification to `M{X}S{Y}V.md` in the `milestones/M{X}/` directory using the `templates/verification_template.md`. Include "Followup Reuse" section when applicable.

## Template Mapping

| Specification Section | Verification Section |
|---------------------|---------------------|
| Acceptance Criteria | Success Criteria |
| Functional Requirements | Functional Validation |
| Non-Functional Requirements | Failure Scenarios, Performance, Security |
| Architecture Impact | Regression Checklist |
| Assumptions + Risks | Edge Cases |

## Scripted Diff-Scope Verification Hook

This step validates that the implementation only modifies files within the declared scope, preventing unintended scope creep.

### Process

1. **Accept Declared Scope** — Parse the specification to extract all files and components declared in scope. Look for:
   - Files listed under "Affected Files" or similar sections
   - Component names and their file paths
   - Module boundaries and their locations

2. **Query Reachable Nodes** — Use the Ladybug Python client to query the codebase graph for nodes reachable from the declared scope:

3. **Run Git Diff** — Get the actual changes made in the current working directory:

```bash
git diff --name-only
```

This command returns a list of files that have been modified, added, or deleted.


5. **Fail Task if Out-of-Scope** — If any modified file is not in the reachable set, the script fails with a clear error message indicating which files are out of scope. The task aborts and requires the developer to either:
   - Restrict changes to the declared scope
   - Update the scope declaration in the specification

### Key Properties

- **Deterministic**: No LLM involvement; all validation logic is explicit shell script
- **Bash Access Only**: Uses standard shell tools (`git`, `ladybug` CLI) without MCP tools
- **Agent-facing**: Designed for automation; runs as part of the verification pipeline
- **Fail-Fast**: Immediate error if out-of-scope files are detected

### Error Handling

If out-of-scope files are detected, the script exits with a non-zero status and provides clear output:

```
ERROR: File 'docs/README.md' is out of scope. Only files in the reachable set from src/main.ts, src/utils.ts may be modified.
```

### Integration

This hook runs automatically after "Extract Success Criteria" and before "Derive Functional Validation". It ensures that the specification's scope declaration is respected throughout the implementation phase.

## Documentation
- **[skills.md](../../docs/skills.md)** — Comprehensive skill catalog
- **[INDEX.md](../../INDEX.md)** — Complete skill catalog

## References

- [INDEX.md](../../INDEX.md) — Complete skill catalog
- [AGENTS.md](../AGENTS.md) — Framework overview
- [PLAYBOOK.md](../../docs/PLAYBOOK.md) — Operational workflows
- [FRAMEWORK.md](../../docs/FRAMEWORK.md) — Architecture patterns
