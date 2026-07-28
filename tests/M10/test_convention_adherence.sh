#!/bin/bash

# Self-validity check: Ensure necessary tools are available.
command -v grep >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'grep' command not found."; exit 2; }
command -v find >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'find' command not found."; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'bash' command not found."; exit 2; }

echo "Running Convention Adherence Tests..."

# Test 1: Check for consistent application of metadata interpretation patterns in SKILL.md files.
# This is a conceptual check. In a real scenario, we'd parse SKILL.md and look for specific patterns.
# For now, we'll check if SKILL.md files exist and have a basic structure.

echo "Testing convention adherence in SKILL.md files..."

found_convention_issues=false

# Find all SKILL.md files within the skills directory.
skill_files=$(find skills/ -name "SKILL.md")

if [ -z "$skill_files" ]; then
    echo "INFO: No SKILL.md files found. Skipping convention adherence check for SKILL.md."
else
    for skill_file in $skill_files;
    do
        echo "Checking conventions in $skill_file..."

        # Basic check: Ensure the file is not empty and contains at least a header.
        # This is a weak check; a real test would parse and validate specific conventions.
        if [ ! -s "$skill_file" ]; then
            echo "FAIL: SKILL.md file '$skill_file' is empty."
            found_convention_issues=true
            continue
        fi

        # Check for a minimal header pattern (e.g., '# Skill Name')
        if ! grep -q "^# " "$skill_file"; then
            echo "FAIL: SKILL.md file '$skill_file' seems to be missing a primary header."
            found_convention_issues=true
            continue
        fi

        # Add more specific checks here based on known conventions for SKILL.md
        # Example: check for specific sections, mandatory fields, etc.
        # Without specific conventions from M10S2.md or AGENTS.md, these are placeholders.
        echo "PASS: SKILL.md file '$skill_file' has basic structure."
    done
fi

# Test 2: (Placeholder) Verify adherence to other documented conventions (e.g., AGENTS.md, FRAMEWORK.md).
# This test is highly dependent on the specific conventions defined in M10S2.md and related docs.
# For now, we'll assume basic adherence if the files exist.

echo "Verifying existence of key convention documents..."

if [ ! -f "AGENTS.md" ]; then
    echo "FAIL: AGENTS.md not found."
    found_convention_issues=true
elif [ ! -f "FRAMEWORK.md" ]; then
    echo "FAIL: FRAMEWORK.md not found."
    found_convention_issues=true
else
    echo "PASS: AGENTS.md and FRAMEWORK.md exist."
fi

# Add more checks as specific conventions become known from M10S2.md

if [ "$found_convention_issues" = true ]; then
    exit 1
else
    echo "All convention adherence tests passed."
    exit 0
fi
