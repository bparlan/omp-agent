#!/usr/bin/env python3
"""Check graph schema using Ladybug Python client."""

import ladybug
import json

db = ladybug.Database("/Users/bparlan/devcode/BariaDAO/.omp/graph/baria.lbug")
conn = ladybug.Connection(db)

result = conn.execute("CALL show_tables() RETURN *;")
tables = []
type_names = []

while result.has_next():
    row = result.get_next()
    tables.append(row)
    # Row is a list: [id, name, type, database_name, comment]
    _, name, type_, _, _ = row
    if type_ in ("NODE", "REL"):
        type_val = type_.split()[0]
        type_names.append(name)

type_names = sorted(set(type_names))

manifest = {
    "project_name": "baria",
    "graph_file": ".omp/graph/baria.lbug",
    "schema_version": "V1",
    "node_types": type_names,
    "created_at": "2026-07-25T18:30:00Z",
}

print(json.dumps(manifest, indent=2))
