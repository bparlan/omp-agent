import sys
import tempfile
import os

# Set up path
sys.path.insert(0, '/Users/bparlan/devcode/aef/agent')

from core.validation import validate_metadata

# Create test artifact with missing keys
with tempfile.TemporaryDirectory() as tmpdir:
    artifact_path = os.path.join(tmpdir, "test_artifact.md")
    content = """---
title: Test Artifact
content: Some content
---
Actual artifact content.
"""
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Testing artifact at: {artifact_path}")
    print(f"File exists: {os.path.exists(artifact_path)}")

    # Test validate_metadata
    result = validate_metadata(artifact_path)
    print(f"Result: {result}")

    # Check if result indicates missing fields
    if not result.get("valid"):
        print(f"SUCCESS: Function correctly returned valid=false")
        missing_fields = result.get("missing_fields", [])
        print(f"Missing fields: {missing_fields}")

        # Check if required fields are in missing_fields
        required = {"id", "type", "title", "milestone_id", "status", "derived_from", "template_version", "metadata"}
        found = {field.split(".")[-1] for field in missing_fields}

        print(f"Expected required: {required}")
        print(f"Found in missing_fields: {found}")

        if required.issubset(found):
            print("SUCCESS: All required fields correctly reported as missing")
        else:
            print("FAIL: Not all required fields are in missing_fields")
    else:
        print(f"FAIL: Function returned valid=true when it should be valid=false")
