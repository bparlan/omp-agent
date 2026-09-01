"""
Mise CLI implementation for mise-validate, mise-generate, and mise-merge commands
"""

import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, Any, List


def validate_inner_config(config: Dict[str, Any]) -> List[str]:
    """Validate a config object that is missing the outer wrapper (schema_version, mise_config)"""
    errors = []

    # Validate environment (required in inner config)
    if "environment" not in config:
        errors.append("Missing required field: environment")
    else:
        env = config["environment"]

        if "runtime" not in env:
            errors.append("Missing required field: environment.runtime")
        else:
            runtime = env["runtime"]
            if runtime not in ["python", "node", "rust", "go", "deno", "common"]:
                errors.append(f"Invalid runtime value: {runtime}")

        if "version" not in env:
            errors.append("Missing required field: environment.version")
        else:
            version = env["version"]
            # Check version pattern - use proper regex
            version_pattern = r"^([0-9]+)\.([0-9]+)\.([0-9]+)([-+][a-zA-Z0-9]+)?$"
            if not re.match(version_pattern, version):
                errors.append(f"Invalid version format: {version}")

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
            if "isolation" in workspace and not isinstance(
                workspace["isolation"], bool
            ):
                errors.append("workspace.isolation must be a boolean")
            if "path" in workspace and not isinstance(workspace["path"], str):
                errors.append("workspace.path must be a string")
            if "permissions" in workspace:
                permissions = workspace["permissions"]
                if not isinstance(permissions, list):
                    errors.append("workspace.permissions must be an array")
                else:
                    for i, perm in enumerate(permissions):
                        if not isinstance(perm, str):
                            errors.append(
                                f"workspace.permissions[{i}] must be a string"
                            )

    # Validate cross_language (optional)
    if "cross_language" in config:
        cross_lang = config["cross_language"]
        if not isinstance(cross_lang, dict):
            errors.append("cross_language must be an object")
        else:
            if "compatibility_mode" in cross_lang and not isinstance(
                cross_lang["compatibility_mode"], bool
            ):
                errors.append("cross_language.compatibility_mode must be a boolean")
            if "fallback_strategies" in cross_lang:
                strategies = cross_lang["fallback_strategies"]
                if not isinstance(strategies, list):
                    errors.append("cross_language.fallback_strategies must be an array")
                else:
                    for i, strategy in enumerate(strategies):
                        if not isinstance(strategy, str):
                            errors.append(
                                f"cross_language.fallback_strategies[{i}] must be a string"
                            )
            if "shared_components" in cross_lang:
                components = cross_lang["shared_components"]
                if not isinstance(components, list):
                    errors.append("cross_language.shared_components must be an array")
                else:
                    for i, component in enumerate(components):
                        if not isinstance(component, str):
                            errors.append(
                                f"cross_language.shared_components[{i}] must be a string"
                            )

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
        elif schema_version != "1.0.0":
            errors.append(f"Invalid schema_version: {schema_version}")

    # Validate that config has mise_config field
    if "mise_config" not in config:
        errors.append("Missing required field: mise_config")
    else:
        mise_config = config["mise_config"]

        if not isinstance(mise_config, dict):
            errors.append("mise_config must be an object")
        else:
            # Validate environment
            if "environment" not in mise_config:
                errors.append("Missing required field: mise_config.environment")
            else:
                env = mise_config["environment"]
                if not isinstance(env, dict):
                    errors.append("mise_config.environment must be an object")
                else:
                    if "runtime" not in env:
                        errors.append(
                            "Missing required field: mise_config.environment.runtime"
                        )
                    else:
                        runtime = env["runtime"]
                        if runtime not in [
                            "python",
                            "node",
                            "rust",
                            "go",
                            "deno",
                            "common",
                        ]:
                            errors.append(f"Invalid runtime value: {runtime}")

                    if "version" not in env:
                        errors.append(
                            "Missing required field: mise_config.environment.version"
                        )
                    else:
                        version = env["version"]
                        version_pattern = (
                            r"^([0-9]+)\.([0-9]+)\.([0-9]+)([-+][a-zA-Z0-9]+)?$"
                        )
                        if not re.match(version_pattern, version):
                            errors.append(f"Invalid version format: {version}")

            # Validate tools
            if "tools" in mise_config:
                tools = mise_config["tools"]
                if not isinstance(tools, list):
                    errors.append("mise_config.tools must be an array")
                else:
                    for i, tool in enumerate(tools):
                        if not isinstance(tool, dict):
                            errors.append(f"mise_config.tools[{i}] must be an object")
                        else:
                            if "name" not in tool:
                                errors.append(
                                    f"mise_config.tools[{i}] missing required field: name"
                                )
                            if "version" not in tool:
                                errors.append(
                                    f"mise_config.tools[{i}] missing required field: version"
                                )

            # Validate workspace
            if "workspace" in mise_config:
                workspace = mise_config["workspace"]
                if not isinstance(workspace, dict):
                    errors.append("mise_config.workspace must be an object")
                else:
                    if "isolation" in workspace and not isinstance(
                        workspace["isolation"], bool
                    ):
                        errors.append(
                            "mise_config.workspace.isolation must be a boolean"
                        )
                    if "path" in workspace and not isinstance(workspace["path"], str):
                        errors.append("mise_config.workspace.path must be a string")
                    if "permissions" in workspace:
                        permissions = workspace["permissions"]
                        if not isinstance(permissions, list):
                            errors.append(
                                "mise_config.workspace.permissions must be an array"
                            )
                        else:
                            for i, perm in enumerate(permissions):
                                if not isinstance(perm, str):
                                    errors.append(
                                        f"mise_config.workspace.permissions[{i}] must be a string"
                                    )

            # Validate cross_language
            if "cross_language" in mise_config:
                cross_lang = mise_config["cross_language"]
                if not isinstance(cross_lang, dict):
                    errors.append("mise_config.cross_language must be an object")
                else:
                    if "compatibility_mode" in cross_lang and not isinstance(
                        cross_lang["compatibility_mode"], bool
                    ):
                        errors.append(
                            "mise_config.cross_language.compatibility_mode must be a boolean"
                        )
                    if "fallback_strategies" in cross_lang:
                        strategies = cross_lang["fallback_strategies"]
                        if not isinstance(strategies, list):
                            errors.append(
                                "mise_config.cross_language.fallback_strategies must be an array"
                            )
                        else:
                            for i, strategy in enumerate(strategies):
                                if not isinstance(strategy, str):
                                    errors.append(
                                        f"mise_config.cross_language.fallback_strategies[{i}] must be a string"
                                    )
                    if "shared_components" in cross_lang:
                        components = cross_lang["shared_components"]
                        if not isinstance(components, list):
                            errors.append(
                                "mise_config.cross_language.shared_components must be an array"
                            )
                        else:
                            for i, component in enumerate(components):
                                if not isinstance(component, str):
                                    errors.append(
                                        f"mise_config.cross_language.shared_components[{i}] must be a string"
                                    )

    # If we have all the required fields from mise_config, validate the inner structure
    if "mise_config" in config and not errors:
        mise_config = config["mise_config"]
        inner_errors = validate_inner_config(mise_config)
        errors.extend(inner_errors)

    return errors


class MiseValidator:
    """Implements Mise configuration validation functionality"""

    def __init__(self):
        self.evidence_log = []

    def validate_config(
        self, config_path: str, schema_version: str = "1.0.0"
    ) -> Dict[str, Any]:
        """Validate a .mise.toml configuration file"""
        try:
            # Load config file
            config_path_obj = Path(config_path)
            if not config_path_obj.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")

            # Try to parse as YAML first (mise uses YAML-like format)
            try:
                with open(config_path_obj, "r") as f:
                    content = f.read()
                    # Try to parse as YAML
                    import yaml

                    config = yaml.safe_load(content)
                    if config is None:
                        raise ValueError("Empty configuration file")
            except yaml.YAMLError:
                # Try to parse as JSON (mise config is also JSON-like)
                with open(config_path_obj, "r") as f:
                    config = json.load(f)

            # Validate the loaded config
            errors = validate_mise_config(config)

            if errors:
                return {
                    "status": "error",
                    "message": f"Validation failed: {'; '.join(errors)}",
                    "config_path": config_path,
                    "schema_version": schema_version,
                    "errors": errors,
                }
            else:
                return {
                    "status": "success",
                    "message": "Configuration validated successfully",
                    "config_path": config_path,
                    "schema_version": schema_version,
                    "errors": [],
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Validation failed: {str(e)}",
                "config_path": config_path,
                "schema_version": schema_version,
            }

    def generate_template(
        self, runtime: str, output_path: str, template_type: str = "default"
    ) -> Dict[str, Any]:
        """Generate a .mise.toml template for a specific runtime"""
        try:
            # Create a basic template based on runtime
            template = {
                "schema_version": "1.0.0",
                "mise_config": {
                    "environment": {"runtime": runtime, "version": "1.0.0"},
                    "tools": [],
                },
            }

            # Add runtime-specific tools
            if runtime == "python":
                template["mise_config"]["tools"].extend(
                    [
                        {"name": "python", "version": "3.11.0"},
                        {"name": "pip", "version": "22.0.0"},
                    ]
                )
            elif runtime == "node":
                template["mise_config"]["tools"].extend(
                    [
                        {"name": "node", "version": "18.0.0"},
                        {"name": "npm", "version": "8.0.0"},
                    ]
                )
            elif runtime == "rust":
                template["mise_config"]["tools"].extend(
                    [
                        {"name": "rustc", "version": "1.70.0"},
                        {"name": "cargo", "version": "1.70.0"},
                    ]
                )
            elif runtime == "go":
                template["mise_config"]["tools"].extend(
                    [{"name": "go", "version": "1.20.0"}]
                )
            elif runtime == "deno":
                template["mise_config"]["tools"].extend(
                    [{"name": "deno", "version": "1.35.0"}]
                )

            # Write template to output file
            with open(output_path, "w") as f:
                json.dump(template, f, indent=2)

            return {
                "status": "success",
                "message": f"Template generated for {runtime}",
                "runtime": runtime,
                "output_path": output_path,
                "template_type": template_type,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Template generation failed: {str(e)}",
                "runtime": runtime,
                "output_path": output_path,
                "template_type": template_type,
            }

    def merge_configs(
        self, base_path: str, override_path: str, output_path: str
    ) -> Dict[str, Any]:
        """Merge two configuration files"""
        try:
            # Load base config
            base_path_obj = Path(base_path)
            with open(base_path_obj, "r") as f:
                base_config = json.load(f)

            # Load override config
            override_path_obj = Path(override_path)
            with open(override_path_obj, "r") as f:
                override_config = json.load(f)

            # Merge configurations (override takes precedence)
            merged_config = {**base_config, **override_config}

            # Recursively merge mise_config objects
            if "mise_config" in base_config and "mise_config" in override_config:
                merged_config["mise_config"] = {
                    **base_config["mise_config"],
                    **override_config["mise_config"],
                }

            # Write merged config
            with open(output_path, "w") as f:
                json.dump(merged_config, f, indent=2)

            return {
                "status": "success",
                "message": "Configurations merged successfully",
                "base_path": base_path,
                "override_path": override_path,
                "output_path": output_path,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Config merge failed: {str(e)}",
                "base_path": base_path,
                "override_path": override_path,
                "output_path": output_path,
            }

    def _log_evidence(self, event_type: str, evidence_data: Dict[str, Any]):
        """Log evidence for verification"""
        evidence = {
            "timestamp": str(__import__("datetime").datetime.now()),
            "event_type": event_type,
            "data": evidence_data,
        }
        self.evidence_log.append(evidence)

    def get_evidence_report(self) -> Dict[str, Any]:
        """Generate evidence report"""
        return {
            "evidence_log": self.evidence_log,
            "total_events": len(self.evidence_log),
        }


def main():
    parser = argparse.ArgumentParser(description="Mise Configuration CLI")

    subparsers = parser.add_subparsers(dest="command", help="Mise command")

    # mise-validate command
    parser_mise_validate = subparsers.add_parser(
        "mise-validate", help="Validate .mise.toml configuration"
    )
    parser_mise_validate.add_argument(
        "--config", required=True, help="Path to config file"
    )
    parser_mise_validate.add_argument(
        "--schema", default="1.0.0", help="Schema version"
    )

    # mise-generate command
    parser_mise_generate = subparsers.add_parser(
        "mise-generate", help="Generate .mise.toml template"
    )
    parser_mise_generate.add_argument("--runtime", required=True, help="Runtime type")
    parser_mise_generate.add_argument("--output", required=True, help="Output path")
    parser_mise_generate.add_argument(
        "--template", default="default", help="Template type"
    )

    # mise-merge command
    parser_mise_merge = subparsers.add_parser("mise-merge", help="Merge configurations")
    parser_mise_merge.add_argument("--base", required=True, help="Base config path")
    parser_mise_merge.add_argument(
        "--override", required=True, help="Override config path"
    )
    parser_mise_merge.add_argument("--output", required=True, help="Output config path")

    args = parser.parse_args()

    validator = MiseValidator()

    if args.command == "mise-validate":
        result = validator.validate_config(args.config, args.schema)
    elif args.command == "mise-generate":
        result = validator.generate_template(args.runtime, args.output, args.template)
    elif args.command == "mise-merge":
        result = validator.merge_configs(args.base, args.override, args.output)
    else:
        parser.print_help()
        sys.exit(1)

    # Save results if output file specified
    if args.output and args.command != "mise-merge":
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)

    # Print result
    if result["status"] == "success":
        print(f"✓ {args.command} completed successfully")
        print(f"  Result: {result}")
    else:
        print(f"✗ {args.command} failed")
        print(f"  Error: {result['message']}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
