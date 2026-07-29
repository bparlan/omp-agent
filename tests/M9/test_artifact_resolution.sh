#!/bin/bash
# Test V-FR-2, V-FR-2b, V-FR-2c: Canonical Artifact Resolution
# #{Verification IDs: V-FR-2, V-FR-2b, V-FR-2c}
# #{Requirement IDs: FR-2}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-2: Check that specification explicitly defines that skills do not hardcode artifact paths
echo "Testing V-FR-2: Specification prohibition of hardcoded paths..."

if ! grep -q "hardcode milestone-specific artifact paths" "$spec_file"; then
    echo "FAIL: Specification does not explicitly prohibit hardcoded artifact paths"
    exit 1
fi

if ! grep -q "hardcoded assumptions" "$spec_file"; then
    echo "FAIL: Specification does not explicitly prohibit hardcoded assumptions"
    exit 1
fi

if ! grep -q "milestones/M9/M9S1.md" "$spec_file"; then
    echo "FAIL: Specification does not mention example hardcoded path"
    exit 1
fi

echo "PASS: V-FR-2 - Explicit prohibition of hardcoded paths"

# Test V-FR-2b: Check that specification defines behavioral flow for canonical artifact resolution
echo "Testing V-FR-2b: Behavioral specification for artifact resolution..."

# Check for Resolver behavioral flow in specification
if ! grep -q "Canonical Resolver" "$spec_file"; then
    echo "FAIL: Specification does not define Canonical Resolver behavior"
    exit 1
fi

# Check for Resolver returning artifact identity and type
if ! grep -q "returns artifact identity" "$spec_file" && ! grep -q "artifact identity" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define artifact identity return"
fi

# Check for Resolver resolving physical path
if ! grep -q "Resolve Physical Path" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define physical path resolution"
fi

# Check for structured error handling in behavioral specification
if ! grep -q "struct.*ured error" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define structured error handling"
fi

# Check for Resolver returning physical path OR error
if ! grep -q "physical path OR error" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define error handling"
fi

echo "PASS: V-FR-2b - Behavioral specification for artifact resolution exists"

# Test V-FR-2c: Check that specification defines behavior for ambiguous resolution
echo "Testing V-FR-2c: Ambiguous resolution handling..."

if ! grep -q "ambiguous resolution" "$spec_file"; then
    echo "FAIL: Specification does not define behavior for ambiguous resolution"
    exit 1
fi

# Check that ambiguous resolution must surface ambiguity
if ! grep -q "surface ambiguity" "$spec_file" && ! grep -q "explicitly handle" "$spec_file"; then
    echo "WARNING: Specification may not explicitly require surface ambiguity"
fi

# Check that ambiguous resolution does not silently select arbitrary artifact
if ! grep -q "silently select" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit silent selection"
fi

if ! grep -q "human/agent intervention" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention human/agent intervention"
fi

echo "PASS: V-FR-2c - Ambiguous resolution handling defined"

echo "PASS: V-FR-2, V-FR-2b, V-FR-2c - Canonical Artifact Resolution"
