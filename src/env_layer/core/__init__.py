"""
Core environment layer components.

This package contains the core functionality for environment detection,
workspace management, and configuration handling.
"""

from .detector import EnvironmentDetector
from .workspace import WorkspaceManager
from .config import EnvironmentConfig

__all__ = [
    "EnvironmentDetector",
    "WorkspaceManager",
    "EnvironmentConfig",
]