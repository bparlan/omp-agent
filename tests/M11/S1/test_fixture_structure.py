#!/usr/bin/env python3
# {Verification IDs: V-FIX-1}
# {Requirement IDs: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5}
# Test Type: SPECIFICATION_CHECK
# Strategy: pytest, using python yaml and json libraries to validate fixture structure.
# All SPECIFICATION_CHECK tests must pass on a blank codebase (exit 0).

import yaml
from pathlib import Path

def test_env_detection_fixture():
    """Validate env_detection.yml fixture structure for FR-1.1."""
    fixture_path = Path("tests/M11/test_fixtures/env_detection.yml")
    assert fixture_path.exists(), f"Fixture file missing: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Verify fixture contract structure
    assert isinstance(data, dict), "Fixture must be a YAML mapping"
    assert "env_detection" in data, "Fixture must contain 'env_detection' key"

    fixture_contract = data["env_detection"]
    assert isinstance(fixture_contract, dict), "Fixture contract must be a mapping"
    assert "test_cases" in fixture_contract, "Fixture contract must contain 'test_cases'"

    test_cases = fixture_contract["test_cases"]
    assert isinstance(test_cases, list), "test_cases must be a list"
    assert len(test_cases) == 5, f"Expected 5 test cases, got {len(test_cases)}"

    for i, tc in enumerate(test_cases):
        assert isinstance(tc, dict), f"Test case {i} must be a mapping"
        assert "name" in tc, f"Test case {i} must contain 'name'"
        assert "project" in tc, f"Test case {i} must contain 'project'"
        assert "expected_runtime" in tc, f"Test case {i} must contain 'expected_runtime'"
        assert "expected_tools" in tc, f"Test case {i} must contain 'expected_tools'"
        assert "threshold" in tc, f"Test case {i} must contain 'threshold'"

        assert isinstance(tc["name"], str), f"Test case {i} name must be string"
        assert isinstance(tc["project"], str), f"Test case {i} project must be string"
        assert isinstance(tc["expected_runtime"], str), f"Test case {i} expected_runtime must be string"
        assert isinstance(tc["expected_tools"], list), f"Test case {i} expected_tools must be list"
        assert isinstance(tc["threshold"], (int, float)), f"Test case {i} threshold must be number"
        assert 0.0 <= tc["threshold"] <= 1.0, f"Test case {i} threshold must be between 0 and 1"

def test_mise_config_fixture():
    """Validate mise_config.yml fixture structure for FR-1.2."""
    fixture_path = Path("tests/M11/test_fixtures/mise_config.yml")
    assert fixture_path.exists(), f"Fixture file missing: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "Fixture must be a YAML mapping"
    assert "mise_config_validation" in data, "Fixture must contain 'mise_config_validation' key"

    fixture_contract = data["mise_config_validation"]
    assert isinstance(fixture_contract, dict), "Fixture contract must be a mapping"
    assert "test_cases" in fixture_contract, "Fixture contract must contain 'test_cases'"

    test_cases = fixture_contract["test_cases"]
    assert isinstance(test_cases, list), "test_cases must be a list"
    assert len(test_cases) == 3, f"Expected 3 test cases, got {len(test_cases)}"

    for i, tc in enumerate(test_cases):
        assert isinstance(tc, dict), f"Test case {i} must be a mapping"
        assert "name" in tc, f"Test case {i} must contain 'name'"
        assert "config" in tc, f"Test case {i} must contain 'config'"
        assert "should_pass" in tc, f"Test case {i} must contain 'should_pass'"

        assert isinstance(tc["name"], str), f"Test case {i} name must be string"
        assert isinstance(tc["config"], dict), f"Test case {i} config must be a mapping"
        assert isinstance(tc["should_pass"], bool), f"Test case {i} should_pass must be boolean"

def test_env_detection_pre_task_fixture():
    """Validate env_detection_pre_task.yml fixture structure for FR-1.3."""
    fixture_path = Path("tests/M11/test_fixtures/env_detection_pre_task.yml")
    assert fixture_path.exists(), f"Fixture file missing: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "Fixture must be a YAML mapping"
    assert "env_detection_pre_task" in data, "Fixture must contain 'env_detection_pre_task' key"

    fixture_contract = data["env_detection_pre_task"]
    assert isinstance(fixture_contract, dict), "Fixture contract must be a mapping"
    assert "test_cases" in fixture_contract, "Fixture contract must contain 'test_cases'"

    test_cases = fixture_contract["test_cases"]
    assert isinstance(test_cases, list), "test_cases must be a list"
    assert len(test_cases) == 2, f"Expected 2 test cases, got {len(test_cases)}"

    for i, tc in enumerate(test_cases):
        assert isinstance(tc, dict), f"Test case {i} must be a mapping"
        assert "name" in tc, f"Test case {i} must contain 'name'"
        assert "project" in tc, f"Test case {i} must contain 'project'"
        assert "runtime" in tc, f"Test case {i} must contain 'runtime'"
        assert "expected_detection_result" in tc, f"Test case {i} must contain 'expected_detection_result'"
        assert "should_pass" in tc, f"Test case {i} must contain 'should_pass'"

        assert isinstance(tc["name"], str), f"Test case {i} name must be string"
        assert isinstance(tc["project"], str), f"Test case {i} project must be string"
        assert isinstance(tc["runtime"], str), f"Test case {i} runtime must be string"
        assert isinstance(tc["expected_detection_result"], dict), f"Test case {i} expected_detection_result must be a mapping"
        assert isinstance(tc["should_pass"], bool), f"Test case {i} should_pass must be boolean"

def test_workspace_isolation_fixture():
    """Validate workspace_isolation.yml fixture structure for FR-1.4."""
    fixture_path = Path("tests/M11/test_fixtures/workspace_isolation.yml")
    assert fixture_path.exists(), f"Fixture file missing: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "Fixture must be a YAML mapping"
    assert "workspace_isolation" in data, "Fixture must contain 'workspace_isolation' key"

    fixture_contract = data["workspace_isolation"]
    assert isinstance(fixture_contract, dict), "Fixture contract must be a mapping"
    assert "test_cases" in fixture_contract, "Fixture contract must contain 'test_cases'"

    test_cases = fixture_contract["test_cases"]
    assert isinstance(test_cases, list), "test_cases must be a list"
    assert len(test_cases) == 2, f"Expected 2 test cases, got {len(test_cases)}"

    for i, tc in enumerate(test_cases):
        assert isinstance(tc, dict), f"Test case {i} must be a mapping"
        assert "name" in tc, f"Test case {i} must contain 'name'"
        assert "project" in tc, f"Test case {i} must contain 'project'"
        assert "runtime" in tc, f"Test case {i} must contain 'runtime'"
        assert "should_pass" in tc, f"Test case {i} must contain 'should_pass'"

        assert isinstance(tc["name"], str), f"Test case {i} name must be string"
        assert isinstance(tc["project"], str), f"Test case {i} project must be string"
        assert isinstance(tc["runtime"], str), f"Test case {i} runtime must be string"
        assert isinstance(tc["should_pass"], bool), f"Test case {i} should_pass must be boolean"

def test_cross_language_runtime_fixture():
    """Validate cross_language_runtime.yml fixture structure for FR-1.5."""
    fixture_path = Path("tests/M11/test_fixtures/cross_language_runtime.yml")
    assert fixture_path.exists(), f"Fixture file missing: {fixture_path}"

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert isinstance(data, dict), "Fixture must be a YAML mapping"
    assert "cross_language_runtime" in data, "Fixture must contain 'cross_language_runtime' key"

    fixture_contract = data["cross_language_runtime"]
    assert isinstance(fixture_contract, dict), "Fixture contract must be a mapping"
    assert "test_cases" in fixture_contract, "Fixture contract must contain 'test_cases'"

    test_cases = fixture_contract["test_cases"]
    assert isinstance(test_cases, list), "test_cases must be a list"
    assert len(test_cases) == 2, f"Expected 2 test cases, got {len(test_cases)}"

    for i, tc in enumerate(test_cases):
        assert isinstance(tc, dict), f"Test case {i} must be a mapping"
        assert "name" in tc, f"Test case {i} must contain 'name'"
        assert "project" in tc, f"Test case {i} must contain 'project'"
        assert "from_runtime" in tc, f"Test case {i} must contain 'from_runtime'"
        assert "to_runtime" in tc, f"Test case {i} must contain 'to_runtime'"
        assert "should_pass" in tc, f"Test case {i} must contain 'should_pass'"

        assert isinstance(tc["name"], str), f"Test case {i} name must be string"
        assert isinstance(tc["project"], str), f"Test case {i} project must be string"
        assert isinstance(tc["from_runtime"], str), f"Test case {i} from_runtime must be string"
        assert isinstance(tc["to_runtime"], str), f"Test case {i} to_runtime must be string"
        assert isinstance(tc["should_pass"], bool), f"Test case {i} should_pass must be boolean"

def test_all_fixtures_exist():
    """Ensure all required fixture files exist."""
    fixtures_dir = Path("tests/M11/test_fixtures")
    assert fixtures_dir.exists(), f"Fixtures directory missing: {fixtures_dir}"

    required_fixtures = [
        "env_detection.yml",
        "mise_config.yml",
        "env_detection_pre_task.yml",
        "workspace_isolation.yml",
        "cross_language_runtime.yml",
    ]

    for fixture_name in required_fixtures:
        fixture_path = fixtures_dir / fixture_name
        assert fixture_path.exists(), f"Required fixture file missing: {fixture_name}"

if __name__ == "__main__":
    tests = [
        test_all_fixtures_exist,
        test_env_detection_fixture,
        test_mise_config_fixture,
        test_env_detection_pre_task_fixture,
        test_workspace_isolation_fixture,
        test_cross_language_runtime_fixture,
    ]

    failed = []
    for test_func in tests:
        try:
            test_func()
            print(f"PASS: {test_func.__name__}")
        except AssertionError as e:
            failed.append(f"{test_func.__name__}: {e}")
            print(f"FAIL: {test_func.__name__}: {e}")

    if failed:
        print("\n".join(failed))
        exit(1)
    exit(0)