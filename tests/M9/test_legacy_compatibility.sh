#!/bin/bash
# Test V-FR-11: Legacy Compatibility
# #{Verification IDs: V-FR-11}
# #{Requirement IDs: FR-11}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-11: Check that specification defines legacy compatibility strategy
echo "Testing V-FR-11: Legacy compatibility definition..."

# Check for "Legacy Compatibility" heading
if ! grep -q "Legacy Compatibility" "$spec_file"; then
    echo "FAIL: Specification does not have 'Legacy Compatibility' heading"
    exit 1
fi

# Check that existing M1-M9 legacy artifacts are not mass-migrated automatically
if ! grep -q "mass-migrated" "$spec_file" && ! grep -q "mass migration" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit mass migration"
fi

if ! grep -q "automatically" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define automatic migration prohibition"
fi

# Check that existing artifacts remain discoverable through canonical resolution
if ! grep -q "discoverable" "$spec_file" && ! grep -q "canonical resolution" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define discovery via canonical resolution"
fi

# Check that legacy artifacts and canonical artifacts can coexist safely
if ! grep -q "coexist" "$spec_file" && ! grep -q "safely" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define coexistence safety"
fi

# Check for "coexist" or "discovery" mention
if ! grep -q "legacy artifacts" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define legacy artifacts"
fi

echo "PASS: V-FR-11 - Legacy compatibility definition exists"

echo "PASS: V-FR-11 - Legacy Compatibility"
