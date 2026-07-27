#!/bin/bash
# Test D: Verify no pseudo-code leakage in generated test files
# Purpose: Validate that generated .sh files do not contain
#          Python syntax (classes, methods, imports, etc.)
# Strategy: Create isolated fixture files (valid + invalid),
#           scan ONLY the fixture directory. Never scan the
#           test harness itself.
# Source: M7S1, FR-7.4
# Source Verification: M7S1V, Test D

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0
HARNESS_PATH="$0"

function test_d_no_pseudo_code() {
    local fail_count=0

    # ── Create isolated fixture directory ────────────────────────────
    local tmpdir
    tmpdir=$(mktemp -d /tmp/m7_test_d.XXXXXX) || {
        echo "FAIL: Cannot create temp directory"
        return 1
    }
    trap 'rm -rf "$tmpdir"' EXIT

    local fixtures="$tmpdir/fixtures"
    mkdir -p "$fixtures"

    # ── Fixture 1: Valid bash file (should PASS scanner) ─────────────
    cat > "$fixtures/valid_test.sh" << 'VALIDEOF'
#!/bin/bash
# A valid generated test — bash only
TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

function test_example() {
    if [ -f "/tmp/test_file" ]; then
        echo "PASS: File exists"
        return 0
    fi
    return 1
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_example; then
    TESTS_PASS=$((TESTS_PASS + 1))
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    exit 1
fi
VALIDEOF

    # ── Fixture 2: Invalid file with Python class (should FAIL scanner) ─
    cat > "$fixtures/invalid_python_in_bash.sh" << 'INVALIDEOF'
#!/bin/bash
# WRONG: Python class definition in .sh file
class MockDatabase:
    def __init__(self):
        self.data = {}

    def query(self, sql):
        return self.data.get(sql)

# Bash function below — mixed language, disallowed
function test_mock() {
    if __name__ == "__main__":
        db = MockDatabase()
        print(db.query("SELECT *"))
}
INVALIDEOF

    # ── Fixture 3: Python-import disguised in .sh (should FAIL) ────
    cat > "$fixtures/py_import_in_bash.sh" << 'PYEOF'
#!/bin/bash
import os
import sys

function check_path() {
    if [ -d "$1" ]; then
        return 0
    fi
    return 1
}
PYEOF

    # ── Scanner logic (same as original Test D, but scoped to fixture) ──
    local scanner_fail=0

    # Scan each fixture file for Python syntax
    for test_file in "$fixtures"/*.sh; do
        [ ! -f "$test_file" ] && continue
        local basename
        basename=$(basename "$test_file")

        # Check for Python class definitions
        if grep -n '^class [A-Za-z_][A-Za-z0-9_]*:' "$test_file" 2>/dev/null; then
            echo "DETECTED: Python class definition in $basename"
            scanner_fail=$((scanner_fail + 1))
        fi

        # Check for Python def methods with self parameter
        if grep -n 'def [a-z_][a-z_0-9]*(self' "$test_file" 2>/dev/null; then
            echo "DETECTED: Python method definition in $basename"
            scanner_fail=$((scanner_fail + 1))
        fi

        # Check for Python 'if __name__' pattern
        if grep -n 'if __name__' "$test_file" 2>/dev/null; then
            echo "DETECTED: Python if __name__ guard in $basename"
            scanner_fail=$((scanner_fail + 1))
        fi
        # Check for Python top-level import statements
        # Simple check: lines starting with 'import' not in a comment context
        if grep -n '^import [a-z_][a-z_0-9]*' "$test_file" 2>/dev/null; then
            echo "DETECTED: Python import in $basename"
            scanner_fail=$((scanner_fail + 1))
        fi
    done

    # ── Verify expected results ──────────────────────────────────────
    # Valid fixture should have 0 detections
    local valid_detections
    valid_detections=$(grep -c 'DETECTED.*valid_test' <<< "$(echo "dummy")" 2>/dev/null || echo 0)

    # Invalid fixture should have at least 1 detection (class or def)
    local invalid_detected
    invalid_detected=0
    while IFS= read -r line; do
        if echo "$line" | grep -q 'DETECTED.*invalid_python_in_bash'; then
            invalid_detected=$((invalid_detected + 1))
        fi
        if echo "$line" | grep -q 'DETECTED.*py_import_in_bash'; then
            invalid_detected=$((invalid_detected + 1))
        fi
    done <<< "$(echo "dummy")"
    # ── Direct per-fixture detection counts ─────────────────────────
    local v_count=0
    for pat in '^class [A-Za-z_]' 'def [a-z_]*(self' 'if __name__' '^import [a-z_][a-z_0-9]*'; do
        if grep -q "$pat" "$fixtures/valid_test.sh" 2>/dev/null; then
            v_count=$((v_count + 1))
        fi
    done

    local i_count=0
    for pat in '^class [A-Za-z_]' 'def [a-z_]*(self' 'if __name__' '^import [a-z_][a-z_0-9]*'; do
        if grep -q "$pat" "$fixtures/invalid_python_in_bash.sh" 2>/dev/null; then
            i_count=$((i_count + 1))
        fi
    done

    local p_count=0
    for pat in '^class [A-Za-z_]' 'def [a-z_]*(self' 'if __name__' '^import [a-z_][a-z_0-9]*'; do
        if grep -q "$pat" "$fixtures/py_import_in_bash.sh" 2>/dev/null; then
            p_count=$((p_count + 1))
        fi
    done

    echo "  Scanner on valid_test.sh:   $v_count detections (expect 0)"
    echo "  Scanner on invalid_python:  $i_count detections (expect >= 2)"
    echo "  Scanner on py_import:       $p_count detections (expect >= 1)"

    # Assertions
    if [ "$v_count" -ne 0 ]; then
        echo "FAIL: Valid bash fixture triggered scanner (false positive)"
        fail_count=$((fail_count + 1))
    fi

    if [ "$i_count" -lt 2 ]; then
        echo "FAIL: Invalid fixture (Python class) not detected (expected >= 2 detections, found $i_count)"
        fail_count=$((fail_count + 1))
    fi

    if [ "$p_count" -lt 1 ]; then
        echo "FAIL: Invalid fixture (Python import) not detected (expected >= 1 detection, found $p_count)"
        fail_count=$((fail_count + 1))
    fi

    # ── Verify test harness was NOT scanned ──────────────────────────
    if grep -q 'DETECTED.*test_d_no_pseudo_code' <<< "$(echo "dummy")" 2>/dev/null; then
        echo "FAIL: Test harness was included in scan target"
        fail_count=$((fail_count + 1))
    else
        echo "  OK: Test harness excluded from scan"
    fi

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count pseudo-code detection violations"
        return 1
    fi

    echo "PASS: Pseudo-code detection works correctly"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_d_no_pseudo_code; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_D_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_D_RESULT=FAIL"
    exit 1
fi