#!/bin/bash
# Test V-FR-7: Application-Specific Agent Guidance
# #{Verification IDs: V-FR-7}
# #{Requirement IDs: FR-7}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-7: Check that specification defines parameterized guidance model
echo "Testing V-FR-7: Application-specific agent guidance definition..."

# Check for "Application-Specific Agent Guidance" heading
if ! grep -q "Application-Specific Agent Guidance" "$spec_file"; then
    echo "FAIL: Specification does not have 'Application-Specific Agent Guidance' heading"
    exit 1
fi

# Check that bootstrap generates or installs project-local agent guidance
if ! grep -q "project-local agent guidance" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project-local agent guidance"
fi

# Check that technology-specific rules are parameterized
if ! grep -q "parameterized" "$spec_file"; then
    echo "FAIL: Specification does not explicitly mention parameterized guidance"
    exit 1
fi

# Check that parameterized approach is mentioned
if ! grep -q "parameterized approach" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define parameterized approach"
fi

# Check that bootstrap architecture supports Project Mode + Project Technology/Stack
if ! grep -q "Project Mode" "$spec_file" && ! grep -q "Project Technology" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define technology stack support"
fi

# Check that system does NOT assume single technology stack
if ! grep -q "does NOT assume" "$spec_file" && ! grep -q "not assume" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit single technology stack assumption"
fi

# Check for parameterized guidance model heading
if ! grep -q "Parameterized Guidance Model" "$spec_file"; then
    echo "WARNING: Specification may not define Parameterized Guidance Model"
fi

# Check for example guidance in parameter library
if ! grep -q "parameter library" "$spec_file"; then
    echo "WARNING: Specification may not mention parameter library"
fi

echo "PASS: V-FR-7 - Application-specific agent guidance defined"

echo "PASS: V-FR-7 - Application-Specific Agent Guidance"
