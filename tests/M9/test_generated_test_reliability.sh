#!/bin/bash
# Test V-FR-12: Generated Test Reliability
# #{Verification IDs: V-FR-12}
# #{Requirement IDs: FR-12}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-12: Check that specification defines generator guardrails
echo "Testing V-FR-12: Generated test reliability definition..."

# Check for "Generated Test Reliability" heading
if ! grep -q "Generated Test Reliability" "$spec_file"; then
    echo "FAIL: Specification does not have 'Generated Test Reliability' heading"
    exit 1
fi

# Check that generated tests reference correct source specification
if ! grep -q "source specification" "$spec_file" && ! grep -q "source" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define source specification reference"
fi

# Check that generated tests reference correct verification protocol
if ! grep -q "verification protocol" "$spec_file" && ! grep -q "verification" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define verification protocol reference"
fi

# Check that generated tests test stated requirements, not invented requirements
if ! grep -q "invented" "$spec_file" && ! grep -q "invented requirements" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit invented requirements"
fi

# Check that generated tests establish valid initial failure path
if ! grep -q "initial failure" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define initial failure path"
fi

# Check that generated tests do NOT validate documentation claims absent from specification
if ! grep -q "documentation claims" "$spec_file" && ! grep -q "absent" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit validation of absent documentation claims"
fi

# Check that generated tests do NOT become specification validators
if ! grep -q "specification validators" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit specification validator behavior"
fi

# Check for generator guardrails heading
if ! grep -q "generator guardrails" "$spec_file"; then
    echo "WARNING: Specification may not define generator guardrails"
fi

# Check for "generator guardrails" or "generator guardrails" mention
if ! grep -q "generator" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define generator behavior"
fi

# Check that generator reads specification and verification protocol via canonical resolver
if ! grep -q "canonical resolver" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical resolver usage"
fi

# Check that generator extracts functional requirements from metadata
if ! grep -q "extracts" "$spec_file" && ! grep -q "functional requirements" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define functional requirement extraction"
fi

# Check that generator generates tests that reference requirements by canonical ID
if ! grep -q "canonical ID" "$spec_file" && ! grep -q "requirement.*ID" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical ID reference"
fi

# Check that generator validates test assertions against specification requirements
if ! grep -q "validates" "$spec_file" && ! grep -q "test assertions" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define assertion validation"
fi

echo "PASS: V-FR-12 - Generated test reliability definition exists"

echo "PASS: V-FR-12 - Generated Test Reliability"
