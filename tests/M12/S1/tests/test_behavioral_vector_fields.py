#!/usr/bin/env python3
"""
Test behavioral-vector fields validation for M12S1 Persona Overhaul.

This test suite validates the six behavioral-vector schema fields:
- baseline
- pressure_shift
- optimizes_for
- neglects
- phase_affinity
- continuation_anchor

Tests MUST fail initially because the current implementation doesn't fully
enforce these behavioral-vector schema requirements.

Requirements: FR-M12S1-1 (Schema), VR-M12S1-1 (Validation), AC-M12S1-1 (Completeness)
"""

import re
from pathlib import Path
from typing import Dict, Any, List


def extract_persona_vectors_from_skill(skill_content: str) -> Dict[str, Dict[str, Any]]:
    """Extract persona vectors from manage-development SKILL.md.

    Parses the actual persona definitions in the skill file and returns
    behavioral-vector data for validation.
    """
    personas = {}

    # Pattern to match persona sections in the skill file
    # Matches: **Persona 1: the-skeptic** with its associated fields
    persona_sections = re.findall(
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*\s*\n(?:.*?)(?=\n---|\*\*Persona \d+:|\Z)",
        skill_content,
        re.DOTALL,
    )

    for section in persona_sections:
        # Extract persona ID from first line
        id_match = re.search(r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*", section)
        if not id_match:
            continue

        persona_id = id_match.group(1)

        # Extract all behavioral-vector fields
        persona_data = {"id": persona_id}

        # Label field (required)
        label_match = re.search(r"- \*\*Label:\*\*\s*([^*\n]+)", section)
        persona_data["label"] = label_match.group(1).strip() if label_match else ""

        # Baseline field (behavioral-vector schema requirement)
        baseline_match = re.search(r"- \*\*Baseline:\*\* ([^*\n]+)", section)
        persona_data["baseline"] = (
            baseline_match.group(1).strip() if baseline_match else ""
        )

        # Pressure Shift field (behavioral-vector schema requirement)
        pressure_match = re.search(r"- \*\*Pressure Shift:\*\* ([^*\n]+)", section)
        persona_data["pressure_shift"] = (
            pressure_match.group(1).strip() if pressure_match else ""
        )

        # Optimizes For field (behavioral-vector schema requirement)
        optimizes_match = re.search(r"- \*\*Optimizes For:\*\* ([^*\n]+)", section)
        persona_data["optimizes_for"] = (
            optimizes_match.group(1).strip() if optimizes_match else ""
        )

        # Neglects field (behavioral-vector schema requirement)
        neglects_match = re.search(r"- \*\*Neglects:\*\* ([^*\n]+)", section)
        persona_data["neglects"] = (
            neglects_match.group(1).strip() if neglects_match else ""
        )

        # Phase Affinity field (behavioral-vector schema requirement)
        phase_match = re.search(r"- \*\*Phase Affinity:\*\* ([^*\n]+)", section)
        if phase_match:
            phase_text = phase_match.group(1).strip()
            # Convert comma-separated list to array
            persona_data["phase_affinity"] = [p.strip() for p in phase_text.split(",")]
        else:
            persona_data["phase_affinity"] = []

        # Continuation Anchor field (behavioral-vector schema requirement)
        anchor_match = re.search(r"- \*\*Continuation Anchor:\*\* ([^*\n]+)", section)
        persona_data["continuation_anchor"] = (
            anchor_match.group(1).strip().lower() == "true" if anchor_match else False
        )

        personas[persona_id] = persona_data

    return personas


def validate_field_requirements(persona: Dict[str, Any]) -> List[str]:
    """Validate that a persona meets all behavioral-vector field requirements.

    Returns list of error messages for any validation failures.
    """
    errors = []

    # Requirement 1: All six behavioral-vector fields must be present
    required_fields = [
        "baseline",
        "pressure_shift",
        "optimizes_for",
        "neglects",
        "phase_affinity",
        "continuation_anchor",
    ]

    for field in required_fields:
        if field not in persona:
            errors.append(f"Missing behavioral-vector field: {field}")
        elif persona[field] is None:
            errors.append(f"Behavioral-vector field '{field}' is None")

    # Requirement 2: String fields must be non-empty and >= 20 characters
    string_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]
    for field in string_fields:
        value = persona.get(field, "")
        if not isinstance(value, str):
            errors.append(f"Field '{field}' must be string, got {type(value)}")
        elif not value.strip():
            errors.append(f"Field '{field}' must be non-empty")
        elif len(value.strip()) < 20:
            errors.append(
                f"Field '{field}' must be >= 20 chars (got {len(value.strip())})"
            )

    # Requirement 3: phase_affinity must be array with valid enum values
    valid_phases = [
        "milestone",
        "specification",
        "verification",
        "tests",
        "evaluation",
        "implementation",
    ]
    phase_affinity = persona.get("phase_affinity", [])
    if not isinstance(phase_affinity, list):
        errors.append(f"phase_affinity must be array, got {type(phase_affinity)}")
    else:
        for phase in phase_affinity:
            if phase not in valid_phases:
                errors.append(
                    f"Invalid phase_affinity value: '{phase}' (valid: {valid_phases})"
                )

    # Requirement 4: continuation_anchor must be boolean
    continuation_anchor = persona.get("continuation_anchor")
    if not isinstance(continuation_anchor, bool):
        errors.append(
            f"continuation_anchor must be boolean, got {continuation_anchor} (type: {type(continuation_anchor)})"
        )

    # Requirement 5: id must match pattern ^[a-z0-9-]+$
    persona_id = persona.get("id", "")
    if not re.match(r"^[a-z0-9-]+$", persona_id):
        errors.append(f"id '{persona_id}' must match pattern ^[a-z0-9-]+$")

    return errors


def test_behavioral_vector_fields_present():
    """Test that all six behavioral-vector schema fields are present in all personas.

    Validates that each persona has all the behavioral-vector fields required by FR-M12S1-1.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    skill_content = skill_path.read_text()

    personas = extract_persona_vectors_from_skill(skill_content)

    # Expected number of personas from FR-M12S1-2
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

    # Check each persona has all behavioral-vector fields
    all_errors = []
    for persona_id, persona in personas.items():
        errors = validate_field_requirements(persona)
        if errors:
            all_errors.append(
                f"Persona '{persona_id}' validation errors:\n"
                + "\n".join(f"  - {e}" for e in errors)
            )

    assert not all_errors, "\n".join(all_errors)

    print(
        f"✓ Behavioral-vector fields present validation passed for {len(personas)} personas"
    )


def test_field_data_quality():
    """Test that behavioral-vector field data meets quality standards.

    Validates that all behavioral-vector fields contain meaningful, properly-formatted data.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    skill_content = skill_path.read_text()

    personas = extract_persona_vectors_from_skill(skill_content)

    quality_issues = []

    for persona_id, persona in personas.items():
        # Check that string fields contain substantive content (not just placeholders)
        string_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]
        for field in string_fields:
            value = persona.get(field, "")
            if not value or len(value.strip()) < 50:
                quality_issues.append(
                    f"Persona '{persona_id}' field '{field}' appears too short ({len(value)} chars)"
                )

        # Check that phase_affinity has appropriate content (at least one phase for most personas)
        if not persona.get("phase_affinity"):
            # Only the-analyst might have no phase affinity, but others should have at least one
            if persona_id != "the-analyst":
                quality_issues.append(
                    f"Persona '{persona_id}' has empty phase_affinity array"
                )

        # Check that continuation_anchor has meaningful value
        if persona_id == "the-implementer":
            assert (
                persona.get("continuation_anchor") == True
            ), "Persona 'the-implementer' must have continuation_anchor: true"
        else:
            assert (
                persona.get("continuation_anchor") == False
            ), f"Persona '{persona_id}' should have continuation_anchor: false"

    assert not quality_issues, "\n".join(quality_issues)

    print("✓ Behavioral-vector field data quality validation passed")


def test_field_contract_compliance():
    """Test that behavioral-vector fields comply with the schema contract from FR-M12S1-1.

    Validates the exact schema contract defined in the specification.
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    skill_content = skill_path.read_text()

    personas = extract_persona_vectors_from_skill(skill_content)

    contract_violations = []

    for persona_id, persona in personas.items():
        # Schema contract validation per FR-M12S1-1

        # 1. id field pattern
        if not re.match(r"^[a-z0-9-]+$", persona["id"]):
            contract_violations.append(
                f"Persona '{persona_id}': id '{persona['id']}' doesn't match ^[a-z0-9-]+$"
            )

        # 2. All four vector fields present and >= 20 chars
        vector_fields = ["baseline", "pressure_shift", "optimizes_for", "neglects"]
        for field in vector_fields:
            value = persona.get(field, "")
            if len(value) < 20:
                contract_violations.append(
                    f"Persona '{persona_id}': {field} too short (min 20 chars, got {len(value)})"
                )

        # 3. phase_affinity enum values
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
                contract_violations.append(
                    f"Persona '{persona_id}': phase_affinity contains invalid value '{phase}'"
                )

        # 4. continuation_anchor type
        if not isinstance(persona.get("continuation_anchor"), bool):
            contract_violations.append(
                f"Persona '{persona_id}': continuation_anchor must be boolean, got {type(persona.get('continuation_anchor'))}"
            )

    assert not contract_violations, "\n".join(contract_violations)

    print("✓ Behavioral-vector field contract compliance validation passed")


if __name__ == "__main__":
    print("Running M12S1 Behavioral-Vector Fields Validation Tests...\n")

    try:
        test_behavioral_vector_fields_present()
        print()
        test_field_data_quality()
        print()
        test_field_contract_compliance()
        print()
        print("✅ All M12S1 behavioral-vector fields validation tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
