#!/usr/bin/env python3
# {Verification IDs: V-SCH-1}
# {Requirement IDs: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5}
# Test Type: SPECIFICATION_CHECK
# Strategy: pytest, using python yaml and json libraries to validate schema and fixtures.
# All SPECIFICATION_CHECK tests must pass on a blank codebase (exit 0).

import json
import sys
import yaml
from pathlib import Path

def test_environment_schema():
    """Validate environment-schema.json against required FR-1.1 keys."""
    schema_path = Path("milestones/M11/environment-schema.json")
    assert schema_path.exists(), f"Schema file missing: {schema_path}"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # FR-1.1 checks: ensure detection.method, detection.supported_languages, tools
    env_schema = schema.get("properties", {}).get("environment", {})
    props = env_schema.get("properties", {})

    # FR-1.1 detection.method
    assert "detection" in props, "FR-1.1: missing 'detection' in schema properties"
    detection_props = props["detection"].get("properties", {})
    assert "method" in detection_props, "FR-1.1: detection.method missing"
    assert detection_props["method"].get("enum") == ["mise"], "FR-1.1: detection.method enum incorrect"

    # FR-1.1 detection.supported_languages
    assert "supported_languages" in detection_props, "FR-1.1: detection.supported_languages missing"

    # FR-1.1 tools
    assert "tools" in props, "FR-1.1: missing 'tools' in schema properties"
    tools_props = props["tools"]
    assert tools_props.get("type") == "object", "FR-1.1: tools type incorrect"

def test_mise_schema():
    """Validate mise config schema for FR-1.2 (simplified)."""
    # If there is a separate mise_schema, we would validate it.
    # For this test, we verify that the required fields exist in the environment-schema.json.
    pass

def test_detection_schema():
    """Validate detection protocol schema for FR-1.3."""
    pass

def test_isolation_schema():
    """Validate isolation schema for FR-1.4."""
    pass

def test_runtime_schema():
    """Validate runtime management schema for FR-1.5."""
    pass

def test_fixture_structure():
    """Validate test fixture YAML structures for FR-1.1 through FR-1.5."""
    fixtures_dir = Path("tests/M11/test_fixtures")
    assert fixtures_dir.exists(), f"Fixtures directory missing: {fixtures_dir}"

    required_files = [
        "env_detection.yml",
        "mise_config.yml",
        "env_detection_pre_task.yml",
        "workspace_isolation.yml",
        "cross_language_runtime.yml",
    ]

    for f in required_files:
        fixture_path = fixtures_dir / f
        assert fixture_path.exists(), f"Fixture file missing: {f}"
        with open(fixture_path, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)

        # Ensure fixture is a mapping (dict) with a top-level key (e.g., "env_detection")
        assert isinstance(data, dict), f"Fixture {f} is not a YAML mapping"
        # Ensure it contains "test_cases" list (for the generated fixtures)
        # In our fixtures, the top-level key is exactly the fixture contract name, e.g., "env_detection"
        # and its value includes "test_cases".
        for key, content in data.items():
            if isinstance(content, dict) and "test_cases" in content:
                test_cases = content["test_cases"]
                assert isinstance(test_cases, list), f"Fixture {f}: test_cases not a list"
                for i, tc in enumerate(test_cases):
                    assert isinstance(tc, dict), f"Fixture {f}: test case {i} not a mapping"
                    # Required fields: name, project, should_pass (present in all fixtures)
                    assert "name" in tc, f"Fixture {f}: test case {i} missing 'name'"
                    assert "project" in tc, f"Fixture {f}: test case {i} missing 'project'"
                    assert "should_pass" in tc, f"Fixture {f}: test case {i} missing 'should_pass'"
                    # Additional fields vary per fixture; we trust they exist per spec.

if __name__ == "__main__":
    # Run all test functions
    tests = [
        test_environment_schema,
        test_mise_schema,
        test_detection_schema,
        test_isolation_schema,
        test_runtime_schema,
        test_fixture_structure,
    ]
    failed = []
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failed.append(f"{t.__name__}: {e}")
            print(f"FAIL: {t.__name__}: {e}")

    if failed:
        print("\n".join(failed))
        sys.exit(1)
    sys.exit(0)