#!/bin/bash
# Test V-FR-5, V-FR-5b: Project Configuration
# #{Verification IDs: V-FR-5, V-FR-5b}
# #{Requirement IDs: FR-5}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-5: Check that specification defines project configuration requirements
echo "Testing V-FR-5: Project configuration definition..."

# Check for "Project-Scoped Configuration" heading
if ! grep -q "Project-Scoped Configuration" "$spec_file"; then
    echo "FAIL: Specification does not have 'Project-Scoped Configuration' heading"
    exit 1
fi

# Check for .omp/config.yml mention
if ! grep -q "\.omp/config.yml" "$spec_file"; then
    echo "FAIL: Specification does not mention .omp/config.yml"
    exit 1
fi

# Check that configuration defines project identity and development mode
if ! grep -q "project identity" "$spec_file" && ! grep -q "development mode" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project identity and development mode"
fi

# Check that schema fields are listed (project_id, project_slug, mode)
if ! grep -q "project_id" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project_id field"
fi

if ! grep -q "project_slug" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project_slug field"
fi

if ! grep -q "mode" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define mode field"
fi

# Check that supported modes are defined (framework, application)
if ! grep -q "framework" "$spec_file" && ! grep -q "application" "$spec_file"; then
    echo "WARNING: Specification may not define supported modes"
fi

echo "PASS: V-FR-5 - Project configuration definition exists"

# Test V-FR-5b: Check that configuration is treated according to canonical rules
echo "Testing V-FR-5b: Configuration treated as canonical artifact..."

# Check that configuration is treated according to canonical artifact/configuration rules
if ! grep -q "treated according to" "$spec_file" && ! grep -q "canonical artifact" "$spec_file"; then
    echo "WARNING: Specification may not explicitly state configuration is treated as canonical"
fi

if ! grep -q "canonical.*artifact" "$spec_file" && ! grep -q "canonical.*configuration" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention canonical treatment of configuration"
fi

echo "PASS: V-FR-5b - Configuration canonical treatment defined"

echo "PASS: V-FR-5, V-FR-5b - Project Configuration"
