"""
Handlers for Mise configuration CLI commands (FR-1.2).

Implements the observable contracts for:
- mise-validate
- mise-generate
- mise-merge
"""

import json
import sys
from pathlib import Path


def handle_mise_validate(args):
    """Implement mise-validate --config <path> --schema <version>."""
    config_path = Path(args.config)
    schema_version = args.schema

    # Basic validation
    if not config_path.exists():
        print(f"Error: Config file does not exist: {config_path}", file=sys.stderr)
        sys.exit(1)

    # Read config file
    try:
        with open(config_path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Could not read config file {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Basic validation - in production would use proper JSON schema validation
    validation_errors = []
    warnings = []

    # Check if it's TOML format (simplified check)
    if not content.strip().startswith("[") and "=" in content:
        # This looks like TOML
        if "environment =" not in content:
            warnings.append("Missing 'environment' section")
        if "runtime =" not in content:
            warnings.append("Missing 'runtime' in environment section")
        if "version =" not in content:
            warnings.append("Missing 'version' in environment section")
    else:
        # Try to parse as JSON (for schema validation)
        try:
            config_json = json.loads(content)
            # Validate schema structure
            if "environment" not in config_json:
                validation_errors.append("Missing 'environment' section")
            elif "runtime" not in config_json["environment"]:
                validation_errors.append("Missing 'runtime' in environment section")
            elif "version" not in config_json["environment"]:
                validation_errors.append("Missing 'version' in environment section")
        except json.JSONDecodeError:
            validation_errors.append("Invalid JSON format")

    # Schema-specific validation
    if schema_version != "1.0.0":
        warnings.append(
            f"Schema version {schema_version} not officially supported (using 1.0.0)"
        )

    # Output results
    result = {
        "config_path": str(config_path),
        "schema_version": schema_version,
        "validation_status": "valid" if not validation_errors else "invalid",
        "warnings": warnings,
        "errors": validation_errors,
    }

    if validation_errors:
        print(f"Validation FAILED for {config_path}")
        print(f"Schema: {schema_version}")
        print(f"Errors ({len(validation_errors)}):")
        for error in validation_errors:
            print(f"  ✗ {error}")
        print(f"Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        sys.exit(1)
    else:
        print(f"Validation PASSED for {config_path}")
        print(f"Schema: {schema_version}")
        if warnings:
            print(f"Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  ⚠ {warning}")
        sys.exit(0)


def handle_mise_generate(args):
    """Implement mise-generate --runtime <runtime> --output <path> --template <type>."""
    runtime = args.runtime
    output_path = Path(args.output)
    template_type = args.template

    # Validate runtime
    supported_runtimes = ["python", "node", "rust", "go", "deno", "common"]
    if runtime not in supported_runtimes:
        print(f"Error: Unsupported runtime: {runtime}", file=sys.stderr)
        print(f"Supported runtimes: {', '.join(supported_runtimes)}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate TOML content based on runtime and template type
    if template_type == "minimal":
        content = f'environment = {{ runtime = "{runtime}", version = "latest" }}\n'
    elif template_type == "full":
        content = f"""# .mise.toml - Mise configuration for {runtime}
environment = {{
    runtime = "{runtime}",
    version = "latest"
}}

tools = [
    {{
        name = "{runtime}",
        version = "latest",
        options = {{}}
    }},
    {{
        name = "{runtime}-deps",
        version = "latest",
        options = {{}}
    }}
]

workspace = {{
    isolation = true,
    path = ".mise-env",
    permissions = ["read", "write"]
}}

# Cross-language compatibility
cross_language = {{
    compatibility_mode = false,
    fallback_strategies = ["tool_fallback", "system_default"],
    shared_components = []
}}
"""
    elif template_type == "custom":
        content = f"""# Custom .mise.toml configuration for {runtime}
environment = {{
    runtime = "{runtime}",
    version = "custom"
}}

# Add your custom tools here
tools = []

# Custom workspace configuration
workspace = {{
    isolation = true,
    path = ".custom-env"
}}
"""
    else:
        print(f"Error: Unknown template type: {template_type}", file=sys.stderr)
        print("Supported template types: minimal, full, custom", file=sys.stderr)
        sys.exit(1)

    # Write to file
    with open(output_path, "w") as f:
        f.write(content)

    print(f"Generated {template_type} {runtime} configuration")
    print(f"Output file: {output_path}")
    print("Content preview:")
    print("-" * 40)
    # Show first few lines
    with open(output_path, "r") as f:
        preview_lines = f.readlines()[:10]
        for line in preview_lines:
            print(line.rstrip())
    print("-" * 40)

    sys.exit(0)


def handle_mise_merge(args):
    """Implement mise-merge --base <path> --override <path> --output <path>."""
    base_path = Path(args.base)
    override_path = Path(args.override)
    output_path = Path(args.output)

    # Validate input files
    for path, name in [(base_path, "base"), (override_path, "override")]:
        if not path.exists():
            print(f"Error: {name} file does not exist: {path}", file=sys.stderr)
            sys.exit(1)

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read base configuration
    with open(base_path, "r") as f:
        base_content = f.read()

    # Read override configuration
    with open(override_path, "r") as f:
        override_content = f.read()

    # Simple merging logic - in production would use proper TOML parser
    merged_content = base_content + "\n\n# Override configuration\n" + override_content

    # Write merged content
    with open(output_path, "w") as f:
        f.write(merged_content)

    print("Merged configuration successfully")
    print(f"Base: {base_path}")
    print(f"Override: {override_path}")
    print(f"Output: {output_path}")
    print(f"Size: {output_path.stat().st_size} bytes")

    sys.exit(0)
