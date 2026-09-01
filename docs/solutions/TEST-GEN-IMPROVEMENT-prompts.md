# Test Generation Skill Improvement - Actionable Prompts

## Simple Prompts for `milestoner` Enhancement

### Prompt 1: Milestone Structure Validation
```
When creating milestone M{X}, verify:
- Has exactly 4 specs: M{X}S1, M{X}S2, M{X}S3, M{X}S4
- Each spec has unique ownership
- M{X}S1 ≠ M{X}S2+ (no shared responsibilities)
- Spec layering rules are enforced

Action: Add validation that rejects milestones violating spec ownership boundaries
```

### Prompt 2: Artifact Creation Completeness
```
For artifact-creating skills, enforce:
1. Determine artifact type before creation
2. Assign canonical identity before creation
3. Generate required metadata before creation
4. Validate metadata before creation
5. Place in canonical storage before creation
6. Report identity and resolved path after creation

Action: Add validation that requires all 6 steps before reporting success
```

### Prompt 3: Specification Scope Enforcement
```
When processing milestones, validate:
- M{X}S1 owns: core infrastructure (registry, resolver, validator, types, legacy, traceability)
- M{X}S2 owns: project configuration (.omp/config.yml schema, validation)
- M{X}S3+ owns: skill integration behavioral contracts
- No spec may redefine skill as CLI executable contract

Action: Add validation that rejects scope violations and provides clear error messages
```

## Simple Prompts for `generate-spec` Enhancement

### Prompt 1: Concrete Contract Extraction
```
For each requirement in M{X}.md:
- Convert prose to mechanical contracts
- Provide exact CLI commands or file paths
- Define specific function signatures or methods
- Include exit codes or error conditions

Example:
- "Generate CLI tool" → "Create src/omp_cli/validate_metadata.py with validate_file() exit codes"
- "Support registry" → "Create src/core/artifacts/registry.py with register_type(), get_type() methods"

Action: Add requirement parser that validates contracts are concrete, not prose
```

### Prompt 2: Frontmatter Completeness
```
Generated specs must have:
- id: "SPEC-M{X}S{Y}" (exact format)
- type: "specification"
- title: "Concrete title describing scope"
- milestone_id: "M{X}"
- derived_from: ["SPEC-M{X}S{Y-1}"] (never circular)
- status: "draft" (or other valid statuses)

Action: Add frontmatter validator that rejects any missing or invalid fields
```

### Prompt 3: Placeholder Elimination
```
Scan all generated specs for:
- "?" values in any field
- Unresolved references (M{X}?, S{Y}?)
- Incomplete information ("TBD", "To be determined")
- Missing concrete values

Action: Add placeholder detector that forces concrete values before completion
```

## Simple Prompts for `generate-verification` Enhancement

### Prompt 1: Requirement-Test Mapping
```
For each requirement FR-{N} in M{X}S{Y}:
- Create at least ONE implementation test
- Test must FAIL on blank codebase (Exit Code 127)
- Test must PASS when implementation exists
- Test must validate actual functionality, not just existence

Action: Add requirement mapper that ensures every requirement has a corresponding test
```

### Prompt 2: Test Classification Enforcement
```
Classify each verification test as:
- IMPLEMENTATION_CHECK: Tests CLI tools/APIs (FAIL on blank)
- SPECIFICATION_CHECK: Tests schemas/docs (PASS immediately)
- ENVIRONMENT_CHECK: Tests setup/dependencies (PASS immediately)

Validation:
- IMPLEMENTATION_CHECK must have target (binary, function, method)
- SPECIFICATION_CHECK must not execute code
- ENVIRONMENT_CHECK must not validate implementation logic

Action: Add classifier that enforces proper test categorization
```

### Prompt 3: Behavioral Test Generation
```
Instead of generating "check if file exists" tests:
- Generate tests that verify actual functionality
- Include edge cases and error conditions
- Test performance and reliability scenarios
- Add integration testing where appropriate

Example:
- Bad: "if [ ! -f src/core/artifacts/registry.py ]"
- Good: "Test register_type() with valid/invalid inputs, verify error handling"

Action: Replace boilerplate tests with behavior-focused test generators
```

## Cross-Skill Quality Gate Prompts

### Prompt 1: Pre-Implementation Validation
```
Before any implementation:
1. Check M{X}TE.md status
2. Verify TESTS_RUN + TESTS_FAILED = total tests
3. Confirm VALID_INITIAL_FAILURES = expected failures
4. Ensure INVALID_TESTS = 0
5. Verify TDD_LEAKS = 0

Action: Add pre-implementation validator that blocks if any gate fails
```

### Prompt 2: Artifact Consistency Validation
```
Validate all artifacts have consistent structure:
- Same frontmatter fields across all .md files
- Consistent shebang formats in test files
- Meaningful exit codes (not hardcoded 127/0)
- Proper requirement traceability

Action: Add consistency checker that flags structural differences
```

### Prompt 3: Quality Reporting Automation
```
For each milestone M{X}:
- Generate quality score (0-100)
- List specific issues found
- Provide suggested fixes
- Recommend next steps

Action: Add quality reporter that summarizes artifact health automatically
```

## Implementation Checklist

### Week 1: Basic Validation
- [ ] Add milestone structure validation
- [ ] Implement frontmatter completeness check
- [ ] Add placeholder detector

### Week 2: Content Validation
- [ ] Implement requirement-to-test mapper
- [ ] Add test classifier validator
- [ ] Create behavioral test generator

### Week 3: Integration
- [ ] Deploy cross-skill quality gates
- [ ] Add artifact consistency checker
- [ ] Implement quality reporting system

### Week 4: Enhancement
- [ ] Add automated repair suggestions
- [ ] Implement continuous improvement tracking
- [ ] Create documentation and training

## Success Metrics

### Quality Gates
- 100% specs pass frontmatter validation
- 0% tests classified incorrectly
- 0% requirements without corresponding tests

### Process Improvements
- Quality checks complete in <30 seconds
- <5% artifacts rejected for quality issues
- <24 hours to fix quality rejections

## Recommended Starting Point

Begin with these 3 simple prompts:
1. `milestoner` - Add milestone structure validation
2. `generate-spec` - Add frontmatter completeness check
3. `generate-verification` - Add requirement-to-test mapping validation

These provide immediate quality improvement with minimal implementation complexity.
