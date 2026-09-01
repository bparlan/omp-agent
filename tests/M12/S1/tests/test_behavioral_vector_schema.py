#!/usr/bin/env python3
"""
Test behavioral-vector schema validation for M12S1 Persona Overhaul.

This test suite validates the behavioral-vector persona overhaul specification
against the M12S1 schema requirements. Tests MUST fail initially because the
current implementation has not been updated to fully enforce the behavioral-vector
schema fields.

Coverage: All 6 behavioral-vector schema fields:
- baseline
- pressure_shift
- optimizes_for
- neglects
- phase_affinity
- continuation_anchor

Requirement: FR-M12S1-1 (Behavioral-Vector Persona Definition Schema)
             VR-M12S1-1 (Schema Validation)
             AC-M12S1-1 (Persona Vector Completeness)
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, List


def load_fixture_schema():
    """Load the persona vector schema from fixture."""
    fixture_path = Path(
        "tests/fixtures/synthetic_managedev_personas/persona_vectors.yml"
    )
    with open(fixture_path, "r") as f:
        return yaml.safe_load(f)["persona_vector_validation"]


def load_actual_personas_from_skill():
    """Load actual persona definitions from manage-development skill.

    Extracts behavioral-vector personas from SKILL.md using the actual format:
    **Persona 1: the-skeptic**
    - **Label:** Adversarial Verification Engineer
    - **Baseline:** [text]
    - **Pressure Shift:** [text]
    ...

    Returns dict of persona data with behavioral-vector fields.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    personas = {}

    # Pattern to match persona definitions in SKILL.md format
    # Matches: **Persona 1: the-skeptic** followed by persona content
    persona_blocks = re.findall(
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*[\s\S]*?(?=\n---|\*\*Persona \d+:|\Z)",
        content,
    )

    for block in persona_blocks:
        # Extract ID from first line
        id_match = re.search(r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*", block)
        if not id_match:
            continue

        persona_id = id_match.group(1)

        # Extract behavioral vector fields
        # Label field
        label_match = re.search(r"- \*\*Label:\*\*\s*([^*\n]+)", block)
        label = label_match.group(1).strip() if label_match else ""

        # Baseline field
        baseline_match = re.search(r"- \*\*Baseline:\*\* ([^*\n]+)", block)
        baseline = baseline_match.group(1).strip() if baseline_match else ""

        # Pressure Shift field
        pressure_match = re.search(r"- \*\*Pressure Shift:\*\* ([^*\n]+)", block)
        pressure_shift = pressure_match.group(1).strip() if pressure_match else ""

        # Optimizes For field
        optimizes_match = re.search(r"- \*\*Optimizes For:\*\* ([^*\n]+)", block)
        optimizes_for = optimizes_match.group(1).strip() if optimizes_match else ""

        # Neglects field
        neglects_match = re.search(r"- \*\*Neglects:\*\* ([^*\n]+)", block)
        neglects = neglects_match.group(1).strip() if neglects_match else ""

        # Phase Affinity field
        phase_affinity_match = re.search(r"- \*\*Phase Affinity:\*\* ([^*\n]+)", block)
        phase_affinity = []
        if phase_affinity_match:
            phase_text = phase_affinity_match.group(1).strip()
            # Convert from "verification, evaluation" to ["verification", "evaluation"]
            phase_affinity = [p.strip() for p in phase_text.split(",")]

        # Continuation Anchor field
        anchor_match = re.search(r"- \*\*Continuation Anchor:\*\* ([^*\n]+)", block)
        continuation_anchor = (
            anchor_match.group(1).strip().lower() == "true" if anchor_match else False
        )

        personas[persona_id] = {
            "id": persona_id,
            "label": label,
            "baseline": baseline,
            "pressure_shift": pressure_shift,
            "optimizes_for": optimizes_for,
            "neglects": neglects,
            "phase_affinity": phase_affinity,
            "continuation_anchor": continuation_anchor,
        }

    return personas


def validate_persona_vector_schema(
    persona: Dict[str, Any], schema_fixture: Dict[str, Any]
) -> List[str]:
    """Validate a single persona vector against schema requirements.

    Returns list of error messages if validation fails, empty list if passes.
    """
    errors = []

    # Requirement 1: id must match pattern ^[a-z0-9-]+$ (from FR-M12S1-1)
    if not re.match(r"^[a-z0-9-]+$", persona["id"]):
        errors.append(f"id '{persona['id']}' does not match pattern ^[a-z0-9-]+$")

    # Requirement 2: All four required fields must be non-empty and >= 20 chars
    required_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]
    for field in required_fields:
        value = persona.get(field, "")
        if not value or len(value.strip()) < 20:
            errors.append(
                f"{field} must be non-empty and >= 20 chars (got '{value[:50]}...')"
            )

    # Requirement 3: phase_affinity must contain only valid enum values
    valid_phases = [
        "milestone",
        "specification",
        "verification",
        "tests",
        "evaluation",
        "implementation",
    ]
    for phase in persona.get("phase_affinity", []):
        if phase not in valid_phases:
            errors.append(f"Invalid phase_affinity value '{phase}'")

    # Requirement 4: continuation_anchor must be boolean
    if not isinstance(persona.get("continuation_anchor"), bool):
        errors.append(
            f"continuation_anchor must be boolean (got {persona.get('continuation_anchor')})"
        )

    return errors


def test_behavioral_vector_fields_present():
    """Test that all behavioral-vector schema fields are present and populated.

    Validates FR-M12S1-1: Each persona MUST be defined with four mandatory vector fields
    and two optional affinity fields.
    """
    personas = load_actual_personas_from_skill()

    # Expected behavioral-vector fields from schema
    expected_fields = {
        "baseline": "Core behavioral state under normal conditions",
        "pressure_shift": "How behavior changes under stress, time pressure, or ambiguity",
        "optimizes_for": "Primary value this persona contributes to the team",
        "neglects": "Blind spots or tendencies this persona underweights",
        "phase_affinity": "Phases where this persona provides above-average value",
        "continuation_anchor": "Whether this persona serves as continuity anchor across all phases",
    }

    for persona_id, persona in personas.items():
        missing_fields = []
        for field in expected_fields.keys():
            if field not in persona or not persona[field]:
                missing_fields.append(field)

        assert (
            not missing_fields
        ), f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"

        # Also validate each field's content meets schema requirements
        errors = validate_persona_vector_schema(persona, {})
        assert not errors, f"Persona '{persona_id}' validation errors:\n" + "\n".join(
            errors
        )

    print(f"✓ Behavioral-vector schema validation passed for {len(personas)} personas")


def test_schema_field_requirements():
    """Test specific schema field requirements from FR-M12S1-1.

    Validates the exact schema contract defined in FR-M12S1-1.
    """
    personas = load_actual_personas_from_skill()

    # Schema requirements from FR-M12S1-1
    schema_requirements = {
        "id": {"pattern": r"^[a-z0-9-]+$", "description": "Stable vector identifier"},
        "label": {
            "type": "string",
            "description": "Human-readable role label for display",
        },
        "baseline": {
            "type": "string",
            "minLength": 20,
            "description": "Core behavioral state under normal conditions",
        },
        "pressure_shift": {
            "type": "string",
            "minLength": 20,
            "description": "How behavior changes under stress, time pressure, or ambiguity",
        },
        "optimizes_for": {
            "type": "string",
            "minLength": 20,
            "description": "Primary value this persona contributes to the team",
        },
        "neglects": {
            "type": "string",
            "minLength": 20,
            "description": "Blind spots or tendencies this persona underweights",
        },
        "phase_affinity": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "milestone",
                    "specification",
                    "verification",
                    "tests",
                    "evaluation",
                    "implementation",
                ],
            },
            "description": "Phases where this persona provides above-average value",
        },
        "continuation_anchor": {
            "type": "boolean",
            "description": "Whether this persona serves as continuity anchor across all phases",
        },
    }

    for persona_id, persona in personas.items():
        # Validate each field against schema requirements
        field_errors = []

        # Check id pattern
        if not re.match(schema_requirements["id"]["pattern"], persona["id"]):
            field_errors.append(f"id '{persona['id']}' pattern mismatch")

        # Check required fields exist and meet length requirements
        for field in ["baseline", "pressure_shift", "optimizes_for", "neglects"]:
            if field not in persona:
                field_errors.append(f"Missing required field: {field}")
            else:
                value = persona[field]
                if len(str(value)) < schema_requirements[field]["minLength"]:
                    field_errors.append(
                        f"{field} too short (min {schema_requirements[field]['minLength']} chars)"
                    )

        # Check phase_affinity enum values
        valid_phases = schema_requirements["phase_affinity"]["items"]["enum"]
        for phase in persona.get("phase_affinity", []):
            if phase not in valid_phases:
                field_errors.append(f"Invalid phase_affinity value: {phase}")

        # Check continuation_anchor is boolean
        if not isinstance(persona.get("continuation_anchor"), bool):
            field_errors.append(
                f"continuation_anchor must be boolean (got {persona.get('continuation_anchor')})"
            )

        assert not field_errors, (
            f"Persona '{persona_id}' schema violations:\n" + "\n".join(field_errors)
        )

    print(f"✓ Schema field requirements validation passed for {len(personas)} personas")


def test_persona_vector_fixture_completeness():
    """Test that all personas in fixtures are represented in actual implementation.

    Validates that the behavioral-vector personas defined in fixtures match
    those defined in the actual implementation.
    """
    # Load personas from fixture
    schema_fixture = load_fixture_schema()
    fixture_personas = []

    for test_case in schema_fixture["test_cases"]:
        if test_case["should_pass"]:
            fixture_personas.append(test_case["vector"])

    fixture_ids = {p["id"] for p in fixture_personas}

    # Load personas from actual implementation
    actual_personas = load_actual_personas_from_skill()
    actual_ids = set(actual_personas.keys())

    # Check for missing personas
    missing_personas = fixture_ids - actual_ids
    assert (
        not missing_personas
    ), f"Missing personas in implementation: {missing_personas}"

    # Check for extra personas (should be exactly 7 as per FR-M12S1-2)
    extra_personas = actual_ids - fixture_ids
    assert (
        not extra_personas or len(extra_personas) <= 1
    ), f"Unexpected extra personas: {extra_personas}"

    print("✓ Persona vector fixture completeness validation passed")
    print(f"  - {len(fixture_personas)} personas expected in fixtures")
    print(f"  - {len(actual_personas)} personas found in implementation")


if __name__ == "__main__":
    print("Running M12S1 Behavioral-Vector Schema Validation Tests...\n")

    try:
        test_behavioral_vector_fields_present()
        print()
        test_schema_field_requirements()
        print()
        test_persona_vector_fixture_completeness()
        print()
        print("✅ All M12S1 Behavioral-Vector Schema validation tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
