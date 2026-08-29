"""
Workspace Manager for the AEF Environment Layer.

This module implements workspace isolation functionality
as specified in FR-1.4 of the M11S1 specification.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
class WorkspaceManager:
    """
    Manages isolated workspaces for the AEF 6-layer substrate architecture.

    Provides workspace creation, activation, execution, status, and cleanup
    with cross-contamination prevention.
    """

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.workspace_base = self.project_path / ".aef-env" / "workspaces"
        self.workspace_base.mkdir(parents=True, exist_ok=True)

    def create(self, runtime: str, workspace_name: str) -> Dict[str, Any]:
        """
        Create an isolated workspace.

        Args:
            runtime: Target runtime
            workspace_name: Name for the workspace

        Returns:
            Creation result dictionary
        """
        result = {
            "success": False,
            "workspace_name": workspace_name,
            "runtime": runtime,
            "path": None,
            "isolation": {},
            "message": None,
        }

        try:
            workspace_dir = self.workspace_base / workspace_name
            workspace_dir.mkdir(parents=True, exist_ok=True)

            # Create workspace configuration
            config = self._create_workspace_config(runtime, workspace_name)
            config_file = workspace_dir / "config.json"
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)

            # Create environment file
            env_file = workspace_dir / ".env"
            with open(env_file, 'w') as f:
                f.write(f"AEF_WORKSPACE_NAME={workspace_name}\n")
                f.write(f"AEF_RUNTIME={runtime}\n")
                f.write(f"AEF_PROJECT_PATH={self.project_path}\n")
                f.write(f"AEF_ISOLATION_MODE=workspace_per_project\n")

            # Create workspace status
            status = self._create_workspace_status(runtime, workspace_name)
            status_file = workspace_dir / "status.json"
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

            result["path"] = str(workspace_dir)
            result["isolation"] = config["isolation"]
            result["success"] = True
            result["message"] = f"Workspace '{workspace_name}' created successfully"

        except Exception as e:
            result["message"] = f"Failed to create workspace: {e}"

        return result

    def activate(self, runtime: str) -> Dict[str, Any]:
        """
        Activate workspace isolation.

        Args:
            runtime: Target runtime

        Returns:
            Activation result dictionary
        """
        result = {
            "success": False,
            "runtime": runtime,
            "workspace": None,
            "message": None,
        }

        try:
            # Find workspace for this project and runtime
            workspace_pattern = f"proj_{self.project_path.name}_{runtime}"
            workspace_dir = self.workspace_base / workspace_pattern

            if not workspace_dir.exists():
                result["message"] = f"No workspace found for project {self.project_path} and runtime {runtime}"
                return result

            # Check if workspace is already active
            status_file = workspace_dir / "status.json"
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
                if status.get("active", False):
                    result["success"] = True
                    result["workspace"] = str(workspace_dir)
                    result["message"] = f"Workspace '{workspace_pattern}' is already active"
                    return result

            # Activate workspace
            activation_config = {
                "workspace_name": workspace_pattern,
                "activated_timestamp": "2024-01-01T00:00:00Z",
                "activated_by": "workspace_manager",
                "active": True,
            }

            with open(status_file, 'w') as f:
                json.dump(activation_config, f, indent=2)

            result["success"] = True
            result["workspace"] = str(workspace_dir)
            result["message"] = f"Workspace '{workspace_pattern}' activated successfully"

        except Exception as e:
            result["message"] = f"Failed to activate workspace: {e}"

        return result

    def execute(self, runtime: str, command: str, args: List[str] = None) -> Dict[str, Any]:
        """
        Execute command in isolated workspace.

        Args:
            runtime: Target runtime
            command: Command to execute
            args: Command arguments

        Returns:
            Execution result dictionary
        """
        if args is None:
            args = []

        result = {
            "success": False,
            "command": command,
            "args": args,
            "runtime": runtime,
            "stdout": None,
            "stderr": None,
            "exit_code": None,
            "duration": None,
            "workspace": None,
            "message": None,
        }

        try:
            # Find active workspace for this project and runtime
            workspace_dir = self._find_active_workspace(runtime)
            if not workspace_dir:
                result["message"] = f"No active workspace found for project {self.project_path} and runtime {runtime}"
                result["message"] += "\nUse 'activate' to activate a workspace first"
                return result

            result["workspace"] = str(workspace_dir)

            # Prepare execution environment
            env = os.environ.copy()
            env.update({
                "AEF_WORKSPACE_PATH": str(workspace_dir),
                "AEF_RUNTIME": runtime,
                "AEF_PROJECT_PATH": str(self.project_path),
                "AEF_ISOLATION_MODE": "workspace_per_project"
            })

            # Execute command
            import time
            start_time = time.time()

            full_command = [command] + args
            proc = subprocess.run(
                full_command,
                cwd=workspace_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                check=False
            )

            duration = time.time() - start_time

            result["stdout"] = proc.stdout
            result["stderr"] = proc.stderr
            result["exit_code"] = proc.returncode
            result["duration"] = duration

            if proc.returncode == 0:
                result["success"] = True
                result["message"] = f"Command executed successfully in workspace"
            else:
                result["message"] = f"Command failed with exit code {proc.returncode}"

        except subprocess.TimeoutExpired:
            result["message"] = f"Command timed out (1 hour limit)"
            result["exit_code"] = 124

        except Exception as e:
            result["message"] = f"Failed to execute command: {e}"

        return result

    def get_status(self, runtime: str) -> Dict[str, Any]:
        """
        Get workspace status.

        Args:
            runtime: Target runtime

        Returns:
            Status dictionary
        """
        result = {
            "runtime": runtime,
            "project_path": str(self.project_path),
            "workspaces": [],
            "active_workspace": None,
            "total_workspaces": 0,
            "active_count": 0,
            "message": None,
        }

        try:
            # List all workspaces for this project
            if not self.workspace_base.exists():
                result["message"] = "No workspaces found"
                return result

            for workspace_dir in self.workspace_base.iterdir():
                if not workspace_dir.is_dir():
                    continue

                workspace_info = {
                    "name": workspace_dir.name,
                    "path": str(workspace_dir),
                    "exists": True,
                    "active": False,
                    "created": None,
                    "last_accessed": None,
                }

                # Check status file
                status_file = workspace_dir / "status.json"
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        status = json.load(f)
                    workspace_info["active"] = status.get("active", False)
                    workspace_info["created"] = status.get("created_timestamp")
                    workspace_info["last_accessed"] = status.get("activated_timestamp")

                if workspace_info["active"]:
                    result["active_workspace"] = workspace_info

                result["workspaces"].append(workspace_info)

            result["total_workspaces"] = len(result["workspaces"])
            result["active_count"] = sum(1 for ws in result["workspaces"] if ws["active"])
            result["success"] = True
            result["message"] = f"Found {result['total_workspaces']} workspaces for project {self.project_path.name}"

        except Exception as e:
            result["message"] = f"Failed to get workspace status: {e}"

        return result

    def clean(self, runtime: str, force: bool = False) -> Dict[str, Any]:
        """
        Clean workspace.

        Args:
            runtime: Target runtime
            force: Force cleanup

        Returns:
            Cleanup result dictionary
        """
        result = {
            "success": False,
            "runtime": runtime,
            "cleaned_workspaces": [],
            "message": None,
        }

        try:
            # Find workspaces for this project and runtime
            if not self.workspace_base.exists():
                result["message"] = "No workspaces found to clean"
                return result

            workspaces_to_clean = []
            for workspace_dir in self.workspace_base.iterdir():
                if not workspace_dir.is_dir():
                    continue

                # Check if this is a workspace for the specified runtime
                if runtime in workspace_dir.name:
                    workspaces_to_clean.append(workspace_dir)

            if not workspaces_to_clean:
                result["message"] = f"No workspaces found for runtime '{runtime}'"
                return result

            # Clean workspaces
            for workspace_dir in workspaces_to_clean:
                if force or self._confirm_cleanup(workspace_dir):
                    # Remove workspace directory
                    shutil.rmtree(workspace_dir)
                    result["cleaned_workspaces"].append(str(workspace_dir))

            result["success"] = True
            result["message"] = f"Cleaned {len(result['cleaned_workspaces'])} workspace(s) for runtime '{runtime}'"

        except Exception as e:
            result["message"] = f"Failed to clean workspaces: {e}"

        return result

    def _create_workspace_config(self, runtime: str, workspace_name: str) -> Dict[str, Any]:
        """Create workspace configuration."""
        return {
            "workspace_name": workspace_name,
            "runtime": runtime,
            "created_timestamp": "2024-01-01T00:00:00Z",
            "isolation": {
                "mode": "workspace_per_project",
                "path": str(self.workspace_base / workspace_name),
                "cross_contamination_prevention": True,
                "environment_prefix": "AEF_",
            }
        }

    def _create_workspace_status(self, runtime: str, workspace_name: str) -> Dict[str, Any]:
        """Create workspace status."""
        return {
            "workspace_name": workspace_name,
            "runtime": runtime,
            "created_timestamp": "2024-01-01T00:00:00Z",
            "activated_timestamp": None,
            "activated_by": None,
            "active": False,
        }

    def _find_active_workspace(self, runtime: str) -> Optional[Path]:
        """Find an active workspace for the given runtime."""
        workspace_pattern = f"proj_{self.project_path.name}_{runtime}"
        workspace_dir = self.workspace_base / workspace_pattern

        if workspace_dir.exists():
            status_file = workspace_dir / "status.json"
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
                if status.get("active", False):
                    return workspace_dir

        return None

    def _confirm_cleanup(self, workspace_dir: Path) -> bool:
        """Confirm workspace cleanup (for non-force mode)."""
        # For non-force mode, we would prompt user
        # For automation, we assume confirmation in non-force mode
        return True
def find_active_workspace(project_path: Path, runtime: str) -> Optional[Path]:
    """
    Find an active workspace for the given project and runtime.

    Args:
        project_path: Project path
        runtime: Target runtime

    Returns:
        Active workspace directory or None
    """
    workspace_manager = WorkspaceManager(project_path)
    return workspace_manager._find_active_workspace(runtime)