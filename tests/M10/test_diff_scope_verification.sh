#!/bin/bash

# Self-validity check: Ensure necessary tools are available.
command -v git >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'git' command not found."; exit 2; }
command -v grep >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'grep' command not found."; exit 2; }
command -v cat >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'cat' command not found."; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'bash' command not found."; exit 2; }
command -v find >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'find' command not found."; exit 2; }
command -v xargs >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'xargs' command not found."; exit 2; }

echo "Running Diff-Scope Verification Test..."

# Test AV-M10S2-2: Diff-Scope Verification
# Description: Verify M10 changes are confined to an Allowlist, distinguish pre-existing vs. M10 changes, and flag contamination.

# --- Define the Allowlist for M10 specific changes ---
# This list specifies files expected to be modified by M10 work.
# It's derived from the test design document and M10S2V.md context.
# Any file modified that is NOT in this list, AND is not the explicitly contaminated file, is an M10 scope violation.

# Create a temporary file to hold the Allowlist.
ALLOWLIST_FILE="/tmp/allowlist_M10S2_$(date +%s).txt"
cat << EOF > "$ALLOWLIST_FILE"
# This is the M10 Allowlist. Files modified outside this list (excluding contamination) are scope violations.
milestones/M10/M10S1.md
milestones/M10/M10S2.md
milestones/M10/M10S2V.md
milestones/M10/M10S2T1.md
tests/M10/test_artifact_id_validation.sh
tests/M10/test_metadata_validation.sh
tests/M10/test_convention_adherence.sh
tests/M10/test_forbidden_infrastructure.sh
tests/M10/test_diff_scope_verification.sh
EOF

# Add SKILL.md files from skills directory to the allowlist (as M10 might impact conventions)
find skills/ -name "SKILL.md" >> "$ALLOWLIST_FILE"

# Add AGENTS.md and FRAMEWORK.md if they exist, as M10 might reference/impact them for conventions
if [ -f "AGENTS.md" ]; then echo "AGENTS.md" >> "$ALLOWLIST_FILE"; fi
if [ -f "FRAMEWORK.md" ]; then echo "FRAMEWORK.md" >> "$ALLOWLIST_FILE"; fi

# --- Contamination Check ---
# Check for modification of tools/generate_skeleton_from_python.py, which is assumed unrelated to M10.
CONTAMINATION_TARGET="tools/generate_skeleton_from_python.py"
contamination_found=false

echo "Checking for contamination: modification of $CONTAMINATION_TARGET..."
if git diff --name-only | grep -q "^$CONTAMINATION_TARGET$"; then
    echo "CONTAMINATED_TEST: Modification detected in $CONTAMINATION_TARGET, which is unrelated to M10 scope."
    contamination_found=true
fi

# --- M10 Scope Check ---
# Get all modified files.
ALL_MODIFIED_FILES=$(git diff --name-only)

if [ -z "$ALL_MODIFIED_FILES" ]; then
    echo "INFO: No file changes detected. Diff-scope verification passes trivially."
    rm "$ALLOWLIST_FILE"
    # If no contamination and no diffs, it's a VALID_PASS regarding M10 scope.
    # However, if contamination was found, the overall test must reflect that.
    if [ "$contamination_found" = true ]; then
        exit 1 # Fail the test because of contamination
    else
        exit 0 # Pass if no diff and no contamination
    fi
fi

echo "Detected file changes:\n$ALL_MODIFIED_FILES"

# Compare all modified files against the Allowlist and contamination target.
# A file is problematic if it's modified AND it's NOT in the M10 allowlist AND it's NOT the contaminated file.

found_m10_scope_violation=false

while IFS= read -r changed_file; do
    # Skip the known contaminated file if it was modified.
    if [ "$changed_file" = "$CONTAMINATION_TARGET" ]; then
        continue
    fi

    # Check if the changed file is in the M10 Allowlist.
    if ! grep -Fxq "$changed_file" "$ALLOWLIST_FILE"; then
        echo "VALID_INITIAL_FAILURE: Modified file \"$changed_file\" is outside M10 scope and not the known contamination target."
        found_m10_scope_violation=true
    fi
done <<< "$ALL_MODIFIED_FILES"

# Clean up the temporary allowlist file.
rm "$ALLOWLIST_FILE"

# Determine final exit code:
# If contamination was found, the test is CONTAMINATED_TEST (exit 1).
# If contamination was NOT found, but M10 scope violations were, it's VALID_INITIAL_FAILURE (exit 1).
# If neither contamination nor scope violations were found, and diffs existed, it implies changes were within M10 scope (VALID_PASS for scope, but might be VALID_INITIAL_FAILURE if expected M10 changes were not made - this test doesn't check for missing changes, only unauthorized ones).

if [ "$contamination_found" = true ]; then
    exit 1 # Contaminated test failure
elif [ "$found_m10_scope_violation" = true ]; then
    exit 1 # M10 scope violation failure
else
    # If no contamination and no scope violation, it means all changes were either M10-allowed or non-existent.
    # This counts as a pass for scope adherence purposes.
    echo "M10 scope adherence verified."
    exit 0 # Pass for scope adherence
fi
