#!/bin/bash

set -euo pipefail

# This script enforces the 'No Prose Contracts' rule by checking for forbidden patterns
# in verification artifacts, ensuring they are properly tagged.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <verification_artifact_file>"
    exit 1
fi

VERIFICATION_FILE="$1"
FORBIDDEN_PATTERNS=("grep" "text search" "text-match" "text matching")
ALLOWED_TAG="<!-- ALLOWED: literal-boilerplate -->"

EXIT_CODE=0
OFFENDING_LINES=() # Array to store offending lines

while IFS= read -r line || [[ -n "$line" ]]; do
    is_forbidden=false
    for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
        # Case-insensitive check for forbidden patterns
        if echo "$line" | grep -qi "$pattern"; then
            is_forbidden=true
            break
        fi
    done

    if $is_forbidden; then
        # Check if the line is NOT tagged
        if ! echo "$line" | grep -q "$ALLOWED_TAG"; then
            OFFENDING_LINES+=("$line")
            EXIT_CODE=1
        fi
    fi
done < "$VERIFICATION_FILE"

if [ $EXIT_CODE -ne 0 ]; then
    echo "Error: Found forbidden verification patterns without the required tag. Offending lines:"
    for offending_line in "${OFFENDING_LINES[@]}"; do
        echo "  $offending_line"
    done
    exit 1
else
    echo "Verification contract linting passed. No forbidden patterns found without the required tag."
    exit 0
fi
