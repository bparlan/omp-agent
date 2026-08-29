#!/bin/bash
# Simple test to understand env-check behavior

# Check if env-check exists
if command -v env-check >/dev/null 2>&1; then
    echo "env-check command exists"

    # Run env-check with a test project
    project_path="test_project"
    runtime="python"

    # Create the directory to make the test work
    mkdir -p "$project_path"

    # Try running env-check
    env_check_output=$(env-check --project "$project_path" --runtime "$runtime" --validate 2>&1 || true)
    echo "Command output: $env_check_output"

    # Check exit code
    echo "Exit code check: $?"

    # Run again without redirecting output
    echo "Direct execution:"
    env-check --project "$project_path" --runtime "$runtime" --validate
    echo "Exit code: $?"

else
    echo "env-check command does not exist"
fi
