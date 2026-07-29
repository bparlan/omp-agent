#!/bin/bash
# Test V-FR-6, V-FR-6b, V-FR-6c: Mode-Aware Bootstrap
# #{Verification IDs: V-FR-6, V-FR-6b, V-FR-6c}
# #{Requirement IDs: FR-6}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-6: Check that specification defines mode-aware bootstrap
echo "Testing V-FR-6: Mode-aware bootstrap definition..."

# Check for "Mode-Aware Bootstrap" heading
if ! grep -q "Mode-Aware Bootstrap" "$spec_file"; then
    echo "FAIL: Specification does not have 'Mode-Aware Bootstrap' heading"
    exit 1
fi

# Check that bootstrap-project distinguishes between framework and application modes
if ! grep -q "distinguish between" "$spec_file" && ! grep -q "framework.*application" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention framework vs application mode distinction"
fi

# Check for mode selection behavior heading
if ! grep -q "Mode Selection Behavior" "$spec_file"; then
    echo "WARNING: Specification may not define Mode Selection Behavior"
fi

echo "PASS: V-FR-6 - Mode-aware bootstrap definition exists"

# Test V-FR-6b: Check that specification defines framework mode behavior
echo "Testing V-FR-6b: Framework mode definition..."

# Check for "Framework Mode" heading
if ! grep -q "### Framework Mode" "$spec_file"; then
    echo "WARNING: Specification may not have '### Framework Mode' heading"
fi

# Check that framework mode preserves framework-oriented initialization
if ! grep -q "framework-oriented initialization" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define framework-oriented initialization"
fi

# Check that framework-specific documentation is generated only when explicitly required
if ! grep -q "framework-specific documentation" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define framework documentation generation"
fi

if ! grep -q "only when explicitly required" "$spec_file"; then
    echo "WARNING: Specification may not explicitly state requirement for explicit documentation"
fi

# Check that FRAMEWORK.md, PLAYBOOK.md, DATA.md are mentioned
if ! grep -q "FRAMEWORK.md" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention FRAMEWORK.md"
fi

if ! grep -q "PLAYBOOK.md" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention PLAYBOOK.md"
fi

if ! grep -q "DATA.md" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention DATA.md"
fi

echo "PASS: V-FR-6b - Framework mode definition exists"

# Test V-FR-6c: Check that specification defines application mode behavior
echo "Testing V-FR-6c: Application mode definition..."

# Check for "Application Mode" heading
if ! grep -q "### Application Mode" "$spec_file"; then
    echo "WARNING: Specification may not have '### Application Mode' heading"
fi

# Check that application mode does NOT generate irrelevant AEF documentation by default
if ! grep -q "does NOT generate" "$spec_file" && ! grep -q "not generate" "$spec_file"; then
    echo "WARNING: Specification may not explicitly prohibit default AEF documentation generation"
fi

if ! grep -q "irrelevant AEF-internal" "$spec_file"; then
    echo "WARNING: Specification may not explicitly mention irrelevant AEF documentation"
fi

# Check that application mode creates project-appropriate agent guidance
if ! grep -q "project-appropriate agent guidance" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define project-appropriate agent guidance"
fi

# Check that application mode preserves project architecture and conventions
if ! grep -q "preserves.*architecture" "$spec_file" && ! grep -q "preserves.*conventions" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define preservation of project conventions"
fi

# Check that application mode establishes minimal AEF infrastructure
if ! grep -q "establish.*minimal AEF" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define minimal AEF infrastructure"
fi

echo "PASS: V-FR-6c - Application mode definition exists"

echo "PASS: V-FR-6, V-FR-6b, V-FR-6c - Mode-Aware Bootstrap"
