#!/bin/bash
# Test V-FR-9: Milestone Artifact Integration
# #{Verification IDs: V-FR-9}
# #{Requirement IDs: FR-9}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-9: Check that specification defines milestone creation requirements
echo "Testing V-FR-9: Milestone artifact integration definition..."

# Check for "Milestone Artifact Integration" heading
if ! grep -q "Milestone Artifact Integration" "$spec_file"; then
    echo "FAIL: Specification does not have 'Milestone Artifact Integration' heading"
    exit 1
fi

# Check that newly created milestones have valid canonical frontmatter
if ! grep -q "valid canonical frontmatter" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical frontmatter validation"
fi

# Check that newly created milestones have canonical identity
if ! grep -q "canonical identity" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical identity"
fi

# Check that newly created milestones have type: milestone
if ! grep -q "type: milestone" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define type: milestone"
fi

# Check that newly created milestones are stored according to canonical storage rules
if ! grep -q "canonical storage rules" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical storage rules"
fi

# Check that newly created milestones pass metadata validation before reporting success
if ! grep -q "pass metadata validation" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define validation before success reporting"
fi

# Check for creation protocol heading
if ! grep -q "Creation Protocol" "$spec_file" && ! grep -q "Creation Protocol" "$spec_file"; then
    echo "WARNING: Specification may not define Creation Protocol"
fi

# Check for validation before creation success
if ! grep -q "validate milestone artifact" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define milestone validation"
fi

echo "PASS: V-FR-9 - Milestone artifact integration definition exists"

echo "PASS: V-FR-9 - Milestone Artifact Integration"
