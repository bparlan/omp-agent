#!/bin/bash
# Test V-FR-3: Canonical Artifact Creation
# #{Verification IDs: V-FR-3}
# #{Requirement IDs: FR-3}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-3: Check that specification defines the 7-step creation protocol
echo "Testing V-FR-3: 7-step creation protocol definition..."

# Check for "7-step creation protocol" or similar
if ! grep -q "7-step" "$spec_file" && ! grep -q "seven-step" "$spec_file"; then
    echo "FAIL: Specification does not define the 7-step creation protocol"
    exit 1
fi

# Check for "7-Step Creation Protocol" heading
if ! grep -q "7-Step Creation Protocol" "$spec_file"; then
    echo "WARNING: Specification may not explicitly use '7-Step Creation Protocol' heading"
fi

# Extract and verify the 7 steps
# Step 1: Determine artifact type
if ! grep -q "determine the artifact type" "$spec_file"; then
    echo "FAIL: Step 1 missing - determine the artifact type"
    exit 1
fi

# Step 2: Assign or request canonical artifact identity
if ! grep -q "assign or request canonical artifact identity" "$spec_file"; then
    echo "FAIL: Step 2 missing - assign or request canonical artifact identity"
    exit 1
fi

# Step 3: Generate required metadata
if ! grep -q "generate required metadata" "$spec_file"; then
    echo "FAIL: Step 3 missing - generate required metadata"
    exit 1
fi

# Step 4: Write canonical frontmatter
if ! grep -q "write canonical frontmatter" "$spec_file"; then
    echo "FAIL: Step 4 missing - write canonical frontmatter"
    exit 1
fi

# Step 5: Place artifact in canonical storage location
if ! grep -q "place the artifact in its canonical storage location" "$spec_file"; then
    echo "FAIL: Step 5 missing - place artifact in canonical storage location"
    exit 1
fi

# Step 6: Validate resulting artifact
if ! grep -q "validate the resulting artifact" "$spec_file"; then
    echo "FAIL: Step 6 missing - validate the resulting artifact"
    exit 1
fi

# Step 7: Report created artifact identity and resolved path
if ! grep -q "report the created artifact identity" "$spec_file" && ! grep -q "report.*artifact identity" "$spec_file"; then
    echo "FAIL: Step 7 missing - report created artifact identity and resolved path"
    exit 1
fi

echo "PASS: V-FR-3 - 7-step creation protocol defined"

echo "PASS: V-FR-3 - Canonical Artifact Creation"
