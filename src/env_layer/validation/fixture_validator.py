"""
Fixture Validator for the AEF Environment Layer.

This module validates fixture contracts as specified in milestone specifications.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class FixtureValidator:
    """
    Validates fixture contracts for the AEF 6-layer substrate architecture.

    Provides deterministic validation of all fixture contracts (CLI, Schema, Fixture)
    as specified in Environment Layer specifications.
    """

    def __init__(self, fixtures_dir: Path = None):
        self.fixtures_dir = (
            Path(fixtures_dir)
            if fixtures_dir
            else Path(__file__).parent.parent.parent / "tests" / "fixtures"
        )

    def validate_cli_fixtures(self) -> Dict[str, Any]:
        """Validate all CLI fixtures."""
        result = {
            "valid": True,
            "fixtures_validated": [],
            "errors": [],
            "warnings": [],
        }

        # Check for required fixture files
        required_fixtures = [
            "env_detection.yml",
            "mise_config.yml",
            "env_detection_pre_task.yml",
            "workspace_isolation.yml",
            "cross_language_runtime.yml",
        ]

        for fixture_name in required_fixtures:
            fixture_path = self.fixtures_dir / fixture_name
            if not fixture_path.exists():
                result["errors"].append(f"Missing fixture file: {fixture_name}")
                result["valid"] = False
                continue

            # Validate fixture content
            validation = self._validate_fixture_file(fixture_path)
            result["fixtures_validated"].append(
                {
                    "file": fixture_name,
                    "valid": validation["valid"],
                    "errors": validation.get("errors", []),
                    "warnings": validation.get("warnings", []),
                }
            )

            if not validation["valid"]:
                result["valid"] = False
                result["errors"].extend(validation.get("errors", []))

        return result

    def validate_schema_fixtures(self) -> Dict[str, Any]:
        """Validate all schema fixtures."""
        result = {
            "valid": True,
            "fixtures_validated": [],
            "errors": [],
            "warnings": [],
        }

        # For schema validation, we validate the schema definitions themselves
        schema_dir = self.fixtures_dir.parent / "milestones" / milestone_id
        if not schema_dir.exists():
            result["errors"].append(f"Schema directory not found: {schema_dir}")
            result["valid"] = False
            return result

        # Check for schema files
        schema_files = [
            "environment-schema.json",
            "environment-fixture.json",
        ]

        for schema_name in schema_files:
            schema_path = schema_dir / schema_name
            if not schema_path.exists():
                result["warnings"].append(f"Schema file not found: {schema_name}")
                continue

            # Validate schema JSON structure
            validation = self._validate_schema_file(schema_path)
            result["fixtures_validated"].append(
                {
                    "file": schema_name,
                    "valid": validation["valid"],
                    "errors": validation.get("errors", []),
                    "warnings": validation.get("warnings", []),
                }
            )

            if not validation["valid"]:
                result["valid"] = False
                result["errors"].extend(validation.get("errors", []))

        return result

    def validate_all_fixtures(self) -> Dict[str, Any]:
        """Validate all fixture contracts (CLI + Schema)."""
        result = {
            "overall_valid": True,
            "cli_fixtures": self.validate_cli_fixtures(),
            "schema_fixtures": self.validate_schema_fixtures(),
            "summary": {},
        }

        # Calculate summary
        result["summary"] = {
            "cli_fixtures_valid": result["cli_fixtures"]["valid"],
            "schema_fixtures_valid": result["schema_fixtures"]["valid"],
            "total_fixtures": len(result["cli_fixtures"]["fixtures_validated"])
            + len(result["schema_fixtures"]["fixtures_validated"]),
            "valid_fixtures": sum(
                1 for f in result["cli_fixtures"]["fixtures_validated"] if f["valid"]
            )
            + sum(
                1 for f in result["schema_fixtures"]["fixtures_validated"] if f["valid"]
            ),
        }

        result["overall_valid"] = (
            result["cli_fixtures"]["valid"] and result["schema_fixtures"]["valid"]
        )

        return result

    def _validate_fixture_file(self, fixture_path: Path) -> Dict[str, Any]:
        """Validate a single fixture file."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        try:
            with open(fixture_path, "r") as f:
                content = f.read()

            # Try to parse as YAML
            try:
                import yaml

                fixture_data = yaml.safe_load(content)
            except ImportError:
                result["errors"].append(
                    "PyYAML not installed - cannot validate YAML fixtures"
                )
                result["valid"] = False
                return result
            except yaml.YAMLError as e:
                result["errors"].append(
                    f"Invalid YAML in fixture {fixture_path.name}: {e}"
                )
                result["valid"] = False
                return result

            # Validate fixture structure based on type
            if not fixture_data:
                result["errors"].append(f"Empty fixture file: {fixture_path.name}")
                result["valid"] = False
                return result

            # Determine fixture type and validate
            fixture_type = self._determine_fixture_type(fixture_data)
            if fixture_type:
                validation = getattr(self, f"_validate_{fixture_type}_fixture")(
                    fixture_data
                )
                result.update(validation)

        except Exception as e:
            result["errors"].append(
                f"Error validating fixture {fixture_path.name}: {e}"
            )
            result["valid"] = False

        return result

    def _validate_schema_file(self, schema_path: Path) -> Dict[str, Any]:
        """Validate a schema file."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        try:
            with open(schema_path, "r") as f:
                content = f.read()

            # Parse JSON
            try:
                schema_data = json.loads(content)
            except json.JSONDecodeError as e:
                result["errors"].append(
                    f"Invalid JSON in schema {schema_path.name}: {e}"
                )
                result["valid"] = False
                return result

            # Validate schema structure
            validation = self._validate_json_schema(schema_data)
            result.update(validation)

        except Exception as e:
            result["errors"].append(f"Error validating schema {schema_path.name}: {e}")
            result["valid"] = False

        return result

    def _determine_fixture_type(self, fixture_data: Dict[str, Any]) -> str:
        """Determine the type of fixture based on its structure."""
        if "env_detection" in fixture_data:
            return "env_detection"
        elif "mise_config_validation" in fixture_data:
            return "mise_config"
        elif "env_detection_pre_task" in fixture_data:
            return "env_detection_pre_task"
        elif "workspace_isolation" in fixture_data:
            return "workspace_isolation"
        elif "cross_language_runtime" in fixture_data:
            return "cross_language_runtime"
        else:
            return None

    def _validate_env_detection_fixture(
        self, fixture_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate environment detection fixture."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if "test_cases" not in fixture_data:
            result["errors"].append("Missing test_cases")
            result["valid"] = False
            return result

        test_cases = fixture_data["test_cases"]

        for i, test_case in enumerate(test_cases):
            case_errors = self._validate_env_detection_test_case(test_case, i)
            if case_errors:
                result["valid"] = False
                result["errors"].extend(case_errors)

        return result

    def _validate_env_detection_test_case(
        self, test_case: Dict[str, Any], index: int
    ) -> List[str]:
        """Validate a single environment detection test case."""
        errors = []

        required_fields = [
            "name",
            "project",
            "expected_runtime",
            "expected_tools",
            "threshold",
        ]
        for field in required_fields:
            if field not in test_case:
                errors.append(f"Test case {index} missing required field: {field}")

        if "threshold" in test_case:
            threshold = test_case["threshold"]
            if (
                not isinstance(threshold, (int, float))
                or threshold < 0
                or threshold > 1
            ):
                errors.append(
                    f"Test case {index}: Invalid threshold value: {threshold}"
                )

        if "expected_tools" in test_case and not isinstance(
            test_case["expected_tools"], list
        ):
            errors.append(f"Test case {index}: expected_tools must be a list")

        return errors

    def _validate_mise_config_fixture(
        self, fixture_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate mise configuration fixture."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if "test_cases" not in fixture_data:
            result["errors"].append("Missing test_cases")
            result["valid"] = False
            return result

        test_cases = fixture_data["test_cases"]

        for i, test_case in enumerate(test_cases):
            case_errors = self._validate_mise_config_test_case(test_case, i)
            if case_errors:
                result["valid"] = False
                result["errors"].extend(case_errors)

        return result

    def _validate_mise_config_test_case(
        self, test_case: Dict[str, Any], index: int
    ) -> List[str]:
        """Validate a single mise config test case."""
        errors = []

        required_fields = ["name", "config", "should_pass"]
        for field in required_fields:
            if field not in test_case:
                errors.append(f"Test case {index} missing required field: {field}")

        if "config" in test_case:
            config = test_case["config"]
            if "environment" not in config:
                errors.append(f"Test case {index}: Missing environment in config")
            elif "runtime" not in config["environment"]:
                errors.append(f"Test case {index}: Missing runtime in environment")
            elif "version" not in config["environment"]:
                errors.append(f"Test case {index}: Missing version in environment")

        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            errors.append(f"Test case {index}: should_pass must be a boolean")

        return errors

    def _validate_env_detection_pre_task_fixture(
        self, fixture_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate environment detection pre-task fixture."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if "test_cases" not in fixture_data:
            result["errors"].append("Missing test_cases")
            result["valid"] = False
            return result

        test_cases = fixture_data["test_cases"]

        for i, test_case in enumerate(test_cases):
            case_errors = self._validate_env_detection_pre_task_test_case(test_case, i)
            if case_errors:
                result["valid"] = False
                result["errors"].extend(case_errors)

        return result

    def _validate_env_detection_pre_task_test_case(
        self, test_case: Dict[str, Any], index: int
    ) -> List[str]:
        """Validate a single environment detection pre-task test case."""
        errors = []

        required_fields = [
            "name",
            "project",
            "runtime",
            "expected_detection_result",
            "should_pass",
        ]
        for field in required_fields:
            if field not in test_case:
                errors.append(f"Test case {index} missing required field: {field}")

        if "expected_detection_result" in test_case:
            expected = test_case["expected_detection_result"]
            required_expected_fields = [
                "runtime_detected",
                "tools_found",
                "version",
                "isolation_setup",
            ]
            for field in required_expected_fields:
                if field not in expected:
                    errors.append(
                        f"Test case {index}: Missing expected_detection_result field: {field}"
                    )

            if "tools_found" in expected and not isinstance(
                expected["tools_found"], list
            ):
                errors.append(
                    f"Test case {index}: expected_detection_result.tools_found must be a list"
                )

        if "should_pass" in test_case and not isinstance(
            test_case["should_pass"], bool
        ):
            errors.append(f"Test case {index}: should_pass must be a boolean")

        return errors

    def _validate_workspace_isolation_fixture(
        self, fixture_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate workspace isolation fixture."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if "test_cases" not in fixture_data:
            result["errors"].append("Missing test_cases")
            result["valid"] = False
            return result

        test_cases = fixture_data["test_cases"]

        for i, test_case in enumerate(test_cases):
            case_errors = self._validate_workspace_isolation_test_case(test_case, i)
            if case_errors:
                result["valid"] = False
                result["errors"].extend(case_errors)

        return result

    def _validate_workspace_isolation_test_case(
        self, test_case: Dict[str, Any], index: int
    ) -> List[str]:
        """Validate a single workspace isolation test case."""
        errors = []

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
                errors.append(f"Test case {index} missing required field: {field}")

        return errors

    def _validate_cross_language_runtime_fixture(
        self, fixture_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate cross-language runtime fixture."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        if "test_cases" not in fixture_data:
            result["errors"].append("Missing test_cases")
            result["valid"] = False
            return result

        test_cases = fixture_data["test_cases"]

        for i, test_case in enumerate(test_cases):
            case_errors = self._validate_cross_language_runtime_test_case(test_case, i)
            if case_errors:
                result["valid"] = False
                result["errors"].extend(case_errors)

        return result

    def _validate_cross_language_runtime_test_case(
        self, test_case: Dict[str, Any], index: int
    ) -> List[str]:
        """Validate a single cross-language runtime test case."""
        errors = []

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
                errors.append(f"Test case {index} missing required field: {field}")

        return errors

    def _validate_json_schema(self, schema_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON schema structure."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        # Basic validation
        if not isinstance(schema_data, dict):
            result["errors"].append("Schema must be a JSON object")
            result["valid"] = False
            return result

        # Check for required top-level fields based on schema type
        if "schema_version" not in schema_data:
            result["warnings"].append("Missing schema_version")

        if "mise_config" in schema_data:
            mise_config = schema_data["mise_config"]
            if "environment" not in mise_config:
                result["errors"].append("Missing environment in mise_config")
                result["valid"] = False

        return result
