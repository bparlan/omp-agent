#!/usr/bin/env python3
"""Function API tests for M9S2 specification.

Tests functional requirement FR-PROJECT_CONFIG_VALIDATION API contract.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, ".")

from core.validation import validate_project_config
from core.artifacts.artifact_types import get_artifact_type


class TestValidateProjectConfigFunction(unittest.TestCase):
    """Validate the validate_project_config function API contract."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def test_returns_dict_with_required_keys(self):
        """FR-PROJECT_CONFIG_VALIDATION: Function returns dict with valid, errors, missing_fields."""
        result = validate_project_config(self.test_dir)
        self.assertIsInstance(result, dict)
        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("missing_fields", result)

    def test_valid_config_returns_valid_true(self):
        """FR-PROJECT_CONFIG_VALIDATION: Valid config returns valid=true, errors=[]."""
        omp_dir = os.path.join(self.test_dir, ".omp")
        os.makedirs(omp_dir, exist_ok=True)
        config_path = os.path.join(omp_dir, "config.yml")
        with open(config_path, "w") as f:
            f.write(
                "project_id: test-1\nproject_slug: test-project\nversion: 1.0.0-stable\n"
            )
        result = validate_project_config(self.test_dir)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_invalid_config_returns_valid_false(self):
        """FR-PROJECT_CONFIG_VALIDATION: Invalid config returns valid=false with errors."""
        omp_dir = os.path.join(self.test_dir, ".omp")
        os.makedirs(omp_dir, exist_ok=True)
        config_path = os.path.join(omp_dir, "config.yml")
        with open(config_path, "w") as f:
            f.write("project_id: test-2\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)

    def test_nonexistent_root_returns_error(self):
        """FR-PROJECT_CONFIG_VALIDATION: Nonexistent path returns error."""
        result = validate_project_config("/nonexistent/path/that/should/not/exist")
        self.assertFalse(result["valid"])

    def test_empty_string_root_returns_error(self):
        """FR-PROJECT_CONFIG_VALIDATION: Empty string root returns error."""
        result = validate_project_config("")
        self.assertFalse(result["valid"])


class TestProjectConfigArtifactTypeRegistration(unittest.TestCase):
    """Validate project-config artifact type is registered (FR-PROJECT_CONFIG_REGISTRATION)."""

    def test_project_config_type_exists(self):
        """FR-PROJECT_CONFIG_REGISTRATION: get_artifact_type('project-config') returns definition."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)

    def test_project_config_storage_location(self):
        """FR-PROJECT_CONFIG_REGISTRATION: Storage location is .omp/config.yml."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.canonical_storage_location, ".omp/config.yml")

    def test_health_check_type_exists(self):
        """Verify health-check type is registered for M9S3 integration."""
        result = get_artifact_type("health-check")
        self.assertIsNotNone(result)

    def test_health_check_storage_location(self):
        """Verify health-check storage follows artifact convention."""
        result = get_artifact_type("health-check")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertIn("health-check", result.canonical_storage_location)


if __name__ == "__main__":
    unittest.main()
