#!/bin/bash

# Verification IDs: V-FR-1, V-FR-2, V-FR-3, V-FR-4, V-NFR-1
# Requirement IDs: FR-1, FR-2, FR-3, FR-4, NFR-1

# Test Type: SPECIFICATION_CHECK

set -euo pipefail

# --- Test Setup ---
SPEC_FILE="milestones/M7/M7S1.md"
VERIF_FILE="milestones/M7/M7S1V.md"

# Self-validity assertion: Check if specification and verification files exist
if [[ ! -f "$SPEC_FILE" ]]; then
    echo "VALIDITY FAILURE: Specification file not found: $SPEC_FILE"
    exit 2
fi
if [[ ! -f "$VERIF_FILE" ]]; then
    echo "VALIDITY FAILURE: Verification file not found: $VERIF_FILE"
    exit 2
fi

# -- Verifications --

# V-FR-1 / FR-1: Define canonical machine identifiers
# Checks for presence of examples of canonical identifiers in the specification.
echo "Checking for definition of canonical identifiers..."
grep -qF 'SPEC-001' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-1): Canonical identifier 'SPEC-001' not found in $SPEC_FILE" && exit 1)
grep -qF 'VER-001' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-1): Canonical identifier 'VER-001' not found in $SPEC_FILE" && exit 1)
grep -qF 'TEST-001' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-1): Canonical identifier 'TEST-001' not found in $SPEC_FILE" && exit 1)
grep -qF 'INV-001' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-1): Canonical identifier 'INV-001' not found in $SPEC_FILE" && exit 1)

# V-FR-2 / FR-2: Mandate YAML frontmatter
# Checks for explicit mention of YAML frontmatter requirement.
echo "Checking for mandate of YAML frontmatter..."
grep -q 'Mandate YAML frontmatter' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-2): Explicit mandate for YAML frontmatter not found in $SPEC_FILE" && exit 1)

# V-FR-3 / FR-3: Specify required YAML frontmatter fields
# Checks for explicit listing of required fields.
echo "Checking for required YAML frontmatter fields..."
grep -q 'id:' "$SPEC_FILE" || \
(echo "ASSERTION FAILURE (FR-3): Required field 'id' not found in $SPEC_FILE" && exit 1)
grep -q 'type:' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-3): Required field 'type' not found in $SPEC_FILE" && exit 1)
grep -q 'title:' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-3): Required field 'title' not found in $SPEC_FILE" && exit 1)
grep -q 'milestone_id:' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-3): Required field 'milestone_id' not found in $SPEC_FILE" && exit 1)
grep -q 'status:' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-3): Required field 'status' not found in $SPEC_FILE" && exit 1)
grep -q 'derived_from:' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-3): Required field 'derived_from' not found in $SPEC_FILE" && exit 1)

# V-FR-4 / FR-4: Prohibit semantic qualifiers in artifact IDs
# Checks for explicit prohibition of semantic qualifiers and requirement for sequential numerical IDs.
echo "Checking for prohibition of semantic qualifiers in artifact IDs..."
grep -q 'Prohibit semantic qualifiers in artifact IDs' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-4): Prohibition of semantic qualifiers not found in $SPEC_FILE" && exit 1)
grep -q 'sequential numerical identifiers' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (FR-4): Requirement for sequential numerical IDs not found in $SPEC_FILE" && exit 1)

# V-NFR-1 / NFR-1: Schema extensibility
# Checks for statement regarding schema extensibility.
echo "Checking for statement on schema extensibility..."
grep -q 'extensible to accommodate future artifact types' "$SPEC_FILE" || \
  (echo "ASSERTION FAILURE (NFR-1): Statement on schema extensibility not found in $SPEC_FILE" && exit 1)

# --- Post-Implementation Expectation ---
# For SPECIFICATION_CHECK tests, we expect PASS if the spec file exists and contains the required information.

echo "All specification checks passed."
exit 0
