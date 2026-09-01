#!/usr/bin/env python3
"""Verification hook for graph-context tasks.
Takes a declared file scope and verifies that only those files were modified.
Optionally uses graph-based verification to check reachability via IMPORTS edges.
"""

import sys
import subprocess
import re
from pathlib import Path


def get_graph_path():
    """Get the path to the graph file from command-line arguments.
    Default: .omp/graph/<project-name>.lbug relative to project root.
    """
    if "--graph-path" in sys.argv:
        idx = sys.argv.index("--graph-path")
        if idx + 1 < len(sys.argv):
            return Path(sys.argv[idx + 1])
    # Walk up from cwd to find project root (where .git exists)
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".git").exists() or (parent / ".omp").exists():
            graph_dir = parent / ".omp" / "graph"
            if graph_dir.exists():
                lbug_files = list(graph_dir.glob("*.lbug"))
                if lbug_files:
                    return lbug_files[0]
            # Fall back to project-name.lbug
            project_name = parent.name
            return graph_dir / f"{project_name}.lbug"
    return Path.cwd() / "graph.lbug"


def get_declared_scope():
    """Get the declared file scope from command-line arguments.
    Format: --scope file1.py,file2.py,dir1/
    """
    scope_str = sys.argv[1] if len(sys.argv) > 1 else ""
    if not scope_str.startswith("--scope="):
        print("ERROR: Must provide --scope=file1.py,file2.py")
        sys.exit(1)

    # Extract scope after --scope=
    scope_files = scope_str[8:].split(",")
    return set(scope_files)


def normalize_path(path):
    """Normalize a file path to a consistent format."""
    return str(Path(path).resolve())


def get_modified_files():
    """Get list of files modified or staged in git."""
    try:
        # Get modified files
        result = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, check=False
        )
        modified = set()
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                modified.add(line[2:].strip())

        # Get staged files (added but not yet committed)
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line:
                # Status is first character, filename starts after space
                parts = line.split(None, 1)
                if len(parts) == 2:
                    modified.add(parts[1])

        return modified
    except Exception:
        return set()


def check_graph_reachability(declared_scope, modified_files, graph_path):
    """Check if modified files are reachable from declared scope via graph."""
    if not declared_scope or not modified_files:
        return False

    scope_files_normalized = [normalize_path(f) for f in declared_scope]

    # Add scope files themselves as reachable (modifying scope file is always allowed)
    reachable_files = set(scope_files_normalized)

    # Build scope filter and collect directory children for all scope entries
    for scope_file in scope_files_normalized:
        scope_path = Path(scope_file).resolve()
        if scope_path.is_dir():
            # All files directly in the directory are reachable
            for child in scope_path.iterdir():
                if child.is_file():
                    reachable_files.add(str(child.resolve()))

    # Query graph for files reachable via IMPORTS from scope files/dirs
    scope_filters = []
    for scope_file in scope_files_normalized:
        scope_path = Path(scope_file).resolve()
        if scope_path.is_dir():
            for child in scope_path.iterdir():
                if child.is_file():
                    scope_filters.append(f"a.path = '{child.resolve()}'")
        elif scope_path.is_file():
            scope_filters.append(f"a.path = '{scope_path}'")

    if scope_filters:
        scope_filter = " OR ".join(scope_filters)
        dir_cypher = f"""MATCH (a:File)
MATCH (a)-[r]->(b:File)
WHERE {scope_filter}
RETURN DISTINCT b.path AS reachable_file"""

        try:
            import ladybug

            db = ladybug.Database(str(graph_path))
            conn = ladybug.Connection(db)
            result = conn.execute(dir_cypher)
            while result.has_next():
                row = result.get_next()
                if row and row[0]:
                    reachable_files.add(row[0])
        except ImportError:
            # Fall back to lbug CLI
            result = subprocess.run(
                ["lbug", str(graph_path)],
                input=dir_cypher,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if line.startswith("│"):
                        parts = line.split("│")
                        if len(parts) >= 2:
                            file_path = parts[1].strip()
                            if file_path and file_path not in [
                                "STRING",
                                "BOOLEAN",
                                "INTEGER",
                                "FLOAT",
                                "reachable_file",
                            ]:
                                reachable_files.add(file_path)
        except Exception:
            pass

    # Check if all modified files are reachable
    for modified_file in modified_files:
        normalized = normalize_path(modified_file)
        if normalized not in reachable_files:
            print(f"\nFAILURE: Modified file not reachable from scope: {modified_file}")
            print(f"Reachable files from scope: {reachable_files}")
            return False

    print(
        "\nSUCCESS: All modified files are reachable from declared scope via IMPORTS graph"
    )
    return True


def check_scope_compliance(declared_scope, modified_files):
    outside_scope = []
    declared_normalized = {normalize_path(f) for f in declared_scope}

    for modified_file in modified_files:
        normalized = normalize_path(modified_file)
        mod_path = Path(modified_file).resolve()

        is_in_scope = False
        for scope_file in declared_normalized:
            scope_resolved = Path(scope_file).resolve()

            if normalized == scope_file:
                is_in_scope = True
                break
            if scope_resolved.is_dir() and str(mod_path).startswith(
                str(scope_resolved) + "/"
            ):
                is_in_scope = True
                break

        if not is_in_scope:
            outside_scope.append(modified_file)

    return outside_scope


def main():
    """Main verification logic."""
    # Check for --graph flag to enable graph-based verification
    use_graph = "--graph" in sys.argv

    # Get declared scope
    declared_scope = get_declared_scope()
    print(f"Declared scope: {sorted(declared_scope)}")

    # Get modified files
    modified_files = get_modified_files()
    print(f"Modified files: {sorted(modified_files) if modified_files else '(none)'}")

    # Exclude graph database files from modified set
    modified_files = {
        f for f in modified_files if not re.search(r"\.omp/graph/.*\.lbug$", f)
    }

    # If no files modified, this is a pass
    if not modified_files:
        print("SUCCESS: No files modified - verification passes")
        sys.exit(0)

    # Check scope compliance
    outside_scope = check_scope_compliance(declared_scope, modified_files)

    if outside_scope:
        print("\nFAILURE: Diff touches files outside declared scope:")
        for file in sorted(outside_scope):
            print(f"  - {file}")
        sys.exit(1)

    # If graph verification is enabled, perform graph-based check
    if use_graph:
        print("\nRunning graph-based verification...")
        graph_reachable = check_graph_reachability(
            declared_scope, modified_files, get_graph_path()
        )
        if not graph_reachable:
            print(
                "\nFAILURE: Graph-based verification failed - modified files not reachable from scope"
            )
            sys.exit(1)
        else:
            print(
                "\nSUCCESS: All modified files are reachable from declared scope via IMPORTS graph"
            )
            sys.exit(0)
    else:
        print("\nSUCCESS: All modified files are within declared scope")
        sys.exit(0)


if __name__ == "__main__":
    main()
