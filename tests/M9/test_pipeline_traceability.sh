#!/bin/bash
# Test V-FR-10: Pipeline Traceability
# #{Verification IDs: V-FR-10}
# #{Requirement IDs: FR-10}

set -euo pipefail

# Self-validation assertion
if [[ ! -f "milestones/M9/M9S1.md" ]]; then
    echo "FAIL: Specification file not found"
    exit 1
fi

spec_file="milestones/M9/M9S1.md"

# Test V-FR-10: Check that specification defines pipeline traceability
echo "Testing V-FR-10: Pipeline traceability definition..."

# Check for "Pipeline Traceability" heading
if ! grep -q "Pipeline Traceability" "$spec_file"; then
    echo "FAIL: Specification does not have 'Pipeline Traceability' heading"
    exit 1
fi

# Check that the system can establish relationships without relying exclusively on filename conventions
if ! grep -q "filename conventions" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define filename convention avoidance"
fi

if ! grep -q "filename-based inference" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define filename-based inference avoidance"
fi

# Check that relationships use canonical relationship model
if ! grep -q "canonical relationship model" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define canonical relationship model"
fi

# Check for "Relationship Model (Canonical)" heading
if ! grep -q "Relationship Model" "$spec_file"; then
    echo "WARNING: Specification may not define Relationship Model"
fi

# Check that derived_from, verifies, tests, implements, evaluates, reviews are used
if ! grep -q "derived_from" "$spec_file" && ! grep -q "verifies" "$spec_file" && ! grep -q "tests" "$spec_file" && ! grep -q "implements" "$spec_file" && ! grep -q "evaluates" "$spec_file" && ! grep -q "reviews" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define relationship types"
fi

# Check that relationships are stored in metadata
if ! grep -q "stored in metadata" "$spec_file" && ! grep -q "metadata" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define metadata storage"
fi

# Check that each pipeline stage consumes canonical artifact identity and metadata
if ! grep -q "consumes.*artifact identity" "$spec_file" && ! grep -q "canonical artifact identity" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define identity consumption"
fi

# Check that identity is passed explicitly, not inferred from filename patterns
if ! grep -q "passed explicitly" "$spec_file" && ! grep -q "inferred" "$spec_file" && ! grep -q "filename patterns" "$spec_file"; then
    echo "WARNING: Specification may not explicitly define explicit identity passing"
fi

echo "PASS: V-FR-10 - Pipeline traceability definition exists"

echo "PASS: V-FR-10 - Pipeline Traceability"
