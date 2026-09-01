#!/usr/bin/env python3
"""Ingest skeleton.md into Ladybug graph - outputs only Cypher statements."""

import sys
import re

try:
    import yaml
except ImportError:
    import yaml


def parse_skeleton(skeleton_path):
    """Parse skeleton.md using PyYAML."""
    with open(skeleton_path, "r") as f:
        content = f.read()

    data = yaml.safe_load(content) or {}

    files = []
    imports = []

    if isinstance(data, dict) and "files" in data:
        files_data = data["files"]
    elif isinstance(data, list):
        files_data = data
    else:
        raise ValueError("Skeleton file must contain files")

    imports_data = data.get("imports", []) if data.get("imports") is not None else []

    for file_data in files_data:
        file_path = file_data.get("path", "")
        file_name = file_data.get("name", "")
        language = file_data.get("language", "python")
        symbols = []
        file_imports = []

        if isinstance(file_data, dict):
            symbols_data = file_data.get("symbols", [])
            file_imports_data = file_data.get("imports", [])

            for symbol_data in symbols_data:
                if isinstance(symbol_data, dict):
                    symbols.append(
                        {
                            "name": symbol_data.get("name", ""),
                            "kind": symbol_data.get("kind", "unknown"),
                            "line": symbol_data.get("line", 0),
                        }
                    )

            for imp_data in file_imports_data:
                if isinstance(imp_data, dict):
                    to_field = imp_data.get("to", "")
                    if to_field:
                        match = re.match(
                            r"^(?:from\s+(\S+)\s+import|import\s+(\S+))", to_field
                        )
                        if match:
                            module = match.group(1) or match.group(2)
                            file_imports.append(
                                {
                                    "from": module,
                                    "to": module,
                                    "import_statement": to_field,
                                }
                            )

        files.append(
            {
                "path": file_path,
                "name": file_name,
                "language": language,
                "symbols": symbols,
                "imports": file_imports,
            }
        )

    for imp_data in imports_data:
        if isinstance(imp_data, dict):
            to_field = imp_data.get("to", "")
            if to_field:
                match = re.match(r"^(?:from\s+(\S+)\s+import|import\s+(\S+))", to_field)
                if match:
                    module = match.group(1) or match.group(2)
                    imports.append(
                        {"from": module, "to": module, "import_statement": to_field}
                    )
    file_paths = {f["path"] for f in data.get("files", [])}

    for imp in imports:
        module = imp["from"]
        project_path = get_project_local_path(module)
        if project_path and project_path in file_paths:
            # Create edges from all files in the graph to the imported file
            # This models that all files import these common dependencies
            dest_path = project_path.replace("'", "''")
            for file in skeleton_data["files"]:
                source_path = file["path"].replace("'", "''")
                statements.append(
                    f"MERGE (a:File {{path: '{source_path}'}}) MERGE (b:File {{path: '{dest_path}'}}) CREATE (a)-[:IMPORTS]->(b)"
                )

    return {"files": files, "imports": imports}


def get_project_local_path(module):
    """Convert a Python module path to a file path."""
    if module.startswith("src."):
        parts = module.split(".")
        if len(parts) == 2:  # src.data
            return f"/Users/bparlan/devcode/BariaDAO/src/{parts[1]}.py"
        elif len(parts) == 3:  # src.data.content_loader
            return f"/Users/bparlan/devcode/BariaDAO/src/{parts[1]}/{parts[2]}.py"
    return None


def generate_cypher(skeleton_data):
    """Generate Cypher statements for graph nodes and edges."""
    statements = []

    # Create File nodes for all files in skeleton
    for file in skeleton_data["files"]:
        statements.append(f"MERGE (f:File {{path: '{file['path']}'}})")

    # Create Symbol nodes for each symbol with line number
    # Using id, name, kind, file, line properties to match lbug database schema
    for file in skeleton_data["files"]:
        for symbol in file.get("symbols", []):
            name = symbol.get("name", "")
            kind = symbol.get("kind", "unknown")
            file_name = file["name"]
            node_id = f"{file_name}:{name}"
            file_path = file["path"].replace("'", "''")
            statements.append(
                f"MERGE (s:Symbol {{id: '{node_id}', name: '{name}', kind: '{kind}', file: '{file_path}', line: {symbol.get('line', 0)}}})"
            )

    # Collect all File paths
    file_paths = {f["path"] for f in skeleton_data["files"]}

    # Process file-level imports - ONLY project-local imports
    for file in skeleton_data["files"]:
        for imp in file.get("imports", []):
            module = imp["from"]
            import_statement = imp["to"]

            # Check if this is a project-local import
            project_path = get_project_local_path(module)
            if project_path and project_path in file_paths:
                # Use the full file path for both source and destination
                source_path = file["path"].replace("'", "''")
                dest_path = project_path.replace("'", "''")
                statements.append(
                    f"MERGE (a:File {{path: '{source_path}'}}) MERGE (b:File {{path: '{dest_path}'}}) CREATE (a)-[:IMPORTS]->(b)"
                )

    # Process global imports (if any)
    for imp in skeleton_data.get("imports", []):
        module = imp["from"]
        import_statement = imp["to"]

        project_path = get_project_local_path(module)
        if project_path and project_path in file_paths:
            # Use the full file path for both source and destination
            source_path = project_path.replace("'", "''")
            dest_path = project_path.replace("'", "''")
            statements.append(
                f"MERGE (a:File {{path: '{source_path}'}}) MERGE (b:File {{path: '{dest_path}'}}) CREATE (a)-[:IMPORTS]->(b)"
            )

    return statements


if __name__ == "__main__":
    skeleton_path = sys.argv[1]

    skeleton_data = parse_skeleton(skeleton_path)

    # Generate and output Cypher statements only
    for stmt in generate_cypher(skeleton_data):
        print(stmt)
