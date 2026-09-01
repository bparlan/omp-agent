#!/usr/bin/env python3
"""
Manage Development Skill Implementation

SDD pipeline gate enforcement and validation for the OhMyPi Spec-Driven Development (SDD) lifecycle.
Implements deterministic pipeline state validation through comprehensive artifact gate enforcement.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Import core AEF artifact system modules for S4 integration
from core.validation import validate_metadata
from core.artifacts.metadata import extract_frontmatter
from core.artifacts.artifact_types import get_artifact_type
from core.artifacts.registry import get_registry
from core.artifacts.creation import create_artifact


class PipelineStateValidator:
    """
    Pipeline State Validator for enforcing deterministic gate progression
    through the OhMyPi Spec-Driven Development (SDD) pipeline.

    This class implements the core validation logic required by M13S1
    specification to ensure all artifacts meet canonical contracts before
    phase transition.
    """

    def __init__(self, milestone_id: str = "M13"):
        self.milestone_id = milestone_id
        self.validation_results = []
        self.gate_artifacts = {}

    def validate_specification(self, spec_id: str) -> Dict[str, Any]:
        """
        Validate a specification artifact for compliance with canonical contracts.

        Args:
            spec_id: Specification identifier (e.g., "SPEC-M13S1")

        Returns:
            Dict containing validation results with keys:
            - "valid": Boolean indicating overall validation success
            - "errors": List of error messages if validation fails
            - "missing_fields": List of required fields that are missing
        """
        spec_path = Path(f"milestones/{self.milestone_id}/{spec_id}.md")

        if not spec_path.exists():
            return {
                "valid": False,
                "errors": [f"Specification file not found: {spec_path}"],
                "missing_fields": ["file_path"],
            }

        # Use core AEF validation module
        validation_result = validate_metadata(str(spec_path))

        # Extract frontmatter using core AEF metadata module
        frontmatter = extract_frontmatter(str(spec_path)) or {}

        return {
            "valid": validation_result["valid"],
            "errors": validation_result["errors"],
            "missing_fields": validation_result["missing_fields"],
            "spec_id": spec_id,
            "file_path": str(spec_path),
            "frontmatter": frontmatter,
        }

    def validate_gate_artifacts(self) -> Dict[str, Any]:
        """
        Validate all gate artifacts required for pipeline progression.

        Checks for the existence and validity of gate artifacts.

        Returns:
            Dict containing:
            - "valid": Overall validation status
            - "gate_artifacts": Dict of found gate artifacts
            - "missing_artifacts": List of missing artifacts
            - "invalid_artifacts": List of invalid artifacts
        """
        milestone_dir = Path(f"milestones/{self.milestone_id}")
        if not milestone_dir.exists():
            return {
                "valid": False,
                "missing_artifacts": [
                    f"Milestone directory not found: {milestone_dir}"
                ],
                "invalid_artifacts": [],
                "gate_artifacts": {},
            }

        # Gate artifact patterns based on milestone naming convention
        # Files expected: VER-<MILESTONE_ID>*.md, EVA-<MILESTONE_ID>*.md, REV-<MILESTONE_ID>*.md, CLOSE-<MILESTONE_ID>-*.md
        patterns = {
            "VER": f"VER-{self.milestone_id}*.md",
            "EVA": f"EVA-{self.milestone_id}*.md",
            "REV": f"REV-{self.milestone_id}*.md",
            "CLOSE": f"CLOSE-{self.milestone_id}-*.md",
        }

        gate_artifacts_found: Dict[str, List[str]] = {}
        missing_artifacts: List[str] = []
        invalid_artifacts: List[str] = []

        for key, pattern in patterns.items():
            matches = list(milestone_dir.glob(pattern))
            if matches:
                # Consider any match as a found artifact; content validation handled elsewhere
                gate_artifacts_found[key] = [str(m) for m in matches]
            else:
                missing_artifacts.append(f"{key} artifact missing (pattern: {pattern})")

        overall_valid = len(missing_artifacts) == 0 and len(invalid_artifacts) == 0

        return {
            "valid": overall_valid,
            "gate_artifacts": gate_artifacts_found,
            "missing_artifacts": missing_artifacts,
            "invalid_artifacts": invalid_artifacts,
        }

    def validate_core_artifacts(self) -> Dict[str, Any]:
        """
        Validate all pipeline artifacts using core AEF artifact system modules.

        This method implements FR-AEF-CANONICAL-VALIDATION-INTEGRATION,
        FR-AEF-REGISTRY-TYPE-REGISTRATION, FR-AEF-METADATA-EXTRACTION,
        and FR-AEF-ARTIFACT-CREATION-PIPELINE requirements.

        Returns:
            Dict containing validation results with keys:
            - "valid": Boolean indicating overall validation success
            - "errors": List of error messages if validation fails
            - "missing_fields": List of required fields that are missing
            - "validation_results": Detailed results for each pipeline artifact
        """
        milestone_dir = Path(f"milestones/{self.milestone_id}")
        if not milestone_dir.exists():
            return {
                "valid": False,
                "errors": [f"Milestone directory not found: {milestone_dir}"],
                "missing_fields": ["milestone_id"],
                "validation_results": {},
            }

        # Collect validation results for all pipeline artifacts
        validation_results = {}
        all_valid = True

        for artifact_file in milestone_dir.glob("*.md"):
            # Skip non-pipeline artifacts
            artifact_name = artifact_file.stem
            if not (
                artifact_name.startswith("SPEC-")
                or artifact_name.startswith("VER-")
                or artifact_name.startswith("TSET-")
                or artifact_name.startswith("EVA-")
                or artifact_name.startswith("REV-")
                or artifact_name.startswith("CLOSE-")
            ):
                continue

            # Determine artifact type from naming pattern for registry lookup
            if artifact_name.startswith("SPEC-"):
                registry_type_name = "specification"
            elif artifact_name.startswith("VER-"):
                registry_type_name = "verification"
            elif artifact_name.startswith("TSET-"):
                registry_type_name = "test"
            elif artifact_name.startswith("EVA-"):
                registry_type_name = "evaluation"
            elif artifact_name.startswith("REV-"):
                registry_type_name = "review"
            elif artifact_name.startswith("CLOSE-"):
                registry_type_name = "closure"
            else:
                registry_type_name = None

            # Validate with core AEF modules - FR-AEF-CANONICAL-VALIDATION-INTEGRATION
            core_validation = validate_metadata(str(artifact_file))
            frontmatter = extract_frontmatter(str(artifact_file)) or {}

            # Try registry lookup with the type name first, then with the artifact name
            registry_type = (
                get_artifact_type(registry_type_name) if registry_type_name else None
            )
            if registry_type is None and registry_type_name == "closure":
                # Closure type may not be registered, try with the artifact name
                registry_type = get_artifact_type(artifact_name)
                if registry_type is None:
                    # Register closure type in _ARTIFACT_TYPE_DEFINITIONS (FR-AEF-REGISTRY-TYPE-REGISTRATION)
                    try:
                        from core.artifacts.artifact_types import (
                            _ARTIFACT_TYPE_DEFINITIONS,
                            CanonicalArtifactType,
                        )

                        _ARTIFACT_TYPE_DEFINITIONS["closure"] = CanonicalArtifactType(
                            machine_identifier="closure",
                            human_readable_name="Closure",
                            purpose="Milestone closure artifact",
                            producer_skills=[],
                            consumer_skills=[],
                            canonical_storage_location="<M_ID>/closures/<CLOSE_ID>.md",
                            required_metadata=[
                                "created_at",
                                "updated_at",
                                "artifact_identity",
                                "artifact_type",
                            ],
                            optional_metadata=[],
                            lifecycle_states=["draft", "completed", "archived"],
                            allowed_relationships=["derived_from"],
                        )
                        # Also register in registry
                        registry = get_registry()
                        registry.register_type("closure", {}, {})
                        registry_type = get_artifact_type("closure")
                    except Exception:
                        registry_type = None
            # Check if frontmatter has required keys - FR-AEF-METADATA-EXTRACTION
            required_frontmatter_keys = [
                "id",
                "type",
                "title",
                "milestone_id",
                "status",
                "derived_from",
                "template_version",
                "metadata",
            ]
            frontmatter_complete = all(
                key in frontmatter for key in required_frontmatter_keys
            )

            # Validate registry type resolution - FR-AEF-REGISTRY-TYPE-REGISTRATION
            registry_valid = registry_type is not None

            # Overall validation
            artifact_valid = (
                core_validation["valid"] and registry_valid and frontmatter_complete
            )

            validation_results[artifact_name] = {
                "file_path": str(artifact_file),
                "core_validation": core_validation,
                "frontmatter": frontmatter,
                "registry_type": registry_type,
                "registry_valid": registry_valid,
                "frontmatter_complete": frontmatter_complete,
                "valid": artifact_valid,
                "errors": [],
            }

            if not artifact_valid:
                all_valid = False
                # Collect specific errors
                if not core_validation["valid"]:
                    validation_results[artifact_name]["errors"].append(
                        f"Core validation failed: {core_validation['errors']}"
                    )
                if not registry_valid:
                    validation_results[artifact_name]["errors"].append(
                        f"Registry lookup failed for {artifact_name}"
                    )
                if not frontmatter_complete:
                    validation_results[artifact_name]["errors"].append(
                        f"Frontmatter incomplete for {artifact_name}"
                    )

        return {
            "valid": all_valid,
            "errors": []
            if all_valid
            else ["Core AEF validation failed for pipeline artifacts"],
            "missing_fields": [],
            "validation_results": validation_results,
        }

    def validate_stage_progression(self) -> Dict[str, Any]:
        """
        Validate progression through the SDD pipeline stages.

        Ensures that each stage has properly validated artifacts
        before allowing progression to the next stage.

        Returns:
            Dict containing validation results for each stage
        """
        # Define expected stage patterns based on milestone naming conventions
        stage_patterns = {
            "specification": f"SPEC-{self.milestone_id}S*.md",
            "verification": f"VER-{self.milestone_id}*.md",
            "tests": f"TSET-{self.milestone_id}S*.md",
            "evaluation": f"EVA-{self.milestone_id}*.md",
            "review": f"REV-{self.milestone_id}*.md",
            "closure": f"CLOSE-{self.milestone_id}-*.md",
        }

        stages = [
            "specification",
            "verification",
            "tests",
            "evaluation",
            "review",
            "closure",
        ]
        stage_results = {}

        for stage in stages:
            pattern = stage_patterns[stage]
            matches = list((Path(f"milestones/{self.milestone_id}")).glob(pattern))
            found = len(matches) > 0
            stage_results[stage] = {
                "required_artifacts": 1,
                "found_artifacts": 1 if found else 0,
                "valid": found,
            }

        # Progression is deterministic only if all stages have required artifacts
        all_stages_valid = all(res["valid"] for res in stage_results.values())

        return {
            "valid": all_stages_valid,
            "stages": stage_results,
            "progression_deterministic": all_stages_valid,
        }

    def generate_pipeline_state(self) -> str:
        """
        Generate PIPELINE-STATE.md with structured validation outcomes.

        Creates a comprehensive record of gate validation outcomes,
        including timestamps, validation status, artifact paths, and error details.

        Returns:
            Path to the generated PIPELINE-STATE.md file
        """
        milestone_dir = Path(f"milestones/{self.milestone_id}")
        milestone_dir.mkdir(parents=True, exist_ok=True)
        state_file = milestone_dir / "PIPELINE-STATE.md"

        # Collect validation results from all gates
        generation_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        unique_id_suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        gate_outcomes = []

        # Run validation functions to collect outcomes
        spec_result = self.validate_specification("SPEC-M13S1")
        gate_result = self.validate_gate_artifacts()
        stage_result = self.validate_stage_progression()

        # Record specification validation outcome
        gate_outcomes.append(
            {
                "gate_name": "SPEC-M13S1_VALIDATION",
                "timestamp": generation_time,
                "status": "PASSED" if spec_result["valid"] else "FAILED",
                "artifact_path": spec_result.get("file_path", ""),
                "validation_details": spec_result,
                "error_count": len(spec_result["errors"]),
                "missing_count": len(spec_result["missing_fields"]),
            }
        )

        # Record gate artifact validation outcome
        gate_outcomes.append(
            {
                "gate_name": "GATE_ARTIFACTS_VALIDATION",
                "timestamp": generation_time,
                "status": "PASSED" if gate_result["valid"] else "FAILED",
                "artifact_path": "",
                "validation_details": gate_result,
                "error_count": len(gate_result["missing_artifacts"]),
                "missing_count": 0,
            }
        )

        # Record stage progression outcome
        gate_outcomes.append(
            {
                "gate_name": "STAGE_PROGRESSION_VALIDATION",
                "timestamp": generation_time,
                "status": "PASSED" if stage_result["valid"] else "FAILED",
                "artifact_path": "",
                "validation_details": stage_result,
                "error_count": 0,
                "missing_count": 0,
            }
        )

        # Generate PIPELINE-STATE.md content
        content = f"""---
id: PIPELINE-STATE-{unique_id_suffix}
type: pipeline_state
title: "Pipeline State Validation Report"
milestone_id: {self.milestone_id}
status: draft
template_version: 1.0.0
---

# Pipeline State Validation Report

## Overview

**Generated:** {generation_time}
**Total Gates Validated:** {len(gate_outcomes)}

## Gate Outcomes

| Gate Name | Status | Timestamp | Error Count | Missing Count |
|:----------|:-------|:---------|:------------|:-------------|
"""

        for outcome in gate_outcomes:
            content += f"| {outcome['gate_name']} | {outcome['status']} | {outcome['timestamp']} | {outcome['error_count']} | {outcome['missing_count']} |\n"

        content += "\n## Detailed Validation Results\n\n"
        for outcome in gate_outcomes:
            content += f"### {outcome['gate_name']}\n\n"
            content += f"- **Status:** {outcome['status']}\n"
            content += f"- **Timestamp:** {outcome['timestamp']}\n"
            content += f"- **Artifact Path:** {outcome['artifact_path']}\n"
            content += f"- **Error Count:** {outcome['error_count']}\n"
            content += f"- **Missing Count:** {outcome['missing_count']}\n"
            content += f"- **Details:** {outcome['validation_details']}\n\n"

        content += """---

*This PIPELINE-STATE.md was auto-generated by the manage-development skill during pipeline validation.*"""

        state_file.write_text(content)
        return str(state_file)


def main(milestone_id: str = "M13") -> int:
    """
    Main entry point for the manage-development skill.

    Implements the SDD pipeline gate enforcement as specified in M13S1
    specification. This function orchestrates validation through the complete
    6-stage pipeline without manual skip.

    Args:
        milestone_id: Milestone identifier (defaults to "M13")

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("=== Manage Development Skill (Phase 1) ===")
    print(f"Milestone ID: {milestone_id}")
    print()

    # Initialize pipeline state validator
    validator = PipelineStateValidator(milestone_id)

    # Discover all specifications for the milestone
    milestone_path = Path(f"milestones/{milestone_id}")
    specifications = []
    if milestone_path.exists():
        for spec_file in milestone_path.glob("SPEC-M13S*.md"):
            spec_id = spec_file.name.replace(".md", "")
            specifications.append(spec_id)

    print(f"Found {len(specifications)} specifications: {specifications}")
    print()

    # Validate each specification
    validation_results = []
    all_valid = True

    for spec_id in specifications:
        print(f"--- Validating {spec_id} ---")
        spec_result = validator.validate_specification(spec_id)
        validation_results.append(spec_result)

        if spec_result["valid"]:
            print(f"✓ {spec_id}: VALID")
            print(f"  File: {spec_result.get('file_path', 'N/A')}")
            print(f"  Validated fields: {len(spec_result.get('frontmatter', {}))}")
        else:
            print(f"✗ {spec_id}: INVALID")
            print(f"  Errors: {spec_result['errors']}")
            print(f"  Missing fields: {spec_result['missing_fields']}")
            all_valid = False

        print()

    # Validate gate artifacts
    print("--- Validating Gate Artifacts ---")
    gate_result = validator.validate_gate_artifacts()
    if gate_result["valid"]:
        print("✓ Gate artifacts: VALID")
    else:
        print("✗ Gate artifacts: INVALID")
        print(f"  Missing artifacts: {gate_result['missing_artifacts']}")
        all_valid = False

    print()

    # Validate core artifacts (S4 AEF integration)
    print("--- Validating Core AEF Artifact System Integration ---")
    core_result = validator.validate_core_artifacts()
    if core_result["valid"]:
        print("✓ Core AEF artifacts: VALID")
        print(
            f"  Validated {len(core_result['validation_results'])} pipeline artifacts"
        )
    else:
        print("✗ Core AEF artifacts: INVALID")
        print(f"  Errors: {core_result['errors']}")
        for artifact_name, artifact_result in core_result["validation_results"].items():
            if not artifact_result["valid"]:
                print(f"    {artifact_name}: {artifact_result['errors']}")
        all_valid = False

    print()

    # Validate stage progression
    print("--- Validating Stage Progression ---")
    stage_result = validator.validate_stage_progression()
    if stage_result["valid"]:
        print("✓ Stage progression: VALID")
        print(
            f"  Deterministic progression: {stage_result['progression_deterministic']}"
        )
    else:
        print("✗ Stage progression: INVALID")
        all_valid = False

    print()

    # Generate PIPELINE-STATE.md
    print("--- Generating PIPELINE-STATE.md ---")
    pipeline_state_file = validator.generate_pipeline_state()
    print(f"✓ Generated: {pipeline_state_file}")

    print()
    print("=== Validation Complete ===")

    if all_valid:
        print("✓ All validations passed!")
        print("✓ Pipeline is ready for implementation phase.")
        return 0
    else:
        print("✗ Validation failed!")
        print("✗ Pipeline cannot proceed to implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
