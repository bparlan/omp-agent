#!/usr/bin/env bash
# Check graph schema using embedded Python

python3 <<'PYEOF'
import json
import subprocess

# Run lbug via subprocess and capture structured output
result = subprocess.run(
    ['lbug', '/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug'],
    input='CALL show_tables() RETURN *;',
    capture_output=True,
    text=True
)

lines = result.stdout.split('\n')
tables = []
types = []

for line in lines:
    line = line.strip()
    # Skip headers and separators
    if 'id' in line.lower() or 'type' in line.lower() or line.startswith('┌') or line.startswith('├') or line.startswith('└'):
        continue
    # Skip pipeline messages
    if 'PIPELINES' in line or 'Pipeline' in line:
        continue
    # Skip empty lines
    if not line:
        continue
    # Extract data rows
    if line.startswith('│'):
        parts = line.split('│')
        if len(parts) >= 5:
            name = parts[1].strip()
            type_ = parts[2].strip()
            tables.append({'name': name, 'type': type_})
            if type_ in ('NODE', 'REL'):
                type_val = type_.split(' ')[1] if ' ' in type_ else type_
                types.append(type_val)

all_types = sorted(set(types))

manifest = {
    "project_name": "baria",
    "graph_file": ".omp/graph/baria.lbug",
    "schema_version": "V1",
    "node_types": all_types,
    "created_at": "2026-07-25T18:30:00Z"
}

print(json.dumps(manifest, indent=2))
PYEOF
