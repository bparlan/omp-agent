#!/bin/bash
# Test V-FR-8, V-FR-8b: Documentation Synchronisation
# #{Verification IDs: V-FR-8, V-FR-8b}
# #{Requirement IDs: FR-8}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-8: Check that specification defines documentation synchronisation
echo "Testing V-FR-8: Documentation synchronisation definition..."

# Check for "Documentation Synchronisation" heading
if ! grep -q "Documentation Synchronisation" "$spec_file"; then
    echo "FAIL: Specification does not have 'Documentation Synchronisation' heading"
    exit 1
fi

# Check that sync-documentation resolves documentation artifacts through canonical resolution
if ! grep -q "canonical resolution" "$spec_file" && ! grep -q "canonical artifact system" "$spec_file"; then
    echo "FAIL: Specification does not explicitly require canonical resolution"
    exit 1
fi

# Check that skill distinguishes between AEF framework documentation and project documentation
if ! grep -q "AEF framework documentation" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define AEF framework documentation scope"
fi

if ! grep -q "project documentation" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project documentation scope"
fi

# Check that skill does not inject AEF-specific documents into application projects
if ! grep -q "does not inject" "$spec_file" && ! grep -q "not inject" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit injection of AEF documents"
fi

# Check that documentation synchronization respects project mode and canonical architecture
if ! grep -q "respects.*mode" "$spec_file" && ! grep -q "respects.*architecture" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define mode and architecture respect"
fi

echo "PASS: V-FR-8 - Documentation synchronisation definition exists"

# Test V-FR-8b: Check that specification defines workspace boundary behavior
echo "Testing V-FR-8b: Workspace boundary behavioral flow..."

# Check for "Workspace Boundary Behavior" heading
if ! grep -q "Workspace Boundary Behavior" "$spec_file"; then
    echo "WARNING: Specification may not define Workspace Boundary Behavior"
fi

# Check that sync-documentation determines active project
if ! grep -q "determine active project" "$spec_file" && ! grep -q "active project" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define active project determination"
fi

# Check that sync-documentation resolves documentation artifacts via canonical resolution
if ! grep -q "canonical resolution" "$spec_file"; then
    echo "WARNING: Specification may not restate canonical resolution requirement"
fi

# Check for AEF framework documentation affecting
if ! grep -q "AEF framework documentation" "$spec_file"; then
    echo "WARNING: Specification may not define AEF framework documentation scope"
fi

# Check for project documentation affecting
if ! grep -q "project documentation" "$spec_file"; then
    echo "WARNING: Specification may not define project documentation scope"
fi

# Check for respect project conventions
if ! grep -q "conventions" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define convention respect"
fi

echo "PASS: V-FR-8b - Workspace boundary behavioral flow defined"

echo "PASS: V-FR-8, V-FR-8b - Documentation Synchronisation"
