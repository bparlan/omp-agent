#!/usr/bin/env python3
"""
Initial M12S1 TDD baseline test for behavioral-vector persona overhaul.

This test MUST fail initially because the current manage-development SKILL.md
has incomplete persona vector definitions. The test validates the exact
behavioral-vector schema requirements from FR-M12S1-1.

Tests validate all 6 behavioral-vector fields:
- baseline (>= 20 chars, present)
- pressure_shift (>= 20 chars, present)
- optimizes_for (>= 20 chars, present)
- neglects (>= 20 chars, present)
- phase_affinity (array, enum validation)
- continuation_anchor (boolean)

This test will serve as the fail-first baseline that implementation must
pass to complete the M12S1 Persona Overhaul.

Requirement: FR-M12S1-1 (Behavioral-Vector Persona Definition Schema)
             VR-M12S1-1 (Schema Validation)
             AC-M12S1-1 (Persona Vector Completeness)
"""

import re
from pathlib import Path


def extract_persona_vectors_from_skill():
    """Extract all persona vectors from the manage-development SKILL.md file.

    Returns a dictionary of persona data with behavioral-vector fields.
    This parser correctly handles the actual format in SKILL.md:
    **Field:** Value (with colon and two asterisks)
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Pattern to match persona sections
    # Format: **Persona 1: the-skeptic** followed by field definitions
    persona_pattern = (
        r"\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)"
    )

    personas = {}

    for match in re.finditer(persona_pattern, content):
        persona_id = match.group(1)
        section = match.group(2)

        persona = {"id": persona_id}

        # Extract all behavioral-vector fields
        # The actual format in SKILL.md uses: **Field:** Value
        # with two asterisks, not single asterisk

        # Extract Label field
        label_match = re.search(r"- \*\*Label:\s*([^*\n]+)", section)
        if label_match:
            persona["label"] = label_match.group(1).strip()

        # Extract Baseline field (behavioral-vector requirement)
        baseline_match = re.search(r"- \*\*Baseline:\s*([^*\n]+)", section)
        if baseline_match:
            persona["baseline"] = baseline_match.group(1).strip()

        # Extract Pressure Shift field (behavioral-vector requirement)
        pressure_match = re.search(r"- \*\*Pressure Shift:\s*([^*\n]+)", section)
        if pressure_match:
            persona["pressure_shift"] = pressure_match.group(1).strip()

        # Extract Optimizes For field (behavioral-vector requirement)
        optimizes_match = re.search(r"- \*\*Optimizes For:\s*([^*\n]+)", section)
        if optimizes_match:
            persona["optimizes_for"] = optimizes_match.group(1).strip()

        # Extract Neglects field (behavioral-vector requirement)
        neglects_match = re.search(r"- \*\*Neglects:\s*([^*\n]+)", section)
        if neglects_match:
            persona["neglects"] = neglects_match.group(1).strip()

        # Extract Phase Affinity field (behavioral-vector requirement)
        phase_match = re.search(r"- \*\*Phase Affinity:\s*([^*\n]+)", section)
        if phase_match:
            phase_text = phase_match.group(1).strip()
            # Convert comma-separated list to array
            persona["phase_affinity"] = [p.strip() for p in phase_text.split(",")]

        # Extract Continuation Anchor field (behavioral-vector requirement)
        anchor_match = re.search(r"- \*\*Continuation Anchor:\s*([^*\n]+)", section)
        if anchor_match:
            anchor_value = anchor_match.group(1).strip().lower()
            persona["continuation_anchor"] = anchor_value == "true"

        personas[persona_id] = persona

    return personas


def test_persona_completeness_requirement():
    """Test AC-M12S1-1: All 7 behavioral-vector personas are defined.

    This is the core requirement of the M12S1 Persona Overhaul.
    All 7 personas must be present with complete behavioral-vector fields.
    """
    # Load actual persona definitions from SKILL.md
    personas = extract_persona_vectors_from_skill()

    # Expected 7 personas from FR-M12S1-2
    expected_personas = {
        "the-skeptic",
        "the-architect",
        "the-implementer",
        "the-auditor",
        "the-strategist",
        "the-reviewer",
        "the-analyst",
    }

    # Requirement: All 7 personas MUST be present
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas in SKILL.md: {missing_personas}"

    # Requirement: No extra personas beyond the 7 expected
    extra_personas = set(personas.keys()) - expected_personas
    assert (
        not extra_personas
    ), f"Unexpected extra personas in SKILL.md: {extra_personas}"

    # Requirement: Each persona must have all 6 behavioral-vector fields
    required_fields = [
        "label",
        "baseline",
        "pressure_shift",
        "optimizes_for",
        "neglects",
        "phase_affinity",
        "continuation_anchor",
    ]

    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert (
            not missing_fields
        ), f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"

        # Requirement: All string fields must be non-empty
        string_fields = [
            "label",
            "baseline",
            "pressure_shift",
            "optimizes_for",
            "neglects",
        ]
        for field in string_fields:
            value = persona[field]
            assert (
                value and len(value.strip()) > 0
            ), f"Persona '{persona_id}' field '{field}' is empty or whitespace"

    print(f"✓ All {len(personas)} personas are complete with behavioral-vector fields")


def test_baseline_field_requirement():
    """Test baseline field meets schema requirements (>= 20 chars)."""
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


def test_pressure_shift_field_requirement():
    """Test pressure_shift field meets schema requirements (>= 20 chars)."""
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


def test_optimizes_for_field_requirement():
    """Test optimizes_for field meets schema requirements (>= 20 chars)."""
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


def test_neglects_field_requirement():
    """Test neglects field meets schema requirements (>= 20 chars)."""
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


def test_phase_affinity_field_requirement():
    """Test phase_affinity field meets schema requirements (valid enum values)."""
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


def test_continuation_anchor_field_requirement():
    """Test continuation_anchor field meets schema requirements (boolean)."""
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


def test_id_pattern_requirement():
    """Test that all persona IDs follow the required pattern (^[a-z0-9-]+$)."""
    personas = extract_persona_vectors_from_skill()

    pattern_violations = []
    for persona_id in personas.keys():
        if not re.match(r"^[a-z0-9-]+$", persona_id):
            pattern_violations.append(
                f"Persona ID '{persona_id}' does not match pattern ^[a-z0-9-]+$"
            )

    assert not pattern_violations, "\n".join(pattern_violations)

    print(f"✓ All {len(personas)} persona IDs comply with required pattern")


if __name__ == "__main__":
    print("Running M12S1 Initial Failure Test Suite...\n")
    print("This test suite MUST FAIL initially because the manage-development")
    print("SKILL.md does not yet implement the complete behavioral-vector")
    print("persona overhaul as specified in M12S1.\n")

    try:
        test_persona_completeness_requirement()
        print()
        test_baseline_field_requirement()
        print()
        test_pressure_shift_field_requirement()
        print()
        test_optimizes_for_field_requirement()
        print()
        test_neglects_field_requirement()
        print()
        test_phase_affinity_field_requirement()
        print()
        test_continuation_anchor_field_requirement()
        print()
        test_id_pattern_requirement()
        print()
        print("✅ ALL TESTS PASSED!")
        print("\nThis indicates that the manage-development skill implementation")
        print("successfully implements the M12S1 behavioral-vector persona")
        print("overhaul as specified in the requirements.\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\nThis is the expected initial failure. The tests confirm that")
        print("the manage-development SKILL.md does not yet have the complete")
        print("behavioral-vector persona definitions required by M12S1.\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
