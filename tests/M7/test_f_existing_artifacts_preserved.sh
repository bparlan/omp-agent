#!/bin/bash
# Test F: Verify existing milestone artifacts preserved
# Purpose: Validate that M6/M6S1/M6S1V and other legacy artifacts
#          remain unchanged after test generation
# Source: M7S1, FR-7.6
# Source Verification: M7S1V, Test F

TESTS_RUN=0
TESTS_PASS=0
TESTS_FAIL=0

function test_f_existing_artifacts_preserved() {
    local fail_count=0

    # Known checksums captured before test generation (from initial state)
    # These represent the expected, immutable state of legacy artifacts
    local -A expected_checksums
    expected_checksums["milestones/M6/M6.md"]="a7d7ca0d8ad09938b73b415c7c7d49147c66a7b7ce419c9b85b33287031fdc97"
    expected_checksums["milestones/M6/M6S1.md"]="d641f29ea5ee7b7cb2aa1e5b583d0572e1e259e6ac7aef29df2b260c233b5881"
    expected_checksums["milestones/M6/M6S1V.md"]="d1f0ba06548891e211b11145bead95054329f34e4b815a83287c20a9947dbbcd"
    expected_checksums["milestones/M5/M5.md"]="87968e1813f2faddb60edac1788843337dc2a27263e063442cafe21dd8abc18d"
    expected_checksums["milestones/M5/M5S1.md"]="c65520c8323749ed2e6faeadebbd4b13b8d8db9ca8ce0bb4ef1070db004ae1fc"

    # Check each artifact
    for artifact in "${!expected_checksums[@]}"; do
        if [ ! -f "$artifact" ]; then
            echo "FAIL: Artifact missing (may have been deleted): $artifact"
            fail_count=$((fail_count + 1))
            continue
        fi

        local actual
        actual=$(shasum -a 256 "$artifact" 2>/dev/null | cut -d' ' -f1)
        local expected="${expected_checksums[$artifact]}"

        if [ "$actual" != "$expected" ]; then
            echo "FAIL: Artifact checksum mismatch for $artifact"
            echo "  Expected: $expected"
            echo "  Actual:   $actual"
            fail_count=$((fail_count + 1))
        else
            echo "PASS: $artifact — checksum verified"
        fi
    done

    # Check that no milestone directories were deleted
    for dir in milestones/M3 milestones/M4 milestones/M5 milestones/M6; do
        if [ ! -d "$dir" ]; then
            echo "FAIL: Milestone directory missing: $dir"
            fail_count=$((fail_count + 1))
        fi
    done

    if [ "$fail_count" -gt 0 ]; then
        echo "FAILED: $fail_count artifact preservation violations"
        return 1
    fi

    echo "PASS: All existing artifacts preserved"
    return 0
}

TESTS_RUN=$((TESTS_RUN + 1))
if test_f_existing_artifacts_preserved; then
    TESTS_PASS=$((TESTS_PASS + 1))
    echo "TEST_F_RESULT=PASS"
    exit 0
else
    TESTS_FAIL=$((TESTS_FAIL + 1))
    echo "TEST_F_RESULT=FAIL"
    exit 1
fi
