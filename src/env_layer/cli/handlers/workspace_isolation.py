"""
Handlers for workspace isolation CLI commands (FR-1.4).

Implements the observable contracts for:
- workspace-create
- workspace-activate
- workspace-execute
- workspace-status
- workspace-clean
"""

import sys
from pathlib import Path

# Absolute import for WorkspaceManager
from env_layer.core.workspace import WorkspaceManager


def handle_workspace_create(args):
    """Implement workspace-create --project <project_path> --runtime <runtime> --name <workspace_name>."""
    project_path = Path(args.project)
    runtime = args.runtime
    workspace_name = args.name

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Use WorkspaceManager to create workspace
    manager = WorkspaceManager(project_path)
    result = manager.create(runtime, workspace_name)

    if result["success"]:
        print("Workspace created successfully")
        print(f"Workspace name: {result['workspace_name']}")
        print(f"Project path: {project_path}")
        print(f"Runtime: {result['runtime']}")
        print(f"Workspace directory: {result['path']}")
        print(f"Isolation mode: {result['isolation'].get('mode', 'unknown')}")
        sys.exit(0)
    else:
        print(f"Error: {result['message']}", file=sys.stderr)
        sys.exit(1)


def handle_workspace_activate(args):
    """Implement workspace-activate --project <project_path> --runtime <runtime>."""
    project_path = Path(args.project)
    runtime = args.runtime

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Use WorkspaceManager to activate workspace
    manager = WorkspaceManager(project_path)
    result = manager.activate(runtime)

    if result["success"]:
        print(f"Workspace '{result['workspace']}' activated successfully")
        print(f"Runtime: {result['runtime']}")
        print(f"Workspace directory: {result['workspace']}")
        sys.exit(0)
    else:
        print(f"Error: {result['message']}", file=sys.stderr)
        sys.exit(1)


def handle_workspace_execute(args):
    """Implement workspace-execute --project <project_path> --runtime <runtime> --command <command> [--args]."""
    project_path = Path(args.project)
    runtime = args.runtime
    command = args.command
    command_args = getattr(args, "args", []) or []

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Use WorkspaceManager to execute command
    manager = WorkspaceManager(project_path)
    result = manager.execute(runtime, command, command_args)

    if result["success"]:
        print("Command executed successfully in workspace")
        print(f"Command: {command} {' '.join(command_args)}")
        if result["stdout"]:
            print(f"Output:\n{result['stdout']}")
        if result["stderr"]:
            print(f"Stderr:\n{result['stderr']}")
        print(f"Duration: {result['duration']:.3f}s")
        sys.exit(0)
    else:
        print(f"Command failed with exit code {result['exit_code']}")
        print(f"Command: {command} {' '.join(command_args)}")
        if result["stdout"]:
            print(f"Stdout:\n{result['stdout']}")
        if result["stderr"]:
            print(f"Stderr:\n{result['stderr']}")
        print(f"Error: {result['message']}")
        sys.exit(result["exit_code"] if result["exit_code"] else 1)


def handle_workspace_status(args):
    """Implement workspace-status --project <project_path> --runtime <runtime>."""
    project_path = Path(args.project)
    runtime = args.runtime

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Use WorkspaceManager to get status
    manager = WorkspaceManager(project_path)
    result = manager.get_status(runtime)

    if "success" in result:
        print(f"Workspace Status for {project_path}")
        print(f"Runtime: {runtime}")
        print(f"Total workspaces: {result['total_workspaces']}")
        print(f"Active workspaces: {result['active_count']}")

        if result["active_workspace"]:
            aw = result["active_workspace"]
            print("\nActive Workspace:")
            print(f"  Name: {aw['name']}")
            print(f"  Path: {aw['path']}")
            print(f"  Active: {aw['active']}")
            print(f"  Created: {aw['created']}")
            print(f"  Last accessed: {aw['last_accessed']}")
        else:
            print("\nNo active workspace found")
            print("Use 'workspace-activate' to activate a workspace")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


def handle_workspace_clean(args):
    """Implement workspace-clean --project <project_path> --runtime <runtime> [--force]."""
    project_path = Path(args.project)
    runtime = args.runtime
    force = getattr(args, "force", False)

    # Basic validation
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Use WorkspaceManager to clean workspaces
    manager = WorkspaceManager(project_path)
    result = manager.clean(runtime, force)

    if result["success"]:
        print("Workspace cleanup completed")
        print(f"Runtime: {runtime}")
        print(f"Cleaned workspaces: {len(result['cleaned_workspaces'])}")
        for ws in result["cleaned_workspaces"]:
            print(f"  - {ws}")
        sys.exit(0)
    else:
        print(f"Error: {result['message']}", file=sys.stderr)
        sys.exit(1)


def find_active_workspace(project_path: Path, runtime: str) -> Path | None:
    """Find an active workspace for the given project and runtime."""
    # Use WorkspaceManager's static method
    return WorkspaceManager.find_active_workspace(project_path, runtime)
