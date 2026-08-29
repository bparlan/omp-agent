#!/usr/bin/env python3
"""
Test WorkspaceManager functionality
"""

import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, 'src')

from env_layer.core.workspace import WorkspaceManager

def test_workspace_manager():
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = Path(temp_dir)

        # Test WorkspaceManager initialization
        manager = WorkspaceManager(project_path)

        # Test workspace creation
        result = manager.create('python', 'test_ws_1')
        print(f"Create result: {result['success']} - {result['message']}")
        assert result['success'], f"Workspace creation failed: {result.get('message')}"
        assert result['workspace_name'] == 'test_ws_1'
        assert result['runtime'] == 'python'
        assert result['path'] is not None

        # Test workspace status
        status = manager.get_status('python')
        print(f"Status success: {status.get('success', 'N/A')}")
        print(f"Total workspaces: {status['total_workspaces']}")
        print(f"Active count: {status['active_count']}")

        # Find active workspace
        from env_layer.core.workspace import find_active_workspace
        active_ws = find_active_workspace(project_path, 'python')
        print(f"Active workspace found: {active_ws is not None}")

        print("\nWorkspaceManager basic functionality test PASSED")
        return True

if __name__ == "__main__":
    try:
        success = test_workspace_manager()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)