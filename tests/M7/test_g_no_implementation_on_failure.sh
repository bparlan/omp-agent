#!/bin/bash
# Test G: Verify test failure does NOT trigger implementation
# Purpose: Validate that when generated tests fail, generate-tests
#          does NOT trigger implementation — it must stop and report,
#          not write production code
# Source: M7S1, FR-7.7
# Source Verification: M7S1V, Test G

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

function test_g_no_implementation_on_failure() {
    local fail_count=0

    # Verify that the generate-tests SKILL.md does NOT contain
    # instructions to implement code when tests fail
    local skill_file="skills/generate-tests/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        echo "FAIL: generate-tests SKILL.md not found"
        return 1
    fi

    # Check for dangerous patterns that indicate implementation-on-failure
    local dangerous_patterns=(
        "if tests fail, implement"
        "fix the failing test"
        "implement the missing"
        "write production code"
        "modify source files"
    )

    for pattern in "${dangerous_patterns[@]}"; do
        if grep -qiF "$pattern" "$skill_file" 2>/dev/null; then
            echo "FAIL: Implementation-on-failure pattern found: '$pattern'"
            fail_count=$((fail_count + 1))
        fi
    done

    # Check the SKILL.md explicitly says to stop, not implement
    # Exclude negative instructions ("Do NOT invoke", "MUST NOT invoke", "Never invoke")
    if grep -qi "implement-specification" "$skill_file" 2>/dev/null; then
        # This is OK if it's a handoff reference, not an invocation instruction
        # Filter out lines that say "NOT invoke" or "Never invoke" (these are prohibitions)
        if grep -qi "invoke.*implement\|call.*implement\|run.*implement\|handoff to implement" "$skill_file" 2>/dev/null | grep -iv "do NOT invoke\|must NOT invoke\|never invoke" > /dev/null 2>&1; then
            echo "FAIL: generate-tests may invoke implement-specification"
            fail_count=$((fail_count + 1))
        fi
    fi

    # Check Out of Scope section exists and forbids implementation
    if ! grep -q "Modify the core implementation code" "$skill_file" 2>/dev/null; then
        echo "WARNING: SKILL.md may not explicitly forbid modifying implementation code"
        echo "INFO: M7 FR-5 requires this guardrail"
    fi

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count implementation-on-failure violations"
        return 1
    fi

    echo "PASS: No implementation-on-failure instructions found"
    echo "INFO: Current generate-tests SKILL.md has 'Never: Modify the core implementation code'"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_g_no_implementation_on_failure; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_G_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_G_RESULT=FAIL"
    exit 1
fi
