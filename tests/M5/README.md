# Test Suite for M5S1I1-CORRECTED

This directory contains executable test scripts that validate the fix for M5 test script hallucination (Python syntax in bash files).

## Test Scripts

### 1. test_1_python_syntax_check.sh
**Tests:** Test Case 1.1, 1.2, 1.3

Validates:
- No Python class definitions in bash files
- Bash scripts use bash function syntax
- Scripts have valid shebangs
- Bash scripts pass bash -n syntax validation

**Execution:**
```bash
bash tests/M5/test_1_python_syntax_check.sh
```

### 2. test_2_bash_syntax_validation.sh
**Tests:** Test Case 1.2, 1.4 (additional checks)

Validates:
- Bash function definitions count
- Test counter definitions (TESTS_RUN, TESTS_PASS, TESTS_FAIL)
- Comprehensive bash syntax checks
- Mock functions use bash syntax

**Execution:**
```bash
bash tests/M5/test_2_bash_syntax_validation.sh
```

### 3. test_3_template_constraints.sh
**Tests:** Test Case 2.1, 2.2, 2.3, 2.4

Validates:
- Template specifies bash script requirements
- Template prohibits embedded mock code
- Template enforces language extension consistency
- Template has complete documentation structure

**Execution:**
```bash
bash tests/M5/test_3_template_constraints.sh
```

### 4. test_4_skill_validation.sh
**Tests:** Test Case 3.1, 3.2, 3.3, 3.4, 3.5

Validates:
- generate-tests skill includes syntax validation gate
- Skill runs bash syntax check (bash -n)
- Skill runs Python syntax check (py_compile)
- Skill rejects completion if syntax errors found
- Skill marks test plan complete only after validation passes

**Execution:**
```bash
bash tests/M5/test_4_skill_validation.sh
```

### 5. test_5_regression_check.sh
**Tests:** Regression validation

Validates:
- M4 test suite still works (no regression)
- M3 test script still works (no regression)
- Exit codes are valid

**Execution:**
```bash
bash tests/M5/test_5_regression_check.sh
```

## Running All Tests

### Sequential Execution
```bash
bash tests/M5/test_1_python_syntax_check.sh
bash tests/M5/test_2_bash_syntax_validation.sh
bash tests/M5/test_3_template_constraints.sh
bash tests/M5/test_4_skill_validation.sh
bash tests/M5/test_5_regression_check.sh
```

### Combined Execution
```bash
for script in tests/M5/test_*.sh; do
    echo "Running $script..."
    bash "$script"
    echo ""
done
```

### All at Once
```bash
bash tests/M5/test_*.sh
```

## Expected Results

All tests should exit with code 0 and report "ALL TESTS PASSED" if the fix has been properly implemented.

### Success Indicators:
- No Python class definitions found in bash files
- All scripts pass `bash -n` syntax validation
- Template enforces bash syntax constraints
- generate-tests skill includes syntax validation
- M4 and M3 tests still work (no regression)

## Test Coverage

This test suite covers:
- **Functional Validation:** FR-1, FR-2, FR-3 (all functional requirements)
- **Edge Cases:** Empty inputs, invalid syntax, multiple scripts, exit code verification
- **Failure Scenarios:** Template lacks constraints, skill doesn't validate, Python syntax remains

## Derived From

- Verification Protocol: `milestones/M5/M5S1I1-CORRECTEDV.md`
- Specification: `milestones/M5/M5S1I1-CORRECTED.md`

## Test Plan Documentation

See `milestones/M5/M5S1I1-CORRECTEDT1.md` for the detailed test plan.
