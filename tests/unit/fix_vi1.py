#!/usr/bin/env python3
import sys
import os
import tempfile

# Import with the correct path
sys.path.insert(0, "/Users/bparlan/devcode/aef/agent")
sys.path.insert(0, "/Users/bparlan/devcode/aef/agent/core")

from core.validation import validate_metadata

# Test the exact scenario from VI-1
with tempfile.TemporaryDirectory() as tmpdir:
    artifact_path = os.path.join(tmpdir, "missing_keys.yaml")
    with open(artifact_path, "w") as f:
        f.write("title: Test Artifact\\ncontent: Some content\\n")

    result = validate_metadata(artifact_path)
    print("VI-1 validation result:", result)

    # Check the key requirements
    missing_fields = result.get("missing_fields", [])
    print("Missing fields count:", len(missing_fields))
    print("Missing fields:", missing_fields)

    # Check what _required_artifact_keys() returns
    from core.validation import _required_artifact_keys

    required_keys = _required_artifact_keys()
    print("Required keys:", required_keys)
    print("Title in required:", "title" in required_keys)
    print("Title in missing_fields:", "title" in missing_fields)
    print(
        "Missing fields should include all required keys except title:",
        all(k in missing_fields for k in required_keys if k != "title"),
    )
