# Deferred: Python Client Installation

## Issue

Specification M3S1 FR-2 requires "Add the Python client (uv add ladybug)" but the AEF repository is Node.js-based and does not have Python project configuration.

## Resolution

**Decision**: Defer Python client installation. The AEF framework will use lbug CLI directly for all graph operations, satisfying NFR-5 (Bash access as sole agent-facing surface).

**Rationale**:
- AEF is a Node.js-based framework with no Python runtime in the stack
- Using lbug CLI through bash is sufficient for all V1 requirements
- Avoids unnecessary Python dependency overhead
- Maintains single-runtime consistency (Node.js only)

**Impact**:
- graph-context skill SKILL.md documents parser behavior but does not implement actual Python parser
- Verification hook will use bash commands to lbug instead of Python client API
- All graph operations will be executed via lbug CLI

**Future Consideration**:
- Python client can be added later as an optional enhancement
- Requires Python 3.9+ and pip/uv configuration
- Not blocking for V1 milestone
