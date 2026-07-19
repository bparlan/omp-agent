# evaluate-implementation Skill: Test Executor and Auto-Fixer

## Role in OMP AEF

`evaluate-implementation` executes tests, autonomously fixes minor implementation bugs, and generates an Evaluation Report to prepare the implementation for review.

## Usage in Framework Skills

### When evaluate-implementation is Used

| Skill | Purpose | Example Commands |
|-------|---------|------------------|
| `generate-tests` | After tests generated, execute and fix | `M{X}S{Y}T{Z}.md` → evaluate-implementation |
| `review-implementation` | After evaluation, perform analytical review | `M{X}S{Y}E.md` → review-implementation |

## Integration Points

### Auto-Fix Workflow

```bash
# Execute tests
./tests/M{X}/test_script.py

# Fix minor bugs if found
# Re-run tests to verify
./tests/M{X}/test_script.py
```

### Evaluation Report Generation

- **Output**: `milestones/M{X}/M{X}S{Y}E.md`
- **Template**: `~/devcode/aef/agent/templates/evaluation_template.md`
- **Purpose**: Document test execution, auto-fixes, and remaining failures

## Requirements

### Prerequisites

1. **Test Scripts Generated**
   - Executable test scripts from `generate-tests`
   - Test plan documentation `M{X}S{Y}T{Z}.md`

2. **Implementation Code**
   - Implementation files from `implement-specification`
   - Completion report `M{X}S{Y}C.md`

### Setup

1. **Locate Tests:**
   ```bash
   # Find test scripts
   glob path="tests/M{X}/*.py"
   glob path="tests/M{X}/*.sh"
   ```

2. **Execute Tests:**
   ```bash
   # Run tests (offline, dry-run, or real execution)
   ./tests/M{X}/test_runner.sh
   ```

3. **Analyze Traces:**
   ```bash
   # Read stack traces, test results, UI errors
   read "milestones/M{X}/test_output.txt"
   ```

## Best Practices

### Before Evaluating

**Use evaluate-implementation when:**
- Test scripts have been generated
- Implementation is complete
- You want to catch and fix minor bugs before review

**Avoid evaluate-implementation when:**
- Tests are structurally wrong (let `generate-tests` handle it)
- Major architectural changes are needed
- You need to modify specifications or milestones

### Auto-Fix Guidelines

**Fix Only:**
- Minor logical errors
- Typos
- Missing basic connections
- Simple type mismatches

**Do NOT Fix:**
- Structurally wrong tests
- Major architectural changes
- Missing API definitions
- Specification violations

## Output

**Evaluation Report:**
- File: `milestones/M{X}/M{X}S{Y}E.md`
- Format: Evaluation template from `templates/evaluation_template.md`
- Contents: Test execution results, auto-fixed bugs, remaining failures

**Test Scripts:**
- Executable test files in `tests/M{X}/` directory

## Out of Scope

**Never:**
- Rewrite testing scripts entirely if structurally wrong
- Make major architectural changes or rewrite entire modules
- Modify specifications, milestones, or canonical documentation
- Create README.md, SUMMARY.md, .txt files, or generic documentation

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

## Troubleshooting

**Tests fail due to minor issues:**
- Use `edit` tool to fix the specific lines
- Re-run tests to verify fix

**Tests fail due to structural issues:**
- Document as "Remaining Failure" in evaluation report
- Do NOT attempt to fix
- Hand off to human or use `hotfix-issue`

## Template Reference

- **Evaluation Template**: `~/devcode/aef/agent/templates/evaluation_template.md`
