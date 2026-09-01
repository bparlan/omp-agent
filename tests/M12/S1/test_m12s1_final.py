#!/usr/bin/env python3
"""
M12S1 Initial Failure Test - Behavioral-Vector Persona Overhaul

This test validates the behavioral-vector persona requirements from M12S1.
The test should pass when the manage-development skill implementation
successfully implements the persona overhaul.

Tests all 6 behavioral-vector schema fields from FR-M12S1-1:
- baseline (>= 20 chars, present)
- pressure_shift (>= 20 chars, present)
- optimizes_for (>= 20 chars, present)
- neglects (>= 20 chars, present)
- phase_affinity (array, enum validation)
- continuation_anchor (boolean)

Also validates:
- All 7 personas present
- Correct persona IDs (pattern ^[a-z0-9-]+$)
- continuation_anchor: true only for the-implementer
- All other personas have continuation_anchor: false
- Valid phase_affinity enum values

Requirement: FR-M12S1-1, VR-M12S1-1, AC-M12S1-1
"""

import re
from pathlib import Path
from typing import Dict, Any, List

def extract_persona_vectors_from_skill():
    """Extract persona vectors from manage-development SKILL.md.

    Returns a dictionary of persona data with behavioral-vector fields.
    This parser correctly handles the actual format in SKILL.md:
    - **Label:** Value (with dash, colon, two asterisks)
    """
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Pattern to match persona sections
    # Format: **Persona 1: the-skeptic** followed by field definitions
    persona_pattern = r'\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)'

    personas = {}

    for match in re.finditer(persona_pattern, content):
        persona_id = match.group(1)
        section = match.group(2)

        # Parse section using string operations (more reliable)
        lines = section.strip().split('\n')

        persona = {'id': persona_id}

        # Extract fields from each line
        for line in lines:
            line = line.strip()

            # Parse Label field
            if line.startswith('- **Label:**'):
                persona['label'] = line.split('**Label:**', 1)[1].strip()

            # Parse Baseline field
            elif line.startswith('- **Baseline:**'):
                persona['baseline'] = line.split('**Baseline:**', 1)[1].strip()

            # Parse Pressure Shift field
            elif line.startswith('- **Pressure Shift:**'):
                persona['pressure_shift'] = line.split('**Pressure Shift:**', 1)[1].strip()

            # Parse Optimizes For field
            elif line.startswith('- **Optimizes For:**'):
                persona['optimizes_for'] = line.split('**Optimizes For:**', 1)[1].strip()

            # Parse Neglects field
            elif line.startswith('- **Neglects:**'):
                persona['neglects'] = line.split('**Neglects:**', 1)[1].strip()

            # Parse Phase Affinity field
            elif line.startswith('- **Phase Affinity:**'):
                phase_text = line.split('**Phase Affinity:**', 1)[1].strip()
                persona['phase_affinity'] = [p.strip() for p in phase_text.split(',')]

            # Parse Continuation Anchor field
            elif line.startswith('- **Continuation Anchor:**'):
                anchor_text = line.split('**Continuation Anchor:**', 1)[1].strip().lower()
                persona['continuation_anchor'] = anchor_text == 'true'

        personas[persona_id] = persona

    return personas

def test_all_personas_present():
    """Test AC-M12S1-1: All 7 behavioral-vector personas are defined."""
    personas = extract_persona_vectors_from_skill()

    # Expected 7 personas from FR-M12S1-2
    expected_personas = {
        'the-skeptic', 'the-architect', 'the-implementer',
        'the-auditor', 'the-strategist', 'the-reviewer', 'the-analyst'
    }

    # Check we have all expected personas
    missing_personas = expected_personas - set(personas.keys())
    assert not missing_personas, f"Missing personas in SKILL.md: {missing_personas}"

    # Check we don't have unexpected extra personas
    extra_personas = set(personas.keys()) - expected_personas
    assert not extra_personas, f"Unexpected extra personas in SKILL.md: {extra_personas}"

    # Requirement: Each persona must have all behavioral-vector fields
    required_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for',
                      'neglects', 'phase_affinity', 'continuation_anchor']

    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert not missing_fields, \
            f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"

    print(f"✓ All {len(personas)} personas have all 6 behavioral-vector fields")

def test_field_content_requirements():
    """Test that all behavioral-vector fields meet content requirements."""
    personas = extract_persona_vectors_from_skill()

    # Requirement: All required string fields must be >= 20 characters
    required_string_fields = ['baseline', 'pressure_shift', 'optimizes_for', 'neglects']

    for persona_id, persona in personas.items():
        for field in required_string_fields:
            value = persona.get(field, '')
            assert len(value.strip()) >= 20, \
                f"Persona '{persona_id}' field '{field}' too short "
                f"({len(value.strip())} chars, minimum 20)"

    print(f"✓ All {len(personas)} personas have string fields >= 20 chars")

    # Requirement: phase_affinity must be array with valid enum values
    valid_phases = ['milestone', 'specification', 'verification', 'tests', 'evaluation', 'implementation']

    for persona_id, persona in personas.items():
        phase_affinity = persona.get('phase_affinity', [])
        assert isinstance(phase_affinity, list), \
            f"Persona '{persona_id}' phase_affinity must be array, got {type(phase_affinity)}"

        for phase in phase_affinity:
            assert phase in valid_phases, \
                f"Persona '{persona_id}' phase_affinity contains invalid value: '{phase}'"

    print(f"✓ All {len(personas)} personas have valid phase_affinity enum values")

    # Requirement: continuation_anchor must be boolean
    for persona_id, persona in personas.items():
        anchor = persona.get('continuation_anchor')
        assert isinstance(anchor, bool), \
            f"Persona '{persona_id}' continuation_anchor must be boolean, got {type(anchor)}"

    # Requirement: the-implementer must have continuation_anchor: true
    implementer = personas.get('the-implementer')
    assert implementer is not None, "Persona 'the-implementer' not found"
    assert implementer['continuation_anchor'] == True, \
        "Persona 'the-implementer' must have continuation_anchor: true"

    # Requirement: All other personas must have continuation_anchor: false
    for persona_id, persona in personas.items():
        if persona_id != 'the-implementer':
            assert persona['continuation_anchor'] == False, \
                f"Persona '{persona_id}' (non-continuity anchor) must have continuation_anchor: false"

    print(f"✓ All {len(personas)} personas have correct continuation_anchor values")

    # Requirement: All persona IDs must match pattern ^[a-z0-9-]+$
    for persona_id in personas.keys():
        assert re.match(r'^[a-z0-9-]+$', persona_id), \
            f"Persona ID '{persona_id}' does not match pattern ^[a-z0-9-]+$"

    print(f"✓ All {len(personas)} persona IDs comply with required pattern")

if __name__ == "__main__":
    print("=" * 80)
    print("M12S1 Initial Failure Test - Behavioral-Vector Persona Overhaul")
    print("=" * 80)
    print("\nThis test validates the behavioral-vector persona requirements from M12S1.")
    print("The test should pass when the manage-development skill implementation")
    print("successfully implements the persona overhaul.\n")
    print("Tests all 6 behavioral-vector schema fields from FR-M12S1-1:")
    print("  - baseline (>= 20 chars, present)")
    print("  - pressure_shift (>= 20 chars, present)")
    print("  - optimizes_for (>= 20 chars, present)")
    print("  - neglects (>= 20 chars, present)")
    print("  - phase_affinity (array, enum validation)")
    print("  - continuation_anchor (boolean)\n")

    try:
        test_all_personas_present()
        print()
        test_field_content_requirements()
        print()
        print("=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("\nThis indicates that the manage-development skill implementation")
        print("successfully implements the M12S1 behavioral-vector persona")
        print("overhaul as specified in the requirements.\n")
        print("=" * 80 + "\n")

    except AssertionError as e:
        print("\n" + "=" * 80)
        print(f"❌ TEST FAILED: {e}")
        print("\nThis is the expected initial failure.")
        print("The tests confirm that the manage-development SKILL.md")
        print("does not yet have the complete behavioral-vector persona")
        print("definitions required by M12S1.\n")
        print("=" * 80 + "\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
