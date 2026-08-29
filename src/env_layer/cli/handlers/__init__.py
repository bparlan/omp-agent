"""
CLI command handlers for the Environment Layer.

This package contains the individual handlers for each CLI command,
implementing the observable contracts specified in the M11S1 specification.
"""

from .env_management import (
    handle_env_check,
    handle_env_setup,
    handle_env_list,
    handle_env_diagnose,
)
from .mise_config import (
    handle_mise_validate,
    handle_mise_generate,
    handle_mise_merge,
)
from .environment_detection import (
    handle_env_detect,
    handle_env_status,
    handle_env_refresh,
)
from .workspace_isolation import (
    handle_workspace_create,
    handle_workspace_activate,
    handle_workspace_execute,
    handle_workspace_status,
    handle_workspace_clean,
)
from .cross_language_runtime import (
    handle_runtime_switch,
    handle_runtime_exec,
    handle_runtime_list,
    handle_runtime_validate,
    handle_runtime_install,
)
from .validation import (
    handle_validate_schema,
    handle_validate_fixtures,
)

__all__ = [
    # Environment Management
    "handle_env_check",
    "handle_env_setup",
    "handle_env_list",
    "handle_env_diagnose",
    # Mise Configuration
    "handle_mise_validate",
    "handle_mise_generate",
    "handle_mise_merge",
    # Environment Detection
    "handle_env_detect",
    "handle_env_status",
    "handle_env_refresh",
    # Workspace Isolation
    "handle_workspace_create",
    "handle_workspace_activate",
    "handle_workspace_execute",
    "handle_workspace_status",
    "handle_workspace_clean",
    # Cross-Language Runtime
    "handle_runtime_switch",
    "handle_runtime_exec",
    "handle_runtime_list",
    "handle_runtime_validate",
    "handle_runtime_install",
    # Validation
    "handle_validate_schema",
    "handle_validate_fixtures",
]