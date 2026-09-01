#!/usr/bin/env python3
"""
Project Configuration Module - FR-PROJECT_CONFIG_INTEGRATION

Handles reading, writing, and validating project configuration stored in .omp/config.yml.
Implements contracts: load_project_config(), validate_config(config)
"""

import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from jsonschema import validate, ValidationError

# JSON schema for project configuration
CONFIG_SCHEMA = {
    "type": "object",
    "required": ["project_id", "project_slug", "mode"],
    "properties": {
        "project_id": {"type": "string", "pattern": "^[a-zA-Z0-9-]+$"},
        "project_slug": {"type": "string", "pattern": "^[a-z0-9-]+$"},
        "mode": {"type": "string", "enum": ["framework", "application"]},
        "artifact_registry_path": {"type": "string"},
        "legacy_boundaries": {"type": "array", "items": {"type": "string"}},
    },
}


def _find_project_root() -> Path:
    """Locate project root by finding .omp/config.yml or .git directory."""
    current = Path.cwd()
    while True:
        # Check for .omp/config.yml
        config_path = current / ".omp" / "config.yml"
        if config_path.exists():
            return current

        # Check for .git directory
        if (current / ".git").exists():
            return current

        # Move up one level
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    raise FileNotFoundError(
        "Could not find project root (no .omp/config.yml or .git directory)"
    )


def load_project_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and validate project configuration.

    Returns:
        Dict containing project configuration

    Raises:
        FileNotFoundError: If config file not found
        ValidationError: If config invalid
    """
    if config_path:
        config_file = Path(config_path)
    else:
        project_root = _find_project_root()
        config_file = project_root / ".omp" / "config.yml"

    if not config_file.exists():
        raise FileNotFoundError(f"Project configuration file not found: {config_file}")

    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValidationError(f"Invalid configuration format in {config_file}")

    validation_errors = validate_config(config)
    if not validation_errors:
        raise ValidationError(f"Configuration validation failed: {validation_errors}")

    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration against JSON schema.

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
        return True
    except ValidationError as e:
        print(f"Configuration validation error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected validation error: {e}")
        return False


def save_project_config(
    config: Dict[str, Any], config_path: Optional[str] = None
) -> None:
    """
    Save project configuration to file.

    Args:
        config: Configuration dictionary to save
        config_path: Optional path to save config (defaults to .omp/config.yml)
    """
    if config_path:
        config_file = Path(config_path)
    else:
        project_root = _find_project_root()
        config_file = project_root / ".omp" / "config.yml"

    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def create_default_config(
    project_id: str, project_slug: str, mode: str
) -> Dict[str, Any]:
    """
    Create a default project configuration.

    Args:
        project_id: Unique project identifier
        project_slug: Project slug (used in URLs)
        mode: Framework or application mode

    Returns:
        Default configuration dictionary
    """
    return {
        "project_id": project_id,
        "project_slug": project_slug,
        "mode": mode,
        "artifact_registry_path": "artifacts/registry.json",
        "legacy_boundaries": ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9"],
    }
