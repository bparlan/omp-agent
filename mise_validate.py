#!/usr/bin/env python3
"""mise-validate command for FR-1.2 .mise.toml Configuration Schema validation"""
import sys
import json
import argparse
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List

def validate_version_format(version: str) -> bool:
    """Validate version format using the regex from specification"""
    pattern = r'^([0-9]+)\.([0-9]+)\.([0-9]+)([-+][a-zA-Z0-9]+)?$'
    return re.match(pattern, version) is not None

def validate_inner_config(config: Dict[str, Any]) -> List[str]:
    """Validate a config object that is missing the outer wrapper (schema_version, mise_config)"""
    errors = []

    # Validate environment (required in inner config)
    if "environment" not in config:
        errors.append("Missing required field: environment")
    else:
        env = config["environment"]
        # Validate runtime (required)
        if "runtime" not in env:
            errors.append("Missing required field: environment.runtime")
        elif env["runtime"] not in ["python", "node", "rust", "go", "deno", "common"]:
            errors.append(f"Invalid runtime: {env['runtime']}")
        # Validate version (required with specific format)
        if "version" not in env:
            errors.append("Missing required field: environment.version")
        elif not validate_version_format(env["version"]):
            errors.append(f"Invalid version format: {env['version']}")

    # Validate tools (optional but if present, must have name and version)
    if "tools" in config:
        tools = config["tools"]
        if not isinstance(tools, list):
            errors.append("tools must be an array")
        else:
            for i, tool in enumerate(tools):
                if not isinstance(tool, dict):
                    errors.append(f"tools[{i}] must be an object")
                else:
                    if "name" not in tool:
                        errors.append(f"tools[{i}] missing required field: name")
                    if "version" not in tool:
                        errors.append(f"tools[{i}] missing required field: version")

    # Validate workspace (optional)
    if "workspace" in config:
        workspace = config["workspace"]
        if not isinstance(workspace, dict):
            errors.append("workspace must be an object")
        else:
            if "isolation" in workspace and not isinstance(workspace["isolation"], bool):
                errors.append("workspace.isolation must be a boolean")
            if "path" in workspace and not isinstance(workspace["path"], str):
                errors.append("workspace.path must be a string")
            if "permissions" in workspace:
                if not isinstance(workspace["permissions"], list):
                    errors.append("workspace.permissions must be an array")
                else:
                    for i, perm in enumerate(workspace["permissions"]):
                        if not isinstance(perm, str):
                            errors.append(f"workspace.permissions[{i}] must be a string")

    # Validate cross_language (optional)
    if "cross_language" in config:
        cross_lang = config["cross_language"]
        if not isinstance(cross_lang, dict):
            errors.append("cross_language must be an object")
        else:
            if "compatibility_mode" in cross_lang and not isinstance(cross_lang["compatibility_mode"], bool):
                errors.append("cross_language.compatibility_mode must be a boolean")
            if "fallback_strategies" in cross_lang:
                if not isinstance(cross_lang["fallback_strategies"], list):
                    errors.append("cross_language.fallback_strategies must be an array")
                else:
                    for i, strat in enumerate(cross_lang["fallback_strategies"]):
                        if not isinstance(strat, str):
                            errors.append(f"cross_language.fallback_strategies[{i}] must be a string")
            if "shared_components" in cross_lang:
                if not isinstance(cross_lang["shared_components"], list):
                    errors.append("cross_language.shared_components must be an array")
                else:
                    for i, comp in enumerate(cross_lang["shared_components"]):
                        if not isinstance(comp, str):
                            errors.append(f"cross_language.shared_components[{i}] must be a string")

    return errors

def validate_mise_config(config: Dict[str, Any]) -> List[str]:
    """Validate a complete mise config with schema_version wrapper"""
    errors = []

    # Validate that config has schema_version field
    if "schema_version" not in config:
        errors.append("Missing required field: schema_version")
    else:
        schema_version = config["schema_version"]
        if not isinstance(schema_version, str):
            errors.append("schema_version must be a string")

    # Validate that config has mise_config field
    if "mise_config" not in config:
        errors.append("Missing required field: mise_config")
    else:
        mise_config = config["mise_config"]
        if not isinstance(mise_config, dict):
            errors.append("mise_config must be an object")

    # Validate inner structure of mise_config if present
    if "mise_config" in config and isinstance(config["mise_config"], dict):
        inner_errors = validate_inner_config(config["mise_config"])
        errors.extend(inner_errors)

    return errors

def main():
    parser = argparse.ArgumentParser(
        description="Validate .mise.toml configuration against schema"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to config file"
    )
    parser.add_argument(
        "--schema",
        default="1.0.0",
        help="Schema version"
    )

    args = parser.parse_args()

    try:
        # Load config file
        config_path_obj = Path(args.config)
        if not config_path_obj.exists():
            print(f"Error: Configuration file not found: {args.config}")
            sys.exit(1)

        # Try to parse as YAML first (mise uses YAML-like format)
        try:
            with open(config_path_obj, 'r') as f:
                content = f.read()
            config = yaml.safe_load(content)
            if config is None:
                raise ValueError("Empty configuration file")
        except yaml.YAMLError:
            # Fall back to JSON
            with open(config_path_obj, 'r') as f:
                config = json.load(f)

        # Validate the loaded config
        errors = validate_mise_config(config)

        if errors:
            print("Validation failed with the following errors:")
            for error in errors:
                print(f"  - {error}")
            print(f"\nConfig file: {args.config}")
            print(f"Schema version: {args.schema}")
            print(f"Status: INVALID")
            sys.exit(1)
        else:
            print("Configuration validated successfully")
            print(f"Config file: {args.config}")
            print(f"Schema version: {args.schema}")
            print(f"Status: VALID")
            sys.exit(0)

    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Config file: {args.config}")
        print(f"Schema version: {args.schema}")
        print(f"Status: ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
