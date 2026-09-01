#!/usr/bin/env python3
"""
M12S1 Initial Failure Test - Behavioral-Vector Persona Overhaul

This test MUST FAIL initially because the current manage-development
SKILL.md does not implement the complete behavioral-vector persona
dover as specified in M12S1.

This test validates that the behavioral-vector schema fields are properly
extracted and meet the requirements from FR-M12S1-1.

Requirements to test:
- All 7 personas present
- All 6 behavioral-vector fields per persona
- Field content meets requirements (>= 20 chars for string fields)
- Valid phase_affinity enum values
- Correct continuation_anchor boolean values
"""

import re
from pathlib import Path
from typing import Dict, Any

def extract_persona_vectors_correct():
    """Extract persona vectors from SKILL.md using correct parsing logic."""
    skill_path = Path("skills/manage-development/SKILL.md")
    content = skill_path.read_text()

    # Pattern to match persona sections
    persona_pattern = r'\*\*Persona \d+:\s*([a-z0-9-]+)\*\*([\s\S]*?)(?=\n---|\n\*\*Persona|\Z)'

    personas = {}

    for match in re.finditer(persona_pattern, content):
        persona_id = match.group(1)
        section = match.group(2)

        # Parse section using string splitting (more reliable than regex)
        lines = section.strip().split('\n')

        persona = {'id': persona_id}

        # Parse each field line
        for line in lines:
            line = line.strip()

            # Extract fields using string operations
            if line.startswith('- **Label:**'):
                persona['label'] = line.split('**Label:**', 1)[1].strip()
            elif line.startswith('- **Baseline:**'):
                persona['baseline'] = line.split('**Baseline:**', 1)[1].strip()
            elif line.startswith('- **Pressure Shift:**'):
                persona['pressure_shift'] = line.split('**Pressure Shift:**', 1)[1].strip()
            elif line.startswith('- **Optimizes For:**'):
                persona['optimizes_for'] = line.split('**Optimizes For:**', 1)[1].strip()
            elif line.startswith('- **Neglects:**'):
                persona['neglects'] = line.split('**Neglects:**', 1)[1].strip()
            elif line.startswith('- **Phase Affinity:**'):
                phase_text = line.split('**Phase Affinity:**', 1)[1].strip()
                persona['phase_affinity'] = [p.strip() for p in phase_text.split(',')]
            elif line.startswith('- **Continuation Anchor:**'):
                anchor_text = line.split('**Continuation Anchor:**', 1)[1].strip().lower()
                persona['continuation_anchor'] = anchor_text == 'true'

        personas[persona_id] = persona

    return personas

def test_behavioral_vector_personas_complete():
    """Test that all behavioral-vector personas meet M12S1 requirements."""
    personas = extract_persona_vectors_correct()

    # Requirement 1: All 7 personas must be present
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

    # Requirement 2: Each persona must have all behavioral-vector fields
    required_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for',
                      'neglects', 'phase_affinity', 'continuation_anchor']

    for persona_id, persona in personas.items():
        missing_fields = [field for field in required_fields if field not in persona]
        assert not missing_fields, \
            f"Persona '{persona_id}' missing behavioral-vector fields: {missing_fields}"

    print(f"✓ All {len(personas)} behavioral-vector personas are complete")

def test_field_content_requirements():
    """Test that all behavioral-vector fields meet content requirements."""
    personas = extract_persona_vectors_correct()

    # Requirement: All string fields must be >= 20 characters
    string_fields = ['label', 'baseline', 'pressure_shift', 'optimizes_for', 'neglects']

    for persona_id, persona in personas.items():
        for field in string_fields:
            value = persona.get(field, '')
            assert len(value.strip()) >= 20, \
                f"Persona '{persona_id}' field '{field}' too short "
                f"({len(value.strip())} chars, minimum 20)"

    print(f"✓ All {len(personas)} personas have string fields >= 20 chars")

    # Requirement: phase_affinity must be valid enum values
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
    print("\nThis test suite validates that the manage-development SKILL.md")
    print("implementation satisfies all M12S1 behavioral-vector persona")
    print("requirements.\n")

    try:
        test_behavioral_vector_personas_complete()
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
