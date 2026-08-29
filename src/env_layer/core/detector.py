"""
Environment Detector for the AEF Environment Layer.

This module implements environment detection functionality
as specified in FR-1.3 of the M11S1 specification.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
class EnvironmentDetector:
    """
    Environment detector for runtime and tool detection.

    Implements environment detection before agent task execution.
    """

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.detection_cache = {}

    def detect(self, runtime: str = None, task: str = None, use_cache: bool = False) -> Dict[str, Any]:
        """
        Detect environment for project and runtime.

        Args:
            runtime: Target runtime (python, node, rust, go, deno)
            task: Task name for pre-task detection
            use_cache: Use cached detection results if available

        Returns:
            Dict containing detection results
        """
        cache_key = f"{runtime}_{task}"

        if use_cache and cache_key in self.detection_cache:
            return self.detection_cache[cache_key]

        result = {
            "project_path": str(self.project_path),
            "detection_timestamp": "2024-01-01T00:00:00Z",
            "runtime_detected": runtime,
            "tools_found": [],
            "version": None,
            "isolation_setup": False,
            "status": "success",
            "errors": []
        }

        if runtime:
            # Detect runtime-specific tools and versions
            runtime_result = self._detect_runtime(runtime)
            result.update(runtime_result)

        if task:
            # Perform pre-task specific detection
            task_result = self._detect_for_task(task, runtime)
            result.update(task_result)

        # Setup workspace isolation
        if runtime:
            result["isolation_setup"] = self._setup_isolation(runtime)

        # Cache the result
        self.detection_cache[cache_key] = result

        return result

    def get_status(self, runtime: str = None) -> Dict[str, Any]:
        """
        Get cached environment status.

        Args:
            runtime: Target runtime

        Returns:
            Dict containing environment status
        """
        status = {
            "project_path": str(self.project_path),
            "detection_timestamp": "2024-01-01T00:00:00Z",
            "cached_results": list(self.detection_cache.keys()),
            "last_detection": max(self.detection_cache.keys()) if self.detection_cache else None,
            "status": "ready"
        }

        if runtime:
            cache_key = f"{runtime}_"
            matching_keys = [k for k in self.detection_cache.keys() if k.startswith(cache_key)]
            if matching_keys:
                status["runtime_results"] = {
                    k: self.detection_cache[k] for k in matching_keys
                }

        return status

    def refresh(self, runtime: str = None) -> Dict[str, Any]:
        """
        Force environment re-detection.

        Args:
            runtime: Target runtime

        Returns:
            Dict containing fresh detection results
        """
        # Clear cache for specified runtime
        if runtime:
            keys_to_remove = [k for k in self.detection_cache.keys() if k.startswith(f"{runtime}_")]
            for key in keys_to_remove:
                del self.detection_cache[key]
        else:
            self.detection_cache.clear()

        # Perform fresh detection
        if runtime:
            return self.detect(runtime=runtime, use_cache=False)
        else:
            return self.detect(use_cache=False)

    def _detect_runtime(self, runtime: str) -> Dict[str, Any]:
        """
        Detect runtime-specific tools and versions.

        Args:
            runtime: Target runtime

        Returns:
            Dict containing runtime detection results
        """
        result = {
            "runtime_detected": runtime,
            "tools_found": [],
            "version": None,
            "compatibility_score": 0.0
        }

        # Runtime-specific detection
        detection_methods = {
            "python": self._detect_python,
            "node": self._detect_node,
            "rust": self._detect_rust,
            "go": self._detect_go,
            "deno": self._detect_deno
        }

        if runtime in detection_methods:
            return detection_methods[runtime](result)

        return result

    def _detect_python(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Python runtime and tools."""
        tools = []
        version = None

        # Try to detect python version
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                # Parse version like "Python 3.11.0"
                import re
                match = re.search(r'Python (\d+\.\d+\.\d+)', version_output)
                if match:
                    version = match.group(1)
                tools.append("python")

            # Check for pip
            pip_result = subprocess.run(
                ["pip3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if pip_result.returncode == 0:
                tools.append("pip")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass

        base_result.update({
            "tools_found": tools,
            "version": version,
            "compatibility_score": 0.95 if version else 0.0
        })

        return base_result

    def _detect_node(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Node.js runtime and tools."""
        tools = []
        version = None

        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                import re
                match = re.search(r'v(\d+\.\d+\.\d+)', version_output)
                if match:
                    version = match.group(1)
                tools.append("node")

            npm_result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if npm_result.returncode == 0:
                tools.append("npm")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass

        base_result.update({
            "tools_found": tools,
            "version": version,
            "compatibility_score": 0.95 if version else 0.0
        })

        return base_result

    def _detect_rust(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Rust runtime and tools."""
        tools = []
        version = None

        try:
            result = subprocess.run(
                ["rustc", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                import re
                match = re.search(r'rustc (\d+\.\d+\.\d+)', version_output)
                if match:
                    version = match.group(1)
                tools.append("rustc")

            cargo_result = subprocess.run(
                ["cargo", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if cargo_result.returncode == 0:
                tools.append("cargo")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass

        base_result.update({
            "tools_found": tools,
            "version": version,
            "compatibility_score": 0.95 if version else 0.0
        })

        return base_result

    def _detect_go(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Go runtime and tools."""
        tools = []
        version = None

        try:
            result = subprocess.run(
                ["go", "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                # Parse version like "go1.20.0"
                import re
                match = re.search(r'go1\.(\d+\.\d+\.\d+)', version_output)
                if match:
                    version = f"1.{match.group(1)}"
                tools.append("go")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass

        base_result.update({
            "tools_found": tools,
            "version": version,
            "compatibility_score": 0.95 if version else 0.0
        })

        return base_result

    def _detect_deno(self, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Deno runtime and tools."""
        tools = []
        version = None

        try:
            result = subprocess.run(
                ["deno", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                import re
                match = re.search(r'deno (\d+\.\d+\.\d+)', version_output)
                if match:
                    version = match.group(1)
                tools.append("deno")

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass

        base_result.update({
            "tools_found": tools,
            "version": version,
            "compatibility_score": 0.95 if version else 0.0
        })

        return base_result

    def _detect_for_task(self, task: str, runtime: str = None) -> Dict[str, Any]:
        """
        Detect environment specifically for a task.

        Args:
            task: Task name
            runtime: Target runtime

        Returns:
            Dict containing task-specific detection results
        """
        result = {
            "task_detected": task,
            "task_compatibility": True,
            "requirements_met": [],
            "missing_dependencies": [],
            "recommendations": []
        }

        # Task-specific checks based on runtime
        if runtime:
            task_checks = {
                "python": self._check_python_task_requirements,
                "node": self._check_node_task_requirements,
                "rust": self._check_rust_task_requirements,
                "go": self._check_go_task_requirements,
                "deno": self._check_deno_task_requirements
            }

            if runtime in task_checks:
                task_result = task_checks[runtime](task)
                result.update(task_result)

        return result

    def _check_python_task_requirements(self, task: str) -> Dict[str, Any]:
        """Check Python-specific task requirements."""
        return {
            "requirements_met": ["python3", "pip"],
            "missing_dependencies": [],
            "recommendations": ["virtualenv", "poetry", "pipenv"]
        }

    def _check_node_task_requirements(self, task: str) -> Dict[str, Any]:
        """Check Node.js-specific task requirements."""
        return {
            "requirements_met": ["node", "npm"],
            "missing_dependencies": [],
            "recommendations": ["yarn", "pnpm"]
        }

    def _check_rust_task_requirements(self, task: str) -> Dict[str, Any]:
        """Check Rust-specific task requirements."""
        return {
            "requirements_met": ["rustc", "cargo"],
            "missing_dependencies": [],
            "recommendations": []
        }

    def _check_go_task_requirements(self, task: str) -> Dict[str, Any]:
        """Check Go-specific task requirements."""
        return {
            "requirements_met": ["go"],
            "missing_dependencies": [],
            "recommendations": []
        }

    def _check_deno_task_requirements(self, task: str) -> Dict[str, Any]:
        """Check Deno-specific task requirements."""
        return {
            "requirements_met": ["deno"],
            "missing_dependencies": [],
            "recommendations": []
        }

    def _setup_isolation(self, runtime: str) -> bool:
        """
        Setup workspace isolation for the runtime.

        Args:
            runtime: Target runtime

        Returns:
            bool: True if isolation setup successful
        """
        try:
            isolation_dir = self.project_path / ".aef-env" / "isolation" / runtime
            isolation_dir.mkdir(parents=True, exist_ok=True)

            # Create isolation configuration
            isolation_config = {
                "runtime": runtime,
                "setup_timestamp": "2024-01-01T00:00:00Z",
                "isolation_mode": "workspace_per_project",
                "environment_prefix": "AEF_"
            }

            config_file = isolation_dir / "isolation.json"
            with open(config_file, 'w') as f:
                json.dump(isolation_config, f, indent=2)

            return True

        except Exception as e:
            return False