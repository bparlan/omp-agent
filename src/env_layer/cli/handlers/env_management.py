"""
Handlers for environment management CLI commands (FR-1.1).

Implements the observable contracts for:
- env-check
- env-setup
- env-list
- env-diagnose
"""

import json
import subprocess
import sys
from pathlib import Path


def handle_env_check(args):
    """Implement env-check --project <project_path> --runtime <runtime> [--validate]."""
    project_path = Path(args.project)
    runtime = args.runtime
    validate = getattr(args, "validate", False)

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Check if .mise.toml exists
    mise_toml = project_path / ".mise.toml"
    if not mise_toml.exists():
        print(
            f"Warning: .mise.toml not found in project: {project_path}", file=sys.stderr
        )

    # Determine available tools based on runtime
    tools_map = {
        "python": ["python", "pip"],
        "node": ["node", "npm"],
        "rust": ["rustc", "cargo"],
        "go": ["go"],
        "deno": ["deno"],
    }

    available_tools = tools_map.get(runtime, [])

    # Check if tools are available
    tool_status = {}
    for tool in available_tools:
        try:
            result = subprocess.run(
                [tool, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            tool_status[tool] = {"available": True, "version": result.stdout.strip()}
        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            tool_status[tool] = {"available": False, "version": None}

    # Build response
    response = {
        "project_path": str(project_path),
        "runtime": runtime,
        "validation_performed": validate,
        "tools_status": tool_status,
        "summary": {
            "total_tools": len(available_tools),
            "available_tools": sum(
                1 for tool in tool_status.values() if tool["available"]
            ),
            "missing_tools": [
                tool for tool, status in tool_status.items() if not status["available"]
            ],
        },
    }

    # Output based on format preference
    if hasattr(args, "json") and args.json:
        print(json.dumps(response, indent=2))
    else:
        print(f"Environment Check Results for {project_path}")
        print(f"Runtime: {runtime}")
        print("Tools Status:")
        for tool, status in tool_status.items():
            status_icon = "✓" if status["available"] else "✗"
            version_info = f" ({status['version']})" if status["available"] else ""
            print(f"  {status_icon} {tool}{version_info}")
        print(
            f"Summary: {response['summary']['available_tools']}/{response['summary']['total_tools']} tools available"
        )

    # Exit with appropriate code
    if response["summary"]["available_tools"] == 0:
        sys.exit(1)
    elif validate and response["summary"]["missing_tools"]:
        sys.exit(2)
    else:
        sys.exit(0)


def handle_env_setup(args):
    """Implement env-setup --project <project_path> --runtime <runtime> --tool <tool_name> --version <version>."""
    project_path = Path(args.project)
    runtime = args.runtime
    tool_name = args.tool
    version = args.version

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Create project directory if it doesn't exist
    project_path.mkdir(parents=True, exist_ok=True)

    # Update or create .mise.toml
    mise_toml = project_path / ".mise.toml"
    config = {}

    if mise_toml.exists():
        # Read existing config
        try:
            with open(mise_toml, "r") as f:
                content = f.read()
                # Simple parsing - in production would use proper TOML parser
                if "environment =" in content:
                    # Extract existing environment section
                    lines = content.split("\n")
                    env_start = None
                    for i, line in enumerate(lines):
                        if "environment =" in line and "{" in line:
                            env_start = i
                            break
                    if env_start is not None:
                        # Find the end of environment section
                        brace_count = 0
                        for i in range(env_start, len(lines)):
                            brace_count += lines[i].count("{")
                            brace_count -= lines[i].count("}")
                            if brace_count == 0:
                                env_end = i
                                break
                        # Keep the rest of the file
                        config_lines = lines[:env_start] + lines[env_end + 1 :]
                        config_content = "\n".join(config_lines)
                    else:
                        config_content = content
                else:
                    config_content = content
        except Exception as e:
            print(f"Warning: Could not parse existing .mise.toml: {e}", file=sys.stderr)
            config_content = ""
    else:
        config_content = ""

    # Build new environment section
    new_env_section = (
        f'environment = {{ runtime = "{runtime}", version = "{version}" }}\n'
    )
    new_tools_section = f'tools = [{{ name = "{tool_name}", version = "{version}" }}]\n'

    # Combine config
    if config_content:
        # Simple approach: append if sections don't exist
        if "environment =" not in config_content:
            config_content += f"\n{new_env_section}"
        if "tools =" not in config_content:
            config_content += f"\n{new_tools_section}"
    else:
        config_content = f"{new_env_section}{new_tools_section}\n"

    # Write back
    with open(mise_toml, "w") as f:
        f.write(config_content)

    print(f"Environment setup completed for {project_path}")
    print(f"Runtime: {runtime}")
    print(f"Tool: {tool_name} version {version}")
    print(f"Configuration saved to: {mise_toml}")

    sys.exit(0)


def handle_env_list(args):
    """Implement env-list --runtime <runtime> --all [--json]."""
    runtime = args.runtime
    all_runtimes = getattr(args, "all", False)
    output_json = getattr(args, "json", False)

    # Available runtimes and their tools
    runtimes_info = {
        "python": {
            "description": "Python runtime",
            "tools": ["python", "pip"],
            "versions": ["3.8", "3.9", "3.10", "3.11", "3.12"],
        },
        "node": {
            "description": "Node.js runtime",
            "tools": ["node", "npm"],
            "versions": ["14", "16", "18", "20"],
        },
        "rust": {
            "description": "Rust runtime",
            "tools": ["rustc", "cargo"],
            "versions": ["1.56", "1.60", "1.65", "1.70"],
        },
        "go": {
            "description": "Go runtime",
            "tools": ["go"],
            "versions": ["1.18", "1.19", "1.20"],
        },
        "deno": {
            "description": "Deno runtime",
            "tools": ["deno"],
            "versions": ["1.30", "1.35"],
        },
    }

    if all_runtimes:
        # List all runtimes
        result = {}
        for rt, info in runtimes_info.items():
            result[rt] = info
    else:
        # List only the specified runtime
        if runtime in runtimes_info:
            result = {runtime: runtimes_info[runtime]}
        else:
            print(f"Error: Unknown runtime: {runtime}", file=sys.stderr)
            sys.exit(1)

    # Output based on format
    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"Available {runtime if not all_runtimes else 'all'} runtime information:"
        )
        for rt, info in result.items():
            print(f"\n{rt.upper()}:")
            print(f"  Description: {info['description']}")
            print(f"  Tools: {', '.join(info['tools'])}")
            print(f"  Available versions: {', '.join(info['versions'])}")

    sys.exit(0)


def handle_env_diagnose(args):
    """Implement env-diagnose --project <project_path> [--output <format>]."""
    project_path = Path(args.project)
    output_format = getattr(args, "output", "text")

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Initialize diagnostic results
    diagnostics = {
        "project_path": str(project_path),
        "timestamp": "2024-01-01T00:00:00Z",  # Simplified - would use actual timestamp
        "issues": [],
        "warnings": [],
        "status": "healthy",
    }

    # Check for .mise.toml
    mise_toml = project_path / ".mise.toml"
    if not mise_toml.exists():
        diagnostics["warnings"].append("No .mise.toml configuration found")
        diagnostics["status"] = "warning"

    # Check if project directory is empty or has no source files
    source_extensions = [".py", ".js", ".ts", ".rs", ".go", ".md"]
    has_source_files = any(project_path.glob(f"*.[{''.join(source_extensions)}]"))

    if not has_source_files:
        diagnostics["warnings"].append(
            "Project directory appears to be empty or lacks source files"
        )
        diagnostics["status"] = "warning"

    # Check runtime compatibility (simplified)
    # In production, would check mise.toml for runtime specification

    # Check for environment variables that might indicate runtime issues
    import os

    if "PYTHONPATH" in os.environ and runtime not in ["python"]:
        diagnostics["warnings"].append(
            "PYTHONPATH environment variable set but runtime is not Python"
        )
        diagnostics["status"] = "warning"

    # Build detailed diagnosis
    if output_format == "json":
        print(json.dumps(diagnostics, indent=2))
    else:
        print(f"Environment Diagnosis for {project_path}")
        print(f"Status: {diagnostics['status'].upper()}")
        print(f"\nWarnings ({len(diagnostics['warnings'])}):")
        for warning in diagnostics["warnings"]:
            print(f"  ⚠ {warning}")

        print(f"\nIssues ({len(diagnostics['issues'])}):")
        if diagnostics["issues"]:
            for issue in diagnostics["issues"]:
                print(f"  ✗ {issue}")
        else:
            print("  None")

        print(
            f"\nOverall Health: {'✅ HEALTHY' if diagnostics['status'] == 'healthy' else '⚠️ WARNING' if diagnostics['status'] == 'warning' else '❌ HEALTHY'}"
        )

    # Exit based on status
    if diagnostics["status"] == "healthy":
        sys.exit(0)
    else:
        sys.exit(2)
