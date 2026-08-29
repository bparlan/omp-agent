"""
Environment / Reproducibility Layer for AEF 6-layer substrate architecture.

Provides language-agnostic environment management for deterministic runtime
environments and workspace isolation across Python, Node.js, Rust, Go, and Deno.
"""

from .cli.main import main
from env_layer.core.detector import EnvironmentDetector
from env_layer.core.workspace import WorkspaceManager
from env_layer.core.config import EnvironmentConfig
from .validation.schema_validator import SchemaValidator

__all__ = [
    "main",
    "EnvironmentDetector",
    "WorkspaceManager",
    "EnvironmentConfig",
    "SchemaValidator",
]