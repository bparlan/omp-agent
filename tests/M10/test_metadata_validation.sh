#!/bin/bash

# Self-validity check: Ensure necessary tools are available.
command -v grep >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'grep' command not found."; exit 2; }
command -v yq >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'yq' command not found. Please install yq (https://github.com/mikefarah/yq)."; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'bash' command not found."; exit 2; }

echo "Running Metadata Validation Tests..."

# Test 1: Verify presence and structure of YAML frontmatter in .md artifacts.
# This test checks for files with .md extension that are expected to have YAML frontmatter.
# We'll look in milestones/ and potentially other relevant directories.

echo "Testing for YAML frontmatter in .md artifacts..."
# Adjust the path globbing if M10S2.md implies other locations for .md artifacts.
# For now, checking milestones/ and potentially a broader search if needed.
found_frontmatter_issues=false

# Find .md files that are likely to contain metadata (e.g., in milestones/)
# Exclude the test design doc itself to avoid testing the test.
find milestones/ -name "*.md" ! -name "*T*.md" -print0 | while IFS= read -r -d $'\0' file;
do
    if ! yq eval --exit-status '. | select(true)' "$file" > /dev/null 2>&1; then
        echo "FAIL: File '$file' is missing YAML frontmatter or is not valid YAML."
        found_frontmatter_issues=true
    else
        echo "PASS: File '$file' has valid YAML frontmatter."
    fi
done

# Test 2: Validate mandatory metadata fields (`id`, `type`, `title`, `milestone_id`, `status`).
# This requires parsing the YAML frontmatter. Using yq for this.

echo "Testing for mandatory metadata fields..."

# List of mandatory fields, derived from M10S2V.md and M10S1V.md context.
# M10S2V.md mentions: `id`, `type`, `title`, `milestone_id`, `status` (EC-M10S2-3)
# M10S1V.md mentions: `id`, `type`, `title`, `milestone_id`, `status` (Implicitly required for canonical metadata model)
mandatory_fields=( "id" "type" "title" "milestone_id" "status" )

while IFS= read -r -d $'\0' file;
do
    echo "Checking metadata fields in '$file'..."

    # Extract YAML frontmatter using yq
    metadata=$(yq eval '.' "$file")

    fields_present=0
    for field in "${mandatory_fields[@]}"; do
        # Check if field exists and is not null/empty string
        if yq eval "has('$field')" <<< "$metadata" | grep -q "true"; then
            field_value=$(yq eval ".$field" <<< "$metadata")
            if [ "$field_value" != "" ] && [ "$field_value" != "null" ]; then
                echo "  PASS: Mandatory field '$field' is present and has a value."
            else
                echo "  FAIL: Mandatory field '$field' is present but empty or null in '$file'."
                found_frontmatter_issues=true
            fi
        else
            echo "  FAIL: Mandatory field '$field' is missing in '$file'."
            found_frontmatter_issues=true
        fi
done
done < <(find milestones/ -name "*.md" ! -name "*T*.md" -print0)

if [ "$found_frontmatter_issues" = true ]; then
    exit 1
else
    echo "All metadata validation tests passed."
    exit 0
fi
