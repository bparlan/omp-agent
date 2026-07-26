#!/bin/bash
# M3S2 — FR-5: Ground-Truth Helper Utility
# Verifies that bin/ground-truth-check.sh exists, is executable, supports all
# 5 commands (file-exists, dir-exists, command-exists, file-contains, git-status),
# returns correct PASS/FAIL exit codes, and contains zero write operations.
# Usage: ./tests/M3/test_ground_truth_helper.sh

set -euo pipefail
FAILED=0
SCRIPT="bin/ground-truth-check.sh"
TMPDIR=""

report_pass() { echo "  PASS: $1"; }
report_fail() { echo "  FAIL: $1"; FAILED=1; }

cleanup() { [ -z "${TMPDIR:-}" ] || rm -rf "$TMPDIR"; }
trap cleanup EXIT

echo "=== FR-5: Ground-Truth Helper Utility ==="

# --- Test 1: File exists and is executable ---
if [ -f "$SCRIPT" ]; then
    report_pass "Script exists at $SCRIPT"
else
    report_fail "Script does NOT exist at $SCRIPT"
    echo "RESULT: FR-5 FAILED (script missing)"
    exit 1
fi

if [ -x "$SCRIPT" ]; then
    report_pass "Script is executable"
else
    report_fail "Script is NOT executable"
fi

# --- Test 2: --help prints usage ---
output=$("$SCRIPT" --help 2>&1) && rc=0 || rc=$?
if echo "$output" | grep -qiE "usage|synopsis|commands|file-exists"; then
    report_pass "--help prints usage information"
else
    report_fail "--help does not print usage (output: $output)"
fi

# --- Test 3: No args prints usage (no crash) ---
output=$("$SCRIPT" 2>&1) && rc=0 || rc=$?
if echo "$output" | grep -qiE "usage|synopsis|commands|file-exists"; then
    report_pass "No args prints usage (no crash)"
else
    report_fail "No args does not print usage or crashes (output: $output)"
fi

# --- Test 4: file-exists on existing file ---
output=$("$SCRIPT" file-exists "$SCRIPT" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^PASS"; then
    report_pass "file-exists existing file: PASS"
else
    report_fail "file-exists existing file: expected PASS, got: $output"
fi
if [ "$exitcode" -eq 0 ]; then
    report_pass "file-exists existing file: exit code 0"
else
    report_fail "file-exists existing file: expected exit 0, got $exitcode"
fi

# --- Test 5: file-exists on non-existing file ---
output=$("$SCRIPT" file-exists "/nonexistent_path_xyz_123_test" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^FAIL"; then
    report_pass "file-exists non-existing file: FAIL"
else
    report_fail "file-exists non-existing file: expected FAIL, got: $output"
fi
if [ "$exitcode" -eq 1 ]; then
    report_pass "file-exists non-existing file: exit code 1"
else
    report_fail "file-exists non-existing file: expected exit 1, got $exitcode"
fi

# --- Test 6: dir-exists on existing directory ---
output=$("$SCRIPT" dir-exists /tmp 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^PASS"; then
    report_pass "dir-exists /tmp: PASS"
else
    report_fail "dir-exists /tmp: expected PASS, got: $output"
fi
if [ "$exitcode" -eq 0 ]; then
    report_pass "dir-exists /tmp: exit code 0"
else
    report_fail "dir-exists /tmp: expected exit 0, got $exitcode"
fi

# --- Test 7: dir-exists on non-existing directory ---
output=$("$SCRIPT" dir-exists "/nonexistent_dir_xyz_123" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^FAIL"; then
    report_pass "dir-exists non-existing dir: FAIL"
else
    report_fail "dir-exists non-existing dir: expected FAIL, got: $output"
fi
if [ "$exitcode" -eq 1 ]; then
    report_pass "dir-exists non-existing dir: exit code 1"
else
    report_fail "dir-exists non-existing dir: expected exit 1, got $exitcode"
fi

# --- Test 8: command-exists on existing command ---
output=$("$SCRIPT" command-exists ls 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^PASS"; then
    report_pass "command-exists ls: PASS"
else
    report_fail "command-exists ls: expected PASS, got: $output"
fi
if [ "$exitcode" -eq 0 ]; then
    report_pass "command-exists ls: exit code 0"
else
    report_fail "command-exists ls: expected exit 0, got $exitcode"
fi

# --- Test 9: command-exists on non-existing command ---
output=$("$SCRIPT" command-exists "nonexistent_cmd_xyz_123" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^FAIL"; then
    report_pass "command-exists non-existing cmd: FAIL"
else
    report_fail "command-exists non-existing cmd: expected FAIL, got: $output"
fi
if [ "$exitcode" -eq 1 ]; then
    report_pass "command-exists non-existing cmd: exit code 1"
else
    report_fail "command-exists non-existing cmd: expected exit 1, got $exitcode"
fi

# --- Test 10: file-contains with matching pattern ---
output=$("$SCRIPT" file-contains "$SCRIPT" "PASS" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^PASS"; then
    report_pass "file-contains matching pattern: PASS"
else
    report_fail "file-contains matching pattern: expected PASS, got: $output"
fi
if [ "$exitcode" -eq 0 ]; then
    report_pass "file-contains matching pattern: exit code 0"
else
    report_fail "file-contains matching pattern: expected exit 0, got $exitcode"
fi

# --- Test 11: file-contains with non-matching pattern ---
output=$("$SCRIPT" file-contains "$SCRIPT" "UNLIKELY_STRING_ZZZ_123" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^FAIL"; then
    report_pass "file-contains non-matching pattern: FAIL"
else
    report_fail "file-contains non-matching pattern: expected FAIL, got: $output"
fi
if [ "$exitcode" -eq 1 ]; then
    report_pass "file-contains non-matching pattern: exit code 1"
else
    report_fail "file-contains non-matching pattern: expected exit 1, got $exitcode"
fi

# --- Test 12: git-status on existing directory ---
output=$("$SCRIPT" git-status "$(dirname "$SCRIPT")" 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^(PASS|FAIL)"; then
    report_pass "git-status on bin/ dir: returns PASS or FAIL"
else
    report_fail "git-status on bin/ dir: expected PASS or FAIL, got: $output"
fi

output=$("$SCRIPT" git-status /tmp 2>&1) && exitcode=0 || exitcode=$?
if echo "$output" | grep -qiE "^(PASS|FAIL)"; then
    report_pass "git-status on /tmp (no git): returns PASS or FAIL gracefully"
else
    report_fail "git-status on /tmp: expected PASS or FAIL, got: $output"
fi
if [ "$exitcode" -eq 1 ] || [ "$exitcode" -eq 0 ]; then
    report_pass "git-status on /tmp: exit code $exitcode (no crash)"
else
    report_fail "git-status on /tmp: unexpected exit code $exitcode"
fi

# --- Test 14: Write operation audit (no >, >>, mv, cp, rm, mkdir, touch, chmod, chown) ---
write_ops=$(grep -cPn -- '>[>]?|mv[[:space:]]|cp[[:space:]]|rm[[:space:]]|mkdir[ [:space:]]|touch[[:space:]]|chmod|chown' "$SCRIPT" 2>/dev/null || true)

# Filter out comments, string literals, and false positives
# Count lines that are NOT comments and contain write operations
dangerous_lines=$(grep -n -- '>[>]?\|mv[[:space:]]\|cp[[:space:]]\|rm[[:space:]]\|mkdir[[:space:]]\|touch[[:space:]]\|chmod\|chown' "$SCRIPT" 2>/dev/null | grep -v '^\s*#' | grep -v '^\s*: ' | grep -v '".*"' || true)

if [ -z "$dangerous_lines" ]; then
    report_pass "Write operation audit: CLEAN (zero write ops outside comments/strings)"
else
    report_fail "Write operation audit: Found potential write operations:"
    echo "$dangerous_lines" | while read -r line; do echo "    $line"; done
fi

# --- Test 15: Script header contains agent-facing documentation ---
header=$(head -30 "$SCRIPT")
if echo "$header" | grep -qiE "usage|usage|purpose|example|agent"; then
    report_pass "Script header contains agent-facing documentation"
else
    report_fail "Script header missing agent-facing documentation"
fi

echo "---"
if [ "$FAILED" -eq 0 ]; then
    echo "RESULT: FR-5 PASSED"
else
    echo "RESULT: FR-5 FAILED"
fi
exit "$FAILED"