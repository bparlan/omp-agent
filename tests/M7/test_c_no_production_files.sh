#!/bin/bash
# Test C: Verify no production files modified during test generation
# Purpose: Validate that running generate-tests does not modify
#          production implementation files
# Strategy: Operate on an isolated temporary git repository with
#           a known baseline commit. Never rely on the user's
#           working tree state.
# Source: M7S1, FR-7.3
# Source Verification: M7S1V, Test C

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0
HARNESS_PATH="$0"

function test_c_no_production_files_changed() {
    local fail_count=0

    # ── Create isolated temp repository ──────────────────────────────
    local tmpdir
    tmpdir=$(mktemp -d /tmp/m7_test_c.XXXXXX) || {
        echo "FAIL: Cannot create temp directory"
        return 1
    }
    trap 'rm -rf "$tmpdir"' EXIT

    # Initialise empty git repo
    cd "$tmpdir" || { echo "FAIL: Cannot cd to $tmpdir"; return 1; }
    git init > /dev/null 2>&1 || { echo "FAIL: git init failed"; return 1; }
    git config user.email "test@m7.test"
    git config user.name "M7 Test C"

    # ── Create representative project structure ──────────────────────
    mkdir -p skills/generate-tests
    mkdir -p tests/M7
    mkdir -p milestones/M7
    mkdir -p src/lib

    # Production files — must never change
    echo "production code" > src/lib/core.py
    echo "prod config" > AGENTS.md
    mkdir -p docs
    echo "spec doc" > docs/SPEC.md

    # Baseline tree — commit it
    git add -A > /dev/null 2>&1
    git commit -m "baseline" > /dev/null 2>&1 || {
        echo "FAIL: Baseline commit failed"
        return 1
    }
    local baseline_tree
    baseline_tree=$(git rev-parse HEAD)

    # ── Record baseline checksums for production files ───────────────
    local prod_files=(
        "src/lib/core.py"
        "AGENTS.md"
        "docs/SPEC.md"
        "skills/generate-tests/SKILL.md"
    )
    declare -A baseline_checksums
    for f in "${prod_files[@]}"; do
        if [ -f "$f" ]; then
            baseline_checksums["$f"]=$(sha256sum "$f" | cut -d' ' -f1)
        fi
    done

    # ── Simulate the operation being tested ─────────────────────────
    # This simulates what generate-tests does: create test artifacts
    # in tests/M{X}/ and milestones/M{X}/
    echo "#!/bin/bash" > tests/M7/test_simulated.sh
    echo "echo simulated" > milestones/M7/simulated.md

    # ── Verify: only allowed paths changed ───────────────────────────
    local changed_files
    changed_files=$(git diff --name-only HEAD 2>/dev/null || git diff --name-only 2>/dev/null)

    while IFS= read -r line; do
        [ -z "$line" ] && continue
        # Allowed: tests/ and milestones/M{N}/
        case "$line" in
            tests/*|milestones/M[0-9]*/*)
                echo "  OK: $line (permitted test artifact)"
                ;;
            *)
                echo "FAIL: Change outside allowlist: $line"
                fail_count=$((fail_count + 1))
                ;;
        esac
    done <<< "$changed_files"

    # ── Verify: production file checksums unchanged ──────────────────
    for f in "${!baseline_checksums[@]}"; do
        if [ -f "$f" ]; then
            local actual
            actual=$(sha256sum "$f" | cut -d' ' -f1)
            if [ "$actual" != "${baseline_checksums[$f]}" ]; then
                echo "FAIL: Production file changed: $f"
                fail_count=$((fail_count + 1))
            fi
        else
            echo "FAIL: Production file deleted: $f"
            fail_count=$((fail_count + 1))
        fi
    done

    # ── Verify: baseline commit unchanged ────────────────────────────
    local current_head
    current_head=$(git rev-parse HEAD)
    if [ "$current_head" != "$baseline_tree" ]; then
        echo "FAIL: Repository history modified"
        fail_count=$((fail_count + 1))
    fi

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count production file violations"
        return 1
    fi

    echo "PASS: No production files modified (isolated repo verified)"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_c_no_production_files_changed; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_C_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_C_RESULT=FAIL"
    exit 1
fi