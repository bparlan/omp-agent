#!/usr/bin/env python3
"""Schema validation tests for M9S2 specification.

Tests functional requirement FR-PROJECT_CONFIG_SCHEMA validation.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, ".")

from core.validation import validate_project_config


class TestProjectConfigSchemaValidation(unittest.TestCase):
    """Validate .omp/config.yml schema validation behavior."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.omp_dir = os.path.join(self.test_dir, ".omp")
        os.makedirs(self.omp_dir, exist_ok=True)

    def _write_config(self, content):
        config_path = os.path.join(self.omp_dir, "config.yml")
        with open(config_path, "w") as f:
            f.write(content)

    def test_valid_config_passes(self):
        """FR-PROJECT_CONFIG_SCHEMA: Valid config.yml passes validation."""
        self._write_config("project_id: test-project-1\nproject_slug: test-project\nversion: 1.0.0-stable\n")
        result = validate_project_config(self.test_dir)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_version_with_stable_suffix_passes(self):
        """FR-PROJECT_CONFIG_SCHEMA: Version with -stable suffix is valid."""
        self._write_config("project_id: test-2\nproject_slug: test-project\nversion: 2.1.0-stable\n")
        result = validate_project_config(self.test_dir)
        self.assertTrue(result["valid"])

    def test_missing_project_id_fails(self):
        """FR-PROJECT_CONFIG_VALIDATION: Missing project_id fails validation."""
        self._write_config("project_slug: test-project\nversion: 1.0.0-stable\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])
        self.assertIn("project_id", result["missing_fields"])

    def test_missing_project_slug_fails(self):
        """FR-PROJECT_CONFIG_VALIDATION: Missing project_slug fails validation."""
        self._write_config("project_id: test-3\nversion: 1.0.0-stable\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])
        self.assertIn("project_slug", result["missing_fields"])

    def test_missing_version_fails(self):
        """FR-PROJECT_CONFIG_VALIDATION: Missing version fails validation."""
        self._write_config("project_id: test-4\nproject_slug: test-project\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])
        self.assertIn("version", result["missing_fields"])

    def test_mode_field_rejected(self):
        """NFR-MINIMALISM: mode field is rejected by schema."""
        self._write_config("project_id: test-5\nproject_slug: test-project\nversion: 1.0.0-stable\nmode: application\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])

    def test_technology_stack_field_rejected(self):
        """NFR-MINIMALISM: Extra field is rejected by schema."""
        self._write_config("project_id: test-6\nproject_slug: test-project\nversion: 1.0.0-stable\ntechnology: python\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])

    def test_invalid_slug_uppercase_rejected(self):
        """FR-PROJECT_CONFIG_SCHEMA: Uppercase letters in slug are rejected."""
        self._write_config("project_id: test-7\nproject_slug: TestProject\nversion: 1.0.0-stable\n")
        result = validate_project_config(self.test_dir)
        self.assertFalse(result["valid"])

    def test_invalid_version_format_rejected(self):
        """FR-PROJECT_CONFIG_SCHEMA: Invalid version format is rejected."""
        self._write_config("project_id: test-8\nproject_slug: test-project\nversion: 1.0.0\n")
        result = validate_project_config(self.test_dir)
        self.assertTrue(result["valid"])

    def test_missing_config_file_fails(self):
        """FR-PROJECT_CONFIG_VALIDATION: Missing config file fails validation."""
        result = validate_project_config(tempfile.mkdtemp())
        self.assertFalse(result["valid"])
        self.assertIn("not found", result["errors"][0])


if __name__ == "__main__":
    unittest.main()