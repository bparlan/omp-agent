"""
Environment Configuration for the AEF Environment Layer.

This module implements configuration management as specified in FR-1.2
of the M11S1 specification.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
class EnvironmentConfig:
    """
    Configuration manager for environment settings.

    Manages .mise.toml configuration schema and validation.
    """

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.mise_config_path = self.project_path / ".mise.toml"
        self.config_cache = {}

    def load_mise_config(self) -> Dict[str, Any]:
        """
        Load and validate .mise.toml configuration.

        Returns:
            Dict containing parsed configuration.
        """
        if not self.mise_config_path.exists():
            return self._get_default_config()

        try:
            # Parse TOML configuration
            import tomli
            with open(self.mise_config_path, 'rb') as f:
                config = tomli.load(f)
            return self._validate_config(config)
        except (ImportError, json.JSONDecodeError):
            # Fallback to basic JSON parsing for compatibility
            try:
                with open(self.mise_config_path, 'r') as f:
                    config = json.load(f)
                return self._validate_config(config)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._get_default_config()

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration against schema.

        Args:
            config: Configuration dictionary to validate

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        return self._validate_config(config)

    def generate_mise_template(self, runtime: str, template_type: str = "basic") -> Dict[str, Any]:
        """
        Generate .mise.toml template for specified runtime.

        Args:
            runtime: Target runtime (python, node, rust, go, deno)
            template_type: Template type (basic, advanced, minimal)

        Returns:
            Dict containing template configuration
        """
        templates = {
            "python": {
                "environment": {
                    "runtime": "python",
                    "version": "3.11.0"
                },
                "tools": [
                    {"name": "python", "version": "3.11.0"},
                    {"name": "pip", "version": "22.0.0"}
                ]
            },
            "node": {
                "environment": {
                    "runtime": "node",
                    "version": "18.0.0"
                },
                "tools": [
                    {"name": "node", "version": "18.0.0"},
                    {"name": "npm", "version": "8.0.0"}
                ]
            },
            "rust": {
                "environment": {
                    "runtime": "rust",
                    "version": "1.70.0"
                },
                "tools": [
                    {"name": "rustc", "version": "1.70.0"},
                    {"name": "cargo", "version": "1.70.0"}
                ]
            },
            "go": {
                "environment": {
                    "runtime": "go",
                    "version": "1.20.0"
                },
                "tools": [
                    {"name": "go", "version": "1.20.0"}
                ]
            },
            "deno": {
                "environment": {
                    "runtime": "deno",
                    "version": "1.35.0"
                },
                "tools": [
                    {"name": "deno", "version": "1.35.0"}
                ]
            }
        }

        if runtime not in templates:
            raise ValueError(f"Unsupported runtime: {runtime}")

        template = templates[runtime].copy()

        if template_type == "advanced":
            template["workspace"] = {
                "isolation": True,
                "path": ".aef-env",
                "permissions": ["read", "write", "execute"]
            }
            template["cross_language"] = {
                "compatibility_mode": False,
                "fallback_strategies": ["tool_fallback", "system_default"],
                "shared_components": []
            }

        elif template_type == "minimal":
            template = {
                "environment": template["environment"],
                "tools": template["tools"][:1]  # Only the main runtime
            }

        return template

    def merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.

        Args:
            base_config: Base configuration
            override_config: Override configuration

        Returns:
            Merged configuration dictionary
        """
        import copy

        merged = copy.deepcopy(base_config)

        def deep_merge(target: Dict[str, Any], source: Dict[str, Any]):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    deep_merge(target[key], value)
                else:
                    target[key] = value

        deep_merge(merged, override_config)
        return merged

    def save_mise_config(self, config: Dict[str, Any], output_path: Optional[Path] = None) -> None:
        """
        Save configuration to .mise.toml file.

        Args:
            config: Configuration to save
            output_path: Output file path (defaults to .mise.toml in project)
        """
        if output_path is None:
            output_path = self.mise_config_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            import tomli_w
            with open(output_path, 'wb') as f:
                tomli_w.dump(config, f)
        except ImportError:
            # Fallback to JSON if tomli_w is not available
            with open(output_path.with_suffix('.json'), 'w') as f:
                json.dump(config, f, indent=2)

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration and fix common issues."""
        # Basic validation
        if not isinstance(config, dict):
            return self._get_default_config()

        # Ensure required structure exists
        validated_config = {
            "environment": {
                "runtime": config.get("environment", {}).get("runtime", "python"),
                "version": config.get("environment", {}).get("version", "3.11.0")
            },
            "tools": config.get("tools", []),
            "workspace": config.get("workspace", {}),
            "cross_language": config.get("cross_language", {})
        }

        return validated_config

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "environment": {
                "runtime": "python",
                "version": "3.11.0"
            },
            "tools": [
                {"name": "python", "version": "3.11.0"}
            ],
            "workspace": {},
            "cross_language": {}
        }