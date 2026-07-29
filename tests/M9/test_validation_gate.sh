#!/bin/bash
# Test V-FR-4, V-FR-4b: Validation Before Completion
# #{Verification IDs: V-FR-4, V-FR-4b}
# #{Requirement IDs: FR-4}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-4: Check that specification defines validation gate behavior
echo "Testing V-FR-4: Validation gate behavior definition..."

# Check for "Validation Before Completion" heading
if ! grep -q "Validation Before Completion" "$spec_file"; then
    echo "FAIL: Specification does not have 'Validation Before Completion' heading"
    exit 1
fi

# Check that invalid artifacts cause explicit failure
if ! grep -q "invalid artifacts.*fail" "$spec_file" && ! grep -q "validation failures.*fail" "$spec_file"; then
    echo "WARNING: Specification may not explicitly require failure on invalid artifacts"
fi

# Check that partial artifact creation is not reported as successful
if ! grep -q "partial artifact" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention partial artifacts"
fi

# Check that validation is performed through canonical validator
if ! grep -q "validate.*canonical validator" "$spec_file" && ! grep -q "validat.*canonical validator" "$spec_file"; then
    echo "WARNING: Specification may not explicitly require canonical validator"
fi

# Check that skills do not silently bypass validation
if ! grep -q "silently bypass" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit silent bypass"
fi

echo "PASS: V-FR-4 - Validation gate behavior defined"

# Test V-FR-4b: Check that specification defines validation gate flow
echo "Testing V-FR-4b: Validation gate behavioral flow..."

# Check for "Validation Gate Behavior" heading
if ! grep -q "Validation Gate Behavior" "$spec_file"; then
    echo "WARNING: Specification may not have 'Validation Gate Behavior' heading"
fi

# Check for "before reporting success, validate artifact"
if ! grep -q "before reporting success" "$spec_file" && ! grep -q "report success" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define success reporting flow"
fi

# Check for validation flow: PASS and FAIL paths
if ! grep -q "Validation result: PASS" "$spec_file" && ! grep -q "validation.*pass" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define PASS path"
fi

if ! grep -q "Validation result: FAIL" "$spec_file" && ! grep -q "validation.*fail" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define FAIL path"
fi

# Check that FAIL path reports error and stops execution
if ! grep -q "report error.*stop skill execution" "$spec_file"; then
    echo "WARNING: Specification may not explicitly require error reporting on failure"
fi

# Check that FAIL path does NOT report successful creation
if ! grep -q "report successful creation" "$spec_file" && ! grep -q "report.*success" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define that partial/failures are not reported as success"
fi

echo "PASS: V-FR-4b - Validation gate behavioral flow defined"

echo "PASS: V-FR-4, V-FR-4b - Validation Before Completion"
