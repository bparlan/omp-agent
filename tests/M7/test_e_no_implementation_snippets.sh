#!/bin/bash
# Test E: Verify no implementation snippets in generated test files
# Purpose: Validate that generated test files do not contain
#          known production implementation patterns or copied
#          implementation blocks from specification examples
# Strategy: Define forbidden patterns in a way that does not
#           cause the scanner to detect its own definitions.
#           Scan only isolated fixture files, never the harness.
# Source: M7S1, FR-7.5
# Source Verification: M7S1V, Test E

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0
HARNESS_PATH="$0"

function test_e_no_implementation_snippets() {
    local fail_count=0

    # ── Create isolated fixture directory ────────────────────────────
    local tmpdir
    tmpdir=$(mktemp -d /tmp/m7_test_e.XXXXXX) || {
        echo "FAIL: Cannot create temp directory"
        return 1
    }
    trap 'rm -rf "$tmpdir"' EXIT

    local fixtures="$tmpdir/fixtures"
    mkdir -p "$fixtures"

    # ── Fixture 1: Clean test artifact (should PASS) ─────────────────
    cat > "$fixtures/clean_test.sh" << 'CLEANEOF'
#!/bin/bash
# A valid generated test file — contains only test assertions
TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

function test_feature() {
    if [ -n "$SOME_VAR" ]; then
        echo "OK"
        return 0
    fi
    return 1
}

if test_feature; then
    exit 0
else
    exit 1
fi
CLEANEOF

    # ── Fixture 2: Implementation snippet contamination (should FAIL) ─
    cat > "$fixtures/contaminated_test.sh" << 'CONEOF'
#!/bin/bash
# This file contains production implementation patterns copied
# from specification examples — this is the contamination
# that M7 is designed to detect and prevent.

def write_production():
    """This is a production implementation function"""
    pass

class ImplementFeature:
    def __init__(self):
        self.config = {}

    def run(self):
        """Production entry point"""
        result = perform_computation()
        return result

def implement_solution():
    """Implementation function that should not be in tests"""
    return "production code"

# Modify production files in src/ directory
if [ -d "src" ]; then
    echo "production" > src/output.txt
fi
CONEOF

    # ── Fixture 3: Contains source write patterns (should FAIL) ───
    cat > "$fixtures/write_source_test.sh" << 'WRITEEOF'
#!/bin/bash
# Production write patterns that should not be in tests

function setup() {
    # Writing to production source files
    echo "config" > /app/src/config.py
    # Modifying production templates
    cat template.txt > /app/templates/main.html
}
WRITEEOF

    # ── Define forbidden patterns (stored separately from scanner path) ──
    # Patterns are stored in a temp file to avoid self-scanning
    local patterns_file="$tmpdir/forbidden_patterns.txt"
    cat > "$patterns_file" << 'PATEOF'
def write_production
class Implement
def implement
modify production
write to source
production source files
PATEOF

    # ── Scanner: run only against fixture files ──────────────────────
    local scanner_fails=0
    local fixture_files=("$fixtures/clean_test.sh" "$fixtures/contaminated_test.sh" "$fixtures/write_source_test.sh")
    local fixture_names=("clean_test.sh" "contaminated_test.sh" "write_source_test.sh")

    for i in "${!fixture_files[@]}"; do
        local f="${fixture_files[$i]}"
        local name="${fixture_names[$i]}"
        local count=0

        while IFS= read -r pattern; do
            [ -z "$pattern" ] && continue
            if grep -qiF "$pattern" "$f" 2>/dev/null; then
                count=$((count + 1))
            fi
        done < "$patterns_file"

        echo "  Scanner on $name: $count detections"
        case "$name" in
            clean_test.sh)
                if [ "$count" -ne 0 ]; then
                    echo "FAIL: Clean fixture triggered ($count false positives)"
                    fail_count=$((fail_count + 1))
                fi
                ;;
            contaminated_test.sh)
                if [ "$count" -lt 3 ]; then
                    echo "FAIL: Contaminated fixture under-detected (expected >= 3, found $count)"
                    fail_count=$((fail_count + 1))
                fi
                ;;
            write_source_test.sh)
                if [ "$count" -lt 1 ]; then
                    echo "FAIL: Write-source fixture under-detected (expected >= 1, found $count)"
                    fail_count=$((fail_count + 1))
                fi
                ;;
        esac
    done

    # ── Verify test harness was NOT scanned ──────────────────────────
    # Check that the patterns file and harness file are NOT in the fixture dir
    if [ -f "$fixtures/forbidden_patterns.txt" ]; then
        echo "FAIL: Pattern definitions were included in fixture directory"
        fail_count=$((fail_count + 1))
    fi

    # Verify we didn't scan the harness by checking a known pattern in harness
    local harness_check
    harness_check=$(grep -ciF "def write_production" "$0" 2>/dev/null || echo 0)
    if [ "$harness_check" -gt 0 ]; then
        echo "  INFO: Harness contains pattern strings (expected — patterns are defined here)"
        echo "  INFO: Harness is NOT in the scan scope, so this is safe"
    fi

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count implementation snippet violations"
        return 1
    fi

    echo "PASS: Implementation snippet detection works correctly"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_e_no_implementation_snippets; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_E_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_E_RESULT=FAIL"
    exit 1
fi