#!/usr/bin/env python3
"""
Test behavioral-vector requirements for M12S1 Persona Overhaul.

This test suite validates all behavioral-vector schema requirements defined in FR-M12S1-1.
Tests MUST fail initially because the current manage-development SKILL.md
has incomplete persona vector definitions.

Validates the 6 behavioral-vector schema fields:
- baseline (>= 20 chars, present)
- pressure_shift (>= 20 chars, present)
- optimizes_for (>= 20 chars, present)
- neglects (>= 20 chars, present)
- phase_affinity (array, enum validation)
- continuation_anchor (boolean)

Requirement: FR-M12S1-1, VR-M12S1-1, AC-M12S1-1
"""

import re
from pathlib import Path
from typing import Dict, Any, List


def extract_persona_vectors_from_skill():
    """Extract all persona vectors from manage-development SKILL.md.

    Parses the behavioral-vector personas from the actual skill file.
    Returns a dictionary of persona data with all behavioral-vector fields.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Pattern to match persona definitions with their fields
    # Format: **Persona 1: the-skeptic** followed by field definitions
    persona_sections = re.findall(
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)",
        content,
    )

    personas = {}
    for persona_id, section in persona_sections:
        persona = {"id": persona_id}

        # Extract Label field
        label_match = re.search(r"- \*\*Label:\s*([^*\n]+)", section)
        if label_match:
            persona["label"] = label_match.group(1).strip()
        else:
            persona["label"] = ""

        # Extract Baseline field (behavioral-vector requirement)
        baseline_match = re.search(r"- \*\*Baseline:\s*([^*\n]+)", section)
        if baseline_match:
            persona["baseline"] = baseline_match.group(1).strip()
        else:
            persona["baseline"] = ""

        # Extract Pressure Shift field (behavioral-vector requirement)
        pressure_match = re.search(r"- \*\*Pressure Shift:\s*([^*\n]+)", section)
        if pressure_match:
            persona["pressure_shift"] = pressure_match.group(1).strip()
        else:
            persona["pressure_shift"] = ""

        # Extract Optimizes For field (behavioral-vector requirement)
        optimizes_match = re.search(r"- \*\*Optimizes For:\s*([^*\n]+)", section)
        if optimizes_match:
            persona["optimizes_for"] = optimizes_match.group(1).strip()
        else:
            persona["optimizes_for"] = ""

        # Extract Neglects field (behavioral-vector requirement)
        neglects_match = re.search(r"- \*\*Neglects:\s*([^*\n]+)", section)
        if neglects_match:
            persona["neglects"] = neglects_match.group(1).strip()
        else:
            persona["neglects"] = ""

        # Extract Phase Affinity field (behavioral-vector requirement)
        phase_match = re.search(r"- \*\*Phase Affinity:\s*([^*\n]+)", section)
        if phase_match:
            phase_text = phase_match.group(1).strip()
            # Convert "verification, evaluation" to ["verification", "evaluation"]
            persona["phase_affinity"] = [
                p.strip() for p in phase_text.split(",") if p.strip()
            ]
        else:
            persona["phase_affinity"] = []

        # Extract Continuation Anchor field (behavioral-vector requirement)
        anchor_match = re.search(r"- \*\*Continuation Anchor:\s*([^*\n]+)", section)
        if anchor_match:
            anchor_value = anchor_match.group(1).strip().lower()
            persona["continuation_anchor"] = anchor_value == "true"
        else:
            persona["continuation_anchor"] = False

        personas[persona_id] = persona

    return personas


def validate_behavioral_vector_fields(persona: Dict[str, Any]) -> List[str]:
    """Validate that a persona meets all behavioral-vector schema requirements.

    Returns list of error messages for any validation failures.
    """
    errors = []

    # FR-M12S1-1: All 7 behavioral-vector personas MUST be defined
    # with four mandatory vector fields and two optional affinity fields

    # Required behavioral-vector fields
    required_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]

    for field in required_fields:
        if field not in persona:
            errors.append(
                f"Persona '{persona['id']}' missing required behavioral-vector field: {field}"
            )
        else:
            value = persona[field]
            # Must be non-empty string
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"Persona '{persona['id']}' field '{field}' must be non-empty string"
                )
            # Must be >= 20 characters (schema requirement)
            elif len(value.strip()) < 20:
                errors.append(
                    f"Persona '{persona['id']}' field '{field}' must be >= 20 chars (got {len(value.strip())})"
                )

    # Optional behavioral-vector fields
    optional_fields = ["phase_affinity", "continuation_anchor"]

    for field in optional_fields:
        if field not in persona:
            errors.append(
                f"Persona '{persona['id']}' missing optional behavioral-vector field: {field}"
            )

    # Validate phase_affinity enum values (from FR-M12S1-1 schema)
    if "phase_affinity" in persona:
        phase_affinity = persona["phase_affinity"]
        valid_phases = [
            "milestone",
            "specification",
            "verification",
            "tests",
            "evaluation",
            "implementation",
        ]

        if not isinstance(phase_affinity, list):
            errors.append(
                f"Persona '{persona['id']}' phase_affinity must be array, got {type(phase_affinity)}"
            )
        else:
            for phase in phase_affinity:
                if phase not in valid_phases:
                    errors.append(
                        f"Persona '{persona['id']}' phase_affinity contains invalid value: '{phase}'"
                    )

    # Validate continuation_anchor is boolean (from FR-M12S1-1 schema)
    if "continuation_anchor" in persona:
        anchor = persona["continuation_anchor"]
        if not isinstance(anchor, bool):
            errors.append(
                f"Persona '{persona['id']}' continuation_anchor must be boolean, got {type(anchor)}"
            )

    # Validate id pattern (from FR-M12S1-1 schema)
    if "id" in persona:
        persona_id = persona["id"]
        if not re.match(r"^[a-z0-9-]+$", persona_id):
            errors.append(f"Persona '{persona_id}' id must match pattern ^[a-z0-9-]+$")

    return errors


def test_all_personas_defined():
    """Test AC-M12S1-1: All 7 behavioral-vector personas are defined.

    Validates that all 7 expected personas exist with complete behavioral-vector fields.
    """
    personas = extract_persona_vectors_from_skill()

    # Expected personas from FR-M12S1-2
    expected_personas = {
        "the-skeptic",
        "the-architect",
        "the-implementer",
        "the-auditor",
        "the-strategist",
        "the-reviewer",
        "the-analyst",
    }

    # Check we have all expected personas
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas in SKILL.md: {missing_personas}"

    # Check we don't have unexpected extra personas
    extra_personas = set(personas.keys()) - expected_personas
    assert (
        not extra_personas
    ), f"Unexpected extra personas in SKILL.md: {extra_personas}"

    # Validate each persona has all behavioral-vector fields
    all_errors = []
    for persona_id, persona in personas.items():
        errors = validate_behavioral_vector_fields(persona)
        if errors:
            all_errors.extend(errors)

    assert not all_errors, "\n".join(all_errors)

    print(
        f"✓ All {len(personas)} personas are correctly defined with behavioral-vector fields"
    )


def test_baseline_requirement():
    """Test baseline field requirement (>= 20 chars for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    baseline_violations = []
    for persona_id, persona in personas.items():
        baseline = persona.get("baseline", "")
        if len(baseline.strip()) < 20:
            baseline_violations.append(
                f"Persona '{persona_id}' baseline too short ({len(baseline.strip())} chars, minimum 20)"
            )

    assert not baseline_violations, "\n".join(baseline_violations)

    print(f"✓ All {len(personas)} personas have baseline >= 20 chars")


def test_pressure_shift_requirement():
    """Test pressure_shift field requirement (>= 20 chars for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    pressure_violations = []
    for persona_id, persona in personas.items():
        pressure = persona.get("pressure_shift", "")
        if len(pressure.strip()) < 20:
            pressure_violations.append(
                f"Persona '{persona_id}' pressure_shift too short ({len(pressure.strip())} chars, minimum 20)"
            )

    assert not pressure_violations, "\n".join(pressure_violations)

    print(f"✓ All {len(personas)} personas have pressure_shift >= 20 chars")


def test_optimizes_for_requirement():
    """Test optimizes_for field requirement (>= 20 chars for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    optimizes_violations = []
    for persona_id, persona in personas.items():
        optimizes = persona.get("optimizes_for", "")
        if len(optimizes.strip()) < 20:
            optimizes_violations.append(
                f"Persona '{persona_id}' optimizes_for too short ({len(optimizes.strip())} chars, minimum 20)"
            )

    assert not optimizes_violations, "\n".join(optimizes_violations)

    print(f"✓ All {len(personas)} personas have optimizes_for >= 20 chars")


def test_neglects_requirement():
    """Test neglects field requirement (>= 20 chars for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    neglects_violations = []
    for persona_id, persona in personas.items():
        neglects = persona.get("neglects", "")
        if len(neglects.strip()) < 20:
            neglects_violations.append(
                f"Persona '{persona_id}' neglects too short ({len(neglects.strip())} chars, minimum 20)"
            )

    assert not neglects_violations, "\n".join(neglects_violations)

    print(f"✓ All {len(personas)} personas have neglects >= 20 chars")


def test_phase_affinity_requirement():
    """Test phase_affinity field requirement (valid enum values for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    phase_violations = []
    valid_phases = [
        "milestone",
        "specification",
        "verification",
        "tests",
        "evaluation",
        "implementation",
    ]

    for persona_id, persona in personas.items():
        phase_affinity = persona.get("phase_affinity", [])

        if not isinstance(phase_affinity, list):
            phase_violations.append(
                f"Persona '{persona_id}' phase_affinity must be array, got {type(phase_affinity)}"
            )
            continue

        for phase in phase_affinity:
            if phase not in valid_phases:
                phase_violations.append(
                    f"Persona '{persona_id}' phase_affinity contains invalid value: '{phase}'"
                )

    assert not phase_violations, "\n".join(phase_violations)

    print(f"✓ All {len(personas)} personas have valid phase_affinity enum values")


def test_continuation_anchor_requirement():
    """Test continuation_anchor field requirement (boolean for all 7 personas)."""
    personas = extract_persona_vectors_from_skill()

    anchor_violations = []

    for persona_id, persona in personas.items():
        anchor = persona.get("continuation_anchor")
        if not isinstance(anchor, bool):
            anchor_violations.append(
                f"Persona '{persona_id}' continuation_anchor must be boolean, got {type(anchor)}"
            )

    # Special requirement: the-implementer MUST be continuation_anchor: true
    implementer = personas.get("the-implementer")
    if implementer and implementer.get("continuation_anchor") != True:
        anchor_violations.append(
            "Persona 'the-implementer' must have continuation_anchor: true"
        )

    # All other personas MUST have continuation_anchor: false
    for persona_id, persona in personas.items():
        if persona_id != "the-implementer":
            if persona.get("continuation_anchor") != False:
                anchor_violations.append(
                    f"Persona '{persona_id}' (non-continuity anchor) must have continuation_anchor: false"
                )

    assert not anchor_violations, "\n".join(anchor_violations)

    print(
        f"✓ All {len(personas)} personas have correct continuation_anchor boolean values"
    )


def test_schema_contract_compliance():
    """Test that all behavioral-vector fields comply with the schema contract from FR-M12S1-1."""
    personas = extract_persona_vectors_from_skill()

    schema_violations = []

    for persona_id, persona in personas.items():
        # Schema contract validation

        # 1. All four required vector fields present
        required_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]
        for field in required_fields:
            if field not in persona or not persona[field]:
                schema_violations.append(
                    f"Persona '{persona_id}' missing or empty required field: {field}"
                )

        # 2. All fields meet length requirements (>= 20 chars)
        for field in required_fields:
            if field in persona:
                value = persona[field]
                if len(str(value).strip()) < 20:
                    schema_violations.append(
                        f"Persona '{persona_id}' field '{field}' too short (min 20 chars)"
                    )

        # 3. phase_affinity enum validation
        if "phase_affinity" in persona:
            valid_phases = [
                "milestone",
                "specification",
                "verification",
                "tests",
                "evaluation",
                "implementation",
            ]
            for phase in persona["phase_affinity"]:
                if phase not in valid_phases:
                    schema_violations.append(
                        f"Persona '{persona_id}' phase_affinity invalid value: '{phase}'"
                    )

        # 4. continuation_anchor boolean validation
        if "continuation_anchor" in persona:
            if not isinstance(persona["continuation_anchor"], bool):
                schema_violations.append(
                    f"Persona '{persona_id}' continuation_anchor not boolean"
                )

    assert not schema_violations, "\n".join(schema_violations)

    print(f"✓ All {len(personas)} personas comply with schema contract from FR-M12S1-1")


if __name__ == "__main__":
    print("Running M12S1 Behavioral-Vector Requirements Tests...\n")

    try:
        test_all_personas_defined()
        print()
        test_baseline_requirement()
        print()
        test_pressure_shift_requirement()
        print()
        test_optimizes_for_requirement()
        print()
        test_neglects_requirement()
        print()
        test_phase_affinity_requirement()
        print()
        test_continuation_anchor_requirement()
        print()
        test_schema_contract_compliance()
        print()
        print("✅ All M12S1 behavioral-vector requirements tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
