#!/bin/bash
# Test V-FR-1: Canonical Artifact Contract Adoption
# #{Verification IDs: V-FR-1}
# #{Requirement IDs: FR-1}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

if [[ ! -s "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file is empty"
    exit 1
fi

# Read specification file
spec_file="milestones/M9/M9S1.md"

# Parse YAML frontmatter using yq
echo "Using yq for YAML parsing..."

# Extract just the frontmatter (lines 1-10)
frontmatter=$(sed -n '1,10p' "$spec_file")

# Parse frontmatter with yq
type=$(echo "$frontmatter" | yq eval '.type')
milestone_id=$(echo "$frontmatter" | yq eval '.milestone_id')
id=$(echo "$frontmatter" | yq eval '.id')
status=$(echo "$frontmatter" | yq eval '.status')

# Check values
if [[ "$type" != "specification" ]]; then
    echo "FAIL: Type mismatch, expected 'specification', got '$type'"
    exit 1
fi

if [[ "$milestone_id" != "M9" ]]; then
    echo "FAIL: Milestone ID mismatch, expected 'M9', got '$milestone_id'"
    exit 1
fi

if [[ "$id" != "SPEC-M9S1" ]]; then
    echo "FAIL: ID mismatch, expected 'SPEC-M9S1', got '$id'"
    exit 1
fi

if [[ "$status" != "draft" ]]; then
    echo "FAIL: Status mismatch, expected 'draft', got '$status'"
    exit 1
fi

echo "PASS: V-FR-1 - Canonical Artifact Contract Adoption"

# Test V-FR-1: Check that specification defines canonical artifact model adoption
echo "Testing V-FR-1: Canonical artifact model adoption..."

# Check for FR-1 mention
if ! grep -q "adopt the M9 canonical artifact model" "$spec_file" && ! grep -q "canonical artifact model" "$spec_file"; then
    echo "FAIL: Specification does not define FR-1 — Canonical Artifact Contract Adoption"
    exit 1
fi

# Check that specification explicitly states all affected skills must adopt canonical model
if ! grep -q "All affected artifact-producing and artifact-consuming skills must adopt the M9 canonical artifact model" "$spec_file"; then
    echo "FAIL: Specification does not explicitly define canonical artifact model adoption"
    exit 1
fi

# Check that no affected skill independently defines competing schema
if ! grep -q "competing canonical artifact schema" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define schema competition prohibition"
fi

# Check that artifacts must use canonical identity, type, metadata, lineage, storage
if ! grep -q "decisions originate exclusively from the canonical artifact system" "$spec_file"; then
    echo "FAIL: Specification does not define artifact system requirements"
    exit 1
fi

canonical_system_keywords=('Artifact Registry' 'Resolver' 'Validator' 'canonical artifact system')
found_keywords=()
for kw in "${canonical_system_keywords[@]}"; do
    if grep -q "$kw" "$spec_file"; then
        found_keywords+=("$kw")
    fi
done

if [ ${#found_keywords[@]} -ge 2 ]; then
    echo "PASS: V-FR-1: Specification defines canonical system integration"
else
    echo "WARNING: Specification may not explicitly define all canonical system components"
fi

echo "PASS: V-FR-1 - Canonical Artifact Contract Adoption"
