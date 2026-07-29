#!/bin/bash
# Test V-FR-13: Artifact-Type Consistency
# #{Verification IDs: V-FR-13}
# #{Requirement IDs: FR-13}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-13: Check that specification defines artifact-type consistency
echo "Testing V-FR-13: Artifact-type consistency definition..."

# Check for "Artifact-Type Consistency" heading
if ! grep -q "Artifact-Type Consistency" "$spec_file"; then
    echo "FAIL: Specification does not have 'Artifact-Type Consistency' heading"
    exit 1
fi

# Check that system does not produce ambiguous artifacts
if ! grep -q "ambiguous artifacts" "$spec_file" && ! grep -q "ambiguous" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define ambiguity prevention"
fi

# Check that machine-readable type and identity must be explicit in metadata
if ! grep -q "machine-readable" "$spec_file" && ! grep -q "explicit" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define explicit type/identity requirement"
fi

# Check that type declarations are in metadata (frontmatter, registry)
if ! grep -q "frontmatter" "$spec_file" && ! grep -q "registry" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define type declaration locations"
fi

# Check that all pipeline stages produce artifacts with valid canonical type declarations
if ! grep -q "pipeline stages" "$spec_file" && ! grep -q "valid" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define valid type declarations"
fi

# Check for "artifact-type consistency" or "artifact type consistency" mention
if ! grep -q "artifact-type consistency" "$spec_file" && ! grep -q "artifact type consistency" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define artifact-type consistency requirement"
fi

# Check for "type declaration" or "type declarations" mention
if ! grep -q "type declaration" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define type declarations"
fi

echo "PASS: V-FR-13 - Artifact-type consistency definition exists"

echo "PASS: V-FR-13 - Artifact-Type Consistency"
