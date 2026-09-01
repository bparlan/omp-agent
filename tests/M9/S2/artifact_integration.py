#!/usr/bin/env python3
"""Artifact integration tests for M9S2 specification.

Tests FR-PROJECT_CONFIG_REGISTRATION integration with Artifact Registry.
"""

import sys
import unittest

sys.path.insert(0, ".")

from core.artifacts.artifact_types import get_artifact_type, get_all_artifact_types
from core.artifacts.artifact_types import _ARTIFACT_TYPE_DEFINITIONS


class TestProjectConfigArtifactRegistration(unittest.TestCase):
    """Validate project-config is registered in the global artifact type registry."""

    def test_project_config_in_all_types(self):
        """FR-PROJECT_CONFIG_REGISTRATION: project-config is in get_all_artifact_types."""
        all_types = get_all_artifact_types()
        identifiers = [t.machine_identifier for t in all_types]
        self.assertIn("project-config", identifiers)

    def test_project_config_in_definitions(self):
        """FR-PROJECT_CONFIG_REGISTRATION: project-config is in _ARTIFACT_TYPE_DEFINITIONS."""
        self.assertIn("project-config", _ARTIFACT_TYPE_DEFINITIONS)

    def test_project_config_producer_skills(self):
        """Verify project-config lists correct producer skills."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)
        self.assertIn("bootstrap-project", result.producer_skills)
        self.assertIn("manage-roadmap", result.producer_skills)

    def test_project_config_consumer_skills(self):
        """Verify project-config lists healthcenter as consumer."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)
        self.assertIn("healthcenter", result.consumer_skills)

    def test_project_config_required_metadata(self):
        """Verify project-config has standard required metadata fields."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)
        self.assertIn("artifact_type", result.required_metadata)
        self.assertIn("created_at", result.required_metadata)

    def test_project_config_allowed_relationships(self):
        """Verify project-config supports derived_from relationship."""
        result = get_artifact_type("project-config")
        self.assertIsNotNone(result)
        self.assertIn("derived_from", result.allowed_relationships)


class TestHealthCheckArtifactRegistration(unittest.TestCase):
    """Validate health-check is registered for M9S3 integration."""

    def test_health_check_in_all_types(self):
        """FR-PROJECT_CONFIG_REGISTRATION: health-check is in get_all_artifact_types."""
        all_types = get_all_artifact_types()
        identifiers = [t.machine_identifier for t in all_types]
        self.assertIn("health-check", identifiers)

    def test_health_check_producer_skills(self):
        """Verify health-check is produced by healthcenter skill."""
        result = get_artifact_type("health-check")
        self.assertIsNotNone(result)
        self.assertIn("healthcenter", result.producer_skills)


if __name__ == "__main__":
    unittest.main()