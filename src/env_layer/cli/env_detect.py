"""
Environment detection CLI implementation for env-detect command
"""
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

from env_layer.core.detector import EnvironmentDetector

def main():
    parser = argparse.ArgumentParser(description="Pre-task environment detection")
    parser.add_argument("--project", required=True, help="Project path")
    parser.add_argument("--runtime", required=True, help="Runtime type (python, node, rust, go, deno)")
    parser.add_argument("--task", help="Task name for pre-task detection")
    parser.add_argument("--cache", action="store_true", help="Use cached detection results")
    parser.add_argument("--output", help="Output file for results")
    parser.add_argument("--format", choices=["json", "yaml"], default="json", help="Output format")

    args = parser.parse_args()

    project_path = Path(args.project)
    if not project_path.exists():
        print(f"Error: Project path '{project_path}' does not exist")
        exit(1)

    # Initialize detector with project path
    detector = EnvironmentDetector(project_path)

    # Perform environment detection
    result = detector.detect(
        runtime=args.runtime,
        task=args.task,
        use_cache=args.cache
    )

    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == "yaml":
                import yaml
                f.write(yaml.dump(result, default_flow_style=False))
            else:
                json.dump(result, f, indent=2)

    # Print results to stdout
    if args.format == "yaml":
        import yaml
        print(yaml.dump(result, default_flow_style=False))
    else:
        print(json.dumps(result, indent=2))

    exit(0 if result["status"] in ["success", "partial"] else 1)

if __name__ == "__main__":
    main()