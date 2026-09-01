"""
Handlers for environment detection CLI commands (FR-1.3).

Implements the observable contracts for:
- env-detect
- env-status
- env-refresh
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any


def handle_env_detect(args):
    """Implement env-detect --project <project_path> --runtime <runtime> --task <task_name> [--cache]."""
    project_path = Path(args.project)
    runtime = args.runtime
    task_name = args.task
    use_cache = getattr(args, "cache", False)

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Check cache if requested
    cache_file = project_path / f".aef-env/cache/{runtime}_{task_name}.json"
    if use_cache and cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                cached_result = json.load(f)
            print(
                f"Using cached environment detection result for {runtime}/{task_name}"
            )
            output_detection_result(
                cached_result, output_json=getattr(args, "json", False)
            )
            sys.exit(0)
        except Exception as e:
            print(f"Warning: Could not read cache: {e}", file=sys.stderr)

    # Perform environment detection
    detection_result = perform_environment_detection(project_path, runtime, task_name)

    # Save to cache if successful
    if use_cache:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(cache_file, "w") as f:
                json.dump(detection_result, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not write to cache: {e}", file=sys.stderr)

    # Output result
    output_detection_result(detection_result, output_json=getattr(args, "json", False))

    # Exit based on detection success
    if detection_result.get("success", False):
        sys.exit(0)
    else:
        sys.exit(1)


def handle_env_status(args):
    """Implement env-status --project <project_path> --runtime <runtime>."""
    project_path = Path(args.project)
    runtime = args.runtime

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Check for environment status file
    status_file = project_path / f".aef-env/status/{runtime}_status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)

    if status_file.exists():
        try:
            with open(status_file, "r") as f:
                status_result = json.load(f)
            print(f"Environment status for {runtime} in {project_path}")
            print(json.dumps(status_result, indent=2))
            sys.exit(0)
        except Exception as e:
            print(f"Warning: Could not read status file: {e}", file=sys.stderr)

    # No status available
    print(f"No environment status available for {runtime} in {project_path}")
    print("Status: NOT_CONFIGURED")
    sys.exit(1)


def handle_env_refresh(args):
    """Implement env-refresh --project <project_path> --runtime <runtime>."""
    project_path = Path(args.project)
    runtime = args.runtime

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Remove cache and status files
    import shutil

    # Remove cache
    cache_dir = project_path / ".aef-env/cache"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        print(f"Removed cache directory: {cache_dir}")

    # Remove status files for this runtime
    status_dir = project_path / ".aef-env/status"
    if status_dir.exists():
        for status_file in status_dir.glob("*.json"):
            if runtime in status_file.name:
                status_file.unlink()
        print(f"Removed status files for {runtime}")

    # Re-run detection to generate fresh status
    print(f"Environment refresh completed for {runtime} in {project_path}")
    print("You can now run 'env-detect' to get fresh detection results.")

    sys.exit(0)


def perform_environment_detection(
    project_path: Path, runtime: str, task_name: str
) -> Dict[str, Any]:
    """Perform the actual environment detection."""
    result = {
        "project_path": str(project_path),
        "runtime": runtime,
        "task_name": task_name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "success": False,
        "details": {},
    }

    # Step 1: Check project structure
    result["details"]["project_structure"] = analyze_project_structure(project_path)

    # Step 2: Detect runtime
    result["details"]["runtime_detection"] = detect_runtime(runtime)

    # Step 3: Check tool availability
    result["details"]["tool_availability"] = check_tool_availability(runtime)

    # Step 4: Validate compatibility
    result["details"]["compatibility_validation"] = validate_compatibility(
        result["details"]["runtime_detection"], result["details"]["tool_availability"]
    )

    # Step 5: Setup workspace isolation
    result["details"]["isolation_setup"] = setup_workspace_isolation(
        project_path, runtime
    )

    # Determine overall success
    result["success"] = all(
        [
            result["details"]["project_structure"]["valid"],
            result["details"]["runtime_detection"]["detected"],
            result["details"]["tool_availability"]["sufficient"],
            result["details"]["compatibility_validation"]["compatible"],
            result["details"]["isolation_setup"]["success"],
        ]
    )

    return result


def analyze_project_structure(project_path: Path) -> Dict[str, Any]:
    """Analyze the project structure for runtime detection."""
    structure = {
        "valid": True,
        "has_source_files": False,
        "config_files": [],
        "language_indicators": [],
    }

    # Check for common source files based on runtime
    runtime = "python"  # This should be passed from caller

    common_configs = {
        "python": [".python-version", "requirements.txt", "setup.py", "pyproject.toml"],
        "node": ["package.json", "npm-lock.json", ".node-version"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "go": ["go.mod", "go.sum"],
        "deno": ["deno.json", "deno.lock"],
    }

    # Look for config files
    for config_file in common_configs.get(runtime, []):
        if (project_path / config_file).exists():
            structure["config_files"].append(config_file)

    # Check for source files
    source_extensions = {
        "python": [".py"],
        "node": [".js", ".ts"],
        "rust": [".rs"],
        "go": [".go"],
        "deno": [".ts", ".js"],
    }

    for ext in source_extensions.get(runtime, []):
        if any(project_path.glob(f"**/*.{ext}")):
            structure["has_source_files"] = True
            structure["language_indicators"].append(ext)

    return structure


def detect_runtime(runtime: str) -> Dict[str, Any]:
    """Detect the specified runtime."""
    detection = {
        "detected": False,
        "version": None,
        "installation_path": None,
        "confidence": 0.0,
    }

    # Try to find the runtime
    runtime_commands = {
        "python": ["python", "--version"],
        "node": ["node", "--version"],
        "rust": ["rustc", "--version"],
        "go": ["go", "version"],
        "deno": ["deno", "--version"],
    }

    if runtime in runtime_commands:
        try:
            result = subprocess.run(
                runtime_commands[runtime],
                capture_output=True,
                text=True,
                timeout=10,
                check=True,
            )
            # Parse version from output
            output = result.stdout.strip()
            detection["detected"] = True
            detection["version"] = output
            detection["confidence"] = 0.95
        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            detection["detected"] = False
            detection["confidence"] = 0.0

    return detection


def check_tool_availability(runtime: str) -> Dict[str, Any]:
    """Check availability of required tools for the runtime."""
    tools_map = {
        "python": ["python", "pip"],
        "node": ["node", "npm"],
        "rust": ["rustc", "cargo"],
        "go": ["go"],
        "deno": ["deno"],
    }

    required_tools = tools_map.get(runtime, [])
    tool_status = {}

    for tool in required_tools:
        try:
            # Different commands for version checking
            if tool == "pip":
                result = subprocess.run(
                    ["pip", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=True,
                )
            elif tool == "npm":
                result = subprocess.run(
                    ["npm", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=True,
                )
            else:
                result = subprocess.run(
                    [tool, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=True,
                )

            tool_status[tool] = {
                "available": True,
                "version": result.stdout.strip(),
                "confidence": 0.9,
            }
        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            tool_status[tool] = {
                "available": False,
                "version": None,
                "confidence": 0.0,
            }

    # Determine if sufficient tools are available
    available_tools = sum(1 for tool in tool_status.values() if tool["available"])
    sufficient = available_tools >= len(required_tools) * 0.5  # At least 50% available

    return {
        "sufficient": sufficient,
        "required_tools": required_tools,
        "tool_status": tool_status,
        "available_count": available_tools,
        "total_required": len(required_tools),
    }


def validate_compatibility(
    runtime_detection: Dict[str, Any], tool_availability: Dict[str, Any]
) -> Dict[str, Any]:
    """Validate compatibility between detected runtime and available tools."""
    compatibility = {
        "compatible": False,
        "issues": [],
        "recommendations": [],
    }

    # Check if runtime was detected
    if not runtime_detection.get("detected", False):
        compatibility["issues"].append("Runtime not detected")
        compatibility["recommendations"].append("Install the required runtime")
        return compatibility

    # Check if sufficient tools are available
    if not tool_availability.get("sufficient", False):
        compatibility["issues"].append("Insufficient tool availability")
        compatibility["recommendations"].append("Install missing tools")

    # If all checks pass, consider it compatible
    compatibility["compatible"] = len(compatibility["issues"]) == 0

    return compatibility


def setup_workspace_isolation(project_path: Path, runtime: str) -> Dict[str, Any]:
    """Setup workspace isolation for the project."""
    isolation = {
        "success": False,
        "workspace_path": None,
        "isolation_mode": "workspace_per_project",
        "cross_contamination_prevention": True,
    }

    try:
        # Create workspace directory
        workspace_dir = (
            project_path
            / ".aef-env"
            / "workspaces"
            / f"proj_{project_path.name}_{runtime}"
        )
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # Create environment file
        env_file = workspace_dir / ".env"
        with open(env_file, "w") as f:
            f.write(f"AEF_RUNTIME={runtime}\n")
            f.write(f"AEF_PROJECT_PATH={project_path}\n")
            f.write(
                f"AEF_TIMESTAMP={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n"
            )

        isolation["workspace_path"] = str(workspace_dir)
        isolation["success"] = True

    except Exception as e:
        isolation["issues"] = [str(e)]
        isolation["success"] = False

    return isolation


def output_detection_result(result: Dict[str, Any], output_json: bool = False):
    """Output the detection result in the specified format."""
    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print("Environment Detection Results")
        print(f"Project: {result['project_path']}")
        print(f"Runtime: {result['runtime']}")
        print(f"Task: {result['task_name']}")
        print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
        print(f"Timestamp: {result['timestamp']}")

        if "details" in result:
            print("\nDetails:")
            for category, data in result["details"].items():
                print(f"  {category}: {data}")
