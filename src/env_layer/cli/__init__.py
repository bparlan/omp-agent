"""
Environment Layer CLI Interface
Main entry point for all environment layer commands
"""
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .env_check import main as env_check_main
from .env_detect import main as env_detect_main

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Environment Layer CLI")
        print("Available commands:")
        print("  env-check   Check environment status and validation")
        print("  env-detect  Detect environment for a project")
        print("")
        print("Use 'env-check --help' or 'env-detect --help' for command-specific help")
        sys.exit(1)

    command = sys.argv[1]

    if command == "env-check":
        env_check_main()
    elif command == "env-detect":
        env_detect_main()
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  env-check   Check environment status and validation")
        print("  env-detect  Detect environment for a project")
        sys.exit(1)