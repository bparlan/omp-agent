#!/bin/bash

# Self-validity check: Ensure necessary documentation artifacts exist and have content.
# M10 focuses on standards in documentation and templates, not executables.

# Check for M10 Specification (M10S1.md) and Test Template.
if [ ! -f "milestones/M10/M10S1.md" ]; then
    echo "VALIDITY FAILURE: test did not exercise intended subject"
    echo "Subject: M10 Specification (milestones/M10/M10S1.md)"
    echo "Reason: M10 Specification file not found."
    exit 2
fi
if [ ! -s "milestones/M10/M10S1.md" ]; then
    echo "VALIDITY FAILURE: test did not exercise intended subject"
    echo "Subject: M10 Specification (milestones/M10/M10S1.md)"
    echo "Reason: M10 Specification file is empty."
    exit 2
fi

# The test template is referenced in the generate-tests skill instructions.
# Use the path provided by the user, expanding HOME variable.
TEST_TEMPLATE_PATH="$HOME/devcode/aef/agent/templates/test_template.md"
if [ ! -f "$TEST_TEMPLATE_PATH" ]; then
    echo "VALIDITY FAILURE: test did not exercise intended subject"
    echo "Subject: Test Template ($TEST_TEMPLATE_PATH)"
    echo "Reason: Test template file not found."
    exit 2
fi
if [ ! -s "$TEST_TEMPLATE_PATH" ]; then
    echo "VALIDITY FAILURE: test did not exercise intended subject"
    echo "Subject: Test Template ($TEST_TEMPLATE_PATH)"
    echo "Reason: Test template file is empty."
    exit 2
fi

# Check for standard unix tools required for assertions.
command -v grep >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'grep' command not found."; exit 2; }
command -v bash >/dev/null 2>&1 || { echo "VALIDITY FAILURE: 'bash' command not found."; exit 2; }

echo "Running Artifact Type Identifiers Test..."

# --- Assertions based on M10S1.md content ---
# These assertions check if the M10 Specification document itself reflects the requirements.
# Expected failures here indicate missing or poorly defined requirements in the spec.

found_assertion_failures=false

# FV-2: Support for minimum set of artifact types (conceptual)
# Check if M10S1.md lists specific artifact types.
if ! grep -qE '(milestone|specification|verification|test_set|investigation|evaluation|review|audit|completion_report)' milestones/M10/M10S1.md;
then
    echo "FAIL: FV-2 - M10S1.md does not clearly define minimum artifact types."
    found_assertion_failures=true
else
    echo "PASS: FV-2 - M10S1.md conceptually defines minimum artifact types."
fi

# FV-1 & FV-3: Recommended identifier forms and prohibition of semantic qualifiers
# Check for definition of forms like 'M{N}', 'SPEC-{N}' and prohibition of qualifiers.
if ! grep -qE 'recommended forms' milestones/M10/M10S1.md || ! grep -qE 'prohibit semantic qualifiers' milestones/M10/M10S1.md;
then
    echo "FAIL: FV-1/FV-3 - M10S1.md does not clearly define identifier forms or prohibit qualifiers."
    found_assertion_failures=true
else
    echo "PASS: FV-1/FV-3 - M10S1.md conceptually defines identifier forms and prohibits qualifiers."
fi

# FV-6: Metadata distinguishes identity, type, lineage, status, revision
# Check if M10S1.md clarifies how these concepts are distinctly represented.
if ! grep -qE 'distinguishes identity, type, lineage, status, and revision' milestones/M10/M10S1.md;
then
    echo "FAIL: FV-6 - M10S1.md does not clarify distinct representation of metadata concepts."
    found_assertion_failures=true
else
    echo "PASS: FV-6 - M10S1.md conceptually addresses distinct representation of metadata concepts."
fi

# NFR-2 (Security), EC-1, EC-3, EC-4, FS-1, FS-2, FS-4: Metadata constraints and edge cases
# Check if M10S1.md addresses sensitive data, missing mandatory fields, ambiguous distinctions, filename conflicts, etc.
if ! grep -qE 'metadata constraints' milestones/M10/M10S1.md || ! grep -qE 'edge cases' milestones/M10/M10S1.md;
then
    echo "FAIL: NFR-2/EC/FS - M10S1.md does not clearly address metadata constraints and edge cases."
    found_assertion_failures=true
else
    echo "PASS: NFR-2/EC/FS - M10S1.md conceptually addresses metadata constraints and edge cases."
fi

# Check for requirement of YAML frontmatter (derived from M10S2V.md and test_metadata_validation.sh)
# This checks if the spec mentions YAML frontmatter.
if ! grep -qE 'YAML frontmatter' milestones/M10/M10S1.md;
then
    echo "FAIL: M10S1.md does not specify YAML frontmatter requirements."
    found_assertion_failures=true
else
    echo "PASS: M10S1.md specifies YAML frontmatter requirements."
fi

# --- Final Test Result ---
# The test should fail if M10's conceptual requirements are not met in the spec.
if [ "$found_assertion_failures" = true ]; then
    exit 1 # FAIL - missing M10 behavior in spec
else
    echo "All assertions passed. M10 conceptual requirements seem to be reflected in the spec."
    exit 0 # PASS - for test execution, indicating spec is present and assertions checked.
fi
