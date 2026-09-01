#!/bin/env bash
# {Verification IDs: VI-M12S3-5}
# {Requirement IDs: FR-END_TO_END_CIRCULATION_VALIDATION}
# Test Type: IMPLEMENTATION_CHECK

# The script directly invokes the circulation validation command.
# This follows the Direct Execution Rule - no explicit interpreter prefix.

CIRCULATION_SCRIPT="~/devcode/aef/agent/bin/validate-circulation.sh"

# Execute circulation validation using direct path invocation
# This allows natural shell resolution of the script's shebang line

"$CIRCULATION_SCRIPT"
