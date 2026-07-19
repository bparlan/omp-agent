# generate-tests Skill: Test Generator

## Role in OMP AEF

`generate-tests` translates verification protocols into executable use-case scripts and tests, preparing implementations for evaluation.

## Usage in Framework Skills

### When generate-tests is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `generate-verification` | After spec ready, create verification protocol | `M{X}S{Y}.md` → generate-verification |
| `implement-specification` | After verification ready, generate tests | `M{X}S{Y}V.md` → generate-tests |
| `evaluate-implementation` | After tests, execute and fix | `M{X}S{Y}T{Z}.md` → evaluate-implementation |

## Integration Points

### Test Generation Workflow

```bash
# Load verification protocol
read "milestones/M{X}/M{X}S{Y}V.md"

# Generate executable tests
# Save test scripts
# Save test plan documentation
```

### Test Script Templates

**Use the template at:**
- `~/devcode/aef/agent/templates/test_template.md`
- Python, JavaScript, bash, or UI test scripts

## Requirements

### Prerequisites

1. **Verification Protocol**
   - Verification document (`M{X}S{Y}V.md`)
   - Functional requirements and success criteria

2. **Implementation Code**
   - Implementation files from `implement-specification`
   - Completion report (`M{X}S{Y}C.md`)

3. **Test Infrastructure**
   - Access to test framework (pytest, Jest, etc.)
   - Test execution environment

### Setup

1. **Read Verification Protocol:**
   ```bash
   read "milestones/M{X}/M{X}S{Y}V.md"
   ```

2. **Read Implementation:**
   ```bash
   # Scan newly written code
   glob path="src/**/*.py"
   glob path="src/**/*.ts"
   ```

3. **Generate Executable Tests:**
   - Write programmatic use-case files
   - Create test scripts (pytest, bash, UI scripts)
   - Create localized testing utilities

## Best Practices

### Before Generating Tests

**Use generate-tests when:**
- Verification protocol exists and is approved
- Implementation code is complete
- You need test coverage before evaluation

**Avoid generate-tests when:**
- You want to execute tests (use `evaluate-implementation`)
- You need to modify implementation (use `implement-specification`)
- You need to create verification protocols (use `generate-verification`)

### Test Generation Guidelines

**Create:**
- Programmatic use-case files
- Test scripts (pytest, Jest, bash)
- Testing utilities
- Test plan documentation

**Do NOT:**
- Execute the tests
- Modify core implementation code
- Update documentation or specifications

## Output

**Test Documentation Artifact:**
- File: `milestones/M{X}/M{X}S{Y}T{Z}.md`
- Format: Test template from `templates/test_template.md`
- Contents: Test plan, coverage, execution steps

**Executable Test Scripts:**
- Directory: `tests/M{X}/`
- Python/JS/bash test scripts
- Create directory if it does not exist

## Out of Scope

**Never:**
- Run the tests or attempt to evaluate the results
- Modify the core implementation code
- Update documentation or specifications

## Edit Tool Usage

### Single-line Replacements (Use `bash`)

```bash
# Replace line 27 with new text
sed -i.bak '27s/.*/NEW_TEXT/' /path/to/file
```

### Multi-line Block Edits (Use `edit`)

```bash
# Use SWAP or SWAP.BLK operations
# Always use + prefix for new lines
```

## Template Reference

- **Test Template**: `~/devcode/aef/agent/templates/test_template.md`
