#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

# --- Test Execution Strategies ---


def execute_markdown_strategy(project_path: str) -> None:
    """Executes tests for Markdown projects."""
    print(f"Executing Markdown strategy for project: {project_path}")

    # Construct the path to the markdown test script.
    # We assume the script is relative to the project root where aef-test-runner is invoked.
    markdown_test_script = Path("tests/M10/test_markdown_execution.sh")

    if not markdown_test_script.is_file():
        print(
            f"Error: Markdown test script not found at {markdown_test_script}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        # Execute the test script. We need to ensure it runs in the correct context.
        # The bin/aef-test-runner is assumed to be run from the project root.
        # We pass the project_path to the test script if it expects it.
        # Currently, the test scripts don't seem to take arguments, so we run it directly.
        # For future compatibility, a mechanism to pass args might be needed.

        # To mimic the original execution, we'll run it as a subprocess.
        # The result of the subprocess will determine success/failure.

        # NOTE: The previous failure was 'Fixture directory tests/fixtures/synthetic_project_docs/ not found.'
        # This strategy assumes that fixture setup is handled externally or by the test script itself.
        # If the fixture setup is part of the strategy, it would be implemented here.

        result = subprocess.run(
            ["bash", str(markdown_test_script)],
            capture_output=True,
            text=True,
            check=False,
        )  # check=False to capture non-zero exit codes

        print(result.stdout)
        if result.returncode != 0:
            print(
                f"Markdown strategy script failed with exit code {result.returncode}",
                file=sys.stderr,
            )
            print(f"Stderr:\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)

        print("Markdown strategy executed successfully.")

    except FileNotFoundError:
        print("Error: Bash executable not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred during Markdown strategy execution: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def execute_htmlcss_strategy(project_path: str) -> None:
    """Executes tests for Static HTML/CSS projects."""
    print(f"Executing HTML/CSS strategy for project: {project_path}")

    htmlcss_test_script = Path("tests/M10/test_htmlcss_execution.sh")
    if not htmlcss_test_script.is_file():
        print(
            f"Error: HTML/CSS test script not found at {htmlcss_test_script}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = subprocess.run(
            ["bash", str(htmlcss_test_script)],
            capture_output=True,
            text=True,
            check=False,
        )

        print(result.stdout)
        if result.returncode != 0:
            print(
                f"HTML/CSS strategy script failed with exit code {result.returncode}",
                file=sys.stderr,
            )
            print(f"Stderr:\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)

        print("HTML/CSS strategy executed successfully.")

    except FileNotFoundError:
        print("Error: Bash executable not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred during HTML/CSS strategy execution: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def execute_python_strategy(project_path: str) -> None:
    """Executes tests for Python projects."""
    print(f"Executing Python strategy for project: {project_path}")

    python_test_script = Path("tests/M10/test_python_execution.sh")
    if not python_test_script.is_file():
        print(
            f"Error: Python test script not found at {python_test_script}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        # For Python projects, we might need to ensure pytest is available.
        # The test script itself handles the check for pytest.
        result = subprocess.run(
            ["bash", str(python_test_script)],
            capture_output=True,
            text=True,
            check=False,
        )

        print(result.stdout)
        if result.returncode != 0:
            print(
                f"Python strategy script failed with exit code {result.returncode}",
                file=sys.stderr,
            )
            print(f"Stderr:\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)

        print("Python strategy executed successfully.")

    except FileNotFoundError:
        print("Error: Bash executable not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred during Python strategy execution: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def execute_aef_task_strategy(project_path: str) -> None:
    """Executes tests for Framework/AEF tasks."""
    print(f"Executing AEF Task strategy for project: {project_path}")

    aef_task_test_script = Path("tests/M10/test_aef_task_execution.sh")
    if not aef_task_test_script.is_file():
        print(
            f"Error: AEF Task test script not found at {aef_task_test_script}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = subprocess.run(
            ["bash", str(aef_task_test_script)],
            capture_output=True,
            text=True,
            check=False,
        )

        print(result.stdout)
        if result.returncode != 0:
            print(
                f"AEF Task strategy script failed with exit code {result.returncode}",
                file=sys.stderr,
            )
            print(f"Stderr:\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)

        print("AEF Task strategy executed successfully.")

    except FileNotFoundError:
        print("Error: Bash executable not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(
            f"An unexpected error occurred during AEF Task strategy execution: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python execution_strategies.py <project_path> <project_type>",
            file=sys.stderr,
        )
        sys.exit(1)

    project_path = sys.argv[1]
    project_type = sys.argv[2]

    if project_type == "markdown":
        execute_markdown_strategy(project_path)
    elif project_type == "htmlcss":
        execute_htmlcss_strategy(project_path)
    elif project_type == "python":
        execute_python_strategy(project_path)
    elif project_type == "aef_task":
        execute_aef_task_strategy(project_path)
    else:
        print(f"Error: Unknown project type '{project_type}'", file=sys.stderr)
        sys.exit(1)
