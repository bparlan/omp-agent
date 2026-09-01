"""
Handlers for validation CLI commands.

Implements the observable contracts for:
- validate-schema
- validate-fixtures
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


def handle_validate_schema(args):
    """Implement validate-schema --schema <type> --input <path>."""
    schema_type = args.schema
    input_path = Path(args.input)

    # Basic validation
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load and validate schema based on type
    validation_result = validate_schema_by_type(schema_type, input_path)

    # Output results
    output_json = getattr(args, "json", False)
    if output_json:
        print(json.dumps(validation_result, indent=2))
    else:
        print(f"Schema validation for {schema_type}")
        print(f"Input file: {input_path}")
        print(f"Status: {'VALID' if validation_result['valid'] else 'INVALID'}")

        if "errors" in validation_result:
            print(f"Errors ({len(validation_result['errors'])}):")
            for error in validation_result["errors"]:
                print(f"  ✗ {error}")

        if "warnings" in validation_result:
            print(f"Warnings ({len(validation_result['warnings'])}):")
            for warning in validation_result["warnings"]:
                print(f"  ⚠ {warning}")

    sys.exit(0 if validation_result["valid"] else 1)


def handle_validate_fixtures(args):
    """Implement validate-fixtures --fixture <path>."""
    fixture_path = Path(args.fixture)

    # Basic validation
    if not fixture_path.exists():
        print(f"Error: Fixture file does not exist: {fixture_path}", file=sys.stderr)
        sys.exit(1)

    # Load and validate fixture
    fixture_result = validate_fixture_file(fixture_path)

    # Output results
    output_json = getattr(args, "json", False)
    if output_json:
        print(json.dumps(fixture_result, indent=2))
    else:
        print(f"Fixture validation for {fixture_path.name}")
        print(f"Status: {'VALID' if fixture_result['valid'] else 'INVALID'}")

        if "errors" in fixture_result:
            print(f"Errors ({len(fixture_result['errors'])}):")
            for error in fixture_result["errors"]:
                print(f"  ✗ {error}")

        if "warnings" in fixture_result:
            print(f"Warnings ({len(fixture_result['warnings'])}):")
            for warning in fixture_result["warnings"]:
                print(f"  ⚠ {warning}")

    sys.exit(0 if fixture_result["valid"] else 1)


def validate_schema_by_type(schema_type: str, input_path: Path) -> Dict[str, Any]:
    """Validate schema based on type."""
    result = {
        "schema_type": schema_type,
        "input_file": str(input_path),
        "valid": False,
        "errors": [],
        "warnings": [],
    }

    try:
        with open(input_path, "r") as f:
            content = f.read()

        # Parse JSON content
        data = json.loads(content)

        # Basic validation based on schema type
        if schema_type == "environment":
            result.update(validate_environment_schema(data))
        elif schema_type == "mise":
            result.update(validate_mise_schema(data))
        elif schema_type == "detection":
            result.update(validate_detection_schema(data))
        elif schema_type == "workspace":
            result.update(validate_workspace_schema(data))
        elif schema_type == "runtime":
            result.update(validate_runtime_schema(data))
        else:
            result["errors"].append(f"Unknown schema type: {schema_type}")

    except json.JSONDecodeError as e:
        result["errors"].append(f"Invalid JSON: {e}")
    except Exception as e:
        result["errors"].append(f"Validation error: {e}")

    return result


def validate_environment_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate environment schema."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    # Required fields based on FR-1.1 specification
    required_fields = ["detection", "isolation"]

    for field in required_fields:
        if field not in data:
            result["errors"].append(f"Missing required field: {field}")
            result["valid"] = False

    # Validate detection section
    if "detection" in data:
        detection = data["detection"]
        if "api_version" not in detection:
            result["warnings"].append("Missing api_version in detection")

        if "runtime_detection" not in detection:
            result["errors"].append("Missing runtime_detection in detection")
            result["valid"] = False

    # Validate isolation section
    if "isolation" in data:
        isolation = data["isolation"]
        required_isolation_fields = [
            "mode",
            "shared_base",
            "cross_contamination_prevention",
        ]

        for field in required_isolation_fields:
            if field not in isolation:
                result["errors"].append(f"Missing required isolation field: {field}")
                result["valid"] = False

    return result


def validate_mise_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate mise configuration schema."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    # Required fields based on FR-1.2 specification
    required_fields = ["schema_version", "mise_config"]

    for field in required_fields:
        if field not in data:
            result["errors"].append(f"Missing required field: {field}")
            result["valid"] = False

    # Validate mise_config structure
    if "mise_config" in data:
        mise_config = data["mise_config"]
        required_config_fields = ["environment", "tools", "workspace", "cross_language"]

        for field in required_config_fields:
            if field not in mise_config:
                result["warnings"].append(f"Missing mise_config field: {field}")

        # Validate environment sub-schema
        if "environment" in mise_config:
            env = mise_config["environment"]
            if "runtime" not in env:
                result["errors"].append("Missing runtime in environment")
                result["valid"] = False

            if "version" not in env:
                result["errors"].append("Missing version in environment")
                result["valid"] = False
            else:
                # Validate version format
                import re

                version_pattern = r"^([0-9]+)\\.([0-9]+)\\.([0-9]+)([-+][a-zA-Z0-9]+)?$"
                if not re.match(version_pattern, env["version"]):
                    result["warnings"].append(
                        f"Version '{env['version']}' doesn't match semantic version pattern"
                    )

    return result


def validate_detection_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate detection protocol schema."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    if "detection_protocol" not in data:
        result["errors"].append("Missing detection_protocol")
        result["valid"] = False
        return result

    detection_protocol = data["detection_protocol"]

    # Validate pre_task_execution section
    if "pre_task_execution" not in detection_protocol:
        result["warnings"].append("Missing pre_task_execution in detection_protocol")
        return result

    pre_task = detection_protocol["pre_task_execution"]

    # Check required sequence elements
    required_sequence = [
        "project_structure_analysis",
        "runtime_detection",
        "tool_availability_check",
        "compatibility_validation",
        "isolation_setup",
    ]

    if "sequence" not in pre_task:
        result["errors"].append("Missing sequence in pre_task_execution")
        result["valid"] = False
    else:
        sequence = pre_task["sequence"]
        for item in required_sequence:
            if item not in sequence:
                result["errors"].append(f"Missing required sequence element: {item}")
                result["valid"] = False

    return result


def validate_workspace_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate workspace isolation schema."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    if "workspace_isolation" not in data:
        result["errors"].append("Missing workspace_isolation")
        result["valid"] = False
        return result

    workspace = data["workspace_isolation"]

    # Validate structure section
    if "structure" not in workspace:
        result["errors"].append("Missing structure in workspace_isolation")
        result["valid"] = False
    else:
        structure = workspace["structure"]
        required_structure_fields = [
            "base_path",
            "project_prefix",
            "runtime_subdirectory",
        ]

        for field in required_structure_fields:
            if field not in structure:
                result["warnings"].append(f"Missing structure field: {field}")

    # Validate permissions section
    if "permissions" not in workspace:
        result["warnings"].append("Missing permissions in workspace_isolation")
    else:
        permissions = workspace["permissions"]
        if "require_isolation" not in permissions:
            result["warnings"].append("Missing require_isolation in permissions")

    # Validate protection section
    if "protection" not in workspace:
        result["warnings"].append("Missing protection in workspace_isolation")
    else:
        protection = workspace["protection"]
        if "prevent_cross_contamination" not in protection:
            result["warnings"].append(
                "Missing prevent_cross_contamination in protection"
            )

    return result


def validate_runtime_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate runtime management schema."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    if "cross_language_management" not in data:
        result["errors"].append("Missing cross_language_management")
        result["valid"] = False
        return result

    cross_lang = data["cross_language_management"]

    # Validate runtime_switching section
    if "runtime_switching" not in cross_lang:
        result["warnings"].append(
            "Missing runtime_switching in cross_language_management"
        )
    else:
        runtime_switching = cross_lang["runtime_switching"]

        # Check supported_transitions
        if "supported_transitions" not in runtime_switching:
            result["warnings"].append("Missing supported_transitions")
        else:
            transitions = runtime_switching["supported_transitions"]
            # Validate expected transitions
            expected_transitions = [
                "python_to_node",
                "node_to_python",
                "rust_to_go",
                "go_to_rust",
                "deno_to_node",
                "node_to_deno",
            ]

            for transition in expected_transitions:
                if transition not in transitions:
                    result["warnings"].append(
                        f"Missing supported transition: {transition}"
                    )

    # Validate execution_context section
    if "execution_context" not in cross_lang:
        result["warnings"].append(
            "Missing execution_context in cross_language_management"
        )
    else:
        execution_context = cross_lang["execution_context"]
        required_context_fields = [
            "runtime_specific_env",
            "tool_path_isolation",
            "library_conflict_resolution",
            "version_compatibility_matrix",
        ]

        for field in required_context_fields:
            if field not in execution_context:
                result["warnings"].append(f"Missing execution_context field: {field}")

    return result


def validate_fixture_file(fixture_path: Path) -> Dict[str, Any]:
    """Validate fixture file structure and content."""
    result = {
        "fixture_file": str(fixture_path),
        "valid": False,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    try:
        with open(fixture_path, "r") as f:
            content = f.read()

        # Try to parse as YAML
        import yaml

        try:
            fixture_data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            result["errors"].append(f"Invalid YAML: {e}")
            return result

        # Validate fixture structure
        if not fixture_data:
            result["errors"].append("Empty fixture file")
            return result

        # Determine fixture type and validate
        if "env_detection" in fixture_data:
            result.update(validate_env_detection_fixture(fixture_data["env_detection"]))
        elif "mise_config_validation" in fixture_data:
            result.update(
                validate_mise_config_fixture(fixture_data["mise_config_validation"])
            )
        elif "env_detection_pre_task" in fixture_data:
            result.update(
                validate_env_detection_pre_task_fixture(
                    fixture_data["env_detection_pre_task"]
                )
            )
        elif "workspace_isolation" in fixture_data:
            result.update(
                validate_workspace_isolation_fixture(
                    fixture_data["workspace_isolation"]
                )
            )
        elif "cross_language_runtime" in fixture_data:
            result.update(
                validate_cross_language_runtime_fixture(
                    fixture_data["cross_language_runtime"]
                )
            )
        else:
            result["errors"].append(
                "Unknown fixture format - no recognized top-level key"
            )

    except Exception as e:
        result["errors"].append(f"Fixture validation error: {e}")

    return result


def validate_env_detection_fixture(fixture_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate environment detection fixture."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    if "test_cases" not in fixture_data:
        result["errors"].append("Missing test_cases")
        result["valid"] = False
        return result

    test_cases = fixture_data["test_cases"]

    for i, test_case in enumerate(test_cases):
        case_result = {
            "name": test_case.get("name", f"Test case {i}"),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Required fields for environment detection
        required_fields = [
            "name",
            "project",
            "expected_runtime",
            "expected_tools",
            "threshold",
        ]

        for field in required_fields:
            if field not in test_case:
                case_result["errors"].append(f"Missing required field: {field}")
                case_result["valid"] = False

        # Validate threshold range
        if "threshold" in test_case:
            threshold = test_case["threshold"]
            if (
                not isinstance(threshold, (int, float))
                or threshold < 0
                or threshold > 1
            ):
                case_result["errors"].append(
                    f"Invalid threshold value: {threshold}. Must be between 0 and 1"
                )
                case_result["valid"] = False

        # Validate expected_tools is a list
        if "expected_tools" in test_case and not isinstance(
            test_case["expected_tools"], list
        ):
            case_result["errors"].append("expected_tools must be a list")
            case_result["valid"] = False

        case_result["test_case_number"] = i + 1
        result["test_cases"].append(case_result)

        if not case_result["valid"]:
            result["valid"] = False

    return result


def validate_mise_config_fixture(fixture_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate mise configuration fixture."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    if "test_cases" not in fixture_data:
        result["errors"].append("Missing test_cases")
        result["valid"] = False
        return result

    test_cases = fixture_data["test_cases"]

    for i, test_case in enumerate(test_cases):
        case_result = {
            "name": test_case.get("name", f"Test case {i}"),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Required fields for mise config
        required_fields = ["name", "config", "should_pass"]

        for field in required_fields:
            if field not in test_case:
                case_result["errors"].append(f"Missing required field: {field}")
                case_result["valid"] = False

        # Validate config structure
        if "config" in test_case:
            config = test_case["config"]
            if "environment" not in config:
                case_result["errors"].append("Missing environment in config")
                case_result["valid"] = False
            elif "runtime" not in config["environment"]:
                case_result["errors"].append("Missing runtime in environment")
                case_result["valid"] = False
            elif "version" not in config["environment"]:
                case_result["errors"].append("Missing version in environment")
                case_result["valid"] = False

        # Validate should_pass is boolean
        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            case_result["errors"].append("should_pass must be a boolean")
            case_result["valid"] = False

        case_result["test_case_number"] = i + 1
        result["test_cases"].append(case_result)

        if not case_result["valid"]:
            result["valid"] = False

    return result


def validate_env_detection_pre_task_fixture(
    fixture_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate environment detection pre-task fixture."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    if "test_cases" not in fixture_data:
        result["errors"].append("Missing test_cases")
        result["valid"] = False
        return result

    test_cases = fixture_data["test_cases"]

    for i, test_case in enumerate(test_cases):
        case_result = {
            "name": test_case.get("name", f"Test case {i}"),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Required fields for pre-task detection
        required_fields = [
            "name",
            "project",
            "runtime",
            "expected_detection_result",
            "should_pass",
        ]

        for field in required_fields:
            if field not in test_case:
                case_result["errors"].append(f"Missing required field: {field}")
                case_result["valid"] = False

        # Validate expected_detection_result structure
        if "expected_detection_result" in test_case:
            expected_result = test_case["expected_detection_result"]
            required_result_fields = [
                "runtime_detected",
                "tools_found",
                "version",
                "isolation_setup",
            ]

            for field in required_result_fields:
                if field not in expected_result:
                    case_result["errors"].append(
                        f"Missing expected_detection_result field: {field}"
                    )
                    case_result["valid"] = False

            # Validate types
            if "tools_found" in expected_result and not isinstance(
                expected_result["tools_found"], list
            ):
                case_result["errors"].append(
                    "expected_detection_result.tools_found must be a list"
                )
                case_result["valid"] = False

        # Validate should_pass is boolean
        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            case_result["errors"].append("should_pass must be a boolean")
            case_result["valid"] = False

        case_result["test_case_number"] = i + 1
        result["test_cases"].append(case_result)

        if not case_result["valid"]:
            result["valid"] = False

    return result


def validate_workspace_isolation_fixture(
    fixture_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate workspace isolation fixture."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    if "test_cases" not in fixture_data:
        result["errors"].append("Missing test_cases")
        result["valid"] = False
        return result

    test_cases = fixture_data["test_cases"]

    for i, test_case in enumerate(test_cases):
        case_result = {
            "name": test_case.get("name", f"Test case {i}"),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Required fields for workspace isolation
        required_fields = [
            "name",
            "project",
            "runtime",
            "workspace_config",
            "expected_isolation_result",
            "should_pass",
        ]

        for field in required_fields:
            if field not in test_case:
                case_result["errors"].append(f"Missing required field: {field}")
                case_result["valid"] = False

        # Validate workspace_config
        if "workspace_config" in test_case:
            config = test_case["workspace_config"]
            required_config_fields = [
                "mode",
                "shared_base",
                "cross_contamination_prevention",
                "workspace_prefix",
            ]

            for field in required_config_fields:
                if field not in config:
                    case_result["errors"].append(
                        f"Missing workspace_config field: {field}"
                    )
                    case_result["valid"] = False

        # Validate expected_isolation_result
        if "expected_isolation_result" in test_case:
            expected_result = test_case["expected_isolation_result"]
            required_result_fields = [
                "workspace_created",
                "isolation_enforced",
                "cross_contamination_prevented",
                "access_control",
            ]

            for field in required_result_fields:
                if field not in expected_result:
                    case_result["errors"].append(
                        f"Missing expected_isolation_result field: {field}"
                    )
                    case_result["valid"] = False

        # Validate should_pass is boolean
        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            case_result["errors"].append("should_pass must be a boolean")
            case_result["valid"] = False

        case_result["test_case_number"] = i + 1
        result["test_cases"].append(case_result)

        if not case_result["valid"]:
            result["valid"] = False

    return result


def validate_cross_language_runtime_fixture(
    fixture_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate cross-language runtime fixture."""
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "test_cases": [],
    }

    if "test_cases" not in fixture_data:
        result["errors"].append("Missing test_cases")
        result["valid"] = False
        return result

    test_cases = fixture_data["test_cases"]

    for i, test_case in enumerate(test_cases):
        case_result = {
            "name": test_case.get("name", f"Test case {i}"),
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Required fields for cross-language runtime
        required_fields = [
            "name",
            "project",
            "source_runtime",
            "target_runtime",
            "runtime_config",
            "expected_switch_result",
            "should_pass",
        ]

        for field in required_fields:
            if field not in test_case:
                case_result["errors"].append(f"Missing required field: {field}")
                case_result["valid"] = False

        # Validate runtime_config
        if "runtime_config" in test_case:
            config = test_case["runtime_config"]
            required_config_fields = [
                "tool_chain",
                "compatibility_matrix",
                "fallback_strategies",
                "shared_components",
            ]

            for field in required_config_fields:
                if field not in config:
                    case_result["errors"].append(
                        f"Missing runtime_config field: {field}"
                    )
                    case_result["valid"] = False

            # Validate types
            if "tool_chain" in config and not isinstance(config["tool_chain"], list):
                case_result["errors"].append("runtime_config.tool_chain must be a list")
                case_result["valid"] = False

            if "fallback_strategies" in config and not isinstance(
                config["fallback_strategies"], list
            ):
                case_result["errors"].append(
                    "runtime_config.fallback_strategies must be a list"
                )
                case_result["valid"] = False

            if "shared_components" in config and not isinstance(
                config["shared_components"], list
            ):
                case_result["errors"].append(
                    "runtime_config.shared_components must be a list"
                )
                case_result["valid"] = False

        # Validate expected_switch_result
        if "expected_switch_result" in test_case:
            expected_result = test_case["expected_switch_result"]
            # These should be boolean values or booleans
            for field in [
                "switch_successful",
                "runtime_available",
                "tool_compatibility_confirmed",
                "isolation_preserved",
            ]:
                if field not in expected_result:
                    case_result["errors"].append(
                        f"Missing expected_switch_result field: {field}"
                    )
                    case_result["valid"] = False
                elif not isinstance(expected_result[field], bool):
                    case_result["errors"].append(
                        f"expected_switch_result.{field} must be a boolean"
                    )
                    case_result["valid"] = False

        # Validate should_pass is boolean
        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            case_result["errors"].append("should_pass must be a boolean")
            case_result["valid"] = False

        case_result["test_case_number"] = i + 1
        result["test_cases"].append(case_result)

        if not case_result["valid"]:
            result["valid"] = False

    return result
