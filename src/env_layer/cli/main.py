"""
Environment Layer CLI Main Entry Point
Provides unified interface for all environment layer commands
"""
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation.schema_validator import SchemaValidator
from cli.env_check import main as env_check_main
from cli.env_detect import main as env_detect_main
from cli.mise_validate import main as mise_validate_main
from cli.workspace_cli import main as workspace_cli_main
from cli.handlers.validation import handle_validate_schema, handle_validate_fixtures

def main():
    """Main CLI entry point for environment layer"""
    if len(sys.argv) < 2:
        print("Environment Layer CLI")
        print("Available commands:")
        print("  env-check   Check environment status and validation")
        print("  env-detect  Detect environment for a project")
        print("  mise-validate    Validate .mise.toml configuration")
        print("  workspace-cli    Manage workspace isolation")
        print("  validate-schema  Validate schema contracts")
        print("  validate-fixtures Validate test fixtures")
        print("")
        print("Use '<command> --help' for command-specific help")
        sys.exit(1)

    command = sys.argv[1]

    if command == "env-check":
        env_check_main()
    elif command == "env-detect":
        env_detect_main()
    elif command == "mise-validate":
        mise_validate_main()
    elif command == "workspace-cli":
        workspace_cli_main()
    elif command == "validate-schema":
        handle_validate_schema(sys.argv)
    elif command == "validate-fixtures":
        handle_validate_fixtures(sys.argv)
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  env-check   Check environment status and validation")
        print("  env-detect  Detect environment for a project")
        print("  mise-validate    Validate .mise.toml configuration")
        print("  workspace-cli    Manage workspace isolation")
        print("  validate-schema  Validate schema contracts")
        print("  validate-fixtures Validate test fixtures")
        sys.exit(1)

if __name__ == "__main__":
    main()